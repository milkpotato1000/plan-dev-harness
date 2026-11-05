# P002 실제 세션 검증 계약

상태: 준비 검토 완료. 이 문서는 기대 동작과 실행 절차이며 수행 결과가 아니다.
작업서: [P002](plans/P002.md). 준비 검토: [P002 readiness](reviews/P002-readiness.md).

## 기준과 역할

기능 기대값은 [제어 흐름 계약](../process/workflow-controls.md),
[역할 규칙](../process/agent-workflow.md), [큐 계약](../process/work-queue.md)에서 도출했다.
기존 dev의 `docs/verification-v0.2.0.md`는 CLI 회귀, `docs/verification-local-harness-setup.md`는
설치와 두 채팅 초기화의 증거다. 이 둘만으로 아래 실제 세션 흐름의 PASS를 만들 수 없다.

| 담당 | 책임 |
| --- | --- |
| 배포 dev 채팅 | P002 정확한 채택, 검증 환경 준비, fixture dev 역할, 실행 증거 수집·커밋·결과 보고 |
| 배포 plan 채팅 | 같은 승인 계약에 따라 fixture plan 역할 수행, 결정 영향·해결 근거 검토·커밋, 수신 확인 |
| 사용자 | 두 기존 채팅에 실행 경로/단계를 전달, 단계별 실제 중지·재개 발언, 기본 수동 인계 전달 |

두 채팅을 식별할 수 있는 참조와 실제 실행 시각을 비공개 실행 기록에 남긴다.
공개 증거에는 `session-plan`, `session-dev` 별칭과 원문 중 비민감 발췌를 쓴다.
앱 전체 대화·토큰·개인 경로·인증정보를 공개하지 않는다. 원본 참조가 비공개이면 그 한계를 밝힌다.
같은 채팅의 역할 전환, sub-agent/명령 두 개 또는 작성자가 만든 대화문은 별도 실제 채팅 2개의 대체 증거가 아니다.
새 채팅 생성·자동 메시지·모델 API 호출을 요구하지 않는다.

## 환경과 증거 계약

1. dev는 P002가 포함된 plan 커밋 전체 40자리 SHA와 검토 경로를 기록하고 실제 dev에
   통합·채택·커밋한다. guard의 worktree/index/HEAD와 큐를 확인한 후 준비를 시작한다.
2. 배포 dev의 소스 커밋과 `assets/` 및 installed runtime의 hash를 기록한다.
   별도 임시 부모 아래 부재한 목적지에 현재 dev의 `scripts/bootstrap_workspace.py`를
   먼저 preview하고 같은 옵션으로 apply한다. 기존 디렉터리나 다른 프로젝트는 재사용하지 않는다.
   새 fixture 자체의 baseline main 생성은 허용되며 배포 저장소의 main과 무관하다.
3. bootstrap은 배포 assets를 설치하므로 fixture 설치 manifest·runtime hash가 검증하려는
   현재 v0.2.0 구현과 일치하는지 확인한다. 불일치하면 멈추고 기록한다. 실행 중 임의 교체하지 않는다.
   fixture에서만 설치되는 로컬 훅을 사용하며 실제 배포 저장소의 훅 설정은 바꾸지 않는다.
4. 두 채팅이 사용자로부터 동일 run ID와 fixture 절대 경로를 받아 각자 plan/dev 역할을
   확인한다. 배포 저장소의 역할은 유지한다. fixture당 writer도 각 역할 하나다.
   plan 채팅이 참여할 수 없으면 dev는 준비 결과와 대기 지점을 커밋하고 기다린다.
5. fixture에는 아래 가상 카드만 plan 채팅이 만든다. 이 번호는 별도 저장소에 한정되며
   배포 프로젝트의 P번호·실제 과제가 아니다. 카드의 fixture 승인 근거는 P002 계약이다.

| fixture 카드 | 준비/우선순위/선행 | 무해한 동작 |
| --- | --- | --- |
| P901 | 준비 완료 / 10 / 없음 | plan이 결정한 완료 marker를 증거 파일에 기록 |
| P902 | 준비 완료 / 20 / 없음 | marker와 무관한 독립 확인 파일 기록 |
| P903 | 준비 완료 / 30 / P901 | P901 완료 후에만 별도 확인 파일 기록 |
| P904 | 초안 / 40 / 없음 | plan 큐 선택이 가능한지 관찰하는 초안; 실행 금지 |

