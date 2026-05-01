---
name: poc-writer
description: Guide the main session or any agent through writing a business-facing Proof of Concept (PoC) document.
---

# PoC Writer Skill

## Purpose

Guide the main session or any agent through writing a business-facing Proof of Concept (PoC) document. A PoC is produced **before** any technical work begins — it is a business justification document, not a technical experiment. Its audience is product owners, business stakeholders, and management.

## Core Principle

> A PoC answers one question: "Is this idea worth investing in?" It is not code. It is a structured argument for why a problem is real, why this solution addresses it, and whether the investment is justified.

---

## When to Use This Skill

Triggers: "write a PoC", "create a proof of concept", "PoC for [project]", "business case for [idea]", "justify this idea", "should we build [X]"

---

## Information Gathering (Ask First)

Before writing the PoC, gather this from the user. Ask all at once — do not ask one by one:

1. **What is the problem?** What pain point or inefficiency exists today?
2. **Who is affected?** Which users, teams, or departments experience this problem?
3. **What is the proposed solution?** What would the product or feature do at a high level?
4. **What is the expected value?** Time saved, cost reduced, revenue gained, risk avoided?
5. **What is the scope?** What is included? What is explicitly out of scope?
6. **What are the risks?** What could prevent this from working?
7. **What does success look like?** How do we know the PoC passed?
8. **Who are the stakeholders?** Who needs to approve this?
9. **What is the rough timeline?** When does a decision need to be made?
10. **Who is the audience for this document?** (e.g., finance team, client, internal management) — this determines vocabulary and detail level.

If context is already provided (e.g., user described the project), infer answers and note assumptions — do not ask for information already given.

---

## Audience Rules

**The PoC audience is typically non-technical.** Before writing, identify who will read the document and enforce these rules throughout:

- **Never include:** programming language names, framework names, library names, file names, code snippets, technical architecture, or developer tooling references
- **Never include in Resources table:** tools/systems used to build the solution (e.g., "Python 3.x, pandas, openpyxl"). Only list tools/systems the stakeholder cares about (e.g., "Access to CTR_0422.xlsx")
- **Describe WHAT the tool does, not HOW it is built:** "Standalone desktop application" not "PyInstaller-packaged Python app"; "Web application" not "Vue.js frontend with FastAPI backend"
- **Technical jargon test:** Before finalizing, re-read every sentence. If a non-technical stakeholder would need to Google a term, replace it with plain language.
- **Exception:** If the audience IS technical (e.g., engineering leadership), the user will say so. Only then can technical terms appear.

---

## Timeline Estimation Rules

**Never put arbitrary dates.** Timelines must be grounded in realistic effort estimates.

### How to estimate build time

Break the application into functional components and estimate each:

1. List what needs to be built (e.g., file parser, calculation engine, output generator, UI)
2. Estimate each component: simple (1-2 days), moderate (2-3 days), complex (3-5 days)
3. Add integration + testing time (typically 30-50% of build time)
4. Add bug fix buffer (1-2 days)
5. Sum it up — this is the build phase

### Timeline structure

| Phase | Typical Duration |
|-------|-----------------|
| Build (single developer) | Sum of component estimates |
| Internal validation + fixes | 2-3 days after build |
| Client/stakeholder review | 1 week (external dependency) |
| Go / No-Go decision | 1-3 days after review |

### Rules

- **Always show your math** to the user before writing the timeline — ask "does this feel right?"
- **Never compress build time** to fit a desired deadline — flag the conflict instead
- **Separate internal vs external milestones** — build time is in your control, client review is not
- **Break build milestones into functional components** — not "PoC build complete" but the individual pieces (parser, engine, output, etc. described in business terms)

---

## Scope Rules

### In-scope must match the actual deliverable

Before writing the Scope section, confirm with the user:
- **What is the final deliverable?** (desktop app, web app, both, script, report?)
- **What does the user hand to the client/stakeholder?** — that is in scope

Common mistake: listing a deliverable (e.g., desktop application, web interface) as "out of scope" when it is actually part of what is being built. If the user is building it, it is in scope.

### Out-of-scope must use business language

- Wrong: "PyInstaller packaging", "Vue.js frontend"
- Right: "Desktop installer", "Web-based interface"

---

## PoC Document Template

Save to: `{project-root}/docs/proof-of-concept.md`

