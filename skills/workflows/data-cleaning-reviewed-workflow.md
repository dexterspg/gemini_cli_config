---
name: data-cleaning-reviewed
description: 'Reviewed flow for data cleaning including quality guardian gates. Triggers: "clean and review this data", "reviewed data cleaning pipeline".'
---
# Data Cleaning Workflow (with Quality Review)

**Tier (decide first):** Small — one file, a few hundred rows, no spec: the main session profiles it and writes the cleaning script itself, no agent chain. Standard — larger or several files: the flow below.

## Flow

1. agent-data-analysis-expert (initial analysis)
2. agent-data-doc-specialist --profile (profiling report)
3. quality-guardian reviews profiling report
4. agent-data-doc-specialist --plan (cleaning plan)
5. quality-guardian reviews cleaning plan
6. agent-implementation-engineer (implement cleaning)
7. agent-qa-engineer (validate clean output)
8. DONE

## Routing

- APPROVED -> next step
- DATA_ISSUE -> data-doc-specialist (max 2)
- PROFILING_ISSUE -> data-doc-specialist --profile (max 2)
- CLEANING_PLAN_ISSUE -> data-doc-specialist --plan (max 2)
- CONTENT_ISSUE -> data-doc-specialist (max 1, then escalate)
- CODE_ISSUE -> implementation-engineer (max 2)
