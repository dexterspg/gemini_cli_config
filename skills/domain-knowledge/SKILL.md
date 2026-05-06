---
name: domain-knowledge
description: >
  Governs the creation of public domain knowledge files and maps the logical web of topics between them.
  Triggers on: "discover domain knowledge in [path]", "document [concept]", "map intersections between [A] and [B]".
---

# Domain Knowledge Skill (Router)

**Purpose:** Provides the rules and triggers for maintaining a public-domain knowledge base. All detailed procedures are lazy-loaded from separate rule and workflow files.

## Dependencies

- **agent-concept-tutor** -- Primary writing and review agent.
- **agent-codebase-archaeologist** -- Targeted codebase scanning and pattern detection.
- **learning-strategy** -- Generation of pedagogical plans and pacing models.

## Routing Index

| Trigger | Action |
|---|---|
| \"discover domain knowledge in [path]\" | **MANDATORY:** Load WORKFLOWS.md -> Codebase Discovery Workflow |
| \"document [concept]\" | **MANDATORY:** Load WORKFLOWS.md -> Reactive Documentation Workflow |
| \"map intersections between [A] and [B]\" | **MANDATORY:** Load WORKFLOWS.md -> Cross-Domain Mapping Workflow |
| \"discover intersections in [path]\" | **MANDATORY:** Load WORKFLOWS.md -> Cross-Domain Mapping Workflow |

## Do NOT trigger for:
- Project-specific implementation details. Use `documentation-specialist` instead.
- General teaching of a concept without the goal of creating a permanent knowledge file. Use `agent-concept-tutor` directly.

## Core Mandates

1. **Lazy Loading:** For rules, read RULES.md. For step-by-step procedures, read WORKFLOWS.md. For output formats, read TEMPLATES.md.
2. **Decision Rule:** Apply 3-Question Rule in RULES.md to assign to `knowledge/` vs `documentation/`.
3. **Reference Rule:** All technical implementation details and Java paths must live in _metadata.md or _formulas.md, never in the pure concept files.

## File Locations

- **Rules:** `C:/Users/dpagkaliwangan/.gemini/skills/domain-knowledge/RULES.md`
- **Templates:** `C:/Users/dpagkaliwangan/.gemini/skills/domain-knowledge/TEMPLATES.md`
- **Workflows:** `C:/Users/dpagkaliwangan/.gemini/skills/domain-knowledge/WORKFLOWS.md`

## Lifecycle & Sync

- **Validation:** Snapshot-date > 12 months = status: stale.
- **Sync:** Decision backlog managed in knowledge/_PENDING_SYNC.md. Sync to notebook is user-triggered.

---

## Decision Values for _PENDING_SYNC.md

pending | promote (Option A) | stub (Option B) | keep (Option C)
