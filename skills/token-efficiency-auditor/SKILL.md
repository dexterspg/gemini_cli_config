---
name: token-efficiency-auditor
description: >-
  Audit and validate Gemini agent system prompts, SKILL.md files, and prompt templates
  for token waste, context inefficiency, and structural correctness. Use this skill whenever
  the user wants to check, review, score, validate, or improve a prompt, agent definition,
  or skill file — for token efficiency, caching potential, verbosity, or structural
  completeness. Triggers on: "check my prompt", "is this token efficient", "audit my skill",
  "validate my agent", "review my SKILL.md", "is my skill correct", "does this skill have
  everything it needs", "too verbose?", "optimize my system prompt", "how many tokens is this",
  "can I make this shorter", "is my agent well structured".
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
| Path under an `agents/` folder, or a `Role:` / `Tools:` block | Agent definition |
| File named `SKILL.md`, or `---` frontmatter with `name:` and `description:` outside `agents/` | SKILL.md |
| Markdown table with `Trigger` and `Action` / `Route to` columns | GEMINI.md routing table |
| References other files by heading/section to pick which one to read next, without restating their rules | Dispatch/router file (apply "Dispatch / Router File Economics" under AUDIT 1) |
| `{placeholder}` or `[slot]` syntax | Prompt template |
| None of the above | System prompt |

- File path provided → read first
- Description only → ask for actual content
- < 10 tokens or unrecognizable → reject with: "Provide a system prompt, SKILL.md, agent definition, or prompt template."

**Do NOT trigger for:**
- General code review → code-review skill
- Writing a skill/agent from scratch → skill-creator skill

---

## AUDIT 1 — Token Efficiency

### Token Classification

Estimate token count (±30% variance):
- English prose: 1 token ≈ 4 characters
- Code: 1 token ≈ 3 characters
- Label-colon blocks: ~30–50% cheaper than prose equivalent
- XML tag pairs: ~2–6 tokens each

Classify each block:
- STATIC: never changes across calls → cache candidate
- DYNAMIC: changes per call → must be in user turn
- MIXED: static framing with dynamic slots → needs refactoring

Flag DYNAMIC content inside the system prompt as highest-priority — it destroys cache hits on every call.

---

### Token Efficiency Checklist

Mark each: PASS / WARN / FAIL

#### Structure
- [ ] Static content before dynamic content
- [ ] Dynamic variables in user turn, not system prompt
- [ ] Clear boundary between instructions and data
- [ ] Most stable content (tools, task statement) comes first
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
- [ ] Task statement is first line, not buried; no identity line ("You are a…")
- [ ] Scope limiters appear before the task, not after
- [ ] Data / content to act on is last

#### Caching Potential
- [ ] No timestamps, UUIDs, or session IDs in static blocks
- [ ] Tool definitions are in stable deterministic order
- [ ] Few-shot examples are frozen, not dynamically generated
- [ ] Cache breakpoint is placeable after the static prefix

#### Runtime Read Cost (only if the file tells Gemini to read files or call tools)

The checks above size the prompt file; these size what a run makes the model read. Fails fold into the **Structure** deduction.
- [ ] Source checks ordered cheapest first, and the costliest (large source, many files, a subagent) only when a question is left? *Fail: a fixed expensive step before a cheap one that usually answers.*
- [ ] "Do we already have X" names a search (a grep over an index, a listing)? *Fail: "read the index/README" for a large file, or a hand-kept index with no `--check` (a stale index costs more than it saves).*
- [ ] What a run reads is saved with its pin so a later step does not re-read it? *Fail: review re-reads the same source.*
- [ ] Spawns a subagent or a panel only for a stated reason — reads far more than the answer needs, independent parallel parts, an independent check, a permission boundary, an outside tool? *Fail: a fixed fan-out on every input (e.g. four reviewer personas for a one-file review). Multi-agent runs cost several times a single agent's tokens; figures and the local test: `~/.gemini/skills/quality-guardian/EVIDENCE-agent-design.md` → rules 4 and 9.*

