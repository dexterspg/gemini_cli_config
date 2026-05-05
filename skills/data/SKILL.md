---
name: data-documentation-templates
description: 'Standard templates for Data Profiling Reports and Cleaning Plans.'
---

# Data Documentation Templates

Templates for agent-data-doc-specialist output documents. Read the template for the mode you are running.

**Section applicability:** Omit sections that are not applicable (e.g., "Plugin/Tool Overlap" for plain CSV). Do not leave empty sections — remove them.

---

## --profile: DATA_PROFILING_REPORT.md

**Save to:** `{project-root}/01-profiling/DATA_PROFILING_REPORT.md` (or `_v2.md`, `_v3.md` on feedback loops)

```markdown
# Data Profiling Report: [Dataset Name]

> **Source:** [System name, export method]
> **Date profiled:** [Date]
> **Profiled by:** [Agent/person]
> **Version:** v1 (increment on feedback loop updates)

## 1. Source Overview
What was exported, from where, date range, format.

| Metric | Value |
|---|---|
| Total records | X |
| Total columns | X |
| File size | X |
| Date range | X – X |

## 2. Structure Observations
Patterns, groups, naming.

### 2A. Column Expansion
[List-type fields that exploded into many columns]

### 2B. Empty Columns
[Columns with 0% fill]

### 2C. Constant-Value Columns
[Same value on every row]

## 3. Duplication Observations
### 3A. Same Data in Multiple Columns
### 3B. System Field Copies
### 3C. Plugin/Tool Overlap

## 4. Data Quality Observations
### 4A. Format Issues (Dates, numbers, text)
### 4B. Encoding Issues
### 4C. Corrupted Values (Error codes, unreadable data)
### 4D. Anomalies (Unexpected/impossible values)

## 5. Fill Rate Analysis
[Measured percentages per column/group]

## 6. Fields From Other Systems

## 7. Assessment Summary
| Category | Count | Impact |
|---|---|---|
| Usable columns | X | Core dataset |
| Empty columns | X | No data loss |
| Duplicate columns | X | Redundant |
| Corrupt/unusable | X | Non-meaningful |
| Other teams' fields | X | Irrelevant |
| Multi-value expanded | X | Collapsible |
```

---

## --plan: DATA_CLEANING_PLAN.md

**Save to:** `{project-root}/02-cleaning/DATA_CLEANING_PLAN.md` (or `_v2.md`, `_v3.md` on feedback loops)

```markdown
# Data Cleaning Plan: [Dataset Name]

> **Based on:** Data Profiling Report ([date], version)
> **Target output:** [Describe the clean dataset]
> **Prepared by:** [Agent/person]
> **Date:** [Date]
> **Version:** v1 (increment on feedback loop updates)

## 1. Cleaning Actions Overview

| Action | Description | Columns Affected |
|---|---|---|
| DROP | Remove entirely | X columns |
| COLLAPSE | Merge many → one | X columns → Y |
| DEDUPLICATE | Keep one of N copies | X columns |
| FIX | Correct format/encoding | X columns |
| RENAME | Standardize names | X columns |

## 2. Step-by-Step Cleaning Sequence

### Step 1: [Action] — [What and Why]
**Columns affected:** [list raw names]
**Rule:** [Specific transformation]
**Validation:** [How to verify]

## 3. Target Schema

### Tier 1 — [Group Name]
| Raw Column Name | Clean Column Name | Type | Transformation | Validation |
|---|---|---|---|---|
| `Original Name` | Clean_Name | type | Rule | Check |

## 4. Collapsing Rules
### [Field Group]
**Raw columns:** `FieldName` (indices X–Y)
**Output column:** `Clean_Name`
**Rule:** [Exactly how to collapse]
**Edge cases:** [Nulls, special values]

## 5. Deduplication Decisions
| Duplicate Set | Keep | Drop | Justification |
|---|---|---|---|
| `Col_A` vs `Col_B` | `Col_A` | `Col_B` | [Reason] |

## 6. Data Quality Fixes
### Fix 1: [Issue Name]
**Columns:** [Which ones]
**Problem:** [What's wrong]
**Rule:** [How to fix]

## 7. Validation Checklist
| Check | Expected Result | Method |
|---|---|---|
| Row count preserved | N before = N after | Count comparison |

## 8. Column Reduction Summary
| Step | Removed | Running Total |
|---|---|---|
| Starting | — | X |
| [Final] | — | **Y** |
```
