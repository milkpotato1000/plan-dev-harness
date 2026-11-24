# P009 live execution — 2026-11-25 (Asia/Seoul)

**P901/P902 native delivery and sequential execution succeeded; C3 remains incomplete.**
Review key: P009-live-P901-P902-results (same fixture result key); linked preparation
key P009-live-setup-v0.2.4. Source version0.2.4 remains unreleased.

Actual human “dev 실행했어” was directly verified in the existing parent plan chat.
Exact reviewed response/delivery a5a967de133512106eb65f8ecf48290b598c019e was applied
internally (parent dev adoption a12169f). No repeated trust/adoption input, permission
change, restart or new worker. Observer used only existing fixture sessions and
read-only Git/file/native-event observations, plus test verification after dev idle.

## Actual outcome

| Step | Evidence | Result |
| --- | --- | --- |
| Independent roles | Official host inventory and bounded native-tool metadata; separate interactive sessions/processes/cwds; same fixture Git common directory | Confirmed; aliases only published |
| P901 plan → dev | Native send08:43:06; exact63da7b6b8a569623b0d410e1f1f8e79b6abdb358 applied at58bad43 | M1 passed; no human adoption sentence |
| P901 implementation | 126016f;10tests PASS; completion d6b7363 at08:44:00 | Confirmed |
| Next plan turn | P901 sender final08:43:23.910; STARTED peer input08:43:23.951; P902 card/review write08:43:47.211 | Separate model planning overlaps real P901 work |
| P902 review/send | Reviewed commit08:44:02; native send08:44:11.562; receiver input08:44:11.766 | After P901 complete; **busy reception not exercised** |
| P902 internal application | Exactf69f30ae9763dd05085003d8151b0a7d6d134d9c applied atbffaad7,08:44:20 | Safe sequential boundary, P901 preserved |
| P902 implementation | 5810133;16tests PASS including P901; completion29872f3 at08:44:51 | Confirmed |
| Results to fixture plan | Native result packet with common key; plan reads dev evidence and records review bd8d5f9 | Confirmed; no completion wait loop |

Times in the table are 2026-11-25 UTC+09. observations.json retains UTC source times.
Final fixture plan bd8d5f92ad09f6c0ce65ecc328df83d4087ad98e and dev
c387f9d536d7d500b4c18a99ca9422d12f90d152 are clean. Both sessions observed idle.
Observer reran the16tests with -B (no bytecode writes), dev guard and both queues;
all passed. Fixture has no remote; no fixture push, cleanup or session shutdown.

## Acceptance limits and conflicting claims

M2's technical overlap is supported by actual native Bash action08:43:47.211 writing
P902 card and review, not only file mtimes or inference from a later commit. P901
was still active until08:44:00. However there was **no new human P902 conversation**:
the next turn was triggered by a peer STARTED message under the prior fixture scope.
Do not claim the user continued a new planning conversation or that all of M2 passed.

M3 requires P902 delivery while P901 is busy, preserving it until a safe boundary.
Actual arrival was11.766seconds after P901 completed. Later safe application proves
ordering but cannot prove busy-message handling. Full C3 remains unchecked.
P901's real work was short (~31seconds); neither role added artificial sleeps.

Fixture plan initially claimed send happened during P901 work. Its later results
review corrected the acceptance conclusion. An older SENT-history description and
one timeline row still repeat the initial claim; exports preserve them as historical
claims, not trusted timing. Native timestamps and Git commits control this verdict.
Fixture dev inferred no planning overlap from commit times alone; bounded native
write metadata adds evidence of drafting overlap but does not rescue M3/full C3.
No fixture records were edited by the parent observer to reconcile these claims.

Native ListAgents did not expose peer cwd in the sessions. Parent observer separately
matched the official host inventory's private identities/cwds and actual Git roots;
this validates the observed pair, not automatic discovery by the installed doctor.
Claude version was2.1.331 for this run (earlier setup2.1.318 retained as history).
Actual permission/trust clicks and effective global policy were not inspected;
successful native delivery is not a blanket permission grant.

## Evidence and next decision

24 selected committed fixture files exported with original and redacted SHA256 in
export-manifest.json. Roots, peer names/addresses and UUID identities were replaced
with aliases. Private originals/limited native metadata remain local; no full session
transcript, credential or private mapping is published. observations.json is a bounded
cross-check, independent-checks.json contains observer verification. Earlier failed
start and P009 source/install/89test evidence remain unchanged; source payload did
not change, so no redundant full regression was needed. P008 main/tag and personal
skills are unchanged.

Parent plan should prepare a bounded supplemental live scenario that can naturally
keep meaningful first-task work active long enough for the reviewed second handoff,
using the existing workers and preserving these completed cards/failures. Do not
retroactively relax C3, add artificial sleeps, reset/rewrite P901/P902, manufacture
a human planning turn, or automatically spawn/restart a worker. This is a test
adequacy/next-scenario review within P009, not a new trust question or0.2.4 release.
The observer has not authored a replacement fixture contract or executed its work.
Any genuinely necessary new human interaction remains the plan gateway's one scoped
question, connected to the existing preparation key.