---

### Dispatch / Router File Economics (only if Step 1 classified this as a dispatch/router file)

Mark each PASS / WARN / FAIL; folds into the **Structure** deduction (-15 per FAIL). **This covers
TOKEN COST shape only** — whether the decision tree is correct (unreachable rows, ambiguous
branches) is `agent-quality-guardian`'s call (`CHECKLIST-agents-skills.md` → its dispatch items);
run both, neither substitutes.

- [ ] **Fully static, no per-call dynamic content?** → Strong caching candidate; confirm it sits in a
        stable-prefix zone of anything that loads it.
- [ ] **Dispatch file small relative to the smaller source file it routes into?** *Fail: it
        approaches or exceeds that file's size — collapse it into that file's opening section.*
- [ ] **Does any fact `agent-quality-guardian` confirmed branch-specific still sit in the always-loaded
        shared body instead of its branch's target?** (Universal-vs-branch is its call, not yours.)
        *Fail: every branch pays that fact's token cost on every load.*
- [ ] **Row/mode count past ~10 without re-justifying the split?** *WARN, not FAIL: each row is fixed
        cost on every load; check whether rows are one mode with a cosmetic difference.*
- [ ] **Per-row cells as terse as the disambiguation needs?** Apply the Word Discipline anti-pattern
        table to cells too.

---

### Token Efficiency Score

```
Start: 100
Deduct per FAIL:
  Caching Potential: -20
  Structure:         -15
  Sentence Order:    -7
  Word Discipline:   -3
Output: overall score (floor 0) + per-category breakdown
```

- 90–100: Excellent — cache-ready, minimal waste
- 70–89:  Good — minor rewrites needed
- 50–69:  Fair — structural issues, moderate token waste
- Below 50: Poor — significant refactoring required

Prioritize Structure and Caching FAILs in the recommendation section — they carry higher real-world cost.

---

## AUDIT 2 — Skill/Agent Validation

### Skill Validation Checklist (SKILL.md only)

Mark each: PASS / WARN / FAIL / N/A — use N/A for a whole subsection that doesn't
apply to this input (e.g. Capabilities/Never on a SKILL.md), never to dodge a real check.

#### Frontmatter
- [ ] Has `name:` — short, lowercase, hyphenated
- [ ] Has `description:` — not empty
- [ ] Description is quoted if it contains `: ` (colon-space) to prevent YAML parsing ambiguity.
        If the description also contains embedded double quotes, use a block scalar (`>-`) instead of double quotes to avoid backslash escaping.
- [ ] Description states WHAT the skill does
- [ ] Description states WHEN to trigger (specific contexts, not just a category)
- [ ] Description includes example trigger phrases — but is ≤ ~150 tokens: it loads every session, the body only when invoked, so each added phrase pays that cost every session
- [ ] Description triggers on implicit user intent, not just exact keywords

#### Trigger Design
- [ ] Trigger conditions are explicit in the body
- [ ] Has a "Do NOT trigger for" section with routing alternatives
- [ ] Trigger phrases — including in the description — are literal user-typed strings covering
        casual/implicit variants, not category labels
        Bad: "Tool operations" | Good: "create [entity]", "is this any good?"
- [ ] No overlap with other known skills causing ambiguous routing
- [ ] Every load instruction (dependencies, always-load skills) is MANDATORY with a stated
        condition, never advisory — this applies to LOADING a file/skill specifically (skipping
        it silently is the failure mode), not to behavioral rules elsewhere in the body
        Bad: "load when relevant" | Good: "MANDATORY: Load [file] when [condition]"
