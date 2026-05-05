---
name: architecture-audit
description: 'Codebase exploration and redesign workflow for addressing structural friction. Triggers: "this code is getting messy", "audit the architecture".'
---
# Architecture Audit Workflow


## Steps
Main session reads architecture-audit skill → explores codebase for friction → presents candidates → user picks → proposes redesign → writes `docs/architecture-audit.md` → quality-guardian reviews → if APPROVED, hand off to prd-to-tasks (treat migration steps as slices) → implementation-engineer

## Rules
- Never trigger during new feature development — use feature-development-workflow instead
- Scope guard: one candidate per session; surface others in "Further Observations" only
- Output is `docs/architecture-audit.md` — never a GitHub issue or Jira ticket
- Parallel competing designs are optional for complex cases; start with single proposal
