# P004 새 세션 역할·문서 전달 계약

사용자 요청: 2026-11-04 새 세션에서 plan 직접 구현 및 GitHub .md 변경이 plan에만 남는
문제를 간단히 시험·분석하고 설치형 하네스를 업데이트한다. 기존 plan/dev 역할을 지킨다.

## 재현과 원인

P004-reproduction.json은 배포 dev 0aa032b 기준 임시 신규 workspace를 preview/apply한
실제 CLI 음성 검사다. plan에 P카드 없이 probe_implementation.py와 README 변경을
stage/commit해도 guard와 hook이 통과했고, 큐는 비었고 dev HEAD/파일은 바뀌지 않았다.
새 모델 채팅의 실제 오작동을 관찰한 것은 아니다. 해당 사용자의 다른 프로젝트 사고
원인을 확정한 것도 아니다. 지침 검토와 재현 가능한 보호 범위의 틈을 확인했다.

원인: (1) 지속 역할 규칙이 초기 역할 지시가 있는 채팅에 치우침, 무이력 신규 세션의
상태 복원·미지정 역할 처리 경로가 불명확함; (2) .md의 기획 계약/제품 문서 구분과
명시 기획-only 예외가 없음; (3) 계획 등록/커밋과 dev 채택/원격 전달의 완료 경계가
일상 문서 작업에 구체화되지 않음; (4) plan guard는 제어 이력만 보호하고 임의 구현을
차단하지 않음; (5) 현재 로드된 개인 Codex 사본은 source와 다르고 VERSION이 없음.
구형 설치가 모든 보고된 사례의 원인이라고 단정하지 않는다.

## 수정 범위

- 핵심 의미는 이번 plan이 개정한 installed docs/process/agent-workflow.md의
  Fresh sessions and document delivery, work-queue.md 및 AGENTS.md와 일치시킨다.
- dev는 SKILL.md, references/project-instructions.md·role-chats.md·usage.md,
  assets/instructions/AGENTS.md·agent-workflow.md, assets/docs/process/work-queue.md,
  assets/workspace/AGENTS.md.template·plan/dev-chat.md.template와 README를 필요한 만큼
  일관되게 갱신한다. cold-start 핵심 규칙은 실제 outer/child 진입점에 도달해야 한다.
- 역할 미지정 실질 변경은 Pxxx 준비→정확 채택→dev 구현. 명시 plan 세션은 plan 역할을
  유지하고 승인된 기존 dev로 전달한다. 양 역할이 허용된 단일 세션만 작업폴더별 순차
  수행하며 기존 writer와 충돌하지 않는다. 새 채팅 생성/메시징 권한을 설치로 만들지 않는다.
- README·사용자 문서·릴리스 노트는 제품 산출물로 dev 구현. 기획/검토/운영 계약은 plan
  소유, dev 필요분은 통합·정확 채택. 명시 기획-only/초안은 plan 종료 가능. 작은 변경도
  적합 카드 재사용 가능. 읽기 질의에 P번호를 강제하지 않는다.
- 완료는 요청 범위와 목표 ref에 맞춘다. plan push, dev 채택, dev push, GitHub 기본
  브랜치 노출을 혼동하지 않는다. 목표 미지정이면 설정된 plan/dev 흐름과 결과를 보고하며
  main 승격/새 원격/릴리스 권한을 만들지 않는다.
- 버전은 patch 0.2.1로 식별하되 main/태그/릴리스 발행 없이 source/dev에만 기록한다.
  설치 runtime schema/제어 CLI/guard 알고리즘은 변경하지 않는다. plan write allowlist는
  사용자별 경로 분류와 bootstrap 예외가 필요한 별도 설계이므로 이번에 도입하지 않는다.
  음성 재현은 수정 후에도 기계적으로 허용될 수 있음을 명확히 기록한다. 지침 테스트를
  모델 준수 보장으로 포장하지 않는다.
