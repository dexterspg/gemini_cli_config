---
name: support-investigation
description: 'Support/L2 methodology using logs, screenshots, and Jira data. Triggers: "investigate this", "analyze logs", "triage", "what caused this".'
---

# Support Investigation Skill

> **Distinction:** Diagnoses at application level (logs/data/UI). Does NOT read source code. Use `agent-debugger` for source tracing.

## Hard Boundaries
- **No source code:** Never read `.java`, `.xml`, or files in codebase roots. Use logs/KEDB only.
- **No scripts:** Spec the fix (table/field); never write SQL/scripts directly.
- **Rationale:** Preserves support/dev boundary; ensures durable diagnoses.

## Do NOT Trigger For
- Source code tracing -> `agent-debugger`
- Implementation/Scripting -> `agent-implementation-engineer`
- General codebase questions -> `agent-codebase-archaeologist`

## Phase 0: Pattern Lookup (KEDB)
1. **Signals:** ID error code + component (ignore client-reported labels).
2. **Lookup:** Grep `kedb/INDEX.md`.
3. **Scoring:** `error_code` + `signature_variant` = Strong match.
4. **Mandatory:** Output `kedb_check` block in report.

## Phase 1-3: Evidence & Analysis
- **Intake:** Read Jira + Screenshots first. Verify attachments exist.
- **Logs:** Identify THREAD and work BOTTOM-UP through "Caused by" chain.
- **Five Whys:** Trace surface error to actionable data/config cause.
- **Reference:** `references/examples.md` for methodology examples.

## Phase 4-5: Triage & Confirmation
- **Categorize:** Use the Decision Tree in `references/examples.md`.
- **Confirm:** Hypothesis must be proven by direct log/config evidence.

## Phase 6: Resolution Routing
- **Data Fix:** Spec table/field/value for implementation agent.
- **Escalation:** Package evidence/repro steps for `agent-debugger`.
- **Gate:** WAIT for user confirmation before spawning any agent.

## Output Contract
- **Report:** `support-investigation.md` (TL;DR, KEDB, Root Cause, Evidence, 5 Whys, Fix).
- **Narrative:** `support-walkthrough.md` (Plain-English story of the investigation).
- **Handoff:** Reusable signal patterns for canonical documentation.

## Customer Communication
- **Rules:** Align language with Confirmed/Probable/Suspected status.
- **Reference:** `references/language-rules.md` for hedging rules.

---

## File Locations
- **Core:** `SKILL.md`
- **Examples:** `references/examples.md`
- **Language:** `references/language-rules.md`
