"""Real Git workflows, scoped stops, snapshot guards and recorded handoffs."""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import unittest

import test_numbered_queue as fixtures

BASE = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.NumberedQueueTests()
        self.f.setUp()
        self.addCleanup(self.f.doCleanups)
        self.plan, self.dev, self.root = self.f.plan, self.f.dev, self.f.root
        self.f.card()
        template = (self.plan/'docs/planning/plans/P001.md').read_text()
        for name in ('P002', 'P003'):
            text = template.replace('P001', name)
            if name == 'P003': text = text.replace('> 선행: 없음', '> 선행: P001')
            (self.plan/('docs/planning/plans/'+name+'.md')).write_text(text)
        self.commit_plan('Add independent and dependent cards')
        self.adopt()

    def command(self, *args, role='dev', ok=True):
        return self.f.run_cmd(sys.executable, 'scripts/workflow_control.py', *args,
                              cwd=self.plan if role == 'plan' else self.dev, ok=ok)

    def commit_plan(self, message):
        self.f.git('add', 'docs', cwd=self.plan)
        self.f.git('commit', '-m', message, cwd=self.plan)
        return self.f.git('rev-parse', 'HEAD', cwd=self.plan)

    def commit_dev(self, message='Control checkpoint'):
        self.f.git('add', 'docs', cwd=self.dev)
        self.f.git('commit', '-m', message, cwd=self.dev)

    def adopt(self):
        sha=self.f.git('rev-parse','HEAD',cwd=self.plan)
        self.f.git('merge','--no-commit','design',cwd=self.dev)
        self.f.adopt(sha)
        return sha

    def decision(self):
        question=self.root/'question.txt';question.write_text('Choose the expected behavior and record its impact.')
        self.command('decision','--task','P001','--question-file',str(question))
        self.commit_dev()
        return str(next((self.dev/'docs/feedback/dev').glob('P001-decision-*.md')).relative_to(self.dev))

    def classify(self, path, *tasks):
        self.command('classify',path,'--scope','tasks','--tasks',*(tasks or ('P001',)),
                     '--reason','Independent work does not use this decision','--review-reference','Fixture plan review',role='plan')
        return self.commit_plan('Classify decision impact')

    def test_scoped_decision_requires_plan_adoption_and_blocks_dependents(self):
        path=self.decision()
        self.assertIsNone(self.f.queue(self.dev)['next']['dev'])
        self.classify(path)
        self.assertIsNone(self.f.queue(self.dev)['next']['dev'])
        self.adopt()
        queue=self.f.queue(self.dev)
        self.assertEqual(queue['next']['dev'],'P002')
        rows={r['id']:r for r in queue['tasks']}
        self.assertEqual(rows['P003']['blocked_by_decisions'],[path])
        self.assertEqual(rows['P002']['blocked_by_decisions'],[])
        self.command('classify',path,'--scope','all','--reason','x','--review-reference','x',ok=False)

    def test_resolution_requires_full_adopted_commit_and_preserves_user_stop(self):
        path=self.decision();self.classify(path)
        sha=self.f.git('rev-parse','HEAD')
        self.command('resolve',path,'--plan-commit',sha,ok=False)
        self.adopt()
        self.command('resolve',path,'--plan-commit',sha[:12],ok=False)
        self.command('pause','--request','User explicitly paused all work')
        self.command('resolve',path,'--plan-commit',sha)
        queue=self.f.queue(self.dev)
        self.assertEqual(queue['pending_decisions'],[])
        self.assertEqual(queue['next'],{'plan':None,'dev':None})
        self.commit_dev()
        self.command('resume','--request','User explicitly resumed dev')
        self.assertEqual(self.f.queue(self.dev)['next']['dev'],'P001')

    def test_legacy_decision_and_checkpoint_default_to_all(self):
        path=self.dev/'docs/feedback/dev/P001-decision-legacy.md';path.parent.mkdir(parents=True)
        path.write_text('> 유형: PLAN_DECISION\n> 상태: OPEN\n> 작업: P001\n> 결정 plan: -\n')
        checkpoint=self.dev/'docs/progress/sessions/dev.md';checkpoint.parent.mkdir(parents=True)
        checkpoint.write_text('> 역할: dev\n> 상태: PAUSED\n> 사용자 요청: User stop\n> 재개 요청: -\n')
        queue=self.f.queue(self.dev)
        self.assertEqual(queue['pending_decisions'][0]['scope'],'all')
        self.assertEqual(queue['paused_sessions'][0]['scope'],'all')
        self.assertEqual(queue['next'],{'plan':None,'dev':None})

    def test_pause_visibility_and_role_scope_with_custom_branches(self):
        self.command('pause','--scope','role','--request','Only plan paused',role='plan')
        self.assertEqual(self.f.queue(self.dev)['paused_sessions'],[])
        self.commit_plan('Record plan pause')
        queue=self.f.queue(self.dev)
        self.assertEqual(queue['paused_sessions'][0]['role'],'plan')
        self.assertEqual(queue['next']['dev'],'P001')
        self.command('pause','--request','Both roles paused',role='plan')
        self.commit_plan('Expand explicit user stop')
        self.assertIsNone(self.f.queue(self.dev)['next']['dev'])
        self.command('resume','--request','User resumed plan',role='plan')
        self.commit_plan('Resume plan')
        self.assertEqual(self.f.queue(self.dev)['next']['dev'],'P001')

    def test_resume_does_not_clear_other_role_or_decision(self):
        self.decision()
        self.command('pause','--request','Plan paused',role='plan');self.commit_plan('Pause plan')
        self.command('pause','--request','Dev paused');self.commit_dev()
        self.command('resume','--request','Dev resumed');self.commit_dev()
        self.assertIsNone(self.f.queue(self.dev)['next']['dev'])
        self.command('resume','--request','Plan resumed',role='plan');self.commit_plan('Resume plan')
        queue=self.f.queue(self.dev)
        self.assertEqual(queue['paused_sessions'],[])
        self.assertTrue(queue['pending_decisions']);self.assertIsNone(queue['next']['dev'])

    def test_checkpoint_deletion_and_fake_resume_rejected_by_index_guard(self):
        self.command('pause','--request','User pause');self.commit_dev()
        path=self.dev/'docs/progress/sessions/dev.md';original=path.read_text()
        path.unlink();self.f.git('add','docs',cwd=self.dev)
        self.f.run_cmd(sys.executable,'scripts/contract_guard.py','check','--target','index',cwd=self.dev,ok=False)
        path.write_text(original.replace('상태: PAUSED','상태: ACTIVE'))
        self.f.git('add','docs',cwd=self.dev)
        self.f.run_cmd(sys.executable,'scripts/contract_guard.py','check','--target','index',cwd=self.dev,ok=False)
        path.write_text(original)
        self.command('resume','--request','User resume');self.commit_dev()
        self.f.run_cmd(sys.executable,'scripts/contract_guard.py','check','--target','HEAD',cwd=self.dev)

    def test_decision_edit_delete_and_dev_scope_forgery_rejected(self):
        path=self.decision();file=self.dev/path;original=file.read_text()
        for text in (original+'changed question\n', None):
            if text is None:file.unlink()
            else:file.write_text(text)
            self.f.git('add','docs',cwd=self.dev)
            self.f.run_cmd(sys.executable,'scripts/contract_guard.py','check','--target','index',cwd=self.dev,ok=False)
            file.write_text(original)
        self.f.git('add','docs',cwd=self.dev)
        scope=self.dev/'docs/planning/decision-scopes/forged.json';scope.parent.mkdir(parents=True);scope.write_text('{}')
        self.f.run_cmd(sys.executable,'scripts/contract_guard.py','check',cwd=self.dev,ok=False)

    def test_stale_classification_and_unknown_task_rejected(self):
        path=self.decision()
        self.command('classify',path,'--scope','tasks','--tasks','P999','--reason','x','--review-reference','x',role='plan',ok=False)
        self.classify(path)
        scope=next((self.plan/'docs/planning/decision-scopes').glob('*.json'))
        value=json.loads(scope.read_text());value['request_sha256']='0'*64;scope.write_text(json.dumps(value))
        self.f.queue(self.plan,ok=False)

    def test_handoff_idempotence_receipts_and_monotonic_history(self):
        sha=self.f.git('rev-parse','HEAD',cwd=self.dev)
        args=('handoff','--kind','WORK_READY','--target-role','plan','--commit',sha,
              '--document','docs/planning/plans/P001.md','--summary','Verified result','--next-action','Review evidence')
        self.command(*args)
        path=next((self.dev/'docs/progress/handoffs/dev').glob('*.json'));before=path.read_bytes()
        self.command(*args);self.assertEqual(path.read_bytes(),before)
        self.command(*args[:-1],'Different next step',ok=False)
        self.command('handoff-status',path.stem,'--status','ACKNOWLEDGED','--evidence','receipt',ok=False)
        self.command('handoff-status',path.stem,'--status','SENT','--evidence','Tool delivery receipt')
        self.commit_dev()
        self.command('handoff-status',path.stem,'--status','ACKNOWLEDGED','--evidence','Recipient confirmation')
        self.commit_dev()
        self.assertEqual(self.f.queue(self.plan)['handoffs'][0]['status'],'ACKNOWLEDGED')
        value=json.loads(path.read_text());value['history'][0]['evidence']='rewritten';path.write_text(json.dumps(value))
        self.f.git('add','docs',cwd=self.dev)
        self.f.run_cmd(sys.executable,'scripts/contract_guard.py','check','--target','index',cwd=self.dev,ok=False)

    def test_new_intake_does_not_pause_unrelated_approved_work(self):
        file=self.root/'new.txt';file.write_text('Add a future capability')
        self.f.run_cmd(sys.executable,'scripts/plan_intake.py','request','--title','New request','--request-file',str(file),
                       '--source','User request','--impact','Future scope',cwd=self.dev)
        self.commit_dev()
        queue=self.f.queue(self.dev)
        self.assertEqual(queue['next']['dev'],'P001')
        self.assertEqual(queue['plan_requests'][0]['state'],'PENDING')
        self.assertEqual(queue['pending_decisions'],[])

    def test_plan_checkpoint_cannot_be_deleted_and_history_is_preserved(self):
        self.command('pause','--request','Plan user pause',role='plan');self.commit_plan('Pause plan')
        path=self.plan/'docs/progress/sessions/plan.md';text=path.read_text()
        path.unlink();self.f.git('add','docs',cwd=self.plan)
        self.f.run_cmd(sys.executable,'scripts/contract_guard.py','check','--target','index',cwd=self.plan,ok=False)
        path.write_text(text);self.command('resume','--request','Plan user resume',role='plan');self.commit_plan('Resume plan')
        path.write_text('\n'.join(line for line in path.read_text().splitlines() if ' | PAUSE | ' not in line))
        self.f.git('add','docs',cwd=self.plan)
        self.f.run_cmd(sys.executable,'scripts/contract_guard.py','check','--target','index',cwd=self.plan,ok=False)

    def test_invalid_pause_and_handoff_never_write_records(self):
        self.command('resume','--request','No existing pause',ok=False)
        self.command('pause','--request','-',ok=False)
        self.assertFalse((self.dev/'docs/progress/sessions/dev.md').exists())
        sha=self.f.git('rev-parse','HEAD',cwd=self.dev)
        self.command('handoff','--kind','STOP','--target-role','plan','--commit',sha[:12],
            '--document','docs/planning/plans/P001.md','--summary','x','--next-action','x',ok=False)
        self.command('handoff','--kind','STOP','--target-role','plan','--commit',sha,
            '--document','missing.md','--summary','x','--next-action','x',ok=False)
        self.assertFalse((self.dev/'docs/progress/handoffs/dev').exists())

    def test_push_guard_checks_bad_plan_checkpoint_commit_from_dev(self):
        self.command('pause','--request','Plan pause',role='plan');self.commit_plan('Pause plan')
        path=self.plan/'docs/progress/sessions/plan.md';path.unlink()
        self.f.git('add','docs',cwd=self.plan)
        self.f.git('-c','core.hooksPath=/dev/null','commit','-m','Simulated bypass fixture',cwd=self.plan)
        sha=self.f.git('rev-parse','HEAD',cwd=self.plan)
        result=subprocess.run([sys.executable,'scripts/contract_guard.py','pre-push'],cwd=self.dev,
            input='refs/heads/design '+sha+' refs/heads/design '+'0'*40+'\n',text=True,capture_output=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('Preserve checkpoint',result.stderr)

    def test_default_owner_uses_actual_role(self):
        out=self.f.run_cmd(sys.executable,'scripts/work_queue.py','--json',cwd=self.plan)
        self.assertEqual(json.loads(out.stdout)['owner'],'plan')


class ReleaseUpgradeTests(unittest.TestCase):
    def test_actual_v010_upgrade_preserves_custom_hooks_and_records(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);old=root/'old';old.mkdir();repo=root/'repo'
            # The fixture is the actual published source commit, not a synthetic old version.
            raw=subprocess.check_output(['git','archive','v0.1.0'],cwd=BASE)
            with tarfile.open(fileobj=io.BytesIO(raw)) as archive:
                for entry in archive:
                    if entry.isfile():
                        path=old/entry.name;path.parent.mkdir(parents=True,exist_ok=True)
                        path.write_bytes(archive.extractfile(entry).read());path.chmod(entry.mode)
            def run(*args,ok=True):
                r=subprocess.run(args,cwd=root,text=True,capture_output=True)
                self.assertEqual(r.returncode==0,ok,r.stdout+r.stderr);return r
            run('git','init','-b','plan',str(repo))
            options=['--repo',str(repo),'--protect','specs','--agent','both']
            run(sys.executable,str(old/'scripts/install_harness.py'),*options,'--apply')
            extra=repo/'.githooks/post-commit';extra.write_text('# existing adapter\n')
            record=repo/'docs/progress/sessions/dev.md';record.parent.mkdir(parents=True);record.write_text('Existing session data\n')
            call=[sys.executable,str(BASE/'scripts/install_harness.py'),*options,'--upgrade']
            before=(repo/'scripts/contract_guard.py').read_bytes();run(*call)
            self.assertEqual((repo/'scripts/contract_guard.py').read_bytes(),before)
            run(*call,'--apply')
            self.assertEqual(json.loads((repo/'.harness/installation.json').read_text())['version'],'0.2.0')
            self.assertEqual(extra.read_text(),'# existing adapter\n');self.assertEqual(record.read_text(),'Existing session data\n')
            self.assertTrue((repo/'scripts/workflow_control.py').exists())
            (repo/'AGENTS.md').write_text('User customization\n')
            run(*call,'--apply',ok=False)
            self.assertEqual((repo/'AGENTS.md').read_text(),'User customization\n')


if __name__=='__main__':unittest.main()
