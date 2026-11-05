# Repository-local harness setup review — 2026-10-29

Authorization: the user requested applying the plan/dev harness to this distribution
repository and creating separate plan/dev chats in the same workspace.

## Reviewed scope

- Reuse the existing non-Git parent and main/plan/dev linked worktrees. Preserve
  all branch tips/history and existing v0.2.0 development; do not promote main.
- Install only repository-local runtime/configuration/process files. Runtime
  source is the existing dev implementation commit
  `8bd941471db02ccb641e26835e7edcfd5a84ad28` (v0.2.0), reviewed against its P001
  contract and committed verification. This does not merge implementation into
  plan or publish v0.2.0. Distribution assets/version remain branch-specific.
- Preview `install_harness.py` from that source before `--apply`, using plan/dev/main,
  `--protect docs/planning/plans --protect docs/planning/reviews --agent none`.
  Preserve existing AGENTS.md/CLAUDE.md and manually merge the local workflow.
- Integrate the reviewed setup plan commit into dev; commit exact adoption before
  activating hooks. Protect managed governance and future parsed cards/reviews;
  preserve the legacy P001 and its existing dev completion/evidence separately.
  No new product task or implicit main/release approval is created.
- Enable Git worktree-specific configuration and set `.githooks` only for plan/dev.
  There were no existing hooksPath/default active hooks or core.worktree settings.
  Main stays at its existing released commit with no new runtime or hook changes.
  Do not use the shared `contract_guard.py install` command for this topology.
- Add the outer CLAUDE.md import. It and outer AGENTS.md are local container
  entrypoints outside Git and must be recreated on another computer.
- Verify plan/dev guard/queue, manifest hashes, executable hooks, common Git dir,
  clean worktrees and regression tests. Create same-project local role chats and
  verify both perform read-only bootstrap then wait.

## Existing work and delivery boundary

P001 is the existing v0.2.0 work order, not a newly approved setup task. Its dev
implementation/verification already exist; preserve them byte-for-byte. The new
parsed queue has only its template. Next future P number is P002.
Normal plan/dev branch pushes use standing authorization to the existing origin.
Main, tags, new remotes, external tools, personal skills and unrelated repositories
are outside this setup. A local harness test pass is not a product/release approval.
