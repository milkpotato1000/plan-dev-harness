# Loaded Codex skill transition — PASS (files), host reload unverified

Read actual catalog path <loaded-codex-skill>. It had no VERSION, a longer older
entrypoint and 22 non-cache files. Audit hashes are in active-skill-audit.json.
Several files do not match known distribution commits, so they were not assumed
to be disposable. Reviewed old installer, references, entrypoint and exported
function inventory: existing setup/discovery, nested-worktree, remote authorization,
role-chat, P-card, exact adoption and hook limitations remain covered by the new
source and usage references. No extra old Python function/class disappeared.
UI metadata is byte-identical. Four old test files outside the new shipped payload
are carried at the same paths in the active copy; no other extra files or symlinks
were found. The full original directory is preserved unchanged outside discovery.

A fresh Codex package was first previewed/applied and actually bootstrapped; its
payload and generated manifests passed. A same-filesystem staging copy added the
four extra files, passed skill-creator quick_validate, then the original directory
was renamed to a unique inactive backup and the staged directory selected at the
same loaded path, with rollback on failure. No installer refusal was overridden.
Before-mutation hashes were rechecked; backup matches the complete original
non-cache manifest and also retains cache files via directory rename. Active hashes
match the new package plus preserved extras. Installer --help and a direct reread
of active SKILL.md/VERSION confirm 0.2.1 on disk. Private locations are retained in
/private/tmp/p004-transition-private.json; public hashes use aliases.

No global Claude copy or other project was updated. File replacement at the known
catalog path does not prove this already-open chat refreshed its loaded instructions.
Open a new session and verify the selected path/VERSION. No duplicate same-name
copy was left in an active discovery root. Preserved legacy test files are not
claimed as the 68-test source regression suite.
