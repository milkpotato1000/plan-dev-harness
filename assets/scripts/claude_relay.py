#!/usr/bin/env python3
"""Deliver one committed handoff through the official Claude Agent SDK."""
import argparse
import asyncio
import hashlib
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

import session_handoff
import session_registry as registry


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def current_peers(repo):
    started = time.monotonic()
    rows = registry.inventory_for_claude()
    result = registry.diagnose(repo, 'claude', rows, private=True)
    for role, peer in result['peers'].items():
        age = (registry.moment() - registry.moment(peer['observed_at'])).total_seconds()
        if age > registry.TTL and peer['state'] == 'idle':
            issue = role + '_stale_or_future'
            if issue in result['issues']:
                result['issues'].remove(issue)
    if result['issues'] or time.monotonic() - started > 30:
        raise ValueError('Current peer proof rejected: ' + ','.join(result['issues']))
    return result['peers']


def address(session_id):
    rows = registry.inventory_for_claude()
    match = [r for r in rows if r.get('sessionId') == session_id]
    if len(match) != 1 or match[0].get('kind') != 'interactive':
        raise ValueError('Session changed')
    name = match[0].get('name')
    if not isinstance(name, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}', name) or sum(row.get('name') == name for row in rows) != 1:
        raise ValueError('Ambiguous peer name')
    return name


def exact_send(args, arguments):
    allowed = {**arguments, 'recipient': arguments['to'], 'content': arguments['message'],
               'type': 'message', 'summary': 'Reviewed handoff', 'recipient_kind': 'name'}
    # CLI 2.1.332 includes a display preview alongside the complete message.
    # Accept only the observed prefix format and still require the full message.
    message = arguments['message']
    if len(message) > 30 and args.get('content') == message[:30] + '…':
        allowed['content'] = args['content']
    return all(args.get(k) == v for k, v in arguments.items()) and all(
        k in allowed and allowed[k] == v for k, v in args.items())


def native_status(response):
    """Classify a native send response, independently of receiver input."""
    if not isinstance(response, dict):
        return 'unknown'
    success = response.get('success')
    detail = response.get('message')
    if type(success) is not bool or not isinstance(detail, str):
        return 'unknown'
    detail = detail.casefold().strip()
    state = response.get('status')
    negative = ('refused', 'held')
    if state in negative or detail.startswith(negative):
        if success or any(detail.startswith(other) and state not in (None, other) for other in negative):
            return 'unknown'
        for status in negative:
            if state == status or (state is None and detail.startswith(status)):
                return status
        return 'unknown'
    if success and state in (None, 'sent', 'delivered') and 'in that session\'s inbox' in detail and response.get('msg_id'):
        return 'native_success'
    return 'unknown'


def receipt_records(lines, session_id, message_id, body):
    """Read complete JSONL peer events for one pinned receiver and native message."""
    evidence = set()
    for line in lines:
        if not line.endswith('\n'):
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if not isinstance(row, dict) or row.get('sessionId') != session_id:
            continue
        kind = row.get('type')
        if kind == 'user' and row.get('isMeta') is True:
            event = row
            content = row.get('message', {}).get('content')
        elif kind == 'attachment' and row.get('attachment', {}).get('type') == 'queued_command':
            event = row['attachment']
            content = event.get('prompt', event.get('content'))
        else:
            continue
        origin = event.get('origin')
        if not isinstance(origin, dict) or origin.get('kind') != 'peer' or not message_id or origin.get('msg_id') != message_id:
            continue
        if origin.get('body') != body or origin.get('verifiedLocal') is not True or not isinstance(content, str):
            continue
        if kind == 'attachment' and content == body:
            evidence.add('queued')
            continue
        opening = re.match(r'Another Claude session sent a message:\n<cross-session-message [^>\n]+>\n', content)
        if opening and content[opening.end():].startswith(body + '\n</cross-session-message>') and content.count('</cross-session-message>') == 1:
            evidence.add('peer_input' if kind == 'user' else 'queued')
    return sorted(evidence)


