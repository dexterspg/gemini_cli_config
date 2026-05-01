---
name: migration
description: Use when migrating client data from a third-party system to our platform, or for any software-to-software data migration project. Invoke before starting any migration work — this skill provides the complete workflow (planning → discovery → field mapping → pilot → reconciliation), document templates for all phases, client gate management, PII classification rules, and rollback strategy guidance. Also triggers for: setting up a migration project folder, writing FIELD_MAPPING.md, planning a pilot run, handling a client gate, writing migrate.py or validate.py, or running reconciliation. When in doubt about any migration task, use this skill.
---

# Migration Skill

## Purpose

Guide agents through software-to-software migration when a client is moving from a third-party system to our proprietary platform. Designed for a developer working solo without solution engineers or product support.

## Core Principle

> You are not learning the old software. You are learning the client's data and business rules — the old software is just where that data happens to live right now.

---

## Project Folder Structure

```
{project-root}/migration/
├── 00-planning/                   ← Migration plan (created before any data is touched)
│   ├── MIGRATION_PLAN.md          ← Migration type, rollback strategy, PII classification, timeline
│   └── DATA_CLASSIFICATION.md     ← Sensitive fields inventory and masking rules
│
├── 00-source/                     ← Raw exports from old system (NEVER modified)
│   ├── sample-export.csv
│   └── _README.md                 ← Source system name, export date, who exported
│
├── 01-discovery/                  ← Discovery artifacts
│   ├── DISCOVERY_QUESTIONS.md     ← Questions sent to client
│   ├── CLIENT_RESPONSES.md        ← Client answers (verbatim)
│   └── SOURCE_ANALYSIS.md         ← agent-data-analysis-expert output
│
├── 02-mapping/                    ← Field mapping
│   ├── FIELD_MAPPING.md           ← Old fields → new fields (single source of truth)
│   └── BUSINESS_RULES.md          ← Rules confirmed by client
│
├── 03-transform/                  ← ETL scripts
│   ├── migrate.py
│   ├── validate.py
│   ├── transform_log.csv          ← Record-level audit log (source_id, target_id, status, reason)
│   └── requirements.txt
│
├── 04-pilot/                      ← Pilot run (20 representative records)
│   ├── pilot-input.csv
│   ├── pilot-output.csv
│   └── PILOT_REVIEW.md            ← Client sign-off on pilot
│
├── 05-reconciliation/             ← Full migration validation
│   ├── RECONCILIATION_REPORT.md   ← Old system vs new system comparison
│   └── SIGN_OFF.md                ← Client final approval
│
└── README.md                      ← Migration status + decisions log
```

---

## Phase 0: Migration Planning

This phase happens before any data is touched. Decisions made here prevent irreversible mistakes later.

### Decision 1: Migration type

| Type | Description | Additional steps needed |
|---|---|---|
| **One-time batch** | Full cutover — old system goes dark, all data migrated at once | Standard flow |
| **Incremental / delta** | Client runs both systems in parallel — new data enters old system during migration window | Add delta extraction step before full migration; reconciliation must account for data added after pilot |
| **Phased** | Migrate subsets of records over multiple runs (e.g., by region or business unit) | Each phase is a separate pilot + reconciliation cycle |

Confirm migration type with the client before proceeding.

### Decision 2: Rollback strategy

Every migration needs answers to these three questions before go-live:

| Question | Decision to document |
|---|---|
| Can we undo this? | Yes / No — if yes, how long is the rollback window and what is the procedure? |
| How long does the old system stay available after go-live? | Minimum recommended: 30 days in read-only mode |
| What is the post-go-live support window? | Who handles issues found in the first 2 weeks after cutover? |

### Decision 3: Data classification (PII and sensitive fields)

Before requesting exports or sharing any artifact with the client:

1. Identify fields that contain PII or sensitive data (names, IDs, financial amounts, contact info)
2. Define masking rules for **client-facing artifacts** (FIELD_MAPPING examples, PILOT_REVIEW records)
3. Define data retention policy for `00-source/` exports (e.g., deleted 30 days after go-live sign-off)

### Decision 4: Escalation path

Document before discovery begins — not after the client goes silent:

