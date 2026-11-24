# P009 dev 인계 — 2026-11-24

P008 정식 0.2.3 배포를 먼저 마치고 안전한 경계에서 이 정확 reviewed SHA를 적용한다.
현재 candidate/작업/실패를 취소하지 않는다. P009는 별도 source/설치형 0.2.4 작업이며
main/tag/release 추가 권한이 없다. 독립 dev worker와 plan 실행 승인 체계를 구현한다.

사용자는 iTerm plan/dev 두 터미널을 사용했다고 답했고, 테스트 폴더에서 Claude 두 세션을
열겠다고 제안했다. 현재 공개 source의 Claude file-only 안내와 순차 fallback 조건을 보완하고
실제 ListAgents/SendMessage capability·recipient·inbound 상태를 확인하는 adapter/진단을
구현한다. 같은 plan 세션의 구현, 사용자 dev 채택 재입력, 완료 대기 loop를 금지한다.

상세 W1~W7을 따른다. 기존 역할·위임·중지/OPEN·single writer를 보존한다. 실험 teams,
서브에이전트 자동 생성, 회사 설정/권한 변경, socket 우회는 범위 밖이다. 사용자 사건의 실제
로그가 없으므로 root cause 확정으로 쓰지 않는다. 공식 문서·로컬 help와 live 결과를 구별한다.

격리 fixture와 실제 두 터미널 시작 명령/짧은 첫 입력을 먼저 준비하고, 공통 review key와
준비 artifact/hash로 기존 plan에 전달한다. 사용자가 세션을 연 후 실제 병렬 검증 C3을 마친다.
테스트 통과 전 완료 처리 금지. Dev는 사람에게 동일 확인을 따로 묻지 않는다.
정확 내부 적용부터 구현/검증/정상 dev push까지 자동 진행하며 필요 결정은 plan에 인계한다.
