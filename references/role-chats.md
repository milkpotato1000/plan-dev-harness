# Optional Codex desktop chat adapter

This reference applies only when the host actually exposes the listed app tools.
Claude Code and other hosts use separate user-started sessions with the same prompt
templates and Git handoff; do not assume these app APIs exist there.

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
