# P004 준비 검토 — 2026-11-04

판정: READY. 사용자 새 세션/문서 반영 문제의 재현·분석·플러그인 업데이트 지시를
현재 plan이 검토했다. 별도 기능 요청을 발명하지 않고 현재 요청을 P004로 등록한다.

- before 실제 임시 bootstrap 검사에서 P카드 없는 plan 구현/README 커밋 허용,
  empty queue, unchanged dev를 확인했다. 원본은 P004-reproduction.json에 보존.
- 원인 가설/관찰 사실/기계적 한계를 상세 계약에서 구분했다. 실제 사고 세션·프로젝트는
  지정되지 않았으므로 해당 사건의 단일 원인을 확정하지 않는다.
- 명시 역할과 무역할 cold-start, 계획-only 예외, 문서 목적별 소유권, 원격 목표 및
  완료 경계·중지·권한·writer 제약을 N1~N10 기대값으로 확정했다.
- plan 소유 installed AGENTS.md, docs/process/agent-workflow.md·work-queue.md를
  먼저 반영했다. manifest는 관리 파일 hash만 재산출하며 목록·옵션·runtime 불변이다.
- dev 구현 범위 source/assets/references/tests/README/VERSION 및 승인된 로드 사본
  전환을 확정했다. 새 강제 guard·새 스키마·설치 강제 overwrite는 제외한다.
- P002 fixture 범위의 중지는 다른 배포 P004 작업에 대한 중지가 아니다. 해당 fixture
  쓰기/재개 없이 진행한다. 기존 dev의 로그와 P003 완료를 보존한다.
- 기존 프로젝트 직접 일괄 적용·main 승격·태그 발행은 포함하지 않는다. 실제 loaded
  사본 업데이트는 이번 사용자 플러그인 업데이트 요청의 범위로 수행하되 백업과
  확장 보존·활성 한계 보고가 필요하다. 권한 차단이 있으면 성공으로 표시하지 않는다.
- dev는 이 계약·카드·review·installed 지침이 포함된 정확한 전체 plan SHA를 통합하고
  docs/planning/reviews/P004-readiness.md로 adopt/commit한 뒤 구현·검증한다.
- 전달은 기존 프로젝트 인간 위임에 따라 확인된 기존 dev 채팅에 직접 요청하고
  실제 SENT/ACK/채택/완료 증거를 분리해 남긴다.
