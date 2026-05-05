---
name: concept-tutor-notebook
description: 'Manages notebook searching, context resumption, and capture workflow. Triggers: "--notebook", "teach me and save it".'
---
# Concept Tutor: Notebook Mode

Load this file only when `--notebook` is active or user says "teach me X and save it".

## Pre-step (before teaching)

1. **Search** — Grep `{notebook-root}/` across `20-domains/`, `00-projects/`, and `10-personal-knowledge/` for the topic name or related concept slugs
2. **If notes found** — Read them. Establish what depth level was reached and what was covered
3. **Resume** — Tell the learner: "I found your previous notes on [topic]. You covered [X]. Picking up from [Y]."
4. **If no notes found** — Proceed with full Assess step (gauge learner from scratch)

**Explicit resume triggers:** "continue teaching me", "where did we leave off", "resume my lessons on", "pick up where we left off"   

## Core

Run the standard teaching flow (Steps 1–8). **Always include the Flow Summary** — do not skip it.

## Post-step (after teaching)

Pass the FULL lesson verbatim to agent-note-taker — never summarize or condense. Include:
- Lesson title and topic
- All prose sections (The Problem, Core Idea, Examples, Build-up)  
- Flow Summary (Confirmed flow, Key insights, Misconceptions busted, Vocabulary)
- Practice exercise

Delegate immediately after the lesson ends — do not wait for user to ask.

**Folder targeting:**

| Content type | Notebook tier |
|---|---|
| General concept (design pattern, protocol, algorithm) | `20-domains/` |
| Project-specific topic (how X works in our codebase) | `00-projects/{project-name}/` |

State which tier you're targeting before delegating. If ambiguous, ask the user.

**Tier 1 offer:** When teaching general domain topics (IFRS 16, ASC 842, SAP patterns, etc.) that apply across projects, offer: "This looks like Tier 1 knowledge — want me to propose it for `documentation/platform/domain-concepts/`?" Draft only; user confirms, then agent-codebase-archaeologist --domain formalizes it.

## Boundaries

Never write to the notebook directly. Never create, edit, or delete notebook files.
agent-note-taker owns all file operations inside `{notebook-root}/`.
