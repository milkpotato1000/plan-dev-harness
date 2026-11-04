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
