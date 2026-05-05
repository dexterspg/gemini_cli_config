# Code Review Workflow

## Tier Rules (determine before starting)

- **Small** — single bug fix, refactor, few-line change → quality-guardian only (skip persona-reviewer)
- **Standard** — new feature, significant logic change → quality-guardian → if APPROVED, ask user: "Run deep panel review?" → if yes, persona-reviewer
- **High-stakes** — architecture decision, public API, pre-release, high-risk area → quality-guardian AND persona-reviewer (both mandatory, run sequentially)

## Steps (Standard / High-stakes)

1. agent-quality-guardian → structured verdict (APPROVED / REVISION_NEEDED / BLOCKED)
2. If REVISION_NEEDED → route to implementation-engineer (max 2 iterations) → back to quality-guardian
3. Once APPROVED (or Small tier exits here) → agent-persona-reviewer → panel discussion with cross-examination
4. Present combined findings to user → DONE

## Routing

CODE_ISSUE → implementation-engineer (max 2); TEST_ISSUE → qa-engineer (max 2); DESIGN_ISSUE → system-architect (max 1); SECURITY_ISSUE → implementation-engineer (max 1, then escalate to user)

## Rules

- quality-guardian always runs before persona-reviewer — never reverse order
- Small tier: quality-guardian only, no persona-reviewer unless user explicitly asks
