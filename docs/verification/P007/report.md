# P007 — result review and necessary decisions through plan, 0.2.3

Implementation/package verification is complete; the optional committed result
packet and actual delivery outcome are recorded separately after this artifact
commit. Final completion/guard/remote evidence is added at that boundary.

Dev now commits a scoped result/decision packet rather than asking routine
completion questions. Plan reads its common ledger, opens available read-only
results, reuses valid human answers from either role and asks necessary human
judgment once. The shared key includes P/criterion, artifact identity/material
version and question scope; it survives new transport commits and resumed sessions.
UI confirmation never becomes content/policy approval. Material change requires
new review; non-material equivalence requires evidence. Plan decisions reach dev
through exact reviewed adoption. Optional review, a required human criterion and
critical OPEN retain distinct queue/acceptance behavior.

Exact adopted plan:4217137e966ad9725581f1814830f62043e50cc0;
review:docs/planning/reviews/P007-dev-handoff.md. The current actual human request
was independently read in the existing plan chat and matches the narrow committed
dev-to-plan review delegation. That grant is project-specific; the package grants
no reverse messaging rights to other projects.

Source/installable packages and the same-path selected Codex disk copy are0.2.3.
The project-local managed marker remains0.2.1 with the plan-reviewed document hash
integration and original options/core runtime. The installer adds one generated
review-template file. No event/schema/parser/guard redesign or universal question
blocker was added. Shared-key deduplication is a documented agent obligation,
distinct from existing SHA-based transport event deduplication.

The latest full source regression passes83 tests. Ten new cases cover persistent
packet/ledger state, two roles/restarts, existing dev answers, material/raw hashes,
scope differences, viewer/permission limits, busy plan, directional grants and
failed/unknown sends, real Git decision adoption, optional/required/critical waits
and actual0.2.2 upgrade. P006 asynchronous/stop regressions remain in the suite.
An earlier full run failed only because its older upgrade test fixed the expected
target at0.2.2; it now checks the current source VERSION. The failed83-test log is
retained separately; it is not relabeled as a pass. See [M1–M12](policy-review.md).

Codex and Claude packages were independently installed/bootstrapped. The selected
Codex copy was backed up outside discovery, then safely transitioned at its existing
path. Four personal extra files and UI metadata are byte-identical; no duplicate
active copy or global Claude replacement was made. quick_validate and actual active
bootstrap preview pass. Automatic refresh/compliance in a new model session was
not observed. The retained old fixture tests still have20 PASS/11 unchanged FAIL;
the old active tree matches the P006-measured baseline byte-for-byte, and the new
candidate reproduces the same missing-import fixture failures. Existing files and
raw failure history are preserved, not silently repaired or claimed green.

All126 inspected P002/P005/P006 card/evidence files, the P006 original skill backup,
main803d658a8c61dc6aa007645a98d4160b16746faa, hook configuration and core CLI/runtime
assets remain unchanged. P002 stays2/5 with its archived PAUSED/OPEN state; the missing
temporary Git fixture was not recreated or resumed. Other product projects, product
approvals/results, external services/DB, credentials, main/release and remote
destinations were not changed by this task.

The review demo is a static explanatory artifact, not a product result or actual
human approval. Stateful actor outputs and injected visual observations are
simulations; actual Git/CLI/file hash checks are machine tests. Plan's future viewer
observation/decision must be recorded by plan; dev does not claim it occurred.
The result review is optional and creates no new human acceptance criterion.
