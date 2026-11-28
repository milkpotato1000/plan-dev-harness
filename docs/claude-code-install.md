# 회사 Claude Code에 plan-dev-harness 0.2.3 설치

이 안내는 2026-11-24 배포 `v0.2.3`을 고정해 설치합니다.
[정식 릴리스](https://github.com/milkpotato1000/plan-dev-harness/releases/tag/v0.2.3) ·
[태그 소스](https://github.com/milkpotato1000/plan-dev-harness/tree/v0.2.3).
배포 형식은 **공통 SKILL.md와 Python CLI**이며 marketplace 플러그인이 아닙니다.
`/plugin install`, MCP 서버 등록이나 별도 GitHub 토큰이 필요한 설치가 아닙니다.

## 준비

Python 3.9 이상, Git 2.31 이상, POSIX shell과 GitHub HTTPS 접근이 필요합니다.
Claude Code는 회사에서 허용한 방법으로 설치·로그인되어 있어야 합니다.

```sh
python3 --version
git --version
```

개인 스킬은 `~/.claude/skills/plan-dev-harness/`, 프로젝트 스킬은 해당 프로젝트의
`.claude/skills/plan-dev-harness/`에서 읽힙니다. `/plan-dev-harness`로 직접 요청할 수
있습니다. 이 경로와 호출 방식은 [Claude Code 공식 skills 문서](https://code.claude.com/docs/en/skills)를 따릅니다.
같은 이름의 개인·프로젝트 스킬이 이미 있다면 실제 로드 경로를 먼저 확인하세요.

## 개인 범위 설치: 기본 경로

아래 clone 목적지는 **없어야** 합니다. 이미 있으면 내용을 확인하고 다른 새 경로를 사용하세요.
이 명령은 실제 회사 프로젝트를 생성하거나 기존 프로젝트의 작업·중지 상태를 변경하지 않습니다.

```sh
mkdir -p "$HOME/tools"
git clone --branch v0.2.3 --single-branch \
  https://github.com/milkpotato1000/plan-dev-harness.git \
  "$HOME/tools/plan-dev-harness-v0.2.3"
cd "$HOME/tools/plan-dev-harness-v0.2.3"

git describe --tags --exact-match
cat VERSION
python3 scripts/install_skill.py --agent claude
```

예상 버전은 `v0.2.3`과 `0.2.3`입니다. 마지막 명령은 **미리보기**이며 파일을 쓰지 않습니다.
출력의 `CREATE .../.claude/skills/plan-dev-harness` 목적지를 확인한 뒤 적용합니다.

```sh
python3 scripts/install_skill.py --agent claude --apply
cat "$HOME/.claude/skills/plan-dev-harness/VERSION"
test -f "$HOME/.claude/skills/plan-dev-harness/SKILL.md"
python3 "$HOME/.claude/skills/plan-dev-harness/scripts/bootstrap_workspace.py" --help
```

`VERSION`은 `0.2.3`, 도움말 명령은 exit 0이어야 합니다. 설치기는 스크립트·템플릿·참고 문서를
함께 복사하므로 소스 clone을 나중에 다른 위치로 옮겨도 설치 사본의 CLI를 사용할 수 있습니다.
같은 명령을 다시 적용하면 같은 파일 집합과 바이트인 경우 `KEEP identical skill`을 출력합니다.

새 Claude Code 세션을 열어 다음과 같이 요청합니다.

```text
/plan-dev-harness
현재 프로젝트의 역할·Git 상태·기존 지침을 읽기 전용으로 확인하고,
설치된 스킬 경로와 VERSION을 알려줘. 아직 bootstrap이나 기존 파일 변경은 하지 마.
```

파일 복사 확인과 실제 Claude의 스킬 로드는 별도입니다. 명령이 보이지 않으면 새 세션에서
실제 경로와 `SKILL.md`를 확인하고 회사의 스킬 허용 정책을 점검하세요. 정책을 우회하지 않습니다.

## 프로젝트 한정 설치

개인 범위 대신 프로젝트 범위로 설치할 때, 아래 경로를 실제 프로젝트 루트로 바꿉니다.
앞에서 clone한 소스 폴더에서 실행하며 모든 경로를 인용합니다.

```sh
python3 scripts/install_skill.py --agent claude \
  --skills-dir "/absolute/company project/.claude/skills"
python3 scripts/install_skill.py --agent claude \
  --skills-dir "/absolute/company project/.claude/skills" --apply
cat "/absolute/company project/.claude/skills/plan-dev-harness/VERSION"
```

이 작업은 선택한 스킬 디렉터리만 설치합니다. 프로젝트의 하네스 설치나 worktree 생성은
별도 작업입니다. 팀이 스킬 파일을 Git으로 공유할지는 해당 저장소의 정책에 따라 결정하세요.
이 안내만으로 다른 저장소에 커밋·push하거나 기존 작업을 업그레이드하지 않습니다.

## 기존 설치가 있거나 충돌할 때

| 출력/상태 | 의미와 다음 행동 |
| --- | --- |
| `KEEP identical skill` | 파일 집합과 내용이 같아 변경하지 않음 |
| `Existing skill differs` | 다른 버전·수정 파일·추가 파일이 있어 거절; 대상은 보존됨 |
| symlink 또는 파일인 목적지 | 안전하게 거절; 실제 경로·기존 설정 확인 |
| clone 목적지가 이미 존재 | 기존 clone을 삭제하지 말고 확인 후 새 목적지 선택 |

`install_skill.py`에는 `--upgrade`가 없습니다. 다른 설치를 발견하면 기존 사본과 확장을
백업하고 새 별도 디렉터리에 `--skills-dir`로 미리보기·설치·검증한 뒤, 실제 로드 경로를
검토해 전환하세요. 백업은 스킬 탐색 경로 밖에 보관하고 동시에 같은 이름의 활성 사본을
추가하지 않습니다. 무조건 삭제하거나 강제 덮어쓰는 명령은 사용하지 않습니다.
프로젝트 하네스의 `install_harness.py --upgrade`와 개인 스킬 설치는 다른 절차입니다.

## 설치 이후의 작업 흐름

새 프로젝트의 worktree 생성은 [README의 bootstrap](../README.md#빠른-시작-새-프로젝트),
기존 저장소 설치는 [통합·채택 절차](../references/usage.md)를 따릅니다. 설정된 역할,
한 worktree당 한 writer, 기존 작업과 명시적 중지·미해결 결정을 먼저 확인합니다.
스킬을 설치했다고 준비되지 않은 P카드를 실행하거나 중지를 해제하지 않습니다.

사용자 판단은 plan에서 모으고, dev는 검토된 정확 SHA를 내부적으로 통합·채택한 뒤 실행합니다.
승인된 같은 프로젝트 전달 도구가 있는 경우 사용자가 dev에 채택 문장을 다시 복사할 필요는
없습니다. 설치 자체는 채팅 간 발송 권한·도구·daemon을 만들지 않습니다. 회사 Claude Code에
그 기능이 없는 경우 커밋된 인계 문서와 파일 기반 절차를 사용하며 자동 발송을 보장하지 않습니다.

## 검증 범위

macOS에서 Python/Git CLI와 격리된 설치의 preview·apply·VERSION·독립 실행·KEEP·충돌 보존을
검증합니다. 릴리스 발행 후 공개 `v0.2.3` clone으로 같은 설치 경로를 다시 검증합니다.
Linux/WSL에는 같은 POSIX 절차를 안내하지만 이번 릴리스에서 직접 실행하지 않았습니다.
Native Windows, 실제 회사 Claude Code 로그인·조직 정책·실제 모델 대화는 미검증입니다.
회사 네트워크 차단이나 스킬 허용 여부를 설치 성공만으로 보장하지 않습니다.

[릴리스 변경·한계](releases/v0.2.3.md) · [프로젝트 검증 기록](verification/P008/README.md).

## 독립 worker 0.2.4 개발 소스 시험

위 정식 설치는 v0.2.3입니다. 0.2.4는 아직 발행하지 않았으며, 검토된 **전체 dev commit SHA**를
명시한 별도 clone에서만 시험합니다. 최신 dev tip을 승인된 계약처럼 자동 실행하지 않습니다.
새 목적지에 clone한 뒤 검토된 SHA를 checkout하고 VERSION과 source를 확인합니다.
프로젝트 로컬 `--skills-dir`에 preview/apply하며 개인 사본은 자동 갱신하지 않습니다.
[두 세션 시작·binding·native 전달·진단](../references/claude-workers.md)을 따르세요.
사용자가 plan에서 실행 승인하면 독립 dev는 내부 적용하며 다시 채택 입력을 받지 않습니다.
독립 worker/전송 도구 부재나 hold/refuse는 대기이고, 설정/승인을 우회하지 않습니다.

## 세션 자동 등록·재연결 — 0.2.5 개발 소스

정식 설치 기준은 **v0.2.3**입니다. 미발행 0.2.5 소스에는 프로젝트별 역할 설정,
공식 시작 hook을 통한 로컬 세션 등록, 상대 발견·보수적인 재연결이 추가됩니다.
[설정 절차와 host별 한계](../assets/docs/process/session-registration.md)를 확인하세요.

Runtime 설치·정확 통합 이후 먼저 미리봅니다.

```sh
python3 scripts/configure_sessions.py --plan /absolute/project_plan --dev /absolute/project_dev --role-reference "기존 사용자의 명시 역할 지정"
```

승인된 프로젝트에서만 `--apply`로 적용합니다. 이후 역할 폴더에서 일반 `claude`/`codex`를
시작하면 실제 ID를 hook이 받으므로 사람이 ID를 복사하지 않습니다. 등록은 작업 시작·승인·
중지 해제가 아닙니다. Host trust와 실제 두 세션의 전달·재연결 검증은 별도입니다.
Codex CLI 0.160.1에는 문서화된 JSON inventory와 queue resume이 없어 확인할 수 없는
재연결은 대기로 남깁니다. 기존 P009 fixture와 개인 설치는 이 소스 변경으로 갱신되지 않습니다.

## Codex에서 기존 Claude 세션으로 인계하기 (0.2.6 개발 소스)

등록한 두 역할과 커밋된 PENDING 인계가 있는 프로젝트에서 실행합니다.
전달 전용 Python 가상환경에 `claude-agent-sdk==0.2.189`를 설치하고 평소 사용하는
Claude CLI로 로그인합니다. 인계 문서의 실제 승인 근거를 지정합니다.

```sh
python scripts/claude_relay.py --repo . --event docs/progress/handoffs/plan/EVENT.json --authority-reference '검토 문서와 사용자 승인 위치'
```

중계는 모델을 한 번 실행하며 예산은 0.50 USD, 제한 시간은 60초입니다.
중복 키와 불명확한 결과는 수신 기록을 검토해야 합니다. 수신 세션의 hold 또는
refuse 정책이 적용됩니다. 현재 실제 환경에서는 도구 노출과 사전 거부를 확인했고
첫 P901의 수신과 후속 인계는 검증 중입니다.
