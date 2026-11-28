# P010 continue-input observation

Common key: P010-session-registration-reconnect.
Source 0.2.5: e044e3e7f11ef48d4f9cc4fa41cad7ac00d8e1c8.
Exact parent review adopted: ee7db607a364f48e76366a497a968821a93df75d.
Observation: 2026-11-28T04:09:00.341227+00:00 (13:09:00 Asia/Seoul).

## Result

P901 has not been handed off in the observed fixture. Both worktrees are clean;
plan remains c5d29c7dd4f3449309e5db2bdf38d4b3df2646f8 and dev remains
a8f39aef5be29989f5655cc0569a3061ad19f277. Both have no P card.
The official unsandboxed host inventory identifies exactly one idle session at each
configured role root. Only those two matching session record files were inspected.

The actual human's continue-input confirmation is accepted as a human report.
The corresponding new input is not observed in either matched session's records.
Plan has only its initial human input at 2026-11-27T16:44:35.634Z (01:44:35 KST);
dev has only its initial input at16:45:11.751Z. Neither has a queued-input attachment.
There are zero timestamped records or tool calls after16:49:00Z in either file and
zero native SendMessage tool uses throughout these two sessions. Last timestamped
records are16:48:11.584Z/16:48:48.114Z respectively. Input contents, raw identities,
transcript paths and unrelated hooks are excluded from published evidence.

Both readonly live doctors return plan_stale_or_future and dev_stale_or_future,
dispatch pending. Their last observed_at values remain16:45:10.150534Z and
16:45:46.726154Z. Exit0 means the diagnostic completed, not successful dispatch.
The startup registration PASS remains valid at its original checkpoint.

## Diagnosis and limits

The earliest unverified step is receipt/processing of the continue input by the
existing fixture plan. No attempted P901 dispatch or input-triggered tool/hook error
is recorded, so freshness is a separately observed dispatch restriction, not a proven
cause of the missing input. Process idle alone does not establish a UI/permission
prompt, submission failure, wrong terminal, crash, or a host bug. Those causes remain
unknown; do not infer them or ask the human to repeat the same continue instruction.

The parent lacks Claude native ListAgents/SendMessage tools. The observer does not
write fixture cards, refresh registration timestamps, restart sessions, inject keys,
inspect unrelated sessions or bypass freshness. Reconnect remains unstarted because
first-task completion is absent. Codex actual two-session validation remains NOTRUN.
P010 C3 is incomplete; 4/5 and previous P009 failures remain unchanged.

## Minimum next diagnostic

Parent plan should reuse the user's confirmed input and, once under the common key,
obtain only the visible state of the existing fixture plan terminal: whether the
submitted continue instruction appears as a conversation turn, remains in the input
box, or a concrete prompt/error is displayed. A short description of the last visible
response/prompt suffices; no raw session ID, full transcript, new terminal or repeated
trust/adoption/continue request is needed. This evidence is needed to select a safe
next action; no corrective command is justified yet. Do not restart before P901.

This was observation-only after exact review adoption. No source or active fixture
runtime changes, no full regression rerun, no changes to existing stops, P009, main,
release tags or personal installation. Prior evidence directories remain intact.
