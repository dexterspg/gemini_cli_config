---
name: architecture-audit
description: 'Audit existing code for architectural friction — shallow modules, tight coupling, hard-to-test seams — and propose a concrete redesign with trade-off analysis. Use this when working on an EXISTING codebase that feels hard to change, test, or reason about. Trigger phrases include "this code is getting messy", "hard to test this module", "too much coupling", "refactor the architecture", "audit the architecture", "this design isn''t scaling", "improve the structure of X", "find architectural problems in", or when agent-quality-guardian flags an architectural concern. Do NOT trigger during new feature development — that is agent-system-architect''s territory.'
---

# Architecture Audit

## Purpose

Surface architectural friction in **existing code** and propose a concrete redesign. Backward-looking analysis — audit what exists, not design what is new.

---

## Core Framework: Deep Modules

A well-designed module has a **small interface hiding a large implementation** (Ousterhout, *A Philosophy of Software Design*). Shallow modules (simple interface, simple implementation) add complexity without benefit — they are just call-through layers.

Signs of shallow modules:
- Every caller reaches into implementation details
- Changing internals forces changes in callers
- Mocking this module requires mocking 5 other things
- The interface is almost as complex as the implementation

---

## Dependency Categories

Use this to classify what a module depends on — determines how it can be redesigned and tested:

| Category | Description | Can deepen? | Test strategy |
|---|---|---|---|
| **In-process** | Pure computation, no I/O | Always | Unit test directly |
| **Local-substitutable** | Has a local stand-in (e.g. SQLite, PGLite, in-memory queue) | Yes | Use the stand-in |
| **Remote but owned** | Your own service, your own DB | Yes, via ports & adapters | Define port at boundary, inject transport |      
| **True external** | Third-party API, payment service, email | Mock at boundary only | Stub or fake at the interface boundary |      

**Testing principle: replace, don't layer.** Once you define a clean boundary and write boundary tests, delete the old shallow unit tests — they were testing implementation details, not behavior.    

---

## Process

### Step 1: Explore for Friction

Before asking any questions, read the relevant code. Look for:     
- Modules whose callers reach into their internals
- Functions that do too many things (multiple concerns per function)
- Hard-to-test seams (new X() inside a function, hidden singletons, global state)
- Modules that change for many different reasons (violates single-responsibility)
- Cross-cutting concerns repeated in multiple places

If `docs/technical-specification.md` exists, read it — don't propose redesigns that contradict the intended architecture.

Delegate deep codebase reading to `agent-codebase-archaeologist --domain` if the codebase is large or unfamiliar.

### Step 2: Present Friction Candidates

Present a numbered list. For each candidate:
- **What it is**: module/function/cluster name
- **The friction**: what makes it hard to work with
- **Dependency category**: in-process / local-substitutable / remote-owned / true-external
- **Test impact**: what's currently untestable or brittle because of this

Do NOT propose solutions yet. Ask the user to pick one.

Example format:
```
1. PaymentProcessor — tight coupling to StripeClient (remote-owned). Three callers import and instantiate StripeClient directly. Mocking requires patching the module import. Dependency category: Remote but owned.

2. ReportBuilder — shallow module. Delegates to 7 sub-functions with no abstraction. Callers are aware of the sub-function structure. Hard to add a new report type without touching all callers.      
```

### Step 3: Frame the Problem Space

After the user picks a candidate:

1. Write out the **constraints**: what must not change (public API, data format, downstream consumers)
2. Write out the **dependencies**: classify each one using the dependency table above
3. Sketch the **current interface**: what callers see today        
4. Show an **illustrative example** of the friction in concrete code

Show this framing to the user before proposing solutions. Confirm the constraints are correct.

### Step 4: Propose a Redesign

Generate a single concrete proposal. Structure it as:

**Proposed interface** — what callers would see after the redesign (signatures, not implementation)

**Hidden complexity** — what gets moved behind the interface (the implementation details callers currently reach into)

**Dependency strategy** — using the category from Step 3: how are dependencies injected / stubbed / faked?

**Migration path** — how to move from current to proposed without breaking callers (incremental steps, not a big-bang rewrite)      

**Trade-offs** — what this design optimizes for and what it sacrifices

**Test strategy** — which tests to write first, which existing tests to delete after the boundary is established

For complex cases (multiple competing approaches are genuinely unclear), generate 2-3 proposals and present a comparison:

| | Option A | Option B | Option C |
|---|---|---|---|
| Interface surface | | | |
| Migration cost | | | |
| Testability | | | |
| Dependency count | | | |
| Best for | | | |

Ask the user to pick. Give your recommendation but don't force it. 

### Step 5: Write the Audit Document

After the user picks a proposal, write `docs/architecture-audit.md`:

```markdown
# Architecture Audit: [Module/Cluster Name]
Date: [date]
Status: Proposed

## Problem
[friction description from Step 2]

## Constraints
[what must not change]

## Current Interface
[what callers see today]

## Proposed Interface
[what callers will see after redesign]

## Dependency Strategy
[category + how dependencies are handled]

## Migration Steps
1. [smallest first step that leaves codebase working]
2. ...

## Test Strategy
- Safety nets to write BEFORE refactoring: [list]
- New boundary tests to write: [list]
- Old tests to delete after: [list]

## Trade-offs
[what this optimizes for, what it sacrifices]
```

Do NOT include file paths in the Problem, Constraints, or Trade-offs sections — they go stale. File paths belong only in Migration Steps and Test Strategy, where they are immediately actionable.     

### Step 6: Route to Quality Guardian

After writing the audit document, route to `agent-quality-guardian` with:
- `docs/architecture-audit.md` as the artifact to review
- `docs/technical-specification.md` (if it exists) as the reference standard

The guardian checks: feasibility, edge cases, consistency with existing tech spec, completeness of migration steps.

If APPROVED → the audit is ready to hand off to `agent-implementation-engineer` via the `prd-to-tasks` skill (treat Migration Steps as the slice list).

---

## Scope Guard

Stay focused on the candidate the user picked. If you notice other friction during exploration, note it in a "Further Observations" section at the bottom of the audit document — do not expand scope mid-session. Each architectural concern deserves its own audit.     
