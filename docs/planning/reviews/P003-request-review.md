# P003 요청 접수·중복 검토 — 2026-10-29

판정: 기존 기능 일부와 중복, 전달 실행 절차·배포 정합성은 별도 개선 후보.
연결: [P003 초안](../plans/P003.md), [제안 계약](../P003-direct-handoff.md).
이번 접수는 준비 완료/구현/채팅 발송/개인 설치 변경 승인이 아니다.

## 요청 출처와 보존 범위

다른 프로젝트의 plan 채팅에서 사용자가 하네스 개선 필요를 이 plan 채팅으로 직접 전달하라고
지시했다는 메시지를 수신했다. 인용된 사용자 발언: “직접 전달해줘.” 및 하네스에 해당
내용이 없으면 이 프로젝트에도 전달해 두라는 요청이다. 전달 메시지는 이 plan에서 검토·기록하고
기존 카드와의 중복을 확인하되, 다른 채팅으로 연쇄 전달하거나 새 작업을 무조건 승인하는
근거로 사용하지 말라고 범위를 제한했다.

전달된 사례: 다른 프로젝트에서 준비된 계획 인계 시 붙여넣을 문구만 제공해 사용자가 직접
발송을 재요청했다. 이후 해당 채팅은 정확한 plan SHA와 범위·검증·상한을 dev에 전달했다고
보고했다. 이 사례의 원본 프로젝트 동작이나 수신·착수는 여기서 독립 검증하지 않았다.
공개 저장소에는 타 프로젝트명·작업 번호·실제 SHA·경로·채팅 ID·업무 요구를 옮기지 않는다.

plan으로 직접 들어온 접수이므로 dev의 immutable request가 있었던 것처럼 R번호나
`plan_intake.py review` JSON을 만들지 않는다. 이 검토와 초안이 접수·분류 기록이다.

## 기존 작업과의 중복

| 기존 근거 | 이미 포함하는 내용 | 이번 요청의 차이 |
| --- | --- | --- |
| [P001 계약](../P001-v0.2.0-workflow-controls.md), dev의 완료 증거 | 종류별 인계, event key 중복 방지, PENDING/SENT/ACKNOWLEDGED | 상태 관리 기능을 새로 만들 필요 없음 |
| [현재 제어 절차](../../process/workflow-controls.md) | 사용자 권한+호스트 도구가 있을 때 실제 메시징, 근거 있는 전이 | 권한·수신자 확인 후 직접 발송까지 이어가는 담당 절차가 짧음 |
| [선택 어댑터 경계](../../process/optional-adapters.md) | 실제 수신자, 명시 권한, 전송/수신 근거 | 승인된 발송을 사용자 복사 전달로 되돌리지 않는 구체 흐름 필요 |
| [P002](../plans/P002.md), [S4](../P002-session-validation.md) | 실제 양방향 인계 검증, 기본 수동 경로와 별도 승인된 도구 발송 경로 | P002는 검증 작업이며 제품 절차·배포·개인 설치 개선을 포함하지 않음 |
| `references/role-chats.md` | 명시 요청 시 채팅 생성·초기화, 초기 프롬프트 권한의 한계 | 기존 채팅에 승인된 결정/작업을 보내는 일상 절차와 다름 |

분류: P002의 완료 조건을 바꾸거나 같은 상태 머신을 재구현하지 않고 P003에 제안한다.
P002는 기존 계약 그대로 유지한다. P003을 P002 선행/차단 요인으로 추가하지 않는다.

## 읽기 전용으로 확인한 배포 차이

비교 기준: plan `1240750d450271d5c0f137f12d66b305dd64277e`,
dev `d2b900713fb8aa7be8f1599c9ef92e5b401339dc`, 세션에 제시된 기존 개인 설치.

