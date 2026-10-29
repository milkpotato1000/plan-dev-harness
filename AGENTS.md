# plan-dev-harness distribution development

This is the reusable distribution, not a target product installation. Edit the
installer under scripts/ and generated project machinery under assets/. Keep private
project requirements, data, paths and credentials out of this repository. Preserve
existing install targets and require preview before mutation. No destructive upgrade.
Use Python standard library only unless a concrete requirement justifies a dependency.
Run `python3 -m unittest discover -s tests -v` after relevant code changes. Keep
README, VERSION and compatibility claims consistent with actual verification.
Publishing a new release needs the user's authorization; do not push unrelated repos.

## Distribution development workspace

Open the parent `plan-dev-harness/` container as one project. Its three children
are `plan-dev-harness_plan/` (plan), `plan-dev-harness_dev/` (dev), and
`plan-dev-harness_main/` (main). Run commands inside the appropriate child.
See `docs/workspace.md` for reconstruction and branch responsibilities.

Plan owns requirements and readiness under docs/planning. Dev integrates the
exact reviewed plan commit before implementing and preserves its execution logs.
Read dev completion evidence with `git show dev:<path>`; do not merge dev into
plan just to synchronize completion. Main promotion still requires an explicit
user request. A workspace setup does not authorize new feature work.

This distribution has not installed its generated target harness into itself.
The queue/guard sources under assets/ are deliverables, not active repository
hooks. Planning and adoption are currently recorded through reviewed plan commits
and their integration into dev; do not run nonexistent root queue/guard scripts.
