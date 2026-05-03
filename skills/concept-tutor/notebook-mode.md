# Concept Tutor: Notebook Mode

Load this file only when `--notebook` is active or user says "teach me X and save it".

## Pre-step (before teaching)

1. **Search** — Grep `/c/workarea/notebook/` across `20-domains/`, `00-projects/`, and `10-personal-knowledge/` for the topic name or related concept slugs
2. **If notes found** — Read them. Establish what depth level was reached and what was covered
3. **Resume** — Tell the learner: "I found your previous notes on [topic]. You covered [X]. Picking up from [Y]."
4. **If no notes found** — Proceed with full Assess step (gauge learner from scratch)

**Explicit resume triggers:** "continue teaching me", "where did we leave off", "resume my lessons on", "pick up where we left off"

## Core

Run the standard teaching flow (Steps 1–8).

## Post-step (after teaching)

- Delegate to agent-note-taker to capture the lesson into the appropriate tier
- **Tier 1 offer:** When teaching general domain topics (IFRS 16, ASC 842, SAP patterns, etc.) that apply across projects, offer: "This looks like Tier 1 knowledge — want me to propose it for `documentation/platform/domain-concepts/`?" Draft only; user confirms, then agent-codebase-archaeologist --domain formalizes it.
