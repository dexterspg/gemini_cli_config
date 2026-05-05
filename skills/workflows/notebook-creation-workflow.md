---
name: notebook-creation
description: Orchestrated workflow for teaching, capturing, and reviewing polished notebook entries. Triggers: "teach me and save it", "create polished entry".
---
# Notebook Creation Workflow

**Triggers:** "teach me X, save it, AND review it", "create polished notebook entry"

## Flow

1. concept-tutor teaches the topic
2. note-taker captures to notebook
3. quality-guardian reviews
4. If issues found, route per notebook-review-workflow (CONTENT_ISSUE -> concept-tutor max 2, ORGANIZATION_ISSUE -> note-taker max 2)
