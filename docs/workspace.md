# Distribution workspace

Open `plan-dev-harness/` as the single Codex project. It is a non-Git container:

```text
plan-dev-harness/
  AGENTS.md
  CLAUDE.md                 # @AGENTS.md
  plan-dev-harness_plan/    # plan: requirements, review and handoff
  plan-dev-harness_dev/     # dev: implementation, verification, PRs
  plan-dev-harness_main/    # main: release baseline, contains .git/
```

The children are linked worktrees sharing one Git repository and origin
`https://github.com/milkpotato1000/plan-dev-harness.git`. Always set the child
working directory explicitly. Keep plan/dev chats in this single saved project;
creating a chat or opening the folder does not authorize new feature work.

## Existing work preserved

The 2026-10-29 relocation started main at v0.1.0 (`803d658`) and dev at the
implemented v0.2.0 commit (`8bd9414`). Plan was created from the existing planning
commit `362e9857f468cc43414f8029be0efbefa774b2a9`, which is already an ancestor of
dev. Later layout documentation is integrated plan → dev. Plan's original READY
text is a planning record: the completed implementation and verification remain
on dev in `docs/planning/P001-v0.2.0-workflow-controls.md` and
`docs/verification-v0.2.0.md`. Inspect them with `git show dev:<path>`.

PR https://github.com/milkpotato1000/plan-dev-harness/pull/1 remains the dev → main
review. Relocation does not merge or release it. Historical verification paths
remain unchanged because they describe where earlier commands ran.

## Recreate on another computer

After the plan/dev branches are available on origin, from the desired parent:

```sh
mkdir plan-dev-harness
cd plan-dev-harness
git clone https://github.com/milkpotato1000/plan-dev-harness.git plan-dev-harness_main
git -C plan-dev-harness_main worktree add --track -b plan ../plan-dev-harness_plan origin/plan
git -C plan-dev-harness_main worktree add --track -b dev ../plan-dev-harness_dev origin/dev
```

Before running these commands, verify the destinations are absent; reuse existing
clones/worktrees instead of replacing them. Create the container AGENTS.md with
the directory/branch mapping above, explicit child routing, persistent chat roles,
plan → dev integration, and the explicit main promotion requirement. Create the
container CLAUDE.md containing `@AGENTS.md`. These two local files are not part of
a branch push. Tracked child AGENTS.md and CLAUDE.md remain the repository rules.

## Workflow boundary

This is the reusable distribution, not an installed target project. Its source
assets include queue and guard scripts, but this repository does not currently
activate those target-project hooks or an adopted-plan JSON record. Do not run
`python3 scripts/work_queue.py` or `python3 scripts/contract_guard.py` here.
Prepare and commit requirements on plan, review and integrate the exact commit
on dev, implement and record verification there. Preserve failures and execution
logs. Inspect branch/status before changes and follow standing push authorization.
Self-installing the generated harness would require its own scoped plan.

## Relocation verification (2026-10-29)

- Migration helper: branch tips, working state, origin and hook configuration preserved.
- Container has no .git; all three role worktrees resolve to the same Git common directory.
- Existing ignored Python cache moved intact; legacy sibling worktree paths are absent.
- No matching running harness process was found before relocation.
- `python3 -m unittest discover -s tests -p test_workspace_layout.py -v`: 8 PASS.
- Scope: local layout and routing documentation. No implementation or release changes.
