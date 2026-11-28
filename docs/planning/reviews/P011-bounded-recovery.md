# P011 발송 전 거부와 제한된 후속 시험 검토 — 2026-11-28

Common key: `P011-official-claude-relay`. 기존 실제 인간의 공식 연결 구현·반복 입력 제거
승인 안에서의 검증 복구 결정이다. 새 제품 범위, 권한 확대나 사용자 중지 재개가 아니다.

## 검토한 증거

결과 `335183562eb1d990bbce96ced55ae29b502cd53c`의 report, live.json, tests.json,
review packet과 source `1c3dd70c54f5e27a536ab820e0c36bc4126ab2de`의 relay를 읽었다.
Manifest SHA256 `08e4cda4b97282bdcee65b0995c743044c1faec4db3b22d806c5905f35400586`
및 4개 artifact hash를 Git blob에서 재검산하여 일치를 확인했다.

기록은 SDK pre-execution callback이 실제 SendMessage 인자를 거부했고 허용되지 않았다고
보고한다. 해당 key의 수신 기록은 두 대상에서 0이다. 코드는 인자가 정확히 맞고 identity와
verify를 통과해야 attempted/valid가 참이 되며 그렇지 않으면 deny를 반환한다.
현재 요약은 각 필드의 실제 값/거부 사유 전체를 보유하지 않는다. 이후 격리 probe의 content
미리보기 재현을 과거 실제 거부 원인으로 소급 확정하지 않는다. 모델의 exit 0도 성공 증거가 아니다.

108-test 전체 통과는 preview 수정 전이고 최종 변경에는 focused 4개 PASS가 있다.
최종 소스 전체 회귀가 수행됐다고 표현하지 않는다. P901 수신/실행 및 두 번째 전달은 미검증이다.

## 결정 R1 — 기존 시도 보존과 분류

원래 logical handoff key와 예약된 시도/unknown 원문은 삭제·초기화·덮어쓰기하지 않는다.
새 event/key로 바꿔 중복 방지 장치를 우회하지 않는다. 별도 append-only disposition에
원래 key의 가명/hash, source SHA, 실제 trace/deny evidence hash, 종료 확인을 연결한다.

다음 모두 확인될 때에만 해당 시도를 `REJECTED_BEFORE_SEND`로 분류할 수 있다:

1. 해당 시도의 SendMessage가 승인 경계를 통과하지 않았음을 실제 callback deny/실행 trace로 확인.
2. 같은 실행에서 다른 SendMessage가 허용되거나 실행되지 않았음을 제한된 trace로 확인.
3. relay 프로세스가 끝나 뒤늦은 발송이 불가능하며, 대상/동일 key의 기존 receipt도 없음.

수신 기록이 없다는 사실만으로는 충분하지 않다. 위 증거가 불충분하거나 callback을 통과한
시도가 있으면 UNKNOWN을 유지하고 이 승인으로 다시 보내지 않는다. 추측으로 거부를 확정하지 않는다.

## 결정 R2 — 동일 인계에 연결된 후속 live 한 번

R1이 충족되면 원래 logical key/정확 target/전체 payload hash를 그대로 둔 별도 recovery
attempt 1회를 허용한다. recovery authorization은 이 reviewed commit 전체 SHA와 연결한다.
동시 시도를 막고 consumed 상태를 원자적으로 예약한다. 실제 키/nonce는 로컬에만 보관한다.
이미 delivered/held/refused/unknown execution이라면 이 경로를 사용할 수 없다.
기존 sender가 계속 살아 있거나 writer/target/권한이 달라졌으면 보류한다.

기존 거부 trace와 수정 원인 증거는 유지한다. preview는 관찰된 정규 형식만 허용하고 full
message/recipient/summary 및 알 수 없는 필드 검증을 약화하지 않는다. 새 시도에는 각 필드의
match boolean/허용한 정규화 종류/사전 거부 사유/실행 허용 여부/native 결과를 제한적으로
기록한다. 비밀/원시 ID/전체 대화는 공개하지 않는다. 차단 또는 실패하면 자동 재시도하지 않는다.

이번 복구 구현은 P011의 중복/unknown 처리 검증을 위한 범위 내 수정이다. ledger history와
인계 authority를 연결하는 명시적 recovery 경로를 쓰고 일반 자동 retry 정책으로 확대하지 않는다.
단위 검증에서 원래 키 재사용 차단, recovery 승인 없는 요청, 회수/기소비 승인, 경합,
송신 전 거부와 송신 후 불명의 구분을 확인한다. 최종 수정 source 전체 회귀를 실행한다.

## 결정 R3 — 실제 성공과 다음 단계

원래 W1~W7의 target freshness/권한/중지·OPEN/현재 writer 재확인과 timeout60초/비용0.50USD
한도를 유지한다. 기존 두 fixture 세션을 재사용하고 resume/강제 종료/설정 확대하지 않는다.
실제 전송 결과와 receiver 입력/key/역할 행동을 각각 확인한다. native result가 모호하면
성공으로 변경하지 않는다. 첫 작업이 실제 진행/완료되면 기존 승인 runbook 안의 두 번째
전달 검증을 수행할 수 있으며 이는 첫 실패의 반복 retry와 구분한다.

사람에게 계속 문장을 다시 입력하도록 요청하지 않는다. 새 실제 플랫폼 승인이 필요한
경우에만 정확 근거/최소 행동을 같은 plan 창구에 전달한다. P010 C3 전체나 P009 실패를
자동 완료로 바꾸지 않는다. 결과와 실패/한계를 같은 key로 한 번 인계한다.
기존 source/0.2.5 증거·중지·개인 설치·main/tag는 유지하고 공개 릴리스는 하지 않는다.
