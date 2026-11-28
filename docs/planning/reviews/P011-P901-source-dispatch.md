# P011 기존 P901 이벤트의 source adapter 전달 — 2026-11-28

Common key `P011-official-claude-relay`, linked `P010-session-registration-reconnect`.
기존 인간 승인 안에서 정확 준비 이벤트의 transport만 연결하는 결정이다.

결과 `cba471c9484511eb412c6544e4cc8d00fdfbd706`의 report를 읽고 manifest SHA256
`0e2fc9dba487ed17715d2660dcbe663bb9bfeb18912e4e228c8dd1d000ef7b78` 및 5개 artifact
hash를 재검산했다. Source `cb5b529d082c204325b0222f02c5b24a1cf5f275`의 113tests와
34설치검사, 519byte 정확 실시간 수신 및 같은 msg_id의 실제 refuse 통지를 구분한 증거를
확인했다. Stage A의 검증 범위를 인정한다. Sender deny는 이전의 도구 노출 거부 범위다.

B의 기존 fixture plan 실제 peer input/body/id 일치와 새 턴·P901 계획 작성이 확인됐다.
이는 Codex→기존 Claude plan의 실제 전달 성공이다. P901 plan→dev와 구현 완료는 별도다.
Parent plan의 읽기 전용 확인에서 fixture plan HEAD는
`9975ce8cefbbcf1bbed9319a1d994ee3845197ec`, clean이었다. 아래 이벤트는 PENDING이다:

- 이벤트: `docs/progress/handoffs/plan/f1f4e6df11271e771c44423b967c2cca04f96d028c1a807a2a8058ae6cec3423.json`
- 작성 커밋: `69d2de4ea1e6c6384f5bea4521de5f6d07dfeca3`
- 정확 검토/채택 대상: `057ecbc4ca8ae0c4cb5d64fe1247afd4b7bccdf3`
- 문서: `docs/planning/reviews/P901-review.md`

기존 0.2.5 session_handoff 검사는 idle dev의 오래된 lifecycle 시각 때문에 native 전송 전에
보류됐다. 이것은 수신 권한 거부가 아니며 실제 사람 중지도 아니다. 검증된 0.2.6의 fresh host
proof 경로를 적용할 수 있지만 기존 시각을 수정하거나 guard를 끄지 않는다.

## 실행 결정

기존 parent dev는 위 이벤트의 transport operator로 source cb5b529 또는 그 범위 내 검증된
후행 source adapter를 외부에서 실행할 수 있다. repo/event는 기존 fixture plan을 정확히
지정하고 fresh host identity/세대/유일 writer/common-dir/role/branch·pause/OPEN/current
work·카드/문서/commit hash를 다시 확인한다. 역할 카드 작성/채택/제품 구현은 여전히 기존
fixture plan/dev 소유다. 부모는 fixture tracked 파일을 쓰지 않는다.

기존 이벤트가 아직 미발송이고 같은 key의 시도가 없을 때만 shared private ledger로 원자
예약하여 한 번 전달한다. 실제 plan이 이미 발송했거나 업무가 진행됐다면 재발송하지 않는다.
같은 logical key, exact commit, payload를 사용하며 이전 plan-continue key와 consumed
recovery는 재사용하지 않는다. 이번은 새로 준비된 P901 인계이고 실패 retry가 아니다.
원래 0.2.5 runtime/정책/설치/registry timestamp는 보존하고 source 실행 버전을 명시한다.

timeout/예산/공식 권한/중복·UNKNOWN 계약은 기존 P011 그대로다. native 결과와 fixture dev
peer input, 내부 exact 채택, marker 16byte·증거 commit을 각각 확인한다. 부모가 marker를
대신 작성하거나 사용자에게 dev 채택/계속 문장을 입력시키지 않는다.

전달된 경우 실제 receipt/hash를 기존 fixture plan에 한 번 알려 자신이 소유한 원래 이벤트의
SENT/실행 결과를 기록하게 할 수 있다. 이는 같은 작업의 transport 결과 동기화이며 routine
ACK loop가 아니다. 내용은 실제 증거와 중복 발송 금지에 한정한다. 지원 경로를 통해 전달하고
부모가 fixture plan 파일을 대신 수정하지 않는다. 이미 dev의 결과 패킷으로 충분한 증거가
도착하면 별도 중복 메시지를 보내지 않는다.

실제 수신 이후 기존 fixture dev의 결과 패킷/plan 검토를 보존한다. P010 재연결/후속 카드 및
Codex 두 세션 검증은 별도이며 P901 하나로 전체 완료를 선언하지 않는다. 이번 결정은 기존
interactive 종료/재시작이나 broad permission 변경을 허용하지 않는다.
기존 중지·작업·과거 실패·main/tag·개인 설치를 유지하고 실제 결과를 동일 key로 인계한다.
