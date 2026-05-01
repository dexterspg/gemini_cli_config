---
name: project-estimator
description: Provide realistic time estimates and delivery timelines for software projects. Estimates assume one human developer doing the work manually.
---

# Project Estimator Skill

## Purpose

Provide realistic time estimates and delivery timelines for software projects. Estimates assume **one human developer doing the work manually** — no AI acceleration factored in. If AI speeds things up in practice, that's a bonus, not a planning assumption.

## Core Principle

> A good estimate is one the developer can defend to a client without embarrassment six weeks later. Underestimating erodes trust. Overestimating wastes opportunity. The goal is honest, grounded estimation.

---

## When to Use This Skill

Triggers: "how long will this take", "estimate this project", "timeline for [project]", "is this timeline realistic", "can we do this in [X] weeks", "project estimate", "delivery date"

Also load this skill when:
- Writing PoC documents (timeline and resources sections)
- Product strategist is sizing a project
- User questions whether a timeline is realistic

---

## Step 1: Decompose Into Components

Break the project into functional components the user would recognize. Use business language, not technical jargon.

**Common component categories:**

| Category | Examples |
|----------|---------|
| Data input/parsing | File upload, format validation, data extraction |
| Business logic/engine | Calculations, rules, transformations |
| Data output | Report generation, file export, formatted output |
| Backend API | Server endpoints, data flow, authentication |
| Frontend UI | Screens, forms, navigation, user interactions |
| Packaging/deployment | Installer, hosting, delivery mechanism |
| Integration | Third-party systems, APIs, data sync |

List every component. If you can't name it, you can't estimate it.

---

## Step 2: Estimate Each Component

### Base effort (experienced developer who knows the stack)

| Complexity | Duration | Signals |
|-----------|----------|---------|
| Simple | 1-2 days | Standard CRUD, well-known patterns, minimal logic |
| Moderate | 3-5 days | Custom logic, multiple edge cases, some unknowns |
| Complex | 1-2 weeks | Novel algorithms, many integrations, significant unknowns |
| Very complex | 2-4 weeks | Research required, no clear pattern, high uncertainty |

### Familiarity multiplier

Apply this to **each component** based on the developer's experience with the specific technology:

| Familiarity | Multiplier | Description |
|------------|-----------|-------------|
| Expert | 1.0x | Has built this many times before |
| Comfortable | 1.0x | Knows the stack, done similar work |
| Some experience | 1.3x | Has used it but not for this type of work |
| Beginner | 1.8x | Knows the concepts, first time building with it |
| Brand new | 2.5x | Never used this technology before |

**Rules:**
- The multiplier accounts for learning time — never add a separate "learning" line item in client-facing documents
- Learning is real effort but it's internal. The client sees "build frontend: 3 weeks", not "learn Vue: 1 week, build frontend: 2 weeks"
- Ask the developer about their comfort level. Do not assume.

---

## Step 3: Add Integration, Testing, and Debugging

After summing component estimates, add:

| Phase | Calculation |
|-------|------------|
| Integration (connecting components) | 15-25% of total build time |
| Testing and bug fixes | 20-30% of total build time |
| Debugging and troubleshooting | 10-20% of total build time |

**Debugging is not the same as bug fixes.** Bug fixes are known issues with clear reproduction steps. Debugging is the time spent investigating unexpected behavior — tracing code paths, isolating root causes, ruling out hypotheses, and documenting findings. This is real work that often gets forgotten in estimates.

### When to use the higher percentages

| Factor | Integration | Testing | Debugging |
|--------|------------|---------|-----------|
| Components are tightly coupled | Higher | — | Higher |
| Multiple technologies interact | Higher | Higher | Higher |
| Developer is new to the stack | — | Higher | **Much higher (20%+)** |
| No existing test infrastructure | — | Higher | — |
| Third-party APIs or external systems | Higher | Higher | Higher |
| Complex business logic (financial calculations, etc.) | — | Higher | Higher |

**Debugging estimate rule:** For developers new to the stack, debugging time can easily exceed testing time. Unfamiliar errors take longer to investigate because the developer doesn't yet have mental models of how the framework behaves. Account for this honestly.

---

## Step 4: Add External Dependencies

These are phases outside the developer's control:

| Phase | Typical Duration |
|-------|-----------------|
| Client/stakeholder data delivery | 1 week (ask user) |
| Client/stakeholder review | 1-2 weeks |
| Sign-off / Go decision | 3-5 business days |
| Feedback iteration (if rejected) | 1-2 weeks per round |

**Rule:** Always separate internal milestones (in your control) from external milestones (not in your control) in the timeline.  

---

## Step 5: Generate Timeline

Convert estimates into calendar dates:

1. Start from the project start date (or today if unknown)
2. Lay out components in logical build order (dependencies first)
3. Assign calendar dates accounting for weekdays only
4. Insert external dependency milestones at the right points
5. Add the final Go/No-Go date

### Milestone naming rules (for client-facing documents)

- Use business language: "File processing complete" not "Parser module done"
- Name what the client gets, not what the developer builds
- Never mention specific technologies, frameworks, or libraries

---

## Red Flags to Catch

Before finalizing any estimate, check for these:

| Red Flag | What to Do |
|----------|-----------|
| Full application "from scratch" estimated at under 2 weeks | Challenge it — decompose and re-estimate |
| Frontend + backend estimated at same duration as backend alone | Frontend is almost always equal or longer — check |
| No testing/integration buffer | Add 30-50% to the build total |
| Single milestone called "build complete" | Break it into components |
| Timeline compressed to fit a desired deadline | Flag the conflict honestly — never compress estimates to fit |
| Developer building with unfamiliar stack but estimated at expert pace | Apply familiarity multiplier |
| External review phase under 1 week | Clients are slow — be realistic |

---

## Output Format

When presenting estimates to the user (not the client), show the math:

```
Component Breakdown:
- [Component 1]: [base] × [multiplier] = [adjusted]
- [Component 2]: [base] × [multiplier] = [adjusted]
- ...
Subtotal build: X weeks
+ Integration (20%): Y days
+ Testing + fixes (25%): Z days
+ Debugging + troubleshooting (15%): Z days
Total build: X weeks

External:
+ Client review: 1-2 weeks
+ Sign-off: 3-5 days
Total end-to-end: X weeks
```

For client-facing documents (PoC, proposals), show only the milestone table — never show the multipliers or the math behind it.

---

## What NOT to Include in Client-Facing Estimates

- Learning time as a separate line item
- Technology names (Python, Vue, FastAPI, etc.)
- Familiarity multipliers or skill-level references
- Internal tooling setup
- Developer ramp-up activities

These are real but internal. Bake them into component estimates silently.

---

## Calibration Questions

Ask these before estimating:

1. **How many developers?** (default: 1 — never assume parallel work unless confirmed)
2. **Familiarity with each technology involved?** (expert / comfortable / some experience / beginner / brand new)
3. **Is there existing code to build on, or is this from scratch?**
4. **Are there external dependencies (client data, approvals, third-party access)?**
5. **What is the deliverable?** (prototype, MVP, production app, PoC validation)
6. **Is there a hard deadline?** (if yes, flag conflicts honestly rather than compressing estimates)
