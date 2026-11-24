# P009 독립 dev worker 계약 — 2026-11-24

## 요구와 조사 근거

실제 사용자는 plan에서 결정 후 다음 기획, dev는 전달받아 구현하는 병렬 구성을 요청했다.
사용자는 iTerm의 plan/dev 두 터미널을 이미 사용했는데 plan 터미널이 두 역할을 수행했다고
보고했다. 대상 프로젝트/그때의 세션 로그는 확인하지 않았으므로 원인을 확정하지 않는다.
이후 사용자는 필요하면 테스트 폴더에서 Claude Code 터미널 두 개를 열겠다고 제안했다.
Dev가 구체적 격리 환경·시작 명령을 준비하고 plan이 이를 안내한다. 지금 기존 제품 프로젝트의
터미널에 명령을 주입하거나 설정을 바꾸는 승인은 추정하지 않는다.

조사한 설계상 빈틈: 현재 source의 references/role-chats.md는 Claude를 별도 사용자 시작 세션과
Git 파일 인계로 안내하며, 실제 native peer 목록/전달 검사 절차가 없다. 공유 규칙에는 권한이
있는 한 세션의 양쪽 역할 순차 수행 예외가 있다. P006의 SENT 후 복귀 규칙은 있으나 호스트
연결이 없을 때의 상태와 실제 독립 worker를 확인하는 설치 안내·진단이 부족하다.
현재 plan/dev Codex 채팅은 별개이고 P008 dev가 active이다. 이번 기획은 P008과 병렬 진행한다.

로컬 Claude --version은 2.1.318, help는 agents --json, --bg와 --name/--resume 등을 제공한다.
읽기 전용 agents --json은 []였고 sandbox의 ps는 거절됐다. 이를 사용자 세션 부재나 원인으로
단정하지 않는다. 버전/help 확인은 실제 세션의 messaging/provider/inbound 기능 확인이 아니다.

공식 참고(2026-11-24 조회):
- https://code.claude.com/docs/en/cross-session-messaging
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/agent-teams

메시징 문서는 ListAgents/SendMessage, active 세션의 tool 경계 수신 및 idle 세션 turn 시작,
inbound accept/hold/refuse와 권한 제약을 설명한다. 서브에이전트는 같은 세션 내부 위임이며,
별도 세션을 이미 사용하는 경우 서브에이전트나 실험적 teams가 필수는 아니다. 실제 설치 버전의
도구·설정·회사 정책을 확인한다. 공식 문서만으로 이 환경의 전송 성공을 주장하지 않는다.

## W1 — 역할과 실행 승인

기본은 독립 plan + 독립 dev이다. 명시 plan 세션은 제품 코드/README/설치 안내를 구현하지 않고
dev worktree를 쓰거나 채택 명령을 대신 실행하지 않는다. 사용자 실행 승인/위임을 plan의 기존
P 승인 근거·준비 검토에 기록하고 READY와 정확 커밋으로 확정한다. 범위 안의 준비·인계에
불필요한 승인 질문을 추가하지 않는다. 중요한 사용자 판단은 plan에서 한 번 처리한다.

사용자 용어는 'plan 실행 승인', 'dev 수신·적용', '구현/검증'으로 구분한다. 기존 adopt CLI와
파일 포맷은 호환 유지하며 내부 exact-SHA 적용 근거로 사용한다. Dev는 기존 실제 승인/위임과
범위를 확인해 직접 적용하고 사용자에게 '채택해줘' 입력을 요구하지 않는다. 전달 텍스트 자체를
새 권한으로 해석하지 않는다. 승인되지 않은 최신 plan tip/초안은 실행하지 않는다.

병렬 요청에서 한 세션이 양쪽을 수행하는 fallback은 금지한다. 독립 worker/전달 도구가 없으면
인계 대기와 정확한 누락 조건을 보고하고 plan으로 복귀한다. 순차 모드는 사용자가 그 제약을
인지하고 별도 명시 선택한 경우만 가능하며 병렬 실행이라고 부르지 않는다.

## W2 — 독립 worker 연결과 전달

