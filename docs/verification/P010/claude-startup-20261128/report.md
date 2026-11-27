# P010 actual Claude startup checkpoint — 2026-11-28

Common key: P010-session-registration-reconnect. Source 0.2.5 remains
 e044e3e7f11ef48d4f9cc4fa41cad7ac00d8e1c8. Exact parent startup review
ba1eab5f208a3fa355c89482699b1def2441a312 was internally adopted (2253ac8).
This checkpoint verifies real startup registration only; C3 remains incomplete, 4/5.

## Independently observed

Official existing-session hook results identify the harness SessionStart handler, empty
stdout, stderr `plan-dev-harness: registered`, exit 0:

| Role | Actual startup hook result (Asia/Seoul, 2026-11-28) | Duration |
| --- | --- | --- |
| fixture-plan | 01:44:21.436 | 410 ms |
| fixture-dev | 01:44:47.199 | 391 ms |

Subsequent real Stop hooks also registered successfully (01:45:10.157 and 01:45:46.731).
Only this harness's hook results are exported; unrelated hooks and private identities,
commands, conversation text and settings are excluded. These are actual host lifecycle
results, not the earlier synthetic stdin tests.

Bounded human-input metadata records explicit plan scope at 01:44:35.634 and explicit dev
scope at 01:45:11.751. No later continue/P901 input was observed in that inspected window.
The parent review also records the actual user's report that both terminals were opened.

At 01:49:31.492974, official host inventory found exactly one existing idle session at each
configured role cwd. Independent installed doctor --live, outside the restricted sandbox,
returned identity_consistent, issues=[], performs_actions=false for both roles. Registry
observations were plan generation 1 / dev generation 3. These values are registration
sequence numbers, not evidence of a restart/resume. A point-in-time freshness check is not
an evergreen delivery permit: the actual sender must recheck immediately before sending.

Fixture plan c5d29c7dd4f3449309e5db2bdf38d4b3df2646f8 and dev
a8f39aef5be29989f5655cc0569a3061ad19f277 were clean. Their exact committed precondition/ready
reports are exported with source hashes. The plan report records an earlier dev_missing
check and return; the dev report records both roles ready and awaiting the first handoff.
Report timestamps are not substituted for exact tool query times. Queue was empty with
no P901 card/event, pending decisions or pauses. Dev adoption remained the fixture runtime
baseline 4a361b0d5b6caab77859a7a93df644f38eb01b65.

The parent review preserves the initial sandbox inventory=[]/identity_mismatch observation.
The successful independent host check above distinguishes visibility restriction from
registration failure. No sandbox setting or host permission was changed.

## Remaining boundary

Automatic registration and later peer discovery do not start an idle plan turn. That
startup-order usability limit is now observed: existing plan returned when dev was missing;
later registration did not author/send P901. Parent Codex's available tool inventory still
contains only Codex chat delivery, not Claude native ListAgents/SendMessage. No supported
parent-to-existing-Claude wakeup was performed. The parent has already supplied the single
continue instruction for the existing fixture plan; this observer does not resend it as a
human input or request fresh terminals, trust or adoption.

Current evidence: actual Claude registration and point-in-time identity matching PASS;
first exact native handoff/receipt/application/completion, normal reconnect and next handoff
NOT OBSERVED. Codex two-session startup remains NOTRUN. No first-task restart/reconnect,
forced shutdown, raw socket, terminal injection or competing worker was attempted. Parent
observer did not write fixture cards or implementation. Source has not changed, so the
105-test source suite was not repeated. P009 evidence/stops, installed parent runtime,
personal installations and main/tag remain intact.

This is a bounded checkpoint, not an unchanged-state monitoring loop. Resume observation
on actual new input/work evidence. Keep C3 unchecked until the full Claude/Codex contract
is supported by actual results; no criterion relaxation or automatic repeat.
