---
name: domain-knowledge
description: >
  Governs the creation of public domain knowledge files.
  **Reactive:** "document [concept] for the knowledge base", "how does [X] work in the industry".
  **Proactive:** "discover domain knowledge in [code_path]".
  Orchestrates discovery, pedagogical planning, and delegated writing for a standalone knowledge base.

---

# Domain Knowledge Skill (Router)

**Purpose:** Rules for writing public domain knowledge files in `knowledge/<domain>/` folders.

## Workflows

### 1. Reactive Workflow (User-Driven)
Trigger: explicit request to document a single concept.

1. **Research** (Main Session): Raw facts, snippets, links.
2. **Strategize** (learning-strategy): Structured "Pedagogical Plan".
3. **Execute** (agent-concept-tutor): Write `.md` file based on plan.
4. **Review** (agent-concept-tutor): Self-review against plan.

### 2. Discovery Workflow (Code-Driven)
Trigger: `discover domain knowledge in [path]`.

1. **Scan** (archaeologist): List potential domain keywords.
2. **Backlog** (Main): Update `_keywords.md` (dedupe/cap).
3. **Triage** (Main): 3-Question Rule + Cluster proprietary terms.
4. **Propose** (Main): User approves concept clusters.
5. **Plan** (learning-strategy): detailed pedagogical plan.
6. **Execute** (agent-concept-tutor): Final writing and self-review.
7. **Prune** (Main): Remove cluster from `_keywords.md`.
8. **Index** (Main): Update `_INDEX.md` Tiers (Stand/Walk/Run).

## Core Mandates

1. **Lazy Loading:** Read `TEMPLATES.md` for structure, `WORKFLOWS.md` for discovery, `RULES.md` for governance.
2. **Decision Rule:** Apply 3-Question Rule in `RULES.md` to assign to `knowledge/` vs `documentation/`.
3. **Reference Rules:** `knowledge/` -> `documentation/` (OK); `documentation/` -> `knowledge/` (Stub only).

## File Locations

- **Rules:** `$HOME/.gemini/skills/domain-knowledge/RULES.md`
- **Templates:** `$HOME/.gemini/skills/domain-knowledge/TEMPLATES.md`
- **Workflows:** `$HOME/.gemini/skills/domain-knowledge/WORKFLOWS.md`

## Lifecycle & Sync

- **Validation:** Snapshot-date > 12 months = `status: stale`.
- **Sync:** Decision backlog in `knowledge/_PENDING_SYNC.md`. Sync to notebook is user-triggered.

---

## Decision Values for _PENDING_SYNC.md

`pending` · `promote` (Option A) · `stub` (Option B) · `keep` (Option C)
