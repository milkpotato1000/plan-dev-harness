# Compatibility and verification boundary

The core uses Git and Python standard-library scripts. It does not import Codex or
Claude APIs and does not select models, change permissions, or require chat messaging.
Both agents read the same installed project rules; role is plan/dev, not tool name.

| Surface | Delivered integration | Verified scope |
| --- | --- | --- |
| Codex | AGENTS.md; self-contained skill in .agents/skills | CLI installer output, skill structure, runnable copied scripts |
| Claude Code | CLAUDE.md importing @AGENTS.md; skill in .claude/skills | Same files/commands and conflict/standalone tests |
| Common | Git hooks, exact adoption, P cards, queues, immutable intake, workflow controls | Real temporary Git repositories/worktrees |

No autonomous model session was launched to certify end-to-end compliance. CLI/skill
support does not guarantee all models follow instructions or bypass host sandbox rules.
Git hook execution needs `python3` and POSIX sh on PATH. On macOS the system Python3.9
is supported, including ISO timestamps ending in Z. Python>=3.9 and Git>=2.31 are the
supported targets. macOS is locally verified; Linux/WSL/native Windows are not tested
in this release. Git identity is needed only for bootstrap commits. Remote publication
needs separate authentication/authorization and is never part of the installer.

Official integration references checked 2026-10-29:
- [Codex skills and project instructions](https://learn.chatgpt.com/docs/customization/overview#skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code imports and shared instructions](https://code.claude.com/docs/en/memory)

The Claude bridge explicitly imports shared AGENTS.md, so the distribution does not
rely on a specific release's implicit AGENTS.md discovery. Native app marketplace
plugin packaging and automatic cross-host session orchestration are not included.

Version 0.2 adds read-only control fields to queue JSON without removing old keys.
Legacy Markdown decisions/checkpoints are read conservatively. v0.1 manifests can
upgrade with the same install options. A customized or manifest-less project needs
reviewed manual integration; no deployment/board/agent-specific rules are imported.
