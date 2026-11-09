---
name: adversarial-review-concerns
description: Concern catalog for the adversarial-review skill. Look up the 4 selected concern groups before briefing attack threads.
---

# Concern Catalog

Each heading is a concern group, not an identity. Put its Primary concerns and Challenge style questions in an attack brief, adapted to the actual content; never the heading as a role.

---

#### Test Strategist
- **Primary concerns:** Test pyramid balance (unit vs integration vs E2E), what's actually worth testing, coverage of critical paths, whether tests prove the right things
- **Challenge style:** Asks "are we testing the right things or just the easy things?", "what's the coverage of critical paths?", "would these tests catch the bugs that matter?"

#### Developer Under Test
- **Primary concerns:** "Can I run these tests locally?", "Do they break when I make innocent changes?", "Are they fast enough that I'll actually run them?", "Do they tell me *what* broke and *why*?"
- **Challenge style:** Asks "how long does this suite take?", "what does the failure message look like?", "will this break every time I rename a method?", "do I need a running database to run unit tests?"

#### Business Stakeholder
- **Primary concerns:** Business value, ROI clarity, time-to-value, risk to operations, compliance implications
- **Challenge style:** Asks "what does this cost us?", "what breaks if this fails?", "would a new manager understand this?"

#### Junior Developer
- **Primary concerns:** "Can I run this?", "Where do I start?", "What does X actually do?", "What happens if I do it wrong?"
- **Challenge style:** Asks naive but sharp questions that expose gaps experts take for granted. "Why does it have to be this way?"

#### Senior Developer
- **Primary concerns:** Code quality, maintainability, test coverage, security, edge cases, performance
- **Challenge style:** Points out what will break in production, questions assumptions about scale, flags missing tests

#### Tech Lead / Architect
- **Primary concerns:** System design, scalability, integration points, dependencies, operational complexity, long-term maintainability
- **Challenge style:** Asks about failure modes, operational burden, who owns what, what happens at 10x scale

#### QA Engineer
- **Primary concerns:** Edge cases, error handling, test coverage, regression risk, user-facing failure modes
- **Challenge style:** Lists scenarios not covered, asks "what happens when X is null/empty/missing?", challenges happy-path assumptions

#### Finance Director
- **Primary concerns:** Cost accuracy, financial risk, budget alignment, ROI, compliance with financial standards
- **Challenge style:** Challenges every unsubstantiated number, asks about assumptions behind projections

#### Operations Manager
- **Primary concerns:** Process efficiency, team capacity, handoffs, operational risk, SLAs
- **Challenge style:** Asks about edge cases in process, who handles exceptions, what happens during outages

#### Executive Sponsor
- **Primary concerns:** Strategic fit, organizational risk, stakeholder alignment, headline metrics
- **Challenge style:** Asks "does this move the needle?", "what's our story to leadership?", "what are the risks we must disclose?"

#### Project Manager
- **Primary concerns:** Timeline, dependencies, risks, resource allocation, clear ownership
- **Challenge style:** Asks about who owns what, what blocks what, how long things actually take

#### End User
- **Primary concerns:** "Can I actually use this?", "What do I do first?", "What happens when I make a mistake?"
- **Challenge style:** Asks "where's the example?", "what does this mean in practice?", "what do I do when it doesn't work?"

#### Prompt Engineer
- **Primary concerns:** Instruction clarity, ambiguity in prompts, edge case handling in AI behavior, token efficiency
- **Challenge style:** Finds ambiguous instructions, missing examples, contradictory rules, undefined edge cases

#### AI Systems Designer
- **Primary concerns:** Agent reliability, tool use correctness, workflow correctness, integration points between agents
- **Challenge style:** Asks "what happens when the subagent fails?", "what if the tool returns empty?", "how does routing work at the edges?"

#### Workflow Owner
- **Primary concerns:** Stage order and entry/exit criteria, who is accountable end to end and per step, human approval gates placed by risk (irreversible or costly steps first), handoffs between people and agents with validated inputs and outputs, loops with capped retries and an escalation path, rollback and failure paths, end-to-end reliability across the chain, what "done" means and how it is observed (logs, metrics)
- **Challenge style:** Asks "who triggers this step and who owns its failure?", "what stops this looping forever?", "where does a human say yes or no?", "how do we know it finished and finished correctly?", "if each step is 90% reliable, what is the whole chain?"

#### UX / Interaction Designer
- **Primary concerns:** Information hierarchy, cognitive load, progressive disclosure, visual clarity, whether the interaction model helps or hinders understanding
- **Challenge style:** Asks "what does the user see first?", "how many decisions before they get value?", "is the default the right default?", "what happens when they're overwhelmed?", "does the layout guide the eye or scatter it?"

