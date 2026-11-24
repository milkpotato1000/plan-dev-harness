# P008 준비 검토 — 2026-11-24

READY. P002와 P007의 완료된 dev 증거 및 현재 queue/guard를 확인했다. 기존 dev writer와
같은 프로젝트의 수신 채팅을 확인했다. 이 작업은 P008로 분리하며 이전 완료 기록을 덮어쓰지 않는다.

사용자는 이번에 main 반영·정식 릴리스를 명시 승인했다. 기존 plan/dev 정상 push 위임을
main에 임의 확장한 것이 아니다. 이번 P008 계약 R1~R7의 origin/main·v0.2.3·GitHub Release
발행과 승격 후 main 한정 hook 설정은 승인된 실행 범위다. 회사 계정/다른 프로젝트는 제외한다.

공개 main 0.1.0과 dev 0.2.3의 간극 때문에 기본 clone만 안내하면 최신 설치가 안 됐다.
태그 고정 설치와 main 승격, 누적 변경 기록, 공개 다운로드 후 설치 검증으로 해결한다.
main은 dev의 조상이므로 현 상태에서 fast-forward 가능하나 실행 직전 원격을 재검증한다.
기존 main pre-push가 release gate를 제공하지 않는 점을 반영해 정확 후보 검증을 필수로 한다.

마켓플레이스 manifest가 없는 현 구조를 사실대로 안내한다. 공식 Claude Code skills 문서의
personal/project SKILL 경로·slash invocation과 저장소 installer 옵션을 대조했다. 회사의
실제 관리 정책/Claude 실행 환경이나 Linux/WSL까지 통과했다고 주장하지 않는다.

Plan-owned AGENTS에 이번 승격의 좁은 예외를 명시했다. 그 외 protected runtime/policy 변경은
요구하지 않는다. Dev는 정확 reviewed SHA를 통합·채택 후 제품 문서와 배포를 수행하고
커밋된 증거를 기존 결과 인계 위임으로 plan에 전달한다. 같은 출판 승인을 다시 묻지 않는다.
