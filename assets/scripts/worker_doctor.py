#!/usr/bin/env python3
"""Read-only worker preflight. Never approves, sends, adopts, starts or retries work."""
import argparse
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys


def command(args, cwd):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', PYTHONDONTWRITEBYTECODE='1')
    result = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, timeout=20)
    if result.returncode:
        raise ValueError('Read failed: ' + ' '.join(args[:2]))
    return result.stdout.strip()


def repository(path):
    root = Path(path).expanduser().resolve()
    top = Path(command(['git', 'rev-parse', '--show-toplevel'], root)).resolve()
    if root != top:
        raise ValueError('Binding must name the actual worktree root')
    common = Path(command(['git', 'rev-parse', '--git-common-dir'], root))
    if not common.is_absolute():
        common = root / common
    return dict(root=str(root), common=str(common.resolve()),
                branch=command(['git', 'branch', '--show-current'], root),
                dirty=bool(command(['git', 'status', '--porcelain'], root)))


def diagnose(repo, binding=None, live_inventory=None, now=None):
    """Supplied binding is an observation, not a trust/authorization certificate."""
    state = repository(repo)
    policy = json.loads((Path(state['root']) / '.harness/policy.json').read_text())
    queue = json.loads(command([sys.executable, '-B', 'scripts/work_queue.py', '--owner', 'all', '--json'], state['root']))
    problems, notes = [], []
    result = dict(schema_version=1, repository=state, mode='unbound',
                  binding_evidence='none', dispatch='pending', execution='unknown',
                  performs_actions=False, issues=problems, notes=notes,
                  pending_decisions=len(queue.get('pending_decisions', [])),
                  paused_sessions=len(queue.get('paused_sessions', [])),
                  next_dev=queue.get('next', {}).get('dev'),
                  host_inventory='not_requested' if live_inventory is None else 'live_cli_only')
    if not binding:
        problems.append('worker_binding_missing')
        return result
    if not isinstance(binding, dict) or binding.get('schema_version') != 1:
        raise ValueError('Expected binding schema_version 1')
    result['mode'] = binding.get('mode', 'unknown')
    result['binding_evidence'] = 'supplied_observation_not_independently_authenticated'
    if result['mode'] not in ('simulation', 'host_observation'):
        problems.append('observation_mode_unknown')
    try:
        observed = datetime.datetime.fromisoformat(binding.get('observed_at', '').replace('Z', '+00:00'))
        current = now or datetime.datetime.now(datetime.timezone.utc)
        age = (current - observed).total_seconds()
        if not 0 <= age <= 300:
            problems.append('observation_stale_or_future')
    except (ValueError, TypeError):
        problems.append('observation_time_unknown')
    host = binding.get('host')
    if host not in ('claude', 'codex'):
        problems.append('host_unknown')
    if live_inventory is not None and host != 'claude':
        problems.append('inventory_host_mismatch')
    sessions = []
    for role, branch_key in [('plan', 'planning_branch'), ('dev', 'development_branch')]:
        row = binding.get(role)
        if not isinstance(row, dict):
            problems.append(role + '_binding_missing')
            continue
        if row.get('role') != role or not row.get('role_reference'):
            problems.append(role + '_role_unconfirmed')
        if not row.get('session_id') or not row.get('host_id'):
            problems.append(role + '_identity_missing')
        sessions.append((row.get('host_id'), row.get('session_id')))
        actual = repository(row.get('worktree', '')) if row.get('worktree') else None
        if not actual or actual['common'] != state['common']:
            problems.append(role + '_wrong_project')
        if not actual or actual['branch'] != policy[branch_key]:
            problems.append(role + '_wrong_branch')
        if type(row.get('writer_count')) is not int or row['writer_count'] != 1:
            problems.append(role + '_writer_unconfirmed_or_conflicting')
        if row.get('status') not in ('idle', 'busy'):
            problems.append(role + '_session_unavailable')
        if live_inventory is not None:
            matches = [item for item in live_inventory if item.get('sessionId') == row.get('session_id')]
            if len(matches) != 1:
                problems.append(role + '_not_unique_in_visible_inventory')
            elif not row.get('session_cwd') or Path(matches[0].get('cwd', '')).resolve() != Path(row['session_cwd']).resolve():
                problems.append(role + '_inventory_cwd_mismatch')
    if len(sessions) == 2 and sessions[0] == sessions[1]:
        problems.append('same_session')
    if all(isinstance(binding.get(r), dict) and binding[r].get('worktree') for r in ('plan', 'dev')):
        if Path(binding['plan']['worktree']).resolve() == Path(binding['dev']['worktree']).resolve():
            problems.append('same_worktree')
    capabilities = binding.get('capabilities', {})
    required = ('ListAgents', 'SendMessage') if host == 'claude' else ('list_threads', 'read_thread', 'send_message_to_thread')
    if not isinstance(capabilities, dict) or not all(capabilities.get(tool) is True for tool in required):
        problems.append('native_tools_unconfirmed')
    if not binding.get('capability_reference') or not binding.get('provider') or not binding.get('host_version'):
        problems.append('host_capability_evidence_missing')
    if binding.get('inbound') != 'accept':
        problems.append('inbound_' + str(binding.get('inbound', 'unknown')))
    if not binding.get('human_authority_reference'):
        problems.append('human_authority_unconfirmed')
    # A supplied acceptance record never establishes actual delivery or authority.
    transport = binding.get('transport', 'not_attempted')
    result['transport_observation'] = transport
    if transport in ('held', 'refused', 'unknown', 'failed'):
        problems.append('transport_' + transport)
    if transport not in ('not_attempted', 'sent', 'received', 'held', 'refused', 'unknown', 'failed'):
        problems.append('transport_unrecognized')
    if problems:
        result['dispatch'] = 'pending'
    else:
        result['dispatch'] = 'simulation_only' if result['mode'] == 'simulation' else 'preflight_consistent'
    if isinstance(binding.get('dev'), dict) and binding['dev'].get('status') == 'busy':
        result['execution'] = 'defer_to_safe_boundary'
        notes.append('preserve_current_work_failures_and_adoption')
    elif queue.get('next', {}).get('dev'):
        result['execution'] = 'queue_eligible_requires_exact_application_and_host_checks'
    else:
        result['execution'] = 'no_eligible_adopted_work'
    notes.extend(['no_dispatch_or_execution_authorization', 'fresh_host_check_required_before_send',
                  'no_plan_implementation_fallback', 'do_not_retry_unknown_send',
                  'queue_keeps_scoped_stops_and_open_decisions'])
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='.')
    parser.add_argument('--binding', help='Private JSON observation; never commit identities')
    parser.add_argument('--claude-inventory', action='store_true', help='Read official claude agents --json; does not prove native tool access')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args(argv)
    binding = json.loads(Path(args.binding).read_text()) if args.binding else None
    inventory = None
    inventory_error = None
    if args.claude_inventory:
        try:
            raw = json.loads(command(['claude', 'agents', '--json'], Path(args.repo).resolve()))
            inventory = raw if isinstance(raw, list) else raw.get('agents', raw.get('sessions', []))
            if not isinstance(inventory, list) or not all(isinstance(r, dict) for r in inventory):
                raise ValueError('Invalid inventory')
        except (ValueError, OSError, subprocess.TimeoutExpired):
            inventory_error = 'unavailable_in_this_execution_environment'
    result = diagnose(args.repo, binding, inventory)
    if inventory_error:
        result['host_inventory'] = inventory_error
        result['dispatch'] = 'pending'
        result['issues'].append('live_inventory_unavailable')
    if inventory == []:
        result['notes'].append('empty_visible_inventory_is_not_proof_no_host_sessions_exist')
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print('Dispatch:', result['dispatch'], '| Execution:', result['execution'])
        print('Issues:', ', '.join(result['issues']) or 'none in supplied observations')
        print('Read only; no approval, message, adoption, process or retry was performed.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(json.dumps({'error': str(exc), 'dispatch': 'pending', 'performs_actions': False}), file=sys.stderr)
        sys.exit(1)
