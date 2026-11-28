# P011 공식 Claude 기능을 통한 전달 연결

2026-11-28 · Common key: `P011-official-claude-relay`.
연결된 기존 key: `P010-session-registration-reconnect`.

## 목적과 실제 승인

사용자는 “Codex에서 Claude로 작업을 전달할 수 있는 공식 지원 방식 찾아서 하네스에
연결해줘. 매번 내가 터미널에 입력하지 않아도 되게 하고 싶어”라고 요청했다.
이 요청은 기존 P010의 cross-host bridge 제외 범위에 대한 새 구현 승인이다.
P011을 통해 제한된 relay를 추가하며 P010 과거 실패나 완료 조건을 소급 변경하지 않는다.

목표 흐름은 Codex의 승인된 exact handoff → 짧은 전달 전용 Claude CLI → 기존 Claude
역할 세션의 native 수신 → 해당 역할의 기존 계약 수행이다. Plan은 발송 후 복귀하고 dev는
독립적으로 일한다. 매번 사용자가 입력하거나 dev에서 다시 채택할 필요가 없어야 한다.

기술 기준은 P010 source `e044e3e7f11ef48d4f9cc4fa41cad7ac00d8e1c8`(0.2.5)다.
후행 dev 증거/작업을 보존하며 다음 소스/설치 버전은 0.2.6이다. 공개 main/tag0.2.3,
0.2.5 역사 검증, P009/P010 미완료 조건은 그대로다. 정식 릴리스 권한은 없다.

## W1 — 공식 근거와 지원 확인

조사 시 로컬 Claude Code 2.1.332의 help는 `-p`, `--tools`, `--allowedTools`,
`--permission-prompts`, `--output-format`, `--max-budget-usd` 등을 제공한다.
실행 중인 interactive 세션에 직접 보내는 `claude send` 명령은 확인되지 않았다.
공식 문서의 SDK streaming은 애플리케이션이 소유한 세션의 입력 경로이며, 임의로 이미 열린
interactive 세션을 점유하는 근거가 아니다. live writer를 resume/fork로 복제하지 않는다.

선택 경로는 공식 CLI non-interactive 실행과 native ListAgents/SendMessage의 조합이다.
공식 문서상 idle receiver는 전달된 메시지로 턴을 시작하며 수신 제한/권한은 별도로 적용된다.
이 조합의 실제 로컬 작동은 아직 미검증이므로 기능 probe와 live 검증 전 지원 완료를 쓰지 않는다.

공식 자료(2026-11-28 확인):

