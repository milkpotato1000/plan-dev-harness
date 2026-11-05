"""Real Git boundaries plus a test-only host contract simulation.

There is no production sender in the CLI. SimulatedHost/SenderExercise check
documented adapter expectations and real event persistence, not model compliance
or delivery through a live host. Git/adoption/queue checks use real worktrees.
"""
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import unittest

import test_numbered_queue as fixtures

BASE = Path(__file__).resolve().parents[1]


class SimulatedHost:
    def __init__(self, outcome):
        self.outcome, self.calls = outcome, []

    def send(self):
        self.calls.append('send')
        return self.outcome

    def wait(self):
        raise AssertionError('A successful planning handoff must return without waiting')

    def read(self):
        raise AssertionError('Receipt inspection belongs to a later natural request')


class SenderExercise:
    """Test-only adapter; no networking, scheduler, new schema or runtime API."""
    def __init__(self, case, host, event):
        self.case, self.host, self.event = case, host, event
        self.attempted, self.trace = False, []

    def deliver(self, authorized=True, available=True, recipient=True, paused=False):
        state = json.loads(self.event.read_text())['status']
        if state != 'PENDING' or self.attempted:
            return state
        if not authorized or not available or not recipient or paused:
            return state
        self.attempted = True
        outcome = self.host.send()
        self.trace.append(outcome)
        if outcome == 'success':
            self.case.control('handoff-status', self.event.stem, '--status', 'SENT',
                              '--evidence', 'Simulated host success; not a live receipt')
            self.case.commit_plan('Record actual simulated send result')
            self.case.f.git('push', 'fixture', 'design', cwd=self.case.plan)
            self.trace += ['commit', 'push', 'return']
        else:
            self.trace.append('return')
        return json.loads(self.event.read_text())['status']


class AsyncHandoffTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.NumberedQueueTests()
        self.f.setUp()
        self.addCleanup(self.f.doCleanups)
        self.plan, self.dev = self.f.plan, self.f.dev
        self.card('P010', 30)
        self.initial = self.commit_plan('Prepare current approved P010')
        self.adopt(self.initial)
        remote = self.f.root/'delivery.git'
        self.f.git('init', '--bare', str(remote))
        self.f.git('remote', 'add', 'fixture', str(remote))

    def control(self, *args, role='plan', ok=True):
        return self.f.run_cmd(sys.executable, 'scripts/workflow_control.py', *args,
            cwd=self.plan if role == 'plan' else self.dev, ok=ok)

    def card(self, ident, priority, dependency='없음'):
        text = (self.plan/'docs/planning/plans/_TEMPLATE.md').read_text()
        text = text.replace('P001', ident).replace('> 준비: 초안', '> 준비: 준비 완료')
        text = text.replace('> 승인 근거: 미확정', '> 승인 근거: Isolated P006 fixture review')
        text = text.replace('> 우선순위: 10', '> 우선순위: ' + str(priority))
        text = text.replace('> 선행: 없음', '> 선행: ' + dependency)
        (self.plan/f'docs/planning/plans/{ident}.md').write_text(text)

    def commit_plan(self, note):
        self.f.git('add', 'docs', cwd=self.plan)
        self.f.git('commit', '-m', note, cwd=self.plan)
        return self.f.git('rev-parse', 'HEAD', cwd=self.plan)

    def commit_dev(self, note):
        self.f.git('add', 'docs', cwd=self.dev)
        self.f.git('commit', '-m', note, cwd=self.dev)

    def adopt(self, sha):
        self.f.git('merge', '--no-ff', '--no-commit', sha, cwd=self.dev)
        self.f.adopt(sha)

    def event(self, sha=None):
        sha = sha or self.initial
        self.control('handoff', '--kind', 'WORK_READY', '--target-role', 'dev',
            '--commit', sha, '--document', 'docs/planning/plans/P010.md',
            '--summary', 'Reviewed isolated fixture', '--next-action', 'Adopt at a safe boundary')
        return next((self.plan/'docs/progress/handoffs/plan').glob('*.json'))

    def finish(self, ident):
        path = self.dev/f'docs/planning/plans/{ident}.md'
        text = path.read_text().replace('> 실행: 진행 중', '> 실행: 완료')
        text = text.replace('> 실행: 미착수', '> 실행: 완료').replace('- [ ] C', '- [x] C')
        proof = f'docs/verification/{ident}.md'
        (self.dev/proof).parent.mkdir(parents=True, exist_ok=True)
        (self.dev/proof).write_text('Isolated fixture verification: expected equals actual.\n')
        logs = ''.join(f'- 2026-11-05T01:00:00+00:00 | C{i} | PASS | {proof} | Verified fixture.\n'
                       for i in (1, 2, 3))
        path.write_text(text.replace('<!-- EXECUTION:END -->', logs+'<!-- EXECUTION:END -->'))
        self.commit_dev('Complete ' + ident + ' without deleting earlier failures')

    def test_n1_n4_sent_returns_without_ack_then_later_observation(self):
        event = self.event(); host = SimulatedHost('success')
        actor = SenderExercise(self, host, event)
        self.assertEqual(actor.deliver(), 'SENT')
        self.assertEqual(actor.trace, ['success', 'commit', 'push', 'return'])
        self.assertEqual(self.f.git('--git-dir='+str(self.f.root/'delivery.git'),
                                   'rev-parse', 'design'), self.f.git('rev-parse', 'HEAD'))
        self.assertEqual(host.calls, ['send'])
        sent = json.loads(event.read_text())
        self.assertEqual([e['status'] for e in sent['history']], ['PENDING', 'SENT'])
        # Plan can prepare its next P with no ACK or dev progress at all.
        self.card('P011', 10); self.commit_plan('Independent next planning request')
        self.assertEqual(json.loads(event.read_text()), sent)
        self.assertEqual(actor.deliver(), 'SENT'); self.assertEqual(host.calls, ['send'])
        self.control('handoff-status', event.stem, '--status', 'ACKNOWLEDGED',
                     '--evidence', 'Later natural status query: simulated recipient read the exact SHA')
        self.commit_plan('Record later observed receipt without sending again')
        ack = json.loads(event.read_text())
        self.assertEqual(ack['history'][:2], sent['history'])
        self.assertEqual(ack['status'], 'ACKNOWLEDGED')
        self.assertEqual(actor.deliver(), 'ACKNOWLEDGED'); self.assertEqual(host.calls, ['send'])
        self.assertEqual(json.loads((self.dev/'.harness/adopted-plan.json').read_text())['commit'], self.initial)

    def test_n5_failure_unknown_and_missing_capabilities_never_fake_sent_or_retry(self):
        event = self.event(); original = event.read_bytes()
        # Expectations come from P006 N5, not from an event-state implementation.
        cases = [('failure', {}, 1), ('unknown', {}, 1),
                 ('success', {'authorized': False}, 0), ('success', {'available': False}, 0),
                 ('success', {'recipient': False}, 0), ('success', {'paused': True}, 0)]
        for outcome, flags, sends in cases:
            with self.subTest(outcome=outcome, flags=flags):
                host = SimulatedHost(outcome); actor = SenderExercise(self, host, event)
                self.assertEqual(actor.deliver(**flags), 'PENDING')
                self.assertEqual(actor.deliver(**flags), 'PENDING')
                self.assertEqual(len(host.calls), sends)
                self.assertEqual(event.read_bytes(), original)

    def test_n2_n3_n7_busy_dev_preserved_then_exact_adoption_priority_dependency(self):
        path = self.dev/'docs/planning/plans/P010.md'
        failed = path.read_text().replace('> 실행: 미착수', '> 실행: 진행 중')
        failure = '- 2026-11-05T00:00:00+00:00 | C1 | FAIL | docs/verification/failed.md | Retain this failure.\n'
        failed = failed.replace('<!-- EXECUTION:END -->', failure+'<!-- EXECUTION:END -->')
        (self.dev/'docs/verification').mkdir(parents=True, exist_ok=True)
        (self.dev/'docs/verification/failed.md').write_text('Initial fixture failure retained.\n')
        path.write_text(failed); self.commit_dev('Checkpoint busy P010 with failure evidence')
        dirty = self.dev/'current-work.txt'; dirty.write_text('Uncommitted current implementation.\n')
        before = {p: p.read_bytes() for p in [path, dirty, self.dev/'.harness/adopted-plan.json']}
        self.card('P011', 10); first = self.commit_plan('Prepare P011 while dev is busy')
        self.event(first); self.commit_plan('Register first pending handoff')
        self.card('P012', 1, 'P011'); reviewed = self.commit_plan('Prepare dependent higher-priority P012')
        self.assertEqual(self.f.git('merge-base', '--is-ancestor', first, reviewed), '')
        # A newer unreviewed tip changes the current P; it must never leak into adoption.
        plan_current = self.plan/'docs/planning/plans/P010.md'
        plan_current.write_text(plan_current.read_text().replace('기대 동작과 실제 결과가 일치한다.', 'Unreviewed new criterion.'))
        future = self.commit_plan('Unreviewed future draft changing current contract')
        self.assertNotEqual(reviewed, future)
        self.assertEqual(self.f.queue(self.dev)['next']['dev'], 'P010')
        for p, raw in before.items(): self.assertEqual(p.read_bytes(), raw)
        self.assertFalse((self.dev/'docs/planning/plans/P011.md').exists())
        # Finish and commit current work before adopting a queued exact handoff.
        self.f.git('add', 'current-work.txt', cwd=self.dev)
        self.finish('P010')
        self.assertIn(failure, path.read_text())
        self.adopt(reviewed)
        self.assertEqual(json.loads((self.dev/'.harness/adopted-plan.json').read_text())['commit'], reviewed)
        self.assertNotIn('Unreviewed new criterion.', path.read_text())
        self.assertEqual(dirty.read_text(), 'Uncommitted current implementation.\n')
        q = self.f.queue(self.dev); rows = {r['id']: r for r in q['tasks']}
        self.assertEqual(q['next']['dev'], 'P011')
        self.assertEqual(rows['P011']['priority'], 10)
        self.assertEqual(rows['P012']['priority'], 1)
        self.assertEqual(rows['P012']['state'], 'WAITING')
        self.finish('P011'); self.assertEqual(self.f.queue(self.dev)['next']['dev'], 'P012')
        self.assertIn(failure, path.read_text())

    def test_n6_new_handoffs_preserve_role_all_legacy_pauses_and_open(self):
        self.control('pause', '--scope', 'role', '--request', 'Fixture human paused only plan')
        self.commit_plan('Record role pause'); self.card('P011', 10)
        reviewed = self.commit_plan('Permitted fixture record while paused')
        self.event(reviewed); self.commit_plan('Keep pending handoff while plan paused')
        self.adopt(reviewed)
        q = self.f.queue(self.dev)
        self.assertIsNone(q['next']['plan']); self.assertEqual(q['next']['dev'], 'P011')
        # Urgent human stop has priority even when a new reviewed handoff exists.
        self.control('pause', '--request', 'Fixture urgent human stop of both roles', role='dev')
        self.commit_dev('Preserve urgent stop')
        q = self.f.queue(self.dev); self.assertEqual(q['next'], {'plan': None, 'dev': None})
        checkpoint = self.dev/'docs/progress/sessions/dev.md'
        paused = checkpoint.read_bytes(); self.event(reviewed)
        self.assertEqual(checkpoint.read_bytes(), paused)
        # Legacy no-scope stop plus OPEN continue to block, without any resume call.
        checkpoint.write_text(checkpoint.read_text().replace('> 범위: all\n', ''))
        question = self.f.root/'question.txt'; question.write_text('Fixture critical decision still OPEN.')
        self.control('decision', '--task', 'P010', '--question-file', str(question), role='dev')
        q = self.f.queue(self.dev)
        self.assertEqual(q['paused_sessions'][-1]['scope'], 'all')
        self.assertTrue(q['pending_decisions'])
        self.assertEqual(q['next'], {'plan': None, 'dev': None})


