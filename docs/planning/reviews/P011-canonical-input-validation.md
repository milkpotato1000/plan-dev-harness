# P011 공식 입력 교체 검증과 조건부 실제 전달 — 2026-11-28

Common key `P011-official-claude-relay`. 기존 실제 인간의 공식 연결 구현 승인 안에서
격리 진단 결과를 반영한 기술 결정이다. 이전 실패/unknown/소비된 recovery는 보존한다.

## 검토

결과 `75c85d4cbdb0d1aba6b654ea687ea08e4af7ab76`의 report/probes를 읽고 manifest
SHA256 `730b838b58a93c5a60a14051167134d2b85257e4cc7083912ae0974220d1cc40`와 두
artifact hash를 Git blob에서 재검산했다. 두 합성 호출의 streamed JSON에는 to/summary/message
세 필드만 있고 조립된 ToolUseBlock과 PreToolUse에는 추가 별칭/content가 나타난다.
두 입력의 길이가 달라도 보존되는 본문은 정확하며 preview 길이는 다르다. 이 관찰은
내부 변환 함수나 과거 실제 content 값 또는 수신 바이트를 확정하지 않는다.

[공식 PreToolUse 문서](https://code.claude.com/docs/en/hooks#pretooluse-decision-control)는
updatedInput이 전체 입력을 교체하고 교체된 입력에 권한 평가를 적용한다고 설명한다.
permissionDecision 없는 교체는 권한 허가가 아니다. 이를 이용한 아래 단계적 검증을 승인한다.
지원되지 않는 옵션/콜백 의미를 추측하거나 권한 거부를 allow로 덮어쓰지 않는다.

## A — 구현 및 통제된 수신 검증

정확 예약된 to/summary/message만으로 canonical 입력을 재구성한다. Stream의 완전한
tool-use ID와 callback ID를 상관검증하고 full UTF-8 message hash/대상/summary를 확인한다.
JSON 중복 키·추가 streamed 필드·비문자열·ID 불일치·누락/미완성/다중 호출은 거부한다.
조립된 입력의 원래 세 필드와 recipient alias는 일치해야 하고, 알 수 없는 필드/모순되는
type/recipient_kind는 거부한다. content는 문서화된 canonical payload로 간주하지 않는다.
관찰된 내부 추가 필드만 제거해 예약된 세 필드로 교체하며, 임의 입력을 검증 없이 고쳐 보내지 않는다.
임의 preview 패턴 허용이나 prefix 알고리즘 추측은 하지 않는다.

콜백은 updatedInput만 반환하고 permissionDecision=allow/updatedPermissions를 넣지 않는다.
통상 정책·조직 deny·수신 inbound가 유지돼야 한다. 메시지 전송/본문이 권한 거부된 경우
mode/settings를 바꿔 성공시키지 않는다. Stream과 callback 상관검증을 SDK 실행 순서상
실현할 수 없으면 timeout/deny로 끝내고 지원 한계를 인계한다.

실제 P010 역할과 격리된 중립 SDK 시험 receiver 하나를 사용할 수 있다. 이는 합성 메시지를
받고 수신 바이트를 검증하는 프로세스이며 role writer/제품 작업자/새 사용자 소유 채팅이 아니다.
receiver는 도구/프로젝트 hook/MCP 업무 없이 실행하고 테스트 종료 시 자신이 만든 프로세스만
정리한다. 기존 세션 ID나 원래 handoff를 쓰지 않는다. SendMessage/listing도 이 시험 receiver로
한정하고 다른 세션을 조사/접촉하지 않는다. 최초 권한/로그인 차단은 우회하지 않는다.

실제 수신 입력 이벤트의 bytes/hash를 독립 관찰해 ASCII·한글/줄바꿈·긴 본문이 정확함을
확인한다. 모델이 재작성한 echo/요약만으로 byte 일치를 주장하지 않는다. 권한 deny/수신 거부,
악성 alias/본문 잘림/잘못된 target/추가 호출은 native 발송 전 또는 공식 정책에서 차단돼야 한다.
최대 6개의 합성 발송/정책 probe, 각 sender 60초/0.50USD 이하, receiver 전체 수명 10분 및
추정비용1USD 이하로 제한한다. 허용한 총량 안에서도 원인이 드러나면 불필요한 반복을 중단한다.
SDK 테스트를 위해 기존 user/global settings를 바꾸지 않는다. 코드·단위·최종전체회귀·설치
영향 검증과 증거를 먼저 완료한다.

## B — A 통과 후 한 번의 기존 작업 전달

A의 실제 바이트 일치와 권한 보존이 모두 증명되고, 원래 live와 소비된 recovery 모두에 대해
미허용 callback/다른 실행 없음/sender 종료/수신 없음이 다시 확인되는 경우에만 허용한다.
그 외에는 B를 실행하지 않는다. Receiver echo만의 주장, 정책 우회, 새 identity takeover는
통과 근거가 아니다. 최종 구현 source/hash와 A 증거/hash를 예약 기록에 연결한다.

같은 원래 logical key/정확 대상/전체 payloadhash를 유지한 validation-recovery 1회를
이 정확 reviewed SHA에 묶어 원자적으로 소비한다. 기존 ledger/첫 recovery 파일은 불변으로
보존하고 별도 새 시도 기록만 추가한다. 이미 성공/held/refused/실행 후 unknown인 시도에는
사용할 수 없다. 이 승인도 소비 후 자동 retry할 수 없다. 기존 generic dedup을 끄지 않는다.

현재 기존 P010 fixture의 실제 writer/등록/공식 identity·권한·중지/OPEN·현재 작업을 발송
직전 확인한다. 이미 첫 P가 진행/완료됐으면 중복 작업 지시 대신 상태만 기록한다.
조건이 맞으면 기존 runbook 첫 P901 계속 메시지를 공식 adapter로 보내고 수신/실제 계획·
정확 dev 인계를 검증한다. 첫 업무 완료 후 원래 승인된 두 번째 전달도 검증할 수 있다.
기존 fixture runtime/설정/세션 종료·재시작을 변경하지 않는다. P010 Codex 시험 등 전체
완료를 소급 주장하지 않는다. 사람의 반복 터미널 입력이나 추가 재승인 질문은 필요 없다.

단계별 실제 PASS/FAIL/NOTRUN·source·trace/hash·권한 확인·기존기록 불변을 같은 key로
plan에 인계한다. 어떤 실패도 지우거나 실제 수신 성공으로 둔갑시키지 않는다.
P009/P010 미완료·기존 중지·main/tag0.2.3·개인 설치 보존 및 릴리스 미승인은 그대로다.
