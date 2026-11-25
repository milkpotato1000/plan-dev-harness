# P009 보충 단계 A 전달 제한 검토 — 2026-11-25

Common key P009-supplemental-stage-A; linked P009-live-setup-v0.2.4.
정확 결과952ca73b0af9179c46629e597ceff341123a808d의 preparation.md를 읽고 SHA256
823a10313807200ce7f50fc6b0d28b34bbfb8b4a38fce05f9c4c2e96c6a199d5를 재검산했다.
실제 로컬 P009-SUPPLEMENTAL-PREPARE.md도 읽고 SHA256
ab9b61c7107db314b3f5808b1110a0ef7353674db5bd2f9069ed4a27dcb3f0ab를 확인했다.

현재 parent Codex에서 기존 fixture Claude로 직접 보내는 도구는 확인되지 않았다.
이 제한은 Claude끼리의 성공한 native 메시징과 별개다. 소켓/키 주입/동시 resume/새 relay
worker로 우회하지 않으며 observer가 fixture plan 카드 작성을 대신하지 않는다.
준비된 relay는 실제 P903 READY/P904 DRAFT가 아니다. 단계 A와 C3은 아직 미완료다.

상태 RELAY_INPUT_PENDING. 기존 fixture plan 터미널 한 곳에 준비 파일을 읽고 단계 A만
수행하라는 정확한 한 문장을 안내한다. P903을 전달/구현하지 말고 실제 준비 commit과
단계 B의 두 입력을 돌려주도록 한다. 이는 trust/실행/채택 승인 재요청이 아니다.
입력 전달·준비 결과를 아직 관찰하지 않았으며 전송 성공/완료로 기록하지 않는다.
기존 두 터미널/카드/실패·작업은 보존한다. 같은 입력을 dev에서 중복 요청하지 않는다.
