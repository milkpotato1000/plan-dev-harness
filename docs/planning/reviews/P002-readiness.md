# P002 준비 검토 — 2026-10-29

판정: 준비 완료. dev 큐 등록 대상이며 실제 수행 완료 판정은 아니다.
검토 담당: plan 역할 채팅. 별도 독립 검토자나 다른 세션이 검토했다고 주장하지 않는다.

## 승인과 기준

사용자 요청: “그럼 P002로 실제 세션 간 결정 대기·중지·인계 흐름 검증을 기획하고,
준비 검토까지 마쳐서 dev 큐에 등록해줘.”

이 요청 및 [기존 역할 위임](../../process/work-queue.md)에 따라 plan이 요구·범위·선행·
검증·완료 조건을 준비하고 READY 등록한다. 이번 작업의 산출물은 다음 세 문서다.

- [P002 작업서](../plans/P002.md)
- [실제 세션 검증 계약](../P002-session-validation.md)
- 이 준비 검토

기준 dev는 `d2b900713fb8aa7be8f1599c9ef92e5b401339dc`다. 해당 커밋의
`docs/verification-local-harness-setup.md`는 로컬 설치·정확한 채택·두 역할 채팅 초기화만
확인했다. `8bd941471db02ccb641e26835e7edcfd5a84ad28`의 P001 검증에는 실제 모델 세션과
전달 경로가 미검증으로 남아 있다. P002는 이 차이를 대상으로 하며 P001 이력을 변경하지 않는다.

## 준비 판단

| 항목 | 확인 결과 |
| --- | --- |
| 목표 | 실제 두 역할 채팅의 판단·행동과 커밋된 제어 상태를 연결; CLI 회귀의 반복과 구별 |
| 범위 | macOS/Codex 두 기존 역할 채팅, 독립 fixture 저장소, 현재 커밋된 v0.2.0 구현 |
| 역할 | plan은 fixture 계약/판단, dev는 준비·fixture 실행·결과 증거. writer당 역할 하나 |
| 선행 | P001 완료 및 설치 완료를 커밋된 근거로 확인. legacy P001을 parsed 의존에 넣지 않음 |
| 착수 | dev가 이 검토를 포함한 정확한 plan SHA를 통합·채택·커밋한 후 환경 준비부터 진행 |
| 실제 세션 | 서로 다른 두 채팅의 직접 읽기/행동 필요. 한 세션 대행·subprocess는 C1~C4 대체 불가 |
| 사용자 입력 | 중지 이후 실제 단계별 재개 발언 필요. 아직 없는 발언을 승인/생성하지 않음 |
| 전달 | 수동 사용자 전달로 수행 가능. 이번 큐 등록은 자동 메시징 권한이 아니며 실제 전달/응답이 각 전이의 근거 |
| 독립 기대값 | S0~S5에 큐 선택, blocked_by_decisions, adopted SHA, pause/OPEN 유지, 전이·중복·거부를 고정 |
| 증거 | 세션 발췌·각 단계 queue/CLI·Git SHA·원본 기록 export를 C1~C5에 연결하고 dev에 커밋 |
| 실패·복구 | 미응답/미입력/FAIL을 보존. 해당 단계 차단/재개 지점 기록. 질문·중지·인계 이력을 지우지 않음 |
| 범위 초과 | 제품/runtime/배포 변경 필요 시 intake. main·릴리스·개인 스킬·외부 업무 도구 제외 |
| 완료 | 모든 필수 실제 시나리오와 회귀·guard 및 증거 정합성 통과. 미수행을 PASS로 대체하지 않음 |

## 검토 중 보완한 경계

- 실제 배포 큐에 시험 중지를 넣으면 P002 자체와 다른 실제 업무를 막을 수 있다.
  승인된 가상 카드·결정·중지는 별도 fixture로 격리하며 세션 참여는 실제로 유지한다.
- 분류 scope와 질문의 실질 답변은 별도 커밋으로 검증하여 채택 전후를 혼동하지 않는다.
- 양쪽 중지 중에는 업무를 계속하지 않는다. 중지와 결정 해결의 독립성 검사는 사용자에게
  제어 기록 처리만 명시적으로 요청받은 단계로 제한한다.
- 설치기는 assets를 사용한다. fixture의 manifest/hash와 대상 구현을 먼저 확인하고
  설치 runtime과 배포 버전의 차이를 시험 중 무단 수정으로 덮지 않는다.
- fixture 초안 P904가 남은 `--open` exit 1과 구조 오류 exit 2를 구별한다.
- 두 실제 채팅 참여·사용자 발언·수신 응답은 실행 입력이며 준비 검토의 미결 제품 결정이 아니다.
  dev는 준비를 시작할 수 있고, 해당 입력이 없으면 단계별 차단을 기록한다. 완료 조건은 완화하지 않는다.

## 등록 및 dev 인수

등록 전 실제 확인:

- `plan_cards.parse/validate_execution`: P002 준비 완료·미착수, 체크 0/5, 실행 로그 없음.
- 세 문서의 모든 상대 Markdown 링크 대상 존재 확인.
- `work_queue.py --owner all --json` 및 `--brief`: P002 READY, owner=dev,
  next.dev=P002, 새 요구/결정/중지/인계 목록 비어 있음.
- `contract_guard.py check --target worktree`: plan 기록 검사 PASS.
- 기준 dev HEAD 및 clean 상태 재확인. dev는 여전히 기존 `65ab55647991` 채택 상태이며,
  P002를 자동 채택하거나 실제 시나리오를 실행하지 않았음.

세 문서를 같은 plan 커밋에 기록하고 기존 origin의 plan 브랜치로 정상 push한다.
카드 parser, queue JSON/brief, 링크, diff, plan guard(worktree/index/커밋)를 확인한다.
P002=READY/owner=dev/미착수/0 of 5, next.dev=P002인 것이 plan 측 등록 기대값이다.
검토 기록에 실제 실행 PASS 또는 dev 채택 완료를 미리 기록하지 않는다.

dev 인수 시 이 검토가 포함된 plan 커밋의 전체 SHA를 확인한다. 기존 dev 변경과 실패 로그를
보존하며 통합하고 `contract_guard.py adopt <전체-SHA> --review-reference
docs/planning/reviews/P002-readiness.md`로 기록·커밋한다. 그 후 P002를 실행한다.
이 plan 채팅이 dev를 대신 통합/adopt하지 않으며 큐 등록 자체로 dev가 자동 실행되지는 않는다.
실제 채팅 발송이나 별도의 SENT/ACKNOWLEDGED 상태를 이번 등록의 증거로 만들지 않는다.
