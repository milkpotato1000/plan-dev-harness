# P011 구현 인계 — 2026-11-28

Common key: `P011-official-claude-relay`, linked `P010-session-registration-reconnect`.
실제 사용자 요청은 공식 Codex→Claude 전달을 찾아 하네스에 연결하고 반복 터미널 입력을
없애는 것이다. 정확 reviewed commit을 안전한 경계에서 내부 채택한 뒤 구현·검증을 진행한다.

계약: `docs/planning/plans/P011.md`, `docs/planning/P011-official-claude-relay.md`,
`docs/planning/reviews/P011-readiness.md`. P010의 cross-host 제외 범위를 이번 승인으로 확장한다.
P009/P010 완료는 선행이 아니며 기존 실패/중지/작업을 보존한다. Source/설치형0.2.6,
main/release/개인 설치 변경 없음. Plan은 제품을 구현하거나 dev 완료를 기다리지 않는다.

공식 `claude -p` relay + ListAgents/SendMessage 경로를 실제로 검증해 기존 registration/
exact handoff와 연결한다. 단순 `--allowedTools`는 도구 제한이 아니며 --tools/MCP/상속
설정과 실제 native trace를 확인한다. 필요한 최소 SDK callback 의존성은 이유와 버전을
기록해 사용할 수 있다. Role writer 추가, 기존 session resume, 설정/권한 우회는 금지다.

기존 idle lifecycle stale 문제는 fresh 공식 host proof를 별도 전송 근거로 구현하되 과거
timestamp를 덮어쓰지 않는다. 단위/격리 검증 후 현재 기존 P010 plan에 승인된 runbook 계속
메시지를 실제 전달한다. 정확 receiver는 기존 인간 제공 ID와 live inventory로 다시 확인한다.
재입력 질문 반복 없이 첫 실제 수신/기존 역할 실행과 두 번째 전달을 검증한다.
불명/거부/hold는 성공으로 꾸미지 않는다. 구체적 새 플랫폼 입력만 같은 key로 plan에 인계한다.

현재 iTerm UI 접근은 컴퓨터 제어 도구가 차단했다. 이를 우회하거나 차단된 UI 행동을
Claude에게 요청하지 않는다. 이번 범위는 공식 messaging 기능 구현/검증이다.
최종 증거/hash와 실제 지원 한계를 기존 dev→plan 위임으로 보내고 ACK 대기 루프를 만들지 않는다.