#### Design Systems Engineer
- **Primary concerns:** Every token, component and label traces to source at file:line; token naming and coverage (colour, type, spacing, radius, shadow, size, z-index, dark mode); component anatomy, variants and states; one source of truth with no hand-typed values; the record states what ships, not what should change, with suggestions kept apart and not stale; whether doc, artifact and source can drift and what gate catches it
- **Challenge style:** Asks "where in the source does this value come from?", "what fails if someone changes the CSS tomorrow?", "is this measured or typed?", "which of these two outputs wins when they disagree?"

#### Accessibility Specialist
- **Primary concerns:** Text and non-text contrast against WCAG thresholds (computed, not eyeballed); keyboard reachability and order; focus visibility and management in overlays; ARIA roles, names and states; reduced motion; colour never the only cue
- **Challenge style:** Asks "can I do this with the keyboard alone?", "what does a screen reader announce here?", "where does focus go when this closes?", "which pairs fail, and what is the fix value?"

#### Content Designer
- **Primary concerns:** Fixed labels and microcopy quoted verbatim; consistent casing, punctuation and terminology; where generated text comes from and how it is transformed; empty, error and loading states have words; inconsistencies listed rather than smoothed over
- **Challenge style:** Asks "is this the exact text users see?", "why is this one 'Json' and that one 'JSON'?", "what does the user read when it fails?", "who writes this string, the template or the API?"

#### Learning Designer
- **Primary concerns:** Whether the artifact actually produces learning outcomes, scaffolding from simple to complex, appropriate challenge level, whether the learner builds a correct mental model
- **Challenge style:** Asks "what misconception could this create?", "does the learner know what to focus on?", "is there a way to check understanding before moving on?", "would a novice build the right mental model from this?", "what's the learning objective for each step?"

#### Quality Reviewer
- **Primary concerns:** Completeness, correctness, consistency, adherence to standards
- **Challenge style:** Produces a structured gap analysis, finds missing sections, inconsistencies between stated intent and actual content

#### Business Analyst
- **Primary concerns:** Data completeness, business question answered, insight clarity, actionability
- **Challenge style:** Asks "does this answer the actual business question?", "what's the insight?", "who acts on this and how?"

#### Data Analyst
- **Primary concerns:** Statistical validity, data quality, visualization clarity, methodology
- **Challenge style:** Questions methodology, points out correlation vs causation, asks about sample sizes

#### Data Engineer
- **Primary concerns:** Pipeline reliability, data lineage, schema stability, scale, freshness
- **Challenge style:** Asks about data freshness, what breaks if upstream changes, how to reprocess historical data

#### Executive Stakeholder
- **Primary concerns:** Strategic alignment, headline metrics, risk to business objectives
- **Challenge style:** Asks "so what?", "what decision does this inform?", "what's the risk if we're wrong?"

#### Customer / Requester
- **Primary concerns:** "Is my problem solved?", "What happens next?", "When will this be fixed?"
- **Challenge style:** Asks if the ticket accurately describes their problem, whether the proposed fix addresses root cause

#### Support Engineer
- **Primary concerns:** Reproducibility, workarounds, impact scope, communication to customer
- **Challenge style:** Asks "can I reproduce this?", "what's the workaround?", "how many customers are affected?"

#### Developer (Jira/Ticket context)
- **Primary concerns:** Root cause accuracy, fix scope, regression risk, whether the ticket gives enough info to start coding without guessing
- **Challenge style:** Asks "is the root cause correct or just a symptom?", "what test prevents regression?", "is the scope of the fix clear enough to estimate?", "can I reproduce this from the ticket alone?"

#### QA / Tester
- **Primary concerns:** Acceptance criteria, test coverage, regression, edge cases
- **Challenge style:** Asks "are acceptance criteria testable?", "what regression tests are needed?", "what are the edge cases?"

#### New Team Member
- **Primary concerns:** "Can I follow these instructions?", "Is anything assumed without explanation?", "What do I need to know first?"
- **Challenge style:** Asks "what is X?", "what should I do if step 3 fails?", "where do I find Y?"

#### Domain Expert
- **Primary concerns:** Accuracy, depth, missing nuance — adapted by context:
  - *In KB article review:* Is the information accurate and complete? Are edge cases in the domain knowledge covered?
  - *In test review (domain-heavy):* Do the test assertions reflect real business rules? Are the test scenarios realistic? Are edge cases grounded in actual domain behavior (e.g., boundary values for calculations, valid state transitions, real-world workflow variations)?
- **Challenge style:**
  - *KB:* Points out inaccuracies, oversimplifications, missing edge cases
  - *Tests:* Asks "does this assertion reflect the real rule or a simplified version?", "what happens on month boundaries / zero values / currency rounding?", "is this test scenario something that actually occurs in production?"

#### Documentation Specialist
- **Primary concerns:** Template adherence, audience match, section completeness, cross-references between docs, whether the doc serves its specific reader (DevOps vs new dev vs executive)
- **Challenge style:** Asks "which template does this follow?", "who is the reader and does the tone match?", "are all required sections present?", "does this cross-reference related docs?"

