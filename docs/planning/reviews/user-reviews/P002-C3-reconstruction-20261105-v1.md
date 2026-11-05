# P002 continuation 재구성 검토 — 2026-11-05

- 공통 key: `P002-C3-reconstruction-20261105-v1`.
- 상태: 기존 P002 범위 안에서 아래 조건으로 재구성 방법 승인. 인간 질문 0회.
- Dev packet commit: `b72b967157d4287f60d94d4f148a9edc116d948f`.
- 원본: `docs/feedback/dev/reviews/P002-reconstruction-20261105.md` 및
  `docs/verification/P002/recovery-20261105/inventory.json`.
- 실제 수신: 기존 dev가 위 커밋/방법 검토를 plan에 전달했다. 이 문서는 ACK ping이 아니라
  복구 방법의 실제 결정과 다음 역할 행동을 위한 검토다.
- 기존 인간 답변: `../P002-resume-20261105.md`에 기록한 양쪽 재개·잔여 검증 완료 요청.
  같은 현재 재개를 다시 묻지 않는다. 새 사용자 권한이나 제품 의미 판단은 필요하지 않다.

## 확인한 근거

Plan은 `git show`로 packet, inventory, 원래 S1 RESOLVED 원문 export, marker 판단,
S3 두 번째 OPEN 원문 export와 scope를 직접 읽었다. 역사적 source
`77b757cce25dd2f5ee5b3751dbfb26fb70d88d08`의 `assets/scripts/workflow_control.py`에서
RESOLVED의 결정 SHA가 실제 채택의 ancestor여야 한다는 검사와 상태/결정 필드만 제외하는
immutable fingerprint를 확인했다. Inventory는 원본 파일 0개, 원래 세 role rev-parse128,
원래 SHA 부재, 106개 기존 export 보존, source 29개 hash 일치와 preview exit0/apply 미수행을
기록한다. 이 수치는 dev의 커밋된 실제 조사 근거이며 plan이 같은 inventory를 새 실행했다고
주장하지 않는다. 기존 plan의 읽기 조사에서도 Git 연결/HEAD 부재를 직접 확인했다.

원래 Git 이력의 복원으로 표현할 수 없다. 따라서 새 저장소·새 SHA를 사용하는 명시적
continuation이 필요하며 과거 출력과 신규 실행을 구별하면 기존 P002의 잔여 검증 목적에 맞는다.

## 승인된 방법과 SHA 대응

Dev 제안 1–7을 다음 정확한 경계로 승인한다.

1. `P002-20261029-A-CONT-20261105`를 새 continuation ID로 사용한다. 원래 run ID,
   질문·카드·marker의 `P002-20261029-A`는 보존한다. Preview한 부재 destination에만 역사적
   0.2.0 source와 동일 옵션으로 bootstrap apply한다. 원본 폴더는 보존하고 새 remote는 없다.
   Runtime/관리 파일 hash를 비교하고 경로 등 문맥 차이만 별도로 설명한다. 불일치 시 멈춘다.
2. 실제 plan은 자기 계약/검토/scope와 최종 PAUSED/all checkpoint를 원본 bytes로 복원한다.
   실제 dev는 자기 checkpoint/질문/실행 증거를 복원한다. Dev가 plan 소유 내용을 대신 작성하거나
   양쪽을 한 세션으로 흉내 내지 않는다. Infra bootstrap은 기존 승인 범위의 dev 준비 작업이다.
3. 실제 fixture plan에서 새 continuation decision 문서를 별도 commit한다. 판단은 기존과 같다:
   P901 marker는 `VERIFIED-P002-20261029-A` 뒤 newline 한 개, S5에서만 실행한다.
   P901 영향과 P903 의존 차단, P902 독립·역사적 완료, P904 DRAFT를 유지한다.
   이 배포 저장소 검토 SHA 자체를 fixture의 결정 SHA로 넣지 않는다.
4. Dev가 위 새 fixture decision commit을 정확 통합/adopt한 후 첫 RESOLVED live copy의
   `> 결정 plan:` 한 줄만 원래 `e6dc181e0a330c7f050fcf70638c5fad2fd8f8ee`에서 새 fixture
   decision 전체 SHA로 대응시킬 수 있다. 원본 완전 bytes/hash는 불변 archive에 보존한다.
   원본 hash `ee1737dfb7134d243da7076362b176c03eb14b4ac2ff27bd6494650ee2350b09`, 새 hash,
   정확 단일 필드 diff, fingerprint 동일, ancestor 검사를 기계 검증해 mapping에 기록한다.
   상태 RESOLVED/질문 본문/과거 원문은 바꾸지 않는다. 이것은 재구성 metadata이고 새로운
   S1 resolve나 원래 SHA 복구가 아니다. Guard/runtime을 완화하지 않는다.
5. 두 번째 OPEN은 원본 SHA-256
   `40fc3d247b2d386f8d8f2761e5f81791a60ca5f4468f335522e61dc213d9f8c7`과 bytes가 같아야 한다.
   scope fingerprint `ac4e246fa0d00d3e5bb2eb29f20de253d4492a5ace8f07bd96623f4a23c64410`도
   유지한다. 새 결정 채택만으로 이 OPEN을 resolve하지 않는다.
6. 두 checkpoint PAUSED/all, 두 next=null, second OPEN scoped P901/P903, P902 DONE과
   P904 DRAFT, P901/P903 미실행인 복원 기준선을 실제 두 역할이 확인한다. P902 완료와
   C1/C2/S2는 역사적 증거 승계이며 새 실행으로 표기하지 않는다. 모든 새 commit/time은 실제 값이다.
7. 이미 받은 실제 인간 지시로 dev 자기 checkpoint 먼저 재개하고 plan/all 및 OPEN 차단을
   확인한다. 다음 실제 plan이 자기 checkpoint를 재개해 pauses=[]/OPEN 유지 확인을 한다.
   두 개의 별도 인간 발언이 아니라 하나의 양쪽 재개 지시를 단계적으로 실행한 것으로 기록한다.
   S3.6/7의 이후 새 인간 입력은 실제 단계에 plan 창구에서 한 번만 요청한다. S4/S5는 원래
   독립 기대값과 실제 두 역할·전달·검증 증거를 유지한다. C3–C5를 지금 PASS로 바꾸지 않는다.

## 다음 행동과 전달

배포 dev는 이 검토가 포함된 정확 plan SHA를 통합/adopt한 뒤 bootstrap apply·runtime/hash
검증까지 준비한다. 실제 fixture plan writer가 필요해지는 시점에 새 경로, 양쪽 HEAD/branch,
초기 guard/관리 hash, immutable export 출처와 구체적인 plan import/decision 행동을 전달한다.
Plan이 자기 fixture 기록과 decision을 commit한 뒤 dev가 정확히 채택해 자기 기록을 복원한다.
이미 검토한 방법의 재승인이나 단순 ACK를 요구하지 않는다. 각 전달은 실제 다음 역할 행동을
위한 비동기 인계이며 SENT 후 종료한다. 다른 프로젝트·개인 설치·배포 main·훅은 그대로 둔다.

이번 검토 시 fixture는 아직 생성되지 않았고 이 판단의 dev 채택·bootstrap·재개는 미관찰이다.
완료/전달/채택은 각 실제 근거가 생길 때 기록한다. 원본 조사·실패·기존 중지 이력은 보존한다.
