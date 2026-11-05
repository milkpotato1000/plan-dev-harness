# P003 result — installable direct-handoff procedure

Status: complete, C1–C5 PASS within the policy/distribution scope. Date: 2026-10-29 (Asia/Seoul).
Exact plan snapshot: `283ddd331eb5196bc6b2f36b0ced15ad3ce2ba74`.
Initial snapshot `80dbb3b4e53ffd8f7427e48cb7c827a22f6aa5f4` was adopted at
`77b757cce25dd2f5ee5b3751dbfb26fb70d88d08`; work was preserved in `19e38fe` before
follow-up adoption at `84ea10a`. Readiness and installable-rule reviews were read.
Version stays 0.2.0; this is dev implementation, not main promotion or a release.

## Changed behavior and evidence

The source skill and references now explain how a human-authorized plan hands
committed READY work directly to a verified existing dev, and how dev integrates,
exactly adopts, checks and starts the authorized scope. The rule is present in
installed project instructions, common process, generated workspace entrypoint
and both copied role prompts. Installation does not create a human grant.
Read-only bootstrap, user stops, OPEN decisions and sender-owned SENT/ACK evidence
remain separate. No runtime state machine, CLI flag, hook installer or messaging
service was introduced.

| Criterion | Actual evidence / result |
| --- | --- |
| C1 | [M1–M3 policy walkthrough](policy-matrix.md), source/installed entrypoints and [actual payload exports/hashes](payload-hashes.json); PASS as procedure review |
| C2 | M4–M8 in policy-matrix.md; exact payload, real evidence requirements, receipt observation, failure/unknown outcome handling and no ACK/reverse loops; PASS as procedure review |
| C3 | Existing workflow controls regressions, exact adoption guards and P002 preserved-input gate; fallback keeps stops/adoption/decisions; PASS |
| C4 | [Independent copy/bootstrap commands](payload-commands.json), installed manifests and raw outputs; actual pre-P003 same-option v0.2 [upgrade/conflict records](upgrade-commands.json), legacy/fresh destination integration tests; PASS |
| C5 | [Transition/feature mapping](transition-and-preservation.md), [layer hashes](layers-and-upgrade.json), full regression and guard/queue snapshots; PASS |

## Actual validation

- Python 3.9.6: `python3 -m unittest discover -s tests -v`, exit 0,
  **67 tests PASS in 144.922s**; [final log](regression.log).
- The earlier implementation also passed 67 tests before the follow-up clarification;
  [initial log](regression-initial.log) is preserved. Final full regression was rerun
  because project/workspace AGENTS and output coverage were extended.
- Independent temporary Codex/Claude skill copies installed projects and created
  linked workspaces; preview destinations stayed absent, generated output contents,
  manifest hashes, local links, standalone CLIs, empty tasks/handoffs and no remotes
  were checked. Actual selected outputs are retained as raw .txt exports under outputs/.
- The actual archived pre-P003 v0.2 payload was installed and upgraded with the
  same options; preview was unchanged, custom post-hook/live data survived, and
  managed user customization refused every write. Legacy skill collision checks
  preserved the whole old tree and its extension; a fresh install did not alter it.
- Repository installed manifest hashes match. Guard worktree/index/HEAD and queue
  evidence are recorded in control-checks.json and post-commit-checks.json.

## Limits, failures and retained state

No unexpected failing test occurred in these runs. Expected CLI conflict refusals
are retained with their exit codes in upgrade-commands.json; they are preservation
checks. Policy M1–M8 walkthrough is hypothetical input review, not live-host proof.
This dev received/read/adopted the actual incoming handoffs; it did not send reverse
messages or change plan-owned delivery events. Sender SENT/ACK are not certified here.
No actual personal skill activation, other-project apply, global config, main/tag/
release change or remote addition occurred. Python 3.13 and other OSes were not
rerun for P003; prior v0.2 evidence remains historical.

P002 is incomplete (0/5). Its fixture was prepared from the recorded earlier source
and retained; its S0 actual second-session/user-input gate remains. Supplementary
regression cannot replace actual sessions or pause/resume utterances. The final
queue therefore has unfinished P002 and `--open` exit 1 is expected, not an error.

Implementation and evidence are in this document's containing dev commit and its
subsequent control-evidence commit; final source payload hashes identify tested files.