| Gate | Response SLA | Escalation contact | Stale threshold |
|---|---|---|---|
| Discovery responses | 5 business days | [client project sponsor] | 2 weeks → pause migration |
| Field mapping confirmation | 5 business days | [client project sponsor] | 2 weeks → pause migration |
| Pilot sign-off | 3 business days | [client project sponsor] | 1 week → escalate |
| Final reconciliation sign-off | 3 business days | [client project sponsor] | 1 week → escalate |

### MIGRATION_PLAN.md template

```markdown
# Migration Plan: [Old System] → [New System]

> **Client:** [Name]
> **Date:** [Date]
> **Version:** v1

## Migration Type
[ ] One-time batch  [ ] Incremental/delta  [ ] Phased

**If incremental:** Describe delta extraction approach and parallel-run window: [details]

## Rollback Strategy

| Question | Answer |
|---|---|
| Can we roll back after go-live? | Yes / No |
| Rollback window | [e.g., 48 hours post-go-live] |
| Rollback procedure | [steps to revert — who does what] |
| Old system availability | [e.g., read-only for 30 days after go-live] |
| Post-go-live support window | [e.g., 2 weeks dedicated support] |

## Data Classification

| Field | Sensitivity | Masking Rule for Client Artifacts |
|---|---|---|
| `CustomerName` | PII | Truncate to first name only in examples |
| `ContractValue` | Confidential | Show as `[REDACTED]` in pilot samples |

**Source data retention:** Delete `00-source/` exports [N] days after go-live sign-off.

## Escalation Contacts

| Role | Name | Contact |
|---|---|---|
| Client project sponsor | [name] | [email] |
| Internal migration owner | [name] | [email] |
```

---

## Phase 1: Discovery

### What to request from the client

- Full data export (CSV, Excel, database dump) — a sample of 50–100 real records is enough to start
- Most-used reports from the old system — reports reveal what data actually matters
- Contact for the **power user** — the person who uses the system daily, not the IT contact

### Discovery questions to ask the client power user

**About their data:**
- What fields do you actively use vs. ignore?
- Are there records that follow different rules? (legacy, grandfathered, special cases)
- Was any data manually patched directly in the database outside the normal workflow?
- Are there soft-deleted or archived records that should be included in the migration?

**About their business rules:**
- Walk me through one record end-to-end in the old system
- If I gave you this record after migration, how would you know if it's correct?
- What are the most important fields — the ones that would cause a problem if wrong?
- Are there lookup/reference values (status codes, categories, types) we need to map?

**About validation:**
- What reports do you run regularly? (these become reconciliation targets)
- What does "correct" look like for key totals and counts?

### DISCOVERY_QUESTIONS.md template

```markdown
# Discovery Questions: [Migration Name]

> **Sent to:** [Client contact name, role]
> **Date sent:** [Date]
> **Responses in:** CLIENT_RESPONSES.md

## Data Questions
1. What fields in [old system] do you actively use day-to-day?
2. Are there any records that follow special or legacy rules?
3. Was any data ever manually corrected outside the normal system workflow?
4. Should archived or deleted records be included in the migration?

## Business Rule Questions
5. Can you walk me through one record end-to-end in [old system]?
6. After migration, how would you verify a record is correct?
7. What are the most critical fields — ones that must be right?
8. What status codes or category values does [old system] use?

## Validation Questions
9. What reports do you run regularly in [old system]?
10. What totals or counts should match exactly after migration?
```

---

## Phase 2: Field Mapping

### FIELD_MAPPING.md template

