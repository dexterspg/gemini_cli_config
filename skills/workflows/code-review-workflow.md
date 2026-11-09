# Code Review Workflow

## Tier Rules (determine before starting)

- **Small** — single bug fix, refactor, few-line change → quality-guardian only (skip adversarial-review)
- **Standard** — new feature, significant logic change → quality-guardian → if APPROVED, ask user: "Run deep panel review?" → if yes, adversarial-review
- **High-stakes** — architecture decision, public API, pre-release, high-risk area → quality-guardian AND adversarial-review (both mandatory, run sequentially)

## Steps (Standard / High-stakes)

1. agent-quality-guardian → structured verdict (APPROVED / REVISION_NEEDED / BLOCKED)
2. If REVISION_NEEDED → route to implementation-engineer (max 2 iterations) → back to quality-guardian
3. Once APPROVED (or Small tier exits here) → adversarial-review skill (main session) → adversarial panel with verified findings
4. Present combined findings to user → DONE

## Routing

CODE_ISSUE → implementation-engineer (max 2); TEST_ISSUE → qa-engineer (max 2); DESIGN_ISSUE → system-architect (max 1); SECURITY_ISSUE → implementation-engineer (max 1, then escalate to user); any other issue type → main session picks the route from the guardian's Issue Type table; BLOCKED → escalate to user. Send "iteration N of max" with every re-review; at the cap an open Critical is BLOCKED.

## Rules

- quality-guardian always runs before adversarial-review — never reverse order
- Small tier: quality-guardian only, no adversarial-review unless user explicitly asks