기존 세션을 우선 재사용한다. 프로젝트 Git common directory, 실제 plan/dev worktree·branch,
확정 역할, source/destination의 별개 host session identity, 단일 writer, 실제 인간 전달·실행
위임, 중지/OPEN 및 현재 P를 확인한다. 이름만 같거나 두 터미널 창만 있다는 것은 충분하지 않다.
호스트 식별자는 로컬 evidence에만 두고 공개 증거는 alias와 비민감 결과를 사용한다.

Codex는 실제 list/read/send tools로 현재 adapter를 유지한다. Claude는 실제 ListAgents와
SendMessage가 제공되고 기존 dev 수신자가 확인될 때 이를 사용한다. /list-agents, /status 등
공식 진단·수동 확인 경로를 제공하고 최소 버전/provider/inbound 차이를 문서화한다. CLI의
agents --json/help 존재만으로 실제 native tool 접근이 있다고 단정하지 않는다.
내부 socket 프로토콜을 역공학하거나 iTerm 키 입력·우회 셸로 전달하지 않는다. 플랫폼/회사
권한과 peer-message configuration 제한을 존중한다. 설정/승인 차단을 다른 세션으로 우회하지
않는다. 이 작업만으로 crossSessionInbound를 전역 accept로 바꾸지 않는다.

기존 PENDING/SENT/ACK 이벤트 포맷을 보존한다. 전송 호출 성공·보류·실제 수신·정확 적용·실행은
다른 상태다. 호스트가 held/unknown이면 실제 전달로 주장하지 않고 연계 evidence에 구분한다.
각 payload는 exact SHA, P와 승인 근거, 완료 기준, 안전 다음 행동, 중지 경계를 포함한다.
Plan은 실제 전송 기록·commit/push 뒤 끝내고 ACK/채택/완료를 기다리는 loop를 하지 않는다.
Dev는 busy 작업을 취소하지 않고 안전한 완료/checkpoint 경계에서 다음 exact SHA를 적용하고
준비·우선순위·선행에 따라 순차 실행한다. 수신 메시지는 종료된 worker를 무조건 깨우는 서비스가 아니다.
다음 작업이 없으면 대기한다. 상주 daemon, 새 채팅/worker 자동 증식, experimental teams 강제 활성화는 제외한다.

## W3 — 반복 가능한 진단과 설치형

0.2.4의 source SKILL, assets/instructions, workspace/role-chat templates, references,
README/Claude 설치 안내/CHANGELOG를 함께 정리한다. 정상 읽기 전용 bootstrap과 실제 승인된
work-dispatch 시작을 구분한다. 초기화 템플릿의 '대기'를 승인된 후속 실행 거부로 확대하지 않는다.

표준 라이브러리 기반 읽기 전용 preflight/doctor를 추가한다(명칭은 dev 선택). repo/worktree/branch,
역할·동일 writer 경고, 실제 명시적으로 제공한 worker binding, 버전/capability evidence,
미연결/불명/보류·중지 상태를 기계 판독 가능하게 출력한다. 실제 host 정보를 얻지 못하면 unknown;
추정 연결 성공 금지. queue 조회에 네트워크·전송·실행을 섞지 않는다. credentials/session transcripts
전체 수집 금지. live-check와 입력 fixture의 시뮬레이션을 명확히 구별한다.
고정 개발자 경로/터미널 ID를 패키지에 넣지 않는다. 새 프로젝트 생성·기존 사본의 preview/충돌
보존·설치 패키지에서 같은 절차가 보이는지 검증한다. 설치만으로 다른 프로젝트의 위임이 생기지 않는다.

## W4 — 실제 두 터미널 검증 준비 및 역할

P008 완료 후 dev가 임시 격리 폴더를 preview/apply로 준비한다. 독립 main/plan/dev worktree,
시험 전용 fixture P901/P902, 정확 승인 근거, 무해한 텍스트 산출물과 bounded 검증을 사용한다.
원래 P002 fixture/실패/중지 역사나 실제 제품 저장소를 재사용하지 않는다. 현재 plan은 fixture
기획 계약 준비를 승인하며 dev는 시험 장치 설치를 맡는다. 실제 fixture plan 변경은 fixture plan
세션만, 구현은 fixture dev 세션만 수행한다. writer 중복과 종료 시 cleanup 소유를 기록한다.