- [Programmatic CLI](https://code.claude.com/docs/en/headless)
- [Cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging)
- [CLI reference](https://code.claude.com/docs/en/cli-reference)
- [SDK streaming input](https://code.claude.com/docs/en/agent-sdk/streaming-vs-single-mode)

구현 시작 시 실제 CLI 버전/help/native 도구 유무를 다시 확인한다. 최신 문서의 옵션을
설치 CLI에 있다고 가정하지 않는다. 링크된 커뮤니티 issue의 제안 명령은 공식 기능이 아니다.
문서화된 inbox 설명만으로 wire payload를 추측하거나 raw socket 프로토콜을 역공학하지 않는다.

## W2 — 제한된 전달 프로세스

한 승인 인계당 짧은 `claude -p` relay 하나를 실행하는 adapter를 기본으로 구현한다.
이는 제품/fixture writer나 사용자 소유 채팅이 아니다. 프로젝트 밖 private scratch cwd를 쓰고
plan/dev 역할 등록 hook을 실행하거나 해당 역할 registry를 차지하지 않는다.
사용자의 기존 로그인/모델 설정을 존중하며 새 계정/토큰/결제 수단은 만들지 않는다.

노출 도구는 필요한 ListAgents/SendMessage로 제한한다. `--allowedTools`만으로 도구 목록이
제한된다고 착각하지 말고 `--tools`와 MCP 차단/명시 구성 등 실제 지원 옵션을 검증한다.
relay는 파일 읽기/쓰기, Bash, Agent, browser, 외부 MCP 업무를 수행하지 않는다.
중계 prompt는 전달 지침·정확 목표·승인된 메시지만 포함하고 수신자의 대화/개인 설정은 읽지 않는다.
상속 hook/plugin이 별도 효과를 내지 않도록 격리 방법과 보존되는 조직 정책을 검증한다.
`--bare`가 필요한 메시징을 끄는 등의 조합은 사용하지 않는다. 설정 격리가 기존 deny 정책을
제거하는 결과가 되면 사용할 수 없다. 실제 거부된 작업을 새 sender로 우회하지 않는다.

한 번의 ListAgents 결과에서 정확 대상만 골라 한 번의 SendMessage로 전달한다.
다른 세션 이름/메시지 내용은 지시가 아니라 식별 자료다. target/full message/key/hash 검증과
추가 send 방지의 구현 방식을 명시한다. 프롬프트만을 결정적 보안 경계라고 표현하지 않는다.
공식 SDK의 tool callback 등 더 강한 제한이 필요하면 최소 SDK 의존성의 이유와 버전을
기록해 사용할 수 있다. 별도 상주 service나 새 역할 worker로 확대하지 않는다.

전송은 shell=False argv와 stdin 또는 private message file을 사용한다. 문자열 보간 shell,
전역 credential 출력/커밋을 금지한다. 로컬 private 출력/영수증에만 raw ID를 두고 공개 증거는
가명화한다. 모델 최종 응답만으로 발송을 판정하지 않고 실제 native tool call/result를 파싱한다.
내용 변형/다른 target/추가 tool call이면 성공으로 기록하지 않고 실제 발생 결과를 보존한다.

기본 relay 호출의 wall timeout은 60초, 추정 비용 한도는 USD 1 이내로 두고 설정으로 낮출 수
있게 한다. 공식 비용 cap은 정확 청구 상한 보장이 아님을 문서화한다. 사용량/시간/실제 종료
사유를 남긴다. 무한 재시도/연쇄 reply/완료 감시 프로세스는 만들지 않는다.
timeout은 시작한 relay만 정리하며 수신 worker를 종료하지 않는다. 그 전에 전송됐을 가능성이
있으면 UNKNOWN으로 남기고 같은 메시지를 자동 재발송하지 않는다.

## W3 — identity와 장시간 idle의 재확인

기존 등록부의 project/common-dir/worktree/role/host/session/generation과 공식 inventory,
native listing을 교차 확인한다. UUID를 native address로 임의 변환하지 않는다.
고유한 실제 native recipient와 등록 identity를 연결할 수 없으면 전송하지 않는다.
같은 이름/여러 writer/다른 clone/host/cwd/branch/세대 변경은 보류한다.

P010에서 실제 idle session의 lifecycle timestamp만 오래돼 인계가 막힌 상황을 보존한다.
P011은 timestamp를 쓰거나 TTL 제한을 삭제하지 않고 별도 fresh host proof 경로를 구현한다:
동일 살아 있는 ID/세대/역할/cwd의 유일한 host 관찰(30초 이내) 및 충돌 없음이 확인되고
기존 상태가 idle 또는 busy이며 다른 제어 조건이 모두 통과할 때에만 이번 전송의 liveness
증거로 쓴다. 종료/unknown/새 identity takeover 또는 role 변경에는 이 경로를 사용할 수 없다.
보낸 직전 controls/identity를 다시 검사하고 근거 종류를 명시한다. 읽기 전용 doctor는 그대로
읽기 전용이며 stale lifecycle와 fresh host proof를 분리 표시한다.

## W4 — 권한·큐·정확 인계 연동

기본 전송 대상은 기존 승인된 같은 프로젝트의 plan/dev다. 부모 observer와 격리 fixture처럼
서로 다른 Git 프로젝트 간 전송은 현재 P011/P010의 명시적 fixture 검증 grant만 별도 매핑으로
허용하며 일반 설정에 전체 프로젝트 허용을 넣지 않는다. 설치만으로 messaging grant가 생기지 않는다.

제품 작업은 기존 READY P/exact reviewed SHA/승인 근거/committed handoff를 사용한다.
이미 승인된 작업의 계속 신호는 그 문서/hash/key/기존 인간 응답을 연결하고 새 업무나
실제 인간 입력으로 위장하지 않는다. receiver가 따라야 할 인계는 기존 역할 그대로다.
peer 메시지는 권한 승인, CLAUDE.md/권한 설정 변경, 사람의 중지 재개를 대신하지 않는다.
전송 전에 scoped pause/OPEN/current writer를 확인하고 busy 업무를 유지한다.
사용자 판단/권한 요청은 기존 plan 단일 창구로 보내며 routine 채택 질문은 하지 않는다.

수신 `crossSessionInbound`/managed policy/permission hold/refuse를 유지한다. sender를
bypass 모드로 바꾸거나 target 설정을 넓혀 통과시키지 않는다. 필요할 때만 실제 차단 내용을
plan에 한 번 전달한다. UI 도구의 iTerm 접근 차단과 무관한 공식 messaging API를 쓰는 것이며
거부된 UI 동작/권한 작업을 Claude에게 대리 요청하지 않는다.

발송 전 attempt/key/payload hash를 원자적으로 기록한다. 중복 프로세스/같은 key를 막고
prepared/attempted/held/refused/unknown/delivered/received/applied/completed를 구분한다.
기존 PENDING/SENT/ACK schema와 의미를 유지한다. 실제 tool result와 receiver 입력 증거를
분리하며 CLI exit 0이나 송신 모델의 요약만으로 SENT/ACK를 올리지 않는다.
호출자는 전달 결과를 기록하고 반환한다. dev 완료를 기다리는 경로가 아니다.

## W5 — 실제 환경 적용 범위

먼저 별도 격리 검증에서 target pinning/tool restriction/권한·중복 경계를 통과시킨다.
그 뒤 현재 사용자가 지정한 기존 P010 Claude fixture plan에 한 번의 bounded continue
메시지를 보낼 수 있다. 해당 로컬 ID/경로는 기존 사용자 입력과 실제 host로 다시 확인한다.
메시지는 기존 `P010-LIVE.md` 첫 P901 계획·정확 인계 계속만 요청하며 새 P/새 scope를 추가하지 않는다.
수신자로부터 답신으로 권한을 넓히거나 부모에게 임의 업무를 실행시키지 않는다.

이 제한된 relay 생성/실행은 최신 사용자의 공식 연결 요청에 따른 P011 범위다. P010에서
금지한 경쟁 역할 worker 생성과 구분한다. 기존 두 interactive 세션을 닫거나 resume/fork/
재시작하지 않고 fixture runtime을 덮어쓰지 않는다. 필요하면 검증된 source adapter가 외부에서
기존 registration/queue를 읽어 발송하며 적용 버전·sender 역할을 증거에 남긴다.
P010 fixture 첫 작업이 끝난 뒤 그 runbook의 다음 단계만 진행한다. 인간의 정상 interactive
재시작이 별도 필요하면 정확 행동을 plan에 요청하되 발송마다 터미널 입력은 요구하지 않는다.

두 번째 공식 인계도 사람의 반복 전송 입력 없이 보내 수신을 검증한다. 실제 작업/증거가
이미 존재하면 다시 구현시키지 않는다. 불명확한 수신이나 중복 키에는 blind retry를 하지 않는다.
P011 성공이 P010의 전체 C3(특히 Codex 두 세션 시험)를 자동으로 충족하지 않는다.

## W6 — 설치형과 검증

소스 VERSION/SKILL/assets/runtime/installer payload/안내를 0.2.6으로 정합화한다.
source0.2.5→0.2.6 격리 업그레이드, preview 무변경, apply/KEEP, 사용자 수정 충돌 보존을
검증한다. receiver 사용법에는 최초 구성, 반복 전달 자동화, 공식 권한 요청이 남을 수 있는
조건, relay 모델 호출 비용과 limits를 구분한다. 개인 전역 설치/다른 프로젝트 일괄 갱신은 없다.
부모의 보호된 설치 runtime/policy를 임의 변경하지 않는다. 변경 필요 시 정확 안을 plan에 인계한다.

필수 검증:

- 실제 도구 부재/잘못된 옵션/인증 오류/권한 거부를 전달 성공과 구분.
- 고유 target, 중복 이름, 다른 프로젝트, 바뀐 generation, 종료/unknown, fresh proof 만료.
- idle/busy 전달, 수신 hold/refuse, scoped stops/OPEN, 현재 P와 안전한 적용 경계.
- shell 메타문자/유니코드 메시지 보존, 잘못된 tool call/내용 변형, 비용/시간/출력 크기 상한.
- 동시 같은 key, crash before/after send, ambiguous 결과, 재시도 중복 차단.
- 실제 CLI→native send→receiver 입력→기존 역할 실행 및 두 번째 인계; 합성 mock과 분리.
- 전체 unittest, 설치 payload/독립 CLI/업그레이드, guard/queue, private 정보 유출 검사.

현재 기준 105 tests 위에 필요한 의미 있는 테스트를 추가한다. 미지원 live 항목은 NOTRUN/
BLOCKED로 남기며 증거 없이 체크하지 않는다. 새 단계마다 같은 사용자 입력을 반복 요구하는
절차로 자동 전달 구현을 대체하지 않는다.

## W7 — 결과와 한계 인계

정확 source SHA, 공식 기능/설치 CLI 버전, 실행 argv의 비밀 없는 요약, tool 제한 검증,
전달/수신 증거, 사용량/시간, 모든 실패·한계, manifest/hash를 `docs/verification/P011/`에
커밋한다. 기존 dev→plan grant와 공통 key로 결과/필요 결정을 보낸다. ACK/완료 대기 루프는 없다.
계획 준비/실제 구현/설치형 반영/live 전달/공개 릴리스를 각각 구분해서 보고한다.
