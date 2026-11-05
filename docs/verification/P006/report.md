# P006 — asynchronous handoff, source/skill 0.2.2

Plan now records/commits/pushes actual SENT and ends its response. ACK is observed
on a later natural planning/status request. Busy dev preserves current work and
failures, then adopts the exact reviewed handoff at a safe committed boundary and
selects the next prepared P by priority/dependencies and existing stops/decisions.
The rule is carried by SKILL, references, shared instructions, workflow/adapter
documents, handoff templates, both role prompts and generated outer/child entrypoints.

Exact adopted plan: b3bc7d8b0dd87f48d1fce62958918c0fb68780ac;
review: docs/planning/reviews/P006-dev-handoff.md.
Source/package and the actual selected Codex disk copy are **0.2.2**. This
repository's managed installation remains **0.2.1**, with the plan-reviewed document
hash integration, original options/file list and unchanged runtime/schema. This is
not a claim that the entire local managed installation was upgraded to 0.2.2.

The full source suite passes **73 tests**. Real Git fixtures cover busy work,
failure preservation, exact adoption excluding a newer tip, priority/dependencies,
stops/OPEN, delayed ACK/event history and actual 0.2.1 upgrade. Host adapter cases
are simulations. One actual plan turn was observed returning after successful send,
SENT commit and push with no ACK/completion wait; fresh-model scheduling/behavior
is not universally proven. See [independent N1–N10 review](policy-review.md).

Codex and Claude packages were independently installed and bootstrapped in temporary
directories. The active Codex skill was backed up outside discovery and switched
at its existing path to the verified candidate, preserving four extra files and UI
metadata. Its new SKILL was reread, all candidate hashes match, quick_validate passes,
and its actual bootstrap preview writes nothing. No duplicate active copy was
created. A fresh session's automatic discovery refresh has not been observed.
No global Claude copy or project-specific same-name daily-work skill was changed.

Failure history is retained. The initial focused run had one fixture error: card
priority replacement assumed100 while the template default was10. The fixture was
corrected with explicit priority assertions; the full suite subsequently passed.
The active skill's four retained legacy test files yield20 PASS/11 FAIL on both
the original0.2.1 backup and0.2.2 candidate. The identical11 failures arise because
their old guard fixture omits the plan_intake dependency; they are preserved user
extensions, not passing tests or newly introduced regressions. Their original
files were not edited. Raw baseline/candidate logs remain in the private audit;
the public package summary records the unchanged failing-case set and hashes.

P002 remains2/5 with archived PAUSED/OPEN evidence preserved; its missing temporary
Git fixture was not reconstructed or resumed. P005 stays complete. All115 inspected
P002/P005 files, main803d658a8c61dc6aa007645a98d4160b16746faa, worktree hook config,
and installed/source runtime bytes remain unchanged. No new messaging permission,
product work, external service/DB operation, main promotion or release was performed.
Completion is recorded with actual guards/queue and ordinary origin/dev delivery;
the pushed ref is verified separately after commit.