class AsyncUpgradeTests(unittest.TestCase):
    def test_n8_real_021_upgrade_delivers_async_docs_without_runtime_change(self):
        import tempfile
        with tempfile.TemporaryDirectory(prefix='async-upgrade-') as tmp:
            root = Path(tmp); old = root/'old'; old.mkdir()
            raw = subprocess.check_output(['git', 'archive', '4aaf61cc0d08b5c6de8787beb23bbdf12f59948e'], cwd=BASE)
            with tarfile.open(fileobj=io.BytesIO(raw)) as archive: archive.extractall(old)
            repo = root/'project'
            def cmd(*args): return subprocess.run(args, cwd=root, capture_output=True, text=True, check=True)
            cmd('git', 'init', '-b', 'plan', str(repo)); cmd('git', '-C', str(repo), 'config', 'core.hooksPath', '.githooks')
            options = ['--repo', str(repo), '--protect', 'specs', '--agent', 'both']
            cmd(sys.executable, str(old/'scripts/install_harness.py'), *options, '--apply')
            files = ('contract_guard.py', 'work_queue.py', 'plan_cards.py', 'plan_intake.py', 'workflow_control.py')
            before = {f: (repo/'scripts'/f).read_bytes() for f in files}
            extension = repo/'local-extension.md'; extension.write_text('Retain user extension.\n')
            installer = [sys.executable, str(BASE/'scripts/install_harness.py'), *options, '--upgrade']
            old_version = (repo/'.harness/installation.json').read_bytes()
            cmd(*installer); self.assertEqual((repo/'.harness/installation.json').read_bytes(), old_version)
            cmd(*installer, '--apply')
            self.assertEqual(json.loads((repo/'.harness/installation.json').read_text())['version'],
                             (BASE/'VERSION').read_text().strip())
            for f, raw in before.items(): self.assertEqual((repo/'scripts'/f).read_bytes(), raw)
            self.assertEqual(extension.read_text(), 'Retain user extension.\n')
            self.assertEqual((repo/'docs/process/agent-workflow.md').read_bytes(), (BASE/'assets/instructions/agent-workflow.md').read_bytes())
            self.assertIn('Asynchronous handoff and parallel planning', (repo/'AGENTS.md').read_text())


if __name__ == '__main__': unittest.main()
