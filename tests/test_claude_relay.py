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

    def test_recovery_requires_review_and_consumes_once(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            key, review, message = 'a'*64, 'b'*40, 'exact'
            peer = dict(generation=3, session_id='private')
            relay.reserve(d, key, {'message':message}, 3)
            original = (d/'claude-relay-attempts.json').read_bytes()
            entry = json.loads(original)[key]
            grant = dict(state='REJECTED_BEFORE_SEND', key=key, role='plan', review=review,
                         generation=3, payload=relay.digest(message), target=relay.digest('private'),
                         original_entry=relay.digest(json.dumps(entry, sort_keys=True)), evidence='c'*64)
            disposition = d/('relay-disposition-'+key+'.json')
            def attempt(_):
                try:
                    relay.reserve_recovery(d,key,message,peer,'plan',review)
                    return True
                except ValueError:
                    return False
            self.assertFalse(attempt(0))
            for change in [dict(state='UNKNOWN'), dict(state='revoked'), dict(review='0'*40),
                           dict(generation=4), dict(target='wrong'), dict(payload='changed')]:
                disposition.write_text(json.dumps(dict(grant, **change)))
                self.assertFalse(attempt(0))
            disposition.write_text(json.dumps(grant))
            with concurrent.futures.ThreadPoolExecutor(2) as workers:
                self.assertEqual(sorted(workers.map(attempt, range(2))), [False, True])
            self.assertFalse(attempt(0))
            self.assertEqual(original, (d/'claude-relay-attempts.json').read_bytes())

    def test_canonical_input_stream_and_callback(self):
        import json
        for mutation in ('ok','duplicate','extra','short','wrong-target','missing-end','second','mixed-call','bad-id','alias','type','unexpected'):
            gate = relay.CanonicalSend('unit-target', '한글\n' + 'x'*90)
            original = dict(gate.expected)
            if mutation == 'extra': original['content']='wrong'
            if mutation == 'short': original['message']='한'
            if mutation == 'wrong-target': original['to']='other'
            raw = json.dumps(original)
            if mutation == 'duplicate': raw=raw.replace('{','{"to":"first",',1)
            start=dict(type='content_block_start',index=1,content_block=dict(type='tool_use',name='SendMessage',id='id',input={}))
            gate.observe(start)
            gate.observe(dict(type='content_block_delta',index=1,delta=dict(type='input_json_delta',partial_json=raw)))
            gate.observe(dict(type='content_block_stop',index=1))
            if mutation != 'missing-end': gate.observe(dict(type='message_stop'))
            if mutation == 'second': gate.observe(start)
            if mutation == 'mixed-call': gate.observe(dict(start,content_block=dict(type='tool_use',name='ListAgents',id='other',input={})))
            args=dict(gate.expected,recipient='unit-target',recipient_kind='name',type='message',content='synthetic preview')
            if mutation == 'alias': args['recipient']='elsewhere'
            if mutation == 'type': args['message']=1
            if mutation == 'unexpected': args['other']='unexpected'
            event=dict(tool_use_id='id',tool_name='SendMessage',tool_input=args)
            result=gate.replacement('other' if mutation=='bad-id' else 'id',event)
            with self.subTest(mutation=mutation):
                if mutation=='ok':
                    self.assertEqual(result,{'hookSpecificOutput':{'hookEventName':'PreToolUse','updatedInput':gate.expected}})
                    self.assertIsNone(gate.replacement('id',event))
                else: self.assertIsNone(result)
