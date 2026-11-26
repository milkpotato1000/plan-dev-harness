#!/usr/bin/env python3
"""Project-local lifecycle observations. Registration never starts or approves work."""
import argparse
from contextlib import contextmanager
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile

SCHEMA = 1
LIMIT = 1024 * 1024
TTL = 300
HOSTS = ('claude', 'codex')
EVENTS = ('SessionStart', 'UserPromptSubmit', 'Stop', 'SessionEnd')


def git(root, *args):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True,
                       timeout=3, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
    if p.returncode:
        raise ValueError('Git identity unavailable')
    return p.stdout.strip()


def repository(root):
    root = Path(root).resolve()
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root:
        raise ValueError('Expected explicit worktree root')
    common = Path(git(root, 'rev-parse', '--git-common-dir'))
    common = (root / common).resolve() if not common.is_absolute() else common.resolve()
    branch = git(root, 'branch', '--show-current')
    if not branch:
        raise ValueError('Detached HEAD cannot bind a role')
    return root, common, branch


def project_id(common):
    return hashlib.sha256(str(common).encode()).hexdigest()


def no_symlink(path):
    path = Path(path)
    for part in (path, *path.parents):
        if part.is_symlink():
            aliases={'/var':'/private/var','/tmp':'/private/tmp'}
            if sys.platform=='darwin' and str(part) in aliases and part.resolve()==Path(aliases[str(part)]):
                continue
            raise ValueError('Symlink configuration/registry is not supported')
    return path