- [ ] A behavioral/procedural rule (not a load instruction) uses one of three legal registers:
        MANDATORY (a real hard boundary — tool access, security, data integrity, or a fragile
        fixed sequence; states why it can't flex), CONDITIONAL ("when X, do Y; when not-X, [fallback/judgment]"), or ADVISORY
        (a stated default the model may override with judgment). Flag miscategorization — a
        judgment call written as MANDATORY with no stated rationale — not the mere presence of
        conditional or advisory phrasing.
- [ ] A rule's strictness matches the task's fragility and variability — a fragile,
        sequence-critical or consistency-critical operation keeps MANDATORY wording; a
        context-dependent judgment gets CONDITIONAL or ADVISORY.

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
- [ ] Holds only what Gemini cannot know (project facts, user preferences, verified tool behaviour)? Owner: `CHECKLIST-agents-skills.md` → "For Skill Files".
- [ ] Examples present following Input → Output pattern
- [ ] Examples are concrete, not abstract
- [ ] Instruction-to-example ratio is proportional (examples ≤ 40% of total body)
- [ ] Notes section present for caveats and limitations

#### Size and Loadability
- [ ] Body is under 480 lines AND ~5,000 tokens (WARN above) — dense lines hide cost; line count alone passes a 129-line, 5,000-token file
- [ ] Large reference content (examples, lookup tables) moved to `references/` subfolder if body exceeds 480 lines or ~5,000 tokens
- [ ] References loaded on demand, not always in context
- [ ] Multiple domains/variants organized into subfolders with router in SKILL.md

---

### GEMINI.md Routing Table Validation Checklist (GEMINI.md routing table only)

Mark each: PASS / WARN / FAIL / N/A

- [ ] Each trigger cell contains literal strings user would type, not category labels
        Bad: "Tool operations" | Good: "create [entity]", "check [entity] status"
- [ ] Each action cell contains a MANDATORY load instruction with exact file path
- [ ] Conditional variants are handled inline
        Bad: no variants | Good: "If [variant]: also load ~/.gemini/skills/[skill]/workflows/[VARIANT.md]"
- [ ] No advisory phrasing in action cells
        Bad: "Read skill first" | Good: "MANDATORY: Load [path] first"

---

### Agent Validation Checklist (Agent definitions only)

Mark each: PASS / WARN / FAIL / N/A — same rule as the Skill checklist above.

#### Purpose line
- [ ] First line states the task in the imperative; no identity line ("You are a Senior X") — personas do not reliably improve accuracy (`~/.gemini/skills/quality-guardian/EVIDENCE-agent-design.md` → rule 1)
- [ ] Task is specific (not "help with anything")
- [ ] Domain or stack named if relevant

#### Capabilities and Constraints
- [ ] No Capabilities list that restates rules defined elsewhere in the file — it is read on every spawn and drifts; keep one only for an ability no other section states
- [ ] Constraints (Never:) are in their own block, not prose equivalents
- [ ] Each Never: item names the agent or skill that owns that responsibility
        (e.g. "Never write notebook files — agent-note-taker owns them" — not just "Never save files")
- [ ] Each Never: item is scoped to what its owner owns, and no mode's MANDATORY procedure does what a Never: forbids? *Fail: concept-tutor's "Never: Write files" blocked the files its own `--sandbox` mode must write.*
- [ ] No capability or constraint duplicated across sections

#### Tool Definitions
- [ ] Each tool has a one-sentence description max
- [ ] Tool descriptions say when to use, not just what the tool does
- [ ] Tool parameter descriptions are terse (type + purpose only)
- [ ] No unused optional parameters included
- [ ] Tool list order is stable and deterministic
- [ ] No redundant `required: true` on default-required fields
- [ ] Parameter descriptions use "X (type)" not "a type that represents X"

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

### Validation Score

```
Score = (PASS + 0.5 × WARN) / (total checks − N/A) × 100
```

`total checks` excludes every item marked N/A — an inapplicable subsection must never lower the
score. `WARN` earns half credit here only; AUDIT 1 deducts per `FAIL` alone. Same 90/70/50 bands as AUDIT 1.

**When the input is a system prompt or prompt template, no checklist above applies** — report
`VALIDATION SCORE: N/A — no structural checklist for this input type` rather than computing one.

---

## Step 2 — Produce Combined Report

```
SKILL/AGENT AUDIT REPORT
=========================
Input type: [SKILL.md / Agent definition / System prompt / GEMINI.md / Template]
Estimated tokens: [N]
Static blocks: [N tokens] — cache eligible
Dynamic blocks: [N tokens] — re-processed each call
Mixed blocks: [N tokens] — static framing with dynamic slots, needs refactoring

TOKEN EFFICIENCY SCORE: [N/100] — [rating]
  Breakdown: Caching [-N] | Structure [-N] | Sentence Order [-N] | Word Discipline [-N]
VALIDATION SCORE:       [N/100] — [rating]

CRITICAL ISSUES (FAIL)
----------------------
[issue]: [location] → [one-line fix]

WARNINGS (WARN)
---------------
[issue]: [location] → [one-line fix]

ALL REWRITES (ranked by token impact)
--------------
Original:
[block]
↓
Rewritten:
[block]
Token delta: [+N / -N] tokens ([+N% / -N%])
Trade-off: [required if delta is positive — state what was gained and why it justifies the cost]

CACHING RECOMMENDATION
----------------------
Cacheable prefix: [yes/no]
Estimated cache savings: [N% per call after first]
Action: [specific change needed]

STRUCTURAL GAPS
---------------
[missing section or field] → [what to add]

OVERALL RECOMMENDATION
----------------------
[2–3 sentences. Priority order. Expected improvement if all fixes applied.]
```

---

## Trim Mode — shorten an existing file without losing behavior

On "can I make this shorter" / "trim" / "reduce tokens" for an existing file. Never trim on sight:

1. **Classify each sentence:** DIRECTIVE (changes an action) · VERIFIED FACT · RATIONALE · PROVENANCE (date, incident) · DUPLICATE. Cut only RATIONALE, PROVENANCE, DUPLICATE; keep at most the one clause naming the wrong action a future editor would re-propose.
2. **Test each cut:** delete it — does any action or output change? Yes → keep it, or move it to a file that loads at the same moment, never one that loads less often.
3. **Prove it:** run a behaviour gate if a suite exists; no suite → report the trim as `Behaviour gate: unproven (no suite).`
4. **Growth check:** compare tokens with the first audited size (`git log`); flag > +5% net with no recorded eval. Each added line names what it cut, or why nothing could be.
5. **Report cuts as well as adds,** each with its token delta, and finish with the gate's last line (`Behaviour gate: unproven (no suite).` or the `no sign of loss` result); a reply without it is incomplete.

---

## Format Options

| Option | Includes |
|---|---|
| Quick check | Score + top 3 issues only |
| Full audit (default) | Complete report, both sections |
| Rewrite only | Rewritten content + token delta + Behaviour gate result, no report |
| Validation only | Structural checklist only, no token analysis |
| Clarity check (opt-in) | Report-only list of ambiguity: sentences over 20 words or with several instructions, one thing named by several words, one word with two meanings, passive or stacked-modal phrasing. No rewrite, no score change. |

Not specified → Full audit. Never ask: a subagent or unattended run cannot answer.

---

## Rewrite Rules Reference

MANDATORY: Load `references/rewrite-rules.md` before producing the ALL REWRITES section of the
report — its anti-pattern → fix mappings are not reproducible from this file alone.

---

## Examples

MANDATORY: Load `references/examples.md` when the user requests a worked example, or the input
type is unfamiliar and a concrete Input → Output pattern would settle it.

---

## Dependencies

- `references/rewrite-rules.md` — anti-pattern → fix mappings (MANDATORY before producing rewrites)
- `references/examples.md` — worked Input → Output examples (MANDATORY for an unfamiliar input type)
- `~/.gemini/skills/quality-guardian/CHECKLIST-agents-skills.md` and `EVIDENCE-agent-design.md` → "Decision guide" — load when the input is a global agent, skill or GEMINI.md

---

## Notes

- Token estimates use character-based heuristics (±30%).
- Scores are directional indicators, not exact measurements.
- Undertriggering is the highest-cost routing failure — a skill that never loads scores worse than a verbose one that does. But a description is paid every session, so a trigger phrase must earn its tokens.
