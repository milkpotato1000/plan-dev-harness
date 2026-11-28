import concurrent.futures
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import claude_relay as relay


class RelayBoundary(unittest.TestCase):
    def test_single_attempt_across_competing_callers(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            def attempt(_):
                try:
                    relay.reserve(directory, 'same', {'message': "한글; $(false)"}, 3)
                    return True
                except ValueError:
                    return False
            with concurrent.futures.ThreadPoolExecutor(2) as workers:
                self.assertEqual(sorted(workers.map(attempt, range(2))), [False, True])
            raw = (directory/'claude-relay-attempts.json').read_text()
            self.assertNotIn('false', raw)
            self.assertIn('unknown', raw)
            self.assertFalse(attempt(3))

    def test_live_proof_only_relaxes_old_idle_observation(self):
        def proof(when, state, extra):
            result = {'issues': ['dev_stale_or_future', *extra], 'peers': {
                'dev': {'observed_at': when, 'state': state}}}
            with patch.object(relay.registry, 'inventory_for_claude', return_value=[]), patch.object(relay.registry, 'diagnose', return_value=result):
                return relay.current_peers('.')
        self.assertIn('dev', proof('2000-01-01T00:00:00Z', 'idle', []))
        for when, state, issues in [('2099-01-01T00:00:00Z','idle',[]),
                ('2000-01-01T00:00:00Z','busy',[]),
                ('2000-01-01T00:00:00Z','idle',['dev_multiple_host_writers'])]:
            with self.assertRaises(ValueError):
                proof(when, state, issues)

    def test_normalized_send_fields_must_agree(self):
        args = {'message': '정확 "문구"\n$HOME', 'to': 'fixture-plan'}
        actual = dict(args, type='message', recipient=args['to'], content=args['message'],
                      recipient_kind='name', summary='Reviewed handoff')
        self.assertTrue(relay.exact_send(actual, args))
        for field in actual:
            self.assertFalse(relay.exact_send(dict(actual, **{field: 'changed'}), args))
        self.assertFalse(relay.exact_send(dict(actual, broadcast=True), args))

    def test_native_preview_requires_full_original_body(self):
        body = 'P901 검토를 시작해 주세요. 이미 시작된 경우 보존합니다.'
        expected = {'to': 'plan', 'message': body}
        args = dict(expected, content=body[:30] + '…')
        self.assertTrue(relay.exact_send(args, expected))
        self.assertFalse(relay.exact_send(dict(args, message=args['content']), expected))
        self.assertFalse(relay.exact_send(dict(args, content=body[:29] + '…'), expected))
