# P011 relay recovery review

Common key `P011-official-claude-relay`. Reviewed decision `9f986f4085d1978c272847dad84515d2617aa9e2`. Source `de40ec9255b67959e871247a676d8cb920214031`. Evidence in docs/verification/P011/bounded-recovery/.

The original entry and its hash are preserved. Its full callback trace, sender exit and absent receipts supported a separate REJECTED_BEFORE_SEND disposition. One linked authorization was consumed. On that invocation the complete message and recipient matched, while the content field matched neither approved representation. The callback denied the call. The original key and the recovery reservation are both occupied. The SDK result, callback decision and receiver observations are recorded individually.

P901 delivery, execution and the subsequent handoff remain unverified. Further design review can investigate how the installed CLI represents content in an isolated non-delivering test. The existing human request is recorded. No terminal action is requested.

Final source regression: 110 tests passed. Installation: 34 checks. Manifest SHA256 `c3cbb5162a9a606f4e128efea26721bead02a22e8b52bcef8b855c73a48da833`.
