# P002 C3 — PASS with preserved historical/continuation boundaries

S2 historical actual two-role role-pause visibility, committed blocking and later
actual human resume remain PASS: ../S2/observation.md and its original command,
queue, checkpoint and patch exports. These are historical results, not rerun.
Historical S3 steps 1–3: second question, plan review/adoption, actual independent
dev/all and plan/all pauses: ../S3/checkpoint.md and original exports.

Original temporary Git files later disappeared. inventory.json records 0 files,
not a recoverable original history. Approved reconstruction used source
77b757cce25dd2f5ee5b3751dbfb26fb70d88d08 (0.2.0), all recorded source/managed
hashes matched, and distinct actual role writers restored their own records.
Original 106 exported files remained unchanged. New SHAs/times are truthful;
explicit first RESOLVED metadata mapping preserves original bytes privately and
in archive envelopes. It is not a new S1 execution or restoration of old SHAs.

| Required invariant | Actual evidence | Result |
| --- | --- | --- |
| Reconstructed both independent all-pauses and second OPEN | dev-continuation/both-paused-queues.json, dev-reconstruction.json | PASS baseline, no fresh historical-step claim |
| Dev resumes own checkpoint while plan/all and OPEN block both | dev-resume-summary.json, dev-continuation/dev-resume-result.json | PASS S3.4 continuation |
| Actual plan resumes own checkpoint, pauses empty but OPEN persists | distribution plan P002-continuation-plan/resume.json; dev-observe-plan-resume.json | PASS S3.5 continuation and independent dev observation |
| New actual human dev-role pause | dev-role-pause.json; plan ledger P002-S3.6-dev-role-pause-20261105 | PASS |
| Later separate actual human resolution-only exception | resolution-only.json; plan ledger P002-S3.6-resolution-only-20261105 | PASS: pending=[], unchanged checkpoint bytes, dev PAUSED/role and next=null |
| Later separate actual human final dev resume | final-dev-resume.json; plan ledger P002-S3.7-dev-resume-20261105 | PASS: pauses=[], pending=[], plan=P904/dev=P901 |

Input-form difference at S3.4/5 is explicit: the actual human's one bilateral
resume instruction was applied sequentially by its two actual role writers.
There were not two separate dev-only/plan human utterances. The exact reviewed
P002-resume-20261105 method permitted this while preserving both intermediate
invariants. The later S3.6 pause, resolution-only and S3.7 resume were three
distinct actual user replies; dev directly read each original in session-plan.
No repeated current-resume question, future-input inference or synthetic dialogue.

Final fixture resume commit7a865c904097e8f3c265d771c86b1c0caf0427ac;
evidence HEADd459aea8f44e1727f5c46d98e99220e3a3de5076. Both questions remain
RESOLVED with unchanged fingerprints, prior checkpoint events retained, P902
historical DONE, P904 DRAFT. P901/P903 outputs remain absent until S5.
Actual dev guard worktree/index/HEAD passes. No forced process termination,
remote propagation, other OS/host/model behavior is claimed. Local shared Git
visibility and these two actual chats are the verified boundary. C4/C5 incomplete.
