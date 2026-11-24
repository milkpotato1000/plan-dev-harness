# P008 정식 릴리스 결과 검토 — 2026-11-24

Common key: P008-release-v0.2.3-3ede2e81. 추가 사용자 판단 없음. 기존 main/tag/release 승인 재사용.

정확 결과 commit 9af1e5a904e7c22252348aebc5337108d5eaaf82의 report, manifest와 검토 packet을
직접 읽었다. manifest SHA256 874e4c4320d9d64d8ce1f849aaa4eb49b24b00b6eee3c8a2efd2f908ed564015와
그 안의 11개 artifact hash를 실제 git blob에서 재검산해 일치함을 확인했다.

GitHub connector의 실제 GET으로 Release v0.2.3의 draft=false/prerelease=false,
published_at 2026-11-24T08:14:13Z 및 main/ref, annotated tag object의 peeled SHA를 확인했다.
main/tag는 모두 3ede2e81f53be8252b585a57064f225fb711ccea이다.
Release: https://github.com/milkpotato1000/plan-dev-harness/releases/tag/v0.2.3
설치 안내: https://github.com/milkpotato1000/plan-dev-harness/blob/v0.2.3/docs/claude-code-install.md

커밋된 증거는 83 tests, 정확 후보 guard, 인증 없는 공개 태그 fresh clone 설치 preview/apply,
40파일 payload/독립 CLI/KEEP/충돌 byte보존 통과를 제시한다. 이번 plan 검토는 hash·원격 발행
상태를 재확인했으며 전체 회귀를 다시 실행했다고 주장하지 않는다. 회사 계정/조직정책·실제
모델 대화 및 Linux/WSL/native Windows 미검증은 유지한다.

발행 결과는 승인 범위를 충족한다. 최종 SENT/C5 실행 표시는 후행 dev commit에서 유지하며
그 증거를 넣기 위해 main/tag를 이동하지 않는다. 원래 P002 등 역사/실패를 유지한다.
외부 container 진입점의 main 설명은 현재 정식 0.2.3과 main worktree-local hooks에 맞게
plan이 정정한다. 향후 release 승인이나 shared installer 허용으로 확대하지 않는다.
P009는 별도 0.2.4 후속 작업이며 이 릴리스에 섞지 않는다. 단순 ACK 전송/중복 질문 없음.