class CanonicalSend:
    """Bind one completed model tool call to its SDK pre-execution callback."""
    def __init__(self, target, message):
        self.expected = dict(to=target, summary='Reviewed handoff', message=message)
        self.call_id = None
        self.index = None
        self.raw = ''
        self.closed = False
        self.invalid = False
        self.used = False
        self.message_done = False
        self.turn_tools = 0

    def observe(self, event):
        kind = event.get('type')
        idx = event.get('index')
        if kind == 'message_start':
            self.turn_tools = 0
        if kind == 'content_block_start':
            block = event.get('content_block', {})
            if block.get('type') == 'tool_use':
                self.turn_tools += 1
                if self.turn_tools > 1 and (self.call_id or block.get('name') == 'SendMessage'):
                    self.invalid = True
            if block.get('name') == 'SendMessage':
                if self.call_id or not isinstance(idx, int) or not block.get('id') or block.get('input') != {}:
                    self.invalid = True
                self.call_id = block.get('id')
                self.index = idx
        elif self.call_id and not self.closed and idx == self.index:
            if kind == 'content_block_delta':
                delta = event.get('delta', {})
                part = delta.get('partial_json')
                if delta.get('type') != 'input_json_delta' or not isinstance(part, str) or len(self.raw) + len(part) > 262144:
                    self.invalid = True
                elif not self.invalid:
                    self.raw += part
            elif kind == 'content_block_stop':
                self.closed = True
        if kind == 'message_stop' and self.closed:
            self.message_done = True

    def replacement(self, ident, event):
        if self.used or self.invalid or not self.message_done or not ident or ident != self.call_id or event.get('tool_use_id') != ident:
            return None
        self.used = True

        def unique(pairs):
            obj = dict(pairs)
            if len(obj) != len(pairs):
                raise ValueError('Duplicate input key')
            return obj

        try:
            original = json.loads(self.raw, object_pairs_hook=unique)
        except (ValueError, RecursionError):
            return None
        args = event.get('tool_input')
        if original != self.expected or not isinstance(args, dict) or event.get('tool_name') != 'SendMessage':
            return None
        aliases = dict(recipient=self.expected['to'], recipient_kind='name', type='message')
        if set(args) - (self.expected.keys() | aliases.keys() | {'content'}):
            return None
        if any(args.get(k) != v for k, v in self.expected.items()):
            return None
        if any(args.get(k) != v for k, v in aliases.items()) or not isinstance(args.get('content'), str):
            return None
        return {'hookSpecificOutput': {'hookEventName': 'PreToolUse', 'updatedInput': self.expected.copy()}}


def reserve(directory, key, arguments, generation):
    with registry.locked(directory):
        path = directory / 'claude-relay-attempts.json'
        attempts = registry.read_json(path) if path.exists() else {}
        if key in attempts or len(attempts) >= 128:
            raise ValueError('Duplicate attempt or full ledger')
        attempts[key] = dict(status='unknown', payload=digest(arguments['message']),
                             generation=generation, at=registry.moment().isoformat())
        registry.atomic_json(path, attempts)


def reserve_recovery(directory, key, message, peer, role, review):
    """Consume one externally reviewed disposition under the original registry lock."""
    if not re.fullmatch(r'[0-9a-f]{64}', key) or not re.fullmatch(r'[0-9a-f]{40}', review):
        raise ValueError('Invalid recovery reference')
    disposition = directory / ('relay-disposition-' + key + '.json')
    receipt = directory / ('relay-recovery-' + key + '.json')
    with registry.locked(directory):
        if receipt.exists() or not disposition.is_file():
            raise ValueError('Recovery absent or already consumed')
        grant = registry.read_json(disposition)
        ledger = directory / 'claude-relay-attempts.json'
        entry = registry.read_json(ledger).get(key, {})
        expected = dict(review=review, key=key, payload=digest(message),
                        generation=peer['generation'], target=digest(peer['session_id']),
                        role=role, state='REJECTED_BEFORE_SEND')
        if any(grant.get(k) != v for k, v in expected.items()):
            raise ValueError('Recovery authorization does not match attempt')
        if not all(re.fullmatch(r'[0-9a-f]{64}', grant.get(k, '')) for k in ('evidence', 'original_entry')):
            raise ValueError('Missing reviewed evidence')
        if (entry.get('status') != 'unknown' or entry.get('payload') != expected['payload']
                or entry.get('generation') != expected['generation']
                or digest(json.dumps(entry, sort_keys=True)) != grant['original_entry']):
            raise ValueError('Original ledger entry changed')
        registry.atomic_json(receipt, {**expected, 'state': 'consumed', 'at': registry.moment().isoformat()})
    return receipt


