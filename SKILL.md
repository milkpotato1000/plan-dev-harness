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
send directly when supported, and observe actual receipt without ACK loops.
This procedure grants no messaging authority by itself.
External integrations follow [adapter boundaries](assets/docs/process/optional-adapters.md).

인간이 해당 프로젝트의 plan→dev 전달·착수를 위임한 경우 plan은 검토된 READY 계획의 정확 SHA를
확인된 기존 dev에 직접 전달하고, dev는 기존 작업·실패를 보존해 통합·정확 채택·커밋·guard/큐
확인 후 승인 범위를 시작합니다. 설치 자체는 위임이 아니며 초기화는 읽기 전용 대기를 유지합니다.
