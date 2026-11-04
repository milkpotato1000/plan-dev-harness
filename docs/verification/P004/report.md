# P004 — fresh-session routing and document delivery

Implementation: 0.2.1 on dev; exact adopted plan
46e22e4de27db7074a62d8ccaeb721febdf1fb93, review body
b6f3d3d976cbce26320fd3ca5aa27c1ba48c4fe1. Adoption merge 8f5e756.
Requested delivery target: existing origin/dev and the currently loaded Codex
skill path. No main/tag/release publication or other project upgrade.

## Findings and change

Before evidence: adopted docs/planning/reviews/P004-reproduction.json. The actual
CLI probe accepts plan code/README writes without a card and leaves dev unchanged.
This identifies a guard limit; it does not reproduce an actual fresh model session
or establish the sole cause of the user's unspecified earlier incidents. The
loaded personal skill was an older, versionless copy, another plausible contributor.

New/resumed sessions reconstruct roles, adoption, queue and scoped controls from
files. Explicit plan remains plan; unassigned material requests use a suitable
P-card preparation -> exact adoption -> dev execution. Documentation routes by
purpose. Product README/user guides go to dev; plan contracts needed there are
integrated/adopted. Planning-only drafts and read-only questions retain narrower
scope. Requested target ref/content must be verified; plan push alone is not
completed delivery and does not authorize main promotion. Rules reach SKILL,
references, installed workflow/queue and actual generated outer/child entrypoints.

## Evidence map

- C1: original reproduction plus active-skill-audit.json; before/after CLI limitations separated from model behavior.
- C2: policy-review.md, actual generated/ artifacts from both packages; N1–N10 bounded review PASS.
- C3: installation-commands.json, package-hashes.json, delivery-commands.json and focused-tests.log. Actual standalone copies/bootstrap, manifest validation, 0.2.0 upgrade, unrelated user file preservation and customized AGENTS conflict refusal PASS. Local bare remote shows plan-only push, exact local adoption, dev push and unchanged main separately.
- C4: active-skill-review.md and active-skill-transition.json; 0.2.1 selected at original loaded path, original fully backed up, four extra files/UI metadata preserved. Host context reload remains unverified.
- C5: final full regression/guard/queue and preservation results appended after completion.

## Failures and limits retained

The first verification helper found the historical P002 temporary paths no longer
formed a Git worktree. It was corrected to record unavailable Git state and compare
remaining files without rebuilding or touching the fixture. installation-attempt-1.json
preserves that failed read. The second helper assumed a docs/progress directory
already existed in a new upgrade probe; it did not. That fixture-setup assumption
was corrected, the failure retained in installation-attempt-2.json, and the complete
probe rerun successfully. No product runtime fix was needed for either helper.

First full regression: 68 tests, one stale expected-version assertion (0.2.0 vs
actual 0.2.1). regression-attempt-1.log preserves failure. The upgrade test now
compares to distribution VERSION while retaining hook/record preservation checks.
System and bundled Python lacked PyYAML required by skill-creator's validator;
a dedicated temporary validation environment with PyYAML 6.0.3 passed quick_validate.
No project or global Python dependencies changed.

The post-change negative CLI probes still accept arbitrary plan implementation:
no new write allowlist or schema was added. Policy review is not a live-agent
PASS. Existing projects/outer files require separately scoped upgrades; publishing
the skill does not update them. P002 remains stopped with its last committed
PAUSED/OPEN evidence intact; no fixture control was changed or recreated.
