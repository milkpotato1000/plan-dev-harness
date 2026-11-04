# P005 preservation upgrade — proposal checkpoint

Four actual installations were inspected: this managed installation and three
legacy installations. Package/research copies are not counted as installed targets.
Inventory includes branch/ref/adoption, policy, queues, guards, hooks, remotes,
known app writers, dirty paths, tracked content hashes and original control files.
Private target names, paths, rules, backups and full command logs stay outside this
public distribution repository; their content digests are in proposal-summary.json.

The managed installation is locally upgraded to 0.2.1 via exact plan commit
269d904889f1245194869a7cd175223296d9a489 and dev adoption commit
96a81b1 (full SHA in local-upgrade.json). All 15 managed payload hashes match;
worktree/index/HEAD guards and queue pass. The outer entrypoint matches its tracked
reconstruction document. Main remains 803d658a8c61dc6aa007645a98d4160b16746faa.
All 107 inspected P002 card/export files are unchanged; its 2/5 and stopped status
remain. Missing temporary fixture Git metadata was not recreated or resumed.

Three legacy proposals are ready for final plan review; no live legacy files,
branches, remotes or outer entrypoints have been changed by dev. Installer previews
correctly refuse differing legacy guards. Proposals preserve existing protected
paths and hooks while adding controls/intake ownership. They retain custom approval
ledger checks and the stricter timestamp parser. One project daily-work skill has
only the plan-requested startup sentence clarification; it is not replaced.

For each proposal, isolated actual-history maintenance commits start from the
existing dev adoption, merge into the current plan, and are adopted exactly on a
copy of dev. All six role guards per target pass. Task states, next selections,
decision/pause lists, product paths and dirty deletions are preserved. The final
documentation-only amendment was separately checked; its runtime bytes match the
tested candidates. The real legacy worktrees retain all 27,301 inspected tracked
file contents, dirty states and refs. Runtime variants each have 68 latest passing
test-case results: 67 in the full suite and one focused rerun after restoring an
omitted reference-doc test fixture. Earlier fixture-setup errors are preserved in
private logs, not hidden. Additional legacy/guard checks: 12 PASS; existing custom
approval/timestamp tests: 9 PASS. No product, model, DB or service tests were run.

C1 is complete. C2–C5 remain unchecked across all targets: final target-specific
plan review and live maintenance commits, legacy dev adoption/application, final
live verification and all target remote delivery are still required. Candidate
commits are test fixtures, not reviewed live plan baselines. Recheck actual writer
ownership before application; an idle/not-loaded app snapshot cannot rule out an
external writer. These tests verify machinery and instructions, not universal
compliance by a fresh model session.
