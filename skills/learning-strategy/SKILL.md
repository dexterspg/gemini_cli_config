---
name: learning-strategy
description: Use when a user wants to understand how to approach learning — "help me understand this codebase", "how should I approach learning X", "where do I start with [repo]", "onboard me to [project]", "I want to learn this properly", "best way to get into [field]", "how should I learn [domain]", "I want to get into [discipline]". Invoke this before routing any learning request to concept-tutor or codebase-archaeologist — this skill selects the right strategy, pace, and layers first. When in doubt about a learning request, use this skill.
---

# Learning Strategy Skill

Decision framework for selecting the right strategy, pace, and agents when a user wants to learn a codebase, concept, or domain. Read this before routing any learning request.

## Dependencies

- **agent-concept-tutor** — Primary routing target for concept and domain learning
- **agent-codebase-archaeologist** — Routing target for codebase onboarding and domain investigation
- **agent-tech-detective** — Routing target for quick stack detection before deeper learning
- **walkthrough-planner** — Conditional: suggested to user for flow-based topics at slow-incremental pace (see Walkthrough-Planner Hook)

---

## Step 0: Identify Learning Scope

Before applying a strategy, determine the scope of what the user wants to learn. This narrows which docs, agents, and paths apply.

| Signal | Scope | What to route to |
|--------|-------|-----------------|
| "teach me X concept", "what is [term]", "how does [concept] work" | **Domain-specific** — a business or technical concept | `agent-concept-tutor` |
| "help me understand [repo/project]", "how does the codebase work" | **Project-specific** — the full codebase | Check for a `LEARNING-PATH.md` first; if present, use it. Otherwise: `codebase-onboarding-workflow` |
| "how does [feature] work end-to-end", "what happens when [action]" | **Cross-cutting** — spans domain + code | Domain doc first (if exists), then code trace |
| "I want to learn [project] properly", "onboard me to [repo]" | **Full platform** — structured curriculum | Check for a `LEARNING-PATH.md`; if absent, suggest `codebase-onboarding-workflow` |

**If scope is ambiguous**, ask: "Are you trying to understand the *concept* (what it means), the *codebase* (how it's implemented), or both?"

**How to find the right entry point for any project:**

1. Check if a `LEARNING-PATH.md` exists at the project's `documentation/` root → use it as the curriculum
2. Check if domain deep dives exist (`documentation/projects/{name}/domain/`) → jump directly to the relevant one
3. Check if a top-level doc exists (`README.md`, `DOMAIN.md`, `TECH-STACK.md`) → start there
4. If nothing exists → use `agent-tech-detective` → `agent-codebase-archaeologist --onboard`

---

## Step 1: Identify the Context

Infer from signals in the user's message:

| Signal | Context |
|--------|---------|
| "production is down", "urgent", "fix ASAP", stack trace/error present | 🔥 Urgent Bug |
| "just enough to continue", "quickly understand", "what is this X" | ⚡ Quick Concept |
| "I want to learn properly", "step by step", learning a tutorial/example app | 📚 Deep Learning |
| "new to this codebase", "just joined", "onboarding", large unfamiliar repo | 🤝 Onboarding |
| "business logic", "domain knowledge", "what does X mean in business terms" | 💼 Domain Knowledge |
| "guide me through building this", "walk me through the implementation", user has PRD + tech spec | 🛠️ Guided Build |
| "I want to learn [field/domain]", "how should I learn [skill]", "best way to get into [discipline]", "where do I start with [field]" | 🧑‍🏫 Domain Skill Acquisition |

**Disambiguation:** 🧑‍🏫 Domain Skill Acquisition applies only when the user wants to learn an *entire field or discipline* — not a specific concept, codebase, or project. Match this context last. If the signal could match another context (e.g. "I want to learn accounting" could also match 💼 Domain Knowledge), prefer the more specific context unless the user explicitly frames it as "getting into a field" or "learning a discipline from scratch."

**Routing after Step 1:**
- If context = 🧑‍🏫 Domain Skill Acquisition → proceed to **Step 1.5** before Step 2
- All other contexts → proceed directly to **Step 2**

---

## Step 1.5: Domain Calibration (Domain Skill Acquisition only)

Run this step only when context = 🧑‍🏫 Domain Skill Acquisition.

### Gate 1 — Vocabulary check (run first, before domain table)

Before applying any domain recommendation, verify the learner has enough vocabulary to interpret failure signals. Ask or infer:  

> "Can you name 3–5 core concepts or tools in this domain? If something went wrong in a project, would you know which part failed?"

