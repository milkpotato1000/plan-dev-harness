# P002 events

| Run/stage | Role/action | Expected / actual | Commit / evidence |
| --- | --- | --- | --- |
| P002-20261029-A / S0 prep | session-dev integrated exact reviewed plan | exact adoption, guards pass / observed | 77b757cce25dd2f5ee5b3751dbfb26fb70d88d08; S0/commands.json |
| same / S0 prep | session-dev previewed and created absent isolated fixture | no remote, runtime matches, empty queue / observed | S0/hashes.json; S0/dev-initial-queue.json |
| same / S0 participant gate | session-plan confirmation and fixture plan card commit | required / not yet observed | report.md; resume at S0 |

Timestamps, command inputs, output, exit codes and fixture commits are in S0/commands.json.
No counterpart observation commit is asserted before its actual participation.

| P002-20261029-A / S0 recheck 2026-10-30T11:37:48+09:00 | session-dev received follow-up and revalidated retained fixture | clean/original hashes/guards/no records expected; observed | S0/recheck-20261030.json |
| same / S0 actual input request | session-dev showed exact per-role paths and human message text in this dev chat | real user participation and plan card SHA required; pending | S0/next-input.md |

| P002-20261029-A / S0 actual roles | user instructed dev participation and plan relay; separate plan read the human source and authored its cards | both roles distinct; observed | plan 11706bf5ea2b4091be46784911ad38a4f2e507e0; dev participation 749054a149134767b7eb613fc311b785e85a59b7 |
| same / S0 exact adoption | session-dev integrated and adopted that exact plan | next.plan=P904, next.dev=P901, no controls; observed | 632cc4b4ab5c57546c6fd505cb558e17ed19bbb1; S0/result.md |
| same / S1 step 1 | session-dev committed marker question | unclassified OPEN blocks all dev; next.dev=null; observed | 5295c5b0722e77de276e1a502be691402cc5c0f1; S1/01-unclassified-queue.json |
| same / S1 peer gate 2026-10-30T11:44:40+09:00 | session-dev prepared next classification input | awaiting actual plan commit and applicable delivery authority | S1/next-plan-action.md |

- 2026-10-30T11:51:49+09:00 | P002-20261029-A | S1 | session-dev/session-plan | separate scope and decision, exact adoption, actual P902, rejected resolves, valid resolve | expected=actual PASS | dev 295237313c3e36025b67e1b65cd1ddfb05230424 | plan e6dc181e0a330c7f050fcf70638c5fad2fd8f8ee | S1/result.md

- 2026-10-30T12:00:38+09:00 | P002-20261029-A | S2 | session-plan/session-dev | actual human role pause; pre/post commit visibility | expected=actual | plan 3bab8892fa6fa503b94a54f1ce109d07bcd4427c, dev295237313c3e36025b67e1b65cd1ddfb05230424 | S2/observation.md | human resume pending
