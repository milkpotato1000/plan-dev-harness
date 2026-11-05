# Changelog

## 0.2.3 — Unreleased

- Route result review and necessary human questions through plan using a shared scoped request key.
- Preserve pending questions and verifiable human answers across roles, artifact versions and resumed sessions.
- Add the review packet/ledger template to standalone installs, upgrades and bootstrap output.
- Keep optional review, required human criteria and critical OPEN decisions distinct; preserve asynchronous delivery.

## 0.2.2 — Unreleased

- Finish plan handoffs after actual SENT is committed/pushed; observe ACK on a later natural request.
- Preserve busy dev work and adopt reviewed exact handoffs at safe commit boundaries.
- Carry asynchronous planning rules through both host packages, prompts, bootstrap and upgrade output.
- Retain existing runtime/schema, pauses, decisions, permissions and single-writer boundaries.

## 0.2.0 — Unreleased

- Add plan-owned decision impact classification and dependency-aware queue blocking.
- Preserve legacy OPEN/RESOLVED and PAUSED/ACTIVE records; unresolved scope fails closed.
- Add explicit pause/resume records, role-scoped stops, and plan/dev history guards.
- Add committed handoff events with deduplication and evidence-backed delivery states.
- Keep generic intake independent of workflow stops; expose additive queue JSON fields.
- Fix default queue owner selection to retain the actual configured worktree role.
- Upgrade an unmodified v0.1.0 installation while retaining custom post hooks and records.
- Document optional adapter boundaries without adding external service side effects.

## 0.1.0 — 2026-10-29

- Publish generic Git/Python harness with configurable plan/dev/release branches.
- Add Codex/Claude shared instructions and safe standalone skill installers.
- Bootstrap an absent nested workspace with initial adoption and local hooks.
- Include dev requirement capture, immutable request hashes and plan-owned triage.
- Preview installs/upgrades; refuse modified files, symlinks and competing hook systems.
- Preserve P-card failures and require evidence for completion.
- Accept ISO Z timestamps on Python3.9 without relying on newer datetime parsing.
- Retain optional legacy worktree migration and real Git integration tests.
