# P003 설치형 규칙 반영 직접 전달 — 2026-10-29

- 인간 요청: “이 룰은 플러그인 설치형 자체에 반영 해놔줘.”
- 발송 근거: [이 프로젝트 직접 전달 위임](plan-dev-delivery-delegation.md).
- 수신자: 이전 인계에서 확인한 같은 프로젝트의 기존 dev 역할 채팅. 공개 별칭 `session-dev-harness`.
- 채택 요청 snapshot: `283ddd331eb5196bc6b2f36b0ced15ad3ce2ba74`.
- 문서: [설치형 반영 검토](P003-installable-rule.md), 그 문서 기준 커밋
  `a4658cfedbd36036079b68b043984b4ae0bde3c0`.
- event: `4e519d44993ec87c8ab8e3cf8b27fdd400ab380970112ebdfefa0e9e38386a4c`.
- origin/plan push 성공 후 실제 send_message_to_thread 호출이 성공했다.
  isError=false이며 검증된 수신 채팅을 결과로 반환했다. 실제 식별자는 공개 문서에 옮기지 않는다.
- 메시지에는 정확 SHA·새 검토 문서·패키지/설치 출력 범위·개인 설치/타 프로젝트/main 제외·
  진행 중인 변경 보존과 안전한 재채택·독립 설치 및 전체 회귀 증거 요청을 포함했다.

실제 성공 근거에 따라 SENT를 기록한다. 아래 실제 관찰 전에는 수신/구현 완료로 올리지 않는다.

## 수신·구현 관찰

대기 중. 송신 plan이 read/wait와 커밋된 dev 증거로 확인한다.
