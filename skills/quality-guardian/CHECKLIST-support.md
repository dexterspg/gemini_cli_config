# Checklist: Support Investigation (`support-investigation.md`, `support-walkthrough.md`)

**Before reviewing:** Read the support investigation skill(s) for the project to understand what a complete investigation looks like.

## Structure
- [ ] `kedb_check` block present — with `matched`, `confidence`, `signals_matched`, `candidates_reviewed`, and `action` fields?
- [ ] TL;DR present — root cause in 2 sentences, fix in 1?
- [ ] Five Whys chain present — surface error traced to actionable root cause?
- [ ] Fix Options section present and ordered (data/config first, escalation last)?
- [ ] Ruled Out section present — alternative hypotheses explicitly dismissed?

## Evidence Quality (most important)
- [ ] [critical] Root cause confirmed from attachment (log file, RFC trace) — NOT carried from the Jira description alone? *Fail: root cause stated as fact but only evidence is the client's description.*
- [ ] If description error code differs from attachment error code — is the discrepancy explicitly documented?
- [ ] Each claim in the root cause section traceable to a specific log line, BAPI return code, or config value?
- [ ] No hypothesis stated as confirmed without supporting evidence?

## Hypothesis Coverage
- [ ] At least one alternative hypothesis considered and ruled out?
- [ ] Ruling-out explanations reference evidence (not just "unlikely")?

## Escalation Routing
- [ ] Fix type correctly identified (data/config fix vs. code bug vs. user education vs. infrastructure)?
- [ ] If routed to L3: escalation package includes entity IDs, exact error codes from attachment, reproduction steps, and what data/config fixes were ruled out?
- [ ] If routed to implementation agent: table/field/current value/required value specified — no code, just the specification? 
- [ ] No agent spawned without a documented routing proposal?

## Customer Communication (if a response draft is included)
- [ ] Response accurately reflects the confirmed root cause — not the client-reported one if they differ?
- [ ] Responsibility not pushed to customer's team without evidence from the attachment confirming it?
- [ ] Tone appropriate to urgency (month-end, go-live pressure flagged if present)?

**Verdict guidance** (global default applies — see CHECKLISTS.md)
