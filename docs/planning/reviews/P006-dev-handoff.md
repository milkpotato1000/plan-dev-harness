# P006 dev 인계 — 2026-11-05

요청: P006의 비동기 plan/dev 병렬 규칙을 구현하고 설치형·활성 Codex 사본에 반영한다.
카드와 상세 계약·readiness 및 이 문서를 포함한 정확한 plan SHA는 WORK_READY event와
실제 전달 메시지에 기록한다. 수신자는 검증된 기존 same-project dev 채팅이다.

Plan 완료: 목적/범위/N1~N10·설치/보존 경계 검토, 실제 plan 소유 지침 반영, READY commit.
Dev 미완료: source0.2.2·패키지/생성 진입점 구현, 설치형/활성사본 전환, 회귀/증거·정상 push.

다음: 기존 작업·실패를 보존해 exact integration/adoption/commit, guard/큐 후 P006 범위 실행.
다른 P 실행 중이면 새 메시지를 현재 P 취소 지시로 읽지 말고 안전한 경계 후 처리한다.
P002 fixture와 다른 중지를 resume/resolve하지 않는다. main/tag/release·타 프로젝트 일괄
업그레이드·DB/외부서비스·새 채팅/역방향 메시지는 제외한다. 상세 계약 E/F를 준수한다.

이 인계는 송신 성공 시 SENT만 기록해 plan 턴을 종료한다. ACK는 뒤에 실제 관찰됐을 때만
기록하며 수신·채택·구현 완료는 아직 주장하지 않는다. Dev는 자기 채팅과 커밋된 증거에
결과를 남기고 인간 권한 없는 역방향/연쇄 메시지를 보내지 않는다. Plan은 이번 턴에 반복
read/wait·완료 감시를 하지 않으며, 사용자와 다음 기획을 계속할 수 있다.
