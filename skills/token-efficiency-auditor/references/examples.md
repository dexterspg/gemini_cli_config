# Audit Examples

Concrete Input → Output examples for common audit patterns.

---

## Example 1 — System Prompt with Token Waste

User pastes a system prompt:

```
You are an AI assistant. Certainly, I would be happy to help you with this task.
Please provide me with the information you need, and I will do my best to assist.

[tools and instructions follow...]

Feel free to ask if you need anything else.
```

**Output:**

```
SKILL/AGENT AUDIT REPORT
=========================
Input type: System prompt
Estimated tokens: ~90 (all STATIC)
Static blocks: 90 tokens — cache eligible
Dynamic blocks: 0 tokens

TOKEN EFFICIENCY SCORE: 62/100 — Fair
VALIDATION SCORE: N/A — fragment scope (audit applies to SKILL.md / agent definitions only)

CRITICAL ISSUES (FAIL)
----------------------
Throat-clearing opener ("Certainly, I would be happy...") — 12 tokens of noise
  → DELETE: Remove politeness padding entirely
Trailing sign-off ("Feel free to ask if you need anything else") — 15 tokens
  → DELETE: Move to docs, not system prompt
Dynamic phrasing: "[tools and instructions follow...]" is a placeholder
  → REFACTOR: Move all dynamic content to user turn

WARNINGS (WARN)
---------------
Politeness padding ("Please provide me with...") — contributes 8 extra tokens
  → Rewrite: "Provide [what you need]" (imperative)

ALL REWRITES (ranked by token impact)
-------------------------------------
Before:
You are an AI assistant. Certainly, I would be happy to help you with this task.
Please provide me with the information you need, and I will do my best to assist.

[tools and instructions follow...]

Feel free to ask if you need anything else.

After:
You are an AI assistant.

[tools and instructions — STATIC content only]

Token delta: -35 tokens (-22%)

CACHING RECOMMENDATION
----------------------
After removing dynamic placeholders and politeness, the static prefix is ~800 tokens.
Below current minimum threshold — verify against Google/Gemini documentation. Add more stable content OR move to a 5-minute cache refresh cycle.

STRUCTURAL GAPS
---------------
None — input is a complete system prompt.

OVERALL RECOMMENDATION
----------------------
Remove throat-clearing and trailing sign-offs immediately (35-token savings). These are the highest-impact cuts for cache efficiency. Separate static from dynamic content to restore cache breakpoints.
```

**Key lesson:** Delete throat-clearing and sign-offs first — zero value, real cost at scale.

---

## Example 2 — SKILL.md with Undertriggering

User pastes skill frontmatter and trigger section:

```
---
name: code-review-helper
description: Helps review code for quality and correctness.
---

## Do NOT trigger for
- General feedback → use agent-concept-tutor
- Performance optimization → use agent-system-architect
```

**Output:**

```
SKILL/AGENT AUDIT REPORT
=========================
Input type: SKILL.md (frontmatter + trigger section fragment)
Estimated tokens: ~120 (all STATIC)
Static blocks: 120 tokens — cache eligible
Dynamic blocks: 0 tokens

TOKEN EFFICIENCY SCORE: N/A — fragment scope (tool complexity unclear without full body)
VALIDATION SCORE: 52/100 — Fair

CRITICAL ISSUES (FAIL)
----------------------
Description missing trigger phrases (frontmatter line 3)
  → Add explicit examples: "review this code", "code review", "is this good?", "check for bugs"
Trigger phrases not literal/casual (implied in "Helps review code")
  → Expand: not just "code review" but also "audit this", "feedback on", "look over"

WARNINGS (WARN)
---------------
Do NOT trigger for section exists but lacks routing to alternatives
  → Add: "- General feedback → use agent-concept-tutor (when user asks 'explain this code')"

ALL REWRITES (ranked by token impact)
-------------------------------------
Before:
---
name: code-review-helper
description: Helps review code for quality and correctness.
---

After:
---
name: code-review-helper
description: Helps review code for quality and correctness. Triggers on: "review this code", "code review", "audit this", "check for bugs", "feedback on [file]", "is this good?". For general code explanation, use agent-concept-tutor.
---

Token delta: +120 characters (~30 tokens)

STRUCTURAL GAPS
---------------
None — minimal SKILL.md fragment.

OVERALL RECOMMENDATION
----------------------
Add all missing implicit trigger phrases and expand routing alternatives. Undertriggering is silent — the skill looks fine but never fires in practice.
```

**Key lesson:** Expand trigger phrases for all natural variants — undertriggering is silent but fatal.

---

## Example 3 — GEMINI.md Routing Table Audit

User pastes routing row:

```
| Tool operations | Read the tool skill first, main session handles MCP |
```

**Output:**

```
SKILL/AGENT AUDIT REPORT
=========================
Input type: GEMINI.md routing table (single row fragment)
Estimated tokens: ~20 (all STATIC)
Static blocks: 20 tokens — cache eligible
Dynamic blocks: 0 tokens

TOKEN EFFICIENCY SCORE: N/A — fragment scope (routing table structure, not code quality)
VALIDATION SCORE: 35/100 — Poor

CRITICAL ISSUES (FAIL)
----------------------
Trigger is a category label, not literal strings (line 1)
  → Replace with: "create [entity]", "check [entity] status", "run [action]"

Load instruction is advisory, not mandatory (line 1)
  → Replace with: MANDATORY: Load ~/.gemini/skills/[tool-name]/SKILL.md first

No conditional branch for variants (line 1)
  → Add: If [variant]-specific: also load ~/.gemini/skills/[tool-name]/workflows/[VARIANT.md]

ALL REWRITES (ranked by token impact)
-------------------------------------
Before:
| Tool operations | Read the tool skill first, main session handles MCP |

After:
| Any of: "create [entity]", "check [entity] status", "run [action]" | MANDATORY: Load ~/.gemini/skills/[tool-name]/SKILL.md first. If [variant]-specific: also load ~/.gemini/skills/[tool-name]/workflows/[VARIANT.md] |
```

**Key lesson:** Use literal strings + MANDATORY phrasing + conditional variants for reliable routing.

---

## Example 4 — Agent Capabilities Block with Ownership Gaps

User pastes an agent definition:

```
You are a debugging specialist.

Never:
- Modify source code — use the implementation-engineer
- Write tests — use the QA engineer
- Save investigation findings directly
```

**Output:**

```
VALIDATION SCORE: 68/100 — Fair

WARNINGS (WARN)
---------------
Capabilities section missing (identity defined, but capabilities not enumerated)
  → Add: Capabilities: [7–10 bullet list of what this agent does]

Never: items lack agent/skill ownership attribution (lines 3–5)
  → Rewrite each to name the responsible agent:
    - "Never modify source code — agent-implementation-engineer owns this"
    - "Never write tests — agent-qa-engineer owns this"
    - "Never save findings directly — agent-note-taker owns this"

REWRITE
-------
Before:
You are a debugging specialist.

Never:
- Modify source code — use the implementation-engineer
- Write tests — use the QA engineer
- Save investigation findings directly

After:
You are a debugging specialist.

Capabilities:
- Trace code paths from user action to failure
- Perform root cause analysis on bugs and errors
- Create minimal reproduction steps
- Compare file/config versions to identify changes
- Identify and rule out unrelated theories
- Provide structured investigation reports
- Generate documentation signal patterns

Never:
- Modify source code — agent-implementation-engineer owns this
- Write tests — agent-qa-engineer owns this
- Save investigation findings directly — agent-note-taker owns this
```

**Key lesson:** Separate Capabilities from Never constraints and always name the responsible agent.
