# P008 release 0.2.3 계약 — 2026-11-24

## 실제 승인과 배포 범위

이 plan 채팅의 실제 사용자 요청: “그럼 최신 0.2.3을 main에 반영하고 정식 릴리스까지
발행해줘. 회사 Claude Code에서 바로 설치할 수 있게 설치 안내도 정리해줘.”
이는 기존 공개 저장소 milkpotato1000/plan-dev-harness의 main 승격·정상 push,
v0.2.3 태그·정식 GitHub Release 발행을 승인한다. 같은 승인을 다시 묻지 않는다.
Plan은 기획·검토·정확 인계를 맡고 기존 dev가 문서 작성, 검증과 배포 실행을 맡는다.
기존 같은 프로젝트 결과/결정 인계 위임을 사용한다. 회사 계정 접근·정책 변경·다른 저장소
배포·기존 프로젝트 일괄 업그레이드·개인 설치 갱신·강제 push·태그 덮어쓰기는 제외한다.

## 확인한 출발점

- plan e419c6b, dev 332e8930f7a837144edbf56d8683c588354ceb06, main 803d658a8c61dc6aa007645a98d4160b16746faa. 모두 깨끗함.
- main은 현재 dev 조상, 공개 main/VERSION은 0.1.0, dev/VERSION은 0.2.3.
- 공개 저장소·default main, 기존 정식 릴리스 v0.1.0, v0.2.3 tag 조회는 404.
- P002~P007은 dev 기준 완료, 실행 가능한 기존 작업·OPEN 결정·유효 중지 없음.
- P002 5/5 및 최근 소스 전체 83 tests PASS. P002의 원래 임시 환경 소실·역사 버전 재구성
  한계와 실패/부정 검증 증거를 그대로 보존한다. 새 플랫폼/회사 환경 통과로 확대하지 않는다.
- 이 배포는 공통 SKILL.md + Python CLI 방식. Claude marketplace plugin manifest는 없음.
  로컬 설치형의 제품명과 실제 배포 형식을 구별한다.

## R1 — 사용자 설치 안내

README와 별도 회사 Claude Code 설치 안내(예: docs/claude-code-install.md)를 dev에서 작성한다.
공개 HTTPS clone에 --branch v0.2.3을 사용한 고정 설치 경로, Python/Git 요구사항,
scripts/install_skill.py --agent claude의 preview 후 --apply, 설치된 VERSION 0.2.3 확인,
새 Claude Code 세션의 /plan-dev-harness 사용까지 연결한다. 회사 사용자는 개인 범위
~/.claude/skills를 기본으로 사용하며 필요하면 명시적 --skills-dir로 프로젝트 범위를 선택한다.
명령은 공백 경로에서도 안전하게 인용한다. 기존 대상이 있으면 KEEP 또는 차이로 거절되는
현재 동작과 백업/비교 필요성을 안내하고 존재하지 않는 --upgrade 옵션을 제시하지 않는다.
정상 설치 시 별도 GitHub 토큰·MCP 연결은 필요 없음을 구별한다. Claude Code 계정/회사
정책은 별개이며 이 작업에서 확인하지 않은 조직 허용 상태를 보장하지 않는다.
macOS 실측과 Linux/WSL 절차·native Windows 미검증 범위를 구별한다.
설치는 프로젝트 bootstrap/마이그레이드와 별개이고 기존 작업/중지를 자동 변경하지 않는다.
Claude Code에서 실제 host 도구가 없는 세션 간 자동 발송까지 보장하지 않는다.
공식 참고: https://code.claude.com/docs/en/skills (personal/project skills, slash invocation).

## R2 — 일관된 릴리스 내용

VERSION과 배포 사본은 0.2.3을 유지한다. README·CHANGELOG·Release 본문에 0.1.0 이후의
결정/중지, 새 세션 역할, 비동기 plan/dev, plan 단일 검토 창구를 실제 구현에 맞춰 요약한다.
0.2.0/0.2.2/0.2.3 Unreleased와 누락된 0.2.1 표기를 확인하여 누적 정식 배포를 명확히 한다.
발행하지 않은 중간 버전의 과거 GitHub Release가 있었다고 꾸미지 않는다.
사용자 기준 배포일은 2026-11-24 (Asia/Seoul). 호스트 시계가 다르면 명시적 날짜를 사용하고
GitHub의 실제 발행 시각을 조작하지 않는다. 민감 정보·새 개인 경로를 공개 문서에 추가하지 않는다.

## R3 — 배포 전 후보 검증

