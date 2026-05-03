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

| Step | Phase                     | Handler                             | Output                                                                                                                            |
|------|---------------------------|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| 1    | Scan Codebase             | `agent-codebase-archaeologist`      | A list of potential domain keywords.                                                                                              |
| 2    | Update Backlog            | Gemini (Main Session)               | New keywords are added to `knowledge/<domain>/_keywords.md` after being deduplicated and capped.                                |
| 3    | Triage & Cluster          | Gemini (Main Session)               | Keywords are triaged using the 3-Question Rule. Proprietary terms are clustered under broader public concepts.                  |
| 4    | Propose Cluster & Confirm | Gemini (Main Session)               | The proposed concept clusters are presented to the user for approval.                                                             |
| 5    | **Generate Plan**             | `learning-strategy` skill       | For the approved cluster, a detailed pedagogical plan (why, analogy, etc.) is created autonomously.                             |
| 6    | **Execute & Self-Review**     | Gemini & `agent-concept-tutor` | The Main Session assembles a final prompt containing the plan AND existing documents. The tutor executes and self-reviews. |
| 7    | Prune Backlog             | Gemini (Main Session)               | Once documented, all keywords from the cluster are removed from `_keywords.md`.                                                 |
| 8    | **Update Knowledge Puzzle**   | Gemini (Main Session)               | The domain's `_INDEX.md` is updated to place the new concept in its correct Tier (Stand, Walk, or Run).                          |

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

| Step | Phase      | Handler                   | Output                                                               |
|------|------------|---------------------------|----------------------------------------------------------------------|
| 1    | Research   | Gemini (Main Session)     | Raw facts, code snippets, web links for the approved concept(s).     |
| 2    | Strategize | `learning-strategy` skill | A structured "Pedagogical Plan" with why, analogy, and key points.   |
| 3    | Execute    | `agent-concept-tutor`     | The final, well-written `.md` file based on the plan.                |
| 4    | Review     | `agent-concept-tutor`     | The agent is responsible for reviewing its own output against the plan. |

**Discovery Workflow Automation:**
1. User approves a **Concept Cluster** (Step 4 of Discovery).
2. The Main Session autonomously generates the Pedagogical Plan and the context-aware prompt.
3. The `agent-concept-tutor` is invoked to perform the final writing and self-review without further user intervention.

## Lifecycle & Sync

- **Validation:** Snapshot-date > 12 months = `status: stale`.
- **Sync:** Decision backlog managed in `knowledge/_PENDING_SYNC.md`. Sync to notebook is user-triggered.

---

## Decision Values for _PENDING_SYNC.md

`pending` · `promote` (Option A) · `stub` (Option B) · `keep` (Option C)
