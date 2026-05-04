# Rewrite Rules Reference

Anti-pattern → Fix mappings for token efficiency and validation corrections.

---

## Cacheable Prefix Order (Most → Least Stable)

1. Identity / Role
2. Tool definitions
3. Static instructions / skills
4. Few-shot examples
---
5. User turn / dynamic data ← cache breaks here

---

## Routing & Validation Anti-Patterns

| Anti-Pattern | Rewrite |
|---|---|
| Advisory load instruction ("read skill first") | "MANDATORY: Load [exact path] when [condition]" |
| Category label as trigger ("Tool operations") | Literal strings: "create [entity]", "check [entity] status" |
| Capability mixed with constraint | Split into Capabilities: and Never: blocks |
| Never: without ownership | "Never [X] — [agent-name] owns this" |
| Implicit trigger phrases only ("--flag" style) | Add casual variants: "how does X work", "I don't understand X" |
| Variant handled in separate routing row | Handle inline: "If [variant]: also load ~/.gemini/skills/[skill]/workflows/[VARIANT.md]" |

## Token Efficiency Anti-Patterns

| Anti-Pattern | Rewrite | Savings |
|---|---|---|
| Politeness padding ("please", "kindly", "if you would") | Remove entirely or use imperative voice | 5–15 tokens per instance |
| Throat-clearing openers ("As an AI...", "Certainly...") | DELETE — start with role or constraint | 10–20 tokens |
| Transition filler ("In order to", "Due to the fact that", "Make sure to") | Use direct construction: "To X, do Y" | 3–8 tokens per instance |
| Restatement of question before answering | DELETE — answer directly, no setup | 10–30 tokens |
| Trailing sign-offs ("Feel free to ask", "Let me know if...") | DELETE — move to docs, not system prompt | 15–25 tokens |
| Dynamic content in static blocks (timestamps, UUIDs, session IDs) | Move to user turn or parameterize | Restores cache hits entirely |
| Prose-paragraph instructions | Convert to label-colon bullet structure | 20–40% reduction per section |
| Instruction restatement across sections (internal redundancy) | Keep single authoritative version, cross-reference | 20–100 tokens |
| Parameter descriptions: "a type that represents X" | Use "X (type)" format | 3–5 tokens per param |
| Ambiguous format instruction ("clean", "readable") | Replace with explicit rules: "JSON, no whitespace" or "markdown with headers" | 5–15 tokens |
| Unused optional parameters in tool definitions | Remove completely | 2–8 tokens per param |
| Redundant `required: true` on default-required fields | DELETE — let framework defaults apply | 2–3 tokens per field |

