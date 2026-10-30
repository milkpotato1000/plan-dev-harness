# v0.2.0 implementation verification — 2026-10-29

Status: implemented and locally verified on dev; main promotion/release pending.
Environment: macOS, Git 2.50.1 (Apple Git-155).

| Run | Result | Evidence |
| --- | --- | --- |
| Python 3.9.6 full suite | 66 PASS, 105.376s | [Log](verification/v0.2.0/python39.log) |
| Python 3.13.15 full suite | 66 PASS, 116.688s | [Log](verification/v0.2.0/python313.log) |
| New workflow/upgrade coverage | 15 tests, included in both full runs | [Tests](../tests/test_workflow_controls.py) |
| Skill compatibility | Both copied skill layouts run workflow_control.py --help | Distribution tests in full suite |
| Metadata | SKILL frontmatter unchanged from validated v0.1.0 | Checked against v0.1.0 Git object |

Full command: `python3 -m unittest discover -s tests -v`. Each runtime also supplied
`python3` on PATH for hooks/child commands. Tests operate on disposable Git repositories,
including configurable design/develop/release branches. Product repositories and
personal skill installations were not modified or used as test targets.

The new tests cover conservative legacy stops, plan-owned scoped classification,
adoption before scope changes/resolution, dependent tasks, independent work, short-SHA
refusal, user pause visibility across worktrees, role-only vs all-role pause, explicit
resume, another role's pause and unresolved decisions, index/HEAD checks, plan pre-push
checks, stop/history deletion, handoff event deduplication and ordered receipt states,
generic intake coexistence, and the corrected default queue owner.

Upgrade testing exports the actual v0.1.0 tag, installs it, previews and applies the
new same-option manifest upgrade, preserves custom post hooks and live records,
and rejects modified user instructions. No installer silently repairs old malformed
records; those need a reviewed correction with real evidence.

Known boundaries:
- No live Codex/Claude model session, message transport, Asana, service deployment,
  Linux/WSL/native Windows validation was performed.
- Queue controls do not terminate processes or confer authorization. Missing remote
  fetches and the counterpart's uncommitted state are outside visibility.
- User request/delivery evidence references are recorded and structurally checked;
  their real-world truth is still the human/agent's responsibility.
- Hooks are local and bypassable. They do not prove all implementation stays in scope.
- Optional adapter documentation defines boundaries; it is not an adapter loader/API.

One environment-only compile attempt could not create macOS's external bytecode cache.
AST parsing and both actual interpreter test suites passed without changing permissions.

Plan and acceptance mapping: [P001](planning/P001-v0.2.0-workflow-controls.md).
