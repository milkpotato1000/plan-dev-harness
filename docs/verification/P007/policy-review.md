# P007 independent M1–M12 review

Expected behavior is derived from the reviewed P007 contract. ReviewExercise is
a test-only stateful reference actor persisting fixture Markdown; it is not a
production schema/parser, a shipped sender or a host-wide question blocker.
The semantic scenarios are simulations using actual files. Git/CLI cases use
real temporary linked worktrees. No fixture answer is a real user approval.

| Case | Independent expectation | Evidence and limits |
| --- | --- | --- |
| M1 | Dev commits results without routine questions; plan asks necessary human judgment at most once per scope. | Stateful packet/ledger exercise: dev review/ledger writes are rejected; plan question count stays1 across repeats. Existing-scope decisions ask0. These are simulated question counters, not actual UI messages. |
| M2 | Record actual file/view observation and its limits; unavailable viewer is not PASS. | Fixture bytes are really read/hashed; content read is distinct from injected visual simulation. Viewer absence records NOT_OBSERVED with no invented observation. The dev result packet asks plan to open read-only results; dev does not claim that plan already viewed them. |
| M3 | Transport duplication, new commits and resumed sessions cannot reissue the same semantic question. | Same scoped key persists through actor restart/new delivery commit and preserves question/answer history. Separate real CLI events for different SHAs intentionally remain separate, proving transport dedup is not semantic dedup. |
| M4 | Reuse a valid human answer received in dev; reject unsupported agent approval claims. | Exact scope/material/raw-hash answer with a fixture human-source reference is reused with0 questions. An agent-only claim does not become approval. |
| M5 | UI/content/policy scopes differ; material changes need review; non-material equivalence needs evidence. | Different scope or material content produces a different key/review. Changed raw timestamp bytes reuse only after explicit fixture-specific equivalence evidence. No general metadata-ignore rule is shipped. |
| M6 | Plan may decide within existing scope; a committed decision reaches dev only through exact adoption. | Stateful existing-scope decision asks0. Real protected decision file is absent in dev until exact plan merge/adopt; adoption alone neither resolves critical OPEN nor checks a human criterion. |
| M7 | Optional review does not block independent work; required human criteria remain incomplete; critical OPEN keeps conservative blocking. | Actual queue: optional nested review packet leaves selection available; required P001 is BLOCKED/unchecked while independent P002 is eligible and dependent P003 waits. Critical OPEN then blocks dev. Existing classification/resolution/stop regressions remain in the full suite. |
| M8 | Busy roles keep current work, failures, pending questions and one writer; SENT ends a sender turn. | Busy-plan simulation queues a packet without touching current work or reissuing its question. P006 real worktree/busy-dev, event-history, safe-boundary and no-ACK-wait tests remain. Host scheduling/model compliance is not universally proven. |
| M9 | Actual project grant is directional; absent host or failed/unknown delivery leaves durable pending data without a dev fallback question. | Stateful capability cases: plan→dev permission alone cannot authorize dev→plan; missing host/denial sends0; failure/unknown attempts once and stays PENDING across restart. A real optional result delivery uses only the separately verified human grant and records actual outcome; no receipt is inferred. |
| M10 | Direct code questions/answers in dev remain permitted and link to the common record. | A verifiable fixture answer with received_in=dev is reused by plan at the same hash/scope. No real human answer was fabricated for this task. |
| M11 | Platform approvals/denials cannot be bypassed through another role; no ACK loop/new chat. | Denial records a block without a question or delivery, even with a messaging grant. Wrong-role sender/ledger operations fail in the fixture. Source instructions preserve normal platform approval; no bypass mechanism/runtime API was added. |
| M12 | Both host packages, upgrade/bootstrap, active disk hashes, full regression and historical stops remain consistent. | Independent Codex/Claude packages/bootstrap plus real0.2.2 upgrade deliver the new template; runtime bytes/extensions remain. Active Codex transition is backed up and hash-verified at the same path. Old retained fixture failures are reported separately. P002/main/P005/P006 preservation is fingerprinted. |

Semantic deduplication remains an agent obligation supported by shared durable
records. These tests do not mechanically prevent every future host/model from
asking twice. No new user statement is required to complete this verification.
