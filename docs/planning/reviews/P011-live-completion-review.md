# P011 실제 전달 완료 검토와 최종 상태 정리 — 2026-11-28

Common key `P011-official-claude-relay`. 기존 승인 범위의 결과 검토다.

결과 `a7feb3914c28c2b7401ceef3677009c4d8e3831f`의 report를 읽고 manifest SHA256
`4a435b9b0b1a200883808358083ca3e6dfd532a4987c2654ddd5c1d449125079`와 3개 artifact
hash를 Git blob에서 재검산했다. 실제 fixture dev 완료 commit
`10a4f5fa9407b949113d1c77f151782cdc8a98e8`의 marker blob을 별도 읽어 기대 hex
`5039303120eba788ecbba420e29c930a` 16 bytes와 일치함을 확인했다.

확인된 흐름은 source `cb5b529d082c204325b0222f02c5b24a1cf5f275`로 기존 Claude plan에
계속 인계를 전달해 실제 턴/P901 계획을 만들고, 그 plan이 준비한 정확 이벤트를 기존 Claude
dev에 전달해 채택·marker 구현·검증·plan 결과 검토까지 마친 것이다. 이 과정에서 사람에게
같은 계속/채택 문장 입력을 추가 요구하지 않았다. 초기 plan 수신과 그 후 정확 P901 dev 인계는
P011 C3의 첫 전달/두 번째 전달 증거이며 P010의 재접속 후 P902 시험과는 별개다.

Dev 정확 채택은 `444f4f16a2faab7069c278f2a2e52ab6172ec6ec`에서
`057ecbc4ca8ae0c4cb5d64fe1247afd4b7bccdf3`를 적용했다. 결과 회신 중 종료된 relay 주소로
ENOENT 한 번이 있었고 기존 실제 plan identity로 다시 전달돼 성공했다. 그 실패는 보존하며
중계 세션이 지속적인 결과 수신처라는 주장을 하지 않는다. 이후 fixture plan 자신이
`9bf7e081d00a1c761ae988c0ff7e36b10290067a`로 PASS 검토하고 transport 귀속 통지에 따라
`a9b742dc4379033d9d7cb4bea66169c2b8a4503a`에서 원래 이벤트 SENT를 기록했다.

기능은 자동 공식 relay로 검증됐으나 기존 fixture 설치 runtime은 0.2.5이고 외부 source
adapter를 사용했다. 모든 기존 프로젝트/개인 설치가 0.2.6으로 갱신됐다는 뜻이 아니다.
공개 main/tag0.2.3 및 P009/P010 미완료 기록도 유지한다.

## 최종 정리 인계

현재 dev P011 카드는 C4만 체크되고 이전 FAIL/blocked 상태가 남아 있다. Dev는 이 리뷰를
정확 채택한 뒤 최종 source와 누적 검증을 C1~C5에 대응시켜 실행 필드와 append-only 로그를
정리한다. 실제 충족된 조건만 최신 PASS로 기록하고 과거 FAIL/UNKNOWN/소모된 recovery는
지우지 않는다. Source CLI/도구·대상·내용 제한, 통제/중복/fresh proof, 실제 두 전달,
설치/최종113회귀·34검사·증거/hash·push/결과 인계를 서로 구분한다.

코드 변경 없이 기존 검증이 충분하면 전체 테스트를 반복하지 않는다. 실제 미충족이 발견되면
구체적 조건과 근거를 남기고 완료를 강요하지 않는다. 현재 카드 정리와 최종 결과 artifact는
dev 소유이며 plan이 직접 체크하거나 dev를 병합하지 않는다.

최종 결과에 relay 종료 후 reply 주소의 수명과 실제 plan 결과 전달 경로, 필수 SDK/CLI 버전,
최초 권한 예외/미검증 플랫폼, 실제 적용된 source/설치 대상과 미발행 상태를 명시한다.
P010 재연결/Codex 시험은 자동 실행하거나 P011 완료에 섞지 않는다. 상태 정리/정상 push 후
최종 결과를 같은 key로 인계한다. 사용자 재승인/계속 입력과 ACK 대기 루프는 필요 없다.

## 최종 완료 확인 — 2026-11-28

결과 `f7ac1912ae3235a99adf86c0af767cdee5d2fa33`의 final.md와 P011 실행 카드를 읽었다.
Final SHA256 `38d6ac9598cbbc54a0478102969410005d06c9bbcb1226e84e0d99493fb83541`
일치를 직접 확인했다. scripts/assets/tests/VERSION을 cb5b529와 비교해 차이가 없음을
확인했으므로 기존 최종113회귀/34설치 검증을 적용한다. 불필요한 재실행은 하지 않았다.

Dev 소유 카드 C1~C5 최신 PASS/실행 완료가 기록됐고 과거 FAIL/차단·복구 기록은 남아 있다.
P011 완료 결과를 인정한다. 실제 검증 범위는 이 Mac의 Claude CLI2.1.332/SDK0.2.189,
기존 0.2.5 fixture와 외부0.2.6 source adapter다. 회사계정/다른 OS/전체프로젝트 일괄설치는
검증되지 않았다. 종료된 relay 주소의 회신 실패와 지속 plan으로 재발견한 결과 경로도 보존한다.

0.2.6은 미발행 dev 소스/설치형이고 main/tag 공개버전은0.2.3이다. P009/P010의 별도
미완료를 해제하지 않는다. 기존 작업·중지·개인설치 보존. 이번은 최종 결과 검토이며
새 실행 인계/단순 ACK/완료 감시를 발행하지 않는다.
