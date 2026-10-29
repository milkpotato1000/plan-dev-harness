#!/usr/bin/env python3
"""Create a new local-only nested workspace; preview by default, never publish."""
import argparse
from pathlib import Path
import re
import shlex
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]


def run(*cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--parent', required=True)
    p.add_argument('--name', required=True)
    p.add_argument('--plan-branch', default='plan')
    p.add_argument('--dev-branch', default='dev')
    p.add_argument('--release-branch', default='main')
    p.add_argument('--author-name')
    p.add_argument('--author-email')
    p.add_argument('--apply', action='store_true')
    a = p.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', a.name):
        raise ValueError('Use a short project name containing letters, digits, hyphens or underscores')
    parent = Path(a.parent).expanduser().resolve()
    if not parent.is_dir():
        raise ValueError('Parent directory must exist')
    # Do not silently create nested repositories in another checkout.
    probe = subprocess.run(['git','-C',str(parent),'rev-parse','--show-toplevel'], capture_output=True)
    if probe.returncode == 0:
        raise ValueError('Choose a parent outside an existing Git worktree')
    branches = (a.plan_branch,a.dev_branch,a.release_branch)
    if len(set(branches)) != 3:
        raise ValueError('Branches must be distinct')
    for branch in branches:
        run('git','check-ref-format','--branch',branch)
    if bool(a.author_name) != bool(a.author_email):
        raise ValueError('Supply both author fields or neither; global identity is never changed')
    root = parent/a.name
    if root.exists() or root.is_symlink():
        raise ValueError('Destination must be absent; existing work is never replaced')
    hook = subprocess.run(['git','config','--get','core.hooksPath'],cwd=parent,capture_output=True,text=True)
    if hook.returncode == 0:
        raise ValueError('A parent/global hooksPath exists; integrate it manually before bootstrap')
    if not a.author_name:
        run('git','var','GIT_AUTHOR_IDENT',cwd=parent)
        run('git','var','GIT_COMMITTER_IDENT',cwd=parent)
    for role in ('main','plan','dev'):
        print('CREATE',root/(a.name+'_'+role))
    print('Create initial infrastructure commit, exact dev adoption, then activate local Git hooks. No remotes/push.')
    if not a.apply:
        print('Preview only; repeat with --apply.')
        return
    root.mkdir()
    primary=root/(a.name+'_main'); plan=root/(a.name+'_plan');dev=root/(a.name+'_dev')
    run('git','init','-b',a.release_branch,str(primary))
    if a.author_name:
        run('git','config','user.name',a.author_name,cwd=primary)
        run('git','config','user.email',a.author_email,cwd=primary)
    run(sys.executable,str(BASE/'scripts/install_harness.py'),'--repo',str(primary),
        '--plan-branch',a.plan_branch,'--dev-branch',a.dev_branch,'--release-branch',a.release_branch,
        '--protect','docs/planning','--protect','docs/architecture','--agent','both','--apply')
    workspace=(BASE/'assets/workspace/AGENTS.md.template').read_text()
    for key,value in {'PROJECT':a.name,'PLAN_BRANCH':a.plan_branch,'DEV_BRANCH':a.dev_branch,
        'RELEASE_BRANCH':a.release_branch,'PLAN_DIR_QUOTED':shlex.quote(a.name+'_plan'),
        'DEV_DIR_QUOTED':shlex.quote(a.name+'_dev')}.items():
        workspace=workspace.replace('{{'+key+'}}',value)
    (root/'AGENTS.md').write_text(workspace)
    (root/'CLAUDE.md').write_text('@AGENTS.md\n')
    (primary/'docs/process/workspace-AGENTS.md').write_text(workspace)
    (primary/'README.md').write_text('# '+a.name+'\n\nProject workspace initialized; no product work is approved.\n')
    (primary/'.gitignore').write_text('__pycache__/\n*.pyc\n.venv/\n.DS_Store\n')
    run('git','add','AGENTS.md','CLAUDE.md','README.md','.gitignore','.harness','.githooks','scripts','docs',cwd=primary)
    run('git','commit','-m','Initialize plan/dev infrastructure',cwd=primary)
    sha=run('git','rev-parse','HEAD',cwd=primary)
    run('git','worktree','add','-b',a.plan_branch,str(plan),sha,cwd=primary)
    run('git','worktree','add','-b',a.dev_branch,str(dev),sha,cwd=primary)
    run(sys.executable,'scripts/contract_guard.py','adopt',sha,'--review-reference','Local workspace bootstrap infrastructure only; no product approval',cwd=dev)
    run('git','add','.harness/adopted-plan.json',cwd=dev)
    run('git','commit','-m','Record initial plan adoption',cwd=dev)
    run(sys.executable,'scripts/contract_guard.py','install',cwd=dev)
    run(sys.executable,'scripts/contract_guard.py','check',cwd=dev)
    print('Created',root,'adopted plan',sha)
    print('Open the container in either agent; initialize plan/dev roles explicitly. Queue is empty.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError,OSError) as exc:
        print('FAIL:',exc,'\nIf creation began, partial files are preserved for inspection.',file=sys.stderr)
        sys.exit(1)