| 표면 | 실제 확인 |
| --- | --- |
| plan 소스 | SKILL.md 48행. 배포 assets에는 workflow-controls.md가 없으나 설치된 docs/process에는 존재 |
| dev 소스 | SKILL.md 55행. v0.2 제어 절차 링크와 assets/docs/process/workflow-controls.md 존재 |
| plan/dev 공통 | references/role-chats.md 동일; scripts/install_skill.py 동일. 최신 역할 생성 문서는 직접 발송 일상 절차를 정의하지 않음 |
| 기존 개인 설치 | 긴 End-to-end SKILL. VERSION, scripts/install_skill.py, assets/scripts/workflow_control.py, assets/docs/process/workflow-controls.md 없음 |
| 설치 목적지 | 현재 install_skill.py의 Codex 기본은 ~/.agents/skills. 관찰한 구형 설치는 ~/.codex/skills. 기본 설치만으로 기존 로드 경로 교체를 보장할 수 없음 |
| 설치/업그레이드 | 프로젝트 install_harness.py의 --upgrade는 관리 hash/동일 옵션 조건부. install_skill.py에는 --upgrade가 없고 다른 기존 내용을 거부함 |

plan에 배포 v0.2 구현을 역병합하지 않았다. 개인 설치 파일은 읽었을 뿐 변경하지 않았다.
전체 SHA-256 비교 결과는 다음과 같으며, 같은 이름이 같은 내용/버전을 뜻하지 않음을 확인했다.

| 파일 | SHA-256 |
| --- | --- |
| plan SKILL.md | 8fdd2e5bfd8d10693847a7dbcf5cbf741828e3d2ff1732b67619e25a5342dd1d |
| dev SKILL.md | f9f7c7838482aa47a453a4da2198ca13268040e519daae4adcd34c7f8ae6fbbc |
| 관찰한 구형 설치 SKILL.md | ef68abc71303cec102228b61b0fb60190131d5ce066e1955812d2ce68c48c177 |
| plan/dev 설치된 docs/process/workflow-controls.md | 9a0a37deab0cfe13700e658eb941ca9b1c74690879ed74aef0ab4fa34a82d2aa |
| dev 배포 assets/docs/process/workflow-controls.md | 9a0a37deab0cfe13700e658eb941ca9b1c74690879ed74aef0ab4fa34a82d2aa |

## 후속 판단

P003은 초안이다. 이 메시지의 범위인 요청 검토·기록·초안 연결까지 수행한다.
준비 완료 전에는 적용할 제품 개선 범위의 승인 근거를 확인하고 제안 계약을 확정하며,
plan 소유 docs/process 변경을 plan에서 검토·커밋할 준비가 필요하다.
이후 dev가 정확한 plan을 채택해 배포 소스·문서·테스트를 구현한다.
기존 개인 설치의 전환은 별도 대상/방법/권한 확인 뒤 수행할 일이며 제품 수정 완료와 구별한다.

## 접수 산출물 확인

- P003 parser/실행 검증: 초안·미착수, 체크 0/5, 실행 로그 없음.
- 새 세 문서의 상대 링크 대상 존재 확인. 사례 식별자·개인 절대 경로는 배포 문서에 제외.
- 기존 P002 작업서·상세 계약·준비 검토는 기준 커밋과 byte 단위 동일함을 확인.
- queue JSON: next.plan=P003, next.dev=P002. 새로운 결정/중지/인계 이벤트 생성 없음.
- plan guard(worktree) PASS. 제품 코드/실제 메시징/개인 설치/다른 프로젝트 변경 없음.
  실행 테스트 결과는 없으며 이 검사는 기획 문서와 접수 상태의 정합성 확인이다.

## 후속 진행 — 2026-10-29

이후 사용자가 이 plan 채팅에서 하네스 관련 추가 계획 작업을 계속 진행하라고 요청했다.
그 요청에 따라 P003 계약·준비 검토를 확정하고 dev 큐에 등록한다.
앞 절의 초안/검토 한정은 최초 접수 당시 판단으로 보존한다. 현재 준비 상태와 인수 경계는
[P003 준비 검토](P003-readiness.md)를 따른다. 이 후속 요청도 다른 채팅 발송이나 실제
개인 설치 전환을 상시 위임하는 것으로 확대하지 않는다.
