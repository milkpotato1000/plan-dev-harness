# P005 기존 설치 보존 업그레이드 계약

2026-11-04 사용자 요청: 기존 plan-dev 하네스 프로젝트를 찾아 0.2.1로 업데이트하되
기존 작업과 중지 상태를 유지한다. 이 요청은 현재 유지보수만 승인하며 제품 실행은 승인하지 않는다.

## 대상과 경계

조사에서 실제 설치 4개(배포 저장소 자체 1개, 기존 제품 3개)를 확인했다.
다운로드/연구용 사본은 설치로 보지 않는다. 개인 스킬 0.2.1은 P004에서 완료했으며 재설치하지 않는다.
배포 저장소에는 원격 공개가 불필요한 타 프로젝트 경로·내부 요구·데이터·채팅 ID를 넣지 않는다.
대상 inventory와 백업은 private local artifact에 둔다. 대상별 자체 review는 해당 저장소에 둔다.

## 수행 순서

1. 대상별 지침/branch/status/adoption/queue/hook/remote/writer와 변경·제어 문서 hash를 기록한다.
   현재 writer가 있으면 해당 쓰기가 종료될 때까지 그 worktree를 수정하지 않는다.
2. 관리 설치는 원래 옵션으로 0.2.1 installer preview한다. legacy는 동일 preview의 충돌을
   근거로 수동 통합하며 installation manifest를 조작해서 overwrite 보호를 우회하지 않는다.
3. dev는 설치 diff와 커스텀 규칙 통합안을 임시 디렉터리에서 제안·검증한다. 대상 보호 파일은
   plan 검토 전 변경하지 않는다. plan은 실제 diff와 검증을 보고 승인한 파일을 plan 이력에 넣는다.
4. 이미 dev가 채택한 baseline 이후 plan에 제품 변경이 있으면 유지보수 commit을 그 baseline에
   기반하여 격리한다. plan으로 정상 merge해 ancestry를 만들고 dev는 그 유지보수 SHA만 통합/채택한다.
   최신 plan 제품 변경을 자동 전달하지 않는다. 미커밋은 stash/reset/강제 checkout 없이 보존한다.
5. 대상별 plan commit 후 dev에서 exact merge/adopt/commit, worktree/index/HEAD guard/queue를 확인한다.
   기존 dev 실행 로그를 보존한다. 외부 역할 채팅 발송 권한은 이 계약에서 만들지 않는다.
6. authorized non-force plan/dev push만 기존 remote에 수행하고 실제 refs를 검증한다.
   main/FE/백업·stash·태그·릴리스·서비스 설정·인증을 변경하지 않는다.

## 통합 요구

- 0.2.1 역할 복원 규칙을 실제 outer와 child AGENTS/CLAUDE entrypoint에서 도달 가능하게 한다.
  plan은 계획/검토/인계, dev는 정확 채택 후 구현한다. 문서도 목적에 따라 구분하고 plan-only
  push를 목표 ref 전달 완료로 표시하지 않는다. 명시 역할·single writer·bootstrap 대기를 유지한다.
- 기존 큐/guard의 제품별 추가 보호, 승인 ledger, intake, legacy OPEN/PAUSED 및 adapter hooks를
  stock 파일로 덮어쓰지 않는다. 필요한 0.2.1 runtime은 기존 의미를 보존해 통합·회귀 검증한다.
- 새 controls 도입 시 과거 기록의 parser 호환성과 conservative blocking을 확인한다.
  과거 checkpoint/결정/one-shot 상태를 변환·재무장·resolve·resume하지 않는다.
- 새 runtime을 안전하게 통합할 수 없으면 instruction-only 적용과 full runtime 미완료를
  구분하고 실제 남은 차이를 보고한다. 버전 숫자만 변경하거나 부분 적용을 full upgrade로 부르지 않는다.
- 기존 같은 이름의 프로젝트 일상 작업 skill을 설치용 skill로 치환하지 않는다.
- 배포 저장소의 P002 fixture PAUSED/OPEN·2/5는 그대로다. 없어진 tmp fixture를 재생성하지 않는다.
- 업그레이드는 새 하네스 기능 검증에 한정한다. 제품 테스트/모델/DB/Asana/Confluence 작업과
  대기 제품 큐 시작은 하지 않는다. 제품 P카드의 요구·실행 상태를 바꾸지 않는다.

## 검증 및 완료 증거

실제 네 대상별 적용 방식, source VERSION/hash, 변경 allowlist, baseline parent/plan merge/dev adoption,
상태 보존 fingerprint, guard 세 target, 전후 큐의 동일한 기존 과업/차단 상태, hooks/remotes/main,
필요한 커스텀 하네스 회귀와 원격 ref를 기록한다. code 변경에는 관련 회귀가 필요하다.
기계 테스트·지침 검토와 실제 새로운 모델 세션 준수 검증은 구분한다.
대상 안전성에 필요한 판단이 해결되지 않으면 해당 대상만 pending으로 남기고 나머지는 완료한다.
모든 조건은 실제 증거가 있을 때만 체크한다.
