# P009 live fixture preparation

Client date 2026-11-24. Common preparation key: P009-live-setup-v0.2.4.
Reviewed delivery dede131be57a3cf07a7ced368f05cb74e2447020 was internally applied after
P008's final SENT/completion push. The actual human harness-test install/test
request was directly verified in the existing parent plan chat. No repeated
human adoption input was requested.

Source 0.2.4 introduces independent worker rules, native Claude/Codex procedure,
read-only worker_doctor and six behavioral tests (all passed). Complete regression
and live M1–M3 remain pending at this preparation checkpoint.

The actual user-selected local container was empty/non-Git and had one idle
interactive Claude session. Official host CLI inventory confirmed it; earlier
sandbox inventory absence was not treated as actual absence. Private mapping and
setup command logs are retained locally, not in this public artifact.

Preview/apply installed only the project's .claude/skills/plan-dev-harness and a
new p009 child workspace with linked p009_plan/p009_dev/p009_main, local guards,
empty queue and exact infrastructure adoption. Both worktrees run the installed
doctor. Identical reinstall KEEP passed. Outer AGENTS/CLAUDE and P009-TEST.md record
actual human authority, explicit fixture roles and bounded P901/P902 scenario.
No fixture planning card or product implementation was authored by the coordinator.
The existing interactive session remains available. No extra worker started at
this checkpoint, no global skill/settings or public release changes.

## Starts and first inputs

Use existing plan rather than restarting/resuming it as a competing copy. It is
at <fixture-root>, with plan child <fixture-root>/p009/p009_plan.
If a human input is actually required in that session, the prepared minimum is:

> P009-TEST.md와 AGENTS.md를 읽고 이 fixture의 plan 역할로 시험을 시작해.
> 기존 실제 승인 범위에서 P901을 준비·검토·커밋하고 별도 dev에 native tool로
> 전달한 뒤 복귀해. dev 구현/채택을 대신하거나 완료를 기다리지 마.

For the one authorized independent dev, reuse a verified existing peer or start
using the official CLI at <fixture-root>/p009/p009_dev:

```sh
claude --name p009-fixture-dev
```

First input:

> 이 fixture의 dev 역할이다. outer와 child 지침 및 P009-TEST.md를 읽고
> 실제 승인 범위·독립 plan·단독 writer를 확인해. P901/P902의 정확 검토 SHA를
> 내부 수신·적용하여 순차 실행하고, busy 작업과 실패·중지·OPEN을 보존해.
> plan 기획을 대신하거나 사용자에게 같은 채택 입력을 다시 요구하지 마.

The same role prompt can start the one dev using official --bg, keeping the model
session independent. A background process alone is not overlap evidence. Do not
change permissions/inbound policy to make it pass. Native ListAgents/SendMessage
and actual role/time/commit evidence must demonstrate P901 work overlapping a
separate P902 planning turn and safe sequential P902 application. If actual human
P902 planning/input or permission is necessary, leave C3 incomplete and identify
that specific action through parent plan. Do not fabricate a human turn.

Plan owns fixture planning, dev owns fixture implementation, coordinator owns only
installation/observation and parent evidence. Sessions and files remain preserved
when the bounded test ends; cleanup needs a separate request. Public evidence uses
aliases; exact local commands/paths are delivered privately to existing plan.
