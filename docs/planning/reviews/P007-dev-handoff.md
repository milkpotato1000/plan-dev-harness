# P007 후속 dev 인계 — 2026-11-05

카드 P007, 상세 계약 P007-plan-review-gateway.md와 readiness를 따른다. 정확 commit SHA는
WORK_READY event와 실제 메시지에 제공한다. P006을 먼저 완료/검증/commit한 안전한 경계에서
P007을 정확 채택한다. 진행 중인 작업·개인 사본 전환·실패를 취소하거나 버리지 않는다.

목표: 사용자 확인/결정은 plan 한 곳. Dev는 결과/검증·artifact version/hash·공통 request key와
필요한 판단을 plan에 전달. Plan은 실제 파일/시각 결과를 검토하고 기존 답변을 재사용하며 실제
필요한 사용자 판단만 한 번 질문. Plan 결정은 commit/정확 채택 후 dev에 반영한다.
이 프로젝트의 좁은 reverse-result/decision 위임은 actual user 지시와 별도 위임 문서에 있다.
기존 P006의 ‘그 지시 자체는 역방향 권한을 생성하지 않음’은 유지하며 새 인간 지시를 근거로 한다.

Source/설치형0.2.3·로드된 Codex 사본 안전 갱신·M1~M12·전체 회귀/guard/큐·비민감 증거·정상
origin/dev push를 완료한다. 기존 제품 사례/경로는 공개 배포 Git에 넣지 않는다. 다른 제품 프로젝트
일괄 적용·제품 승인·main/release/DB/외부서비스·새 채팅·P002 재개 제외. 질문 여부가 아닌 실제
실패/판단을 근거로 필요한 handoff를 만들고 ACK 회신/결과 질문을 중복하지 않는다.
Plan 발신자는 SENT 뒤 이번 턴을 종료하고 이후 자연스러운 조회에서만 상태를 확인한다.
