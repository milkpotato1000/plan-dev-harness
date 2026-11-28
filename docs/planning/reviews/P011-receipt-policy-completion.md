# P011 수신 관찰·정책 판정 보완 — 2026-11-28

Common key `P011-official-claude-relay`. 기존 A/B 계약의 미완료 검증 보완이다.

결과 `ea3808b1a5e19eaade9474b4a3b299c2a1353974`의 report/receiver/checks를 읽고
manifest SHA256 `5f891c55893114a65ecd20db4d66d7a53fcc8d54045ce85b2f29b0b7880cd936`
및 4개 artifact hash를 재검산했다. Source d97c948의 111 전체 테스트/34 설치 검사와
합성 메시지 517 UTF-8 bytes의 수신 hash 일치를 확인했다. 원본 body의 단일 framing
newline만 제거한 비교이며 모델 echo가 아니다. 실제 초기/후행 newline 자체를 strip해서
잘못 PASS시키지 않도록 observer 테스트를 추가한다.

현재 A는 partial이다. 관찰기가 peer user 이벤트를 놓쳐 receiver 종료 후에만 수신이
확인됐으며 inbound-refuse는 NOTRUN이다. sender deny는 도구 노출 거부 증거이며
updatedInput 이후 규칙 재평가를 직접 시험한 것으로 표현하지 않는다. B는 미실행이다.

## 보완 승인

1. 수신 관찰은 peer user/isMeta/origin과 queued attachment를 실제 schema별로 인식하되
   role/target/key/tool-use 연결과 정확 전체 bodyhash를 확인한다. partial JSON/변경 중 파일,
   중복 이벤트/서로 다른 메시지/내부 newline/유니코드·framing을 unit 테스트한다.
2. native 결과는 구조화된 status/boolean과 실제 문구의 의미를 바탕으로 판정한다.
   성공 설명에 조건부로 등장한 held/refuses 단어를 substring만으로 실패로 바꾸지 않는다.
   반대로 success=true만으로 실제 receiver 수신을 확정하지 않는다. 모순·알 수 없는 응답은
   unknown으로 남긴다. 실제 성공/실제 거부/조건부 설명/held/timeout을 캡처 기반으로 테스트한다.
3. 격리된 중립 수신 프로세스 최대 2개(동시 role writer 아님), 합성 sender 최대 4회를
   추가로 허용한다. sender 각각60초/0.50USD, receiver각각5분/1USD 이내이며 충분한
   증거가 나오면 남은 호출을 쓰지 않는다. 기존 P010 역할/실제 payload는 사용하지 않는다.
   수신 도구/제품 업무/MCP 없음과 원래 격리 범위는 그대로다.
4. 기본 수신 정책의 실제 성공을 관찰기로 즉시 포착하고, 별도 receiver를 시작부터 명시적
   refuse로 설정하거나 동일 테스트 receiver의 더 엄격한 정책 적용을 공식적으로 확인한 후
   거부 시험을 한다. 반영 시점이 불명인 파일 수정만으로 refuse 적용을 주장하지 않는다.
   테스트 receiver의 정책 강화만 허용하며 기존 사람 세션/조직 정책을 변경하지 않는다.
   독립 수신 입력 부재와 적용된 정책, native 거부/처리 결과를 함께 남긴다.
5. tool deny가 호출 전 도구를 숨기는 플랫폼 동작은 그 정확 범위의 증거로 인정한다.
   공식 updatedInput 경로가 deny를 무시하지 않는지도 지원되는 범위에서 검증하되 존재하지
   않는 tool-specific 규칙을 만들지 않는다. 관찰 불가한 단계를 검증했다고 주장하지 않는다.
   정책 보존 증거가 여전히 불충분하면 A partial/B NOTRUN으로 결과를 인계한다.

코드·최종 전체회귀·변경에 필요한 설치 검사를 진행한다. A의 실제 byte 일치/정책 보존이
충족되면 기존 `P011-canonical-input-validation.md` B의 조건부 validation-recovery 한 번을
사용할 수 있다. 이 문서는 B 횟수를 늘리거나 기존 소모된 recovery를 복구하지 않는다.
최종 source/A evidence와 두 reviewed SHA를 연결하고 원래 logicalkey/payload/target,
이전 pre-execution denial/종료/수신0을 재확인한다. 이미 진행된 실제 업무는 중복 발송하지 않는다.

사용자 계속 입력/재승인 질문 불필요. 기존 P010/P009 미완료·기록·중지·writer·개인 설치·
main/tag는 유지한다. 실제 역할 세션 재시작/설정 확대·guard 우회는 금지한다.
실제 B 성공/실패와 A의 정확한 범위, source/hash를 같은 key로 plan에 인계한다.