def read_json(path, limit=LIMIT):
    path = no_symlink(path)
    fd = os.open(str(path), os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
            raise ValueError('Oversized or nonregular JSON file')
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise ValueError('JSON size limit exceeded')
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise ValueError('Duplicate JSON key')
            result[k] = v
        return result
    return json.loads(raw, object_pairs_hook=pairs)


def atomic_json(path, data):
    path = no_symlink(path)
    raw = (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
    if len(raw) > LIMIT:
        raise ValueError('Registry size limit exceeded')
    fd, temp = tempfile.mkstemp(prefix='.write-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw); stream.flush(); os.fsync(stream.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


@contextmanager
def locked(directory):
    directory = no_symlink(directory)
    directory.mkdir(mode=0o700, exist_ok=True)
    if directory.stat().st_mode & 0o077:
        raise ValueError('Registry directory must be private (0700)')
    path = no_symlink(directory / 'lock')
    fd = os.open(str(path), os.O_CREAT | os.O_RDWR | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError('Nonregular registry lock')
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Registry busy; retry only at a normal later event')
        yield
    finally:
        os.close(fd)  # kernel releases lock even after a crash; no stale lock deletion


def moment(value=None):
    value = dt.datetime.now(dt.timezone.utc) if value is None else value
    if isinstance(value, str):
        value = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if not isinstance(value, dt.datetime):
        raise ValueError('Invalid observation time')
    if value.tzinfo is None:
        raise ValueError('Timezone required')
    return value.astimezone(dt.timezone.utc)


def config_for(repo):
    root, common, branch = repository(repo)
    directory = common / 'plan-dev-sessions'
    cfg = read_json(directory / 'config.json', 65536)
    if not isinstance(cfg, dict) or cfg.get('schema_version') != SCHEMA or cfg.get('project_id') != project_id(common):
        raise ValueError('Project configuration mismatch')
    roles = cfg.get('roles')
    if not isinstance(roles, dict) or set(roles) != {'plan', 'dev'}:
        raise ValueError('Explicit plan/dev mappings required')
    for role, row in roles.items():
        if not isinstance(row, dict) or not row.get('role_reference'):
            raise ValueError('Explicit role reference missing')
        actual, shared, actual_branch = repository(row['worktree'])
        if shared != common or str(actual) != row['worktree'] or actual_branch != row['branch']:
            raise ValueError('Role worktree/branch/project changed; reconfigure explicitly')
    if roles['plan']['worktree'] == roles['dev']['worktree']:
        raise ValueError('Roles must have separate worktrees')
    return root, directory, cfg


def empty_registry(cfg):
    return dict(schema_version=SCHEMA, project_id=cfg['project_id'], revision=0,
                records={}, conflicts={}, retired=[])


def identity(host, sid):
    if host not in HOSTS or not isinstance(sid, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,160}', sid):
        raise ValueError('Invalid host/session identity')
    return hashlib.sha256((host + ':' + sid).encode()).hexdigest()


def load_registry(directory, cfg):
    path = directory / 'registry.json'
    if not path.exists():
        return empty_registry(cfg)
    r = read_json(path)
    if (not isinstance(r, dict) or r.get('schema_version') != SCHEMA or r.get('project_id') != cfg['project_id']
            or type(r.get('revision')) is not int or r['revision'] < 0
            or not isinstance(r.get('records'), dict) or set(r['records']) - {'plan', 'dev'}
            or not isinstance(r.get('conflicts'), dict) or len(r['conflicts']) > 16
            or not isinstance(r.get('retired'), list) or len(r['retired']) > 64):
        raise ValueError('Invalid registry schema; preserve for inspection')
    for role, row in r['records'].items():
        if (not isinstance(row, dict) or row.get('role') != role
                or type(row.get('generation')) is not int or row['generation'] < 1
                or row['generation'] > r['revision'] or row.get('state') not in ('idle', 'busy', 'ended')
                or row.get('project_id') != cfg['project_id']
                or row.get('worktree') != cfg['roles'][role]['worktree']
                or row.get('branch') != cfg['roles'][role]['branch']
                or row.get('identity') != identity(row.get('host'), row.get('session_id'))):
            raise ValueError('Invalid session row')
        if not isinstance(row.get('observed_at'),str):raise ValueError('Missing observation timestamp')
        moment(row['observed_at'])
    for key, row in r['conflicts'].items():
        if not re.fullmatch('[0-9a-f]{64}', key) or not isinstance(row, dict) or row.get('role') not in ('plan', 'dev'):
            raise ValueError('Invalid conflict row')
        if not isinstance(row.get('observed_at'),str):raise ValueError('Missing observation timestamp')
        moment(row['observed_at'])
    if any(not isinstance(x, str) or not re.fullmatch('[0-9a-f]{64}', x) for x in r['retired']):
        raise ValueError('Invalid retired identities')
    return r


def lifecycle(repo, role, host, event, expected_generation=None, now=None, inventory=None):
    root, directory, cfg = config_for(repo)
    mapping = cfg['roles'].get(role)
    if not mapping or root != Path(mapping['worktree']):
        raise ValueError('Explicit role does not match configured worktree')
    if not isinstance(event, dict) or event.get('hook_event_name') not in EVENTS:
        raise ValueError('Unsupported lifecycle event')
    # Host-selected arbitrary transcripts/prompts/tool payloads are never retained or read.
    sid = event.get('session_id'); key = identity(host, sid)
    cwd = event.get('cwd')
    if not isinstance(cwd, str) or not Path(cwd).is_absolute() or Path(cwd).resolve() != root:
        raise ValueError('Host cwd differs from explicit role; shared-parent app entry needs its own binding')
    name = event['hook_event_name']; current = moment(now)
    with locked(directory):
        r = load_registry(directory, cfg); row = r['records'].get(role)
        for old in list(r['records'].values()) + list(r['conflicts'].values()):
            if moment(old['observed_at']) > current:
                raise ValueError('Clock regression/future observation; no mutation')
        if expected_generation is not None and (not row or row['generation'] != expected_generation):
            return {'status':'stale_generation_ignored','performs_work':False}
        if key in r['retired']:
            return {'status':'retired_identity_ignored','performs_work':False}
        if name == 'SessionEnd':
            if key in r['conflicts']:
                del r['conflicts'][key]
            elif row and row['identity'] == key:
                row['state'] = 'ended'; row['observed_at'] = current.isoformat()
            else:
                return {'status':'old_end_ignored','performs_work':False}
        elif row and row['identity'] != key:
            # A matching explicit end is needed. TTL/absence/name matching never authorize takeover.
            if name == 'SessionStart' and row['state'] == 'ended' and not any(c['role'] == role for c in r['conflicts'].values()):
                if len(r['retired']) >= 64:
                    raise ValueError('Retired identity bound reached; explicit maintenance required')
                rows = inventory if inventory is not None else (inventory_for_claude() if host == 'claude' else [])
                if not replacement_proven(rows, host, sid, root, row):
                    return {'status':'replacement_host_proof_required','performs_work':False}
                r['retired'].append(row['identity']); row = None
            else:
                if key not in r['conflicts'] and len(r['conflicts']) >= 16:
                    raise ValueError('Conflict bound reached; no registration')
                r['conflicts'][key] = {'role':role,'observed_at':current.isoformat()}
                r['revision'] += 1; atomic_json(directory/'registry.json', r)
                return {'status':'writer_conflict','performs_work':False}
        elif row and row['state'] == 'ended' and name != 'SessionEnd':
            # Same-ID late end versus resume cannot be distinguished by hook stdin alone.
            # Keep ended, never create a new writer from this ambiguous sequence.
            rows = inventory if inventory is not None else (inventory_for_claude() if host == 'claude' else [])
            if name != 'SessionStart' or not replacement_proven(rows, host, sid, root):
                return {'status':'ended_identity_resume_needs_host_review','performs_work':False}
            row['state'] = 'idle'
        if name != 'SessionEnd':
            if row is None:
                if name != 'SessionStart':
                    return {'status':'start_required','performs_work':False}
                if any(x['identity'] == key for x in r['records'].values()):
                    raise ValueError('Same session cannot own both roles')
                row = dict(role=role, host=host, session_id=sid, identity=key,
                    project_id=cfg['project_id'], worktree=str(root), branch=mapping['branch'],
                    generation=r['revision']+1, state='idle', source='official_lifecycle_stdin',
                    capabilities=['lifecycle_observed'])
                r['records'][role] = row
            if name == 'UserPromptSubmit':row['state'] = 'busy'
            elif name == 'Stop':row['state'] = 'idle'
            row['observed_at'] = current.isoformat()
        r['revision'] += 1; atomic_json(directory/'registry.json', r)
        return {'status':'registered' if name != 'SessionEnd' else 'end_observed',
                'generation':row['generation'] if row else None,'performs_work':False}


def replacement_proven(rows, host, sid, root, old=None):
    """Fresh host observation, never TTL or absence alone. Caller supplies official inventory."""
    if not isinstance(rows, list):return False
    same=[x for x in rows if isinstance(x,dict) and x.get('cwd') and Path(x['cwd']).resolve()==root]
    if len(same)!=1 or same[0].get('sessionId')!=sid or same[0].get('status') not in ('idle','busy'):
        return False
    return not old or (old['host']==host and not any(x.get('sessionId')==old['session_id'] for x in rows))


def inventory_for_claude():
    p = subprocess.run(['claude','agents','--json'],capture_output=True,text=True,timeout=5)
    if p.returncode or len(p.stdout) > LIMIT:
        raise ValueError('Official inventory unavailable')
    rows = json.loads(p.stdout)
    if not isinstance(rows, list):raise ValueError('Unexpected inventory schema')
    return rows


def diagnose(repo, host, inventory=None, now=None, private=False):
    root, directory, cfg = config_for(repo); r = load_registry(directory, cfg)
    current = moment(now); issues=[]; peers={}
    # Discovery is read-only, including when configuration/registry is absent or stale.
    for role in ('plan','dev'):
        row = r['records'].get(role)
        if not row:issues.append(role+'_missing');continue
        if row['host'] != host:issues.append(role+'_cross_host_transport_unavailable')
        if row['state'] == 'ended':issues.append(role+'_ended')
        if not 0 <= (current-moment(row['observed_at'])).total_seconds() <= TTL:issues.append(role+'_stale_or_future')
        if any(c['role']==role for c in r['conflicts'].values()):issues.append(role+'_writer_conflict')
        if inventory is None:
            issues.append(role+'_fresh_host_inventory_required')
        else:
            matches=[x for x in inventory if x.get('sessionId')==row['session_id']]
            if len(matches)!=1 or not isinstance(matches[0].get('cwd'),str) or not Path(matches[0]['cwd']).is_absolute() or Path(matches[0]['cwd']).resolve()!=Path(row['worktree']):
                issues.append(role+'_host_identity_mismatch')
            elif len([x for x in inventory if x.get('cwd') and Path(x['cwd']).resolve()==Path(row['worktree'])]) != 1:
                issues.append(role+'_multiple_host_writers')
            elif matches[0].get('status') not in ('idle','busy'):
                issues.append(role+'_host_status_unknown')
        peers[role]={k:row[k] for k in ('role','host','generation','state','observed_at')}
        if private:peers[role]['session_id']=row['session_id']
    queue = None
    p = subprocess.run([sys.executable,'-B',str(root/'scripts/work_queue.py'),'--owner','all','--json'],
                       cwd=root,capture_output=True,text=True,timeout=5,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1'))
    if not p.returncode:
        queue=json.loads(p.stdout)
    else:issues.append('workflow_queue_unavailable')
    if queue and (queue.get('paused_sessions') or queue.get('pending_decisions')):
        issues.append('workflow_stops_or_open_require_scoped_review')
    return dict(schema_version=1,registration='observations_only',dispatch='pending' if issues else 'identity_consistent',
        issues=issues,peers=peers,performs_actions=False,execution='not_authorized_by_registration',
        next_dev=(queue or {}).get('next',{}).get('dev'),
        notes=['Recheck exact reviewed handoff, real human grant and recipient capabilities before send.',
               'Busy dev preserves current P and applies pending work only at a safe boundary.',
               'Empty/incomplete host inventory is not evidence that another writer is dead.'])


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',default='.')
    p.add_argument('--host',choices=HOSTS,required=True)
    sub=p.add_subparsers(dest='command',required=True)
    hook=sub.add_parser('hook');hook.add_argument('--role',choices=('plan','dev'),required=True)
    reconnect=sub.add_parser('reconnect');reconnect.add_argument('--role',choices=('plan','dev'),required=True);reconnect.add_argument('--host-observation',required=True)
    doctor=sub.add_parser('doctor');doctor.add_argument('--live',action='store_true');doctor.add_argument('--private',action='store_true')
    a=p.parse_args(argv)
    if a.command=='hook':
        raw=sys.stdin.buffer.read(65537)
        if len(raw)>65536:raise ValueError('Hook input too large')
        result=lifecycle(a.repo,a.role,a.host,json.loads(raw))
        # No stdout developer context, no decision/permission fields, no prompt collection.
        print('plan-dev-harness: '+result['status'],file=sys.stderr)
    elif a.command=='reconnect':
        from session_handoff import host_rows
        rows=host_rows(a.host_observation,a.host)
        root=Path(a.repo).resolve();matches=[r for r in rows if r.get('cwd') and Path(r['cwd']).resolve()==root]
        if len(matches)!=1 or matches[0].get('status') not in ('idle','busy'):
            raise ValueError('Unique actual host session required')
        event=dict(session_id=matches[0]['sessionId'],cwd=str(root),hook_event_name='SessionStart')
        print(json.dumps(lifecycle(root,a.role,a.host,event,inventory=rows),indent=2))
    else:
        rows=inventory_for_claude() if a.live and a.host=='claude' else None
        print(json.dumps(diagnose(a.repo,a.host,rows,private=a.private),indent=2))
    return 0


if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,OSError,KeyError,TypeError,subprocess.TimeoutExpired) as e:
        print('plan-dev-harness: pending ('+type(e).__name__+')',file=sys.stderr)
        sys.exit(1)
