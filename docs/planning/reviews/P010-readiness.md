# P010 준비 검토 — 2026-11-26

판정: READY. 실제 사용자가 P010 기획·기존 dev 전달·설치형 반영을 요청했다.
프로젝트별 역할 설정 후 공식 시작 이벤트로 실제 세션을 등록하고 재연결하는 범위다.
설치나 등록 자체가 작업 실행/중지 해제/새 worker 권한이 되지 않도록 계약을 분리했다.

사전 읽기에서 plan HEAD는 `47654c67f2f1a920f8618979da2621bcc861a6df`,
dev HEAD는 `963536ead56f205e16a262748c85460eb5d86902`이며 양쪽 clean이었다.
Dev source는 0.2.4이고 큐의 active pauses/OPEN decisions는 없었다. 이는 미래 중지나
역사 기록을 지우는 권한이 아니며 dev는 적용 직전에 다시 확인해야 한다.

P009는 C3 미충족으로 4/5다. 검토된 source 0.2.4와 실제 busy 수신/순차 적용 증거는
P010의 기술 기준으로 쓸 수 있다. P009 카드의 전체 완료를 의존성으로 걸면 별개 기능이
엄격한 과거 시험에 묶이므로 완료된 P008을 선행으로 두었다. 기존 P009의 조건/상태/실패를
바꾸거나 이 의존성 선택으로 P009 완료를 선언하지 않는다.

공식 hook/peer/queue 문서와 로컬 Claude 2.1.332 / Codex 0.160.1 help를 확인했다.
Codex 최신 문서와 설치 CLI 옵션 차이, Claude native inventory의 cwd 한계, 앱과 CLI의
transport 차이를 포함했다. 자동 등록과 실제 수신/실행은 별도 검증한다. Cross-host bridge나
권한 우회는 범위 밖이다. 현재 실제 P010 live 검증을 수행했다는 주장은 하지 않는다.

W1~W7과 C1~C5는 역할 충돌/재접속 경합·공식 host lifecycle·설정 merge·실제 live·회귀를
구분한다. 설치형 다음 source 버전은 0.2.5, 공개 main/tag는 0.2.3 유지다. 개인 전역 설치,
기존 프로젝트와 P009 fixture를 변경하지 않고 격리 target에서 검증한다.

기존 독립 dev writer가 정확 인계 SHA를 안전한 경계에서 내부 적용하고 구현·검증·정상
push한다. 사람의 채택 재입력은 없다. scoped stop/OPEN이 생겼으면 보존하고 해당 범위
실행을 보류한다. 필요한 판단은 같은 key로 plan에 전달한다. Plan은 실제 발송 후 SENT를
기록하고 종료하며 ACK/완료 대기나 경쟁 worker 생성을 하지 않는다.
