# P903 준비 검토

- 검토자/역할: 기존 fixture plan 세션(별칭 fixture-plan), 2026-11-25, 단계 A.
- 근거: 실제 사용자 단계 A 지시(이 터미널), 부모 보충 계약 전달 98e88db… / 내용 173108e…. P903/P904 번호 미사용 확인(plan·dev·main 브랜치).
- 범위 점검: 계약의 JSONL 규칙(nonblank object, group 문자열, lines 문자열 배열, 기존 함수 재사용, group별 records/lines/characters, 1-based 줄 번호+error code 후 계속, 이름순, UTF-8 파일→stdout JSON, exit 0/2/1)을 모두 반영.
- 계약 안 명확화(새 업무 의미 아님): 오류 코드 4종 이름, 공백 줄 건너뜀, 줄당 첫 위반만 기록, 추가 키 무시, 빈 문자열 group 허용, 빈 lines는 record 1·0·0, UTF-8 디코딩 실패는 exit 1, argparse 사용법 오류는 기본 exit 2.
- 의존성: P902(따라서 P901). 기존 함수 계약 불변.
- 검증 충분성: 계약이 요구한 Unicode·빈입력·빈그룹·잘못된 타입·mixed·중복·trailing newline·CLI exit/output·회귀를 기대값과 함께 지정. 기대값 산술은 plan에서 독립 확인(제품 코드 실행 아님).
- 시험 적합성: 인위적 sleep·반복 연산·benchmark 없이 실제 구현·테스트 분량을 가진다. 실제 소요 시간은 보장하지 않으며 결과는 실제 시각으로만 판정.
- 위험: 로컬 파일 읽기만, 네트워크·권한 없음. 중지·OPEN 없음.
- 결론: 준비 완료(READY). 단계 B 사용자 입력 전에는 발송·착수하지 않는다.
