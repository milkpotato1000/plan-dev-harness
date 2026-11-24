# P008 — v0.2.3 release verification

Client release date: 2026-11-24, Asia/Seoul. Actual host/GitHub timestamps are recorded separately.
Reviewed plan:65a12e3af61dd5b82b52994d185032f9aeb61a57.
Actual human release/main/tag authorization was directly verified in session-plan.

## Immutable release payload and later evidence

This directory in the release tag records the verification contract for its fixed payload.
The exact candidate is committed before tests/publication. Results, failures, exact candidate
SHA, publication URLs and final P008 completion are committed afterwards on dev, without
moving the tag or changing main to include post-publication evidence.
Read the [current P008 evidence on dev](https://github.com/milkpotato1000/plan-dev-harness/tree/dev/docs/verification/P008)
and the [GitHub Release](https://github.com/milkpotato1000/plan-dev-harness/releases/tag/v0.2.3).
The tag's incomplete P008 execution fields describe its pre-publication checkpoint;
current dev records the later outcome.

Required gates: full source unittest suite; explicit `contract_guard.py check --branch dev
--target <candidate>`; isolated Claude installation preview with no writes, apply/version,
standalone CLI/help/bootstrap preview, identical KEEP and conflict-byte preservation.
After publishing, verify public main/tag/Release metadata and clone the public fixed tag
without GitHub credentials, then repeat isolated installation. Logs identify the actual
candidate and payload hashes; no output is passed solely because a previous version passed.

Scope: README/Claude installation guide/release notes and publication of existing0.2.3.
No new policy/runtime feature, company login, marketplace registration, personal skill change or
other project upgrade. Historical P002/P005/P006/P007 artifacts and failures remain preserved.
Official Claude personal/project skill and slash invocation reference was read at
https://code.claude.com/docs/en/skills; installed CLI behavior was checked directly in source.
The source suite and CLI checks on macOS do not certify company login, Linux/WSL execution,
native Windows, model compliance or cross-chat tools in a company Claude installation.
