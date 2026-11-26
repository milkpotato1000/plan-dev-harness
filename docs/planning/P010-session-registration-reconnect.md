# P010 세션 자동 등록·재연결 계약

2026-11-26 · 실행 승인: 실제 사용자 P010 기획·dev 인계·설치형 반영 요청.
공통 request key: `P010-session-registration-reconnect`.

## 목표와 기준선

처음 프로젝트를 구성할 때 역할과 폴더를 명시한다. 이후 사용자는 해당 역할 폴더에서
`claude` 또는 `codex`를 실행한다. 하네스가 공식 host에서 받은 실제 세션 식별자를 등록하고
상대 역할의 유효한 세션을 발견한다. 정상 재접속에는 세션 ID 복사나 dev 채택 재입력이 없다.
앱과 터미널은 같은 역할/승인/큐 계약을 쓰고 discovery와 transport만 host별로 구분한다.

기술 기준은 P009 소스 `4c4b5a3f2ef63deeffa425f49c2bc0161cf48d66`의 0.2.4다.
실제 dev의 후행 증거와 작업을 보존하여 구현하며 과거 커밋으로 reset하지 않는다.
P008은 완료된 선행이다. P009의 엄격 C3는 미충족 상태로 유지하며 P010을 위한 선행 완료로
위장하지 않는다. P010은 추가 기능으로 독립 진행하고 P009 시험을 재실행하지 않는다.

## W1 — 역할 설정과 프로젝트 식별

구성 진입 위치가 plan/dev 어느 쪽이어도 명시된 역할별 worktree 매핑을 읽고 같은 프로젝트로
연결할 수 있어야 한다. 설정은 사용자 요청에 따른 preview/apply 단계에서 확정한다.
기존 명시 인간 역할이 폴더/브랜치/채팅 이름 추정보다 우선한다. 앱의 두 채팅이 같은 부모
폴더를 공유할 수 있으므로 cwd만으로 역할을 정하지 않는다. 모호하면 진단 후 등록을 보류한다.

Git common-dir와 실제 worktree/branch를 교차 확인한다. 같은 basename, remote URL 또는
세션 표시명만으로 프로젝트·수신자를 식별하지 않는다. 다른 clone은 별개 프로젝트다.
역할 변경, worktree 이동, branch 변경, host identity 불일치는 자동 역할 전환 근거가 아니다.
명시 설정이나 검증된 갱신 절차가 없으면 기존 binding을 전송에 사용하지 않는다.

공유 등록부는 해당 Git common-dir의 전용 로컬 디렉터리 등 안전한 프로젝트 전용 위치에 둔다.
위치·schema·권한·최대 크기·보존/정리 규칙을 문서화하고 Git 추적에서 제외한다.
필드는 프로젝트/역할/host namespace/실제 세션 ID/정규화 경로/세대/관찰 시각/능력/등록 출처를
최소한으로 보유한다. 토큰·자격증명·대화·명령 원문을 수집하지 않는다.
로컬 등록부는 연결 관찰 자료이며 실행 승인이나 상대 권한의 증명서가 아니다.

## W2 — lifecycle와 재연결

공식 SessionStart 또는 검증된 host 진입점으로 실제 session_id/cwd를 받는다.
지원되는 활동/종료 이벤트로 갱신·정리하고 외부 상주 daemon이나 모니터를 만들지 않는다.
시작은 등록과 진단만 수행한다. 제품 작업 시작, 자동 새 P 생성, 승인, peer 발송, 중지 재개는
수행하지 않는다. 등록 실패도 사용자 CLI를 무한 대기시키지 않도록 시간/출력 상한을 둔다.

같은 identity의 반복 시작은 idempotent하게 처리한다. 새 identity로 재접속할 때는 이전
세션의 종료/무효 여부와 writer 소유권을 확인한 뒤 새 세대로 연결한다. 살아 있는 동일 역할
세션 둘, busy/unknown, 검증 불가능한 소유권은 충돌로 표시한다. 단순 TTL 만료나 마지막
쓰기 승리가 takeover 권한이 되어서는 안 된다. 필요하면 plan에서 한 번만 소유권 판단을 받는다.

동시 등록에는 잠금과 원자적 저장, 세대별 비교 갱신을 적용한다. 이전 세션의 늦은 종료가
새 세션을 지우지 않아야 한다. 비정상 종료, 잠금 잔재, 깨진 JSON, 시계 역행/미래 시각,
부분 쓰기, 잘못된 필드를 안전하게 처리한다. 등록 경로/입력을 shell 코드로 실행하지 않는다.

