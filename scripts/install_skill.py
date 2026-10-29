#!/usr/bin/env python3
"""Install a self-contained Agent Skill. No global settings or repository setup."""
import argparse
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parents[1]


def files():
    names=['SKILL.md','VERSION','LICENSE']
    for folder in ('scripts','assets','references','agents'):
        names.extend(str(p.relative_to(BASE)) for p in (BASE/folder).rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and p.name!='.DS_Store')
    return {n:(BASE/n).read_bytes() for n in names}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--agent',required=True,choices=('codex','claude'))
    p.add_argument('--skills-dir',help='Override the skill parent directory (e.g. project/.agents/skills)')
    p.add_argument('--apply',action='store_true')
    a=p.parse_args()
    parent=Path(a.skills_dir).expanduser().absolute() if a.skills_dir else Path.home()/('.agents/skills' if a.agent=='codex' else '.claude/skills')
    dest=parent/'plan-dev-harness'
    for part in (dest,*dest.parents):
        if part.is_symlink():
            # macOS exposes its system temporary roots through these aliases.
            aliases = {'/var': '/private/var', '/tmp': '/private/tmp'}
            system_alias = (sys.platform == 'darwin' and str(part) in aliases
                            and part.resolve() == Path(aliases[str(part)]))
            if not system_alias:
                raise ValueError('Refusing symlink destination: '+str(part))
    payload=files()
    if dest.exists():
        if not dest.is_dir():raise ValueError('Destination is not a directory')
        actual={str(p.relative_to(dest)) for p in dest.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        if any(p.is_symlink() for p in dest.rglob('*')):raise ValueError('Existing skill contains symlinks')
        if actual!=set(payload) or any((dest/n).read_bytes()!=b for n,b in payload.items()):
            raise ValueError('Existing skill differs. Review/back it up and choose a fresh directory; never overwrite silently.')
        print('KEEP identical skill:',dest)
        return
    print('CREATE',dest,'for',a.agent,'('+str(len(payload))+' files)')
    if not a.apply:
        print('Preview only; repeat with --apply.')
        return
    dest.mkdir(parents=True)
    for n,b in payload.items():
        target=dest/n;target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as stream:stream.write(b)
        if (BASE/n).stat().st_mode&0o111:target.chmod(target.stat().st_mode|0o111)
    print('Installed. Reopen the agent session if discovery has not refreshed.')


if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as exc:
        print('FAIL:',exc,file=sys.stderr);sys.exit(1)
