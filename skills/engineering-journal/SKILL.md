---
name: engineering-journal
description: >-
  Captures project-specific engineering knowledge alongside code: decisions (ADRs),
  dead ends, gotchas/config facts, and progressively improved runbooks. Triggers on:
  "log a decision", "ADR", "gotcha", "dead end", "tried and failed", "config fact",
  "hard-won fix", "update runbook", "how did we set up [X]", "engineering journal",
  "knowledge log", "sweep knowledge log". NOT for README, API docs, concept tutorials,
  or personal learning notes.
---

# Engineering Journal Skill

**Purpose:** Maintain a project's institutional memory — the knowledge that lives between
the code and the README. Decisions, dead ends, hard-won discoveries, and operational
runbooks that would otherwise rot in Slack threads or leave with the engineer who found them.

**Boundary with `domain-knowledge` skill:** Domain-knowledge captures public-domain concepts
(what is OAuth2, what is event sourcing). Engineering-journal captures project-specific
facts (why WE chose OAuth2, how WE configured Azure for THIS app, what WE tried and abandoned).
If it requires knowing this project's context to be useful, it belongs here.

---

## Document Structure

Create in `engineering-log/` at the project root:

```
engineering-log/
  INDEX.md          topic index — one line per entry, maintained across all categories
  decisions/        ADR-style numbered files  (001-use-postgres.md, 002-drop-redis.md)
  discoveries.md    gotchas, config facts, hard-won fixes — chronological append-only
  dead-ends/        what was tried and abandoned — one file per dead end
  runbooks/         progressively improved step-by-step guides (one file per procedure)
```

If `engineering-log/` does not exist yet, create it with an empty `INDEX.md` before writing
the first entry.

---

## Entry Templates

### 1. Decision (ADR-style — use for: why we chose X, why we rejected Y, architectural choices)

```markdown
# ADR-NNN: [Short imperative title — e.g., "Use PostgreSQL over MongoDB"]

**Date:** YYYY-MM-DD
**Status:** Accepted | Superseded by ADR-NNN | Deprecated
**Tags:** [comma-separated — e.g., database, auth, deployment]

## Context
What forces were at play? What problem triggered this decision? Include constraints,
team size, timeline pressure, existing system dependencies — anything that makes
the decision make sense to someone who wasn't in the room.

## Decision
What was chosen. One clear statement.

## Alternatives Considered
| Option | Why It Lost |
|--------|-------------|
| Option A | [specific reason] |
| Option B | [specific reason] |

## Consequences
- **Easier now:** [what this unlocks]
- **Harder now:** [what this costs]
- **We must now:** [any commitments this creates]
```

File naming: `decisions/NNN-short-title.md` where NNN is zero-padded (001, 002, ...).
Never edit a past decision — if it changes, create a new ADR with `Supersedes: ADR-NNN`.

---

### 2. Discovery (use for: gotchas, config facts, environment quirks, hard-won fixes)

Append to `discoveries.md` — one section per entry, newest at the bottom.

```markdown
## [One-line grep-friendly summary — e.g., "load_dotenv() must run before project imports"]
**Date:** YYYY-MM-DD | **Tags:** [topics] | **Scope:** [service or module]

[The fact. What was discovered. Why it matters. What to do — or what NOT to do.]
```

Keep it short. If it needs more than a paragraph, consider whether it belongs in a
runbook or the README instead.

---

### 3. Dead End (use for: approaches tried and abandoned, what to avoid repeating)

Create one file per dead end: `dead-ends/YYYY-MM-DD-short-title.md`

```markdown
# Dead End: [What Was Attempted]

**Date:** YYYY-MM-DD
**Tags:** [topics]
**Time Invested:** [rough estimate — helps future engineers calibrate whether to re-attempt]

## What We Tried
The approach, concisely. Enough detail that someone could reconstruct what was attempted.

## Why It Failed
The specific failure mode — not just "it didn't work." What broke, what the error was,
what assumption turned out to be wrong.

## What We Learned
The takeaway. What this rules out. What to try instead, if known.
```

---

### 4. Runbook (use for: configuration procedures, setup recipes, operational steps)

