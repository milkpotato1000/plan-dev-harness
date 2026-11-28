# P011 synthetic content diagnostic

On Claude Code 2.1.332 with Python Agent SDK 0.2.189, both streamed tool inputs contained exactly the three requested strings, including the complete message. The assembled SDK ToolUseBlock and the PreToolUse hook agreed with each other. Both preserved the three strings and added type, recipient, recipient_kind and content. In both samples, content held a prefix followed by an ellipsis.

| Sample | Full message length | Prefix before ellipsis | Cost (USD) |
| --- | ---: | ---: | ---: |
| ASCII | 74 | 49 | 0.0334208 |
| Korean | 54 | 28 | 0.0151277 |

Lengths count Unicode code points. Each run used a fresh neutral working directory, one fictional recipient, only SendMessage, strict MCP, safe mode, a 60-second deadline and a USD 0.50 cap. The verified PreToolUse callback always returned deny with block-on-failure. Each run yielded one denied tool result. ListAgents was unavailable. The two raw synthetic comparisons, including complete messages and generated prefixes, are in probes.json.

In these runs the extra fields appeared between the streamed model arguments and the assembled SDK representation. The captures do not localize the transformation to a particular internal function or establish the actual values in the previous live failure. The prior fixed 30-character rule rejects both observed inputs. The synthetic evidence does not establish a stable width algorithm or which representation native delivery ultimately consumes.

## Contract and proposed change for review

The official tool reference describes summary as an optional preview. It does not specify the native meaning of the extra content field in these observations. The installed SDK exposes general tool input dictionaries, with no dedicated Python SendMessage input type found. The CLI help's json-schema flag describes model output. Neither provides a normative mapping from the hook aliases to the delivered bytes. [Anthropic tools reference](https://code.claude.com/docs/en/tools-reference)

The official PreToolUse contract supports replacing the complete input via updatedInput without granting permission. Permission evaluation uses the replacement. The installed SDK's PreToolUseHookSpecificOutput includes this field. The diagnostic exercised denial only. [Anthropic hook reference](https://code.claude.com/docs/en/hooks#pretooluse-decision-control)

Proposed design for separate review: bind the one streamed tool call to the matching hook by tool-use ID. Reject missing or ambiguous correlation, invalid JSON, duplicate keys, extra streamed fields and non-string values. Compare the pinned recipient, exact summary and UTF-8 body digest with the reserved handoff. Require the assembled original fields to match, reject unknown fields or conflicting recipient aliases, and treat unexpected content as unsafe for dispatch. Evaluate a clean replacement object constructed solely from the reserved to, summary and full message in an isolated controlled receiver test. Return updatedInput without an allow decision. Acceptance requires independent proof of the actual received bytes and ordinary policy denial behavior, including malicious aliases, multibyte text and truncated-body negatives. Until this can be demonstrated, keep the existing production guard and both reservations. No third model call was needed.

The diagnostic changes evidence only. Runtime source remains de40ec9255b67959e871247a676d8cb920214031, previously verified by its final 110-test suite. No additional live attempt or product-code change occurred.
