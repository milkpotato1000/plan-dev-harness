# P008 v0.2.3 publication result

Client date: 2026-11-24 (Asia/Seoul). Common review key: `P008-release-v0.2.3-3ede2e81`.
Actual human main/tag/release authorization and internal exact adoption were verified;
reviewed delivery `65a12e3af61dd5b82b52994d185032f9aeb61a57`,
adoption commit `fb9a2360ca1a5234cde9f66fabd4d0d35fcf4d64`. No duplicate human adoption input requested.

## Published payload

- [Release](https://github.com/milkpotato1000/plan-dev-harness/releases/tag/v0.2.3): draft=false, prerelease=false; actual published_at 2026-11-24T08:14:13Z (17:14:13 Asia/Seoul).
- [main](https://github.com/milkpotato1000/plan-dev-harness/tree/main) and [v0.2.3](https://github.com/milkpotato1000/plan-dev-harness/tree/v0.2.3) both resolve to `3ede2e81f53be8252b585a57064f225fb711ccea`.
- Annotated tag object `8a603187330c2a7c61636badf8401be68881a206`; peeled commit equals candidate. Tag was created once and not moved.
- main fast-forwarded from `803d658a8c61dc6aa007645a98d4160b16746faa`; normal origin/main and tag pushes succeeded.
- main alone received worktree-local `core.hooksPath=.githooks` after runtime was present. Plan/dev hooks preserved; shared hook installer not run.
- [Company Claude Code guide](https://github.com/milkpotato1000/plan-dev-harness/blob/v0.2.3/docs/claude-code-install.md), README, CHANGELOG and Release body consistently describe cumulative 0.2.3 as SKILL.md + Python CLI, not a marketplace plugin.
- Actual remote VERSION/README/guide/release-note bytes equal candidate (remote-verification.json).
- Existing [PR #1](https://github.com/milkpotato1000/plan-dev-harness/pull/1) was open before publication; GitHub now reports closed/merged. Its head is an ancestor of candidate. No PR close/merge/comment API was called; main push incorporated its history.

## Verification

Exact candidate isolated clone: **83 tests PASS**, Python 3.9.6 / Apple Git 2.50.1 / macOS,
141.803s unittest duration. Working tree, index and explicit `check --branch dev --target 3ede2e81f53be8252b585a57064f225fb711ccea` PASS.
Queue selected only P008; no pending decisions or active pause. Both current project chats were verified,
with plan owning plan and this dev owning implementation; no main writer identified. All three worktrees clean before publication.

Local isolated install and fresh public HTTPS tag clone both PASS: preview no writes; apply VERSION0.2.3;
40-file payload hashes match source; installed standalone CLI/help and bootstrap preview;
identical reinstall KEEP; modified/extended existing target refuses preview/apply and preserves every byte.
Public clone used no GitHub credentials. Installation used the documented explicit --skills-dir option
with spaces to avoid writing personal or company targets. Source and downloaded tag CLI behavior match.

Historical P002/P005/P006/P007 files and failures, personal Codex skill and absent personal Claude skill
are byte-preserved (preservation.json). Runtime/assets/tests/VERSION unchanged from starting dev0.2.3.
No product regression failed. Initial restricted-shell credential access returned exit1 before any remote
operation; platform-approved credential/network execution then succeeded. Token was never output or persisted.
Read-only process inventory was unavailable in sandbox; suite completion is proven by its exit/result log.

Actual company Claude Code login, organization policy and model conversation are **untested**.
Linux/WSL procedure and native Windows were not executed. Installation does not create host cross-chat
transport/authority, bootstrap existing projects or resume pauses. Prior P002 historical reconstruction
limitations remain in their original evidence. No other project or personal install changed.

## Evidence and plan follow-up

Full logs/metadata are siblings of this report; manifest.json records their hashes. Publication-time
and final delivery evidence belong to later dev commits; main/tag stay on the immutable candidate.
C5 completion/delivery details are recorded separately in delivery.md and the P008 execution log.

The outer non-Git container AGENTS.md/CLAUDE.md still describe main as historical v0.1.0 without runtime.
Plan should update those entrypoints to state main now holds released v0.2.3 candidate `3ede2e81f53be8252b585a57064f225fb711ccea`,
contains installed runtime and has worktree-local hooks; future main/release changes still require explicit
human approval and shared-hook installation remains prohibited. This is a plan-owned local governance
follow-up under R4, not a product change or new release request. Dev has not edited those entrypoints.
No new human judgment or completion approval is required for this release result.
