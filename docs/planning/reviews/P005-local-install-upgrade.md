# P005 local managed installation review

2026-11-04: approved under the user's existing-project 0.2.1 upgrade request.
The loaded 0.2.1 package installer was previewed with the original two protect
paths and agent=none. All 15 managed payload files were KEEP; only manifest
version changed from0.2.0 to0.2.1. P004 had already delivered the same runtime
and fresh-session child instructions. Apply reproduced this preview.

The outer AGENTS entrypoint now carries the same role/document-delivery rules.
Its complete non-Git container content is tracked for reconstruction at
`docs/process/workspace-AGENTS.md`; copy it to the container AGENTS.md when
restoring this workspace. Outer CLAUDE remains @AGENTS.md. Child AGENTS and the
shared workflow already contain the P004 rules. No runtime algorithm changed.

Preserve worktree-specific hook configuration. Do not run the shared-hook installer.
Main stays at the released baseline. P002 exported PAUSED/OPEN evidence and2/5
remain untouched. No checkpoint, product queue, release or personal skill mutation.
Dev must integrate/adopt the exact plan maintenance commit and verify manifest
hashes, guards and queue before marking this target complete.
