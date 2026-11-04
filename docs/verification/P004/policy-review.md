# P004 N1–N10 bounded policy review — PASS

Method: session-dev read actual generated outer/child instructions for both
independent Codex/Claude packages in generated/, followed CLAUDE @AGENTS imports
and child workflow links, and compared each scenario against the adopted P004
contract. This is document/policy review, NOT a fresh model session experiment.
The package/bootstrap tests separately check actual files, imports, manifest
hashes and standalone execution. They do not prove that a model obeys prose.

| Scenario | Expected decision confirmed in generated artifacts |
| --- | --- |
| N1 unassigned feature/fix | outer AGENTS startup reconstructs files/branch/adoption/cards; reuse or prepare P, exact dev adoption then execution; both roles only with authority and no competing writer |
| N2 explicit plan + implement request | outer and child AGENTS retain assigned role; plan prepares/reviews/hands off, does not implement product files |
| N3 README/GitHub Markdown | outer and child route by purpose; README/user guides/release notes go to dev; workflow records file/repository/target ref and delivery proof |
| N4 plan-owned contract needed by dev | plan authoring followed by integration/exact adoption, not plan push alone |
| N5 planning-only draft or explanation | draft may finish on plan; read-only question creates no P card; startup alone waits |
| N6 stale dev adoption | existing child workflow and queue rules inspect latest available prepared plan when adopted queue empty; preserve work and adopt exact review before execution |
| N7 pause/OPEN/other writer | outer + workflow preserve scoped controls and exclusive writers; unrelated fixture pause is not resumed or expanded to another authorized task |
| N8 no messaging grant/tool | pending file handoff; no automatic chats, assumed send or receipt; existing direct-handoff limits retained |
| N9 plan push only | explicit distinction between plan push, dev adoption, dev push and target-ref visibility; no false delivery completion |
| N10 default branch requested without main grant | prepare authorized work, report actual ref, retain explicit main/release authority requirement |

Artifacts reviewed: generated/{codex,claude}/outer-AGENTS.md,
child/AGENTS.md, child/docs/process/agent-workflow.md and work-queue.md; outer and
child CLAUDE.md point to their actual AGENTS.md. Source role prompt templates and
references point to the same workflow. The literal installed P004 workflow section
is carried unchanged into the asset, preserving the separately existing P003
handoff section. No guard/schema algorithm was changed. Both post-change negative
CLI probes still accept a cardless plan implementation commit: this is the
explicit mechanical limitation, not a policy PASS or claimed behavioral fix.
