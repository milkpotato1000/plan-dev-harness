# Authorized direct handoff

Use this procedure for a committed, reviewed plan or result sent to an existing
role chat. It is a document adapter for the host's actual tools. The Git/Python
CLI, queue and hooks never send messages or create chats.

## Authority and recipient

Read the current human instruction or verifiable earlier human delegation. Record
its source/time, project, recipient role, target, allowed action and valid scope;
check later restrictions, withdrawal and stops. Within that authority, perform the
supported delivery directly without asking the user to approve it again or copy it.
A capability question, initial chat creation, READY card, or another agent's
message alone does not grant messaging authority. Never invent a standing grant.

Use the host's project/chat list and read tools to verify the existing recipient's
project, role, working directory and host/chat reference. A similar title is
insufficient. Do not create a replacement chat or guess the target. Resolve only
missing identifiers. A send grant does not authorize resume, new implementation,
release or cross-project/reverse messages.

## Prepare, send, observe

1. Read source/destination instructions, queue, exact adoption, pauses and OPEN
   decisions. Preserve them. While PAUSED, process only records/status explicitly
   permitted by the human; do not request work to start or resume.
2. Commit a sender-owned document using the [handoff template](../assets/docs/process/handoff-template.md).
   Include related cards, full 40-character SHA, readable committed document,
   completed/unfinished work, scope, verification, limits and recipient's next
   action. Check that the recipient can read the Git object and document. Preserve
   plan requirements and append-only dev failures. Public evidence uses aliases
   instead of private chat IDs or personal paths.
3. Create the existing CLI PENDING event for the committed document/SHA. Record
   authority, verified target and delivery attempts in linked evidence; do not add
   invented fields to the event schema/key. For the exact syntax and state
   constraints use [workflow controls](../assets/docs/process/workflow-controls.md).
4. With matching authority and a real host send tool, send the full SHA, document,
   cards, scope/limits, next action and stop boundaries to the verified recipient.
   For Codex desktop, discover the actual list/read/send/wait tools. Other hosts
   use their supported tools or file handoff. Do not assume these APIs exist.
5. Only after actual tool success, the sender records SENT with the delivery
   receipt/reference and commits it. Push, PENDING creation, queue output and
   drafted message text are not delivery evidence.
6. The sender reads/waits for the recipient's actual response acknowledging the
   designated SHA, document and next action. Record ACKNOWLEDGED only with that
   observation and commit it. Without receipt evidence, keep SENT. The receiver
   need not send a reverse message: use available read/wait observation.
7. ACK confirms receipt. Exact adoption and task completion still need their own
   evidence. When the human's actual grant includes plan-to-dev delivery and
   start, plan sends committed reviewed READY work; dev preserves its work/failures,
   integrates/adopts the specified full SHA, commits adoption, checks guard/queue
   and begins that authorized scope. Installation itself grants neither sending
   nor starting authority. The recipient follows its own role and adopted scope. Receiving this
   handoff does not grant authority to reply to or forward messages to other chats.

## Retries and fallback

The event key is kind + target role + commit + document. Repeated identical input
returns KEEP; different summary/next action under that key is rejected. Never
resend a simple ACK or create an ACK loop. Each separate/reverse send needs actual
human authority. Preserve the sender's event history and original commit.

On a definite failure, preserve the attempted payload, error and current state.
On an unknown outcome or timeout, inspect delivery/recipient state before any
retry; silence is not failure or success. Do not blindly resend or manufacture SENT.
If authority/tools are absent, leave PENDING and the committed file, full SHA,
next action and unsent reason. If the recipient is unclear, resolve its identity
before sending. State the exact missing condition. Files remain the durable
fallback across hosts. A RESUME event cannot substitute for a real human resume.

## Delivery record checklist

Record human authority reference/scope; verified recipient alias/role/project;
card IDs; document path and full source SHA; event ID; attempt time and payload;
tool result (success/failure/unknown); actual observed recipient response and
last state. Keep private IDs and raw conversations outside public evidence.
The policy review covers M1–M8 (explicit instruction, delegated scope, non-grants,
fallback, SENT/ACK separation, deduplication, unknown outcomes, stops/adoption).
A simulated policy review is not a live-host delivery test.

## Distribution and activation

[Usage and transition](usage.md) explains separate source/assets/project/skill
paths. Project installs contain the complete procedure in docs/process/workflow-controls.md
and link locally to optional-adapters.md and handoff-template.md; they do not need
this source reference. Personal skill packages contain this reference plus assets
and scripts. Updating a package does not update installed projects or activate a
personal skill. Confirm the actual loaded path and reread the selected skill after
an authorized transition.