Create one file per procedure: `runbooks/short-title.md`

Runbooks are **living documents** — updated each time someone follows or corrects the steps.

```markdown
# Runbook: [What This Configures — e.g., "Azure App Registration for OAuth"]

**Last verified:** YYYY-MM-DD
**Verified against:** [version/environment — e.g., "Azure Portal as of July 2026"]
**Tags:** [topics]
**Prereqs:** [what must exist before starting — accounts, permissions, prior runbooks]

## Steps

1. [Action verb] [what to do] [where to do it]
   - Expected result: [what you should see]
   - If instead you see [X]: [what went wrong and how to fix]

2. [Next step...]
   - Key value: `exact-value-or-pattern`
   - Why: [brief reason this matters — not just "because docs say so"]

## Verification
[How to confirm the procedure worked end-to-end. A curl command, a test login, etc.]

## Changelog
| Date | What Changed | Why |
|------|-------------|-----|
| YYYY-MM-DD | Initial creation | [context] |
| YYYY-MM-DD | Fixed step 3 redirect URI | Was missing trailing slash |
```

**Progressive improvement rule:** Every time someone follows a runbook and hits a snag,
update the relevant step with the fix or add a "If instead you see" clarification.
The changelog at the bottom tracks what evolved and why.

---

## Triggers and What to Create

| User says... | Action |
|---|---|
| "log a decision", "record decision", "ADR", "why did we choose" | New file in `decisions/` |
| "gotcha", "record a gotcha", "discovered that", "config fact", "hard-won fix" | Append to `discoveries.md` |
| "dead end", "this didn't work", "abandoned approach", "tried and failed" | New file in `dead-ends/` |
| "update runbook", "add to runbook", "how did we set up [X]", "config steps" | Create or update in `runbooks/` |
| "what do we know about [topic]", "check knowledge log" | Search INDEX.md and relevant files by tag |
| "sweep knowledge log", "stale entries" | Review entries older than 6 months referencing removed components |

After writing any entry, update `INDEX.md` with a one-line summary:
```
[YYYY-MM-DD] [TYPE] [tags] — [one-line summary]  ->  [filename]
```

Where TYPE is one of: DECISION, DISCOVERY, DEAD-END, RUNBOOK.

---

## Boundary Rules — What Belongs Here vs Elsewhere

| Content | Belongs In |
|---|---|
| Why we chose technology X over Y | `decisions/` (here) |
| How to install and run the project | README |
| Port 8443 is reserved on the staging server | `discoveries.md` (here) |
| Step-by-step Azure App Registration setup | `runbooks/` (here) |
| `load_dotenv()` must run before project imports | `discoveries.md` (here) |
| How OAuth2 works conceptually | `domain-knowledge` skill / concept notebook |
| We tried event sourcing and abandoned it after sprint 3 | `dead-ends/` (here) |
| API endpoint documentation | API reference / `documentation-specialist` |
| Bug fix details | Git commit message / PR description |
| Temporary workaround that expires | `discoveries.md` with an `**Expires:**` tag |
| How to configure [service] for this project | `runbooks/` (here) |

**The litmus test:** If a new team member would need this to avoid a painful mistake or
reproduce a setup without hand-holding, it belongs here. If it explains how something
works in general (any project, any team), it belongs in domain-knowledge.

---

## Entry Quality

Good: answers WHY (not just what), has date + tag + scope, first line is grep-friendly, understandable without follow-up questions.

Bad: no reasoning, no tags/date, requires prior context, over a page long, duplicates README or code comments.

---

## Append-Only Rule (decisions, discoveries, dead-ends)

Never edit a past entry's content — it is a record of what was known at that time.
If something changes or was wrong:
- For decisions: write a new ADR with `Supersedes: ADR-NNN`
- For discoveries: append a new entry with `Corrects: [date of original entry]`
- For dead ends: append a note to the original file under `## Update YYYY-MM-DD`

This preserves the project's timeline of reasoning — "what did we know when?" is as
valuable as "what do we know now?"

**Exception:** Runbooks are living documents and SHOULD be edited in place (with changelog).

