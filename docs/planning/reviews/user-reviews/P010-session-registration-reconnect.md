# P010 소스 결과·실제 시작 준비 검토 — 2026-11-26

Common key: `P010-session-registration-reconnect`. Artifact version: unreleased 0.2.5.
Source `e044e3e7f11ef48d4f9cc4fa41cad7ac00d8e1c8`, 결과
`d12e20ec2cc83ddd9ba3631c1038cb63a3ef6dc0`의 report/runbook/검토 packet을 읽었다.
Manifest SHA256 `593c8fa7bb0bdc55c5e9f468c407c608635928e14c4923dee19256b02eab0676`와
16개 artifact hash를 committed blob에서 독립 재검산하여 모두 일치함을 확인했다.

105-test PASS 로그와 설치/업그레이드 증거를 검토했다. 이 검토에서 전체 테스트를 다시
실행한 것은 아니다. C1/C2/C4 자동 검증과 C5 실제 결과 인계가 기록됐고 C3 실제
Claude/Codex 두 세션 시작·재연결·전달은 NOTRUN이다. P010은 4/5이며 전체 완료가 아니다.
모의 hook stdin 또는 queue 접수를 실제 두 세션 실행 증거로 대체하지 않는다.

실제 준비된 Claude/Codex 각 plan/dev의 clean 상태, 네 HEAD, 로컬 hook hash와 private
역할 설정 hash를 live-preparation.json과 교차 확인했다. 두 runbook SHA256는
`5ce7ba84246b04ea7aff42c9832a0fb3f57723e477d6f4770b6fe8cb7111fbfb`로 일치한다.
첫 검산에서는 Claude 파일을 settings.json으로 가정해 FileNotFoundError가 났으나 실제
installer가 쓰는 settings.local.json을 확인한 뒤 재검산해 통과했다. 이는 검토 스크립트의
경로 가정 오류이며 제품 실패/수정 또는 실제 hook 실행 성공을 뜻하지 않는다.

공통 key의 필요한 사람 행동은 준비된 격리 폴더의 실제 CLI 시작과 표시되는 프로젝트/hook
검토다. 일반 실행 재승인, dev 채택 재입력이나 세션 ID 복사를 요구하지 않는다. 먼저 Claude
두 역할 터미널을 안내하고 실제 시작 응답 후 등록/발견/정확 전달을 확인한다. Codex 단계는
그 다음 진행하며 같은 사람 행동을 반복 요청하지 않는다. 현재 수신한 사용자 시작 응답은 없다.
실제 경로/명령은 로컬 사용자 안내에만 두고 공개 Git에는 기록하지 않는다.

이 단계는 P010 W5/W6의 실제 host 시험을 위한 것으로 새 실행 범위 승인이 아니다.
runbook의 제한된 marker 두 번과 정상 재접속만 허용한다. 새 사용자 소유 채팅·경쟁 writer,
trust 대리 승인·강제 종료·P009 재시험은 하지 않는다. 플랫폼 도구 부재는 pending으로 남긴다.
P009 4/5와 역사 실패, 기존 fixture/작업/중지, 개인 설치와 main/tag0.2.3을 유지한다.
단순 검토 ACK를 발송하거나 완료 대기 loop를 만들지 않는다.

## 실제 사용자 시작 응답과 등록 확인 — 2026-11-28

같은 key의 실제 인간 응답: “둘 다 열고 입력했어. 자동 등록됐는지 확인하고 다음 검증 진행해줘.”
기존 준비된 Claude 두 역할에 한정된 시작 응답이며 Codex 시작/재접속 완료나 중지 재개로
확대하지 않는다. 기존 runbook 범위의 다음 검증을 진행하도록 기존 dev 관찰 담당에 인계한다.

읽기 전용으로 실제 fixture plan/dev가 각각 clean이며 plan의 precondition 기록과 dev의
준비 기록이 커밋됐음을 확인했다. Plan은 먼저 시작해 dev-missing 상태를 기록하고 종료했다.
Dev의 후행 기록은 양쪽 identity_consistent이나 P901 카드/인계가 아직 없음을 보여 준다.
Fixture 역할 소유권을 유지하며 부모 plan/dev가 대신 카드나 제품 코드를 쓰지 않는다.

최초 sandbox CLI inventory는 빈 목록이라 doctor가 양쪽 host_identity_mismatch를 반환했다.
이를 실제 등록 실패로 단정하지 않고 승인된 읽기 전용 host inventory와 doctor를 재확인했다.
실제 host에는 각 정확 역할 cwd에 하나씩 idle 세션이 있고, doctor는 issues=[]와
identity_consistent를 반환했다. 등록부는 plan generation 1, dev generation 3이며 idle이다.
이는 자동 등록과 현재 host identity 일치의 증거다. 세대 번호만으로 재접속 시험 통과를
주장하지 않는다. 관찰은 2026-11-28 Asia/Seoul이며 원시 ID/개인 경로는 기록하지 않는다.

