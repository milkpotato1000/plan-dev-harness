# Single-project workspace layout and migration

Use `<parent>/<project>/` as the agent workspace container. Put the primary Git
repository in `<project>_main/` and linked worktrees in `<project>_plan/` and
`<project>_dev/`. Keep the container outside Git. Existing branch names and remotes
are independent of these directory roles.

For a new project, prefer `scripts/bootstrap_workspace.py`; it creates this layout
with shared AGENTS.md and CLAUDE.md entrypoints and verifies initial adoption.
Manual setup uses `git init` in the release child and `git worktree add` for the
planning/development children. Adapt `assets/workspace/AGENTS.md.template` for the
container and record routing in tracked project instructions.

For an existing sibling layout, inventory branches, status (including ignored
runtimes), worktrees, hook configuration, adoption record, active local services
and any absolute environment links. Preserve historical evidence paths: they
record where past commands ran and are not current routing instructions.

The relocation helper requires existing release/plan/dev worktrees, infers branch
roles from `.harness/policy.json` (or explicit branch flags), and refuses dirty,
locked, symlinked or occupied destinations. It previews by default:

```sh
python3 /absolute/skill/scripts/nest_worktrees.py \
  --repo /parent/project --workspace-root /parent/project
# Review output, stop active writers, then repeat with --apply.
```

The helper parks the primary repository in a temporary sibling, creates the
container at its old path, moves the primary into `<project>_main/`, and repairs
linked Git metadata before using `git worktree move` on the other children. It
then verifies unchanged branch tips, status, remotes and hooks configuration,
and writes the workspace AGENTS.md without overwriting custom routing. Running
again with `--repo /parent/project/project_main` is safe when routing is unchanged.
The legacy migration helper writes AGENTS.md only. For Claude Code, add a
CLAUDE.md importing `@AGENTS.md` at the container and child roots, merging any
existing instructions without overwriting them. It never commits, merges, changes
adoption or pushes. On an interrupted operation,
inspect the printed paths and `git worktree list` from the actual primary path;
use `git worktree repair` to reconcile metadata before continuing. Never prune
or delete directories to hide a relocation failure.

After relocation, repair only known local environment links and launcher paths,
or recreate the environment from its lock file if needed. Do not blanket-rewrite
the source tree or committed verification evidence. Restart a local service only
when its captured environment still points at the old paths, preserving its
models/data and startup settings. Verify executable hooks and dev guard at
worktree/index/HEAD, queue from both children and relevant local runtime tests.

Update tracked routing/setup docs on plan, integrate and adopt that reviewed
commit on dev, preserving P-card requirements and execution history. Do not
edit or promote the release branch merely to change its historical path docs.
The container's current path mapping applies until the next explicit release.
Do not change app-internal databases, existing chat records or other projects.
The user can open the container at the same project path and choose plan/dev in
the request; paths embedded in earlier chat messages remain historical.
