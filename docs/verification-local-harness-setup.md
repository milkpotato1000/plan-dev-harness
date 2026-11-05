# Repository-local harness verification — 2026-10-29

User scope: install this repository's plan/dev harness and initialize separate
plan/dev chats in the existing saved container project. No new product work.
Review: [local setup](planning/reviews/local-harness-setup.md).

## Baseline and preservation

- Reviewed setup plan: `65ab556479915b0bfab808a96cf524a219fe07e7`.
- Integrated on dev with merge `238bed0`; exact adoption recorded in `6f60826`.
- Installed runtime source: existing dev commit `8bd9414` (v0.2.0).
  This does not promote/release that package or update personal skills.
- Main remains `803d658a8c61dc6aa007645a98d4160b16746faa` with no runtime files or
  hooksPath. Existing P001 implementation/completion and verification are preserved.
- Parent has no .git. All three worktrees share one Git common directory.
- Both plan/dev installation manifests match every managed file's SHA-256;
  both hooks are executable. Git worktree-specific `.githooks` configuration
  is active only for plan/dev. Outer CLAUDE.md imports AGENTS.md.

## Actual checks

| Check | Result | Evidence |
| --- | --- | --- |
| Python 3.9.6 plan full suite | 51 PASS, 49.426s | [Log](verification/local-harness-setup/plan-python39.log) |
| Python 3.9.6 dev full suite | 66 PASS, 111.453s | [Log](verification/local-harness-setup/dev-python39.log) |
| Plan guard: worktree / index / HEAD | PASS | Actual repository CLI checks |
| Dev guard: worktree / index / HEAD | PASS; exact adopted SHA above | Actual repository CLI checks |
| Actual plan/dev pre-commit hooks | PASS | Direct hook checks and subsequent evidence commit |
| Queue: both roles | Empty task/intake/decision/pause/handoff lists | `work_queue.py --owner all --json` in each worktree |
| Installed manifests, hooks, clean states, branch roles and main boundary | PASS | Read-only Python/hashlib + Git assertions |
| Separate role chats | Both initialized in the same saved container project, read only, then idle | Host completion snapshots |

Full suite command in each child: `python3 -m unittest discover -s tests -v`.
Test environments are temporary repositories; no other user project was modified.
The new queue contains only the P-card template. Historical P001 was not silently
converted, rerun or declared newly complete. The next future number is P002.

## Boundaries

The outer entrypoints and per-worktree Git settings are local; recreate them using
[workspace instructions](workspace.md) on another computer. Local hooks are
bypassable safeguards. A future main promotion requires explicit authorization and
release-hook review. This setup does not validate new product behavior or release
v0.2.0. The chat bootstrap performed no merge/adoption/commit/push or peer messaging.
