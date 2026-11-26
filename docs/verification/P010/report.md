# P010 source 0.2.5 — registration and reconnect result

Common key: P010-session-registration-reconnect. Actual human request was verified in the
existing parent plan chat on 2026-11-26. Exact reviewed plan
32e00589afa491a47a5e89fadc1aa4f113003a28 was internally adopted at a4a87de; no repeat human
adoption prompt. Source implementation is e044e3e7f11ef48d4f9cc4fa41cad7ac00d8e1c8
(initial ecd32edd26e08e4799eca85140b70f41591aed8e plus validation hardening).

Implementation and isolated installation verification are complete. **Actual two-session
host startup/reconnect/delivery C3 is NOTRUN and remains unchecked.** No new user-owned
Codex chats or competing workers were created; existing P009 sessions were not used or
changed. Prepared role worktrees have no registry yet. This is not a claim of live success.

## Delivered behavior

- `configure_sessions.py`: explicit plan/dev worktree/branch mapping in one Git common-dir,
  private role config and project-local official lifecycle hooks, preview/apply/KEEP, user
  hook/settings preservation, owned-hook conflict refusal and bounded rollback.
- `session_registry.py`: bounded private registry, nonblocking kernel lock, atomic fsync
  writes, generation checks, same-live-ID resume, matching end plus fresh positive host proof
  for replacement, late-old-ID rejection, conflict retention, read-only doctor. Unsupported
  Codex machine inventory and shared-parent ambiguous roles remain pending. Explicit verified
  host-observation reconnect entry selects identity from actual inventory, not human ID copying.
- `session_handoff.py`: resolves a committed PENDING exact reviewed handoff and READY P card,
  checks current guards/queue/identity, emits private native tool arguments. Explicit Codex
  queue action detects local help, records attempts before sending, rejects unknown retries
  and rechecks stops/writer/generation. Queue acceptance is never receipt or execution.
- Runtime copies, generated instructions, installer manifest/payload, SKILL and product
  documentation consistently expose unreleased 0.2.5. Global skills/parent installed runtime
  are separate and were not upgraded. Public installation stays pinned to v0.2.3.

Registration never grants execution, sends peers, clears a pause or rewrites current P.
Local observations are not authentication. Actual human grant/native capability/inbound
checks remain required immediately before delivery; supplied host evidence is explicitly
identified as an observation. Unavailable inventory, stale/crashed/unknown writers and
conflicts fail closed; TTL is never takeover authority. No raw socket/terminal injection,
background daemon, permission/trust bypass, competing resume or worker creation exists.

## Verification matrix

| Contract | Result and evidence |
| --- | --- |
| W1/M1 | PASS in isolated real Git worktrees: explicit roles/common-dir/branches, both startup orders and later peer discovery via simulated hook input. Actual host starts are separately NOTRUN. |
| W2/M2 | PASS at runtime layer: idempotent live-ID start, ended-ID resume with positive proof, fresh identity/end/generation handling, TTL never takeover, contenders and real concurrent Python hook processes preserve one writer. Fresh proof is simulated inventory in unit tests, not live host proof. |
| W3/M3 | PASS: separate clone, wrong role/branch/cwd/host, duplicate writers, malformed/corrupt/symlink JSON, future/backwards time, lock failure, atomic-write failure, missing timestamps/host paths and shell-literal paths fail safely. Bounded oversized/malformed stdin checks create no registry. |
| W3+W5/M4 | PASS: actual fixture stop and OPEN remain unchanged after lifecycle updates; source tests retain scoped stop/decision/busy rules and exact handoff guards. Dispatch refuses a newly observed stop or conflict. |
| W3/M5 | PARTIAL: installed official help and published hook/transport interfaces checked, existing desktop exact-SHA result handoff used for this task. Actual Claude/Codex two-session raw startup→registration→handoff→reconnect→next handoff NOTRUN. CLI queue receipt/wakeup is not inferred. |
| W4/M6 | PASS: exact historical 0.2.4 source installed then upgraded to final 0.2.5; preview no writes, fresh apply, repeated KEEP, exact dev integration; custom hooks/settings/permission rules/uncommitted work/explicit stop preserved; customized managed hooks refuse all writes; simulated partial configuration failure rolls back only owned changes. |
| W6/M7 | PASS for automated scope: final full regression, guards/queue, independent installed CLI help, both SKILL payloads and privacy/version/hash checks. Live host limits remain separate. |

