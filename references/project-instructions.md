# Project instruction section to adapt

Merge this into existing AGENTS.md; substitute the configured branch roles and
avoid duplicating existing rules. Setup approval is not product implementation approval.

## Planning/development workflow

Open `<parent>/<project>/` as one agent workspace (Codex or Claude Code). It is a non-Git container with
`<project>_plan/`, `<project>_dev/` and `<project>_main/` children sharing one Git
repository. From any child the siblings are `../<project>_plan/`,
`../<project>_dev/` and `../<project>_main/`. Route planning to the plan child and
implementation/verification to the dev child, read its AGENTS.md, and use that
working directory explicitly. For both roles proceed plan → dev with review and
exact adoption. The container's AGENTS.md is a local routing entrypoint outside
Git; recreate it with this layout on another machine.

When the user initializes separate plan/dev chats, keep each chat's assigned
role across turns. A generic next-work request follows that role and its child
working directory. Explicit user requests can change scope. Chat creation only
initializes context and reads current status; it does not start product work or
authorize sending prompts to another chat.

One Git repository uses linked planning and development worktrees. Release changes
only through explicitly requested promotion. Inspect status, current branch,
adopted baseline, relevant contracts and dev feedback before material changes.
Preserve existing work.

Plan owns requirements and contracts in protected paths. New tasks use one P-number
from planning through completion at `docs/planning/plans/P*.md`. Read
`docs/process/work-queue.md`; use `python3 scripts/work_queue.py` to select next work.
Plan is delegated readiness review and dev registration within the user's project
objective. Once scope, dependencies, verification and completion criteria are
ready, mark the card prepared, commit and register it without another handoff
approval prompt. Record this workflow and the readiness review as the approval
reference. Unresolved business decisions and actions outside existing authorization
still require resolution; do not infer them from a commit.

Dev implements the exact adopted plan. Only P-card execution status, checkbox marks
and append-only execution logs are dev-editable. Never change requirements or remove
criteria to finish. Implement, verify, fix and reverify until each condition has
PASS evidence; preserve failure history. Evidence belongs in docs/verification/
or docs/progress/. Record meaning mismatches in docs/feedback/dev/ for plan review.
Plan may prepare the next independent card while dev works.

Normal handoff is plan → dev, then exact adoption through scripts/contract_guard.py.
Never merge arbitrary dev history into plan just to update checkmarks. The queue
reads committed dev progress. If dev's adopted queue is empty, check the latest
available plan for prepared work and integrate/adopt that baseline before starting;
old adoption must not be mistaken for absence of work. Main/release promotion is explicit. Honor existing
push authorization per project; do not invent permission for other destinations.
Local hooks and validation are required; CI, hosted branch protection and PR-only
workflows are not required by this harness. Install hooks in each clone.

## New dev requirements

Use the installed `docs/process/plan-intake.md`: immutable dev request, committed
plan decision, prepared card, exact adoption. Use `CLAUDE.md` with `@AGENTS.md` to
load the same ownership instructions in Claude Code. These are Git-owned rules;
no particular chat API or coding agent is required.

## Decisions, explicit stops and durable handoffs

Use installed docs/process/workflow-controls.md. Unclassified decisions stop dev;
plan-owned classifications can limit the stop to affected cards and their dependents.
User pauses are independent, persist across sessions, and need explicit resume records.
Do not delete or rewrite stops or delivery history to unblock a queue. Send messages
only under user authorization and record actual delivery/receipt evidence. Existing
project-local skills may share this skill's name; merge their operating rules deliberately
instead of replacing them with this setup skill. Preserve optional project adapters.

## Fresh sessions and document delivery

Use the shared [startup and delivery rules](../assets/instructions/agent-workflow.md#fresh-sessions-and-document-delivery).
Read actual files/branch/adoption/queue/stops and check writers before material writes.
Preserve an assigned role; unassigned changes use an existing suitable P card or a
reviewed new one, then exact dev adoption and implementation. Plan does not implement
product README/user guides; planning-only drafts may finish on plan, and read-only
questions need no card. Record file/repository/target ref and verify actual delivery;
plan push, dev adoption and default-branch visibility are separate outcomes.
Only authorized, uncontested sessions perform both roles in separate worktrees.
Bootstrap, absent messaging authority and scoped pauses retain their boundaries.

## Asynchronous handoff and parallel planning

Use the shared [asynchronous workflow](../assets/instructions/agent-workflow.md#asynchronous-handoff-and-parallel-planning).
After authorized send success, record/commit/push SENT and end the plan response;
do not wait or poll for ACK, adoption or dev completion. On a later natural
planning/status request record ACK only from observed evidence. Busy dev preserves
its current P and failures, then adopts the exact reviewed handoff at a safe
completed/checkpointed commit boundary and follows readiness, priorities and
dependencies. Keep pauses, OPEN decisions, roles and single writers. Separate
sessions can overlap P stages; a one-chat fallback is sequential. No daemon,
new goal, chat, monitor or messaging authority follows from this procedure.

## User review gateway

Use the [result review protocol](user-review.md): dev commits evidence, artifact
version/hash, shared request key, question scope and existing human-answer sources.
Plan owns read-only result review and necessary human questions, reuses valid
pending/answered scopes across roles and records decisions for exact dev adoption.
Dev does not ask routine completion confirmations. Optional review, required human
criteria and critical OPEN remain distinct. User code questions in dev are allowed.
Reverse delivery needs a real human project grant; no permission or pause bypass.
Preserve asynchronous SENT-then-return and busy-role safe boundaries.
