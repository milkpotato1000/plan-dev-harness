# P002 실제 fixture plan 복원과 다음 dev 행동 — 2026-11-05

실제 plan 채팅이 역사적0.2.0 fixture의 자기 역할에서 11개 계약/검토/scope/최종 checkpoint를
원본 bytes로 복원했다. 새 snapshot commit은 `07da972a6a9512a86ba85075f8d9283323881d2a`다.
새 marker/범위 판단은 별도 commit `60a500f9a29932d74d24e2d1131790eb87a0ec32`이며,
관찰 증거 commit은 `101ffd07150b8edaca92388eeabf8a74158d4a2f`다.

배포에 보존한 원본 fixture export: [복원 hash/provenance](P002-continuation-plan/import.json),
[실제 명령·guard·queue](P002-continuation-plan/checks.json),
[새 fixture 판단](P002-continuation-plan/decision.md).
Worktree/index/HEAD guard 모두 PASS. 실제 plan checkpoint는 PAUSED/all이며 두 next=null이다.
Dev는 아직 초기 infrastructure HEAD `49332a605770478479e0c424f0eeb45261902718`였으므로
현재 관찰의 pending_decisions=[]는 dev 질문이 아직 복원되지 않았다는 뜻이다. OPEN 해결이나
양쪽 PAUSED 복원 완료로 해석하지 않는다. Plan은 dev 기록·완료 필드를 작성하지 않았다.

Dev 다음 행동: 새 fixture decision commit `60a500f9a29932d74d24e2d1131790eb87a0ec32`를
통합/adopt하고 review reference로 `docs/planning/reviews/P002-continuation-decision.md`를 사용한다.
자기 checkpoint·첫 RESOLVED의 승인된 단일 SHA mapping·두 번째 OPEN·P902 역사적 완료를
복원하고 두 중지/OPEN 기준선과 hash를 검증한다. 첫 RESOLVED mapping도 위 fixture decision
SHA를 쓴다. 배포 저장소 SHA와 혼동하지 않는다. 별도 evidence commit은 실제 읽기/보존할 수 있다.

그 후 이미 받은 실제 인간의 양쪽 재개 지시로 dev 자기 기록만 재개하고 남은 plan/all+OPEN에
두 next=null임을 확인한다. 실제 plan에 다음 자기 재개 행동을 전달한다. 지금 plan 재개는
하지 않았으며 역사적 이력/새 metadata mapping/현재 실행 증거를 구분한다. C3–C5는 미완료다.
S3.6/7의 미래 인간 입력은 해당 단계에 plan 창구에서 처리한다. 새 제품 업무·runtime 변경·
배포 main·개인 설치 변경은 없다. 이 인계는 실제 다음 역할 행동이며 S4 시험 자체의 PASS가 아니다.
