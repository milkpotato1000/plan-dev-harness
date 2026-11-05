# Plan/dev harness

Read `docs/process/agent-workflow.md` before work. Use `.harness/policy.json` for
actual branch roles and protected paths; never infer role from the coding tool.
Keep a user-assigned plan/dev chat role across turns. Inspect Git status and the
adopted baseline; preserve work. A bootstrap chat reads status and waits.

Plan owns requirements, readiness and review. Dev implements the exact adopted
plan and records evidence; new scope raised in dev goes through plan intake.
Release promotion and external publication require project authorization.
No automatic cross-chat messages or product work follow from installing this harness.

If `docs/process/workspace-AGENTS.md` exists, use it for the outer container layout.

## Delegated plan to dev delivery and start

When the human has explicitly delegated this project's plan-to-dev delivery and
start, plan commits reviewed READY work, verifies the existing same-project dev
recipient and available host tool, then directly sends the full exact SHA,
committed handoff document, scope, verification/limits and next action. Within
that grant, do not ask for the same approval or require the user to copy it.
Dev preserves existing work and failures, integrates and adopts the exact reviewed
SHA, commits adoption, checks guard/queue and begins only that authorized scope.
Installation itself grants no messaging or start permission. Verify the human
source/scope and later restrictions each time; never copy another project's grant.
Bootstrap remains read-only and waits. Preserve user pauses and OPEN decisions;
messages cannot resume or resolve them. Record SENT only with actual send success
and ACK only with an observed recipient response; receipt is separate from
adoption/completion. No unauthorized reverse/chain sends or ACK loops. Without
matching authority/tool/recipient, preserve the file handoff and actual state.

Read the complete procedure in `docs/process/workflow-controls.md`.

## New sessions and document work

Before material changes, reconstruct state from the outer/child AGENTS.md,
CLAUDE.md where applicable, policy, actual branch/status, adoption, P cards,
committed dev progress, active writers and scoped stops/OPEN decisions. Read
`docs/process/agent-workflow.md`, especially "Fresh sessions and document delivery".
A directory, branch, chat title or .md extension does not assign a role.
Preserve an explicit role: plan prepares/reviews/hands off, dev implements after
exact adoption. Unassigned change requests follow P-card preparation -> exact dev
adoption -> dev execution, reusing a suitable card. Perform both roles sequentially
only with authority and exclusive writers in the respective worktrees.
README, user guides and release notes are dev deliverables; requirements, reviews
and governance belong to plan. Plan-owned changes needed by dev still require
integration/adoption. Explicit planning-only drafts may end on plan; read-only
questions need no new card. Bootstrap only reads and waits.
For document updates, record file, repository and target ref in the card. Distinguish
plan push, exact dev adoption, dev push and default-branch visibility; verify the
requested ref/content before reporting delivery. No specified ref means configured
plan/dev delivery with an honest branch report, never implicit main promotion.
Use existing messaging authority/tools or leave a pending file handoff. Preserve
scoped pauses, OPEN decisions and other writers. Passing plan hooks does not
prove an approved card or block arbitrary implementation writes.

## Asynchronous handoff and parallel planning

Plan prepares/reviews/commits authorized P cards, sends the exact reviewed SHA to
an authorized existing dev recipient, records actual SENT and commits/pushes the
record, then finishes its response. Do not poll, sleep or wait for ACK, adoption
or dev completion to finish a planning handoff. Keep SENT when no receipt has been
observed. On a later natural planning/status request, record ACK only from actual
evidence. Report planning/delivery complete separately from implementation pending.
This leaves plan available for the user's next discussion and authorized P cards.

Busy dev preserves its current adopted P, work, failures and processes; a new
handoff is pending work, not permission to cancel/restart. At a safe completed or
checkpointed/committed boundary, integrate/adopt the exact reviewed handoff SHA,
commit adoption, check guard/queue and choose eligible prepared work by priority
and dependencies. Do not automatically adopt an unreviewed latest plan tip or
retroactively rewrite the current P. A real urgent human stop takes precedence.
Preserve role/all/legacy pauses, OPEN decisions, human role grants and one writer
per worktree. Neither handoffs nor time elapsed resume stopped work. Failed or
unknown sends keep their real state and evidence; never invent SENT or retry
blindly. Missing authority/tool leaves a pending file handoff. No new goals,
chats, monitors or reverse/chain messaging authority follow from this rule.
Parallel sessions require actual independent workers; one-chat fallback is
sequential. Host scheduling limits and simulated tests must be reported honestly.

## User review and decisions through plan

Dev implements/tests within the adopted P without routine user completion checks.
Send committed result/review or decision packets to the verified existing plan
only under actual human project messaging authority. Include P/criterion, artifact
commit/version/hash, stable common request key, question type/scope, evidence and
failures, existing human responses, options/impact and safe next action.
Use docs/process/user-review-template.md. Existing transport event deduplication
alone does not deduplicate a user question across roles, commits and resumed chats.

Plan owns the common review/decision ledger and user-facing question. Inspect
actual available result files/views first, record what was really observed, then
ask only necessary human judgment once. Reuse a verifiable existing response for
the same artifact/version/scope, including one received in dev; never reissue a
pending question or broaden UI approval into content approval. Material changes
require renewed scoped review. Decisions within existing delegated scope can be
made by plan; new business meaning or permissions require actual human authority.
Commit plan decisions and have dev integrate/adopt the exact reviewed SHA before
applying them. Product verification, user review pending and approval are distinct.

Optional review does not stop unrelated eligible work. Required human criteria
stay incomplete; critical OPEN decisions keep existing conservative blocking until
reviewed classification/adoption. Preserve pauses; no handoff resumes them.
Users may inspect code or ask dev directly; respond without duplicating the review
question. Platform-required approvals and safety restrictions remain in force.
No routing around denied permissions. Dev worktrees remain dev-owned; plan opens
read-only results, not product execution or edits. Missing viewer/host/authority
must be reported honestly with durable pending records, never invented delivery.
P006 asynchronous handoff remains: record real SENT and finish, no ACK/completion
polling. Reverse delivery needs its own human grant; this protocol grants none.