`full-tests-final.log` records 105 tests on final source. `installation-checks.json` contains
34 actual isolated commands/checks. `focused-tests.log` records 16 new meaningful tests.
`bounded-input-checks.json` labels synthetic stdin explicitly. Configured fixtures include
paths with spaces, Unicode and shell metacharacters; the actual generated command is run
from a different cwd without interpreting those path bytes as shell instructions.

Initial focused failures are retained in `focused-initial-failure.log`: macOS `/var` alias
rejection and a test's noncanonical path expectation. The implementation now accepts only
known macOS system aliases and retains refusal of arbitrary symlinks; the assertion compares
canonical paths. A first 105-test run passed on the initial candidate; final review then
added strict missing-path/time rejection and repeated the complete suite on final source.
No failing evidence was deleted or reclassified as a live pass.

## Actual host boundaries

Read-only local observations: Claude 2.1.332 and Codex CLI 0.160.1. Full bounded help is in
`host-capabilities.json`. Codex `queue` supports `--thread`/`--message`, lacks `--resume`;
`agents` has no documented JSON flag. No unsupported option was invoked. A sandbox PATH
alias warning is retained; it is not evidence that all host sessions are absent.

Official sources checked 2026-11-26:
[Claude lifecycle hooks](https://code.claude.com/docs/en/hooks),
[Codex lifecycle hooks and trust](https://learn.chatgpt.com/docs/hooks),
[Codex developer commands](https://learn.chatgpt.com/docs/developer-commands).
The implementation uses project-local JSON hooks and actual stdin session_id/cwd fields.
Non-managed Codex hooks require human review/trust. Trust is not installed by our scripts.
These documents and CLI help establish capability/schema references, not actual two-session
execution evidence. macOS/Linux Python 3.9+ support is the implemented scope; Windows and
unverified company policies are not claimed.

## Prepared minimum live prerequisite

Two separate isolated containers, one for Claude and one for Codex, contain explicit plan/dev
worktrees, final runtime, hook configuration and an empty initial queue. They were previewed,
applied, updated to final source, rechecked as KEEP and verified clean with guards/queues.
`live-preparation.json` includes exact fixture commits plus original/exported hook hashes;
`P010-LIVE.md` is the bounded fixture runbook. Raw private local locations are transmitted only
to the existing parent plan, with runnable `cd … && claude` / `cd … && codex` commands and
role input. No session has been started and no trust prompt has been answered by the observer.

Parent plan can ask once under this common key for the real isolated role terminals to be
opened and any actual project/hook trust review to be completed by the human. Claude and
Codex can be staged separately; no precise human timing is required. After actual host
startup, observe registration and carry out the bounded native handoff/reconnect test.
For Codex CLI-only inventory limitations, keep unsupported live scope pending or use real
existing official app tools to export fresh observations; do not ask for ID copying, create
a bridge, resume another worker or claim queued text was executed. No P009 retest is proposed.

## Preservation and delivery

512 pre-existing documentation hashes were retained, excluding the authorized product guide
edit and P010 files. Installed parent policy/guards/queue/control/runtime/hook bytes are
unchanged from prior dev. P009 remains C3 incomplete, 4/5, with original failures intact.
Main/tag still resolve to 3ede2e81f53be8252b585a57064f225fb711ccea. No main/release/personal
installation or other project was written. This report and manifest are delivered on the
configured dev branch; they are not a published 0.2.5 release.
C1/C2/C4 may be checked against automated evidence; C3 stays unchecked. C5 delivery is
recorded only after actual authorized parent-plan send and normal dev push, in a separate
post-send record. Parent plan owns any necessary human question; no ACK/completion loop.