Dev는 'fixture 폴더 + 검증된 두 터미널 시작 명령 + 역할별 짧은 첫 입력 + 사용자에게 필요한
검증 행동'을 커밋된 준비 packet으로 먼저 plan에 보낸다. 시작 명령은 각각 올바른 worktree와
기존 설치형/agent entrypoint를 읽고 기대 역할을 명시한다. 새 Claude 로그인/회사 정책은 자동
변경하지 않는다. 사용자가 두 터미널을 연 뒤 실제 host에서 role/recipient를 확인한다.
현재 사용자의 시험 제안은 아직 실행/전송 성공 증거가 아니다. 불가능한 경우 정확 blocker를
기록하고 C3은 미완료로 남긴다. 자동 unit tests로 실제 Claude 통과를 대체하지 않는다.

## W5 — 필수 시나리오

- M1: plan에서 P901 실행 승인 → 같은 프로젝트 별도 dev에 실제 전달. 사람의 dev 채택 입력 없음.
- M2: dev P901 구현·검증 구간에 plan 턴이 끝나고 사용자와 P902 기획을 진행한 실제 시간/역할
  증거. 단순 background shell 테스트만으로 대화 병렬성을 통과시키지 않는다.
- M3: busy dev에 P902 전달 → P901 보존 → 안전 경계 후 P902 정확 적용·실행, plan 구현 없음.
- M4: 같은 이벤트 재전송/세션 재접속 시 중복 구현·질문 없음. unknown send는 무조건 재시도 금지.
- M5: 동일 세션/같은 worktree/잘못된 프로젝트·모호한 peer/도구 부재/hold/refuse는 시작 금지 또는
  명시 대기, plan이 대신 구현하지 않음. 새 채팅/실험 기능을 자동 생성하지 않음.
- M6: fixture pause/OPEN에서 독립 작업 선택·결정 처리·재개 경계 보존. pause state 회귀는 격리
  fixture로 검증하며 실제 사용자 중지/재개를 요구하는 별도 역사 계약을 이 시험에 복제하지 않음.
- M7: 결과/새 결정은 plan 공통 key로 전달, dev 중복 사용자 질문 없음. bootstrap만이면 여전히
  read-only; 실제 승인된 후속 dispatch와 구별. 권한/회사 정책 거부를 우회하지 않음.

## W6 — 변경 경계 및 검증

source/설치 패키지 0.2.4, 새 진단 도구/관련 meaningful tests, generated instructions를 구현한다.
이 repo의 protected AGENTS/workflow는 plan의 이번 확정 규칙을 정확 채택한다. 추가 protected
runtime/schema 변경이 꼭 필요하면 구체적 proposal을 plan에 인계하고 무제한 수정하지 않는다.
전체 unittest 및 guard/queue, isolated installation 검증을 수행한다. 현재 개인 ~/.codex 또는
~/.claude 사본과 다른 프로젝트 일괄 변경은 제외하고 적용 대상 차이를 결과에 명시한다.
main/tag/release는 P008의 0.2.3 상태를 보존한다. 0.2.4 공개 main 승격/릴리스는 이 계약에 없다.

## W7 — 증거와 완료 인계

docs/verification/P009/에 실제/시뮬레이션/미검증을 구별해 실패와 결과를 커밋한다. 세션 ID·계정
비밀·회사 내용은 공개 증거에 넣지 않는다. Claude C3이 필요한 사용자 세션 개설 준비 요청은
plan 단일 창구로 보내며, 이미 묻고 답한 동일 질문을 dev에서 반복하지 않는다.
P008을 끝낸 뒤 P009를 진행하고 중간 안전 경계·다음 작업이 있으면 함께 보고한다. Plan은
인계 완료 뒤 기다리지 않는다. 완료 주장에는 실제 독립 worker 증거와 source/설치형 버전,
남은 현장 적용 범위를 포함한다.
