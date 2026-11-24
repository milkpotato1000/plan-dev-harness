# Independent Claude plan/dev workers

Use the [installed adapter procedure](../assets/docs/process/worker-adapters.md)
for current requirements, identity, transport, authority and diagnostic semantics.
This file is included with the skill; project installs copy the complete procedure
to docs/process/worker-adapters.md and copy scripts/worker_doctor.py.

## Start or reuse two sessions

First inspect existing sessions; do not create a duplicate writer. For a newly
approved workspace, substitute actual paths and use one terminal per role:

```sh
cd "/absolute/workspace/project_plan"
claude --name project-plan
```

```sh
cd "/absolute/workspace/project_dev"
claude --name project-dev
```

In each session use the corresponding assets/workspace/plan-chat.md.template or
dev-chat.md.template, substituting the actual container/child paths and branches.
Explicitly assign plan or dev; a folder/name alone does not assign it. Those initial
prompts are read-only bootstrap. An existing session at the container can retain its
cwd while using explicit role child paths, after a real role assignment. Record both
session cwd and worktree binding; do not resume an already-running session as a copy.

For authorized work, plan records the real human approval/delegation, reviews READY
scope and commits the exact SHA. It uses native tools to send that packet to the
verified independent dev. Dev applies it internally and executes; the human does
not need another adoption prompt. Plan ends its turn after actual send bookkeeping.
When no worker/tool exists, leave pending with the missing condition. Do not ask
plan to implement on dev. Explicit sequential mode must be separately chosen.

## Verify actual overlap

Use an authorized, isolated fixture, not an active product repo. Fixture plan alone
writes/reviews P901 and P902. Fixture dev alone implements harmless text outputs.
Record actual role/session aliases, tool results, Git commits and timestamps:
P901 send/application/start, plan turn return and subsequent P902 planning while
P901 is active, P902 delivery while busy, then P901 completion/checkpoint and exact
P902 application/execution. Preserve source logs privately and publish sanitized
bounded evidence. A background shell, simulated inventory or one model doing both
roles cannot pass this live check. If inbox approval/login/UI input is required,
prepare a precise packet for the existing plan review channel and leave live
criteria incomplete. Never accept that permission on the user's behalf.

No global skills/settings updates follow from a local test. Install with preview
and an explicit project --skills-dir; existing differing skills are preserved and
refused. Do not invent --upgrade for install_skill.py. Read the installed VERSION
and doctor procedure, not only this source tree. Package installation and actual
session discovery/transport are separate checks.