정확 채택 및 clean/checkpoint 상태를 확인한다. 전체 python3 -m unittest discover -s tests -v,
dev contract guard 및 queue/control 검증을 수행한다. 기존 실패 기록은 삭제하지 않는다.
격리 clone/임시 skills-dir에서 문서와 같은 preview(무변경), apply, VERSION, 설치 사본 독립
실행/도움말 또는 read-only bootstrap, 재설치 KEEP, 다른 기존 대상 충돌 시 byte 보존을 확인한다.
사용자의 실제 ~/.claude 또는 회사 프로젝트를 쓰지 않는다. 필요한 의미 있는 smoke를 수행하고
단순 문구 미러 테스트를 추가할 필요는 없다. 후보 commit SHA와 모든 결과를 연결한다.
회사 Claude Code 로그인/실제 대화까지 수행하지 않았으면 그 한계를 남긴다.

## R4 — main 승격 및 hook 결정

발행 직전 실제 origin main/tag/release와 세 worktree의 상태·writers를 다시 확인한다.
검증한 dev 후보를 고정하고 main에서 git merge --ff-only <candidate>로만 승격한다.
main 직접 편집/커밋, reset, 강제 push, 기존 태그 이동은 금지한다. 원격과 충돌하면 안전하게
원인을 확인하고 필요할 때 같은 plan에 구체적 결정 인계를 한다. 일상 작업 상태를 보존한다.

이번 요청으로 historical v0.1.0 main 유지 제한의 좁은 예외를 승인한다. 승격 후 main에 runtime이
존재하는지 확인하고 main의 core.hooksPath만 git config --worktree로 .githooks에 설정한다.
plan/dev 설정은 보존하고 shared contract_guard.py install은 실행하지 않는다.
현 pre-push는 main/tag의 release 검증을 대신하지 않으므로 후보의 전체 회귀와
contract_guard.py check --branch dev --target <candidate>를 명시적 발행 gate로 사용한다.
현재 소스에서 이 인자/동작을 확인한다. 훅 우회나 새 hook 구현은 범위 밖이다.
이 문서는 local-harness-setup.md의 과거 setup 기록을 수정하지 않고 이번 승격 예외를 추가한다.
외부 container 진입점의 main-baseline 설명이 낡으면 plan에 정확한 수정 요청을 남긴다.

## R5 — 공식 발행

기존 origin/main에 정상 push하고 검증한 동일 후보에 annotated v0.2.3 태그를 생성·push한다.
이미 같은 태그/Release가 생겼으면 실제 상태를 확인하여 안전하게 재진입하고 덮어쓰지 않는다.
GitHub Release는 v0.2.3, 정식(non-draft/non-prerelease), 준비한 설치 안내·검증 한계·변경 요약을
포함한다. 별도 바이너리는 필요 없으며 GitHub 소스 archive/태그 clone 경로를 제공한다.
인증 계정은 확인하되 token/credential은 로그·문서에 출력하지 않는다.
기존 PR이 있다면 상태를 확인하고 main 반영과의 관계를 보고하되 unrelated 변경은 하지 않는다.

## R6 — 공개 결과 검증

main 및 tag의 commit SHA, VERSION, README/안내 링크와 Release draft=false/prerelease=false를
실제 원격에서 확인한다. 새 공개 태그 clone에서 설치 안내 경로를 임시 대상으로 재실행한다.
로컬 후보 통과만으로 회사에서 다운로드 가능하다고 주장하지 않는다.
문서 실패가 발행 후 드러나면 tag를 이동하지 않고 구체적 정정/후속 버전 판단을 plan에 넘긴다.

## R7 — 기록과 비동기 결과 전달

docs/verification/P008/에 검증·실패·실제 원격 URL/SHA·hook 설정·설치 재현 증거를 남긴다.
최종 발행 증거는 발행 후 dev에 추가 commit/push한다. 이를 포함하려고 이미 발행한 tag를
이동하지 않는다. main/tag는 검증된 release candidate에 유지하며 최종 C5 실행/운영 기록은
그 이후 dev commit일 수 있음을 보고한다. 배포 payload와 후행 증거 commit을 구별한다.
plan에는 공통 review key, artifact/version/hash, release·main·tag URL, 최소 설치 명령과
잔여 한계를 한 번 전달한다. 사용자에게 중복 완료 확인을 요구하지 않는다.
Plan은 SENT 후 ACK/채택/완료를 기다리지 않고 다음 기획을 받을 수 있게 턴을 끝낸다.
