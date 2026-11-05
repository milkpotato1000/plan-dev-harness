# P002 continuation reconstruction decision request

Common request key: `P002-C3-reconstruction-20261105-v1`.
Status: concrete proposal, pending plan review; no reconstructed live fixture exists.
Scope: existing P002 C3–C5 continuation after loss of temporary Git history.
Adopted distribution plan: `e3e0074202e1f2471b95ea3d5a625c4618ace67d`.
Evidence: `docs/verification/P002/recovery-20261105/inventory.json`.

## Observed facts and existing human answer

Session-dev directly read the actual human's latest session-plan request:
“그럼 P002 시험의 plan/dev 중지를 재개하고 남은 검증도 마무리해줘.”
The current bilateral resume is authorized; do not ask for this answer again.
Remaining S1–S5 coordination was separately authorized by the actual human in
session-dev. The verified same-project session-plan is the decision recipient.
The new request is a reconstruction-method review, not another human resume gate.

The original fixture has 0 files, including 0 Git object/pack files. Directory
names remain. All three original children return rev-parse exit 128. The last
plan/dev/decision SHAs are also absent from the distribution object database.
There is no exact original history to reconnect from these inspected stores.
No global filesystem search, remote recovery, git init or alteration of the
original fixture was attempted. Its empty directory inventory and all 106
existing P002 export files were copied to private preservation storage.

Historical source `77b757cce25dd2f5ee5b3751dbfb26fb70d88d08` is available.
Its 29 recorded assets/script hashes match S0 hashes exactly, VERSION is 0.2.0.
An extracted copy of that source ran bootstrap preview at a separate absent
candidate; exit 0, apply not run, destination still absent. Current 0.2.3 source
and installed skills are not the fixture runtime. No product files were changed.

## Proposed reconstruction, requiring exact reviewed adoption

Use continuation ID `P002-20261029-A-CONT-20261105` and retain original run ID
`P002-20261029-A` inside historical questions, cards and expected marker text.
The continuation is a new repository with new truthful commit SHAs/timestamps,
not restoration of the original Git graph. Keep originals immutable under an
archive/export location and write a machine-readable original→new provenance map.
Never set original SHAs, backdate commits or claim archived output was rerun.

1. Dev performs only the approved infrastructure bootstrap at the previewed new
   absent destination with the historical 0.2.0 source, same original options,
   local hooks and no remote. Compare every generated managed hash against S0;
   disclose any generated contextual path differences. Stop on runtime mismatch.
2. Actual plan imports its own P901–P904 contract/review/scope snapshots and its
   final PAUSED/all checkpoint byte-for-byte from exports. Actual dev imports its
   own final PAUSED/all checkpoint, second OPEN question byte-for-byte, P902
   completed execution snapshot and its actual archived result/marker evidence.
   Dev does not write plan's fixture checkpoint or authored requirements. Plan
   does not merge arbitrary dev implementation to copy completion marks.
3. Plan reviews the archived S1 marker decision and S3 retention decision into a
   new explicit continuation decision commit. Preserve original review contents
   and SHAs as historical provenance. Dev integrates/adopts that exact new SHA.
   P901/P903 remain unexecuted, P904 remains DRAFT and P902 is a carried-forward
   historical completion, never a newly executed test.
4. The first RESOLVED question currently references original decision
   `e6dc181e0a330c7f050fcf70638c5fad2fd8f8ee`. Runtime requires that decision
   to be a real ancestor of adoption, so copying its live record unchanged would
   fail. Proposal: preserve original complete bytes in the archive; in the
   reconstructed live copy change only `> 결정 plan:` to the newly reviewed and
   adopted continuation decision SHA. Record exact old/new hashes and mapping,
   retain immutable question body/state, explicitly label this a metadata
   reconstruction rather than a fresh S1 resolve. Plan must approve this exact
   treatment; no guard weakening or invented old Git objects. Second question
   remains byte-identical OPEN and is resolved only later under S3.6 authority.
5. Prior to either resume, actual roles inspect their own paths/branches and
   export guards (worktree/index/HEAD), adopted SHA, both queues, checkpoint hashes
   and question fingerprint. Required restored baseline: both PAUSED/all,
   next.plan=null, next.dev=null, second OPEN scoped to P901/P903, P902 DONE,
   P904 DRAFT, no P901/P903 marker execution. All rehydration steps are reconstruction
   evidence, not fresh S0–S2 passes or a claim of original-history restoration.
6. Dev then resumes only its own checkpoint using the already verified human
   bilateral instruction. Capture plan/all + second OPEN still blocking both.
   Deliver a substantive fixture action to actual plan, which resumes its own
   checkpoint from the same human instruction. Capture pauses=[] with second OPEN
   still blocking P901/P903. Do not invent two separate human resume utterances.
7. At S3.6 send the required new role-pause/resolve-only input request to plan's
   single user-question ledger. Those future human inputs and S3.7 resume remain
   mandatory at their corresponding steps. Then execute S4's actual two-role
   delivery tests and S5 verification, with distinct current vs archival evidence.

## Decision needed and limits

Recommended: approve this historical-source continuation and the explicit first
resolved-question SHA mapping, with original exports immutable and actual role
writers. Alternative: retain P002 incomplete if this state reconstruction cannot
meet the evidence contract; do not silently restart S0 or weaken C3–C5.
Plan can decide the method within the human's existing remaining-validation scope;
only materially new authority/acceptance changes require a new human question.
Please commit a reviewed method and exact-SHA handoff with next concrete fixture
action. Dev will not bootstrap/apply or resume before adopting that review.

C1/C2 stay historical PASS; C3/C4/C5 remain unchecked. This request creates no
project-wide PLAN_DECISION/OPEN, new runtime feature, skill update, remote,
main promotion, new chat, monitoring loop or permission bypass. Receipt and
review are distinct; no ACK polling. The old stopped fixture is not represented
as a currently functional runtime.
