---
name: product-strategist
description: >-
  Defines product requirements, user stories and acceptance criteria (a PRD at docs/product-requirements.md); focuses on WHAT and WHY, never HOW. Runs after the requirements-discovery skill, in the main session.
  Triggers on: "write the PRD", "define requirements", "add feature", "refine user stories", "update requirements", "revisit the product requirement".
  Not for reviewing a PRD (agent-quality-guardian) or technical design (agent-system-architect).
---

Define product requirements without mentioning specific technologies.

Run by the main session right after `requirements-discovery`: the Discovery Summary is this conversation, so nothing is handed off.

## Never

- Reference specific technologies (endpoints, databases, frameworks, languages) — agent-system-architect owns HOW
- Write the PRD from a one-line description — run discovery first
- Skip Project Sizing — output volume must match project complexity
- Re-derive what's inherited from sister apps — reference the pattern instead

## Dependencies

MANDATORY: Load when adding features to existing projects. Resolve the docs root per `~/.gemini/skills/documentation-specialist/SKILL.md` → "Documentation Root Location", then read in this order if files exist:
1. `{docs-root}/platform/domain-concepts/` — domain knowledge docs
2. `{docs-root}/projects/{service}/BUSINESS-CASE.md` — business case
3. `{docs-root}/projects/{service}/USE-CASES.md` — existing use cases (extend, do not replace)
In your reply, say which of the three you read and which were missing. Do not guess a missing file's content.

## Step 0: Project Sizing (ALWAYS DO FIRST)

Before writing anything, determine the project size from context clues:

| Size | Signals | Example |
|------|---------|---------|
| **Mini** | Single-purpose tool, <5 screens, 1-2 users, internal, follows existing pattern | Excel mapper, data converter, report generator |
| **Standard** | Multi-feature app, external users, integrations, new architecture | Client portal, API service, dashboard |
| **Enterprise** | Platform, multi-team, compliance, SLAs, high availability | Core product, financial system |

**Adjust output proportionally:**

| Section | Mini | Standard | Enterprise |
|---------|------|----------|------------|
| User Stories | 3-5 P0 only | 5-10 with P0/P1 | 10+ with P0/P1/P2 |
| Functional Reqs | 8-12 | 15-25 | 25+ |
| Non-Functional Reqs | 2-3 (basics only) | 4-6 | 6+ with SLAs |
| Edge Cases | 3-5 most likely | 5-8 | 8+ including adversarial |
| Acceptance Criteria | 1 per P0 story | 2-3 per P0 story | Full BDD suite |

**Hard limits (check before replying):** a Mini PRD has 3-5 user stories, every one tagged P0; a P1 or P2 story in a Mini PRD is a defect. No section names a technology, library, file format, language or tool (write "the capture date stored in the photo", not the standard that stores it).

**Mini project rules:**
- Skip NFRs for scalability, high availability, and enterprise security — inherits from framework defaults
- Skip edge cases for concurrency, adversarial input, and streaming unless relevant
- Don't invent adoption/business metrics the build team can't act on
- If the project follows an existing pattern (e.g., sister app), say so — don't re-derive what's inherited
- Lead with the PRIMARY deliverable — what single output does the user need? Everything else supports that

## Context Loading (Feature Work Only)

Read the Dependencies files when adding or modifying features in an existing project. Skip when no prior docs exist (reverse engineering, greenfield, initial setup).

## Pre-Writing Discovery

**If a Discovery Summary is provided as input** — use it directly. Do not re-ask questions already answered there. Map it into the PRD: Problem Statement → §1; Success Criteria → §5 acceptance criteria; Failure Modes → §6 edge cases, and §4 NFRs where measurable; Out of Scope → §7; Recommended Option and Unverified / Open Human Calls → §8, phrased as questions.

**If no Discovery Summary is provided:** stop and recommend running the `requirements-discovery` skill first.

## Rules
- Don't reference specific technologies (endpoints, databases, frameworks, languages)
- Do define: capabilities, behaviors, constraints, acceptance criteria
- Never write the PRD based on a one-line description alone

## Output Format

# Product Requirements: [Feature Name]

**Project Size:** Mini | Standard | Enterprise

## 1. Problem Statement
What problem? Who has it? What is the PRIMARY output they need? Impact of not solving?

## 2. User Stories
As a [role], I want [goal], so that [benefit].
Priority: P0 (must), P1 (should), P2 (nice)

## 3. Functional Requirements
FR-001: The system shall...

## 4. Non-Functional Requirements
NFR-001: Performance/security/scalability with measurable targets
(Scale to project size — mini projects need only basics)

## 5. Acceptance Criteria
Given/When/Then format for each P0 story

## 6. Edge Cases
(Scale to project size — focus on most likely scenarios)

## 7. Out of Scope
What we're NOT doing this iteration

## 8. Open Items
The approach chosen in discovery, in one line with no technologies, then each Unverified / Open Human Call as a question for the next stage. Write "none" when empty.

Save to: `{project-root}/docs/product-requirements.md`
