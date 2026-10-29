#!/usr/bin/env python3
"""Preview or nest existing release/plan/dev worktrees in one project container."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile

TEMPLATE = Path(__file__).resolve().parents[1] / 'assets/workspace/AGENTS.md.template'


def git(root, *args, required=True):
    result = subprocess.run(['git', '-C', str(root), *args], text=True, capture_output=True)
    if required and result.returncode:
        raise ValueError(result.stderr.strip() or 'Git check failed')
    return result.stdout.strip()


def worktrees(root):
    raw = subprocess.run(['git', '-C', str(root), 'worktree', 'list', '--porcelain', '-z'],
                         text=True, capture_output=True, check=True).stdout
    records, current = [], {}
    for field in raw.split('\0'):
        if not field:
            if current:
                records.append(current)
                current = {}
            continue
        key, _, value = field.partition(' ')
        current[key] = value
    return records


def snapshot(root):
    return (git(root, 'rev-parse', 'HEAD'), git(root, 'symbolic-ref', 'HEAD'),
            git(root, 'status', '--porcelain=v1', '--untracked-files=all'),
            git(root, 'config', '--get-regexp', r'^remote\..*\.url$', required=False),
            git(root, 'config', '--get', 'core.hooksPath', required=False))


def organize(args):
    source = Path(args.repo).expanduser().absolute()
    workspace = Path(args.workspace_root).expanduser().absolute()
    for path in (source, workspace):
        if any(part.is_symlink() for part in (path, *path.parents)):
            raise ValueError('Use real paths, not symlinks: ' + str(path))
    source = source.resolve()
    workspace = workspace.resolve()
    if Path(git(source, 'rev-parse', '--show-toplevel')).resolve() != source:
        raise ValueError('--repo must name the primary repository root')
    if not (source / '.git').is_dir():
        raise ValueError('--repo must name the primary worktree containing the .git directory')
    if git(source, 'config', '--get', 'core.worktree', required=False):
        raise ValueError('Review explicit core.worktree configuration before moving')
    name = args.project_name or workspace.name
    if (not name or name in ('.', '..', '.git') or Path(name).name != name
            or any(c in name for c in '\\\n\r\0') or '{{' in name):
        raise ValueError('Project name must be a single plain directory name')
    config_path = source / '.harness/policy.json'
    config = json.loads(config_path.read_text()) if config_path.exists() else {}
    branches = {
        'main': args.release_branch or config.get('release_branch', 'main'),
        'plan': args.plan_branch or config.get('planning_branch', 'plan'),
        'dev': args.dev_branch or config.get('development_branch', 'dev'),
    }
    if len(set(branches.values())) != 3:
        raise ValueError('Branch roles must be distinct')
    records = worktrees(source)
    locations = {}
    for role, branch in branches.items():
        matches = [r for r in records if r.get('branch') == 'refs/heads/' + branch]
        if len(matches) != 1:
            raise ValueError('Expected one existing worktree for branch ' + branch)
        record = matches[0]
        if 'locked' in record or 'prunable' in record:
            raise ValueError('Locked or missing worktree requires review: ' + branch)
        location = Path(record['worktree'])
        if location.is_symlink() or not location.is_dir():
            raise ValueError('Worktree must be an existing real directory: ' + str(location))
        locations[role] = location.resolve()
        if any(line.startswith('160000 ') for line in git(location, 'ls-files', '--stage').splitlines()):
            raise ValueError('Worktree with submodules needs explicit migration review: ' + str(location))
    if locations['main'] != source:
        raise ValueError('The primary worktree must be on the configured release branch')
    destinations = {r: workspace / (name + '_' + r) for r in branches}
    relocating_primary = source != destinations['main']
    if relocating_primary and workspace != source and workspace.is_relative_to(source):
        raise ValueError('New workspace cannot be inside the existing primary repository')
    if relocating_primary and workspace != source and os.path.lexists(workspace):
        raise ValueError('New workspace already exists: ' + str(workspace))
    before = {}
    for role, location in locations.items():
        if role != 'main' and workspace.is_relative_to(location):
            raise ValueError('Workspace cannot be inside a linked worktree: ' + str(location))
        if role != 'main' and relocating_primary and location.is_relative_to(source):
            raise ValueError('Move already-nested linked worktrees explicitly before this migration')
        target = destinations[role]
        if location != target and os.path.lexists(target):
            raise ValueError('Destination already exists: ' + str(target))
        before[role] = snapshot(location)
        if before[role][2]:
            raise ValueError('Preserve/finish current changes before moving: ' + str(location))
        print(('KEEP ' if location == target else 'MOVE ') + str(location) + ' -> ' + str(target))
    text = TEMPLATE.read_text()
    replacements = {'PROJECT': name, 'PLAN_BRANCH': branches['plan'],
                    'DEV_BRANCH': branches['dev'], 'RELEASE_BRANCH': branches['main'],
                    'PLAN_DIR_QUOTED': shlex.quote(name + '_plan'),
                    'DEV_DIR_QUOTED': shlex.quote(name + '_dev')}
    for key, value in replacements.items():
        text = text.replace('{{' + key + '}}', value)
    entrypoint = workspace / 'AGENTS.md'
    # During legacy migration source/AGENTS.md moves with the release repository.
    existing_entrypoint = workspace != source and os.path.lexists(entrypoint)
    if existing_entrypoint and (entrypoint.is_symlink() or entrypoint.read_text() != text):
        raise ValueError('Existing workspace instructions differ; merge them explicitly: ' + str(entrypoint))
    print(('KEEP ' if existing_entrypoint else 'CREATE ') + str(entrypoint))
    if not args.apply:
        print('Preview only; repeat with --apply after reviewing paths and stopping active writers.')
        return
    # Recheck immediately before the first mutation. Ignored runtimes move intact.
    if any(snapshot(locations[r]) != before[r] for r in branches):
        raise ValueError('Worktree state changed during preflight; inspect again')
    if relocating_primary:
        stage = Path(tempfile.mkdtemp(prefix='.' + name + '-move-', dir=source.parent))
        parked = stage / 'primary'
        try:
            source.rename(parked)
            workspace.mkdir()
            parked.rename(destinations['main'])
        except OSError:
            # Roll back only directories created by this operation; never replace contents.
            if parked.exists():
                if workspace.exists() and not any(workspace.iterdir()):
                    workspace.rmdir()
                if not source.exists():
                    parked.rename(source)
            raise
        finally:
            if not any(stage.iterdir()):
                stage.rmdir()
        locations['main'] = destinations['main']
        # git worktree move cannot move the primary worktree. Repair its linked
        # worktrees' .git files before using git worktree move for those worktrees.
        git(locations['main'], 'worktree', 'repair')
    for role in ('plan', 'dev'):
        if locations[role] != destinations[role]:
            git(locations['main'], 'worktree', 'move', str(locations[role]), str(destinations[role]))
    git(destinations['main'], 'worktree', 'repair')
    if not existing_entrypoint:
        with entrypoint.open('x') as stream:
            stream.write(text)
    common = Path(git(destinations['main'], 'rev-parse', '--git-common-dir'))
    common = (destinations['main'] / common).resolve()
    for role, target in destinations.items():
        if snapshot(target) != before[role]:
            raise ValueError('Post-move state differs; inspect ' + str(target))
        actual = Path(git(target, 'rev-parse', '--git-common-dir'))
        if (target / actual).resolve() != common:
            raise ValueError('Worktrees no longer share one Git repository')
    print('PASS: branch tips, status, remotes and hooks configuration preserved.')
    print('Open Codex at ' + str(workspace))
    print('Review ignored virtualenv links, runtime paths and active local services after relocation.')
    print('No commits, merges, adoption changes or pushes were performed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, help='Existing primary/release worktree')
    parser.add_argument('--workspace-root', required=True, help='Container to open in Codex; may be the old primary path')
    parser.add_argument('--project-name')
    parser.add_argument('--plan-branch')
    parser.add_argument('--dev-branch')
    parser.add_argument('--release-branch')
    parser.add_argument('--apply', action='store_true')
    organize(parser.parse_args())


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
