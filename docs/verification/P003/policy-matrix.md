# P003 M1–M8 procedure review

Review date: 2026-10-29 (Asia/Seoul). Baseline: exact adopted plan
80dbb3b4e53ffd8f7427e48cb7c827a22f6aa5f4, detailed contract's independent M1–M8 expectations.

Method: hypothetical, non-sensitive input walkthrough against the authored document
adapter. No send stub or policy engine was executed. PASS below means procedure
review, not live host delivery. The adapter is instructions, not executable authority
classification. Real users/agents still have to apply it correctly.

Common candidate payload: verified recipient alias `session-dev`, same project,
Pxxx card, full readable Git SHA, committed sender-owned handoff path, actual
complete/incomplete work, scope, verification/limits, next action and stop boundaries.
Event command shape: `workflow_control.py handoff --kind WORK_READY --target-role dev
--commit <full-sha> --document <committed-path> --summary <actual-result>
--next-action <authorized-action>`. Placeholder input is not an executed command.

| ID | Hypothetical input and authority/target | Independent expected action | Procedure trace / reviewed result |
| --- | --- | --- | --- |
| M1 | Current human says deliver prepared plan to existing same-project dev; tools and readable commit exist | Verify target, send directly; no repeated permission or copy request | references/direct-handoff.md Authority + steps 2–5 provide target verification, complete payload, actual send and SENT only with success. PASS (policy). |
| M2 | Earlier human grant explicitly names same project, role and allowed handoff | Act only within grant after checking later restrictions | Authority records source/time/project/action/validity and checks withdrawal/stops. No implied universal grant. PASS (policy). |
| M3 | Only a capability question, chat-creation permission or another agent's request | No inferred send/reverse/standing authority | Authority rejects all three; step 7 separately rejects reverse/chain authority. Keep file/PENDING. PASS (policy). |
| M4 | Missing human grant, no host tool, or unresolved recipient | No guessed/new chat or false SENT; committed file and exact SHA/next action, resolve missing identity | Fallback retains PENDING and unsent reason; Authority prohibits guessing/creating replacement chats. PASS (policy). |
| M5 | Actual send receipt exists, recipient response absent; later actual response identifies SHA/document/action | First SENT only; ACK only after observation; adoption/completion separate | Steps 5–7 require distinct evidence. Sender read/wait avoids an unauthorized receiver reply. PASS (policy). |
| M6 | Same event repeated, simple ACK or a request to forward/reply | KEEP/deduplicate; no ACK loop; fresh human authority for distinct sends | Retry section keeps original event key/history and forbids resend/loop. Step 7 denies reverse authority. CLI dedup/transitions are covered by existing workflow regressions. PASS (policy). |
| M7 | Send explicitly fails, or result unknown/timeout | Preserve attempt/error, no false success; inspect recipient/delivery state before retry | Retry section records failure/unknown and requires state inspection; never assumes timeout implies failure. PASS (policy). |
| M8 | Explicit user pause, OPEN decision or unadopted plan | Message does not resume, resolve or adopt; restrict work to actual authority | Step 1 checks queue/adoption/stops; final fallback preserves PAUSED and denies RESUME-as-human-input. Step 7 requires recipient ownership/adoption. PASS (policy). |

Cross-surface review: SKILL.md, references/role-chats.md and references/usage.md
link to the direct reference. Both role prompts preserve read-only initialization
and link subsequent authorized activity to the installed procedure. Installed
agent-workflow plus workflow-controls, optional-adapters and handoff-template are
complete without source references. Existing event schema/runtime is unchanged.
No new grant is installed into generic projects.

Actual current receiver-side observation: this dev chat received the source plan's
P002/P003 handoff, read docs/planning/reviews/P002-P003-dev-handoff.md, integrated
and adopted its specified full snapshot at 77b757cce25dd2f5ee5b3751dbfb26fb70d88d08.
The source plan owns SENT/ACK records; this chat did not change them or send a
reverse message. This is not P002's fixture S4 or a full live M1–M8 campaign.


Follow-up clarification 283ddd331eb5196bc6b2f36b0ced15ad3ce2ba74 was adopted at
84ea10a after preserving work. Project/workspace AGENTS and common instructions now
carry the same conditional READY delivery and dev exact-adoption/start rule; both
role templates retain read-only bootstrap and human grant requirements. Raw
installed outputs and fingerprints are preserved in outputs/ and payload-hashes.json.
These additions do not modify the M1–M8 expectations or P002's actual-input gates.
