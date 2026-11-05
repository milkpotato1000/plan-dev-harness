---
name: plan-dev-harness
description: Set up or upgrade linked plan/dev Git worktrees, P-number planning, exact plan adoption, evidence-backed queues and dev-to-plan requirement intake. Use for harness setup or migration, not ordinary feature work.
---

# Plan/dev harness

Works with Codex and Claude Code through shared Git/Python files. Tool-specific
chat creation or messaging is optional, never a dependency or automatic permission.
Read [workflow and ownership](references/project-instructions.md) for setup and
[usage](references/usage.md) for actual commands. Scripts resolve assets from this
skill directory; invoke them by absolute path if the current directory is a project.

For the generated project's new or resumed sessions, require file-based state
reconstruction and preserve explicit roles. Unassigned material requests follow
P-card preparation -> exact dev adoption -> dev execution; plan-only drafts and
read-only questions keep their narrower scope. Product documentation is dev work,
while planning contracts belong to plan and must reach dev when needed. A plan
push alone is not completed delivery. See
[fresh sessions and document delivery](assets/instructions/agent-workflow.md#fresh-sessions-and-document-delivery)
for role, writer, target-ref and pause boundaries. Put these rules in actual
outer/child entrypoints during setup or reviewed upgrades, not only this skill.

1. Inspect project AGENTS.md/CLAUDE.md, status, worktrees, branches, remotes, adoption,
   hooks and active writers. Preserve existing work. Infer existing destinations;
   ask only for missing identifiers or decisions. Setup is not product approval.
2. For a NEW project, preview `scripts/bootstrap_workspace.py --parent ... --name ...`.
   It creates an absent container with linked main/plan/dev children, both instruction
   entrypoints, infrastructure commits, exact adoption and local hooks. Apply only
   under setup authorization. It does not create a remote or publish anything.
3. For an EXISTING repository, preview `scripts/install_harness.py --repo ... --protect ...`.
   Install on plan (or an unborn bootstrap branch). Branches and protected paths are
   configurable. `--agent both` writes shared instructions and a CLAUDE.md import.
   Differing instructions/hooks are a merge task, not permission to overwrite.
   `--upgrade` replaces only files matching the previous installation hash; use the
   original options. Customized and legacy installations require reviewed integration.
4. Review plan scope and commit; dev integrates the exact commit, records adoption
   with a real review reference, stages adoption, then finishes the merge. Activate
   hooks only once all participating worktrees have the scripts. Honor release and
   remote permissions. No force/reset, implicit main promotion, or inferred publication.
5. Use the P-card template; no invented READY tasks in an empty project. Plan owns
   readiness; dev owns bounded execution marks and append-only logs. Latest PASS and
   committed nonempty evidence are required for checked conditions. Never remove a
   failed check or loosen requirements to finish. Queue reads never perform actions.
6. New scope raised in dev: immutable request → plan review → prepared P card → exact
   adoption → implementation. Keep scope-contained repairs moving. Dev does not
   author/approve new plan scope by switching roles unless the human authorizes it.
7. Verify guard worktree/index/HEAD, queue, hooks, branch roles and shared Git common
   directory. Report actual tests, paths, adoption, pushed/local-only state and next
   eligible work. Local hooks are bypassable safeguards, not access control.

Keep an explicitly assigned plan/dev role across turns. Bootstrap chats read and
wait. Respect explicit stops. Git handoff works across tools; messaging needs user
authorization and host support. When no tool exists, leave durable handoff files.

Optional legacy sibling-worktree migration uses `scripts/nest_worktrees.py`; read
[its boundary](references/workspace-layout.md) and coordinate writers before moving.
Never install/update this skill globally as a side effect of project installation.

The installed v0.2 controls distinguish ordinary intake, critical decisions and
explicit user pauses. Read [controls](assets/docs/process/workflow-controls.md)
when installing/upgrading these features. Preserve legacy decisions/checkpoints,
plan-owned scope classification and actual delivery evidence. A package upgrade
must not resume work or replace a project's same-named daily-work skill.
For authorized delivery to an existing role chat, follow
[direct handoff](references/direct-handoff.md). Verify the human grant and recipient,
send directly when supported, record/commit/push actual SENT, then finish the plan
response without waiting for ACK, adoption or dev completion. Observe receipts
only on a later natural planning/status request; unobserved ACK stays SENT.
Busy dev preserves its current P and failures, and adopts the exact reviewed
handoff only at a safe completed/checkpointed commit boundary. Choose the next P
by readiness, priority, dependencies and existing stops/decisions. See the shared
[parallel planning rules](assets/instructions/agent-workflow.md#asynchronous-handoff-and-parallel-planning).
This procedure grants no messaging authority by itself.
For dev results and needed decisions, use the [plan review gateway](references/user-review.md).
Commit a packet with a stable shared key, exact artifact version/hash, scope and
existing human-answer sources. Plan opens read-only results, reuses valid answers
and asks necessary human judgment once; dev does not issue routine completion
questions. Optional review does not block independent work, required human criteria
remain incomplete, and critical OPEN/pauses keep their existing rules. Decisions
reach dev through exact reviewed adoption. Reverse delivery needs its own actual
human grant; installation alone grants none.
External integrations follow [adapter boundaries](assets/docs/process/optional-adapters.md).

인간이 해당 프로젝트의 plan→dev 전달·착수를 위임한 경우 plan은 검토된 READY 계획의 정확 SHA를
확인된 기존 dev에 직접 전달하고, dev는 기존 작업·실패를 보존해 통합·정확 채택·커밋·guard/큐
확인 후 승인 범위를 시작합니다. 설치 자체는 위임이 아니며 초기화는 읽기 전용 대기를 유지합니다.
