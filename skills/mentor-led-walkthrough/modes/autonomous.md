# Autonomous Mode (`--auto`)

Runs same build discipline as Interactive mode with no learner present.
Entry: user must explicitly request `--auto`.

**Execution setup (loop mechanics, cron, never-block, state across runs):**
MANDATORY: Load `~/.gemini/skills/scheduled-automation-routine/SKILL.md` to set up the driver.
The scheduled skill owns HOW runs are triggered and chained. This file owns WHAT the mentor does inside each run.

---

## Journal file

Created at first Self-answer invocation:
`{project-root}/mentor-logs/mentor-log-<artifact-slug>.md` (create `mentor-logs/` if needed).

- `<artifact-slug>` = artifact filename without extension, lowercased, hyphenated — no date, stable across runs
- Header: `**Started:** YYYY-MM-DD` and `**Last updated:** YYYY-MM-DD` (update on each entry)
- Write order: complete and save code round first, then append journal entry — never the reverse

**State reconciliation (on each fresh invocation):** the journal is the only persistent *autonomous-state* file — slice/domain artifacts (Build Log, UML, domain log) are written per SKILL.md's Artifact registry regardless of autonomous mode. Before writing, read existing journal if present. Verify on-disk artifact matches last `Code:` entry — reconcile if crash left unlogged round or logged round never landed. Resume from last numbered entry; never restart numbering.

---

## Self-answer protocol

Wherever Socratic Scope says "ask the learner," Autonomous mode instead:

1. States the question in the journal
2. Answers with best judgment — one paragraph, same reasoning depth as explaining to a learner
3. Tags `[ROUTINE]` if mechanical/single-correct-answer, `[REVIEW]` if genuine judgment call or architecture fork
4. Proceeds — never blocks

Covers genuine Socratic prompts only. Narrated reasoning (design trade-off, method purpose) is logged as stated, not re-answered.

---

## Journal entry format

```
### [N] [ROUTINE|REVIEW] <decision or milestone title>
Q: <what would have been asked>
A: <mentor's own answer + one-line reasoning>
Code: <file path + round, if applicable>
```

---

## Resuming from the journal

Session Wrap-Up still applies, plus: `Flagged for review: N — see entries marked [REVIEW]`.

On resume — read journal, summarize `[REVIEW]` entries and last checkpoint, let learner confirm or overrule each before continuing. Do not silently treat self-answered decisions as final.