```markdown
# Proof of Concept: {Project/Feature Name}

**Ticket:** {ticket reference, if applicable}
**Author:** {author name}
**Date:** {date}
**Status:** Draft | Under Review | Approved | Rejected

---

## 1. Executive Summary

{1-2 paragraphs. What are we testing and why? What is the Go/No-Go decision this document supports?}

---

## 2. Problem Statement

**The problem:** {What is the pain point or opportunity?}

**Who is affected:** {Teams, roles, departments}

**Current state:** {How is this handled today? What is the manual workaround?}

**Impact of not solving:** {Cost, risk, inefficiency if nothing changes}

---

## 3. Proposed Solution

{High-level description of the solution. Describe WHAT it does for the user, not HOW it is built.}

**Key capabilities:**
- {Capability 1}
- {Capability 2}
- {Capability 3}

---

## 4. Goals & Objectives

| Goal | Measurable Outcome |
|------|--------------------|
| {Goal 1} | {How it will be measured} |
| {Goal 2} | {How it will be measured} |

---

## 5. Scope

**In scope:**
- {What this PoC covers — must include the actual deliverable}

**Out of scope:**
- {What is explicitly excluded — use business language, not technical terms}

**Assumptions:**
- {What we are assuming to be true}

---

## 6. Required Resources

| Resource | Details |
|----------|---------|
| People | {Roles needed — not technical stack} |
| Data | {Input files, datasets, access needed} |
| Budget (estimate) | {Cost range if applicable} |
| Time | {Duration with build + review phases separated} |

Note: Do NOT include developer tools, languages, or libraries in this table.

---

## 7. Success Criteria

The PoC is considered **passed** if:
- {Criterion 1 — specific, measurable}
- {Criterion 2}

The PoC is considered **failed** if:
- {Failure condition 1}
- {Failure condition 2}

---

## 8. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| {Risk 1} | High/Med/Low | High/Med/Low | {How to reduce} |
| {Risk 2} | | | |

---

## 9. Timeline & Milestones

| Milestone | Target Date |
|-----------|------------|
| {Data/input available} | {date} |
| {Component 1 complete — described in business terms} | {date} |
| {Component 2 complete} | {date} |
| {Internal validation + fixes} | {date} |
| {Client/stakeholder review} | {date} |
| {Go/No-Go decision} | {date} |

---

## 10. Stakeholders

| Name / Role | Responsibility |
|-------------|---------------|
| {Name} | Approver |
| {Name} | Contributor |
| {Name} | Informed |

---

## 11. How It Works

{Plain-language description of the processing steps. Written so a non-technical reader can follow the flow from input to output. Use numbered steps or a simple flow — NO code, NO file names, NO technical architecture.}

### Key Formula

{If the tool performs calculations, show the formula in business/accounting terms.}

### Example Calculation

{Concrete worked example with real-looking numbers.}

---

## 12. Recommendation

**Go / No-Go / Needs More Information**

{1 paragraph. Based on the above, what is the recommendation and the key reason? Do not reference technical stack in the recommendation.}
```

---

## Writing Rules

- **Audience is non-technical by default** — no programming languages, no framework names, no file names unless the user explicitly says the audience is technical
- Executive Summary must stand alone — a busy executive should get the full picture from section 1 alone
- Success Criteria must be specific and measurable — "it works" is not a criterion
- Risk table must have at least 2 rows — if the user says there are no risks, prompt them to think harder
- Recommendation section is mandatory — never leave it blank or vague
- Scope "Out of scope" must have at least 1 entry — a PoC that includes everything is not a PoC
- **Scope "In scope" must include the actual deliverable** — confirm what is being delivered before writing
- **Timeline must be grounded in component-level estimates** — never write arbitrary dates
- **"How It Works" section must exist** — stakeholders need to understand the process flow, just not the code behind it        
- **Resources table must never list developer tools** — only list what the stakeholder cares about (people, data, budget, time)

---

## Output Checklist

Before finalizing, verify:
- [ ] All 12 sections are present (including "How It Works")
- [ ] Executive Summary is 1-2 paragraphs max
- [ ] Success Criteria are measurable
- [ ] At least one risk is documented
- [ ] Out of scope has at least one entry
- [ ] In scope includes the actual deliverable
- [ ] Recommendation is stated clearly (Go / No-Go / Needs More Information)
- [ ] **Audience check:** No programming languages, framework names, library names, or file names appear anywhere in the document (unless audience is explicitly technical)
- [ ] **Timeline check:** Dates are grounded in component-level estimates, not arbitrary
- [ ] **Resources check:** No developer tools listed in the Resources table
