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

## Authorized delivery

Follow [direct handoff](direct-handoff.md) for human authority, verified recipients,
committed SHA/document, actual send/receipt evidence, deduplication and fallback.
The installed project procedure is complete in docs/process/workflow-controls.md;
queue/CLI reads never message a chat. A supported, authorized agent delivery is
performed directly; it does not require a new permission or user copy step.

## Source, project runtime and personal skill transitions

The distribution source has VERSION, SKILL.md, references/, scripts/ and assets/.
install_harness.py copies assets into a project's scripts/ and docs/process/ with
.harness/installation.json hashes; changing source assets does not update a project.
Project --upgrade requires its original flags and unmodified managed hashes.
Preview is read-only; review options, manifest, extra hooks, instructions and live
records before applying under that project's authority. Commit reviewed changes
on plan, integrate/adopt the exact SHA on dev and verify again. Legacy installs
without a manifest need reviewed integration, not a fabricated manifest.

install_skill.py separately copies a self-contained skill package. It has no
--upgrade flag. Its Codex default is ~/.agents/skills; a loaded ~/.codex/skills
installation is a different path. Claude defaults to ~/.claude/skills. Inspect the
actual loaded skill path, VERSION and payload before choosing a transition; same
name does not mean same version or active copy. Never change personal installations
as a side effect of a project task.

For an authorized skill transition, preserve/back up the old payload and user
extensions, preview a fresh destination with --skills-dir, then apply using the
same flags. Test its standalone scripts, references and assets before selecting
it in the host. Do not leave two copies simultaneously active under the same name.
Choose the supported discovery path deliberately, reopen/refresh discovery if
needed and reread the selected SKILL.md. File copying alone proves no activation.
Conflict refusal preserves the old destination; it is not permission to force it.

## Legacy setup capabilities retained in this workflow

Before setup, inspect instructions, status, branches, worktrees, remotes, upstreams,
hooks and active writers. Infer the local parent/name and existing repository from
that evidence; ask together only for missing destination/branch decisions. Reuse
suitable checkouts. For a new hosted repository verify the authenticated identity,
exact owner/name, nonexistence and agreed visibility; do not assume an organization
or reuse another project's accounts. A visibility choice and publication require
human authority. Never request tokens in chat.

New local bootstrap creates infrastructure only. GitHub discovery/creation and
remote configuration are separate host connector/CLI actions, not features of
install_harness.py. Add only agreed exact remotes and publish only authorized
branches with normal pushes; verify destination SHAs. Main publication/promotion
needs explicit authorization. Existing histories must not be reset or force-joined.
For existing repositories add only missing linked worktrees, coordinate active
writers and preserve dirty/ignored files. See [workspace migration](workspace-layout.md).

Keep existing project instructions and optional service adapters. Use --agent none
and reviewed instruction integration when necessary; do not remove extensions to
make a package fit. P-card ownership, immutable intake, exact adoption, pauses and
evidence remain in the installed workflow. Report local-only versus pushed state,
actual checks, loaded paths and unverified limits across computers.