```markdown
# Field Mapping: [Old System] → [New System]

> **Source system:** [Name]
> **Target system:** [Name]
> **Prepared by:** [Agent/person]
> **Client confirmed:** [Date or Pending]
> **Version:** v1

## Status Legend

| Status | Meaning |
|---|---|
| ✅ Confirmed | Client verified this mapping is correct |
| ⏳ Pending | Awaiting client clarification |
| ⚠️ Gap | Old system has data with no equivalent in new system |
| 🚫 Drop | Field not needed in new system — client confirmed |

## Core Mappings

| Old Field | Old Type | New Field | New Type | Transformation Rule | Status |
|---|---|---|---|---|---|
| `OldFieldName` | string | newFieldName | string | Direct copy | ✅ Confirmed |
| `StartDt` | text MM/DD/YYYY | commencementDate | date ISO 8601 | Parse + reformat | ✅ Confirmed |
| `MonthlyAmt` | text | paymentAmount | decimal | Strip currency symbol, cast to decimal | ⏳ Pending |

## Reference / Lookup Value Mappings

| Old Value | New Value | Notes |
|---|---|---|
| `ACTIVE` | `active` | Direct match |
| `CLOSED` | `terminated` | Semantic rename |
| `HOLD` | ⏳ | No equivalent — awaiting client clarification |

## Gaps — Fields With No Mapping

| Old Field | Example Value | Issue | Resolution |
|---|---|---|---|
| `LegacyCode` | `ABC-123` | No equivalent in new system | 🚫 Drop — client confirmed not needed |
| `InternalRef` | `REF-001` | Purpose unclear | ⏳ Pending client clarification |

## Open Questions

| # | Question | Sent | Response |
|---|---|---|---|
| 1 | What does status `HOLD` mean in your workflow? | [date] | [pending] |
```

### Entity Model Mapping (cardinality changes)

Before field mapping, check whether the source and target entity models are 1:1. Many migrations involve structural differences: 

| Pattern | Description | Handling |
|---|---|---|
| **1:1** | One source record → one target record | Standard field mapping applies |
| **1:N split** | One source record → multiple target records | Define the split rule — what determines how many records are created and what each gets |
| **N:1 merge** | Multiple source records → one target record | Define the merge rule — which field wins, how conflicts are resolved |
| **Structural reshape** | Source table structure differs fundamentally from target | Map at entity level first, then field level within each entity |

Document any non-1:1 patterns in `BUSINESS_RULES.md` before writing field mappings.

### Rules for field mapping

- Use exact column names from the source file (in backticks) — readers must be able to Ctrl+F in the CSV
- Never invent or abbreviate column names
- Status column must be updated after every client response — never leave stale ⏳ entries
- FIELD_MAPPING.md is the single source of truth — never split mapping decisions across multiple files
- Apply PII masking rules from `00-planning/DATA_CLASSIFICATION.md` to all example values in this document

### BUSINESS_RULES.md template

```markdown
# Business Rules: [Migration Name]

> **Source system:** [Name]
> **Confirmed by:** [Client contact name, role]
> **Date confirmed:** [Date]
> **Version:** v1

## Confirmed Rules

| Rule ID | Description | Example | Confirmed By | Date |
|---|---|---|---|---|
| BR-001 | Lease term always starts on the 1st of the month | Start date of 15 Mar → rounded to 1 Mar | [name] | [date] |      
| BR-002 | Status `HOLD` means suspended — maps to `suspended` in new system | — | [name] | [date] |

## Reference / Lookup Value Mappings (Confirmed)

| Field | Old Value | New Value | Notes |
|---|---|---|---|
| `Status` | `ACTIVE` | `active` | Direct match |
| `Status` | `CLOSED` | `terminated` | Semantic rename confirmed |

## Open / Unconfirmed Rules

| Rule ID | Question | Sent to Client | Response |
|---|---|---|---|
| BR-003 | What does status `HOLD` mean — paused, cancelled, or pending approval? | [date] | [pending] |

## Edge Cases and Exceptions

| Case | Description | Handling Rule |
|---|---|---|
| Grandfathered records | Contracts created before [date] follow old calculation method | Flag with `legacy_flag = true` — client to review manually |
| Manually patched records | [N] records were directly edited in the database | Client to provide list — migrate as-is, flag for audit |
```

---

## Phase 3: Pilot Migration

Two tiers — both are required:

**Tier 1 — Client review pilot (20 records)**
- Select 20 **representative** records — not random. Cover different statuses, types, date ranges, edge cases, and any records the client flagged as "complex"
- Apply PII masking rules from `00-planning/DATA_CLASSIFICATION.md` before sharing with client
- Generate a side-by-side comparison: old system values vs. new system values
- Send to the client power user: *"Does this look right to you?"*
- Outcome can be APPROVED, PARTIAL, or REJECTED (see template below)

