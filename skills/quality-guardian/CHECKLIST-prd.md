# Checklist: Product Requirements (PRD)

## Sizing
- [ ] Does the doc declare a project size (Mini / Standard / Enterprise)?
- [ ] Are NFRs proportional to project size? *Fail: Mini projects have scalability, HA, or enterprise security NFRs — out of scope for single-user internal tools.*
- [ ] Are user story count and FR count proportional? *Fail: Mini should be 3-5 stories, 8-12 FRs — more than this signals scope creep.*
- [ ] Are edge cases realistic for the scope? *Fail: concurrency or adversarial edge cases listed for a single-user internal tool.*
- [ ] Are success metrics actionable by the build team? *Fail: adoption or business metrics included that the engineering team cannot measure or control.*

## Clarity
- [ ] Is the PRIMARY deliverable stated clearly in the problem statement? *Fail: problem statement describes context but not the single output the user needs.*
- [ ] Are user stories ordered by value? *Fail: the core deliverable is not US-01 — it is buried in a later phase.*
- [ ] Is standalone vs. feature-addition explicitly stated?
- [ ] Are TBD items clearly marked with which phase they belong to?

## Consistency
- [ ] Do acceptance criteria match the current user stories? *Fail: references to removed or renamed stories.*
- [ ] Do phase scope sections match the user stories assigned to each phase?
- [ ] Are there contradictions between NFRs and constraints? *Fail: e.g., "recoverable" combined with "in-memory only".*
- [ ] Is terminology consistent throughout? *Fail: mixing synonyms for the same concept (e.g., "mode" and "standalone app").*    

## Completeness
- [ ] Problem statement explains WHY, not just WHAT?
- [ ] Each P0 story has at least one acceptance criterion?
- [ ] Out of scope is explicitly defined?
- [ ] If following an existing pattern, is the sister project referenced?

**Verdict guidance** (global default applies — see CHECKLISTS.md)
