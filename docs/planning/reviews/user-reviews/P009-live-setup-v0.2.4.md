# P009 설치 준비 검토 — 2026-11-24

Common key: P009-live-setup-v0.2.4. 준비 결과 조회이며 추가 사용자 판단/재승인 없음.

정확 artifact commit 4c4b5a3f2ef63deeffa425f49c2bc0161cf48d66의
docs/verification/P009/preparation.md를 읽고 SHA256
120edabc53cd864a45a73d5d765e0fb64bf034267a679085e122b00d13a3a270를 재검산했다.
같은 commit의 worker-adapters.md, 실제 사용자 지정 fixture의 AGENTS.md/P009-TEST.md와
프로젝트 로컬 설치 VERSION 0.2.4를 직접 확인했다. 실제 경로/세션 식별자는 공개하지 않는다.

준비 packet은 preview/apply, 별도 plan/dev/main worktree, KEEP와 양쪽 doctor 및 새 동작
테스트 6개 통과를 보고한다. Plan은 이번 검토에서 설치 파일/계약/hash를 확인했으며 설치나
해당 테스트를 직접 다시 실행했다고 주장하지 않는다. 전체 회귀 및 Claude live M1~M3는 아직
pending이다. 단순 설치 성공을 세션 연결/병렬 동작 성공으로 확대하지 않는다.

Fixture 규칙은 실제 사용자 지정 시험 범위와 역할을 명시하고 P901/P902를 분리한다. 실제
사람의 추가 기획 turn이 없으면 있었다고 주장하지 않아야 한다. C3의 실제 독립 실행·다음
기획 중첩 증거는 최종 별도 검토 대상이다. 원래 completion 기준을 변경하지 않는다.

사용자는 이어 앱/터미널 차이와 수동 ID 교환 없이 실행 시 역할별 자동 등록·재접속을
질문했다. 현재 source doctor는 명시적인 최신 binding 입력을 검사하는 조회 도구이며,
시작 hook/등록·갱신 구현이 완료됐다는 근거는 없다. Claude native 발견·전달과 Codex
터미널 queue의 실제 기능은 별개이며 현재 Codex adapter 문서는 desktop tools 중심이다.
자동 등록·재접속 및 Codex terminal adapter는 추가 구체화할 요구로 남긴다. 이번 준비 검토가
그 구현 완료나 미검증 기능의 자동 연결 보장을 승인하는 것은 아니다. P009 진행 작업을
소급 변경하거나 배포/개인 설정 변경 범위를 넓히지 않는다.

기존 승인 범위에서 독립 fixture dev를 구성/재사용하고 실제 전달·병렬 검증을 계속할 수 있다.
실제 UI/login/필수 human action이 생길 때만 구체적 단일 질문을 parent plan으로 전달한다.
현재 사용자에게 터미널 재개설이나 ID 복사를 요구할 필요는 없다. 단순 ACK 전송 없음.

## 후속 실제 플랫폼 전제 조건 — fixture dev workspace trust

위 준비 시점 이후 공식 Claude --bg가 exit 1 / Workspace not trusted로 거절됐다.
새 worker 미시작, native send 미시도, 기존 plan/권한 변경 없음. 실제 artifact commit
d6ff8bef29570a9849bafc7805bce81348b72d60의 live-blocker.json 및 검토 packet을 읽고
SHA256 a49faf308c6fc81234876a50ed62c351177bf24c6f1632555cfadf831f00efb6를 재검산했다.
실제 로컬 P009-DEV-START.md의 bounded 역할·동일 fixture 인계 지시도 확인했다.

동일 preparation key의 질문 범위를 fixture dev 폴더에 대한 Claude 최초 trust 확인으로
한정한다. 상태: HUMAN_ACTION_PENDING. 이는 P009 실행 승인/채택 재요청이 아니며 새로운
업무 OPEN 결정을 만들지 않는다. 기존 plan 터미널은 유지하고 사용자에게 별도 dev 터미널에서
준비된 역할 prompt를 포함한 Claude 명령을 실행해 플랫폼 신뢰 내용을 확인하도록 한 번 안내한다.
인간의 확인을 에이전트가 대신하거나 권한 설정으로 우회하지 않는다. 별도 worker 추가 생성 금지.
C3/M1~M3은 여전히 미실행이며 독립적인 회귀·설치 검증은 계속 가능하다. 응답이 오면 이 범위에
기록하고 같은 질문을 dev에서 반복하지 않는다. 실제 확인 전에 resolved/완료로 기록하지 않는다.

## 2026-11-25 실제 사용자 실행 보고 및 세션 확인

실제 사용자가 준비된 dev 실행 안내에 “dev 실행했어”라고 답했다. 공식 host의
`claude agents --json`을 읽어 기존 fixture root의 interactive/idle plan과 별도 fixture dev
worktree의 interactive/busy dev가 함께 존재함을 확인했다. 서로 다른 process와 cwd이며
정확한 private identity는 현재 로컬 인계에만 전달한다. 같은 질문을 다시 요구하지 않는다.

이 기록은 앞선 HUMAN_ACTION_PENDING을 DEV_START_OBSERVED로 갱신한다. 실제 trust dialog의
클릭을 관찰했다고 주장하지 않으며 모든 권한·native 수신이 허용됐다고 확대하지 않는다.
확인한 것은 사용자의 실행 보고와 dev 세션의 실제 가동이다. 앞선 start 실패를 역사로 보존한다.
기존 dev를 재사용하고 현재 작업을 중단하지 않는다. 새 worker 생성/재시작은 불필요하다.

P009의 기존 승인 범위에서 fresh native identity·tool/transport·현재 fixture 상태를 확인하고
C3 M1~M3 증거 수집을 계속한다. 관찰/검증 담당은 fixture plan/dev의 작업을 대신하지 않는다.
단순 두 process 존재를 실제 P901/P902 전달·적용·기획 중첩 통과로 처리하지 않는다. 새로운
구체적 platform 입력이 필요하면 같은 원장의 해당 범위로 한 번 인계한다. 기존 scoped stops/
OPEN, P009 기준, main/tag 및 개인 설치를 보존하며 이번 보고는 pause resume 지시가 아니다.
