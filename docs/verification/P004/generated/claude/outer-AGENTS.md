# claude-project workspace

Open this directory as the single agent workspace (Codex or Claude Code). It is a workspace container;
Git commands and project scripts run inside the selected worktree.

| Directory | Branch | Responsibility |
| --- | --- | --- |
| `claude-project_plan/` | `plan` | Requirements, contracts, P-card readiness and handoff |
| `claude-project_dev/` | `dev` | Adopted implementation, verification and execution logs |
| `claude-project_main/` | `main` | Release baseline; promotion requires an explicit request |

Start a new or resumed session by reading this entrypoint and the appropriate
child AGENTS.md/CLAUDE.md, policy, actual status/branch, adoption, current P cards,
committed dev progress, active writers and scoped stops/decisions. Earlier chat
history is not needed. Keep an explicit human role assignment. A directory or
branch name does not assign a role. In a plan-assigned chat, implementation
requests become plan preparation/review/handoff, never implementation on plan.
Unassigned material requests follow P-card preparation in `claude-project_plan/`
then exact adoption and implementation in `claude-project_dev/`. Reuse an applicable
card or prepare the next unused one. A session may perform both stages only with
matching authority and no competing writer; use the proper child for each stage.
Read-only questions need no new P card; an explicit planning-only draft can end
on plan. Initialization alone reads status and waits.

README, user guides and release notes are dev deliverables after exact adoption.
Planning requirements/reviews/governance are plan-owned; changes needed by dev
still require integration and adoption. For document delivery, record file,
repository and target ref. A plan push is not dev adoption or target-ref delivery.
Check requested ref/content before claiming completion. With no requested ref,
follow configured plan/dev delivery and report branches; do not infer main promotion.
Missing messaging authority/tools leaves a pending file handoff, not sent work.
Preserve scoped pauses/OPEN decisions and existing writers. Passing plan hooks
is not proof of an approved card or a mechanical barrier to plan implementation.
Full procedure: selected child's `docs/process/agent-workflow.md`, section
"Fresh sessions and document delivery".

If a missing business decision changes the scope, ask before dependent work.
Do not choose a role from the workspace root's name or run Git at this level.
Use explicit working directories; do not assume a previous shell's `cd` persists.

A chat initialized by the user as plan or dev keeps that assigned role across
turns. In a plan chat, “다음 작업” means planning in `claude-project_plan/`; in a dev
chat it means the development queue in `claude-project_dev/`. Do not silently switch
roles because both children are visible. The initial role instruction and later
explicit user requests determine scope; a title is only a navigation label.
Creating or bootstrapping role chats reads status/rules/queues and then waits;
it does not authorize new product work or messaging another chat.

All three directories share one Git repository through linked worktrees.
Preserve existing work, P-card requirements, dev execution logs and adoption rules.
Inspect status and the current branch before changes. Never merge dev into plan
just to transfer completion marks. Honor existing remote/push authorization;
release promotion and release pushes require an explicit user request.

From this directory, inspect the queue with:

```sh
(cd claude-project_plan && python3 scripts/work_queue.py --owner all)
(cd claude-project_dev && python3 scripts/contract_guard.py check)
```

This local entrypoint is outside Git. Tracked instructions in each worktree must
also describe this layout so it can be recreated on another computer. The release
worktree may retain historical instructions until explicitly promoted; the path
mapping above describes the current local workspace.

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

Use the selected child's docs/process/workflow-controls.md for the complete procedure.
