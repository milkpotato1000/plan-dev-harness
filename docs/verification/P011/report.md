# P011 official Claude relay verification

Source commit `1c3dd70c54f5e27a536ab820e0c36bc4126ab2de` packages the optional relay in 0.2.6. The reviewed plan is `4487217ecee60dc1a2d6eae0fd453d1c072e7022`. Common review key `P011-official-claude-relay`.

Claude Code 2.1.332 exposed ListAgents and SendMessage in the restricted CLI probe. SDK 0.2.189 supplies the pre-execution argument check. A neutral temporary directory, safe mode, strict MCP configuration, explicit tools, a 60-second timeout and a USD 0.50 invocation budget bound the runner. Managed policy continues to apply. Isolated denial probes returned tool errors even when the enclosing model invocation exited successfully.

The real P010 plan handoff stopped at argument validation. The native call had additional normalized fields. Isolated tests established the native name address, duplicate recipient and content fields, and summary field. The revised attempt compared all fields and recorded a mismatch. The trace available at that point contains the field names and overall comparison only. It cannot identify which value differed. Neither target transcript contains the delivery key. P901 creation, receipt, execution and the second handoff remain unverified. The per-project ledger reserves the revised attempt. A subsequent synthetic send, blocked before execution, reproduced a 30-character preview plus an ellipsis in the content field while the full message matched exactly. Source commit 1c3dd70 recognizes this format and rejects any change to the full message. The actual failed request cannot retrospectively be attributed to this difference. The original delivery key remains consumed.

The local SDK dependency is optional. The released main remains v0.2.3. The isolated 0.2.5 upgrade, preview, apply, KEEP, customized hook conflict, and standalone skill checks cover the development package. The receiver integration still needs a successful trace before it can be recommended for unattended use.

[Anthropic programmatic CLI](https://code.claude.com/docs/en/headless) · [Cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging)
