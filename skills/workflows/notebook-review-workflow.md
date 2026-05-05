---
name: notebook-review
description: 'Quality review workflow for notebook entries focusing on pedagogical quality and organization. Triggers: "QA my notes", "check notes quality".'
---
# Notebook Review Workflow

**Triggers:** "QA my notes", "check notes quality"

**IMPORTANT:** Do NOT trigger on "review my notes" -- that is note-taker's review mode, not this workflow.

## Flow

1. quality-guardian reviews notebook content
2. If APPROVED -> exit
3. If CONTENT_ISSUE -> concept-tutor fixes (max 2 iterations)
4. If ORGANIZATION_ISSUE -> note-taker fixes (max 2 iterations)