상대가 아직 없으면 pending으로 남는다. 상대 시작 후 다음 정상 조회/전달 시 발견한다.
Plan은 상대 시작이나 dev 완료를 기다리지 않는다. 재연결은 P/결정/중지 기록을 변경하지 않는다.

## W3 — host adapter와 실제 전달

Claude는 설치된 버전의 공식 hook, inventory와 native ListAgents/SendMessage 능력을
확인한다. native 목록의 cwd 부재를 가정할 수 있으므로 등록부와 실제 Git/host identity를
교차 확인한다. 이름 검색 하나만으로 다른 세션에 작업을 보내지 않는다.

Codex는 공식 lifecycle hook과 해당 환경의 기존 app thread 도구 또는 공식 CLI queue 경로를
사용한다. 앱 도구가 CLI에도 있다고 가정하지 않는다. 설치된 `--help`와 실제 host 능력을
검사하고 지원하지 않는 옵션은 호출하지 않는다. queue 접수, recipient 입력, 턴 시작,
내부 적용, 실행 완료를 각각 구분한다. 큐 저장만으로 상대가 깨어나 실행했다고 주장하지 않는다.

같은 host의 plan/dev 연결을 필수 지원 대상으로 삼는다. Claude↔Codex 교차 host는 공식
transport가 실제 확인된 경우만 지원하며 이번 범위에 새 bridge 개발은 없다. 연결할 수 없으면
등록/발견 가능 여부와 전달 불가 이유를 분리해 pending으로 표시한다. 세션 ID 수동 복사를
정상 경로로 되돌리거나 plan의 순차 구현을 fallback으로 삼지 않는다.

실제 전달은 기존 reviewed exact SHA/P 승인·위임을 재확인한 후 수행한다. busy dev는 현재
P를 보존하고 안전한 완료/checkpoint 경계에서 다음 정확 인계를 적용한다. 전송 불명은 재시도
전에 공통 key로 중복 여부를 확인한다. PENDING/SENT/ACK와 기존 guard/adoption 계약을 유지한다.
진단과 queue 조회는 읽기 전용이다. 진단 실행만으로 hook 설치/등록/발송을 하지 않는다.

raw socket 우회, iTerm 키 주입, broad inbound 허용, trust/권한 대리 승인, 무단 동시 resume,
새 worker 자동 생성은 금지한다. 최초 host trust 등 실제 사람에게 요구되는 항목은 정확한
폴더/설정/최소 행동을 plan에 한 번 전달하고 해결된 질문을 반복하지 않는다.

## W4 — 설치형과 운영 문서

소스 VERSION은 0.2.5로 올리고 SKILL, assets/runtime/templates/references, installer,
README/설치 안내/변경 이력/manifest의 실제 범위를 일치시킨다. 설치형은 SKILL+CLI 배포이며
검증 없이 marketplace plugin으로 표기하지 않는다. 기능 최소 버전과 unsupported 동작을 명시한다.

역할별 프로젝트 로컬 Claude/Codex 설정에 공식 hook을 구성하는 preview/apply를 제공한다.
기존 hook/config/알 수 없는 사용자 필드/권한 설정을 보존하고 하네스 소유 항목만 추가·갱신한다.
중복 선언/중복 실행을 막고 재실행은 KEEP이어야 한다. 충돌·쓰기 실패에는 부분 구성을
정상 완료로 처리하지 않는다. 롤백은 이번 작업이 생성한 파일/항목에 한정한다.
host trust나 허용 목록을 자동 확대하지 않는다. 실제 CLI 실행과 같은 작업 폴더에서
프로젝트 hook을 읽는지 검증하고 hook의 경로 공백/유니코드/작업 디렉터리 차이를 처리한다.

배포 source 변경과 이 저장소의 이미 설치된 runtime 갱신을 구분한다. 이번 구현은 배포 source,
설치 코드 및 격리 target에 적용한다. 현재 plan/dev 보호 runtime/policy·사용자 전역 설치·기존
다른 프로젝트의 일괄 변경은 하지 않는다. 보호된 운영 파일 변경이 꼭 필요하면 정확 변경안을
plan으로 인계한다. main/tag/release와 0.2.3 공개 설치 기준선은 변경하지 않는다.

## W5 — 보존과 격리 시험

기존 P002~P009, 중지·OPEN 결정·adoption·인계 기록·실패 증거를 byte 보존한다.
기존 harness-test/P009 폴더와 두 interactive 세션은 종료/재시작/설정 갱신 대상이 아니다.
새 P010 fixture는 이 저장소 dev 내부의 Git 미추적 격리 작업 영역 또는 임시 폴더에 준비한다.
테스트용 별도 Git 저장소/worktree/설정은 명확히 한정하고 사용자 전역 설정을 변경하지 않는다.

