---
name: tdd-workflow
description: 'Test-first development flow for high-integrity features or bug fixes. Triggers: "build with TDD", "test-first development".'
---
# TDD Workflow


## Steps
requirements-discovery (Standard/Enterprise only) → product-strategist → ui-design (if UI) → system-architect → prd-to-tasks → implementation-engineer (--tdd, tests first) → qa-engineer (E2E/integration only, optional) → quality-guardian

## Discovery (Step 0.5)
For Standard/Enterprise, run `requirements-discovery` skill first — pass Discovery Summary to product-strategist as input

## Task Decomposition (Step 2.5)
After architect produces tech spec, run `prd-to-tasks` skill → writes `docs/task-plan.md` → user confirms before engineer starts

## Routing
APPROVED → done; CODE_ISSUE/TEST_ISSUE → engineer (max 2); DESIGN_ISSUE → architect (max 1); REQUIREMENTS_ISSUE → strategist (max 1, then escalate); SPEC_DRIFT → architect --sync (max 1)
