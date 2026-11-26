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