6. fixture plan은 준비 카드 및 결정 검토만 작성한다. fixture dev는 정확한 SHA를
   통합·adopt하고 실행 필드·증거만 작성한다. plan은 커밋된 dev 질문을 읽고
   자기 검토를 작성하며 dev 전체를 plan으로 병합하지 않는다.
7. 모든 단계는 작업폴더/branch/HEAD/adopted SHA, ISO 시각(시간대 포함), 입력·명령·
   stdout/stderr/exit code와 두 역할의 queue JSON을 남긴다. 상태가 바뀌기 전후를 연결한다.
   로컬 공용 Git 객체로 전달되는 범위만 검증하며 원격 fetch 전달을 검증했다고 쓰지 않는다.
8. 결과는 배포 dev의 `docs/verification/P002/`에 보존한다.
   `report.md`, `environment.md`, `events.md`, `S0/`~`S5/` 및 `regression.log`를 기본 구조로 쓴다.
   events에는 run ID·시나리오·역할·행동·예상/실제·commit·상대 관찰 commit·근거 경로를 둔다.
   fixture의 결정·scope·checkpoint·handoff JSON/문서와 필요한 Git commit/patch를
   hash와 함께 export하여, 임시 저장소가 없어져도 상태와 변경 이력을 검토할 수 있게 한다.
   전체 저장소/대화를 무차별 첨부하지 않는다.

## S0 — 기준선과 실제 세션 확인 (C1)

fixture plan이 P901~P904를 커밋하고 fixture dev가 해당 전체 SHA를 통합·채택·커밋한다.
각 채팅이 자기 경로·역할과 상대의 커밋된 상태를 직접 읽었다는 발췌를 남긴다.

독립 기대값: plan의 다음 작업은 P904, dev는 P901. pending_decisions/paused_sessions/
handoffs는 비어 있다. 두 역할의 guard는 통과한다. 두 채팅이 각자 쓴 증거가 필요하다.
두 역할 분리 확인 없이 이후 CLI 출력만 수집해 C1을 통과시키지 않는다.

## S1 — 결정 요청·분류·채택·해결 (C2)

| 순서 | 담당과 행동 | 독립 기대값 |
| --- | --- | --- |
| 1 | dev가 P901 완료 marker 선택 질문을 `decision`으로 기록·커밋 | 미분류 OPEN은 dev 전체 차단. dev next=null. plan next=P904 |
| 2 | plan이 커밋된 질문을 읽고 P901만 영향, P903은 그 의존, P902는 무관하다는 검토·scope(tasks P901)를 커밋 | 아직 채택하지 않은 dev는 계속 전체 차단 |
| 3 | dev가 분류 plan 전체 SHA를 통합·채택·커밋 | P901/P903에 blocked_by_decisions. P902는 차단되지 않고 dev next=P902 |
| 4 | dev가 P902의 무해한 작업을 실제 수행·증거 커밋 | 일반 intake/결정 대기로 무관 작업을 멈추지 않았음. P901/P903 실행은 하지 않음 |
| 5 | plan이 marker를 `VERIFIED-<run-id>`로 확정한 판단 문서를 새 커밋 | dev는 그 결정 커밋 채택 전에는 resolve 불가 |
| 6 | dev가 채택 전 전체 결정 SHA로 resolve 시도, 이후 정확한 결정 SHA를 통합·채택하고 짧은 SHA로 resolve 시도 | 각 exit 2. 질문 원문·OPEN 유지. 오류와 파일 hash 보존 |
| 7 | dev가 채택한 전체 결정 SHA로 resolve·커밋 | pending_decisions=[]; P901 선택 가능. P903은 P901 미완료로 WAITING 유지 |

scope 분류 커밋과 실제 판단 커밋을 구별한다. 분류만 했는데 질문이 해결됐다고 쓰지 않는다.
fixture 판단은 이 계약의 가상 marker 선택이며 실제 제품 의사결정 역량을 검증했다고 확장하지 않는다.
실제 세션이 차단된 P901/P903을 작업하지 않고 P902를 선택했는지 행동 근거를 함께 남긴다.

## S2 — 역할 중지와 상대 커밋 가시성 (C3)

1. 사용자가 plan 채팅에 “이번 검증의 plan 역할만 중지해줘”라는 실제 발언을 보낸다.
   plan은 그 참조로 `pause --scope role`를 기록한다. 커밋 전 dev 큐에는 그 중지가 보이지 않는다.
   plan은 checkpoint와 중지 전후 증거만 보존·커밋한다.
