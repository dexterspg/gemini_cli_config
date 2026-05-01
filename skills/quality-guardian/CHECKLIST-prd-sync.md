# Checklist: PRD ↔ Technical Spec Sync

Use when BOTH `docs/product-requirements.md` AND `docs/technical-specification.md` exist. Run before approving either document, and whenever one is updated without the other.

## Traceability
- [ ] [critical] Every FR in the PRD addressed (explicitly or implicitly) in the tech spec? *Fail: one or more FRs have no corresponding design element.*
- [ ] Every design decision in the tech spec aligns with PRD constraints and requirements? *Fail: spec introduces a constraint or approach not supported by the PRD.*
- [ ] No design decisions in the spec contradict a PRD constraint or requirement?

## Input / Output Consistency
- [ ] File formats accepted — do both documents agree? *Fail: PRD says `.xlsx`, spec handles `.csv` only.*
- [ ] Input methods (file upload vs. UI form vs. inline table) — do both documents agree?
- [ ] Output columns, names, and calculation formulas — do both documents agree?
- [ ] Output file naming pattern — does the spec implement what the PRD specifies?
- [ ] Error handling categories — does the spec's error structure cover all error types defined in the PRD?

## Scope Alignment
- [ ] Does the tech spec stay within Phase 1 scope as defined in the PRD?
- [ ] Are any Phase 2+ items from the PRD being built in the spec? *Fail: scope creep — items not in current phase are being implemented.*
- [ ] Are any P0 requirements from the PRD missing from the spec?

## TBD Resolution
- [ ] Any items marked "TBD" in the PRD — has the tech spec resolved them? If yes, update the PRD to match.
- [ ] Any items marked "TBD" in the tech spec — are they also TBD in the PRD, or is there a mismatch?

## Terminology
- [ ] Are the same names used for the same concepts in both documents? *Fail: different names for the same entity (e.g., "account mapping" vs "account map").*
- [ ] Are endpoint names / component names in the spec consistent with capability names in the PRD?

**Verdict guidance** (global default applies — see CHECKLISTS.md)