- **YES** → apply domain table recommendation directly
- **NO** → prepend a structured vocabulary phase (1–2 weeks with a recommended resource) before any PF-first recommendation, regardless of what the domain table says

### Gate 2 — Learner level calibration

Ask or infer before applying the domain row:

> "Have you done anything in [domain] before, even informally?"

Use the answer to shift the recommendation:

| Experience level | Effect on domain recommendation |
|---|---|
| None / complete beginner | Apply domain table as-is |
| Some adjacent experience | Skip vocabulary phase; may compress structured phase |
| Experienced in a related field | Override to PF-first regardless of domain row |

### Domain Calibration Table

| Domain detected | Mode | Recommended approach |
|---|---|---|
| Full-stack web dev | Hybrid | 4–6 weeks structured fundamentals (e.g. Odin Project) → immediate real project with no guide. The structured phase exists to build vocabulary, not mastery. |
| AI engineering | PF-first (except math) | Build first; read theory only when a specific gap blocks you. Exception: linear algebra, probability, calculus — if model internals matter, structured math is irreplaceable. |
| Automation | Threshold-based | Simple/one-off → copy and tweak an existing script. Recurring pipeline running unattended >20 times → invest upfront in understanding error handling, retries, and state management. |
| System design | Interleaved | Read one well-documented design → attempt it from memory without looking → compare. Never passive read-only. Never pure struggle. |
| Accounting | Goal-dependent | Functional use (own business, investments) → PF with personal data first (Wave or QuickBooks for 2 weeks, then fill gaps). Credential or comprehensive coverage → structured textbook. |
| Embedded systems | Structured-first | Hardware failure cost is high (slow feedback, component damage). Study fundamentals before touching hardware. |
| Mobile development | Hybrid | 2–3 weeks on platform fundamentals (Swift/Kotlin basics, lifecycle) → build a real app. Platform APIs change frequently so staying close to real projects keeps knowledge current. |
| Data engineering | Threshold-based | One-off scripts → PF (copy and adapt). Production pipelines → invest in understanding idempotency, partitioning, and failure modes before building. |
| DevOps / Infrastructure | Structured-first for core, PF for tooling | Core concepts (networking, Linux, containers) → structured. Tooling (Terraform, CI/CD configs, Helm) → PF once core is solid. Sandbox environments lower the failure cost significantly. |
| General / unknown | Decision gate | Ask: (1) "Does this domain have fast feedback loops — can you try something and see if it works within minutes?" If YES → PF-first with vocabulary scaffolding. If NO → ask: (2) "Are mistakes costly (time, money, safety)?" If YES → structured-first. If NO → hybrid (1–2 weeks structured intro, then PF). |

**How to extend this table:** When adding a new domain, evaluate three factors: (1) feedback loop speed (fast = favors PF), (2) failure cost (high = favors structured), (3) domain stability (fast-moving = favors PF to stay current). These three factors determine the mode.

### Output from Step 1.5

After applying Gates 1–2 and the domain table, produce a learning mode recommendation:

| Mode | Meaning |
|---|---|
| PF-first | Present challenge/project first; provide theory only when learner hits a specific blocker |
| Structured-first | Teach concepts sequentially before any hands-on work |
| Hybrid | Short structured phase (define duration) → switch to PF |
| Interleaved | Alternating read-attempt-compare cycles |
| Threshold-based | PF below threshold; structured above it |
| Goal-dependent | Ask the user their goal before recommending |

Pass this mode to concept-tutor when routing. Concept-tutor should frame lessons and pacing to match the mode.

---

## Step 2: Apply the Strategy

| Context | Strategy | Pace | Layers to Focus | Agent + Flags |
|---------|----------|------|-----------------|---------------|
| 🔥 Urgent Bug | Targeted Slice (error path only) | Speed Read | ONLY where bug lives | `agent-debugger` |
| ⚡ Quick Concept | Horizontal (one concept) | Medium | Relevant layers only | `agent-concept-tutor --quick` |
| 📚 Deep Learning | Outside-In (UI → data) | Slow Incremental | All layers, systematically | Main session interactive |     
| 🤝 Onboarding | Vertical → Horizontal | Fast overview → Slow deep-dive | All layers, prioritized | `agent-tech-detective` → `agent-codebase-archaeologist --onboard` |
| 💼 Domain Knowledge | Inside-Out (domain first) | Slow for domain, Fast for technical | Domain + Business Logic only | `agent-codebase-archaeologist --domain` → `agent-concept-tutor` |
| 🛠️ Guided Build | Vertical Slice (per task-plan.md) | Slow Incremental | Layers per slice from task-plan.md | `guided-walkthrough-workflow` (concept-tutor → implementation-engineer per slice) |
| 🧑‍🏫 Domain Skill Acquisition | See Step 1.5 output | Varies by domain and learner level | N/A — not codebase-layer-based | `agent-concept-tutor` with learning mode passed from Step 1.5 |

