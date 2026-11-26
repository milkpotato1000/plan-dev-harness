#!/usr/bin/env python3
"""Preview/apply explicit local roles and lifecycle hooks, preserving user configuration."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shlex
import sys
import tempfile
import session_registry as registry


def digest(data):return hashlib.sha256(data).hexdigest()


def encoded(data):return (json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()


def before(path):
    registry.no_symlink(path)
    if not path.exists():return None
    if not path.is_file() or path.stat().st_size>registry.LIMIT:raise ValueError('Invalid configuration file')
    return path.read_bytes()


def install(plan, dev, role_reference, hosts=('claude','codex'), apply=False):
    plan, common, pb=registry.repository(plan);dev, other, db=registry.repository(dev)
    if common!=other or plan==dev or pb==db:raise ValueError('Require distinct role worktrees in one Git common-dir')
    policy=registry.read_json(plan/'.harness/policy.json',65536)
    if pb!=policy.get('planning_branch') or db!=policy.get('development_branch'):
        raise ValueError('Explicit mapping conflicts with project role/branch policy')
    if not role_reference or len(role_reference)>1024:raise ValueError('Explicit human role reference required')
    directory=common/'plan-dev-sessions';registry.no_symlink(directory)
    if directory.exists() and directory.stat().st_mode&0o077:raise ValueError('Private registry permissions required')
    cfg=dict(schema_version=1,project_id=registry.project_id(common),roles={
        'plan':dict(worktree=str(plan),branch=pb,role_reference=role_reference),
        'dev':dict(worktree=str(dev),branch=db,role_reference=role_reference)})
    config_path=directory/'config.json';old_config=before(config_path)
    if old_config and json.loads(old_config)!=cfg:
        raise ValueError('Explicit role migration required; existing bindings preserved')
    manifest_path=directory/'hooks-installation.json';old_manifest=before(manifest_path)
    manifest=json.loads(old_manifest) if old_manifest else {'schema_version':1,'entries':{}}
    if manifest.get('schema_version')!=1 or not isinstance(manifest.get('entries'),dict):raise ValueError('Invalid hook ownership manifest')
    changes={config_path:encoded(cfg)}; owned={}; options=[]
    for role,root in [('plan',plan),('dev',dev)]:
        script=root/'scripts/session_registry.py'
        if not script.is_file():raise ValueError('Install/integrate runtime before configuring roles')
        for host in hosts:
            path=root/('.claude/settings.local.json' if host=='claude' else '.codex/hooks.json')
            current=before(path); obj=registry.read_json(path) if current else {}
            if not isinstance(obj,dict):raise ValueError('Settings must be a JSON object')
            # A second config representation can execute commands twice. Preserve it and refuse ambiguity.
            if host=='codex':
                toml=root/'.codex/config.toml'
                raw=before(toml)
                if raw and (b'[hooks' in raw or b'[[hooks' in raw):
                    raise ValueError('Existing inline Codex hooks: integrate explicitly; no second representation')
            else:
                for extra in [root/'.claude/settings.json']:
                    raw=before(extra)
                    if raw and b'session_registry.py' in raw:raise ValueError('Duplicate harness hook in other project layer')
            obj=copy.deepcopy(obj);hooks=obj.setdefault('hooks',{})
            if not isinstance(hooks,dict):raise ValueError('Invalid hooks configuration')
            entry_key=role+':'+host;previous=manifest['entries'].get(entry_key,{})
            command=shlex.join([sys.executable,'-B',str(script),'--repo',str(root),'--host',host,'hook','--role',role])
            entries={}
            for event in registry.EVENTS:
                group=hooks.setdefault(event,[])
                if not isinstance(group,list):raise ValueError('Invalid hook event')
                want={'hooks':[{'type':'command','command':command,'timeout':2}]}
                existing=previous.get(event)
                if existing:
                    if group.count(existing)!=1:raise ValueError('Owned hook customized/missing/duplicated; preserve for review')
                    group.remove(existing)
                for row in group:
                    if not isinstance(row,dict) or not isinstance(row.get('hooks'),list):raise ValueError('Invalid existing hook matcher')
                    if any('session_registry.py' in str(h.get('command','')) for h in row['hooks'] if isinstance(h,dict)):
                        raise ValueError('Unowned or duplicate harness hook; preserve for review')
                group.append(want);entries[event]=want
            owned[entry_key]=entries;changes[path]=encoded(obj)
            # Codex hooks.json is local/private and includes absolute paths. Claude local settings too.
            if os.path.lexists(path) and path.is_symlink():raise ValueError('Symlink hook config')
    if set(manifest['entries'])-set(owned):raise ValueError('Keep existing host selection; removal requires explicit review')
    changes[manifest_path]=encoded({'schema_version':1,'entries':owned})
    # Keep local hook paths out of Git without touching project .gitignore/policy.
    exclude=common/'info/exclude';raw=before(exclude) or b''
    added=raw
    for line in [b'/.claude/settings.local.json',b'/.codex/hooks.json']:
        if line not in raw.splitlines():added+= (b'\n' if added and not added.endswith(b'\n') else b'')+line+b'\n'
    changes[exclude]=added
    originals={p:before(p) for p in changes}
    modes={p:p.stat().st_mode&0o777 for p,raw in originals.items() if raw is not None}
    for path,data in changes.items():
        options.append({'file':str(path),'action':'KEEP' if originals[path]==data else 'CREATE' if originals[path] is None else 'UPDATE'})
    if not apply:return options
    # Same lock as lifecycle prevents registration against half-written mappings. Never unlink lock files.
    existed=directory.exists()
    with registry.locked(directory):
        for p,raw in originals.items():
            if before(p)!=raw:raise ValueError('Configuration changed during preview/apply')
        created_dirs=[];done=[]
        try:
            for path,data in changes.items():
                if originals[path]==data:continue
                missing=[];parent=path.parent
                while not parent.exists():missing.append(parent);parent=parent.parent
                for parent in reversed(missing):parent.mkdir(mode=0o700);created_dirs.append(parent)
                fd,name=tempfile.mkstemp(prefix='.harness-install-',dir=str(path.parent))
                try:
                    with os.fdopen(fd,'wb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
                    if before(path)!=originals[path]:raise ValueError('Concurrent configuration edit')
                    if path in modes:os.chmod(name,modes[path])
                    os.replace(name,path);done.append(path)
                finally:
                    if os.path.exists(name):os.unlink(name)
        except Exception:
            for path in reversed(done):
                if before(path)!=changes[path]:continue  # never overwrite another writer during rollback
                raw=originals[path]
                if raw is None:path.unlink()
                else:
                    fd,name=tempfile.mkstemp(prefix='.harness-rollback-',dir=str(path.parent))
                    with os.fdopen(fd,'wb') as stream:stream.write(raw)
                    os.chmod(name,modes[path])
                    os.replace(name,path)
            for path in reversed(created_dirs):
                try:path.rmdir()
                except OSError:pass
            raise
    return options


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--plan',required=True);p.add_argument('--dev',required=True)
    p.add_argument('--role-reference',required=True);p.add_argument('--host',choices=('claude','codex','both'),default='both')
    p.add_argument('--apply',action='store_true');a=p.parse_args()
    for row in install(a.plan,a.dev,a.role_reference,('claude','codex') if a.host=='both' else (a.host,),a.apply):
        print(row['action'],row['file'])
    print('Applied local registration hooks.' if a.apply else 'Preview only; repeat with --apply.')
    print('No trust, permission, session, work, pause, approval or delivery was changed.')


if __name__=='__main__':
    try:main()
    except (ValueError,OSError,KeyError,TypeError) as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
