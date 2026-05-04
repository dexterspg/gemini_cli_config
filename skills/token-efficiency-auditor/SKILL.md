---
name: token-efficiency-auditor
description: Audit and validate Gemini CLI agent system prompts, SKILL.md files, and prompt templates for token waste, context inefficiency, and structural correctness. Use this skill whenever the user wants to check, review, score, validate, or improve a prompt, agent definition, or skill file — for token efficiency, caching potential, verbosity, or structural completeness. Triggers on: "check my prompt", "is this token efficient", "audit my skill", "validate my agent", "review my SKILL.md", "is my skill correct", "does this skill have everything it needs", "too verbose?", "optimize my system prompt", "how many tokens is this", "can I make this shorter", "is my agent well structured".
---

# Token Efficiency Auditor + Skill/Agent Validator

Two audits in one:
1. **Token Efficiency Audit** — find waste, improve structure, maximize caching
2. **Skill/Agent Validation** — confirm structural completeness and correctness

Run both by default. Run one only if the user specifies.

---

## Step 1 — Receive and Classify Input

Accepted inputs: system prompt text, SKILL.md, agent definition, prompt template.

| Signal | Classification |
|---|---|
| `---` frontmatter with `name:` and `description:` | SKILL.md |
| `Identity:` / `Role:` / `Tools:` block | Agent definition |
| `{placeholder}` or `[slot]` syntax | Prompt template |
| None of the above | System prompt |

- File path provided — read first
- Description only — ask for actual content
- < 10 tokens or unrecognizable — reject with: "Provide a system prompt, SKILL.md, agent definition, or prompt template."      

**Do NOT trigger for:**
- General code review — code-review skill
- Writing a skill/agent from scratch — skill-creator skill

---

## AUDIT 1 — Token Efficiency

### Token Classification

Estimate token count (±30% variance):
- English prose: 1 token ≈ 4 characters
- Code: 1 token ≈ 3 characters
- Label-colon blocks: ~30–50% cheaper than prose equivalent
- XML tag pairs: ~2–6 tokens each

Classify each block:
- STATIC: never changes across calls — cache candidate
- DYNAMIC: changes per call — must be in user turn
- MIXED: static framing with dynamic slots — needs refactoring

Flag DYNAMIC content inside the system prompt as highest-priority — it destroys cache hits on every call.

---

### Token Efficiency Checklist

Mark each: PASS / WARN / FAIL

#### Structure & Formatting
- [ ] Static content strictly precedes dynamic content (Cache Priority).
- [ ] Instruction boundaries are clear (Uses XML tags or clear Markdown headers).
- [ ] No "leaky" dynamic variables (e.g., {{date}} inside a static instruction block).
- [ ] Label-colon blocks used for lists to minimize prose tokens.
- [ ] Most stable content follows caching order: Role → Tools → Static Skills → Few-Shot → User Turn
- [ ] Output contract defined (format, length, tone)

#### Word Discipline
- [ ] No politeness padding (please, kindly, if you would be so kind)
- [ ] No throat-clearing openers (As an AI..., Certainly...)
- [ ] No transition filler (In order to, Due to the fact that, Make sure to)
- [ ] Instructions use imperative voice
- [ ] No restatement of the question before answering
- [ ] No trailing sign-offs (Feel free to ask, Let me know if...)

#### Sentence Order
- [ ] Constraints and format rules before context and data
- [ ] Role declaration is first line, not buried
- [ ] Scope limiters appear before the task, not after
- [ ] Data / content to act on is last

#### Caching Potential
- [ ] No timestamps, UUIDs, or session IDs in static blocks
- [ ] Tool definitions are in stable deterministic order
- [ ] Few-shot examples are frozen, not dynamically generated
- [ ] Cache breakpoint is placeable after the static prefix
- [ ] Static prefix is at least 1,024 tokens (Gemini CLI heuristic)

---

## AUDIT 2 — Skill/Agent Validation

### Skill Validation Checklist (SKILL.md only)

Mark each: PASS / WARN / FAIL

#### Frontmatter
- [ ] Has `name:` — short, lowercase, hyphenated
- [ ] Has `description:` — not empty
- [ ] Description states WHAT the skill does
- [ ] Description states WHEN to trigger (specific contexts, not just a category)
- [ ] Description includes example trigger phrases
- [ ] Description triggers on implicit user intent, not just exact keywords (e.g., "review my code" also matches "is this any good?")

#### Trigger Design
- [ ] Trigger conditions are explicit in the body
- [ ] Has a "Do NOT trigger for" section with routing alternatives
- [ ] Trigger phrases cover casual/implicit user language
- [ ] No overlap with other known skills causing ambiguous routing
- [ ] Trigger phrases are literal user-typed strings, not category labels (e.g. "jira", "LAE ticket" — not "Jira operations")
- [ ] Skills that must always load have an explicit MANDATORY load instruction, not advisory phrasing like "read skill first"

# These catch undertriggering — the highest-cost routing failure.
# A skill that never loads scores worse than a verbose one that does.

