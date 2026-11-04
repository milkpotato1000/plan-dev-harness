# P005 — existing installations upgraded to 0.2.1

All four local installations are upgraded: this installer-managed repository and
three reviewed manual integrations. Each actual outer/child entrypoint reaches the
startup/document-delivery rules. Legacy integration provenance is explicit; no
installer manifest was fabricated. Custom guards, strict timestamp parsing,
protected paths and adapter hooks remain intact.

The central adopted plan is 5030f3524b56e78192a989ec2e283e734d62905d.
Target approvals and exact SHAs are recorded in the target-integration review and
[target results](target-results.json). The managed installation's 15 payload hashes,
outer template, main and hooks are verified in [managed results](managed-final.json).
All 107 inspected P002 card/export files remain unchanged: 2/5, both fixture roles
stopped, OPEN retained, no missing fixture reconstruction or resumption.

Actual target plan/dev guards passed for worktree, index and HEAD. Task semantics,
next selection and decision/pause behavior were checked at the maintenance boundary.
Original dirty planning files and deleted images remain preserved. Product execution
and evidence were not rewritten to satisfy maintenance checks. Main/FE/backup/stash,
hook configuration and remote destinations are unchanged. Symbolic remote HEADs
continue to point at their original dev tracking branches and naturally resolve to
the newly pushed dev commits; they are not independent main/release changes.

Two targets delivered the reviewed maintenance to their existing single remotes.
One acquired independent product work after our upgrade checks: its verified dev
maintenance was pushed from an isolated clone without touching the active writer's
worktree; the newer remote plan includes the reviewed maintenance integration.

The third target's three remotes contained newer, already-adopted product history.
The first normal push correctly refused to overwrite it. Plan then reviewed the
exact existing remote baseline and combined it with the local maintenance under
7e82a2792da5db39ff012bcf07aedd75c1f13578. An isolated merge preserved both dev
histories and resolved only the adoption record to that reviewed SHA. Actual dev
integration, guards and queue comparison passed against the existing remote product
state. Its product files, logs, decisions, checkpoints and prior evidence match
that remote state; the stale local task count is not claimed unchanged. All three
remote plan/dev pairs now exactly match the verified combined heads.

Validation history is retained: each runtime variant has 68 latest passing cases
(67 in the full suite plus one focused pass after repairing a missing reference-doc
fixture), 12 additional legacy/ledger checks passed, nine custom ledger/timestamp
checks passed, and plan independently verified 35 existing harness tests for the
first legacy target. Initial fixture setup failures, the rejected non-fast-forward
push, and the corrected symbolic-HEAD audit assertion remain in private evidence.
No failed run is relabeled as a clean full-suite success. These are harness tests
and instruction checks, not proof of every future model session's behavior.

No product queue, model/DB/service action, cross-project message or pause resume
was performed by this upgrade. Public evidence is anonymized; complete target
inventory, immutable backups, command logs, diffs and preservation fingerprints
remain in the private local audit. Git-external outer files on this machine were
updated and have tracked reconstruction templates; pushes cannot update another
machine's outer files automatically.

All C1–C5 conditions have supporting evidence. The distribution completion commit
is delivered through its ordinary origin/dev push and the exact resulting ref is
checked separately after commit. Main promotion and releases were not performed.