#### Technical Writer
- **Primary concerns:** Clarity, structure, audience fit, consistent terminology, completeness
- **Challenge style:** Identifies ambiguous phrasing, inconsistent terms, missing examples, wrong audience level

#### Migration Engineer
- **Primary concerns:** ETL reliability, transformation correctness, idempotency, script failure modes, data loss risk, handling dirty source data
- **Challenge style:** Asks "what happens when the source field is null?", "can this be re-run safely if it fails halfway?", "what's the rollback plan?", "how do we handle duplicates in the source?"

#### Customer Success Manager
- **Primary concerns:** Adapted by context:
  - *Migration panel:* Client experience, go-live risk, sign-off clarity, whether the client understands what they're approving
  - *Support panel:* Whether customer communication is accurate and trust-preserving; whether responsibility is being pushed to the customer prematurely
- **Challenge style:**
  - *Migration:* Asks "does the client know what they're validating?", "who owns the go/no-go decision?", "what's the rollback communication plan?"
  - *Support:* Asks "does this response accurately reflect what we found?", "are we blaming the customer's team without proof?", "is the tone appropriate given urgency?"

#### Data Steward
- **Primary concerns:** Data integrity, lineage, what gets lost in translation, reconciliation completeness, whether the migrated data tells the same story as the source
- **Challenge style:** Asks "how do we prove no records were dropped?", "what's the control total comparison?", "are relationships between records preserved?", "what data exists in the old system that has no home in the new one?"

#### Production Reliability Engineer
- **Primary concerns:** Failure modes, retry logic, error categorization, observability, what happens at 3am when nothing works, bounded retries, kill switches, suspend-vs-stop distinctions, measurable SLAs
- **Challenge style:** Asks "what happens when this fails for the 4th time?", "how does the operator know something is wrong?", "is this retry idempotent?", "what's the kill switch?", "can this loop forever?"

#### Minimalist Developer
- **Primary concerns:** Complexity cost, whether each feature earns its place, cognitive load on future maintainers, YAGNI violations, whether simpler alternatives exist
- **Challenge style:** Asks "do we actually need this?", "could a simpler version solve 90% of the problem?", "how much does this cost in complexity?", "will anyone ever use this in practice?"

#### Product Manager (Automation Pipeline)
- **Primary concerns:** Time-to-value for the user setting up a new pipeline, clarity of what the skill delivers, whether suggestions improve real user outcomes vs internal plumbing, onboarding friction, measurable success criteria
- **Challenge style:** Asks "who benefits from this?", "does this make the first pipeline setup faster or slower?", "would a user notice this improvement?", "what does 'better' look like from outside the system?"

#### AI Safety & Governance Expert
- **Primary concerns:** Runaway agent behavior, scope creep beyond project boundaries, immutable guardrails, auditability of autonomous decisions, human override paths, blast radius of failures, what the pipeline can never be allowed to do
- **Challenge style:** Asks "what prevents this from acting outside the project?", "can the operator audit what happened and why?", "what happens if the constitution gets corrupted?", "is there a human override for every autonomous action?", "what's the maximum damage this can do if it goes wrong?"

#### Senior Support Engineer
- **Primary concerns:** Is the root cause evidence-based or just asserted? Are alternative hypotheses ruled out? Is there a workaround? Is the escalation path correct?
- **Challenge style:** Asks "is this confirmed from the attachment or inferred from the description?", "what's the workaround while the fix is pending?", "have we ruled out config/data fixes before going to L3?"

#### Application Domain Expert
- **Primary concerns:** Technical accuracy of the diagnosis — are the application/BAPI behaviors described correctly? Are domain concepts (ledger groups, depreciation areas, posting types, accounting standards) used accurately?
- **Challenge style:** Corrects technical inaccuracies: "that's not how SAP handles this", "CURRENCYAMOUNT being empty is an NLA data issue, not a SAP config problem", "is ledger group YT the local or group ledger for this client?"

#### L3 Dev Escalation Reviewer
- **Primary concerns:** Is this actually a code bug, or a config/data issue mislabeled as one? Is the escalation package complete enough to act on? Is the root cause specific enough to assign to a developer?
- **Challenge style:** Asks "is this a bug or a misconfiguration — I need to know before I look at code", "the package needs the exact BAPI parameters, not a summary", "have all config/data fixes been genuinely ruled out?", "can I reproduce this from what's been provided?"

#### Implementation Consultant
- **Primary concerns:** Real-world migration failure patterns, process gaps, what the plan doesn't account for — drawn from experience of migrations that went wrong
- **Challenge style:** Raises war stories: "we've seen this fail when the old system had undocumented status codes", "what about the records that were manually patched directly in the database?", "has anyone checked if the old system has soft-deleted records?"
