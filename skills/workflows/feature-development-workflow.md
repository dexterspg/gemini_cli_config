---
name: feature-development
description: End-to-end workflow for new feature implementation including requirements, design, architecture, and QA. Triggers: "build [feature]", "implement [X]".
---
# Feature Development Workflow


## Steps
requirements-discovery (Standard/Enterprise only) → product-strategist → ui-design (if UI) → system-architect → prd-to-tasks → implementation-engineer → qa-engineer → quality-guardian    

## Context Loading (Step 0)
product-strategist reads `documentation/platform/domain-concepts/` (Tier 1) + `BUSINESS-CASE.md` + `USE-CASES.md` before writing requirements

## Discovery (Step 0.5)
For Standard/Enterprise, run `requirements-discovery` skill first — pass Discovery Summary to product-strategist as input

## Task Decomposition (Step 3.5)
After architect produces tech spec, run `prd-to-tasks` skill — reads PRD + tech spec + wireframes → writes `docs/task-plan.md` → user confirms before engineer starts

## Knowledge Capture (Step 5)
After implementation, route discoveries via `KNOWLEDGE_CAPTURE.md` — general → Tier 1, use cases → `USE-CASES.md`, implementation → `domain/NN-*.md`

## Routing
APPROVED → done; CODE_ISSUE → engineer (max 2); TEST_ISSUE → qa (max 2); DESIGN_ISSUE → architect (max 1); REQUIREMENTS_ISSUE → strategist (max 1, then escalate); SPEC_DRIFT → architect --sync (max 1)
