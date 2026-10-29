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

This distribution also uses a repository-local harness under scripts/ and
.harness/. Keep that installed runtime separate from distributable sources under
assets/: changing the package does not automatically upgrade the active harness.
Use the process and setup review below for queue, adoption and hook activation.

## Repository-local plan/dev harness

Open the non-Git parent `../` as one project. Sibling worktrees are
`../plan-dev-harness_plan/` (plan), `../plan-dev-harness_dev/` (dev), and
`../plan-dev-harness_main/` (main). Read the selected child's instructions and run
Git/scripts there explicitly. A user-assigned chat role persists across turns;
a generic next-work request follows that role. Both-role requests proceed plan
then dev with reviewed integration and exact adoption. Bootstrap chats only read
status/rules/queues and wait; they do not start implementation or message peers.

Read `docs/process/agent-workflow.md`, `docs/process/work-queue.md`,
`docs/process/plan-intake.md`, `docs/process/workflow-controls.md`, and
`.harness/policy.json`. Plan owns scope/contracts/readiness and registers prepared
work within the authorized objective without repeated handoff approval. Dev
implements the exact adopted plan, changes only P-card execution fields and
append-only logs, and preserves failures with committed verification evidence.
New scope raised in dev uses the immutable intake then plan review/adoption.
User stops persist until explicit human resumption. Never merge arbitrary dev
implementation into plan merely to transfer completion marks.

The pre-harness P001 remains at `docs/planning/P001-v0.2.0-workflow-controls.md`;
read its dev version and existing verification as historical evidence. It is not
an executable parsed card and must not be silently rerun or renumbered. New work
starts with the next unused number, P002, in `docs/planning/plans/`. An empty
parsed queue does not mean no historical work. This setup creates no product task.

Local hook activation is worktree-scoped for plan and dev because main retains
the released v0.1.0 tree without installed runtime scripts. Preserve this topology;
do not run the shared-hook installer until every participating worktree contains
the runtime. A future main promotion must explicitly review release hook setup.
Neither this setup nor a workflow handoff authorizes main promotion, a new
release/tag, a force push, or sending messages to other chats. Honor standing
non-force plan/dev push authorization to the existing configured remote.

Setup/review reference: `docs/planning/reviews/local-harness-setup.md`.
