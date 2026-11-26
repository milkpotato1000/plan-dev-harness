# 0.2.5 (unreleased)

- Add explicit project-local role mapping, bounded private lifecycle registry, atomic updates, conflict/old-end protection and conservative host-verified reconnect.
- Add preserving hook configuration preview/apply/KEEP and read-only discovery/exact handoff adapter; Codex queue acceptance remains separate from delivery.
- Preserve current P, user stops, existing work/global installs and released v0.2.3. Actual two-session host verification is a separate gate; unsupported transport stays pending.

# Changelog

## 0.2.4 — Unreleased

- Independent plan/dev sessions are the default; sequential mode needs an explicit human choice.
- Plan execution approval is distinct from internal exact-SHA application by dev; no repeated adoption input.
- Native Claude ListAgents/SendMessage procedure and read-only worker doctor distinguish missing, ambiguous, busy, held and unknown states.
- Codex delivery, existing controls/adopt/event formats and plan review gateway remain compatible.
- Live Claude evidence and limitations are recorded in docs/verification/P009; no new public release is implied.


## 0.2.3 — 2026-11-24

Cumulative formal release since v0.1.0. The 0.2.0, 0.2.1 and 0.2.2 development
milestones below were not separate formal GitHub Releases. Date uses Asia/Seoul;
GitHub records its own actual publication timestamp.

### Result review (0.2.3)

- Route result review and necessary human questions through plan using a shared scoped request key.
- Preserve pending questions and verifiable human answers across roles, artifact versions and resumed sessions.
- Add the review packet/ledger template to standalone installs, upgrades and bootstrap output.
- Keep optional review, required human criteria and critical OPEN decisions distinct.

### Asynchronous handoff (0.2.2)

- Finish plan handoffs after actual SENT is committed/pushed; observe ACK on a later natural request.
- Preserve busy dev work and adopt reviewed exact handoffs at safe commit boundaries.
- Carry asynchronous rules through both host packages, prompts, bootstrap and upgrade output.
- Retain runtime/schema, pauses, decisions, permissions and single-writer boundaries.

### Fresh sessions and document delivery (0.2.1)

- Reconstruct assigned roles, adoption, progress and scoped stops from project files.
- Route material work through prepared P cards and exact dev adoption; keep product documentation on dev.
- Distinguish plan push, dev adoption/push and visibility on the default branch.
- Preserve existing project extensions and separate source, installed runtime and personal skill versions.

### Decisions and explicit stops (0.2.0)

- Add plan-owned decision impact classification and dependency-aware queue blocking.
- Preserve legacy OPEN/RESOLVED and PAUSED/ACTIVE records; unresolved scope fails closed.
- Add explicit pause/resume records, role-scoped stops, and plan/dev history guards.
- Add committed handoff events with deduplication and evidence-backed delivery states.
- Keep generic intake independent of workflow stops; expose additive queue JSON fields.
- Fix default queue owner selection to retain the actual configured worktree role.
- Upgrade an unmodified v0.1.0 installation while retaining custom post hooks and records.
- Document optional adapter boundaries without external service side effects.

### Distribution and verification

- Publish a fixed v0.2.3 tag, main payload and formal release with a company Claude Code installation guide.
- Document personal/project SKILL + CLI installation, preview/apply/KEEP and conflict preservation.
- Preserve P002 actual two-session evidence and its explicit historical-fixture reconstruction limits.
- No marketplace plugin, automatic message transport, company account access or existing-install auto-update is added.

## 0.1.0 — 2026-10-29

- Publish generic Git/Python harness with configurable plan/dev/release branches.
- Add Codex/Claude shared instructions and safe standalone skill installers.
- Bootstrap an absent nested workspace with initial adoption and local hooks.
- Include dev requirement capture, immutable request hashes and plan-owned triage.
- Preview installs/upgrades; refuse modified files, symlinks and competing hook systems.
- Preserve P-card failures and require evidence for completion.
- Accept ISO Z timestamps on Python3.9 without relying on newer datetime parsing.
- Retain optional legacy worktree migration and real Git integration tests.
