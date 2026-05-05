---
name: prd-to-tasks
description: 'Decomposes PRDs and Technical Specs into implementation-ready task lists (slices).'
---
# PRD to Tasks Skill

## Flow
1. **Input:** Read `docs/product-requirements.md` and `docs/technical-specification.md`.
2. **Analysis:** Identify functional dependencies, infrastructure prerequisites, and core logic components.
3. **Slicing:** Divide work into logical milestones ("Slices"). 
   - Slice 1 must be the foundational "walking skeleton".
   - Successive slices add distinct features or complexity.
4. **Tasking:** Decompose each slice into specific, checkbox-ready tasks (file creations, modifications, tests).
5. **Output:** Save to `docs/task-plan.md`.

## Output Template

# Implementation Plan: [Feature Name]

## Overview
Briefly state the goal and the "Walking Skeleton" definition.

## Slices

### Slice 1: Foundation (Walking Skeleton)
- [ ] Task 1
- [ ] Task 2
- [ ] Validation: [How to prove slice 1 works]

### Slice 2: [Feature Area]
- [ ] ...

## Validation
Final end-to-end check.
