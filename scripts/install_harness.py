#!/usr/bin/env python3
"""Preview/install local governance; upgrade only untouched managed files."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
ASSETS = BASE / 'assets'
VERSION = (BASE / 'VERSION').read_text().strip()
EXECUTABLE = ('scripts/contract_guard.py', 'scripts/work_queue.py', 'scripts/plan_intake.py', 'scripts/workflow_control.py', '.githooks/pre-commit', '.githooks/pre-push')
GENERATED = (*EXECUTABLE, 'scripts/plan_cards.py', 'docs/planning/plans/_TEMPLATE.md', 'docs/process/work-queue.md', 'docs/process/plan-intake.md', 'docs/process/workflow-controls.md', 'docs/process/optional-adapters.md', 'docs/process/checkpoint-template.md', 'docs/process/handoff-template.md')
GOVERNANCE = ('AGENTS.md', 'CLAUDE.md', 'docs/process', '.harness/policy.json', '.harness/installation.json', 'scripts/contract_guard.py', 'scripts/plan_cards.py', 'scripts/work_queue.py', 'scripts/plan_intake.py', 'docs/planning/plans', 'docs/planning/request-decisions', 'docs/planning/decision-scopes', 'scripts/workflow_control.py', 'docs/progress/sessions/plan.md', 'docs/progress/handoffs/plan', '.githooks')
BASELINE = '.harness/adopted-plan.json'
MANIFEST = '.harness/installation.json'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def git(root, *args, required=True):
    result = subprocess.run(['git', '-C', str(root), *args], text=True, capture_output=True)
    if required and result.returncode:
        raise ValueError(result.stderr.strip() or 'Git check failed')
    return result


def protected_path(value):
    path = Path(value)
    if path.is_absolute() or not path.parts or any(p in ('.', '..', '.git') for p in path.parts):
        raise ValueError('Use a repository-relative protected path: ' + value)
    if any(char in value for char in '*?[:\\\n\r'):
        raise ValueError('Use literal protected paths, not Git pathspec expressions: ' + value)
    normalized = path.as_posix().rstrip('/')
    if BASELINE == normalized or BASELINE.startswith(normalized + '/'):
        raise ValueError('The dev-owned adoption record must not be protected: ' + value)
    return normalized


def safe(root, name):
    dest = root / name
    for part in [dest, *dest.parents]:
        if part == root:
            break
        if part.is_symlink():
            raise ValueError('Refusing symlink destination: ' + str(part))
    return dest


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--plan-branch', default='plan')
    parser.add_argument('--dev-branch', default='dev')
    parser.add_argument('--release-branch', default='main')
    parser.add_argument('--protect', action='append', required=True)
    parser.add_argument('--agent', choices=('none', 'codex', 'claude', 'both'), default='none')
    parser.add_argument('--upgrade', action='store_true')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args(argv)
    candidate = Path(args.repo).expanduser().resolve()
    root = Path(git(candidate, 'rev-parse', '--show-toplevel').stdout.strip()).resolve()
    if candidate != root:
        raise ValueError('--repo must name the repository/worktree root')
    branches = (args.plan_branch, args.dev_branch, args.release_branch)
    if len(set(branches)) != 3:
        raise ValueError('Planning, development and release branches must be distinct')
    for branch in branches:
        git(root, 'check-ref-format', '--branch', branch)
    branch = git(root, 'branch', '--show-current').stdout.strip()
    has_head = git(root, 'rev-parse', '--verify', 'HEAD', required=False).returncode == 0
    if has_head and branch != args.plan_branch:
        raise ValueError('Install/upgrade governance on the configured planning branch; integrate/adopt on dev')
    paths = list(dict.fromkeys([protected_path(p) for p in args.protect] + list(GOVERNANCE)))
    config = dict(planning_branch=args.plan_branch, development_branch=args.dev_branch,
                  release_branch=args.release_branch, protected_paths=paths, baseline_file=BASELINE, p_card_execution=True)
    hook_path = git(root, 'config', '--get', 'core.hooksPath', required=False).stdout.strip()
    if hook_path and hook_path != '.githooks':
        raise ValueError('Integrate the existing hook system first: ' + hook_path)
    if not hook_path:
        default = Path(git(root, 'rev-parse', '--git-path', 'hooks').stdout.strip())
        if not default.is_absolute():
            default = root / default
        if default.exists():
            active = [p.name for p in default.iterdir() if p.is_file() and not p.name.endswith('.sample')]
            if active:
                raise ValueError('Existing default hooks must be integrated: ' + ', '.join(active))
    desired = {name: (ASSETS / name).read_bytes() for name in GENERATED}
    desired['.harness/policy.json'] = (json.dumps(config, indent=2) + '\n').encode()
    if args.agent != 'none':
        desired['AGENTS.md'] = (ASSETS / 'instructions/AGENTS.md').read_bytes()
        desired['docs/process/agent-workflow.md'] = (ASSETS / 'instructions/agent-workflow.md').read_bytes()
    if args.agent in ('claude', 'both'):
        desired['CLAUDE.md'] = b'@AGENTS.md\n'
    manifest_path = safe(root, MANIFEST)
    old = json.loads(manifest_path.read_text()) if manifest_path.exists() else None
    if old is not None and (old.get('schema_version') != 1 or not isinstance(old.get('files'), dict)):
        raise ValueError('Invalid installation manifest')
    if old and set(old['files']) - set(desired):
        raise ValueError('Preserve previous --agent selection; automatic removal is not supported')
    if old and old.get('options') != {'branches': list(branches), 'protect': args.protect, 'agent': args.agent}:
        raise ValueError('Reuse the installed options; branch/policy migration requires explicit manual review')
    desired[MANIFEST] = (json.dumps(dict(schema_version=1, version=VERSION,
        options={'branches':list(branches),'protect':args.protect,'agent':args.agent},
        files={name:digest(raw) for name,raw in desired.items()}), indent=2)+'\n').encode()
    actions = []
    for name, raw in desired.items():
        dest = safe(root, name)
        before = dest.read_bytes() if dest.is_file() else None
        if dest.exists() and not dest.is_file():
            raise ValueError('Destination is not a file: ' + name)
        action = 'KEEP' if before == raw else 'CREATE' if before is None else 'UPDATE'
        if action == 'UPDATE':
            owned = old and (name == MANIFEST or old['files'].get(name) == digest(before))
            if not args.upgrade or not owned:
                raise ValueError('Existing file differs; review/integrate instead of overwriting: ' + name)
        actions.append((name, raw, before, action))
    for name, raw, before, action in actions:
        print(action + ' ' + name)
        if not args.apply:
            continue
        dest = safe(root, name)
        if action == 'CREATE':
            dest.parent.mkdir(parents=True, exist_ok=True)
            with dest.open('xb') as stream:
                stream.write(raw)
        elif action == 'UPDATE':
            if dest.read_bytes() != before:
                raise ValueError('File changed during installation; stop and inspect: ' + name)
            dest.write_bytes(raw)
        if name in EXECUTABLE:
            dest.chmod(dest.stat().st_mode | 0o111)
    print('Applied local files.' if args.apply else 'Preview only; repeat with --apply to write files.')
    print('Commit/integrate, adopt exact plan SHA on dev, then install hooks in every clone.')
    print('No Git configuration, branch, remote, task approval or agent session was changed.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
