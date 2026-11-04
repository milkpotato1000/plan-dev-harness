# P005 준비 검토 — 2026-11-04

READY. 사용자 기존 프로젝트 검색·0.2.1 갱신 요청을 정확히 반영한다.
관리 설치 1개와 manifest 없는 custom 설치 3개를 조사했다. 모든 기존 dev guard가 통과했고
큐 조회는 read-only였다. 한 plan의 미커밋 기획 파일 및 다른 dev의 미커밋 삭제를 발견했다.
기존 writer 확인과 전후 내용 검증이 필수다. 최신 plan 전체 채택은 미채택 제품 계획을
섞을 수 있으므로 adopted baseline 기반 유지보수 commit을 plan에 merge한 뒤 dev에 채택한다.

보호 runtime 변경은 dev proposal → 실제 plan diff 검토 → 정확 commit → dev 채택으로 나눈다.
새 기능의 의미적 검증 없이 version marker만 바꾸는 완료는 거부한다. P002 중지는 보존한다.
외부 서비스 쓰기/타 프로젝트 메시징/제품 실행/main 승격은 승인하지 않는다.
이 프로젝트 기존 인간 위임에 따라 확인된 기존 dev 채팅으로 본 계약을 전달·착수한다.
수신자는 P005 proposal부터 진행하고 대상 보호 파일 적용은 plan의 후속 exact review를 기다린다.