---

## Step 3: Layer Isolation Rules

When applying Targeted Slice or layer-specific strategies, tell the agent which layers to focus on and which to ignore:

```
Bug in UI?              → Read: UI layer only        | Skim: API it calls          | Ignore: business logic, database
Bug in Business Logic?  → Read: specific service     | Skim: input/output          | Ignore: UI, other services
Bug in Database?        → Read: failing query        | Skim: data model            | Ignore: UI, business logic
Understanding auth?     → Read: Infra + Biz Logic    | Skim: entry points          | Ignore: UI details, DB schema
Understanding data flow?→ Read: API + Biz + Data     | Skim: integration points    | Ignore: UI, infrastructure
Understanding UI?       → Read: UI + State layers    | Skim: API it calls          | Ignore: backend, business logic
```

---

## Layer Taxonomy Reference

| Layer | Contains | Examples |
|-------|----------|----------|
| UI / Presentation | Components, pages, forms, views | React/Vue components, templates |
| API / Controller | REST endpoints, route handlers | Controllers, GraphQL resolvers |
| Business Logic | Services, use cases, workflows | AuthService, PaymentService |
| Domain / Model | Entities, value objects, domain rules | User, Order, Contract entities |
| Data Access | Repositories, DAOs, ORM | UserRepository, JDBC queries |
| Integration | External APIs, message queues | SAP BAPI calls, webhook handlers |
| Infrastructure | Auth, logging, caching, config | JWT handling, interceptors |

Not all codebases have all layers. Simple apps may combine several; complex systems may split further.

---

## Strategy Reference

| Strategy | WHAT to learn | Best for |
|----------|--------------|----------|
| Vertical Slice | One feature, ALL layers top-to-bottom | Understanding complete flows, fixing bugs |
| Horizontal Slice | ONE layer, ALL features | Becoming expert in a layer, pattern recognition |
| Outside-In | UI → API → Business Logic → Data | Frontend devs, concrete-first learners |
| Inside-Out | Domain → Business Logic → API → UI | Backend devs, complex business domains |
| Hybrid | Simple vertical → horizontal → complex vertical | Most real-world scenarios |
| Targeted Slice | ONLY the path relevant to your task | Time-critical debugging |

**Key principle:** Strategy (WHAT to learn) and Pace (HOW to learn) are independent — mix any combination.

---

## Pace Reference

| Pace | HOW to learn | Good for |
|------|-------------|---------|
| Fast / All-at-once | Complete overview, move on | Experienced devs, quick orientation |
| Slow / Incremental | Step-by-step, confirm each piece | Deep understanding, complex topics, beginners |
| Speed Read | Skim for specific info only | Production bugs, finding specific code |

---

## Routing Instructions for Main Session

When a user asks HOW to approach learning (not just "teach me X"):

1. Read this skill
2. Identify context using Step 1 signals
3. Present recommendation: strategy + pace + agent(s) with flags + layers to focus/ignore
4. Ask if they want to proceed or adjust

When routing to agents, always pass:
- Which strategy applies (e.g., "use Vertical Slice strategy")
- Which pace to use (e.g., "slow incremental — confirm understanding at each step")
- Which layers to focus on and which to ignore
- Time budget if the user mentioned urgency
- **Diagram guidance for concept-tutor:** Defer to concept-tutor's own Step 4 rules for diagram placement and format. Do NOT override with diagram-first or mandatory-diagram instructions. Concept-tutor decides whether an inline diagram is appropriate (3+ actors in sequence, single diagram, embedded mid-prose). If full ASCII walkthroughs are needed, the user invokes `step-visualization` explicitly.

## Step 4: Generate Pedagogical Plan
When the goal is to create a new knowledge file (`Deep Learning` or `Domain Knowledge` context), this skill must generate a structured pedagogical plan to guide the `agent-concept-tutor`.

