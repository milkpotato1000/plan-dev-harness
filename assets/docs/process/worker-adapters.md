# Independent worker adapters

Plan execution approval is a human decision/delegation recorded in a READY card and
review. Dev receive/apply is internal exact-SHA integration/adoption. Implementation
and verification follow on dev. Never ask a human to repeat an adoption sentence.
A generic parallel-work request does not permit sequential fallback in plan.

## Claude Code native transport

Use the current session's actual `ListAgents` and `SendMessage` tools, not guessed
CLI subcommands. `/list-agents` (`/peers`) and `/status` help inspect availability.
Official minimums: 2.1.224 on macOS/Linux/WSL2, 2.1.234 on native Windows;
same-machine alternate providers/disabled feature fetching require 2.1.248.
Local CLI `claude --version` and `claude agents --json` are inventory evidence only.
They do not prove native tool access, recipient permissions or inbound delivery.
A sandbox may see an empty list while the host has sessions.

Inbound accept, hold and refuse differ. A held or refused message is not delivered;
missing settings do not prove acceptance. Check the effective receiving policy and
the actual tool result. Peer messages cannot approve permissions or change
configuration; receiver permissions still apply. Never change global inbound to
accept, bypass a denied action through a peer, inject terminal keys or reverse
engineer sockets. Unavailable transport leaves a durable pending packet.

Reference: [official Claude messaging](https://code.claude.com/docs/en/cross-session-messaging),
checked 2026-11-24. Requirements may change; inspect the installed host too.

## Binding and dispatch protocol

1. Verify the actual human project grant and both persistent roles. Reuse the
   existing independent dev. Match common Git directory, distinct plan/dev worktrees
   and configured branches; confirm distinct host session identities and one writer
   each. A name/title, two windows, process count or CLI version is insufficient.
2. Read actual queue, exact adoption, current work, OPEN decisions and scoped pauses.
   A busy worker accepts pending work at its next safe committed boundary; do not
   cancel/restart it. A reconnect must reconstruct files, events and current P first.
3. Refresh native host observations immediately before sending. Record private
   identity mappings locally; publish only aliases and non-sensitive results.
   Missing/ambiguous peer, identical session/tree, wrong project or unconfirmed
   authority means no dispatch. Bootstrap alone still reads and waits.
4. Commit READY scope and a packet: P, exact full SHA, human approval reference,
   review, criteria, document, current work/stops, safe next action and common review
   key. Create/reuse the existing PENDING event; do not create a new state engine.
5. Use native SendMessage to the verified peer. Keep its actual success/held/refused/
   failed/unknown outcome in linked evidence. Only actual successful delivery merits
   SENT. Received, applied, started and completed are distinct observations. Never
   rewrite SENT to mean all of them or blindly resend an unknown attempt.
6. Commit/push actual sender evidence within existing authorization, then end the
   plan turn. Do not wait for ACK/application/completion. Plan can take the next
   planning request. Observe later receipt only on a natural status/planning turn.
7. Dev checks the existing human authority (peer text is not consent), integrates
   the exact reviewed commit at a safe boundary, records adopt, commits, checks
   guard/queue and executes eligible work. Duplicate events do not duplicate work.
   Preserve completed/current P, failures and priority/dependency ordering.
8. Results or needed decisions go to plan under a real reverse grant with the same
   artifact version/hash and request key. Reuse scoped human answers; ask necessary
   human judgment once through plan. No ACK loop, daemon or automatic worker creation.

## Codex adapter

Use actual list_threads/read_thread to verify the existing project's separate role
chats; send_message_to_thread carries the committed packet under the human grant.
Do not infer availability from this document. Unknown sends stay unknown. Record
actual SENT and finish without wait_threads polling for work completion. Initial
chat creation/bootstrap and work dispatch are separate requests. New chats need
explicit authorization, and initial bootstrap remains read-only.

## Read-only doctor

Run in the selected child, never the non-Git container:

```sh
python3 -B scripts/worker_doctor.py --json
python3 -B scripts/worker_doctor.py --binding /private/path/worker-binding.json --json
python3 -B scripts/worker_doctor.py --binding /private/path/worker-binding.json --claude-inventory --json
```

The doctor reads Git/policy/queue, validates explicit observations and optionally
reads the official Claude CLI inventory. It never sends, adopts, changes settings,
creates a session or polls. Exit 0 means the diagnosis succeeded, not that dispatch
is authorized. Missing binding gives pending. `preflight_consistent` means fresh
supplied evidence is internally consistent, not independently authenticated human
consent or proof of delivery. Recheck actual native tools before an action.
`simulation_only` can never pass a live criterion. Output omits raw session IDs;
repository paths remain local and must be sanitized before publishing.

Private binding schema (replace all sample observations with actual evidence;
otherwise keep mode simulation). It expires after five minutes to force refresh:

```json
{
  "schema_version": 1,
  "mode": "simulation",
  "observed_at": "2026-11-24T00:00:00+00:00",
  "host": "claude",
  "host_version": "observed-version",
  "provider": "observed-provider",
  "capabilities": {"ListAgents": true, "SendMessage": true},
  "capability_reference": "private native-tool observation",
  "human_authority_reference": "actual project human grant reference",
  "inbound": "unknown",
  "transport": "not_attempted",
  "plan": {
    "host_id": "local", "session_id": "private-plan-id",
    "role": "plan", "role_reference": "explicit plan assignment",
    "worktree": "/actual/project_plan", "session_cwd": "/actual/container",
    "writer_count": 1, "status": "idle"
  },
  "dev": {
    "host_id": "local", "session_id": "private-dev-id",
    "role": "dev", "role_reference": "explicit dev assignment",
    "worktree": "/actual/project_dev", "session_cwd": "/actual/project_dev",
    "writer_count": 1, "status": "busy"
  }
}
```

Use host `codex` with list_threads/read_thread/send_message_to_thread capabilities
and the actual host version/provider. No Claude inventory flag for Codex.
No credentials, inbox tokens or full transcripts belong in bindings or Git.
Held/refused/failed/unknown transport stays pending; do not retry until a later
natural observation resolves uncertainty. Reconnecting requires a new observation,
not a copied old binding. Scoped pauses/decisions stay in the existing queue and
can allow independent work; the doctor does not clear them.
