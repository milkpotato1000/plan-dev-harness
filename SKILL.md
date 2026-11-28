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

## Independent worker execution

Default to distinct plan and dev host sessions with one writer per worktree.
Plan records the human execution approval/delegated scope, prepares reviewed READY
work and sends the exact commit to the verified independent dev, records the actual
outcome and returns to planning. Plan must not implement products in either tree,
run dev adoption for the worker, or wait/poll for ACK, adoption or completion.
Dev performs internal receive/integrate/adopt at a safe committed boundary without
asking the human to type another adoption message. Keep the existing adopt CLI and
record formats; a peer message is not new human authority. Preserve current work,
failed evidence, priorities/dependencies, OPEN decisions and explicit pauses.

Missing worker, native tools, matching human grant, distinct identity or unambiguous
recipient means pending handoff with the exact missing condition. A held/refused or
unknown send is not SENT; preserve attempt evidence without blind retries. Never
replace a parallel request with plan doing dev work. Sequential dual-role mode is
available only after a separate explicit human choice of that mode and exclusive
writers; a general request to finish work is insufficient. Do not automatically
create extra workers, enable teams, change permissions/inbound settings or start a daemon.
Bootstrap-only requests remain read-only and wait. A subsequent authorized work
handoff is distinct and can execute without a second human adoption prompt.
Use the read-only worker doctor and native host procedure; diagnostics never
approve, send, adopt or run work. Send results/needed decisions through the plan
review gateway with one request key; no duplicate user completion questions.

See [Claude workers](references/claude-workers.md) and `scripts/worker_doctor.py`.

## Local session registration — source 0.2.5

After authorized setup, preview/apply `scripts/configure_sessions.py` with explicit plan/dev worktrees and role reference. Read [registration and reconnect](assets/docs/process/session-registration.md). Raw host startup registers identity only; it never approves, sends, resumes, takes over or starts work. Same-host discovery uses fresh official evidence; unsupported CLI/app transport remains pending. Preserve existing hooks/settings and global installations.

## Codex에서 기존 Claude 세션으로 인계하기 (0.2.6 개발 소스)

등록한 두 역할과 커밋된 PENDING 인계가 있는 프로젝트에서 실행합니다.
전달 전용 Python 가상환경에 `claude-agent-sdk==0.2.189`를 설치하고 평소 사용하는
Claude CLI로 로그인합니다. 인계 문서의 실제 승인 근거를 지정합니다.

```sh
python scripts/claude_relay.py --repo . --event docs/progress/handoffs/plan/EVENT.json --authority-reference '검토 문서와 사용자 승인 위치'
```

중계는 모델을 한 번 실행하며 예산은 0.50 USD, 제한 시간은 60초입니다.
중복 키와 불명확한 결과는 수신 기록을 검토해야 합니다. 수신 세션의 hold 또는
refuse 정책이 적용됩니다. 현재 실제 환경에서는 도구 노출과 사전 거부를 확인했고
첫 P901의 수신과 후속 인계는 검증 중입니다.
