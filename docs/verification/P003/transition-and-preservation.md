# P003 layer transitions and legacy feature preservation

Source baseline: 77b757cce25dd2f5ee5b3751dbfb26fb70d88d08, version 0.2.0.
Initial adopted plan: 80dbb3b4e53ffd8f7427e48cb7c827a22f6aa5f4.
Follow-up adopted plan: 283ddd331eb5196bc6b2f36b0ced15ad3ce2ba74, integrated at
84ea10a with previous implementation/logs preserved.
Actual file fingerprints and temporary project manifests: layers-and-upgrade.json.
Private installation locations are represented by aliases below.

| Layer | Actual result | Activation boundary |
| --- | --- | --- |
| distribution source | Added direct-handoff reference and SKILL/role/usage/README entrypoints; preserved existing v0.2 implementation | Changed files in dev; not a release or tag |
| distribution assets | Copied three approved control/adapter/template process texts; extended approved common instructions, generic project/workspace AGENTS and both bootstrap prompts | Runtime Python, CLI flags/schema, VERSION and project installer unchanged |
| this repository installed contract | Exact plan adoption; managed manifest hashes all match; four protected documents equal adopted snapshot | No dev rewrite of protected contract, hook installer or Git config |
| temporary project from actual prior v0.2 commit | Real preview/apply from archived source, then same-option v0.2 upgrade; new process texts/hash verified | No other project or remote touched |
| temporary Codex and Claude skill parents | Independent package source, relative links, project installation from copied script, all manifest hashes, CLI --help verified by regression | These disposable payloads are not active personal skills |
| legacy personal skill alias | Read-only inspection: long end-to-end SKILL; no VERSION/control payload; same name differs from package | Not changed, backed up, switched or claimed active |

## Legacy capability mapping

The inspected legacy SKILL's sections 1–6 and reuse guidance were compared to the
current source; no old personal files were copied to this repository.

| Existing capability | Current location / preservation or change |
| --- | --- |
| Destination/name/repo discovery, infer existing state and ask only missing details | SKILL steps 1–3; references/usage.md Legacy setup capabilities |
| Hosted identity/owner/name/visibility, explicit repo creation and remote permissions | references/usage.md Legacy setup capabilities; still separate host/CLI actions, not installer features |
| Container plus linked plan/dev/main, explicit child routing, existing checkout reuse | SKILL steps 1–4; references/project-instructions.md; scripts/bootstrap_workspace.py |
| Safe legacy sibling relocation, dirty/ignored files, no reset/force/join | references/workspace-layout.md; references/usage.md; migration helper unchanged |
| Separate role chats, persistent role, bootstrap read-only | references/role-chats.md; both assets/workspace prompts unchanged in bootstrap scope |
| Preview/apply, configurable branches/protection, existing instructions/hooks | SKILL step 3; references/usage.md; install_harness.py unchanged |
| Exact adoption, install only when participating trees have runtime, worktree/index/HEAD guards | SKILL steps 4/7; references/usage.md; existing runtime regressions |
| Prepared P-number card, dependencies, execution-only dev fields, latest PASS and failed-history preservation | SKILL steps 5–7; installed process and queue; no P002 criteria change |
| New scope intake and plan-owned decisions, feedback | SKILL step 6; usage and installed plan-intake; runtime unchanged |
| Report local-only/pushed state, release/main permission, cross-computer reuse | usage Legacy setup capabilities and transitions; no global skill update inferred from project push |
| Existing project-specific rules and adapters | usage Existing project-specific rules; optional-adapters; --agent none boundary retained |
| Explicit human-authorized direct delivery, receipt observation and fallback | New references/direct-handoff.md and complete installed workflow-controls; documented extension rather than automatic sender |

## Safe transition instructions

Project upgrades require the original options, previous manifest hashes and a
read-only preview before authorized --apply. Review/commit on plan, integrate and
adopt the exact SHA on dev; preserve user extensions, live records and post hooks.
Unmanaged legacy files need deliberate reviewed integration, not forged hashes.

Personal skill installation has no --upgrade option. Default Codex discovery
parent ~/.agents/skills differs from the observed old ~/.codex/skills parent;
Claude defaults to ~/.claude/skills. Under separate human transition authority,
preserve/backup old files, test a fresh --skills-dir destination, select the actual
host-supported load path and avoid simultaneously active duplicate names. Refresh
or reopen discovery and reread the chosen SKILL. This work performs none of those
real personal/other-project transitions; copying a package proves no activation.

Actual preservation checks: previous v0.2 project preview changed no payload files;
same-option apply preserved custom post-commit and live record; a customized managed
control file caused refusal with the entire tree unchanged. Legacy personal-style
payload plus user extension survived preview/apply refusal; fresh alternate skill
installation left the old tree unchanged. Details: upgrade-commands.json and tests/test_distribution.py.


Follow-up installable rule: generic project and workspace AGENTS plus common
instructions explicitly describe delegated READY delivery and dev adoption/start.
Their scope remains conditional on that destination project's actual human grant;
none contains this repository's specific grant, human quotation or chat identity.
The protected repository-local process stays at the adopted plan; generic source
instructions include the follow-up explanation as permitted by the clarified scope.

Both independent package copies actually bootstrapped new temporary workspaces.
Output hashes/manifests: payload-hashes.json. Actual preview/apply/guard/queue CLI
records: payload-commands.json. Selected raw generated files are exported under
outputs/codex/ and outputs/claude/ with a .txt suffix (original payload names are
keys in payload-hashes.json). The exports are evidence text, not another installable
package; links were resolved in the actual complete independent payloads and
project directories by the integration regression.