**Output Format (to be passed to the tutor):**
```markdown
# Pedagogical Plan: [Concept Name]

**1. The "Why" (Problem Statement):**
[1-2 sentence explanation of the business problem this concept solves.]

**2. The Analogy:**
[A simple, concrete analogy to build intuition. e.g., "Think of it like a library's Dewey Decimal system..."]

**3. Key Terms to Define:**
- [Term 1]
- [Term 2]
- [Term 3]

**4. Example Scenario Focus:**
[A single sentence describing the key takeaway the example should illustrate. e.g., "The example must clearly show how a natural break-point is calculated from the base rent."]

**5. Tutor Execution Prompt:**
"You are agent-concept-tutor. Rewrite the provided raw notes for [Concept Name] into a clear, pedagogical knowledge file. Your response must strictly follow the `domain-knowledge` template. Your rewrite must incorporate the following pedagogical plan:
- Start with the 'Why': [Paste from Step 1]
- Introduce the core idea using this 'Analogy': [Paste from Step 2]
- Ensure these 'Key Terms' are clearly defined: [Paste from Step 3]
- Ensure your 'Example Scenario' successfully demonstrates this key takeaway: [Paste from Step 4]"
```

### Walkthrough-Planner Hook

When the strategy is slow-incremental (Deep Learning or Domain Knowledge pace) AND the topic involves 3+ actors in a sequenced flow, suggest a choice to the user before routing:

> "This topic has a multi-step flow. Would you like a structured walkthrough (walkthrough-planner builds a story map first) or a conversational lesson (concept-tutor directly)?"

- User picks **walkthrough** → invoke `walkthrough-planner` skill (Phases 1–3) → pass story map to concept-tutor as teaching structure
- User picks **lesson** → route to concept-tutor directly as normal
- Do NOT auto-route — let the user choose
- Do NOT invoke the planner for Quick Concept or Urgent Bug contexts — the planning overhead exceeds the benefit at those paces

---

## LEARNING-PATH.md Maintenance

A `LEARNING-PATH.md` is a living curriculum document that may exist at a project's `documentation/` root. It bridges multiple related projects or codebases into a single learning progression. It must be updated whenever new documentation is added to the project.

### When to update

| Trigger | What to update |
|---------|---------------|
| New domain deep dive added | Add to the appropriate tier; update task-oriented guides if relevant to a common task |
| New top-level doc added (e.g., new `FRONTEND.md`, `API-REFERENCE.md`) | Check which tier it belongs to and add it |
| Doc moved or renamed | Update all links in `LEARNING-PATH.md` |
| New cross-project terminology gap found | Add a row to the Terminology Mapping table (if one exists) |
| New task-oriented guide written | Add to the task guides section |

### Tier placement rules (generic)

Read the new doc first, then place it based on its nature:

| If the new doc covers... | Place in... |
|--------------------------|-------------|
| Foundational concepts a learner must know before anything else | Earliest tier (orientation/fundamentals) |
| Core flows, data paths, or domain workflows | Middle tier (core workflows) |
| Specific subsystems, config, security, APIs, or UI | Later tier (developer-ready / on-demand) |
| Edge cases, known bugs, or narrow situational topics | Defer/situational table — do not block learners with this |

### How to update (any agent or main session)

1. Read the `LEARNING-PATH.md` to understand its current tier structure
2. Read the new doc to understand its scope, prerequisites, and audience
3. Determine tier using the placement rules above
4. Add an entry with: document link, one-line "what you'll learn", prerequisite if it has one
5. Check if any existing task-oriented guide should now reference the new doc
6. Update the "Last Updated" line at the bottom of `LEARNING-PATH.md`

### Notebook sync rules

The notebook (`/c/workarea/notebook/`) maintains two separate representations of documentation:

| Content | Notebook location | How it gets there |
|---------|------------------|-------------------|
| Raw docs (`projects/`, `platform/`) | `40-references/{project}/projects/` and `40-references/{project}/_platform/` | `import-docs.py` — copies verbatim |
| Root-level `.md` files (`LEARNING-PATH.md`, `README.md`) | `40-references/{project}/` | `import-docs.py` — copies root-level `.md` files from `documentation/` |
| `LEARNING-PATH.md` (as active curriculum) | `30-learning-plans/{project}/` | note-taker — captured as a learning plan when a learning session begins |

`LEARNING-PATH.md` has **two notebook representations** that coexist and serve different purposes:
- `40-references/{project}/LEARNING-PATH.md` — verbatim reference copy (via `import-docs.py`), read-only
- `30-learning-plans/{project}/` — active learning notes taken while following the curriculum (via note-taker)

**After writing any new doc** (root-level, `projects/`, or `platform/`), the notebook reference copy is stale. Remind the user to re-sync:
```bash
python /c/workarea/notebook/import-docs.py {project-root} {project-name}
```