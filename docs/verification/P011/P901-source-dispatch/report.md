# P901 external source dispatch

The fixture plan still owned its READY card and committed PENDING event. The transport operator ran the reviewed 0.2.6 adapter against the existing 0.2.5 fixture plan root. Immediately before sending, the operator checked both clean heads, explicit branches, unchanged card and review blobs, prior session activity, the event, shared project mapping, guards, queue controls and fresh unique host identity. The shared ledger reserved the existing event key. One native send succeeded. The dev peer input matched the native message ID and complete body. See send.json for the payload digest and exact source. The operator did not edit either fixture worktree.

The existing dev writer adopted 057ecbc4ca8ae0c4cb5d64fe1247afd4b7bccdf3 and committed the marker and its verification. Reading the marker directly from commit 10a4f5fa9407b949113d1c77f151782cdc8a98e8 reproduced the expected 16 bytes. The dev card marks C1–C3 complete. See completion.json for the blob and evidence digests.

Dev committed its results-packet delivery at 1c6132bfa6690bb51e78e8308cf3a620b39609d1. Its report records an initial undelivered ENOENT result and a subsequent successful send to the verified existing plan identity. The plan transcript independently contains the peer packet referring to completion commit 10a4f5f. Plan committed its own PASS review at 9bf7e081d00a1c761ae988c0ff7e36b10290067a. Its review explicitly left the original event pending because it lacked the external sender's identity and proof. The parent committed that proof before sending the authorized one-time transport attribution notice.

No source changes were required for this dispatch. The prior 113-test regression and 34 installation checks apply to the adapter version used. P010 reconnect, follow-up card and Codex session validation are outside this execution.

The attribution notice returned native inbox success. The fixture plan writer committed SENT on the original event with external transport attribution at a9b742dc4379033d9d7cb4bea66169c2b8a4503a.
