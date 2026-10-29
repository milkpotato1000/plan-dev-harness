"""Real linked worktrees, configurable branches and evidence-backed card guards."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1]

class NumberedQueueTests(unittest.TestCase):
    def run_cmd(self, *args, cwd=None, ok=True):
        result = subprocess.run(args, cwd=cwd or self.plan, text=True, capture_output=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def git(self, *args, cwd=None, ok=True):
        return self.run_cmd('git', *args, cwd=cwd, ok=ok).stdout.strip()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='harness-worktrees-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.plan = self.root / 'project-plan'
        self.dev = self.root / 'project-dev'
        self.git('init', '-b', 'design', str(self.plan), cwd=self.root)
        for key,value in [('user.name','Harness test'),('user.email','test@example.invalid'),('commit.gpgsign','false'),('core.hooksPath','.githooks')]:
            self.git('config',key,value)
        self.run_cmd('python3', str(SKILL/'scripts/install_harness.py'), '--repo',str(self.plan),
                     '--plan-branch','design','--dev-branch','develop','--release-branch','release',
                     '--protect','specs','--apply')
        # Hooks are only activated after the baseline exists, like the setup workflow.
        self.git('-c','core.hooksPath=/dev/null','add','.')
        self.git('-c','core.hooksPath=/dev/null','commit','-m','Harness baseline')
        self.base = self.git('rev-parse','HEAD')
        self.git('branch','release')
        self.git('worktree','add','-b','develop',str(self.dev),self.base)
        self.adopt(self.base)
        self.run_cmd('python3','scripts/contract_guard.py','install',cwd=self.dev)

    def adopt(self, sha):
        self.run_cmd('python3','scripts/contract_guard.py','adopt',sha,'--review-reference','Test scope approval',cwd=self.dev)
        self.git('add','.harness/adopted-plan.json',cwd=self.dev)
        self.git('commit','-m','Adopt planning baseline',cwd=self.dev)

    def queue(self, cwd=None, ok=True):
        out=self.run_cmd('python3','scripts/work_queue.py','--owner','all','--json',cwd=cwd,ok=ok)
        return json.loads(out.stdout) if ok else out

    def card(self):
        path=Path('docs/planning/plans/P001.md')
        text=(self.plan/'docs/planning/plans/_TEMPLATE.md').read_text()
        text=text.replace('> 준비: 초안','> 준비: 준비 완료').replace('> 승인 근거: 미확정','> 승인 근거: Fixture authorization')
        (self.plan/path).write_text(text)
        self.git('add',str(path));self.git('commit','-m','Prepare P001')
        sha=self.git('rev-parse','HEAD')
        self.git('merge','--no-commit','design',cwd=self.dev)
        self.adopt(sha)
        return path,text

    def test_empty_queue_and_shared_worktree_repository(self):
        self.assertEqual(self.queue()['tasks'],[])
        self.assertEqual(self.queue(self.dev)['tasks'],[])
        common1=self.git('rev-parse','--path-format=absolute','--git-common-dir')
        common2=self.git('rev-parse','--path-format=absolute','--git-common-dir',cwd=self.dev)
        self.assertEqual(common1,common2)
        self.assertEqual(self.git('config','--get','core.hooksPath',cwd=self.dev),'.githooks')
        self.assertFalse((self.plan/'docs/planning/work-queue.json').exists())

    def test_dev_completion_visible_without_merge_back(self):
        path,text=self.card()
        self.assertEqual(self.queue(self.dev)['next']['dev'],'P001')
        finished=text.replace('> 실행: 미착수','> 실행: 완료').replace('- [ ] C','- [x] C')
        log=''.join(f'- 2026-09-16T18:00:00+09:00 | C{i} | PASS | docs/verification/p001.md | Expected equals actual.\n' for i in (1,2,3))
        (self.dev/path).write_text(finished.replace('<!-- EXECUTION:END -->',log+'<!-- EXECUTION:END -->'))
        evidence=self.dev/'docs/verification/p001.md'; evidence.parent.mkdir(parents=True);evidence.write_text('Verified independently.\n')
        self.git('add',str(path),'docs/verification/p001.md',cwd=self.dev)
        self.git('commit','-m','Complete P001',cwd=self.dev)
        row=self.queue()['tasks'][0]
        self.assertEqual((row['state'],row['checked']),('DONE',3))
        # plan file remains untouched, only the query overlays committed progress.
        self.assertIn('> 실행: 미착수',(self.plan/path).read_text())
        revised=text.replace('기대 동작과 실제 결과가 일치한다.','새 요구사항을 검증한다.')
        (self.plan/path).write_text(revised)
        row=self.queue()['tasks'][0]
        self.assertEqual((row['state'],row['checked']),('READY',0))

    def test_no_false_completion_or_criteria_changes(self):
        path,text=self.card()
        node=self.dev/path
        node.write_text(text.replace('- [ ] C1:','- [x] C1:'))
        self.git('add',str(path),cwd=self.dev)
        self.git('commit','-m','Invent completion',cwd=self.dev,ok=False)
        node.write_text(text.replace('기대 동작과 실제 결과가 일치한다.','Skip required verification.'))
        self.git('add',str(path),cwd=self.dev)
        self.git('commit','-m','Change criterion',cwd=self.dev,ok=False)
        node.write_text(text);self.git('add',str(path),cwd=self.dev)
        self.run_cmd('python3','scripts/contract_guard.py','check','--target','index',cwd=self.dev)

    def test_release_worktree_has_shared_guard_and_rejects_direct_commit(self):
        release = self.root / 'project'
        self.git('worktree','add',str(release),'release')
        self.assertTrue((release/'.githooks/pre-commit').exists())
        self.assertEqual(self.git('config','--get','core.hooksPath',cwd=release),'.githooks')
        (release/'direct.txt').write_text('Unpromoted work.')
        self.git('add','direct.txt',cwd=release)
        self.git('commit','-m','Direct release work',cwd=release,ok=False)

    def test_draft_and_dependency_do_not_auto_approve(self):
        path,text=self.card()
        second=text.replace('# P001','# P002').replace('> 선행: 없음','> 선행: P001')
        (self.plan/path.with_name('P002.md')).write_text(second)
        rows={x['id']:x for x in self.queue()['tasks']}
        self.assertEqual(rows['P002']['state'],'WAITING')
        (self.plan/path.with_name('P002.md')).write_text(second.replace('> 준비: 준비 완료','> 준비: 초안'))
        rows={x['id']:x for x in self.queue()['tasks']}
        self.assertEqual(rows['P002']['state'],'DRAFT')

    def test_committed_logs_append_only_and_failure_invalidates_pass(self):
        path,text=self.card()
        log='- 2026-09-16T18:00:00+09:00 | C1 | PASS | docs/verification/p001.md | Verified.\n'
        active=text.replace('> 실행: 미착수','> 실행: 진행 중').replace('- [ ] C1:','- [x] C1:').replace('<!-- EXECUTION:END -->',log+'<!-- EXECUTION:END -->')
        (self.dev/path).write_text(active)
        e=self.dev/'docs/verification/p001.md';e.parent.mkdir(parents=True);e.write_text('Expected equals actual.')
        self.git('add',str(path),str(e.relative_to(self.dev)),cwd=self.dev);self.git('commit','-m','C1 passes',cwd=self.dev)
        (self.dev/path).write_text(active.replace('Verified.','Edited history.'))
        self.git('add',str(path),cwd=self.dev);self.git('commit','-m','Rewrite log',cwd=self.dev,ok=False)
        fail='- 2026-09-16T18:10:00+09:00 | C1 | FAIL | docs/verification/p001.md | Regression.\n'
        (self.dev/path).write_text(active.replace('<!-- EXECUTION:END -->',fail+'<!-- EXECUTION:END -->'))
        self.git('add',str(path),cwd=self.dev);self.git('commit','-m','Keep failed check',cwd=self.dev,ok=False)

if __name__ == '__main__':
    unittest.main()
