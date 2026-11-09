---
name: adversarial-review
description: >-
  Adversarial panel review run by the main session. Detects the content type, spawns 4 parallel read-only attack threads that each try to break the work on one concern group, then judges every claim against the work and reports only verified findings, a coverage grade and a verdict. Use when the user asks to "review from multiple perspectives", "panel review", "get diverse opinions on this", "review this from different angles", "what would [different roles] think of this", "multi-persona review", "stress-test this with multiple reviewers", or wants critique from a junior dev + senior architect + business stakeholder + QA engineer style spread. Not for a routine single check (agent-quality-guardian).
---

# Adversarial Review

The main session detects the type, briefs 4 attack threads in parallel, judges their claims and reports. Threads get a task and
a concern checklist, never an identity. Evidence and limits: `~/.gemini/skills/quality-guardian/EVIDENCE-agent-design.md` → rules 1, 4, 6.

**Scale first:** run a panel only when the user asks for one or the work is high-stakes (global `GEMINI.md` → "review this" row).
For a routine one-file review use `agent-quality-guardian`: one briefed reviewer matched a 3-critic panel on a single script.

## Never

- Give an attack thread an identity ("You are a QA Engineer") — give it a task and a concern checklist
- Spawn threads sequentially — launch all 4 in one turn via `invoke_subagent`
- Report a claim as a finding before it was judged against the work
- Judge work this session wrote or edited — spawn a judge thread instead (Step 4)

## Dependencies

MANDATORY: Read `~/.gemini/skills/adversarial-review/CONCERNS.md` before Step 3. Each heading is a concern group; its
Primary concerns and Challenge style questions are the attack checklist.

## Flags

- **Default:** auto-detect content type and select its concern groups
- **`--type [type]`:** override detection. Valid types: `documentation`, `code`, `business-report`, `workflow`, `agent-skill`, `design`, `design-system`, `frontend`, `test`, `migration`, `scheduled-automation-skill`, `support-investigation`, `data-analysis`, `jira-ticket`, `kb-article`
- **`--personas "[p1],[p2],[p3],[p4]"`:** exactly 4 role titles, read as concern groups (never as identities); they replace the standard selection

## Step 1 — Detect Content Type

| Signal | Detected Type |
|--------|---------------|
| `FIELD_MAPPING.md`, `*migration*`, `*_mapping*`, ETL scripts, reconciliation reports, keywords: "source system", "target system", "cutover", "field mapping", "data migration" | `migration` |
| `DESIGN-SYSTEM.md`, `tokens.json`, `drift.config.json`, a Design System artifact, keywords: "design system", "design tokens", "component guidelines" as the subject of a project doc or artifact | `design-system` |
| `.md` in `documentation/`, `skills/`, `agents/`, README patterns | `documentation` |
| Files in `tests/`, `__tests__/`, `spec/`; filenames matching `test_*.py`, `*Test.java`, `*.test.js`, `*.spec.ts`; content with `describe(`, `@Test`, `def test_`, `assert`, `expect(` patterns | `test` |
| `.js`, `.ts`, `.py`, `.java`, `.cs`, `.go`, source code patterns | `code` |
| Status updates, KPIs, finance tables, executive summary language | `business-report` |
| Prompts that generate visual artifacts (SVG, diagrams, dashboards), rendering specs, animation specs, visualization templates, keywords: "rendering", "diagram", "visualization", "interactive", "artifact" | `design` |
| HTML wireframes, Vue/React/frontend components, CSS layouts, UI mockups, `.vue`/`.jsx`/`.tsx` files, keywords: "wireframe", "frontend", "layout", "component", "UI" | `frontend` |
| A multi-stage process or flow definition — files in `skills/workflows/`, flow diagrams, keywords: "stages", "gates", "handoff", "approval step", "rework loop", "definition of done", "workflow" as the subject | `workflow` |
| Agent frontmatter (`name:`, `model:`), skill files, concern catalogs | `agent-skill` |
| Scheduled automation skills/blueprints — keywords: "cron", "Iron Rule", "pipeline constitution", "work queue", "self-improving", "refiner", "fallback", "orchestrator", "scheduled routine", "stage sequence", "heartbeat", multi-agent pipeline blueprints | `scheduled-automation-skill` |
| Data tables, profiling reports, cleaning plans, statistical analysis | `data-analysis` |
| Jira ticket format, bug reports, issue descriptions | `jira-ticket` |
| KB articles, how-to guides, troubleshooting docs | `kb-article` |
| `support-investigation.md`, `support-walkthrough.md`, files in `issues/` folder, keywords: "Five Whys", "kedb_check", "RFC trace", "RETURN messages", "root cause", "Phase 0", "Fix Options", "Escalation Package" | `support-investigation` |

