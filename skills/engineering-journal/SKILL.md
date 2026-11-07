---
name: engineering-journal
description: >-
  Captures project-specific engineering knowledge alongside code: decisions (ADRs),
  dead ends, gotchas/config facts, and progressively improved runbooks. Triggers on:
  "log a decision", "ADR", "gotcha", "dead end", "tried and failed", "config fact",
  "hard-won fix", "create a runbook", "update runbook", "how did we set up [X]", "setup guide", "engineering journal",
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
If it requires knowing this project's context to be useful, it belongs here. A runbook not about the current project goes to `C:/workarea/runbooks/` (see Known overrides).

---

## Document Structure

Create in `engineering-log/` at the project root (the default; see Known overrides):

```
engineering-log/
  INDEX.md          topic index — one line per entry for discoveries/dead-ends/runbooks only;
                    decisions are NOT indexed here, see "Decision" template below
  decisions/        ADR-style numbered files  (001-use-postgres.md, 002-drop-redis.md)
  discoveries.md    gotchas, config facts, hard-won fixes — chronological append-only
  dead-ends/        what was tried and abandoned — one file per dead end
  runbooks/         progressively improved step-by-step guides (one file per procedure)
```

### Check for a project convention first

**An absent `engineering-log/` is not permission to create one.** It may mean the project keeps
that artifact somewhere else. Before writing any entry, grep `{project-root}/.gemini/skills/**`
and `{project-root}/GEMINI.md` for the category you are about to write (`ADR`/`decision`,
`runbook`, `gotcha`, `dead end`).

A project that documents its own location, filename pattern or template for a category
**overrides this skill for that category only**. Write there, in that format — the project convention wins in full:
path, filename, section set, and status vocabulary — except a runbook not about that project (last row
below). Leave the other categories to this skill.
State which directory you chose and why before writing, so a wrong choice is visible immediately
rather than discovered as a stray folder months later.

Known overrides:

| Project / condition | Category | Goes to instead |
|---|---|---|
| `api-test-app` | decisions | `hurl/adr/ADR-NNN-kebab-title.md` per its `hurl-conventions` skill — do NOT create `engineering-log/decisions/` there |
| any project with a `documentation/` tree | decisions | `documentation/platform/decisions/ADR-NNN-TITLE.md` per `documentation-specialist`, written by `agent-system-architect` |
| a failure caused by one environment's data (a record that must exist or be linked, a company the external system accepts, a scope already full of open items) | discoveries | that project's `docs/environments/<env>-data-blockers.md` if it has one, else ask before creating it; one row per blocker: symptom, a check to run before acting, date. It is read BEFORE acting (global GEMINI.md → Tool Boundaries), so it never waits in `discoveries.md`. `api-test-app`: `docs/environments/ra-env2-data-blockers.md` |
| a runbook not about the current project, or one the user says stays out of its repo | runbooks | `C:/workarea/runbooks/short-title.md`, Runbook template, no `INDEX.md` entry. Overrides a project's runbook convention unless the runbook is about that project. Unsure whether it is: ask. cwd not inside a repo: this row. Create the folder if missing; it is not a git repo, so never commit there. Authoring-time only |

Only once no project convention exists and no row above applies: if `engineering-log/` does not
exist yet, create it with an empty `INDEX.md` before writing the first entry.

---

## Entry Templates

### 1. Decision (ADR-style — use for: why we chose X, why we rejected Y, architectural choices)

One shape for every ADR, regardless of which skill or agent writes it:

```markdown
# ADR-NNN — <short decision title>

**Status:** Accepted | Superseded by ADR-NNN
**Date:** YYYY-MM-DD

## Context
<A few sentences: the problem/tension that forced a choice — nothing more>

## Decision
<The choice made, AND the rejected alternative(s) with why they lost — this is the one
thing an ADR must never omit, and the one thing worth preserving>

## Consequences
<What this commits you to going forward; when to revisit>
```

No `Tags:` line, no mandatory `Alternatives Considered` section (folds into `Decision`), no
`INDEX.md` requirement, no sprawling `Rationale` section. **Carries no operational content** — a
definition, threshold, closed vocabulary, or procedure someone needs to act on today belongs in
the project's own skill/reference file, never the ADR.

An accepted ADR's `Context`/`Decision` is append-only: revisit it with a dated note at the bottom
of the file, or by writing a new ADR whose own `Status` reads `Superseded by ADR-NNN` — never by
editing the original decision in place, and never with a `Supersedes:` key on the new file (the
old file's own `Status` line already carries that relationship, from the side a reader actually
encounters first).

File naming (this skill's own default location, when no project override applies — see "Check for
a project convention first" above): `decisions/NNN-short-title.md`, NNN zero-padded (001, 002, ...).

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

**MANDATORY: before writing, restructuring or reviewing a runbook, load `references/runbook-types.md`** (this skill's folder): the shared section order, the types (API, UI logic, operation, communication, composite), the API per-step block and the 12-point quality gate. For an API runbook the scripts it cites must exist and pass as files first (its gate item 1). A runbook is ordered instructions with an owner, a trigger, an undo and no run history in the steps.

Runbooks are **living documents** — updated each time someone follows or corrects the steps.

The template, the section order per type and the quality gate are in `references/runbook-types.md`.

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
| "create a runbook", "update runbook", "add to runbook", "how did we set up [X]", "config steps" | Create or update in `runbooks/`; for an update or lookup also search `C:/workarea/runbooks/` by filename and `Tags` |
| "what do we know about [topic]", "check knowledge log" | Search INDEX.md and relevant files by tag; also `C:/workarea/runbooks/` by filename and `Tags` |
| "sweep knowledge log", "stale entries" | Review entries older than 6 months referencing removed components |

After writing a DISCOVERY, DEAD-END, or RUNBOOK entry in `engineering-log/`, update `INDEX.md` with a one-line summary:
```
[YYYY-MM-DD] [TYPE] [tags] — [one-line summary]  ->  [filename]
```

Where TYPE is one of: DISCOVERY, DEAD-END, RUNBOOK. **Decisions are not indexed here** — the ADR
Standard has no `INDEX.md` requirement (`Status`/`Superseded by ADR-NNN` on the file itself is
the register); `git log` on `decisions/` is the register when this skill's own default location
is in use.

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
| An ADR in a project whose own skill defines an ADR location | that project's skill — see "Check for a project convention first" |

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
- For decisions: revisit with a dated note at the bottom of the file, or write a new ADR whose
  `Status` reads `Superseded by ADR-NNN` — per the ADR Standard, never a `Supersedes:` key
- For discoveries: append a new entry with `Corrects: [date of original entry]`
- For dead ends: append a note to the original file under `## Update YYYY-MM-DD`

This preserves the project's timeline of reasoning — "what did we know when?" is as
valuable as "what do we know now?"

**Exception:** Runbooks are living documents and SHOULD be edited in place (with changelog).