2. 커밋 후 dev가 직접 조회한다. plan 중지(role)가 보이고 next.plan=null이지만 dev next=P901이다.
   dev는 독립적으로 허용된 상태 확인만 하며 plan에게 추가 업무를 지시하지 않는다.
3. 중지 이후 사용자가 plan에 명시적 재개를 요청한 뒤에만 plan이 `resume`을 기록·커밋한다.
   plan next=P904가 복원되고 중지 이력은 보존된다.

실제 사용자가 보낸 발언의 시각·대상·비민감 발췌가 필수다. 검증 계획 승인이나 미리 준비한
예문, 다른 채팅/에이전트가 전달한 재개 지시는 실제 사용자 재개 발언을 대신하지 않는다.
자동으로 연속 pause/resume을 실행하지 않는다. 시간 경과와 새 큐 조회만으로 재개하지 않는다.
각 제어 요청에는 P002 run ID와 fixture에 한정된 중지/재개라는 범위를 명시한다.
사용자가 실제 프로젝트나 채팅 전체의 중지를 요청하면 이를 시험 입력으로 축소 해석하지 않고
그 요청 범위대로 중지한다. 이후 P002도 해당 범위의 실제 재개 요청 전까지 계속하지 않는다.

## S3 — 전체 중지·각 역할 재개·결정의 독립성 (C3)

1. dev가 P901에 두 번째 가상 질문을 생성·커밋한다. plan은 P901 영향 scope 및
   답변 검토를 커밋하고 dev가 정확히 채택한다. 이 시점 질문은 OPEN 상태로 둔다.
2. 사용자가 dev에 양쪽 중지를 요청한다. dev가 기본 `pause`(scope=all)를 기록·커밋하고
   plan이 사용자 요청의 상태 확인으로 커밋된 중지를 읽는다. 두 next가 null이다.
3. 별도의 실제 사용자 발언으로 plan도 자기 중지를 기록·커밋한다. 원래 dev 중지는 유지된다.
4. 사용자가 dev에만 재개를 요청한 뒤 dev가 자기 기록을 resume·커밋한다.
   plan의 전체 중지와 OPEN 질문은 남고 두 next는 null이다.
5. 이후 사용자가 plan에 재개를 요청하면 plan이 자기 기록을 resume·커밋한다.
   pauses=[]이지만 OPEN 질문은 남고 P901은 차단된다. 중지 해제가 결정을 해결하지 않는다.
6. 사용자가 dev 역할만 중지를 요청하면 dev가 role pause를 기록·커밋한다.
   이어 사용자가 “검증을 위해 기록된 답변으로 결정 해결만 처리하고 업무 선택은 계속 중지”라고
   별도 요청한 경우에만 dev가 이미 채택한 전체 판단 SHA로 resolve·커밋한다.
   pending_decisions=[]이어도 dev의 PAUSED와 next.dev=null은 유지되어야 한다.
7. 사용자가 dev를 명시적으로 재개하면 resume·커밋한다. P901을 선택할 수 있어야 한다.

중지 상태에서 허용하는 예외는 checkpoint/증거 보존, 사용자 요청의 상태 확인 및
6번의 명시적으로 요청받은 제어 기록 처리뿐이다. 제품/fixture 작업을 계속하지 않는다.
필요한 사용자 발언이 오지 않으면 단계와 필요한 입력을 보고하고 대기한다.
중지 이력 삭제·일괄 ACTIVE 전환·다른 역할의 checkpoint 직접 편집은 금지한다.

## S4 — 실제 양방향 인계와 증거 (C4)

두 역할이 ACTIVE이고 OPEN 질문이 없는 상태에서 수행한다.

1. plan은 검증 인계 문서를 먼저 커밋한다. 그 커밋 전체 SHA와 문서 경로로
   WORK_READY(target=dev)를 생성·커밋한다. 상태 PENDING은 아직 전달하지 않았다는 뜻이다.
   같은 명령 재실행은 KEEP이며 파일 hash/이력/이벤트 수가 그대로다.
2. 같은 key에 다른 summary 또는 next-action을 넣으면 exit 2이고 기존 파일은 불변이다.
   PENDING→ACKNOWLEDGED 직접 전이와 비어 있는 전달 증거는 exit 2이며 이력은 불변이다.
3. 기본 전달 경로: 사용자가 event ID·문서 경로·전체 SHA·다음 행동을 dev 채팅에 직접 전달한다.
   송신 plan은 사용자의 실제 전달 확인을 받은 뒤 해당 참조로 SENT를 기록·커밋한다.
   사용자 확인은 전달 근거, dev의 직접 읽기·응답은 별도의 수신 근거다.