#### Structure Completeness
- [ ] Clear named purpose / overview at top
- [ ] Each major action has: Trigger / Input / Process / Output
- [ ] Input expectations defined (format, minimum content)
- [ ] Output contract defined (format, length, file path if applicable)
- [ ] File output uses template naming: `{project-root}/[prefix]-[content-name]-[YYYY-MM-DD].ext`
- [ ] Edge cases and error conditions handled

#### Content Quality
- [ ] Uses label-colon structure, not prose paragraphs for instructions
- [ ] No instructions buried mid-paragraph
- [ ] No instruction restated in different words across sections (internal redundancy)
- [ ] Examples present following Input → Output pattern
- [ ] Examples are concrete, not abstract
- [ ] Instruction-to-example ratio is proportional (examples ≤ 40% of total body)
- [ ] Notes section present for caveats and limitations

#### Size and Loadability
- [ ] Body is under 500 lines
- [ ] Large reference content (examples, lookup tables) moved to `references/` subfolder if body exceeds 300 lines
- [ ] References loaded on demand, not always in context
- [ ] Multiple domains/variants organized into subfolders with router in SKILL.md

---

### Agent Validation Checklist (Agent definitions only)

Mark each: PASS / WARN / FAIL

#### Identity
- [ ] Single-line role declaration at top
- [ ] Role is specific (not just "helpful assistant")
- [ ] Domain or stack named if relevant

#### Capabilities and Constraints
- [ ] Capabilities listed as bullet points, not prose
- [ ] Constraints listed explicitly (what it must never do)
- [ ] Constraints use "Never:" not prose equivalents
- [ ] No capability or constraint duplicated across sections

#### Tool Definitions
- [ ] Each tool has a one-sentence description max
- [ ] Tool descriptions say when to use, not just what the tool does
- [ ] Tool parameter descriptions are terse (type + purpose only)
- [ ] No parameter redundancy (e.g., redundant "required: true", verbose type descriptions)
- [ ] No unused optional parameters included
- [ ] Tool list order is stable and deterministic

#### Skills Integration
- [ ] Each sub-skill has a named trigger condition
- [ ] Routing logic uses skill trigger blocks, not prose if/else
- [ ] No skill responsibility overlaps with another
- [ ] Orchestrator prompt contains routing rules only — not sub-skill instructions

#### Output Contract
- [ ] Format rules defined (JSON / plain text / markdown / code)
- [ ] Tone defined if relevant
- [ ] Length limits defined if relevant
- [ ] No ambiguous format instruction ("clean" or "readable" without specifics)

---

### Scoring Calculation (Weighted)

Calculate a single consolidated score starting from **100**:

| Category | Penalty per FAIL |
|---|---|
| **Structure & Caching** | -20 pts |
| **Validation Gaps** | -15 pts |
| **Tool Density** | -10 pts |
| **Word Discipline** | -5 pts |

Minimum score is 0. Use this weighted system for the "Overall Score" in the report.

---

### Audit Rating Scale
- 90–100: Excellent — cache-ready, minimal waste
- 70–89:  Good — minor rewrites needed
- 50–69:  Fair — structural issues, moderate token waste
- Below 50: Poor — significant refactoring required

---

## Step 2 — Produce Combined Report

```
SKILL/AGENT AUDIT REPORT
=========================
Input type: [SKILL.md / Agent definition / System prompt / Template]
Estimated tokens: [N]
Static blocks: [N tokens] — cache eligible
Dynamic blocks: [N tokens] — re-processed each call

TOKEN EFFICIENCY SCORE: [N/100] — [rating]
VALIDATION SCORE:       [N/100] — [rating]

CRITICAL ISSUES (FAIL)
----------------------
[issue]: [location] → [one-line fix]

WARNINGS (WARN)
---------------
[issue]: [location] → [one-line fix]

IMPACT-RANKED REWRITES
----------------------
(Ranked by token delta / caching ROI)

1. [Block Name]
   Original: [text]
   Rewritten: [text]
   Delta: -N tokens | ROI: [High/Med/Low]

[...Repeat for all identified blocks...]

CACHING STRATEGY
----------------
Cacheable prefix length: [N tokens]
Status: [Optimized / Needs Refactor]
Action: [Specific move to ensure static prefix exceeds 1,024 tokens]

OVERALL RECOMMENDATION
----------------------
[Priority-ordered roadmap for implementation.]
```

---

## Format Options

| Option | Includes |
|---|---|
| Quick check | Score + top 3 issues only |
| Full audit (default) | Complete report, both sections |
| Rewrite only | Rewritten content + token delta, no report |
| Validation only | Structural checklist only, no token analysis |

Ask the user which they want if not specified.

---

## Rewrite Rules Reference

Load on demand: read `references/rewrite-rules.md` for anti-pattern → fix mappings.

---

## Examples

Load on demand: read `references/examples.md` for concrete Input → Output audit examples.

---

## Notes

- Token estimates use character-based heuristics (±30%). For billing-accurate counts: google.generativeai.count_tokens() (Gemini SDK).
- Scores are directional indicators, not exact measurements.
