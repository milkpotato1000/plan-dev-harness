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

## 실제 준비 확인 — 2026-11-25

사용자가 기존 fixture plan에 입력했고 준비됐다고 알렸다. 최초 조회 때 plan은 실제 busy였고
커밋 전이었으며, 읽기 전용 확인 중 기존 plan이 단계 A 파일을 작성·커밋한 것을 관찰했다.
최종 준비 commit은 9f78cb9ccd2fd23f8c82d73c2ffe573609696a75, fixture plan clean.
P903 READY/미착수, P904 DRAFT/미착수 및 두 검토 문서를 실제 읽어 보충 계약과 대조했다.
Fixture dev는 기존 f69f30a 채택과 완료 P901/P902만 있으며 P903을 아직 시작하지 않았다.
따라서 RELAY_INPUT_PENDING을 PREPARATION_VERIFIED로 갱신한다.

정확 준비 blob SHA256:
- P903.md: be8bbd160529ae30b2542d7b5f96a593ec2bdf6a379fc24649ff11e200b7f4c4
- P904.md: 763e09ae2e7fa77e37adeea974882e6648c77fc95e36f8e222a6beab30ba1fce
- P903-review.md: 246f339f683d27bcefd3c9e0f9aa773d91cf71e0035600f4ac64cf183333c319
- P904-draft-review.md: 3a0b33b4cc6c75146ee4a4791ab0ca581859a628fded54e4673e4e4b63c71ee3

P903 JSONL의 검증/예상값·CLI 오류 범위는 parent 계약과 일치한다. P904 제안 기본값은
--format csv, record 오류 stderr 보고/exit 2, csv 기본 CRLF, 정수 숫자 열이다. 기본 JSON,
P903 선행/오류 의미는 유지한다. 아직 실제 사람의 P904 확정 입력은 없으므로 READY로
해석하지 않는다. 다음 시험은 아래 두 실제 사용자 입력을 fixture plan에서 받는다.

1. 준비된 P903 정확 검토 commit을 기존 dev에 전달하고 즉시 기획으로 복귀; P904는 초안 유지.
2. 실제 dev P903 작업 중 같은 plan에 P904를 제안 기본값으로 검토·확정하고 정확 commit을
   기존 dev에 전달하도록 입력. 기본 JSON/P903 선행·exit 의미 보존.

이 두 입력은 실제 사람 기획 turn과 busy 수신의 시험 근거이며 observer가 대신 전송하지 않는다.
새 신뢰/채택 승인이 아니고 기존 터미널을 그대로 사용한다. Parent dev는 기존 worker의 실제
시각·작업/수신·적용·결과를 관찰해 보충 판정한다. 아직 단계 B 실행/C3 통과를 주장하지 않는다.

## 실제 단계 B 입력 보고 — 2026-11-25

두 시험 입력 안내 뒤 실제 사용자가 이 parent plan에서 “했어”라고 답했다. 읽기 전용 조회에서
fixture plan ca472a5(P903 SENT 기록), fixture dev 2ca41fe(P903 정확6758949e87e8c5c797acd789f4a8deae40d050da
적용)를 확인했다. plan 타임라인은 09:32:36 native P903 send와 실제 P904 후속 사용자 메시지의
처리 시작을 기록했다. 조회 시 P904는 아직 DRAFT였다. 이는 진행 중 관찰이며 최종 판정이 아니다.
타임라인에 앞선 요청/확인 거절 이력도 있어 보존하고 최종 native 증거와 대조한다.

상태 STAGE_B_INPUT_REPORTED_AND_P903_APPLIED. 같은 입력/승인을 반복 요구하지 않는다.
새 사용자 turn의 실제 접수 시각, dev의 실제 구현 시작 시각, P904 검토/전송/수신과 P903의
완료·안전 경계 및 P904 적용 순서를 observer가 확인한다. 사용자의 “했어”만으로 중첩이나
성공을 확정하지 않으며 실제 action/시간이 기준이다. 기존 실행을 중단하거나 새 worker를
만들지 않고 결과 artifact를 기다린다. 원래 실패·중지·권한 경계를 보존한다.
