# P009 실제 시험 대상 확정 — 2026-11-24

실제 사용자의 후속 지시: “harness-test 폴더에서 claude 하나 터미널로 (iterm) 띄워놨어.
하네스 설치부터 테스트까지 한번 해놔봐줘.” 이 지시는 P009의 격리 시험을 실제 사용자 지정
폴더에서 설치부터 수행하도록 승인한다. 이전의 '사용자 세션 개설 대기'를 반복해서 요구하지 않는다.

Plan이 확인한 대상은 로컬 workspace/playground 아래 harness-test이다. 조회 시 빈 non-Git
폴더이며 공개 배포 저장소가 아니다. 실제 Claude 공식 agents --json inventory에서 이 cwd의
interactive 세션 1개, idle 상태를 확인했다. 정확 경로·로컬 session alias는 비공개 실제 dev
인계에만 전달한다. 이는 실제 명령 수행/연결 성공 증거가 아니다.

Dev는 P008을 완료하고 P009 정확 채택 후 이 폴더를 우선 fixture 대상으로 사용한다.
실행 직전 파일/기존 Git/활성 writer·새 사용자 입력을 재확인하고 덮어쓰지 않는다. 프로젝트
로컬 스킬·entrypoints, plan/dev/main 작업폴더를 설치 preview 후 적용한다. bootstrap이 이미
존재하는 빈 container를 받지 않으면 harness-test 안에 명시적 fixture 하위 workspace를
사용하고 outer entrypoint로 연결한다. 변경된 경로를 실제 테스트 명령에 반영한다.

사용자가 열어 둔 첫 세션은 fixture plan으로 명시 초기화한다. 이 작업 지시에 따른 fixture
설치·역할 초기화·P901/P902 시험 실행과 같은 fixture 안의 plan↔dev 결과/결정 전달을 허용한다.
사용자의 승인 문장/판단을 대신 만들어내지 않고 이 실제 지시를 근거로 삼는다. 새 시험 dev
worker가 필요하면 동일 fixture의 한 개 독립 Claude 세션만 구성할 수 있다. 공식 CLI/호스트
기능을 사용하고 기존 fixture dev가 있으면 재사용한다. 이는 실제 제품 프로젝트에 새 worker,
Codex 채팅, 무제한 subagent 또는 daemon을 만드는 권한이 아니다.

호스트 세션 조작/전송 도구가 제공되지 않거나 필수 UI 권한·Claude 로그인이 실제 필요하면
구체적인 준비 완료 폴더·명령·최소 사용자 행동을 plan에 전달한다. 허위 전송/권한 우회는 금지.
실제 두 세션 시험을 완료할 수 없으면 C3을 미완료로 남긴다. 독립 worker 실행 중 fixture plan의
추가 기획을 확인하고 단순 shell background를 대화 병렬 성공으로 대체하지 않는다.

대상 폴더 설치는 이 요청의 명시 범위다. 개인 전역 스킬/회사 정책/다른 프로젝트는 변경하지 않는다.
원래 P009 W1~W7, 기존 paused/OPEN, P008 release 보존과 단일 writer 원칙을 유지한다.
