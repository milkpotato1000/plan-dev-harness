# P904 초안 검토 자료 (단계 B 사용자 turn용)

상태: 초안. 이 문서는 사용자 검토 전 준비 자료이며 검토·확정 결과가 아니다.

| ID | 확정할 항목 | 제안 기본값 | 대안 |
|---|---|---|---|
| D1 | 옵션 이름 | `--format csv` (기본 `json`) | `--csv` 플래그 |
| D2 | CSV 모드의 record 오류 보고 | CSV에는 group 행만. 오류는 stderr에 줄마다 `line <k>: <code>`, exit 2 | 오류 무시하고 exit 0 / 오류를 CSV 별도 섹션에 |
| D3 | 줄 끝 | csv 모듈 기본 `\r\n` 유지(stdout `newline=""`) | `\n` 고정(`lineterminator="\n"`) |
| D4 | 숫자 열 형식 | 정수 그대로 | — |

변경 없는 항목: 헤더 `group,records,lines,characters`, 이름순, 빈 결과는 헤더만, 기본 JSON 불변, exit 0/2/1, P903 선행.
단계 B에서 사용자가 "제안대로"라고 하면 위 기본값으로 카드를 확정한다. 다른 지시가 있으면 그 내용을 반영한다.
