# Project-local session registration (source 0.2.5)

Registration is an observation, never work approval, a send, a writer takeover or a
pause/resume. Use the existing explicit plan/dev roles and actual human project grant.
This is SKILL + CLI installation, not a marketplace plugin. macOS/Linux, Python 3.9+
and Git are required; Windows locking and shell hooks are not supported by this version.

## Configure once

Install/integrate the runtime first, then preview from either role worktree:

```sh
python3 scripts/configure_sessions.py --plan /absolute/project_plan --dev /absolute/project_dev --role-reference 'Existing human assignment to plan and dev'
```

Review CREATE/UPDATE/KEEP and repeat with `--apply` under setup authorization. The
explicit mapping checks actual worktree roots, distinct branches and one Git common-dir.
A separate clone is a separate project, even with the same remote or display name.
The installer writes only project-local Claude `settings.local.json`, Codex `hooks.json`,
Git-local excludes and the private project mapping. Existing user keys/hooks/permission
settings remain. Customized owned hooks or ambiguous inline Codex hooks are conflicts.
Repeated installation is KEEP. Role/path/branch changes require explicit reviewed
migration; moving a folder does not change an assigned role. No trust setting is changed.

Start the ordinary `claude` or `codex` from the configured role worktree. Official
SessionStart input supplies the actual identity; no session ID copying is necessary.
UserPromptSubmit/Stop refresh busy/idle observation; SessionEnd records an end. Startup
only registers and reports a short status to stderr. It never runs tasks or sends peers.
Unknown prompt/tool/transcript fields are ignored and never persisted. Two-second host
hook timeouts, bounded input/output and nonblocking locks prevent startup waiting loops.
Host project/hook trust remains a real host prerequisite. Do not use bypass flags.

A desktop chat sharing a parent cwd with the other role must NOT run both role hooks.
This CLI hook setup requires the actual role worktree cwd; shared-parent app binding is
pending until the host can supply an unambiguous role-specific entry. Existing app
exact-SHA send tools remain usable with their own explicit roles and authorization.
Do not infer role from chat title or create new user-owned chats as a fallback.

## Registry and reconnection

The registry lives under `<git-common-dir>/plan-dev-sessions/`, outside tracked files.
Directory mode 0700; new files 0600; schema 1; maximum JSON size 1 MiB (configuration
64 KiB, hook input 64 KiB). It stores two current role records with host namespace,
actual identity, canonical worktree/branch, monotonically assigned generation, observation
time and lifecycle source/capability. It does not store credentials, prompts, transcripts
or command bodies. A local user can forge observations; this is not an authentication
boundary. Fresh official host checks are required before delivery.

Kernel advisory locks are nonblocking and released on process death; the lock filename
is retained. Writes use fsync plus atomic replacement. Do not delete a lock as a takeover
mechanism. Corrupt/oversized/symlink data fails closed without resetting it. Clock reversal
and future observations fail closed. Supplied expected generations reject stale updates.
Same live identity resumes idempotently without a new generation or current-P changes.
A new identity requires the previous identity's explicit matching end AND fresh official
inventory confirming the sole replacement in that worktree and absence of the old one.
TTL expiry or an empty inventory alone never frees ownership. A late old-ID end cannot
remove the replacement; retired identities are retained (maximum 64) to reject replay.
A closed same-ID resume also requires fresh positive host proof; without proof it is pending.

Competing identities preserve the current writer and record bounded conflict fingerprints
(maximum 16). A matching contender end clears its own conflict only. Busy/unknown/crashed
writers are never automatically replaced. Reaching a bound requires explicit plan-led
maintenance; no automatic eviction/cleanup can accidentally free a live writer. Missing
peer remains pending until the next ordinary lookup/event, with no daemon or polling.

## Discover and hand off

```sh
python3 scripts/session_registry.py --repo . --host claude doctor --live
```

Doctor is read-only; it does not install hooks/register/send. Default output omits IDs.
`--private` exposes IDs locally for the host adapter; never commit that output. It checks
registry identity, worktree/branch, freshness (five minutes), collisions and existing queue
controls. A quiet session can be stale; that is not permission to replace it. Registration
and reconnect never alter adoption, P status, decisions or pauses.

Create and commit the normal exact reviewed PENDING handoff event first. Then resolve:

```sh
python3 scripts/session_handoff.py --repo . --host claude --event docs/progress/handoffs/plan/EVENT.json --authority-reference 'Existing committed human project delegation'
```

The result contains private native SendMessage arguments. The current host agent must
verify native tools, inbound state and the actual human grant, send to that exact identity,
and record actual SENT through the existing workflow. Native inbox success is distinct
from peer receipt, exact internal application and completion. Busy dev preserves its P
until a real safe boundary. No new human adoption input is needed.

For Codex, export a fresh official app-tool observation locally (no human ID copying):
`{host:"codex", source:"codex_app_tools", observed_at:<UTC>, sessions:[{sessionId:<actual>, cwd:<actual>, status:"idle"|"busy"}]}`.
Use valid JSON, not the explanatory notation above. Pass its file as `--host-observation`.
The adapter emits existing app-tool arguments or a CLI queue argv. A supplied observation
is not independently authenticated: the host agent must obtain it from real tools and
check actual recipient permissions. Claude native-tool observations use the same envelope
with host `claude` and source `claude_native_tools`. The envelope expires after 30 seconds. With that same actual host observation, the agent
can complete a pending reconnect without copying an ID:
`python3 scripts/session_registry.py --repo . --host codex reconnect --role dev --host-observation /private/local-observation.json`.
This verified-host entry selects only the single actual session at the explicit worktree;
it retains the old writer unless matching end plus positive replacement proof are present.
It is an explicit registry update, not the read-only doctor or permission to execute work.

Codex CLI `--enqueue` is an explicit action after these checks. Installed `queue --help`
is checked; only `--thread` and `--message` are used. No `--resume`, worker creation or
restart. A bounded local delivery ledger records an attempt before the call. Unknown or
already attempted keys are not retried. Success means queue acceptance only; the existing
workflow event is left unchanged until actual delivery evidence is available. Maximum 128
attempts, then explicit maintenance. No source command text is retained in the ledger.

## Host scope and live limits

Official documents checked 2026-11-26:
[Claude hooks](https://code.claude.com/docs/en/hooks),
[Claude messaging](https://code.claude.com/docs/en/cross-session-messaging),
[Codex hooks](https://learn.chatgpt.com/docs/hooks),
[Codex commands](https://learn.chatgpt.com/docs/developer-commands).
Local capability baseline: Claude 2.1.332, Codex CLI 0.160.1. These are observed versions,
not proof all older versions work. Unsupported events/settings/transports remain pending.
Codex 0.160.1 `agents` has no documented JSON inventory and `queue` has no `--resume`.
Codex automatic replacement cannot claim fresh host proof from that CLI alone; existing
app tools or future verified official inventory are needed. Claude uses official
`claude agents --json`; an empty sandbox view is not proof that the host has no sessions.
No new Claude↔Codex bridge, raw sockets, terminal injection or broad inbound permissions.

Two-session actual startup/reconnect/delivery remains a separate live gate. Simulated
stdin or a stored queue is not a live PASS. Prepare isolated targets and route any concrete
trust/interactive prerequisite once through plan. Keep existing projects/global settings,
user stops and earlier failures intact; no forced restarts or timing-based human tests.