현재 부모 도구 목록에는 Claude native ListAgents/SendMessage가 없다. 기존 Codex dev
담당에게는 실제 관찰과 이 정확 시작 응답을 전달할 수 있으나, fixture Claude plan의 다음
턴을 직접 열었다고 주장하지 않는다. 기존 plan 터미널에서 상대 재확인 후 runbook 첫 P901
인계를 계속하도록 하는 최소 입력을 사용자에게 안내한다. 이는 세션 재개설/trust/채택
재승인이 아니라 현재 두 환경 사이의 전달 도구 부재로 필요한 계속 진행 입력이다.
사용자 입력이 이루어졌다는 기록은 실제 답변/증거가 오기 전 추가하지 않는다.

자동 등록과 상대의 뒤늦은 등장만으로 idle plan이 자동으로 깨어나는 것은 현재 계약의
등록 전용 lifecycle와 별개다. 이 시작 순서의 실제 사용성 한계를 결과에 보존한다.
기존 dev는 현재 두 세션을 재사용해 실제 인계/적용/정상 재접속 증거를 수집하고 C3를
미완료로 유지한다. 재시작/재연결 조작은 실제 첫 작업 완료와 소유권 확인 전 안내하지 않는다.

## 실제 시작 hook 증거 검토 — 2026-11-28

동일 key의 결과 `6d4c449c3c59e036cb954a6dc53ad7cae9928993`에서
`docs/verification/P010/claude-startup-20261128/report.md`를 읽고 manifest SHA256
`60ae6324e4f25ee6462af67672fedc08c70c28d02c3dcad414d1423064339046`와 6개 artifact
hash를 Git blob에서 재검산해 일치를 확인했다. 실제 SessionStart hook은 Asia/Seoul 기준
plan 01:44:21.436 / dev 01:44:47.199에 registered, exit 0, stdout 비어 있음으로 기록됐다.
각 소요 410ms/391ms와 후속 Stop hook 성공 증거가 있다. 합성 입력 테스트와 구분한다.

01:49:31 실제 host 관찰과 설치된 doctor 양쪽 일치는 시점 한정 증거다. 새 전송 직전에는
실제 상대/권한/freshness를 다시 확인해야 한다. 등록부 세대 1/3을 재접속 성공으로 해석하지
않는다. P010 C3는 미완료다. 첫 정확 인계/적용/완료, 정상 재접속·후속 인계, Codex 실제
두 세션 시험은 이 checkpoint에서 검증되지 않았다. 새로운 코드 변경이나 전체 회귀 재실행은 없다.

이미 사용자에게 안내한 fixture plan 계속 입력을 중복 요청하지 않는다. 이번 결과에는
새 사람 행동 요청이 없다. 실제 후속 입력/작업 근거가 도착하면 기존 writer로 계속하며,
변함없는 상태를 polling하거나 단순 ACK를 역발송하지 않는다. 기존 작업·중지·P009와
공개 main/tag0.2.3, 개인 설치 보존 범위는 그대로다.

## 계속 입력 응답과 후속 검증 인계 — 2026-11-28

실제 인간 응답: “plan 터미널에 입력했어. 확인하고 다음 검증 진행해줘.”
앞서 요청한 기존 fixture plan 계속 입력에 대한 답변으로 재사용한다. 같은 문장 재입력,
새 세션 개설, trust/채택 재확인을 요청하지 않는다. 실제 입력 접수/처리는 host 증거와 구분한다.

응답 직후 읽기 전용 fixture 확인에서 plan c5d29c7 / dev a8f39ae가 각각 clean이었다.
P901 카드/인계는 아직 보이지 않았다. 실제 host를 사용하는 doctor는 동일 plan gen1/dev gen3
idle 등록과 기존 2026-11-27T16:45:10.150534+00:00 / 16:45:46.726154+00:00를 표시하며
plan_stale_or_future 및 dev_stale_or_future로 dispatch pending을 반환했다.
이는 앞선 시점의 등록 성공을 취소하지 않지만 현재 전송 가능 판정은 아니다. 새 사람 입력이
처리됐다고 단정하거나 잘못된 터미널 입력이라고 추측하지 않는다.

기존 parent dev 관찰 담당에게 이 정확 응답과 상태를 전달하여 승인된 bounded live 검증을
계속한다. 공식 host/해당 fixture의 제한된 입력·hook·도구 결과로 접수와 처리 상태, 실제
대기 원인을 확인한다. 원시 대화/ID를 공개하지 않고 새 입력이 정말 필요한지 먼저 진단한다.
다른 작업자 생성, stale timestamp 수동 갱신, 안전 검사 우회, fixture 카드 대행, 반복 발송,
강제 종료/재시작은 하지 않는다. 새 검증 범위나 P009 재시험 권한이 아니다.
첫 작업 실제 완료 전 재접속 조작을 시작하지 않으며 C3는 기존 미완료 상태를 유지한다.
