# Optional Codex desktop chat adapter

This reference applies only when the host actually exposes the listed app tools.
Claude Code uses its native ListAgents/SendMessage adapter when available; see
[Claude worker setup](claude-workers.md). Do not assume Codex app APIs exist there.

# Separate plan and dev chats in one project

Use this workflow only when the user explicitly asks to create the chats.
Update the reusable harness and requested project rules first. List saved
projects and select the exact workspace container path; a similar label or a
cached isGitRepository flag is not evidence of the actual filesystem layout.
List existing chats to avoid accidental duplicates. When the user asks for new
chats despite an existing pair, create the new pair and use a short distinguishing
suffix if helpful. Preserve the earlier chats unless the user asks to rename,
archive or remove them.

Create two chats with `create_thread`, both targeting the same saved project's
local environment. Do not create another worktree, use a cloud chat, invent a
project id or edit app-internal state. Omit model/thinking unless the user has
requested them. Suggested titles are `[plan] <project>` and `[dev] <project>`.
If no saved project matches, report that it must first be opened/registered in
the app; do not claim an unrelated or projectless chat is attached to it.

Adapt [the plan prompt](../assets/workspace/plan-chat.md.template) and
[the dev prompt](../assets/workspace/dev-chat.md.template). Substitute real
container/child paths, project name and configured branch names. The prompt must
assign a persistent role even though both chats start at the container. Read the
container and selected child's AGENTS.md before Git/scripts; use explicit child
working directories. Bootstrap reads status, branch, rules, queue and relevant
baseline/history, then reports readiness and waits. Do not generate new P-cards,
implement queued work, merge/adopt/commit/push, message another chat or start an
automation merely to initialize a chat.

After creation, wait for both bootstraps using `wait_threads` with their returned
host/thread ids and cursors. Confirm their initial context selected the intended
child/branch and only performed read-only actions. If creation returns an unknown
outcome, inspect the chat list before retrying; do not create extra copies.
Use `set_thread_title` if normalization removed the role label, then use the exact
verified returned titles when identifying the chats. Emit one created-thread
directive per new chat in the final answer. The creation request authorizes the
initial prompt, not unrelated follow-up messages to old or new chats.

## Later delivery to an existing chat

After read-only bootstrap, a separately authorized handoff follows
[direct handoff](direct-handoff.md). Verify the current project/role/child and the
human instruction or scoped delegation; send the committed exact SHA and next
action directly when supported. Commit/push actual SENT and finish the plan turn;
do not wait for ACK, adoption or dev completion. Observe ACK only on a later natural
planning/status request. Busy dev preserves current work and adopts reviewed exact
handoffs at a safe completed/checkpointed commit boundary, then follows priorities,
dependencies and stops. See the shared asynchronous handoff rules.
Initial chat creation alone is not this authority. Receiving a handoff does not
authorize reverse/chain messages or user resume; bootstrap itself remains read-only.

인간이 해당 프로젝트의 plan→dev 전달·착수를 위임한 경우 plan은 검토된 READY 계획의 정확 SHA를
확인된 기존 dev에 직접 전달하고, dev는 기존 작업·실패를 보존해 통합·정확 채택·커밋·guard/큐
확인 후 승인 범위를 시작합니다. 설치 자체는 위임이 아니며 초기화는 읽기 전용 대기를 유지합니다.

## Fresh sessions and document delivery

Use the shared [startup and delivery rules](../assets/instructions/agent-workflow.md#fresh-sessions-and-document-delivery).
Read actual files/branch/adoption/queue/stops and check writers before material writes.
Preserve an assigned role; unassigned changes use an existing suitable P card or a
reviewed new one, then exact dev adoption and implementation. Plan does not implement
product README/user guides; planning-only drafts may finish on plan, and read-only
questions need no card. Record file/repository/target ref and verify actual delivery;
plan push, dev adoption and default-branch visibility are separate outcomes.
Only an explicit human selection of sequential mode permits both roles in one session.
Bootstrap, absent messaging authority and scoped pauses retain their boundaries.

## User review gateway

Use the [result review protocol](user-review.md): dev commits evidence, artifact
version/hash, shared request key, question scope and existing human-answer sources.
Plan owns read-only result review and necessary human questions, reuses valid
pending/answered scopes across roles and records decisions for exact dev adoption.
Dev does not ask routine completion confirmations. Optional review, required human
criteria and critical OPEN remain distinct. User code questions in dev are allowed.
Reverse delivery needs a real human project grant; no permission or pause bypass.
Preserve asynchronous SENT-then-return and busy-role safe boundaries.

## Independent worker execution

Default to distinct plan and dev host sessions with one writer per worktree.
Plan records the human execution approval/delegated scope, prepares reviewed READY
work and sends the exact commit to the verified independent dev, records the actual
outcome and returns to planning. Plan must not implement products in either tree,
run dev adoption for the worker, or wait/poll for ACK, adoption or completion.
Dev performs internal receive/integrate/adopt at a safe committed boundary without
asking the human to type another adoption message. Keep the existing adopt CLI and
record formats; a peer message is not new human authority. Preserve current work,
failed evidence, priorities/dependencies, OPEN decisions and explicit pauses.

Missing worker, native tools, matching human grant, distinct identity or unambiguous
recipient means pending handoff with the exact missing condition. A held/refused or
unknown send is not SENT; preserve attempt evidence without blind retries. Never
replace a parallel request with plan doing dev work. Sequential dual-role mode is
available only after a separate explicit human choice of that mode and exclusive
writers; a general request to finish work is insufficient. Do not automatically
create extra workers, enable teams, change permissions/inbound settings or start a daemon.
Bootstrap-only requests remain read-only and wait. A subsequent authorized work
handoff is distinct and can execute without a second human adoption prompt.
Use the read-only worker doctor and native host procedure; diagnostics never
approve, send, adopt or run work. Send results/needed decisions through the plan
review gateway with one request key; no duplicate user completion questions.

See [Claude workers](claude-workers.md) and the installed worker-adapters procedure.
