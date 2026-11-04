# P005 보존 통합 검토 기준 — 2026-11-04

현재 판정: proposal 대기. 아래는 적용 승인 전 확인할 조건이며 아직 적용 PASS가 아니다.

## 직접 조사한 공통 차이

- 관리 설치는 현재 manifest 0.2.0이고 source0.2.1과 설치 파일 계층이 다르다.
  같은 옵션으로 preview 후 실제 action과 hash를 확인한다.
- legacy 세 설치에는 manifest가 없다. 가짜 managed manifest를 만들지 않는다.
  수동 통합 사실과 stock/custom 구성 및 source hash를 별도 provenance로 기록한다.
- legacy 하나는 immutable intake를 이미 갖고 있고 두 개는 intake가 없다.
  추가될 workflow controls가 기존 결정/중지 기록을 같은 의미로 읽는지 확인한다.
- 한 제품의 Agent 승인 ledger guard는 stock에 없는 보호다. 함수와 check/pre-push
  호출 모두 보존하고 미승인 version negative case를 검증한다.
- 같은 제품의 P카드 timestamp parser는 마지막 Z만 UTC로 바꾸고 내부 Z를 거부한다.
  stock의 무조건 replace로 덮어쓰지 않고 기존 strict parsing을 보존한다.
- 기존 readonly 큐 출력에 추가되는 intake/controls 필드는 허용하되 기존 task 상태,
  next selection, OPEN/PAUSED의 차단 의미는 업그레이드 때문에 바뀌면 안 된다.

## 적용 전 gate

1. 모든 변경은 유지보수 allowlist 안이어야 한다. 제품 카드·요구·실행·검증·one-shot
   상태의 원본 bytes와 미커밋 diff가 그대로인지 확인한다.
2. 보호 정책은 기존 항목을 제거하지 않고 필요한 controls/intake 소유권만 추가한다.
   adapter hooks와 Git 설정·remote·main/FE/backup refs는 그대로다.
3. 새 세션 규칙은 outer/child에서 읽히고 기존 plan role 유지 및 메시징 grant를
   넓히지 않는다. branch=role 같은 과거 지침과 충돌을 남기지 않는다.
4. 실제 파일상 적용 검토 후 계획 담당이 대상 baseline을 확정한다. 오래된 adoption이
   있는 경우 baseline 부모는 그 adoption이며, plan에 merge한 유지보수 SHA를 dev에 준다.
   최신 제품 plan tip을 채택하지 않는다.
5. 실제 적용 후 guard worktree/index/HEAD, queue 및 custom regression을 재검사한다.
   정상 push의 결과는 기존 각 remote ref와 비교한다. 완료 여부를 단계별로 남긴다.

예상 한계: 지침 및 runtime 검사는 실제 새 모델의 모든 행동 준수를 증명하지 않는다.
Git 밖 outer entrypoint는 원격 push로 다른 컴퓨터에 전파되지 않는다.
