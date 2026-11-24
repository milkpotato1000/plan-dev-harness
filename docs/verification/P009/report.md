# P009 0.2.4 implementation and validation checkpoint

Client date: 2026-11-24 Asia/Seoul. **Live C3 incomplete: Claude workspace trust required.**
Common result key P009-source-v0.2.4-4c4b5a3; linked preparation/human-input key
P009-live-setup-v0.2.4. No new human decision is requested by this result review.

## Implemented and verified

Exact reviewed P009 dede131be57a3cf07a7ced368f05cb74e2447020 was internally adopted
in 29ac708 after P008 final completion/SENT push. Source implementation commit:
**4c4b5a3f2ef63deeffa425f49c2bc0161cf48d66**, VERSION **0.2.4**, unreleased.

- C1: source skill, generated child/container/role entrypoints, workflow references,
  README/Claude guide/changelog distinguish plan execution approval, internal dev
  exact application and implementation. Independent worker default, no automatic
  plan implementation or completion wait, explicit human selection for sequential
  mode, bootstrap vs authorized dispatch and plan review gateway are explicit.
- C2: native Claude ListAgents/SendMessage and existing Codex list/read/send procedure,
  version/provider/inbound distinctions and read-only worker_doctor implemented.
  Doctor reads actual Git/common directory/branches/queue and explicitly supplied
  role/identity/writer/tool/authority observations, detects stale/ambiguous/missing
  conditions, and optionally reads official CLI inventory. It does not authenticate
  supplied grants, connect a peer, dispatch, apply, retry or change any settings.
  Unavailable/empty inventory is not falsely reported as no host sessions.
- C4: six new behavioral tests exercise read-only and simulation boundaries,
  same session/tree, wrong project/branch, writer conflict, missing native tools/
  authority, held/refused/unknown/failed send, reconnect/staleness, busy-worker safe
  boundary, pause/OPEN preservation and Codex procedure compatibility. Existing
  stateful control/review tests retain deduplication, scoped decisions, event history,
  exact adoption and one common user-question key. These are simulated policy and
  real-Git tests; they do not prove live Claude cooperation or model compliance.

## Automated and installation evidence

**89 tests PASS**, Python3.9.6/macOS, isolated checkout of exact implementation
commit, 161.352s test duration (full-suite.log and suite-result.json).
Worktree/index/exact-source guard and queue pass (guards.json).

Isolated 0.2.4 skill installation passes preview/no writes, apply/version, 44-file
payload/source equality, independent installed CLI/help/bootstrap preview, identical
KEEP and modified/extended target rejection with all bytes preserved. The actual
published v0.2.3 source was installed in another isolated project, then upgraded to
0.2.4 with original options: preview unchanged, doctor/adapter added, existing
extension/work retained; customized managed instructions subsequently refused
without any changes (upgrade.json). Existing full regression covers older upgrades.

The actual user-selected fixture received project-local skill and a new p009
container with independent linked main/plan/dev worktrees. Preview preceded apply,
initial queue is empty, infrastructure adoption/hooks installed, installed doctor
runs on both role worktrees, KEEP confirms identical package. Actual human setup/
test request was directly verified. The coordinator only installed/prepared the
fixture and read state: no P901/P902 card or implementation was authored by it.

## Actual live gate and remaining acceptance

Official host `claude agents --json` confirmed one idle interactive fixture plan
candidate, whereas sandbox inventory had been empty. Identities and full local
setup logs remain private; public evidence uses aliases and sanitized roots.
Claude version observed2.1.318. This inventory is not native messaging proof.

The one authorized independent dev start through official `claude --bg --name`
returned **exit1: Workspace not trusted**. Claude explicitly requires interactive
human trust review in the new fixture dev directory. No new worker started, no
native send was attempted, no permission/inbound/trust configuration was changed,
no socket/terminal injection or alternative route was attempted.

M1 actual send/internal application, M2 separate plan planning during dev execution,
and M3 busy-worker sequential P902 application are **NOT RUN**. C3 remains unchecked.
A background shell or 89 passing tests cannot replace this live criterion. The
original reported two-iTerm incident has no inspected incident logs; its cause
remains unconfirmed. Actual new human P902 conversation must not be fabricated.

A committed preparation packet was actually sent to existing parent plan before
live start. After the trust gate, committed blocker d6ff8bef29570a9849bafc7805bce81348b72d60
and the exact local interactive command/role file were sent through the same
preparation key. Plan owns this one necessary platform-input question. Existing
fixture plan need not restart; after trust, reuse the one actual dev if present,
refresh native binding and continue M1–M3. Never start a duplicate or blindly retry.
All permissions remain per-session; any further necessary dialog stays a real gate.

## Preservation and delivery

P008 main stays 3ede2e81f53be8252b585a57064f225fb711ccea, annotated v0.2.3 object stays
8a603187330c2a7c61636badf8401be68881a206. No0.2.4 main/tag/Release publication.
P002/P005/P006/P007/P008 historical artifacts and failures are byte-preserved.
Personal Codex skill and absent personal Claude skill unchanged; only the explicitly
authorized fixture project-local installation changed. Distribution-local installed
runtime remains its prior managed version; adding source/generated0.2.4 does not
claim an automatic project-wide upgrade (preservation.json).

C5 regression/install/guard/evidence portions pass. The result packet, normal dev
push and actual SENT bookkeeping are recorded separately in result-delivery.md.
This checkpoint is not P009 completion; C3 remains blocked on the actual live gate.
No ACK/completion wait loop or repeated human adoption/approval question was created.
