# P009 source 결과 검토 — 2026-11-24

Common key: P009-source-v0.2.4-4c4b5a3. 연결된 사람 입력 key: P009-live-setup-v0.2.4.
추가 사용자 승인/채택/동일 trust 질문 없음. P009 전체 완료 승인은 아님.

정확 결과 commit 5bfc20acce29b2de0ddcd7481ea7ab6a29b7d0c1의 report, manifest, 검토 packet과
suite-result를 직접 읽었다. Manifest SHA256
4d56fb2a5dde36f5ee4be26a2b4d27cbe79442da81308fee87738fa24a0726b7 및 그 안의 12개
artifact hash를 git blob에서 재검산해 일치함을 확인했다. source commit은
4c4b5a3f2ef63deeffa425f49c2bc0161cf48d66, 버전 0.2.4, 미발행이다.

증거가 뒷받침하는 범위: 독립 worker 규칙·명시 binding을 검사하는 readonly doctor·native
Claude/기존 Codex desktop adapter 절차, 새 행동 테스트를 포함한 89 tests PASS, 격리 설치
44파일/preview/apply/KEEP/충돌 보존 및 0.2.3→0.2.4 upgrade 검증. 이번 plan 검토가 회귀를
다시 실행한 것은 아니다. C4는 실제 Git과 시뮬레이션 정책 검증이며 live 모델 준수를 증명하지 않는다.

현재 실제 Claude --bg start는 새 fixture dev 폴더 trust 확인으로 막혀 worker 미시작,
native send 및 M1~M3 미실행이다. C3은 미완료로 유지한다. 사용자가 '터미널 하나 확인'을
요청한 뒤 공식 host inventory를 다시 읽었을 때도 기존 fixture root의 idle plan 한 개만
관찰됐다. 그 발언을 trust 완료나 dev 시작으로 해석하지 않는다. 원래 trust 질문 범위는
이미 plan에서 안내했으므로 반복하지 않는다. 실제 응답/worker 관찰 후 안전하게 계속한다.

현재 구현은 세션 시작 시 자동 등록·재연결 또는 모든 Codex CLI 환경의 자동 pair를 보장하지
않는다. 해당 사용자 제안은 준비 검토에 남긴 별도 구체화 대상이며 source 완료로 혼동하지 않는다.
원래 iTerm 사건의 원인은 사건 로그 미확인으로 확정하지 않는다. P008 main/tag, 개인 설치,
기존 역사 증거의 보존 결과를 유지한다. 0.2.4 main 승격/릴리스 권한을 추가하지 않는다.
