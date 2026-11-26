# P010 dev 인계 — 2026-11-26

공통 key: `P010-session-registration-reconnect`.
실제 사용자 지시: 세션 자동 등록·재연결을 P010으로 기획해 dev에 넘기고 설치형에 반영,
기존 작업과 중지 상태 유지.

현재 작업의 안전한 경계에서 이 문서가 포함된 정확 reviewed plan SHA를 내부 적용한다.
`docs/planning/plans/P010.md`, `docs/planning/P010-session-registration-reconnect.md`,
`docs/planning/reviews/P010-readiness.md`가 실행 계약이다. 사람에게 채택을 다시 묻지 않는다.

P009 source 0.2.4를 기반으로 소스/설치형 0.2.5의 역할별 설정·프로젝트 로컬 등록부·공식
시작 hook·재연결·host adapter·읽기 전용 진단을 구현한다. 기존 dev 후행 커밋/증거를 보존한다.
P009 C3는 그대로 미완료이며 P010 전체 선행이 아니다. P009를 reset하거나 추가 시험을
자동 시작하지 않는다. P010 선행은 완료된 P008이다.

우선 실제 지원 hook/transport와 안전한 설정 merge를 확인하고 W1~W7을 수행한다.
세션 등록은 승인/전송/재개가 아니다. 중지/OPEN/단일 writer/현재 P와 안전한 채택 경계를
유지한다. 정상 시작·재접속에 사람이 ID를 복사하지 않도록 하되 도구 없는 전송 성공을
꾸미거나 plan 구현으로 대체하지 않는다. 기존 원장과 exact adoption을 재사용한다.

격리 P010 환경에서 단위/통합·실제 host·설치/업그레이드·회귀를 검증한다. 기존 P009 fixture와
실제 터미널, 개인 설치, 다른 프로젝트, main/tag/release는 변경하지 않는다. 실제 trust/입력이
필요할 때는 준비 artifact/hash와 정확 최소 행동을 plan에 한 번 전달한다. 구현 가능한 부분을
먼저 마치고 검증 미완료 조건은 체크하지 않는다. 결과는 기존 dev→plan 위임으로 인계한다.
