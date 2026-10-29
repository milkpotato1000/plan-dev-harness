# Install, handoff and intake commands

Commands below run inside the selected project worktree, except installer commands
which resolve assets relative to the installed skill/distribution directory.

## Install files vs activate hooks

`install_harness.py` previews by default. It refuses competing hooks, symlinks and
nonmatching files before writes. `--apply` only changes the listed local files.
Run on the planning branch of an existing repo, or an unborn bootstrap branch.
Protected paths and branch names come from your flags; no product tasks are created.
Add `__pycache__/` and `*.pyc` to the existing .gitignore if absent, so Python
runtime files do not enter handoff commits. The installer preserves your .gitignore.

Commit reviewed harness files on plan. Ensure every participating worktree has
these files before shared hooks are activated. On dev:

```sh
# Exact SHA printed by the reviewed plan commit, not a moving branch name.
git merge --no-commit <reviewed-plan-sha>
python3 scripts/contract_guard.py adopt <reviewed-plan-sha> \
  --review-reference docs/planning/reviews/harness-install.md
git add .harness/adopted-plan.json
# Finish the merge/adoption commit with the integrated changes.
git commit -m 'Adopt reviewed plan baseline'
python3 scripts/contract_guard.py install
python3 scripts/contract_guard.py check --target worktree
python3 scripts/contract_guard.py check --target index
python3 scripts/contract_guard.py check --target HEAD
```

Use a real review file/reference. A fast-forward merge can finish before adoption;
still commit the new adoption record before product work. Conflicts require retaining
plan requirements and dev append-only logs. Never bypass hooks to finish a merge.
A new project can instead use `bootstrap_workspace.py`, which performs infrastructure
setup/adoption without installing hooks until all children contain the scripts.

## P cards

Copy `docs/planning/plans/_TEMPLATE.md` to the next unused `Pnnn.md`. The template's
Korean field names are the parser's contract; do not translate them in-place.
Plan writes requirements, priorities, dependencies, readiness and review reference.
Dev updates only execution status, checkmarks and append-only execution logs.
Latest PASS evidence must exist and be nonempty in the snapshot being checked.

```sh
python3 scripts/work_queue.py --owner all --json
python3 scripts/work_queue.py --owner plan --open
```

`--open` exits1 for unfinished relevant tasks/pending requests; malformed records
exit2. Queue output is read-only; registering a request is not an execution grant.

## New scope from dev

Write a non-sensitive UTF-8 request file, then in dev:

```sh
python3 scripts/plan_intake.py request --title 'New capability' \
  --request-file /tmp/project-request.txt --source 'User request and date' \
  --impact 'Affected requirement and scope change'
```

Review and commit the generated `docs/feedback/dev/requests/R*.json`; share through
the configured remote only if authorized. Plan reads committed dev records:

```sh
python3 scripts/plan_intake.py list
python3 scripts/plan_intake.py review <actual-request-id> \
  --disposition linked --cards P001 --reason 'Scope and decision' \
  --review-reference docs/planning/reviews/request-review.md
```

Use actual IDs/cards/review evidence. `linked`, `covered`, `deferred`, `rejected`
are triage decisions, not automatic READY or implementation. Request corrections
are new immutable records. Plan decisions are protected and apply after adoption.
New requirements are classified by the agent; Git cannot infer them from conversation.

## Existing project-specific rules

When an AGENTS.md or CLAUDE.md conflicts with generated files, install core using
`--agent none`, merge `assets/instructions/agent-workflow.md` into the project's
workflow, and add a Claude import without removing existing instructions. Review
policy path changes explicitly. For a legacy installation without a manifest, the
installer refuses to overwrite it; integrate the diff on plan rather than fabricating
an installation manifest to bypass conflict detection.

## v0.2 workflow controls

See [workflow-controls](../assets/docs/process/workflow-controls.md) for the complete
CLI. Decision requests and generic intake serve different purposes: only a critical
OPEN decision or a user pause blocks queue selection. Impact classifications belong
to plan and must be adopted. Old records without scope remain conservative all-role
pauses/all-dev decisions. A RESOLVED decision needs a full adopted plan SHA.

Existing v0.1.0 manifests support the same-option --upgrade path. New scripts and
process documents are managed; live requests/checkpoints/handoffs and extra adapter
hooks are not installer payloads. Review ownership additions before adopting on dev.
Installation does not repair malformed historical records or install optional adapters.
