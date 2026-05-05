# Guided Walkthrough Workflow


## Prerequisites
PRD + tech spec must exist. `docs/task-plan.md` must exist (run prd-to-tasks first if not).

## Steps
Main session reads `~/.gemini/skills/guided-implementation-walkthrough/SKILL.md` → per slice from task-plan.md: concept-tutor (teach) → user confirms → implementation-engineer (build) → update task-plan.md progress

## Rules
- Decomposition comes from prd-to-tasks, not this workflow — vertical slices, not horizontal layers
- Each slice's Goal from task-plan.md becomes the teaching objective
- Pass slice acceptance criteria + teaching summary to the implementation-engineer
- If code already exists for a slice, Step B becomes code review instead of build
- User can skip teach ("just build it") or skip build ("just teach, I'll write it myself") per slice
- Wireframes/mockups are first-class references — teach UI slices against the mockup
- Main session owns task-plan.md updates; subagents never write to task-plan.md directly