async def relay(repo, role, key, message, verify, recovery_review=None):
    import claude_agent_sdk as sdk
    root, directory, cfg = registry.config_for(repo)
    peer = current_peers(root)[role]
    arguments = {'to': address(peer['session_id']), 'message': message}
    gate = CanonicalSend(arguments['to'], message)
    stream_complete = asyncio.Event()
    listed = attempted = False
    result_status = 'unknown'
    trace = []
    verify()
    recovery = None
    if recovery_review is None:
        reserve(directory, key, arguments, peer['generation'])
    else:
        recovery = reserve_recovery(directory, key, message, peer, role, recovery_review)

    async def before(event, ident, context):
        nonlocal attempted
        name, args = event['tool_name'], event['tool_input']
        trace.append({'tool': name, 'target_matches': args.get('to') == arguments['to'],
                      'body_matches': args.get('message') == message, 'exact': exact_send(args, arguments)})
        valid = name == 'ListAgents' and args == {} and not listed
        if name == 'SendMessage' and not gate.message_done:
            try:
                await asyncio.wait_for(stream_complete.wait(), 3)
            except asyncio.TimeoutError:
                pass
        replacement = gate.replacement(ident, event) if name == 'SendMessage' else None
        if replacement and listed and not attempted:
            try:
                latest = current_peers(root)[role]
                if address(latest['session_id']) == arguments['to'] and all(latest[k] == peer[k] for k in ('session_id', 'generation')):
                    verify()
                    attempted = valid = True
            except (ValueError, OSError, subprocess.SubprocessError):
                valid = False
        if name == 'SendMessage':
            trace[-1].update(listed=listed, authorized=valid,
                summary_matches=args.get('summary') == 'Reviewed handoff',
                recipient_matches=args.get('recipient') == arguments['to'],
                full_content=args.get('content') == message,
                display_preview=args.get('content') == message[:30] + '…')
        if valid:
            return replacement or {}
        return {'hookSpecificOutput': {'hookEventName': 'PreToolUse',
                'permissionDecision': 'deny', 'permissionDecisionReason': 'Outside reviewed handoff'}}

    async def after(event, ident, context):
        nonlocal listed, result_status
        if event['tool_name'] == 'ListAgents':
            listing = str(event.get('tool_response', ''))
            listed = len(re.findall(re.escape(arguments['to']) + r' \[([a-f0-9]+)\]', listing)) == 1
        elif attempted and event['tool_name'] == 'SendMessage' and ident == gate.call_id and all(event['tool_input'].get(k) == v for k, v in gate.expected.items()):
            response = event.get('tool_response')
            result_status = native_status(response)
        return {}

    with tempfile.TemporaryDirectory() as cwd:
        hooks = {name: [sdk.HookMatcher(hooks=[fn], on_failure='block')]
                 for name, fn in [('PreToolUse', before), ('PostToolUse', after)]}
        options = sdk.ClaudeAgentOptions(cwd=cwd, cli_path=shutil.which('claude'),
            tools=['ListAgents', 'SendMessage'], strict_mcp_config=True, hooks=hooks, include_partial_messages=True,
            permission_mode='default', extra_args={'safe-mode': None, 'no-session-persistence': None,
            'permission-prompts': 'none'}, max_budget_usd=0.5, max_turns=4, max_buffer_size=262144)
        async with sdk.ClaudeSDKClient(options=options) as client:
            await client.query('Call ListAgents once. Then call SendMessage exactly once with this JSON. Stop on any failure. ' + json.dumps({**arguments, 'summary': 'Reviewed handoff'}, ensure_ascii=False))
            async for event in client.receive_response():
                gate.observe(getattr(event, 'event', {}))
                if gate.message_done:
                    stream_complete.set()
                if isinstance(event, sdk.ResultMessage):
                    print(json.dumps({'status': result_status, 'attempted': attempted,
                                      'cost_usd': event.total_cost_usd, 'trace': trace}))
    with registry.locked(directory):
        if recovery:
            registry.atomic_json(recovery.with_suffix('.result.json'), {
                'status': result_status, 'send_authorized': attempted, 'trace': trace})
        else:
            path = directory / 'claude-relay-attempts.json'
            attempts = registry.read_json(path)
            attempts[key]['status'] = result_status
            registry.atomic_json(path, attempts)
    return result_status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--event', required=True)
    parser.add_argument('--authority-reference', required=True)
    parser.add_argument('--recovery-review', help='Reviewed disposition commit for one consumed attempt')
    args = parser.parse_args()
    def prepare():
        return session_handoff.prepare(args.repo, 'claude', args.event, args.authority_reference,
                                       registry.inventory_for_claude(), relay_proof=True)
    packet = prepare()
    def verify():
        latest = prepare()
        for field in ('key', 'action', 'generation', 'target_id'):
            if latest[field] != packet[field]:
                raise ValueError('Handoff changed')
    state = asyncio.run(asyncio.wait_for(relay(args.repo, packet['target_role'], packet['key'],
                        packet['action']['arguments']['message'], verify, args.recovery_review), 60))
    return 0 if state == 'native_success' else 1


if __name__ == '__main__':
    sys.exit(main())
