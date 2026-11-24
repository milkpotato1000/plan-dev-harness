# P008 dev 인계 — 2026-11-24

P008 카드, 상세 P008-release-0.2.3.md, P008-readiness.md를 정확 reviewed SHA로 채택한다.
현재 P002/P007 완료·clean dev를 보존하고 다른 writer/새 중지가 없음을 재확인 후 진행한다.

실제 사용자가 이번에 main 승격·정상 push·v0.2.3 정식 발행과 회사 Claude Code 설치 안내를
명시 요청했다. 같은 승인을 다시 요구하지 않는다. README/회사 안내/CHANGELOG 작성,
격리 설치·전체 회귀·정확 후보 gate, main fast-forward 및 main만 worktree hook 설정,
태그/Release 발행, 공개 태그 재설치, dev 후행 증거 push까지 R1~R7을 실행한다.
공개 repo origin 이외 배포, marketplace 추가, 다른 프로젝트/개인 설치 갱신은 범위 밖이다.
기존 중지·설정·실패 증거를 보존한다. shared hook installer/force push/tag 이동은 금지한다.

실제 출판 결과는 기존 dev→plan 결과 위임과 공통 review key로 전달한다. plan은 실제 링크와
artifact를 검토하여 사용자에게 설치 안내를 제공한다. 단순 완료 재승인 질문은 하지 않는다.
발신 plan은 실제 SENT 기록·commit/push 후 ACK나 구현/발행 완료를 기다리지 않는다.
