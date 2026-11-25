# P009 supplemental live result — P903/P904

Common review key: P009-C3-supplemental-P903-P904-results.
Linked keys: P009-supplemental-stage-A; P009-live-P901-P902-results; P009-live-setup-v0.2.4.
Source version 0.2.4 remains unreleased. Parent exact decision adopted:
92d38c96cbc49b83a5dd6d7f762285d04673b2ae (adoption commit 6cb5c70).

**C3 remains incomplete.** Actual native delivery, independent plan work while dev was
busy, pending preservation and safe sequential application succeeded. The required new
human P904 input arrived before P903 dispatch/start, so the strict human-turn timing
condition failed. No automatic rerun, new card or lowered criterion follows.

## Evidence and independent verification

Existing fixture-plan and fixture-dev were reused. Official host inventory verified two
distinct existing interactive sessions; both were idle at final observation. Both Git
worktrees were clean. No fixture source/card was authored by the parent observer.
Exact captured final heads:

- plan: 779e2688685f11e8e0ea0ab6aa768d38022959dc
- dev: 1be0f27608ec2a107259daa756634a06cde37292

28 committed fixture files are exported with original and sanitized SHA256 values in
export-manifest.json. Native evidence is a bounded action/queue metadata selection from
these two sessions, with per-source-record hashes. Raw conversations, identities and local
addresses remain private. Native enqueue, mid-turn absorption, local recording and commit
times are separate observations; final commits alone do not prove overlap.

Independent tests on immutable copies of completed fixture code passed: P903 30 tests;
P904 37 tests including earlier regressions. Additional independent CLI expectations passed:
duplicate groups, code-point counts, mixed errors, raw default JSON equivalence to P903,
CSV CRLF/quote/embedded-newline/Unicode roundtrip and stderr/exit 2. Both fixture guards
and queues passed. See independent-checks.json; no tests wrote into fixture worktrees.

## Actual sequence

All times below are 2026-11-25 Asia/Seoul (UTC+09). Raw event timestamps remain UTC.

| Time | Observed action |
| --- | --- |
| 09:31:26.108 | P903 dispatch instruction entered in fixture dev; role retained, no plan dispatch/adoption resulted. |
| 09:31:36.182 | Earlier P904 input in fixture plan; subsequent clarification tool interrupted at 09:31:57.171. No P904 change then. |
| 09:32:06.392 | Actual P903 dispatch instruction in fixture plan. |
| 09:32:14.343 | New P904 input attachment: origin human, humanTurn true. Enqueued 09:32:14.454; absorbed mid-turn 09:32:21.620. This is a real human input, but before P903 dispatch/start. |
| 09:32:31.787 | P903 native SendMessage for exact 6758949e87e8c5c797acd789f4a8deae40d050da. Receiver input 09:32:31.935; native inbox success 09:32:32.057. |
| 09:32:44 | Exact P903 adoption 2ca41fed059826c07a5317ea7d2450d2503cb83f. |
| 09:32:50.293 | One dev STARTED native packet; peer input is not new human input. |
| 09:32:55.282 | Plan action updates P904 card/review from the human's requested defaults. |
| 09:32:59 | Dev records P903 start; first source Write is 09:33:05.968. |
| 09:33:12.486–09:33:13 | Plan action records ACK and commits P904 review 50aa347d87334d51590ba5ba6469247266bce6aa / delivery e5a3da0d913d7b253da3d1a2d24e52a4272b801e, during P903 implementation. |
| 09:33:13 | Dev core checkpoint d8647bab086c55d2dd36bc391c9b93f46e8ff568; CLI/tests still pending, explicitly not a safe P904 boundary. |
| 09:33:22.611 | P904 native send while dev P903 current; receiver peer attachment 09:33:22.707, inbox enqueue 09:33:22.708, native success 09:33:22.854. |
| 09:33:37.488 | Plan returns after SENT, before P903 completion; no completion waiting loop. |
| 09:33:42.334 | Dev writes P903 tests. P904 queue removed/absorbed mid-turn 09:33:43.806. |
| 09:33:51 | Dev records P904 PENDING with P903 current and commits CLI/tests as cb393060e92bdef20533b2da802d9ea5058e58a4. |
| 09:33:58 | P903 completed, 30 tests PASS, commit c3239716dfe8e1e0fbc29c4a694338224a3ae8b3. |
| 09:34:04 | Only after completion: exact P904 adoption afbcbee6f44ba74953f7aa13ad28fb6caecb1539. |
| 09:34:11–09:34:48 | P904 sequential implementation; implementation 1bf5b85dc568577d22659b53c5b4efd0723e822e, 37 tests PASS, completion 7585115b229c7ad90db3e9799415410afd3b0f6b. |
| 09:35:14–09:35:45 | Fixture dev records results send/hash correction; fixture plan commits read-only results review with the same timing limitation. |

The fresh human P904 input preceded P903 native dispatch by 17.444 seconds, the declared
implementation start by 44.657 seconds, and the first source Write by 51.625 seconds.
Human-turn timing therefore fails even though review/commit/send overlaps actual dev work.
The P904 receiver attachment precedes P903 completion by 35.293 seconds; its absorption
and pending record also precede completion. This supplies the busy-reception evidence
missing in the first run. Exact P904 adoption follows the actual completion boundary.

## Reconciliation and preserved failures

Fixture plan's local SENT timestamps 09:32:36 and 09:33:27 describe bookkeeping, not the
native send instants. Its results review reports P904 input time as not exactly known and
inbox time as inferred; the bounded native metadata above resolves those uncertainties.
The human input was queued during an existing plan turn, not sent after dev had started.
Do not relabel its later review work as a later human input.

Fixture dev's 09:33:51 receipt timestamp is a record time; the peer arrival and absorption
are earlier. Its result packet used an erroneous placeholder P904 implementation hash;
1be0f276 records the correction to full 1bf5b85dc568577d22659b53c5b4efd0723e822e. Original
packet/history are preserved, not silently rewritten or resent.

Preservation verification compared ownership correctly: P901/P902 code/tests/cards and
dev-owned old evidence match prior dev c387f9d. Old plan timeline/review match prior final
plan bd8d5f9, inherited by exact adoption. Comparing all old plan-owned evidence to the older
dev baseline initially flagged already-existing plan corrections; no new corruption was found.
Parent first-live/Stage-A evidence directories remain unchanged. Parent source is unchanged
from 4c4b5a3f2ef63deeffa425f49c2bc0161cf48d66; existing 89-test evidence was not rerun.
Main and v0.2.3 still resolve to 3ede2e81f53be8252b585a57064f225fb711ccea. No release,
personal installation, worker replacement, fixture reset, artificial delay or permission
change was performed. The fixture has no remote; parent evidence delivery uses origin/dev.

## Result for parent plan

M1 PASS; real planning-work overlap demonstrated; M3 busy reception, pending preservation
and safe sequential execution PASS. Required fresh human turn during implementation FAIL.
C3 remains unchecked pending parent review, under the unchanged supplemental contract.
Review these concrete artifacts and the timing gap. No repeated trust/adoption question,
ACK loop, automatic additional test or new human action was requested by the observer.