**Tier 2 — Stress pilot (500–1000 records)**
- After Tier 1 is APPROVED or PARTIAL-resolved, run a larger batch to catch scale-dependent bugs
- Do not share with client — this is an internal technical check
- Look for: encoding failures at scale, memory issues, transform performance, duplicate creation, edge cases not present in the 20-record sample
- Fix any failures before proceeding to full migration

### PILOT_REVIEW.md template

```markdown
# Pilot Review: [Migration Name]

> **Pilot date:** [Date]
> **Record count:** 20
> **Reviewed by:** [Client contact name, role]
> **Outcome:** APPROVED / PARTIAL / REJECTED

## Records Reviewed

| Record ID | Key Fields Checked | Result | Notes |
|---|---|---|---|
| [ID] | Status, Amount, Date | PASS / FAIL | [any discrepancy] |

## Issues Found

| Record ID | Field | Expected | Actual | Root Cause |
|---|---|---|---|---|

## Client Decision

- [ ] APPROVED — all records correct, proceed to full migration
- [ ] PARTIAL — specific record types approved, others need rework (detail below)
- [ ] REJECTED — systematic issues, return to field mapping

**If PARTIAL — approved record types:**
[List which statuses/types/categories passed]

**If PARTIAL — rejected record types and next step:**
[List what failed and whether to fix mapping or re-pilot just the failed subset]

**Signed off by:** [name]
**Date:** [date]
```

---

## Phase 4: Reconciliation

### Control totals (must match exactly)

- Total record count: old system vs. new system
- Sum of key financial or quantitative fields
- Count by status and category

### Spot checks

- 5–10 records selected by the client — verify field by field
- Any records the client flagged as "complex", "special", or "exceptions"

### RECONCILIATION_REPORT.md template

```markdown
# Reconciliation Report: [Migration Name]

> **Migration date:** [Date]
> **Prepared by:** [Agent/person]

## Control Totals

| Metric | Old System | New System | Match? |
|---|---|---|---|
| Total records | X | X | PASS / FAIL |
| Total [key amount] | X | X | PASS / FAIL |
| Count by status — Active | X | X | PASS / FAIL |
| Count by status — Closed | X | X | PASS / FAIL |
| Count by [other category] | X | X | PASS / FAIL |

## Referential Integrity Checks

| Check | Expected | Result | Notes |
|---|---|---|---|
| No orphaned child records (child with no parent) | 0 orphans | PASS / FAIL | |
| No broken foreign key references | 0 broken refs | PASS / FAIL | |
| All parent-child links intact | X relationships | PASS / FAIL | |
| No duplicate primary keys in target | 0 duplicates | PASS / FAIL | |
| All lookup/reference values valid in target | 0 invalid refs | PASS / FAIL | |

## Transform Audit Summary

| Status | Count |
|---|---|
| Successfully migrated | X |
| Skipped (with reason) | X |
| Failed (logged in transform_log.csv) | X |

## Discrepancies

| Record ID | Field | Old Value | New Value | Root Cause | Resolution |
|---|---|---|---|---|---|

## Spot Check Results

| Record ID | Checked by | Result | Notes |
|---|---|---|---|

## Sign-Off

- [ ] Control totals match
- [ ] All referential integrity checks pass
- [ ] Transform audit shows 0 unexpected failures
- [ ] Client confirms spot check records are correct
- [ ] Rollback plan confirmed still executable (if within rollback window)
- [ ] Go-live approved by: [name, date]
```

---

## README.md Template (Migration Root)

```markdown
# Migration: [Old System] → [New System]

> **Client:** [Client name]
> **Started:** [Date]
> **Current phase:** [Discovery / Mapping / Transform / Pilot / Reconciliation / Complete]

## Phase Status

| Phase | Status | Completed |
|---|---|---|
| 01 Discovery | DONE / IN PROGRESS / PENDING | [date or —] |
| 02 Mapping | DONE / IN PROGRESS / PENDING | [date or —] |
| 03 Transform | DONE / IN PROGRESS / PENDING | [date or —] |
| 04 Pilot | DONE / IN PROGRESS / PENDING | [date or —] |
| 05 Reconciliation | DONE / IN PROGRESS / PENDING | [date or —] |

## Decisions Log

| Date | Decision | Confirmed By |
|---|---|---|
| [date] | Status `HOLD` maps to `suspended` | [client name] |
| [date] | Archived records excluded from migration | [client name] |

## Key Contacts

| Role | Name | Contact |
|---|---|---|
| Client power user | [name] | [email] |
| Client IT contact | [name] | [email] |
```

