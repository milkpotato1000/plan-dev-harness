# P005 target integration review — 2026-11-04

APPROVED. Plan reviewed the final isolated proposals and applied only the reviewed
governance/runtime files to three legacy plan histories. Private mapping, backups
and full fingerprints remain in local artifacts, outside this public distribution.

## Legacy target 1

- Exact reviewed maintenance SHA: `e019a35a2ad9c671167d2adad54c4890a8c02f99`.
- Parent (old dev adoption): `e065560e3a48a6a4a1d41c26a721ee2a99521dce`.
- Plan integration: `908075f798c0caa5c358b68097fc6e4da28b0777`.
- Target review: `docs/process/harness-0.2.1-review.md`.
- Approved change manifest SHA-256: `09214f5a6ae494f6a401fd0375390338d6520b9487dc976c5083c193b8830da3`.
- Plan worktree/index/HEAD guard passed; dirty content/status preserved; outer applied.

## Legacy target 2

- Exact reviewed maintenance SHA: `65bd7b86e2a61cad770f79974f148513452e27f0`.
- Parent (old dev adoption): `f1b93e082c1c7079d70cd0cbe80b764c4886597b`.
- Plan integration: `39d3e85b5b52993b3b4a36641c269275463f86c6`.
- Target review: `docs/process/harness-0.2.1-review.md`.
- Approved change manifest SHA-256: `985cb868d4d8aedfa0d11fb7c517b24b1b4d9cd5c9c98006ed00437ea75d9bfa`.
- Plan worktree/index/HEAD guard passed; dirty content/status preserved; outer applied.

## Legacy target 3

- Exact reviewed maintenance SHA: `7da28684453a8f2609b127b7f60ac84045fb9fa5`.
- Parent (old dev adoption): `bf02d22600ff14d646571c81ce760dcaae27a51b`.
- Plan integration: `4fab7227e48763bf7b0b11882be995319c811f56`.
- Target review: `docs/process/harness-0.2.1-review.md`.
- Approved change manifest SHA-256: `e4a9cf7c7f2ca6021b7f80437234c720fbc79d8569e29e4a2bfd0bcf323e11e0`.
- Plan worktree/index/HEAD guard passed; dirty content/status preserved; outer applied.

## Review evidence and handoff

Stock runtime parity and retained custom ledger/strict timestamp parsing were
inspected. Policy retains all prior protected paths. Final daily-skill/queue text
clarifications preserve custom behavior. No product plans, progress, verification,
decisions, checkpoints or consumed one-shots were edited. Existing hooks remained
enabled for the actual approved commits and normal plan merges. Each maintenance
commit is based on old adoption, so later unadopted product planning is excluded.

Isolated actual-history rehearsals passed for all three targets. Each proposal
has 68 latest passing runtime cases (67 in the full run plus a focused repaired
fixture case); initial fixture errors remain preserved. Shared legacy regression12
and existing custom ledger/timestamp9 passed. Plan additionally ran the first
legacy project existing harness suite:35 PASS. This is not a fresh-model behavior test.

Dev now integrates/adopts only the exact target SHAs above with each target review,
preserving dirty changes and execution logs; commits adoption, checks guard all
three targets and queue/state/hash parity; then normal-pushes reviewed plan/dev to
existing authorized remotes and verifies refs. No latest-plan product scope adoption,
product queue execution, external service writes, cross-project chat messages or
P002 resume. Complete actual results under P005 evidence before checking criteria.
