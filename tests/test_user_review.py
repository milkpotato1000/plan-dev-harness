"""Stateful document-protocol exercises and actual Git/CLI acceptance boundaries.

ReviewExercise is a test-only reference actor. Its Markdown JSON snapshots are
fixture encoding, not a production schema/parser or a host-wide question guard.
No test emits a real user question or grants production approval.
"""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

import test_numbered_queue as fixtures

BASE = Path(__file__).resolve().parents[1]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class ReviewExercise:
    def __init__(self, root, role):
        self.root, self.role = Path(root), role

    def submit(self, artifact, scope='ui', commit='a'*40, equivalent_reason=''):
        if self.role != 'dev':
            raise PermissionError('Dev owns the source packet')
        raw = artifact.read_bytes()
        # Only this known fixture's generated_at is non-material. This is not
        # a general rule that arbitrary metadata may be ignored in real reviews.
        material = digest(json.dumps(json.loads(raw)['content'], sort_keys=True).encode())
        ident = dict(task='P010', criterion='C1', artifact=artifact.name, scope=scope, material=material)
        key = 'P010-C1-' + digest(json.dumps(ident, sort_keys=True).encode())[:16]
        packet = dict(ident, key=key, path=str(artifact), raw_hash=digest(raw), commit=commit,
                      equivalent_reason=equivalent_reason, failures=['Fixture earlier FAIL retained'])
        path = self.root/'docs/feedback/dev/reviews'/f'{key}.md'
        self.append(path, packet)  # Preserve original and subsequent delivery observations.
        return packet

    @staticmethod
    def append(path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a') as stream:
            stream.write('\n```json\n' + json.dumps(value, sort_keys=True) + '\n```\n')

    def ledger_path(self, packet):
        return self.root/'docs/planning/reviews/user-reviews'/f'{packet["key"]}.md'

    def read(self, packet):
        path = self.ledger_path(packet)
        return json.loads(path.read_text().split('```json\n')[-1].split('\n```')[0]) if path.exists() else dict(questions=[], answers=[], observations=[], state='RECEIVED')

    def save(self, packet, value):
        if self.role != 'plan':
            raise PermissionError('Only plan writes the review ledger')
        self.append(self.ledger_path(packet), value)

    def answer(self, packet, answer):
        value = self.read(packet); value['answers'].append(answer); self.save(packet, value)

    def receive(self, packet, busy=False):
        if self.role != 'plan':
            raise PermissionError('This fixture queues a review for plan')
        self.append(self.root/'pending-plan-reviews.md', dict(key=packet['key'], busy=busy))
        return 'QUEUED_AT_SAFE_BOUNDARY' if busy else 'READY_FOR_REVIEW'

    def deliver(self, packet, grants=(), host=False, outcome='unknown', permission=True):
        """Test-only transport outcome log; no production event/schema changes."""
        if self.role != 'dev':
            raise PermissionError('This fixture exercises only authorized dev-to-plan review delivery')
        path = self.root/'delivery-exercise'/f'{packet["key"]}.md'
        previous = json.loads(path.read_text().split('```json\n')[-1].split('\n```')[0]) if path.exists() else {}
        if previous.get('attempted'):
            return previous  # Observe outcome before any later retry; no blind resend.
        attempt = ('dev', 'plan') in grants and host and permission
        result = dict(attempted=attempt, sends=int(attempt), status='SENT' if attempt and outcome == 'success' else 'PENDING')
        self.append(path, result)
        return result

    def review(self, packet, *, human=False, existing_decision=False, viewer=True,
               visual=False, permission=True, existing_answers=()):
        if self.role != 'plan':
            raise PermissionError('Dev must not reissue the review question')
        value = self.read(packet)
        if not permission:
            value['state'] = 'PERMISSION_BLOCKED'; self.save(packet, value); return value
        if digest(Path(packet['path']).read_bytes()) != packet['raw_hash']:
            raise ValueError('Artifact changed after the packet; re-review exact bytes')
        for answer in value['answers'] + list(existing_answers):
            if (answer.get('actor') == 'human' and answer.get('source')
                and answer.get('material') == packet['material'] and answer.get('scope') == packet['scope']
                and (answer.get('raw_hash') == packet['raw_hash'] or packet['equivalent_reason'])):
                value.update(state='ANSWER_REUSED', approved=answer.get('answer') == 'approve')
                value['answers'] = value['answers'] + [answer] if answer not in value['answers'] else value['answers']
                self.save(packet, value); return value
        if not viewer:
            value['state'] = 'NOT_OBSERVED'; self.save(packet, value); return value
        # An actual read of fixture bytes. A visual observation is separately
        # injected for the simulation; reading bytes never implies visual/human approval.
        Path(packet['path']).read_bytes()
        value['observations'].append(dict(hash=packet['raw_hash'], kind='visual simulation' if visual else 'content read'))
        if human:
            if not value['questions']:
                value['questions'].append(dict(key=packet['key'], owner='plan', scope=packet['scope']))
            value['state'] = 'QUESTION_PENDING'
        elif existing_decision:
            value['state'] = 'DECIDED_WITHIN_EXISTING_SCOPE'
        else:
            value['state'] = 'REVIEWED'
        self.save(packet, value); return value


class ReviewProtocolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='review-protocol-')
        self.addCleanup(self.temp.cleanup); self.root = Path(self.temp.name)
        self.artifact = self.root/'result.json'; self.artifact.write_text(json.dumps(dict(content='Result A', generated_at='t1')))
        self.dev = ReviewExercise(self.root, 'dev'); self.plan = ReviewExercise(self.root, 'plan')

    def human_answer(self, packet, **extra):
        return dict(actor='human', source='fixture:actual-user-turn-1', material=packet['material'],
                    raw_hash=packet['raw_hash'], scope=packet['scope'], answer='approve', **extra)

    def test_m1_m3_pending_and_answered_reviews_survive_events_commits_and_restart(self):
        packet = self.dev.submit(self.artifact)
        result = self.plan.review(packet, human=True)
        self.assertEqual(len(result['questions']), 1)
        first_ledger = self.plan.ledger_path(packet).read_bytes()
        again = self.dev.submit(self.artifact, commit='b'*40)
        self.assertEqual(packet['key'], again['key'])
        restarted = ReviewExercise(self.root, 'plan')
        self.assertEqual(len(restarted.review(again, human=True)['questions']), 1)
        restarted.answer(again, self.human_answer(again))
        after_answer = restarted.review(again, human=True)
        self.assertEqual(after_answer['state'], 'ANSWER_REUSED')
        self.assertEqual(len(after_answer['questions']), 1)
        self.assertIn(first_ledger, self.plan.ledger_path(packet).read_bytes())
        self.assertIn('Fixture earlier FAIL retained', (self.root/'docs/feedback/dev/reviews'/f'{packet["key"]}.md').read_text())
        with self.assertRaises(PermissionError): self.dev.review(packet, human=True)
        with self.assertRaises(PermissionError): self.dev.save(packet, {})

    def test_m4_m10_reuse_valid_dev_human_answer_but_never_an_agent_claim(self):
        packet = self.dev.submit(self.artifact)
        answer = self.human_answer(packet, received_in='dev')
        value = self.plan.review(packet, human=True, existing_answers=[answer])
        self.assertEqual(value['state'], 'ANSWER_REUSED'); self.assertEqual(value['questions'], [])
        self.assertTrue(value['approved'])
        other = self.dev.submit(self.artifact, scope='policy')
        fake = dict(actor='agent', source='agent says user approved', material=other['material'], scope='policy', raw_hash=other['raw_hash'], answer='approve')
        self.assertEqual(len(self.plan.review(other, human=True, existing_answers=[fake])['questions']), 1)

    def test_m5_scope_material_change_and_evidence_for_nonmaterial_equivalence(self):
        packet = self.dev.submit(self.artifact); answer = self.human_answer(packet)
        self.plan.answer(packet, answer)
        content = self.dev.submit(self.artifact, scope='content')
        self.assertNotEqual(content['key'], packet['key'])
        self.assertEqual(self.plan.review(content, human=True, existing_answers=[answer])['state'], 'QUESTION_PENDING')
        self.artifact.write_text(json.dumps(dict(content='Result A', generated_at='t2')))
        timestamp = self.dev.submit(self.artifact)
        self.assertEqual(timestamp['key'], packet['key']); self.assertNotEqual(timestamp['raw_hash'], packet['raw_hash'])
        self.assertNotEqual(self.plan.review(timestamp, human=True)['state'], 'ANSWER_REUSED')
        explained = self.dev.submit(self.artifact, equivalent_reason='Only fixture generated_at changed; content bytes equivalent')
        self.assertEqual(self.plan.review(explained, human=True)['state'], 'ANSWER_REUSED')
        self.artifact.write_text(json.dumps(dict(content='Materially changed Result B', generated_at='t3')))
        changed = self.dev.submit(self.artifact)
        self.assertNotEqual(changed['key'], packet['key'])
        self.assertEqual(self.plan.review(changed, human=True, existing_answers=[answer])['state'], 'QUESTION_PENDING')

    def test_m2_m11_viewer_limits_and_permissions_cannot_be_relabelled_as_human_approval(self):
        packet = self.dev.submit(self.artifact)
        value = self.plan.review(packet, human=True, viewer=False)
        self.assertEqual(value['state'], 'NOT_OBSERVED'); self.assertEqual(value['observations'], [])
        self.assertEqual(value['questions'], [])
        value = self.plan.review(packet, human=True, permission=False)
        self.assertEqual(value['state'], 'PERMISSION_BLOCKED'); self.assertEqual(value['questions'], [])
        value = self.plan.review(packet, human=True, visual=False)
        self.assertEqual(value['observations'][-1]['kind'], 'content read')
        self.assertEqual(value['state'], 'QUESTION_PENDING'); self.assertNotIn('approved', value)
        self.assertEqual(len(value['questions']), 1)

    def test_m6_existing_delegated_decision_needs_no_human_question(self):
        packet = self.dev.submit(self.artifact, scope='within-existing-contract')
        value = self.plan.review(packet, existing_decision=True)
        self.assertEqual(value['state'], 'DECIDED_WITHIN_EXISTING_SCOPE')
        self.assertEqual(value['questions'], [])

    def test_m8_busy_plan_queues_without_preempting_work_or_reissuing_questions(self):
        packet = self.dev.submit(self.artifact)
        task = self.root/'current-plan-work.md'; task.write_text('Current approved planning task; earlier failure retained.\n')
        original = task.read_bytes()
        self.assertEqual(self.plan.receive(packet, busy=True), 'QUEUED_AT_SAFE_BOUNDARY')
        self.assertEqual(task.read_bytes(), original)
        self.assertFalse(self.plan.ledger_path(packet).exists())
        restarted = ReviewExercise(self.root, 'plan')
        self.assertEqual(restarted.review(packet, human=True)['state'], 'QUESTION_PENDING')
        self.assertEqual(restarted.receive(packet, busy=True), 'QUEUED_AT_SAFE_BOUNDARY')
        self.assertEqual(len(restarted.read(packet)['questions']), 1)
        self.assertEqual(task.read_bytes(), original)

    def test_m9_m11_directional_grant_host_failure_and_denial_keep_durable_packet(self):
        cases = [([('plan', 'dev')], True, 'success', True, 'PENDING', 0),
                 ([('dev', 'plan')], False, 'success', True, 'PENDING', 0),
                 ([('dev', 'plan')], True, 'unknown', True, 'PENDING', 1),
                 ([('dev', 'plan')], True, 'failure', True, 'PENDING', 1),
                 ([('dev', 'plan')], True, 'success', False, 'PENDING', 0),
                 ([('dev', 'plan')], True, 'success', True, 'SENT', 1)]
        for i, (grants, host, outcome, permission, state, sends) in enumerate(cases):
            with self.subTest(case=i):
                packet = self.dev.submit(self.artifact, scope='delivery-case-'+str(i))
                result = self.dev.deliver(packet, grants, host, outcome, permission)
                self.assertEqual((result['status'], result['sends']), (state, sends))
                self.assertTrue((self.root/'docs/feedback/dev/reviews'/f'{packet["key"]}.md').exists())
                self.assertEqual(self.plan.read(packet)['questions'], [])
                if result['attempted']:
                    restarted = ReviewExercise(self.root, 'dev')
                    self.assertEqual(restarted.deliver(packet, grants, host, outcome, permission), result)
        with self.assertRaises(PermissionError):
            self.plan.deliver(packet, [('dev', 'plan')], True, 'success')


class ReviewGitTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.NumberedQueueTests(); self.f.setUp(); self.addCleanup(self.f.doCleanups)
        self.plan, self.dev = self.f.plan, self.f.dev
        self.card, self.original = self.f.card()

    def control(self, *args, role='dev'):
        return self.f.run_cmd(sys.executable, 'scripts/workflow_control.py', *args, cwd=self.plan if role == 'plan' else self.dev)

    def test_m6_m7_optional_required_critical_and_exact_plan_decision(self):
        for ident in ['P002', 'P003']:
            text = self.original.replace('P001', ident)
            if ident == 'P003': text = text.replace('> 선행: 없음', '> 선행: P001')
            (self.plan/f'docs/planning/plans/{ident}.md').write_text(text)
        self.f.git('add', 'docs'); self.f.git('commit', '-m', 'Prepare independent and dependent fixture work')
        sha = self.f.git('rev-parse', 'HEAD'); self.f.git('merge', '--no-commit', sha, cwd=self.dev); self.f.adopt(sha)
        packet = self.dev/'docs/feedback/dev/reviews/P001-C1-ui-v1.md'; packet.parent.mkdir(parents=True)
        packet.write_text('Optional review pending. No critical decision and no human criterion completed.\n')
        self.assertEqual(self.f.queue(self.dev)['next']['dev'], 'P001')
        text = self.original.replace('> 실행: 미착수', '> 실행: 차단')
        text = text.replace('<!-- EXECUTION:END -->', '- 2026-11-05T01:00:00+00:00 | STATE | NOTE | - | Required human criterion pending in plan; leave unchecked.\n<!-- EXECUTION:END -->')
        (self.dev/self.card).write_text(text)
        self.f.git('add', 'docs', cwd=self.dev); self.f.git('commit', '-m', 'Preserve required human wait without a global critical stop', cwd=self.dev)
        q = self.f.queue(self.dev); rows = {x['id']: x for x in q['tasks']}
        self.assertEqual(q['next']['dev'], 'P002'); self.assertEqual(rows['P001']['checked'], 0)
        self.assertEqual(rows['P003']['state'], 'WAITING'); self.assertEqual(q['pending_decisions'], [])
        question = self.f.root/'question.txt'; question.write_text('Fixture critical meaning decision, not routine UI review.')
        self.control('decision', '--task', 'P001', '--question-file', str(question))
        self.f.git('add', 'docs', cwd=self.dev); self.f.git('commit', '-m', 'Preserve critical OPEN', cwd=self.dev)
        self.assertIsNone(self.f.queue(self.dev)['next']['dev'])
        decision = self.plan/'docs/process/review-decision.md'; decision.write_text('Fixture existing-scope decision for common request key P001-C1; actual answer source recorded.\n')
        self.f.git('add', str(decision)); self.f.git('commit', '-m', 'Commit plan decision before exact dev adoption')
        reviewed = self.f.git('rev-parse', 'HEAD')
        self.assertFalse((self.dev/'docs/process/review-decision.md').exists())
        self.f.git('merge', '--no-ff', '--no-commit', reviewed, cwd=self.dev); self.f.adopt(reviewed)
        self.assertEqual(json.loads((self.dev/'.harness/adopted-plan.json').read_text())['commit'], reviewed)
        self.assertEqual((self.dev/'docs/process/review-decision.md').read_bytes(), decision.read_bytes())
        self.assertIsNone(self.f.queue(self.dev)['next']['dev'])  # Adoption alone is not resolve or human approval.

    def test_m3_transport_keys_differ_while_review_identity_stays_the_same(self):
        doc = self.plan/'docs/process/review-packet.md'; doc.write_text('Common review key P010-C1-ui-material-A.\n')
        self.f.git('add', str(doc)); self.f.git('commit', '-m', 'Prepare transport fixture')
        shas = [self.f.git('rev-parse', 'HEAD')]
        (self.plan/'unrelated.md').write_text('A new delivery commit is not a new artifact.\n')
        self.f.git('add', 'unrelated.md'); self.f.git('commit', '-m', 'Unrelated delivery wrapper'); shas.append(self.f.git('rev-parse', 'HEAD'))
        for sha in shas:
            self.control('handoff', '--kind', 'WORK_READY', '--target-role', 'dev', '--commit', sha,
                         '--document', 'docs/process/review-packet.md', '--summary', 'Common review key unchanged', '--next-action', 'Link existing ledger', role='plan')
        events = list((self.plan/'docs/progress/handoffs/plan').glob('*.json'))
        self.assertEqual(len(events), 2)  # Existing runtime intentionally deduplicates transport, not meaning.
        self.assertTrue(all(json.loads(p.read_text())['status'] == 'PENDING' for p in events))


