# P011 완료 검증

2026-11-28 기준 C1–C5 모두 PASS. 공통 검토 키는 `P011-official-claude-relay`이고 최종 검토 커밋은 `c24f4f6595549bdf288b690bb5e1ca34cfbcf39e`이다.

| 조건 | 확인한 결과 | 근거 |
| --- | --- | --- |
| C1 | macOS에서 Claude Code 2.1.332와 Claude Agent SDK 0.2.189로 검증했다. 중계가 사용할 수 있는 도구는 ListAgents와 SendMessage이며, 한 번의 호출에 60초와 추정 비용 0.50 USD 상한을 적용한다. 스트리밍 호출 ID와 훅 ID, 수신자와 전체 본문을 대조한 뒤 예약한 세 필드로 입력을 구성한다. | [호출·바이트 검증](canonical-validation/report.md) |
| C2 | 최신 공식 호스트 목록과 기존 세션의 ID·세대·역할·작업 경로를 확인하고 전송 시점의 중지·OPEN 조건을 검사했다. 불명확한 시도와 소모된 복구 예약을 보존했다. 격리 시험에서 기본 수신자는 519바이트를 정확히 받았고 거부 정책 수신자는 같은 메시지 ID의 명시적 거부 통지를 반환했다. | [등록·권한·복구 검증](receipt-policy/report.md) |
| C3 | 첫 전달로 기존 plan이 작업 턴을 시작해 P901을 준비했다. 두 번째 전달로 기존 dev가 정확한 검토 SHA를 채택하고 작업을 완료했다. 사용자가 계속·채택 문장을 반복 입력할 필요가 없었다. | [전달·채택·검토](P901-source-dispatch/report.md) |
| C4 | 소스 0.2.6 설치형의 격리된 0.2.5 업그레이드, preview/apply/KEEP, 사용자 설정과 충돌 보존을 확인했다. | [설치 결과](installation.json), [최종 소스 검사](receipt-policy/checks.json) |
| C5 | 최종 소스에서 전체 회귀 113개와 설치 검사 34개가 통과했다. 가드·큐를 확인했고, 정상 origin/dev push와 기존 plan으로의 실제 결과 전달을 기록했다. | [회귀 결과](receipt-policy/checks.json), [결과 인계 기록](../../progress/handoffs/dev/0ca9969d9e8236e1bf61e80f8b689f9a86cc5ddb7fcdde5c2d8c3227add2360a.json) |

실제 fixture 설치 버전은 **0.2.5**였다. 외부에서 검증한 0.2.6 소스 `cb5b529d082c204325b0222f02c5b24a1cf5f275`로 전달만 수행했다. Dev가 채택한 SHA는 `057ecbc4ca8ae0c4cb5d64fe1247afd4b7bccdf3`이고, 완료 커밋 `10a4f5fa9407b949113d1c77f151782cdc8a98e8`의 마커는 기대값과 정확히 같은 16바이트였다. Fixture plan은 결과를 PASS로 검토하고 원래 이벤트에 외부 발송 근거와 SENT를 기록했다.

결과 회신은 수명이 짧은 relay 주소가 종료되어 한 번 ENOENT로 실패했다. Dev가 공식 목록으로 기존 plan 세션을 다시 확인해 그쪽으로 회신하면서 결과가 도착했다. 최초 로그인·신뢰·권한 설정과 조직별 수신 정책은 호스트에서 적용된다. 실제 검증은 이 Mac의 CLI/SDK 조합에 한정되며 다른 운영체제와 회사 계정 환경은 미검증이다.

0.2.6은 dev 개발 소스이며 공개 릴리스는 v0.2.3이다. P009의 미완료 항목과 P010의 재접속·후속 카드·Codex 두 세션 검증은 별도 과제로 남는다.
