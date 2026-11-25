# P904 준비 검토

- 검토자/역할: 기존 fixture plan(별칭 fixture-plan), 2026-11-25.
- 근거: 실제 사용자 기획 turn — 초안의 제안 기본값으로 검토·확정, 기본 JSON·P903 선행·오류 종료 코드 유지, READY 정확 커밋을 기존 dev에 전달. 이 turn은 P903 발송 직후 받았으며 그 시점에 dev STARTED는 아직 관찰되지 않았다.
- 확정 항목(P904-draft-review.md 제안 기본값):
  - D1: `--format {json,csv}`, 기본 json.
  - D2: CSV 모드는 group 행만 stdout에 쓰고, 오류는 stderr에 `line <k>: <code>`, exit 2.
  - D3: csv 모듈 기본 `\r\n` 줄 끝.
  - D4: 정수 그대로.
- 유지 확인: 기본 JSON 출력 바이트 동일, 선행 P903, exit 0/2/1 의미 불변.
- 의존성: P903. dev는 P903 완료/안전 checkpoint 커밋 뒤에만 채택·순차 실행.
- 검증 충분성: 헤더만 있는 빈 결과, 쉼표·따옴표·개행·Unicode 왕복, 결정적 순서, exit·stderr, 기본 JSON 불변, 회귀. 기대값의 CSV 인용은 plan에서 csv 모듈로 독립 확인했다(제품 코드 실행 아님).
- 위험·중지·OPEN: 없음.
- 결론: 준비 완료(READY).
