# plan-dev-harness workspace

Open this directory as the single Codex project. This is a non-Git container.
Run Git and project scripts with an explicit child working directory.

| Directory | Branch | Responsibility |
| --- | --- | --- |
| `plan-dev-harness_plan/` | `plan` | Requirements, P-number plans, review and handoff |
| `plan-dev-harness_dev/` | `dev` | Implementation, tests, evidence and PRs |
| `plan-dev-harness_main/` | `main` | Released baseline; promotion requires an explicit request |

Read the selected child's AGENTS.md before changes. Requests covering both roles
proceed plan → dev: prepare and commit the plan, integrate that exact reviewed
commit on dev, then implement and record verification. A chat explicitly assigned
plan or dev retains that role until the user changes it. Bootstrap reads status
and waits; it does not start new product work or message another chat.

All three children share one repository. Preserve existing changes and execution
logs. Do not merge dev into plan to transfer completion marks. Plan can inspect
committed dev evidence using `git show dev:<path>`. Main is not changed or released
by a folder-layout request. Follow standing plan/dev push authorization.

This repository develops the reusable distribution and also uses a local harness
in plan/dev. Each child has installed runtime under scripts/, configuration under
.harness/, and workflow rules under docs/process/. Distributable sources remain
under assets/ and do not automatically update the installed runtime. See the
child's docs/planning/reviews/local-harness-setup.md for the authorized setup.

Plan owns prepared cards and reviews; dev adopts the exact reviewed plan before
implementation. New scope in dev uses immutable intake then plan review/adoption.
The historical P001 and its dev verification stay in their original paths; the
new parsed queue is empty, and the next new P number is P002. Never infer new
product authorization or completion merely from this setup or an empty queue.

Git hooks are enabled only in plan/dev using worktree-specific config. Main stays
at its released baseline without installed runtime or hook activation. Do not run
the shared-hook installer in this topology; future main promotion requires an
explicit request and review of release hook setup. Preserve explicit user pauses
until the human resumes. Chat bootstrap performs only read-only checks and waits.

Current status can be inspected with:

```sh
git -C plan-dev-harness_plan status --short --branch
(cd plan-dev-harness_plan && python3 scripts/work_queue.py --owner all --brief)
git -C plan-dev-harness_dev status --short --branch
(cd plan-dev-harness_dev && python3 scripts/contract_guard.py check)
```

This local entrypoint and CLAUDE.md are outside Git. Recreate them using the tracked
`docs/workspace.md` instructions on another computer. Main may retain historical
instructions until explicitly promoted; the mapping above describes this machine.

## Fresh sessions and document delivery — harness 0.2.1

Before material changes, read the selected child's AGENTS.md/CLAUDE.md and
`docs/process/agent-workflow.md`, including Fresh sessions and document delivery.
Reconstruct the actual branch, adoption, P cards, committed dev evidence, active
writers and scoped stops/OPEN decisions. Preserve an explicit human role; a
folder, branch, title or .md extension alone does not authorize switching roles.
Unassigned material requests follow reviewed P-card preparation, exact dev
adoption and dev execution. Plan prepares/reviews/hands off. Product README,
user guides and release notes are dev deliverables; planning/governance documents
belong to plan and reach dev through adoption where required. Planning-only drafts
may end on plan and read-only questions need no new card. Bootstrap reads and waits.
Record the requested repository/file/target ref; plan push, exact adoption, dev
push and default-branch visibility are distinct. No target ref implies configured
plan/dev delivery, never automatic main promotion. Existing messaging grants,
writer ownership, unresolved decisions and explicit stops remain in force.

## Asynchronous plan/dev handoff

Plan finishes its turn after reviewed commit, authorized exact-SHA delivery and
actual SENT record/commit/push. Do not wait/poll for ACK, adoption or dev completion.
Observe receipt later on a natural planning/status request; keep unobserved ACK
as SENT. Plan remains available for further authorized planning while dev works.
Busy dev preserves its current P and adopts queued exact reviewed handoffs only
at a safe completed/checkpointed boundary. Preserve priorities/dependencies,
explicit roles, single writers, pauses and OPEN decisions. See the child's
agent-workflow.md section Asynchronous handoff and parallel planning. No automatic
new goals, chats, monitors, reverse messaging or pause resumption is authorized.

## User review and decision gateway

Plan is the normal user-facing review and decision channel. Dev implements/tests
and hands committed results/necessary decisions to plan under a real project grant,
with one common request key, artifact version/hash and question scope. Plan opens
read-only results, checks existing answers and asks necessary human judgment once.
Verifiable answers given in dev are reused for their exact scope. Commit plan
choices and adopt exact reviewed decisions on dev. Preserve asynchronous delivery,
existing work, required human checks, pauses and OPEN decisions. This project's
narrow actual human dev→plan grant is in the child's
 docs/planning/reviews/dev-to-plan-review-delegation.md. No cross-project send,
new chat, permission bypass, automatic resume or ACK loop follows from this rule.
