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
