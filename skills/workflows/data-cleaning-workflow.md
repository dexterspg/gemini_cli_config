---
name: data-cleaning
description: 'End-to-end flow from raw data scan to Python cleaning script. Triggers: "clean this data", "how to fix this CSV".'
---
# Data Cleaning Workflow


## Flow

1. agent-data-analysis-expert → initial raw analysis of the data source
2. agent-data-doc-specialist --profile → Data Profiling Report (what's in the data, what's wrong)
3. agent-data-doc-specialist --plan → Data Cleaning Plan (how to fix it, target schema)
4. agent-implementation-engineer → cleaning script (Python/pandas)

Steps are sequential — each reads the previous step's output. No quality review gate.
For reviewed output, use `data-cleaning-reviewed-workflow` instead.