---

## Feedback Loops

Migration is not purely linear. Three failure loops can occur:

```
01-discovery → 02-mapping → 03-transform → 04-pilot → 05-reconciliation
                   ↑               ↑              |              |
                   |               └── Loop 2 ────┘              |
                   └──────────────── Loop 3 ─────────────────────┘
```

| Loop | Trigger | What to do | Versioning |
|---|---|---|---|
| **Loop 1: Mapping gap** | Client rejects pilot — systematic field mapping error | Return to Phase 2, correct FIELD_MAPPING.md, re-run pilot | `FIELD_MAPPING_v2.md`, `BUSINESS_RULES_v2.md` |
| **Loop 2: Transform bug** | Reconciliation fails — ETL script produces wrong values despite correct mapping | Fix `migrate.py`, re-run reconciliation | No new version needed — script is code, not a doc artifact |
| **Loop 3: Discovery gap** | Pilot or reconciliation reveals undiscovered business rules | Return to Phase 1, update CLIENT_RESPONSES.md, update mapping | `FIELD_MAPPING_v2.md` |

**Versioning rule:** When a feedback loop forces a document update, append `_v2`, `_v3`, etc. Never overwrite the original — the version trail shows how understanding evolved.

---

## Rules for Agents Using This Skill

1. **Plan before touching data** — Phase 0 (rollback strategy, PII classification, escalation contacts) must be complete before any export is requested or any script is written.
2. **Never guess business rules** — always confirm with the client. One wrong assumption corrupts thousands of records.        
3. **Document every decision** — who confirmed what, on what date. This protects you when something is questioned post-migration.
4. **Expect dirty data** — source systems always have nulls, inconsistent formats, and duplicates. Handle defensively in ETL scripts (log failures, never crash).
5. **ETL scripts must be idempotent** — `migrate.py` must be safe to re-run. Running it twice must not create duplicate records. Use upsert logic or check-before-insert.
6. **ETL scripts must produce a transform log** — every record processed must be logged to `transform_log.csv` with: `source_id`, `target_id`, `status` (success/skipped/failed), `failure_reason`.
7. **Mask PII in all client-facing artifacts** — apply masking rules from `00-planning/DATA_CLASSIFICATION.md` before sharing FIELD_MAPPING examples, pilot output, or any document sent outside the team.
8. **Pilot first, always** — never run full migration without a Tier 1 client-reviewed pilot AND a Tier 2 stress pilot.        
9. **Keep source data untouched** — `00-source/` is read-only. All transformations happen in scripts, never manually.
10. **Client gates are hard stops** — Steps requiring client confirmation cannot be skipped or assumed. Apply the escalation SLAs from `MIGRATION_PLAN.md` when clients are unresponsive.

---

## Relationship to Existing Agents

| Agent | Phase | Role |
|---|---|---|
| `agent-data-analysis-expert` | 01-discovery | Scans raw export → produces `SOURCE_ANALYSIS.md` (note: migration context uses this name instead of the standard `_initial_analysis.md`) |
| Main session | 02-mapping | Reads `SOURCE_ANALYSIS.md` + `CLIENT_RESPONSES.md` → produces `FIELD_MAPPING.md` + `BUSINESS_RULES.md` using skill templates |
| `agent-implementation-engineer` | 03-transform | Reads `FIELD_MAPPING.md` → writes `migrate.py` + `validate.py` |
| `agent-qa-engineer` | 05-reconciliation | Runs reconciliation → writes `RECONCILIATION_REPORT.md` |
| `agent-quality-guardian` | Any | Reviews any artifact at any phase |
| `agent-persona-reviewer` | Any | Panel review (auto-detects `migration` content type; panel: Migration Engineer, Client Success Manager, Data Steward, Implementation Consultant) |