단위/통합 시험은 stdlib를 기본으로 하고 공식 host 기능을 통해 격리 시험 세션을 구성한다.
새 사용자 소유 Codex 채팅 생성은 하지 않는다. 실제 interactive 시작이나 trust가 필요하면
실행 가능한 폴더/명령/역할 입력을 먼저 준비하고 plan에 최소한의 입력만 요청한다.
자동으로 마련할 수 있는 증거/코드/검증을 먼저 완료한다. 실제 사람 입력의 정확한 타이밍을
추가 완료 조건으로 만들지 않는다. 기존 실제 세션의 중지/재시작을 시험에 이용하지 않는다.

## W6 — 검증 매트릭스

| ID | 필수 검증과 증거 |
| --- | --- |
| M1 | plan 먼저/dev 먼저 시작, 상대 미존재 후 등장, 실제 ID 자동 등록 및 프로젝트/역할 정확성 |
| M2 | 같은 ID resume, 새 ID 재시작, 과거 종료 이벤트, crash/stale/unknown, 동시 동일 역할 충돌과 단일 writer 보존 |
| M3 | 다른 clone/host/branch/cwd/역할 불일치, 이름 중복, 손상/악성 입력, 원자성·잠금 실패·시간 이상 |
| M4 | 역할/업무/프로젝트 중지와 OPEN 결정을 가진 fixture에서 등록/재연결/결정 해결 후에도 명시 재개 없이는 실행 금지; busy 현재 P 보존 |
| M5 | 실제 Claude 두 세션, 실제 Codex 두 세션에서 raw CLI 시작→자동 등록→정확 인계→재연결 후 다음 인계; ID 수동 복사 없음; 앱의 기존 exact handoff 회귀 |
| M6 | preview 무변경, fresh apply, 재실행 KEEP, 실제 0.2.4→0.2.5 업그레이드, 기존 custom hook/config/작업/중지 보존, 충돌/부분 실패 안전성 |
| M7 | 전체 unittest, guard/queue, 독립 설치된 CLI, package 파일/버전 일치, Git 내 private ID/토큰/개인 경로 유출 검사 |

모의 stdin/schema 시험과 실제 host 증거를 구별한다. M5는 host 버전, 시작 이벤트 출처,
가명화된 세대 전후 identity, 실제 전송/수신/내부 적용 결과를 남긴다. 등록만 된 상태나
지원되지 않는 transport는 live PASS가 아니다. 필요한 공식 능력이 없으면 해당 C를 미완료로
두고 구체적 제한과 가능한 후속안을 plan에 전달한다. 플랫폼 제약을 숨기기 위한 기준 완화,
새 프로세스 무한 증식, sleep으로 만든 가짜 병렬 실행은 하지 않는다.

## W7 — 결과 인계

정확 source SHA, 검증 환경·명령·성공/실패/NOTRUN, 설치 manifest/hash, 실제 host 범위와
보존 확인을 `docs/verification/P010/`에 커밋한다. 원시 식별자는 공개하지 않고 재현 가능한
가명화 export와 hash를 사용한다. 검증하지 못한 플랫폼/회사 정책은 지원 완료로 쓰지 않는다.
기존 dev→plan 위임과 공통 key로 결과/필요 결정 한 번을 전달한다. 사용자에게 dev 채택이나
중복 결과 확인을 요청하지 않는다. Plan은 이번 exact handoff의 실제 SENT 후 대기 없이 복귀한다.

## 공식 근거와 구현 시 재확인

2026-11-26 로컬 관찰은 Claude 2.1.332 / Codex 0.160.1이다. 공식 문서의 최신 옵션이
로컬 help에 없을 수 있다. 예를 들어 Codex queue의 `--resume` 지원을 가정하지 않는다.

- [Claude hooks](https://code.claude.com/docs/en/hooks): lifecycle 입력과 설정 범위.
- [Claude cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging): 공식 peer transport와 수신 제한.
- [Codex hooks](https://learn.chatgpt.com/docs/hooks): lifecycle hook의 실제 제공 범위.
- [Codex advanced config](https://learn.chatgpt.com/docs/config-file/config-advanced): 프로젝트 hook 설정과 trust.
- [Codex developer commands](https://learn.chatgpt.com/docs/developer-commands): queue/agents 등 공식 CLI 경로.