4. dev는 실제 커밋 문서와 event를 읽고 받은 SHA·완료/미완료·다음 행동을 응답한다.
   사용자가 그 응답을 plan에 전달하면 송신 plan이 실제 응답 참조로 ACKNOWLEDGED를 기록·커밋한다.
   sender가 수신 사실을 추측하거나 receiver를 대신하여 응답문을 쓰지 않는다.
5. ACK 후 같은 원본 handoff 명령은 KEEP이며 재전송하지 않는다. ACK를 다시 상태 전이로
   기록하려 하면 exit 2이고 기존 이력은 유지된다.
6. dev가 비민감 결과 문서를 커밋한 뒤 DECISION_REQUEST(target=plan)의 별도 인계로
   1~5를 반대 방향으로 반복한다. 이 인계 자체는 OPEN 결정 요청을 생성하지 않는다.
   plan이 결과 문서를 직접 읽고 응답하고 송신 dev가 최종 ACK를 기록한다.

도구 발송은 별도 사용자 명시 권한이 있을 때만 사용한다. 그 경우 실제 도구 성공 결과를
SENT에, 수신자의 직접 읽기·응답을 ACK에 연결한다. Git push·PENDING 파일 생성·큐 표시만으로
SENT/ACK를 올리지 않는다. 전송 실패·미응답은 그 상태로 남기고 C4를 체크하지 않는다.

## S5 — 결과·회귀·보존 (C5)

- 무해한 P901 marker 기록과 그 증거를 완료 처리한 후 P903이 선택 가능해지는지 확인한다.
  필요한 fixture 작업을 마치고 P904는 초안으로 남긴다. fixture의 pause/OPEN은 해소되었는지 확인한다.
- fixture 양쪽 guard(worktree/index/HEAD), queue JSON 및 `--open` 결과를 보존한다.
  P904 초안이 남으므로 fixture `--open` exit 1은 정상이다. exit 2는 정상으로 처리하지 않는다.
- 배포 dev에서 기존 전체 회귀를 수행해 stdout/stderr/exit code와 Python/Git 버전을 보존한다.
  P002 실행 필드·검증 증거 변경에 대해 실제 guard(worktree/index/HEAD)를 확인한다.
  실제 P002 미완료 동안 배포 큐 `--open` exit 1을 완료 오류와 혼동하지 않는다.
- `report.md`는 S0~S5와 C1~C5를 근거 경로에 연결하고 실제 세션 수행/CLI 보조 검사를 구분한다.
  FAIL이면 원인과 이전 근거를 보존하고 재검증 결과를 추가한다. SKIP/BLOCKED는 PASS가 아니다.
  가용 도구·수동 전달·공용 로컬 Git에 한정된 결과이며 Claude/다른 OS/원격 전달/실행 중
  프로세스 강제 중단/모든 모델의 준수까지 검증했다고 쓰지 않는다.
- P002 체크는 조건별 최신 PASS 근거와 함께 갱신한다. 실제 증거를 커밋한 후 HEAD 검사를 하고,
  plan이 커밋된 dev 증거를 큐로 읽을 수 있는지 확인한다. plan으로 구현 이력을 병합하지 않는다.
- 배포 저장소 실제 main/릴리스/훅 설정과 기존 P001 기록은 보존되었음을 확인한다.
  양쪽 writer가 종료했는지와 fixture 보관 위치를 보고한다. 증거 export 전 삭제하지 않으며,
  자동 정리를 수행하지 않는다. 후속 세션이 재검토/재개할 수 있도록 checkpoint를 남긴다.

## 실패·입력 대기·범위 변경

참여 세션·발언·전달·권한이 없거나 증거가 부족하면 dev는 P002 실행 상태를 차단으로 바꾸고
STATE 로그에 해당 단계, 완료/미완료, 필요한 실제 입력, 재개 방법을 쓴다. 불필요한 반복 질문이나
별도 채팅으로의 무단 메시지로 보충하지 않는다. 사용자 중지는 실제 요청에 따라 별도로 유지한다.
검증 실패는 FAIL 근거로 보존한다. 새 기능이나 제품 수정이 필요하면 immutable intake 후
plan 검토·정확한 채택을 거친다. 검증 중 기대값을 낮춰 완료하거나 설치 runtime을 몰래 바꾸지 않는다.