class ReviewUpgradeTests(unittest.TestCase):
    def test_m12_real_022_upgrade_adds_template_and_preserves_runtime_extensions(self):
        with tempfile.TemporaryDirectory(prefix='review-upgrade-') as tmp:
            root = Path(tmp); old = root/'old'; old.mkdir()
            raw = subprocess.check_output(['git', 'archive', 'b932fc81de18b7780c8b7858f9de7e3ecbd27965'], cwd=BASE)
            with tarfile.open(fileobj=io.BytesIO(raw)) as archive: archive.extractall(old)
            def cmd(*args): return subprocess.run(args, cwd=root, capture_output=True, text=True, check=True)
            repo = root/'project'; cmd('git', 'init', '-b', 'plan', str(repo)); cmd('git', '-C', str(repo), 'config', 'core.hooksPath', '.githooks')
            options = ['--repo', str(repo), '--protect', 'specs', '--agent', 'both']
            cmd(sys.executable, str(old/'scripts/install_harness.py'), *options, '--apply')
            template = repo/'docs/process/user-review-template.md'; self.assertFalse(template.exists())
            runtime = {p.name: p.read_bytes() for p in (repo/'scripts').glob('*.py')}
            extra = repo/'custom-extension.txt'; extra.write_text('User extension retained.\n')
            installer = [sys.executable, str(BASE/'scripts/install_harness.py'), *options, '--upgrade']
            cmd(*installer); self.assertFalse(template.exists()); cmd(*installer, '--apply')
            self.assertEqual(template.read_bytes(), (BASE/'assets/docs/process/user-review-template.md').read_bytes())
            self.assertEqual(json.loads((repo/'.harness/installation.json').read_text())['version'],
                             (BASE/'VERSION').read_text().strip())
            self.assertEqual(extra.read_text(), 'User extension retained.\n')
            for n, raw in runtime.items(): self.assertEqual((repo/'scripts'/n).read_bytes(), raw)


if __name__ == '__main__': unittest.main()