Read top to bottom, except: `workflow` is checked first and wins over `documentation`, `agent-skill` and
`scheduled-automation-skill` when its keywords are the subject; `test` before `code`; `design-system` above `documentation`,
`design` and `frontend`; a skill or agent file whose subject is design systems goes to `agent-skill`. Ambiguous → read the
first 50 lines.

## Step 2 — Select Concern Groups

Each name is a heading in `CONCERNS.md`.

| Content Type | Group 1 | Group 2 | Group 3 | Group 4 |
|-------------|-----------|-----------|-----------|-----------|
| `migration` | Migration Engineer | Customer Success Manager | Data Steward | Implementation Consultant |
| `documentation` | Business Stakeholder | Junior Developer | Senior Architect | Documentation Specialist |
| `test` (simple — utility, CLI, script, no domain logic) | Test Strategist | Developer Under Test | QA Engineer | Tech Lead / Architect |
| `test` (domain-heavy — financial, state machine, workflow, NLA/NFS context) | Test Strategist | Developer Under Test | QA Engineer | Domain Expert |
| `code` | Junior Developer | Senior Developer | Tech Lead / Architect | QA Engineer |
| `business-report` | Finance Director | Operations Manager | Executive Sponsor | Project Manager |
| `design` | End User | UX / Interaction Designer | Learning Designer | Prompt Engineer |
| `frontend` | End User | Senior Developer | UX / Interaction Designer | QA Engineer |
| `design-system` | Design Systems Engineer | Accessibility Specialist | UX / Interaction Designer | Senior Developer† |
| `workflow` | Workflow Owner | Operations Manager* | AI Systems Designer | End User |
| `agent-skill` | End User | Prompt Engineer | AI Systems Designer | Quality Reviewer |
| `scheduled-automation-skill` | Production Reliability Engineer | Minimalist Developer | Product Manager | AI Safety & Governance Expert |
| `data-analysis` | Business Analyst | Data Analyst | Data Engineer | Executive Stakeholder |
| `jira-ticket` | Customer / Requester | Support Engineer | Developer | QA / Tester |
| `kb-article` | New Team Member | Domain Expert | Support Engineer | Technical Writer |
| `support-investigation` | Senior Support Engineer | Application Domain Expert | Customer Success Manager | L3 Dev Escalation Reviewer |

*`workflow` Group 2: keep Operations Manager when several people or teams run the workflow. Replace it with Domain Expert when
the result's correctness depends on domain rules, or Senior Developer when a built script is part of the review.

†`design-system` Group 4: Senior Developer checks the rebuild ("can the UI be ported from this alone?"). Replace it with
Content Designer when labels, casing or microcopy are the subject.

**`test` complexity:** domain-heavy (use Domain Expert) when domain entity names appear in imports or test subjects (Order,
Contract, Invoice, Lease, Account…), the subject is a state machine, approval workflow or multi-step business process, the
service has a business domain, or assertions check money, business dates, status transitions or calculations. Otherwise
simple (use Tech Lead / Architect). In doubt: business outcomes asserted → domain-heavy.

## Step 3 — Spawn 4 Attack Threads

One turn, 4 parallel read-only subagents via `invoke_subagent(TypeName="research")` (or `TypeName="self"` if outside the workspace sandbox, with strict read-only bounds). Each brief carries, and nothing else:
1. **Task:** "Try to break this work on the concerns below. Report only defects you can point to in the work."
2. **Input:** the work's path (or its content when it has no path).
3. **Checklist:** the group's Primary concerns and Challenge style questions from `CONCERNS.md`, adapted to the content.
4. **Project rules:** the work's project `GEMINI.md` (or `CLAUDE.md`) path, plus the path of every rule file it makes mandatory for this file type; a brief without the project rule file misses its project-specific rules (for example a customer-neutral repo).
5. **Bounds:** read-only — no edits, no state-changing commands, no external calls.
6. **Output:** one line per defect, `location — defect — evidence`, 300 words maximum.

## Step 4 — Judge

