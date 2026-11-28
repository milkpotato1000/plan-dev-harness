# P011 content 표현 격리 진단 — 2026-11-28

Common key `P011-official-claude-relay`. 기존 공식 연결 구현 승인 범위의 원인 조사다.
실제 수신자에 대한 추가 recovery 승인이 아니다.

결과 `47dbe3a54792cc2d33b96dc417a00e4c15fdd814`의 report/outcome을 읽고 manifest
SHA256 `c3cbb5162a9a606f4e128efea26721bead02a22e8b52bcef8b855c73a48da833` 및 3개
artifact hash를 독립 재검산했다. Source `de40ec9255b67959e871247a676d8cb920214031`에서
소비된 recovery는 target/recipient/message/summary 일치, content의 full/preview 불일치로
callback deny 됐다. 수신 key0, sender 종료, 기존 ledger 불변 증거를 유지한다.
최종110tests/34설치 검사 보고는 source에 대한 검증이며 실제 전송 성공이 아니다.

## 결정

동일한 실제 send를 또 실행하지 않는다. 이미 소비된 recovery와 unknown 원문은 그대로 두고,
표현을 보지 못한 상태에서 preview 허용 패턴을 계속 늘리거나 content 검사를 삭제하지 않는다.
원인이 모델이 만든 필드인지 CLI/SDK 정규화인지 아직 구분되지 않았다.

Dev는 다음 bounded 격리 진단을 진행한다:

1. 설치된 공식 SDK/CLI schema와 공식 hook/SDK 문서에서 SendMessage의 실제 입력 필드,
   canonical body/recipient 의미와 callback 입력 변환 경계를 확인한다. 문서가 없는 의미를
   private socket 역공학으로 채우거나 한 번의 관찰을 안정된 API 계약이라고 단정하지 않는다.
2. 새 synthetic ASCII/한글·30자 초과 payload와 존재하지 않는 fixture recipient만 사용한다.
   실제 세션 ID/실제 handoff 내용을 넣지 않고, native 실행 전 항상 deny하는 callback을 둔다.
   model 원래 tool_use input과 PreToolUse 입력을 가능하면 함께 비교한다. 순수 synthetic
   필드 값은 그대로 보존해 의미를 분석할 수 있으며 개인 metadata는 제거한다.
3. 최대 3개의 격리 모델 호출, 각 60초/0.50USD 이내. ListAgents 실제 세션 열람이나
   SendMessage native 실행은 불필요하며 허용하지 않는다. 검증된 항상-deny 없이 호출하지 않는다.
4. 차이가 모델 출력/SDK 변환/표시용 요약 중 어디서 생기는지 증거로 분리한다. 필요하면
   mock SDK trace 및 표준 unit test로 재현하고 실제 모델 호출을 반복해 맞추지 않는다.
5. 정확 payload를 보장할 수정안을 제시한다. 공식 callback의 검증 가능한 입력 교체가
   지원된다면 canonical field만 생성하는 설계를 검토할 수 있으나 권한 우회가 되어서는 안 된다.
   최소 필드·허용 타입·추가 필드 거부·정확 bodyhash/recipient 검증과 negative tests를 유지한다.

범위 내 진단/코드 수정/단위 검증과 필요한 최종회귀는 dev가 진행한다. 그러나 기존 실제
수신자에 보내는 새 live 시도는 원인·설계·격리 검증 결과를 plan에 인계하여 구체적 다음 검토를
받은 뒤 진행한다. 같은 사용자 계속 문장/재승인 질문은 필요 없다. 새로운 작업 범위가 아니라
사전에 정한 단일 recovery를 다 쓴 상태에서 중복 안전성을 유지하는 기술 검토 단계다.

진단 결과가 불명확하면 supported 한계를 명시하고 멈추며 또 다른 실제 키를 만들지 않는다.
P901/두 번째 전달·P010 C3·P009 미완료, 기존 두 writer/중지/개인 설치/main/tag를 유지한다.
결과/정확source/한계/hash를 동일 key로 기존 plan에 인계한다. ACK나 동일 상태 대기는 없다.
