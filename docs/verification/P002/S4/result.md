# P002 C4 — PASS, actual two-role delivery in both directions

| Direction | Artifact | Trial event | Actual receiver commit | Final sender evidence |
| --- | --- | --- | --- | --- |
| plan→dev WORK_READY | 77d47f0e3bdafdf44a7ff613c519a9e41f9d4a30 | 72f842952277b996a9bc459626d63881529dd6919c59b3edb600eaf528c0ffed | e86217895835cb2a77786aba5f17c3699894dc9d | plan3c29422a3aeb14fe3f9869a2c0fa650d3b753e2a |
| dev→plan DECISION_REQUEST | fdf0e69c5462dc75c5193309c1fa0bb591a71e80 | 191ac08374500963ee0fde0b96c2fd4dac8a64a95462652ecf5ab2c9e0bf574a | plan05c18fe35e48ab5b7a12da3a5f06fdae742fa9d0 | devc1bcaa14c9909dbb0d409828560cfee342a237c1 |

Both events have actual PENDING→SENT→ACKNOWLEDGED history. Actual host send success
was linked to SENT; each receiving role directly read the exact artifact/event and
committed its own receipt; each sender read that actual receipt before ACK.
Original human S1–S5 same-project two-role messaging authority covered the tool
route. Public aliases hide private chat identifiers; raw host references are private.

Each actual sender verified identical create KEEP, changed summary exit2, changed
next-action exit2, PENDING→ACK exit2, and empty SENT evidence exit2. Event bytes,
history and count stayed unchanged. After actual ACK, identical create remained
KEEP and repeated ACK rejected exit2 without changing bytes/history/count.

Evidence: plan-pending-tests.json, plan-event-at-receipt.json, dev-receipt.md,
plan-ack-tests.json, plan-ack-event.json; dev-pending-tests.json,
dev-event-pending.json, dev-event-sent.json, plan-reverse-receipt.md/json,
dev-ack-tests.json and dev-event-ack.json. All negative outputs are preserved.

Reverse recipient's first immediate observation was PENDING even though the host
message had arrived. It preserved that observation, then recorded the actual SENT
commit when writing its receipt. Arrival and sender persistence were distinct;
no inferred SENT or retroactive rewriting. DECISION_REQUEST created no OPEN.
These finite receipt-test steps are S4's actual behavior; earlier distribution
coordination events are not substituted for trial evidence. No background polling,
new chat, extra human question or marker execution occurred in S4.
