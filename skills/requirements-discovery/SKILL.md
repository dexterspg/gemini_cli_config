---
name: requirements-discovery
description: Structured discovery interview conducted BEFORE writing any PRD or requirements. Use this when the user has a feature idea or project but isn't sure what exactly to build — phrases like "where do we even start", "help me understand what we actually need to build", "I want to gather requirements", "let's define the problem first", "before we write the PRD", "I have an idea but I'm not sure what it should do", or kicking off any new feature at the ideation/definition stage. Do NOT trigger when the PRD already exists, the feature is in development, the user wants to review or implement existing requirements, or write a tech spec or test cases.
---

# Requirements Discovery

## Purpose

Validate and understand the problem **before writing any requirements**. This is a structured interview — nothing is written to a document until the user has answered all relevant questions and the discovery summary is confirmed.

Think of this as the examination before the prescription.

---

## When to Use

| Project Size | Discovery Mode |
|---|---|
| **Mini** | Ask 2-3 inline targeted questions then produce summary |
| **Standard** | 5-question structured interview then produce summary |
| **Enterprise** | Full relentless interview (grill-me depth) then produce summary |

**Skip this skill entirely** only when the user provides a long, detailed brief that already answers all the fields in the Discovery Summary below.

---

## Rules

- Ask **one question at a time** — never bundle multiple questions
- **Always give a suggested answer** alongside each question — never leave the user without a proposed direction
- For Mini: ask only what is genuinely unclear — do not over-interview simple tools
- For Enterprise: walk every branch of the decision tree before producing the summary
- **Do not write requirements during discovery** — that is the strategist's job
- Stop when all Discovery Summary fields can be filled confidently

---

## Question Bank (scale to project size)

### Always Ask (all sizes)
1. What problem does this solve, and who has it? *(Suggested: describe the pain point in one sentence from the user's perspective)*
2. What does success look like — what specific outcome makes this "done"? *(Suggested: a measurable or observable outcome)*    
3. What is the single most important output the user needs from this? *(Suggested: the primary deliverable)*

### Standard + Enterprise Only
4. Who are the primary users and what is their current workflow? *(Suggested: describe the role and what they do today without this feature)*
5. What are the known constraints — timeline, budget, compliance, technical limits? *(Suggested: list any hard deadlines or non-negotiables)*

### Enterprise Only
6. Are there existing systems or patterns this must integrate with or follow?
7. What have you already tried or considered, and why was it ruled out?
8. What are the failure modes — what happens if this goes wrong?
9. Who else is impacted that hasn't been mentioned yet?
10. What is explicitly out of scope for this effort?

---

## Output — Discovery Summary

Once all questions are answered, produce this summary and confirm it with the user before handing off to the strategist.

```
## Discovery Summary

**Project Size:** Mini | Standard | Enterprise

**Problem Statement (confirmed):**
[One paragraph — the actual problem, validated with the user]

**Primary Users:**
[Who they are and what their current workflow looks like]

**Primary Deliverable:**
[The single most important output the user needs]

**Constraints:**
- [Timeline, budget, compliance, technical limits]

**Resolved Ambiguities:**
- [Question asked → answer given]
- [Question asked → answer given]

**Out of Scope (confirmed):**
- [What the user explicitly said they do NOT want]
```

---

## Handoff

After the user confirms the Discovery Summary:

1. Pass the full summary to **agent-product-strategist** as context
2. Tell the strategist: "Use this Discovery Summary as your input — do not re-ask these questions"
3. The strategist writes the formal PRD using the summary as its foundation
