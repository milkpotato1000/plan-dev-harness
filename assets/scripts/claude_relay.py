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


def reserve(directory, key, arguments, generation):
    with registry.locked(directory):
        path = directory / 'claude-relay-attempts.json'
        attempts = registry.read_json(path) if path.exists() else {}
        if key in attempts or len(attempts) >= 128:
            raise ValueError('Duplicate attempt or full ledger')
        attempts[key] = dict(status='unknown', payload=digest(arguments['message']),
                             generation=generation, at=registry.moment().isoformat())
        registry.atomic_json(path, attempts)


async def relay(repo, role, key, message, verify):
    import claude_agent_sdk as sdk
    root, directory, cfg = registry.config_for(repo)
    peer = current_peers(root)[role]
    arguments = {'to': address(peer['session_id']), 'message': message}
    listed = attempted = False
    result_status = 'unknown'
    trace = []
    verify()
    reserve(directory, key, arguments, peer['generation'])

    async def before(event, ident, context):
        nonlocal attempted
        name, args = event['tool_name'], event['tool_input']
        trace.append({'tool': name, 'target_matches': args.get('to') == arguments['to'],
                      'body_matches': args.get('message') == message, 'exact': exact_send(args, arguments)})
        valid = name == 'ListAgents' and args == {} and not listed
        if name == 'SendMessage' and listed and not attempted and exact_send(args, arguments):
            try:
                latest = current_peers(root)[role]
                if address(latest['session_id']) == arguments['to'] and all(latest[k] == peer[k] for k in ('session_id', 'generation')):
                    verify()
                    attempted = valid = True
            except (ValueError, OSError, subprocess.SubprocessError):
                valid = False
        if valid:
            return {}
        return {'hookSpecificOutput': {'hookEventName': 'PreToolUse',
                'permissionDecision': 'deny', 'permissionDecisionReason': 'Outside reviewed handoff'}}

    async def after(event, ident, context):
        nonlocal listed, result_status
        if event['tool_name'] == 'ListAgents':
            listing = str(event.get('tool_response', ''))
            listed = len(re.findall(re.escape(arguments['to']) + r' \[([a-f0-9]+)\]', listing)) == 1
        elif attempted and event['tool_name'] == 'SendMessage' and exact_send(event['tool_input'], arguments):
            response = event.get('tool_response')
            if isinstance(response, dict):
                detail = str(response.get('message', '')).lower()
                if 'held' in detail:
                    result_status = 'held'
                elif 'refus' in detail:
                    result_status = 'refused'
                elif response.get('success') is True:
                    result_status = 'native_success'
        return {}

    with tempfile.TemporaryDirectory() as cwd:
        hooks = {name: [sdk.HookMatcher(hooks=[fn], on_failure='block')]
                 for name, fn in [('PreToolUse', before), ('PostToolUse', after)]}
        options = sdk.ClaudeAgentOptions(cwd=cwd, cli_path=shutil.which('claude'),
            tools=['ListAgents', 'SendMessage'], strict_mcp_config=True, hooks=hooks,
            permission_mode='default', extra_args={'safe-mode': None, 'no-session-persistence': None,
            'permission-prompts': 'none'}, max_budget_usd=0.5, max_turns=4, max_buffer_size=262144)
        async with sdk.ClaudeSDKClient(options=options) as client:
            await client.query('Call ListAgents once. Then call SendMessage exactly once with this JSON. Stop on any failure. ' + json.dumps({**arguments, 'summary': 'Reviewed handoff'}, ensure_ascii=False))
            async for event in client.receive_response():
                if isinstance(event, sdk.ResultMessage):
                    print(json.dumps({'status': result_status, 'attempted': attempted,
                                      'cost_usd': event.total_cost_usd, 'trace': trace}))
    with registry.locked(directory):
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
                        packet['action']['arguments']['message'], verify), 60))
    return 0 if state == 'native_success' else 1


if __name__ == '__main__':
    sys.exit(main())
