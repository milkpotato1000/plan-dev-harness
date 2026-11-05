# Result review and decisions through plan

Use this protocol when dev has a result to review or needs a scoped decision.
Dev implements/tests within the exact adopted P and reports evidence; it does not
ask routine “confirm completion / continue?” questions. Plan is the review/question
owner. Direct user code questions in dev are still answered there and linked to
the common record. Actual platform approvals and safety blocks retain their normal
process; never route around a denial through another chat.

## Packet and common identity

Commit the dev original at `docs/feedback/dev/reviews/<key>.md` using the
[review template](../assets/docs/process/user-review-template.md). Plan records
its ledger at `docs/planning/reviews/user-reviews/<key>.md`; dev does not edit that
ledger. These are document conventions and role obligations, not a new runtime
schema, parser, sender or universal write guard.

Before creating a request, search existing packets, pending questions and human
answers. Use a common project-local key based on P/criterion, confirmation type
and scope, artifact identity and material version. Reuse the key across transport
events, new delivery commits and resumed sessions for the same review. Link any
older aliases. Transport event SHA deduplication alone does not deduplicate user
questions semantically.

Record exact source commit, repository-relative artifact path or authorized URL,
raw hash, material version/hash, question type/scope, actual verification/failures,
unconfirmed conditions, existing human answer references, recommendation/options,
impact, next safe action and blocking scope. A packet's own new commit is not a
material artifact change. Do not include tokens, raw conversations or other
projects' private data in public records. Preserve original requests, answers and
failures; append/link later observations rather than replacing history.

Material changes require a new scoped review linked to the earlier one. If only
a timestamp or delivery wrapper changed, reuse requires recorded evidence that
the material artifact and confirmation scope are equivalent. Record both exact
hashes and that reason; do not silently ignore fields or carry approval to a
larger scope. UI appearance/interaction approval does not approve answer content,
business meaning, permissions or policy.

## Plan review before a human question

1. Read the common ledger and verify existing answers against exact artifact,
   material version and scope. A pending question is linked, not reissued.
   Reuse an actual identifiable human answer received in either role. An agent's
   unsupported “the user approved” sentence is not a human approval source.
2. Open the committed result or a safe independent read-only copy with available
   file/viewer/browser tools. Record the version/hash, tool, what was actually
   observed and limits. Reading source, offering a link and visually inspecting
   a rendered result are distinct. Never invent an observation when a viewer is
   unavailable or permission is denied. Dev prepares an authorized preview/server
   when needed; plan does not edit, generate or execute product code in dev.
3. Resolve checks within existing contracts/delegation and record the reasoning.
   Ask only necessary human preference, business meaning or an explicitly human
   acceptance criterion, once in plan. A tool observation cannot substitute for
   a required human answer. No new permission or business decision is invented.
4. Commit the scoped decision/actual answer and needed P/readiness changes. Dev
   integrates/adopts that exact reviewed SHA before implementation, resolving a
   critical decision or checking a human criterion. A plan answer alone does not
   alter an unadopted dev contract. New scope still follows immutable intake.

## Review versus blocking

Optional result review leaves independent eligible work available. Keep automatic
verification PASS, review pending, actual human approval and implementation done
as distinct facts. A required human criterion stays unchecked; use the existing
P BLOCKED/log fields while unrelated eligible work can proceed under current rules.
Do not create global critical OPEN merely for a routine UI review.

For a critical meaning/permission/correctness issue, retain PLAN_DECISION/OPEN and
the existing conservative legacy/unclassified block. Plan classification and exact
dev adoption are required before limiting its scope. Review, message arrival,
new version or elapsed time cannot resume pauses or resolve decisions.

## Authorized asynchronous delivery

Use existing WORK_READY targeting plan for result review, or DECISION_REQUEST for
a critical decision. Verify actual human project authority, existing recipient,
host and later stops. The package itself grants no reverse messaging permission.
With authority and tools, send the committed packet/full SHA/key directly, record
actual SENT, commit/push and return without waiting for ACK/decision/completion.
Busy plan receives queued work at its safe boundary; preserve its current task,
single writer and pending questions. Never resend an ACK or turn review into a
status ping/monitor. A separate reviewed plan-to-dev handoff carries any decision.

Without a host/grant, or after failure/unknown delivery, preserve the durable
pending packet, real outcome and safe next step. Do not claim delivery/wakeup or
ask the same human question in dev as a fallback. Inspect before any later retry;
no blind resend. See [direct handoff](direct-handoff.md) and
[asynchronous workflow](../assets/instructions/agent-workflow.md#asynchronous-handoff-and-parallel-planning).