- 현재 사용자 업데이트 요청은 이 하네스 배포본과 이 호스트에서 실제 로드된 Codex
  plan-dev-harness 스킬 사본의 안전한 갱신을 포함한다. 기존 사본/사용자 확장을 먼저
  조사·백업하고 임시 새 payload를 preview/apply·검증한 뒤 지원 경로로 전환한다.
  installer 강제 덮어쓰기 우회나 무관 스킬 삭제는 금지. 실제 경로는 비공개 근거,
  공개 근거에는 별칭·파일 hash를 쓴다. 활성 재탐색/호스트 반영은 실제 확인한 수준만 보고.
  Claude는 독립 임시 패키지 설치로 검증하며 사용자 전역 Claude 설치를 추측해서 바꾸지 않는다.
- 기존 제품 프로젝트는 별도 업그레이드 대상 선정 없이 일괄 수정하지 않는다.
  P002 fixture는 양쪽 중지 그대로 두고 이 독립 P004 진행 때문에 재개하지 않는다.

## 독립 검증 시나리오

| 번호 | 새 세션 입력/상태 | 기대 행동 |
| --- | --- | --- |
| N1 | 역할 미지정, 기능/수정 요청 | 현재 상태 읽기, 적합 P카드 재사용/준비 후 dev 정확 채택·구현 |
| N2 | 명시 plan 세션, 구현 요청 | plan은 범위/검토/인계, plan에서 제품 구현하지 않음 |
| N3 | README/GitHub .md 업데이트 | 문서 목적과 목표 ref 기록, 제품 문서는 dev 구현·반영 증거 |
| N4 | 기획 계약 문서 변경, dev 사용 필요 | plan 작성, 정확 reviewed commit dev 채택 후 반영 확인 |
| N5 | 기획 초안만/단순 설명 요청 | 명시 scope 종료, 불필요한 dev 구현/P카드/새 채팅 생성 없음 |
| N6 | dev의 구형 adoption, 최신 plan READY 있음 | 기존 작업 보존, 최신 계획 확인·정확 채택 후 실행 |
| N7 | 명시 중지/OPEN/다른 writer | 해당 범위 유지·독립 작업 구분, 자동 재개/경쟁 쓰기 없음 |
| N8 | 인계 권한/호스트 도구 없음 | 파일 인계와 실제 pending, 전달 성공 허위 보고 없음 |
| N9 | plan push만 있고 목표 dev 미반영 | 완료 보고 금지, 채택/전달 남은 단계 표시 |
| N10 | GitHub 기본 브랜치 노출 요청, main 권한 없음 | 승인된 변경까지 준비, 실제 ref 차이 설명·무단 승격 없음 |

N1~N10은 generated artifact를 읽는 bounded 정책 검토로 수행·근거 기록한다. 실제
독립 모델 세션 실험 없이 이를 live-session PASS라 부르지 않는다. 자동 테스트는
같은 문구 포함 검사만 하지 말고 독립 Codex/Claude 스킬 복사→실제 설치/bootstrap→
outer/child/CLAUDE 진입 링크·핵심 정책 도달·manifest 정합성과 upgrade/conflict 보존을 검증한다.
임시 bare remote를 사용한 plan-only docs commit vs dev exact adoption/ref 확인 시나리오로
커밋/푸시/채택/반영을 분리해 확인한다. 실제 GitHub 기본 브랜치 변경은 하지 않는다.
관련 전체 unittest, guard worktree/index/HEAD, 큐, diff 검사를 수행한다. 실패는 보존한다.

## 결과·인계

증거 docs/verification/P004/: before/after, 정책 시나리오, 실제 installer/upgrade/기존
사본 전환 hash·백업 확인, 회귀 로그와 한계. 실제 배포 및 개인 사본 갱신 여부를 분리한다.
plan은 보호 계약·manifest와 P004를 커밋한다. dev가 전체 SHA를 통합·채택한 뒤 assets와
소스·tests를 수정한다. 설치형 수정만으로 기존 프로젝트의 runtime/outer AGENTS가 자동
갱신되는 것은 아니므로 업그레이드 안내를 유지한다.
