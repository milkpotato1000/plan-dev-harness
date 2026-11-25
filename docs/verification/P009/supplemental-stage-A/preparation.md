# P009 supplemental stage A: prepared relay, native transport unavailable

Client date2026-11-25. Key P009-supplemental-stage-A; linked preparation key
P009-live-setup-v0.2.4 and original result key P009-live-P901-P902-results.
Exact reviewed delivery98e88dbea1b560dee31017fb980ab78a6bd934b9 applied internally;
content173108e229ac4d635ef9cf5b0605ff6f59cb3236.

## Actual state

Official host inventory: existing fixture-plan and fixture-dev both interactive/idle.
Plan clean atbd8d5f92ad09f6c0ce65ecc328df83d4087ad98e; dev clean at
c387f9d536d7d500b4c18a99ca9422d12f90d152. Only P901/P902 exist in both card directories;
P903/P904 are free at observation time. Fixture plan must recheck before writing.
No worker creation/restart/stop, no role takeover, no P903 implementation or send.

Current parent Codex host has no native Claude ListAgents/SendMessage tool. Its
send_message_to_thread addresses Codex/ChatGPT chats, not these Claude sessions.
Official local claude --help and claude agents --help expose inventory and session
management but no documented CLI command for sending into an existing interactive
session. The fixture native adapter worked inside Claude in the previous test;
this missing parent-to-Claude transport is distinct from that successful adapter.
No raw socket, iTerm key injection, concurrent resume/copy or new relay worker used.
The supplemental contract expressly requires honest reporting when no tool exists.

## Concrete preparation

Observer prepared one local relay file <fixture-root>/P009-SUPPLEMENTAL-PREPARE.md,
SHA256 ab9b61c7107db314b3f5808b1110a0ef7353674db5bd2f9069ed4a27dcb3f0ab.
It contains the exact adopted supplemental contract and stage A-only bounds.
It is not a fixture P card, a reviewed fixture commitment or a new human P904 turn.
No source, installed instructions/settings or fixture worktree was changed.

Parent plan can provide this one minimum preparation input in the **existing fixture
plan terminal at <fixture-root>**, using its privately verified current name:

> P009-SUPPLEMENTAL-PREPARE.md를 읽고 단계 A만 수행해. P903 READY와 P904 DRAFT를
> 준비·커밋하고 정확 SHA와 두 짧은 시험 입력을 알려줘. P903을 dev에 보내거나
> 구현을 시작하지 말고, 기존 P901/P902와 두 세션을 보존해.

This is a tool-availability prerequisite, not renewed trust/execution approval or
an adoption input in dev. Do not start stage B before actual preparation exists.
Parent observer can inspect those committed artifacts after the input; it cannot
write the fixture cards for plan. No generic request to reopen two terminals.

## Stage B input drafts — not sent, not ready to run yet

After the fixture plan returns an actual reviewed preparation SHA and card numbers,
parent plan should verify them and give the human the final two short inputs once:

1. “준비된 P903의 정확 검토 커밋을 기존 dev에 전달하고 바로 기획으로 복귀해.”
2. During actual dev P903 work, in the same fixture plan terminal:
   “P904 CSV 내보내기 요구를 검토·확정해. 기본 JSON과 P903 선행·오류 exit 의미는
   유지하고, READY 정확 커밋을 기존 dev에 전달한 뒤 복귀해.”

These are proposed future human actions. Neither was typed/sent by the observer.
If numbers changed, the actual preparation packet must use verified numbers.
Keep P903 idle now so the execution window is not consumed before human guidance.
No artificial sleeps, polling ACK, fresh workers, automatic retries or weakened C3.

## Status

Stage A fixture planning: **NOT STARTED** (relay input needed).
Stage B dispatch/implementation/human follow-up: **NOT STARTED**.
P009 C3 incomplete, prior failure records retained. Existing89-test source payload,
0.2.3 main/tag and personal installs are unchanged; no full regression rerun needed.
