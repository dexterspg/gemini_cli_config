---
name: domain-knowledge
description: Use when writing public domain knowledge files into a project's knowledge/<domain>/ folder. Triggers when: "research [concept] for the knowledge base", "add [topic] to knowledge/", "document domain knowledge for [project]", "write knowledge base entry for [concept]". This skill governs how Gemini writes concept files in knowledge/<domain>/ — covering frontmatter, content structure, scope boundaries, deduplication, and lifecycle rules. Do NOT trigger for project-specific documentation (that goes in documentation/domain/NN-*.md) or platform interpretations (that goes in documentation/platform/domain-concepts/).
---

# Domain Knowledge Skill (Router)

**Purpose:** Rules for writing public domain knowledge files in `knowledge/<domain>/` folders.

## Core Mandates

1. **Lazy Loading:** For detailed templates, read `TEMPLATES.md`. For discovery workflows, read `WORKFLOWS.md`. For foundational governance, read `RULES.md`.
2. **Decision Rule:** Apply the three-question decision rule in `RULES.md` to assign concepts to `knowledge/`, `documentation/domain/`, or `documentation/platform/`.
3. **Reference Rules:** `knowledge/` may point to `documentation/`, but `documentation/` must NOT depend on `knowledge/` (use stubs only).

## File Locations

- **Foundational Rules:** `C:/Users/dexte/.gemini/skills/domain-knowledge/RULES.md`
- **Detailed Templates:** `C:/Users/dexte/.gemini/skills/domain-knowledge/TEMPLATES.md`
- **Discovery Workflows:** `C:/Users/dexte/.gemini/skills/domain-knowledge/WORKFLOWS.md`

## Ownership and fallback

| Condition | Handler |
|---|---|
| agent-gemini available | agent-gemini — codebase discovery + web research + writes `knowledge/` files |
| agent-gemini NOT available | agent-codebase-archaeologist (discovery) + main session or concept-tutor (writes files from known domain knowledge) |

## Lifecycle & Sync

- **Validation:** Snapshot-date > 12 months = `status: stale`.
- **Sync:** Decision backlog managed in `knowledge/_PENDING_SYNC.md`. Sync to notebook is user-triggered.

---

## Decision Values for _PENDING_SYNC.md

`pending` · `promote` (Option A) · `stub` (Option B) · `keep` (Option C)
