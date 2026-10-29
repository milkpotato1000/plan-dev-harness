# plan-dev-harness distribution development

This is the reusable distribution, not a target product installation. Edit the
installer under scripts/ and generated project machinery under assets/. Keep private
project requirements, data, paths and credentials out of this repository. Preserve
existing install targets and require preview before mutation. No destructive upgrade.
Use Python standard library only unless a concrete requirement justifies a dependency.
Run `python3 -m unittest discover -s tests -v` after relevant code changes. Keep
README, VERSION and compatibility claims consistent with actual verification.
Publishing a new release needs the user's authorization; do not push unrelated repos.
