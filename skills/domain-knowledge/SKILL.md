---
name: domain-knowledge
description: >
  Governs the creation of public domain knowledge files.
  **Reactive Mode:** Trigger with "document [concept] for the knowledge base".
  **Proactive Mode:** Trigger with "discover domain knowledge in [code_path], n=[number]".
  This skill orchestrates a workflow of discovery, pedagogical planning, and delegated writing to build a pure, standalone knowledge base.

---

# Domain Knowledge Skill (Router)

**Purpose:** Rules for writing public domain knowledge files in `knowledge/<domain>/` folders.

## Workflows

This skill operates in two modes:

### 1. Reactive Workflow (User-Driven)

Triggered when a user explicitly asks to document a single concept.

| Step | Phase      | Handler                   | Output                                                               |
|------|------------|---------------------------|----------------------------------------------------------------------|
| 1    | Research   | Gemini (Main Session)     | Raw facts, code snippets, web links for one concept.                 |
| 2    | Strategize | `learning-strategy` skill | A structured "Pedagogical Plan" with why, analogy, and key points.   |
| 3    | Execute    | `agent-concept-tutor`     | The final, well-written `.md` file based on the plan.                |
| 4    | Review     | `agent-concept-tutor`     | The agent is responsible for reviewing its own output against the plan. |

### 2. Discovery Workflow (Code-Driven, Proactive)

Triggered by `discover domain knowledge in [path], n=[5]`. Automatically finds and documents `n` missing concepts from a given codebase area.

| Step | Phase          | Handler                             | Output                                                                                                        |
|------|----------------|-------------------------------------|---------------------------------------------------------------------------------------------------------------|
| 1    | Scan Codebase  | `agent-codebase-archaeologist`      | A list of potential domain keywords (from class names, etc.).                                                 |
| 2    | Update Backlog | Gemini (Main Session)               | New keywords are added to `knowledge/<domain>/keywords.md`.                                                   |
| 3    | Gap Analysis   | Gemini (Main Session)               | The skill compares `keywords.md` with existing `.md` files to find what's missing.                            |
| 4    | Document Batch | **Reactive Workflow** (steps 1-4) | The skill loops `n` times, running the full reactive workflow for the top `n` missing keywords.               |
| 5    | Prune Backlog  | Gemini (Main Session)               | Once a document is created, the keyword is removed from `keywords.md`.                                        |

## Core Mandates


1. **Lazy Loading:** For detailed templates, read `TEMPLATES.md`. For discovery workflows, read `WORKFLOWS.md`. For foundational governance, read `RULES.md`.
2. **Decision Rule:** Apply the three-question decision rule in `RULES.md` to assign concepts to `knowledge/`, `documentation/domain/`, or `documentation/platform/`.
3. **Reference Rules:** `knowledge/` may point to `documentation/`, but `documentation/` must NOT depend on `knowledge/` (use stubs only).

## File Locations

- **Foundational Rules:** `C:/Users/dexte/.gemini/skills/domain-knowledge/RULES.md`
- **Detailed Templates:** `C:/Users/dexte/.gemini/skills/domain-knowledge/TEMPLATES.md`
- **Discovery Workflows:** `C:/Users/dexte/.gemini/skills/domain-knowledge/WORKFLOWS.md`

## Ownership and Delegation

This skill follows a "Strategize, then Delegate" model.

| Step | Phase | Handler | Output |
|------|-------|---------|--------|
| 1 | Research | Gemini (Main Session) | Raw facts, code snippets, web links. |
| 2 | Strategize | `learning-strategy` skill | A structured "Pedagogical Plan" with why, analogy, and key points. |
| 3 | Execute | `agent-concept-tutor` | The final, well-written `.md` file based on the plan. |
| 4 | Review | `agent-concept-tutor` | The agent is responsible for reviewing its own output against the plan. |

**Workflow:**
1. User triggers this skill (e.g., "document [concept]").
2. The Main Session performs initial research to gather raw facts.
3. This skill then invokes the `learning-strategy` skill to generate a Pedagogical Plan from the raw facts.
4. Finally, this skill invokes `agent-concept-tutor`, providing it with the detailed plan for execution.

## Lifecycle & Sync

- **Validation:** Snapshot-date > 12 months = `status: stale`.
- **Sync:** Decision backlog managed in `knowledge/_PENDING_SYNC.md`. Sync to notebook is user-triggered.

---

## Decision Values for _PENDING_SYNC.md

`pending` · `promote` (Option A) · `stub` (Option B) · `keep` (Option C)
