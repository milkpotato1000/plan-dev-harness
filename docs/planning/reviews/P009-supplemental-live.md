# P009 C3 보충 실제 시험 계약 — 2026-11-25

READY: 기존 P009의 시험 적합성 보완이다. 제품 기능·자동 등록·재접속·release 범위를 추가하지
않는다. 기존 P901/P902 완료·실패·상충 기록과 89-test source 증거는 그대로 보존한다.
실제 두 Claude 세션과 기존 parent observer를 재사용하며 새 worker/daemon/권한 변경은 없다.

## 부족한 증거

기존 시험은 실제 기획 작성 중첩과 전달·순차 적용을 확인했으나, 새 인간 기획 turn 및 busy
dev의 후속 handoff 수신을 충족하지 못했다. 사람의 새 대화를 꾸미거나 기준을 낮추지 않는다.
이 보충 시험은 중첩 시간을 인위적 sleep/ACK 대기로 늘리지 않고 의미 있는 작업으로 구성한다.

## 제한된 fixture 작업

Fixture plan이 다음 미사용 번호를 확인한다. 현재 P903/P904가 비어 있으면 사용한다.
번호 충돌 시 기존 카드를 덮어쓰지 말고 다음 미사용 번호를 실제 packet에 기록한다.

- P903: 기존 formatter/summary를 재사용하는 JSONL 배치 처리와 작은 CLI를 추가한다.
  각 nonblank line은 object이며 group은 문자열, lines는 문자열 배열이어야 한다.
  올바른 record는 기존 함수로 정규화하고 group별 record count, normalized line count,
  separator 제외 character count를 집계한다. JSON 오류/형식 오류는 1-based 입력 줄 번호와
  error code를 결과에 남기고 다음 줄을 계속 처리한다. group 출력은 이름순으로 결정적이다.
  CLI는 지정 UTF-8 파일을 읽고 JSON 결과를 stdout에 쓰며 record 오류가 있으면 exit 2,
  파일 I/O 오류면 exit 1, 성공이면 exit 0이다. Unicode·빈입력·빈그룹·잘못된타입·mixed valid/
  invalid·중복그룹·trailing newline·CLI exit/output와 기존 회귀를 의미 있게 검증한다.
- P904: P903 group summary를 CSV(group,records,lines,characters)로 내보내는 옵션을 추가한다.
  기본 JSON은 유지하고 csv 모듈로 쉼표/따옴표/Unicode를 처리한다. 헤더만 있는 빈 결과,
  결정적 순서와 exit semantics/기존 회귀를 검증한다. P903을 선행으로 둔다.

이는 임시 fixture에서만 수행하는 검증 payload다. reusable distribution에 배치/CSV 기능을
추가하지 않는다. 시간 늘리기 위한 반복 연산·거짓 실패·불필요한 sleep·benchmark는 금지한다.

## 단계 A — 준비만 수행 후 구체적 사용자 행동 packet

Fixture plan이 P903 범위/검토/정확 commit을 준비하고, P904는 후속 논의에 사용할 DRAFT와
짧은 검토 재료를 준비한다. 승인된 parent 계약이 payload 근거지만 실제 사람의 후속 turn을
아직 받은 것으로 표시하지 않는다. Dev는 기존 clean/idle 상태·fixture writer를 확인한다.
이 단계에서는 P903을 구현 착수시키지 않는다. 사용자 안내 전에 실행 구간을 소모하지 않는다.

Observer는 실제 기존 plan 터미널의 식별 가능한 이름/위치, 준비 artifact, 아래 두 입력의
최소 명령 및 실제 현재 상태를 parent plan에 한 packet으로 전달한다. 필요 도구가 없으면
기존 역할을 대신 수행하지 말고 정확한 제한을 보고한다. Native 인계는 기존 fixture의
실제 위임·권한 범위에서만 하며 설정 변경 요청/키 주입/소켓 우회는 하지 않는다.

## 단계 B — 사람과 실제 겹치는 기획 및 busy handoff

준비 완료 후 parent plan이 사용자에게 기존 fixture plan 터미널에서 사용할 두 짧은 입력을
한 번 안내한다. 이는 새 승인이나 trust가 아니라 실제 병렬 대화 시험 행동이다.

1. 먼저 P903을 dev에 전달하고 즉시 기획으로 복귀하도록 입력한다.
2. 실제 dev 구현이 시작된 동안 같은 fixture plan 터미널에서 P904 CSV 요구의 검토·확정을
   요청하는 새로운 사용자 turn을 보낸다. Fixture plan은 그 실제 입력과 현재 기준으로
   P904를 검토·READY commit/native 전달한 뒤 복귀한다. 기존 초안은 반응 시간을 줄이는
   준비 자료이며, 실제 사용자 입력 이전의 검토·전송으로 꾸미지 않는다.

Dev는 P903 구현/검증을 계속하며 실제 native tool 경계에서 후속 인계를 수신하고 pending으로
기록한다. 수신 시 current P·정확 adoption·작업/실패를 보존한다. 완료 또는 실제 안전한
checkpoint commit 뒤 P904 정확 SHA를 내부 적용하고 순차 실행한다. P903을 인위적으로
기다리게 하거나 READY를 미리 적용해 busy 수신을 연출하지 않는다.

## 판정과 경계

실제 user turn, plan의 검토/작성, native 송수신, dev current P 및 완료/checkpoint·후속 적용
시각을 구분한다. 단순 file mtime/최종 commit 시각만으로 중첩을 추정하지 않는다.
필수: P903 실제 실행 구간에 새로운 인간 계획 turn/plan 검토가 존재하고 P904 수신도 그
완료 전에 일어나며, P904 적용은 P903의 실제 안전 경계 뒤임을 증명한다.
시각이 다시 맞지 않으면 실패/미검증을 보존하고 parent plan에 돌려보낸다. 자동 반복·새
fixture 카드 증식·기준 완화는 하지 않는다. 새 인간 입력을 observer가 대신 보내지 않는다.

증거는 기존 live 결과와 구별된 보충 디렉터리에 append-only로 남긴다. 원시 session IDs/
대화는 로컬에 두고 공개 artifact는 필요한 비민감 action/time/hash만 내보낸다. 관찰 담당은
fixture 업무를 대신하지 않고 완료 뒤에만 독립 테스트/guard 확인을 한다. 전체 제품 source가
변하지 않았다면 기존 89-test를 불필요하게 반복하지 않는다. P009 C3 완료 여부는 실제 보충
결과를 plan에서 검토한 뒤 판단한다. 다른 중지·OPEN·권한 경계는 그대로 유지한다.