Sort every claim as **VALID** (the work shows it), **INVALID** (the work contradicts it) or **UNSETTLED** (name what would
settle it), and merge duplicates.
- **This session did not write or edit the work:** judge it yourself, reading the cited lines.
- **This session wrote or edited it:** spawn one judge thread (`invoke_subagent(TypeName="research")`) with the work's path, the rule files, and every claim marked
  unchecked; it returns the three verdicts with the evidence it checked.

## Step 5 — Report

```markdown
# Panel Review — [Content Name]
**Concern groups:** [Group 1] | [Group 2] | [Group 3] | [Group 4]
**Content Type:** [detected type] · **Date:** [today] · **Judged by:** main session | judge thread

## Verified Findings
| # | Severity | Location | Defect | Evidence checked | Found by |
|---|----------|----------|--------|------------------|----------|

## Rejected Claims
- [claim] — [why invalid] ([group])

## Unsettled
- [claim] — [what would settle it] ([group])

## Coverage Verdict
| Dimension | [Group 1] | [Group 2] | [Group 3] | [Group 4] |
|-----------|-----------|-----------|-----------|-----------|
Grades: **Excellent** / **Adequate** / **Gap** / **Missing** — from verified findings only.

## Recommendations
| Priority | Gap | Recommended Action | Location |
|----------|-----|--------------------|----------|

## Panel Verdict
**Consensus:** STRONG / ADEQUATE / NEEDS_WORK / INCOMPLETE
**Biggest Gap:** [one sentence] · **Highest Value Section:** [one sentence] · **Recommended Next Step:** [one action]
```

**Dimensions by type:**
- Migration: Field Mapping Completeness, Transformation Correctness, Reconciliation Coverage, Cutover Risk, Client Handoff Clarity
- Documentation: Clarity, Completeness, Accuracy, Audience Fit, Structure
- Test (simple): Coverage Completeness, Assertion Quality, Test Independence, Edge Case Coverage, Maintainability
- Test (domain-heavy): Coverage Completeness, Assertion Quality, Business Rule Correctness, Edge Case Coverage, Realistic Scenarios
- Code: Correctness, Testability, Security, Maintainability, Performance
- Business Report: Data Accuracy, Insight Clarity, Actionability, Risk Coverage, Strategic Alignment
- Design: Information Hierarchy, Cognitive Load, Progressive Disclosure, Visual Clarity, Learning Effectiveness
- Frontend: Layout & Structure, Responsiveness, State Coverage, Data Presentation, User Flow Completeness
- Design System: Source Traceability, Token & Component Coverage, Accessibility, Interaction & Writing Coverage, Drift Protection
- Workflow: Stage Clarity, Ownership & Handoffs, Gates & Approvals, Failure & Rollback Paths, Done Criteria & Observability
- Agent/Skill: Instruction Clarity, Edge Case Handling, Only What Gemini Cannot Know, Tool Use Correctness, Workflow Coverage
- Scheduled Automation Skill: Failure Mode Coverage, Self-Improvement Loop Integrity, Complexity vs Value, Guardrails & Safety, Onboarding Clarity
- Data Analysis: Methodology, Completeness, Business Question Answered, Visualization, Actionability
- Jira Ticket: Reproducibility, Acceptance Criteria, Impact Scope, Root Cause, Priority Justification
- KB Article: Findability, Step Clarity, Prerequisite Coverage, Troubleshooting, Accuracy
- Support Investigation: Evidence Quality, Hypothesis Coverage, Technical Accuracy, Escalation Routing, Customer Communication

## Rules

1. **Exactly 4 threads**, one per concern group in the type's row; never fewer, never more.
2. **Coverage table is mandatory** — every dimension for every group, from verified findings only.
3. **Recommendations are actionable** — what to fix and where; "improve clarity" is not acceptable.
4. **Consensus reflects the range** — grade each group from its verified findings; 3 STRONG + 1 INCOMPLETE = ADEQUATE; on a 2-2
   split use the lower verdict.
5. **`--personas` respects the user's intent** — infer each title's concerns; do not swap in standard groups.
6. **A failed thread** (empty or error) is named in the Panel Verdict; judge the other 3; never re-run the whole panel.

## Save Location

Report in the conversation. Save to disk only when the user or a workflow asks, at
`{project-root}/reviews/panel-[content-name]-[YYYY-MM-DD].md`.
