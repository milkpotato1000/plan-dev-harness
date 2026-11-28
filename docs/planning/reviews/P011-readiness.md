# P011 준비 검토 — 2026-11-28

READY. 실제 인간이 공식 Codex→Claude 전달 연결과 반복 터미널 입력 제거를 요청했다.
기존 P010은 cross-host bridge 구현을 제외했으므로 독립 P011로 범위를 확정했다.
P008을 완료된 선행으로 두며 P009/P010의 미완료 조건과 진행 기록을 보존한다.

공식 programmatic CLI, cross-session messaging, CLI flags, SDK streaming 문서와 로컬
Claude2.1.332 help를 확인했다. 선택은 짧은 공식 CLI relay와 native ListAgents/SendMessage의
조합이다. 각 기능은 공식 지원되지만 이 환경의 조합 성공은 아직 미검증이다.
전용 claude send 명령이나 임의 live interactive 세션을 점유하는 SDK 기능을 가정하지 않는다.
이전 “공식 전달 경로 없음”은 직접 CLI 명령 부재에 대한 판단으로 한정하고, 이번 공식 기능
조합의 가능성까지 배제하는 결론으로 재사용하지 않는다.

도구 제한과 target/message 검증, native 결과 증거, fresh host 재확인, 권한/중복/unknown
처리를 계약에 포함했다. relay는 역할 writer가 아니고 요청당 한정된 전송 프로세스다.
기존 UI 접근 차단은 유지하며 UI 조작이나 실제 거부된 작업을 중계시키지 않는다.
조직/수신 deny를 우회할 설정 변경을 허용하지 않는다. 모델 호출 비용과 제한은 명시한다.

현재 plan/dev clean, dev source0.2.5, 큐에 실행 가능한 다른 승인 작업은 없음을 읽기 전용으로
확인했다. Dev는 적용 직전에 stops/OPEN/writer와 queue를 재확인한다. 다음 source/설치형은
0.2.6이며 공개 main/tag0.2.3이나 기존 개인 설치는 변경하지 않는다.

W1~W7 검토 완료. 단위/격리 검증 후 기존 P010 fixture에 제한된 실제 continue 전달을
승인한다. 원래 P010의 실제 수신/정상 재접속/Codex 검증을 가짜 성공으로 바꾸지 않는다.
같은 사용자 문장 재입력을 요청하지 않고 구현·진단 가능한 일을 먼저 한다.
기존 독립 dev에 정확 SHA를 전달하고 실제 SENT 후 plan은 다음 기획으로 복귀한다.
