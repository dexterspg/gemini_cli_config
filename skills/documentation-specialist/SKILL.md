---
name: documentation-specialist
description: Use when writing, updating, or reviewing any project documentation file — README, INTEGRATION, DEPLOYMENT, API-REFERENCE, BUSINESS-CASE, TECH-STACK, FRONTEND, DATABASE, DOMAIN deep dives, diagrams, or platform-level docs. Invoke before any agent creates or edits a documentation file to ensure correct templates, folder structure, audience tone, and section completeness. Also triggers for: deciding which doc type to write, structuring domain deep dives, checking documentation completeness. When in doubt about any documentation task, use this skill.
---

# Documentation Specialist Skill

**Purpose:** Standard templates, conventions, and guidelines for writing professional project documentation in a microservice architecture.

**Scope:** Covers per-project docs (README, INTEGRATION, DEPLOYMENT, API-REFERENCE, BUSINESS-CASE, FRONTEND, TECH-STACK, DATABASE, DOMAIN), domain deep dives (`domain/`), diagrams (`diagrams/`), and platform-level docs (system overview, integration map, shared stack).

---

## How to Use This Skill

Produces **written documentation files** that serve as permanent reference material.

**Distinction from other agents:**
- `agent-concept-tutor` *explains verbally* in conversation (ephemeral, teaching-oriented)
- `documentation-specialist` *writes structured markdown files* for git (permanent, reference-oriented)
- Both can cover business case and concepts — the difference is the medium, not the topic

Output: Structured markdown files ready for git. See **Writing Standards** below for format rules.

**If you are editing this skill file:** apply these two rules before adding or changing anything:
- **Not project-specific** — no class names, file paths, or concepts that belong to a single codebase. Rules must apply to any tech stack and any project. If an example is needed, make it generic (e.g., `YourService`, `BaseRepository`) not a real class name.
- **Not redundant** — before adding a rule, check if it is already covered here or in a referenced template. A pointer to the template is always better than duplicating its content.

---

## Enforcement Rules (Read Before Doing Anything)

These rules are non-negotiable. Check them before creating any file or folder.

| Rule | Forbidden | Correct action |
|------|-----------|----------------|
| **No unauthorized root-level content** | Any file or folder under `documentation/` other than `platform/`, `projects/`, `README.md`, `LEARNING-PATH.md`, `DOC-INDEX.md` | Move to `platform/`, `projects/`, or outside `documentation/` entirely. `LEARNING-PATH.md` and `DOC-INDEX.md` are only written when their trigger conditions are met — see **Root Navigation Files** |
| **One codebase = one folder** | Creating a second `projects/{service}/` folder for a codebase that already has one — even under a different name, abbreviation, or alias | Before creating a folder, check `projects/README.md` first. If the codebase is already listed, use that folder regardless of what you would have named it |
| **Index registration is mandatory** | A `projects/{service}/` folder with no row in `projects/README.md` | Add the row before or immediately after creating the folder |

---

## Controlled Vocabulary (Reviewers: Check Here Before Flagging Any Term)

**This section is the normative source for all vocabulary values. Downstream tables in this skill may repeat these values for readability but must not introduce new ones.** A reviewer MUST cite the exact row from this table that authorizes or excludes a term before flagging it as non-standard. Values are case-sensitive as written. The `·` separator is display formatting, not part of the value.

### Tier Labels

| Category | Valid values |
|----------|-------------|
| **Service tiers** | `Minimal` · `Standard` · `Full` |
| **Framework / Library tiers** | `Framework-Minimal` · `Framework-Standard` · `Framework-Full` |

### Status Values (projects/README.md — Complete? column)

| Value | Meaning |
|-------|---------|
| `✓` | All files required by the project's current tier exist (see **Documentation Tiers**) |
| `partial` | One or more files required by the project's current tier are missing (see **Documentation Tiers**) |

### Documentation Status Values (per-project README.md status table)

| Value | Meaning |
|-------|---------|
| `✓` | File exists |
| `— missing` | Required by tier but not yet written (em-dash + space + "missing") |
| `n/a` | Not applicable to this project type |
| `planned` | Intentionally deferred — known gap, not an oversight |

### Document Types (projects/README.md — Type column)

`Service` · `Framework` · `Library`

---

## Documentation Root Location

**Decision procedure — run in this order before creating any folder or file:**
1. Check project `GEMINI.md` and personal memory for a docs-location entry — if found, use it (written overrides win over everything, including verbal instructions in the current session)
2. Check the current session for an explicit user instruction — phrases like "separate docs folder", "docs outside the project", "dedicated docs folder", "put docs in a separate repo" trigger the separate-folder path
3. If neither applies, use the default (in-repo)
4. If the project is new and no override exists, state the chosen root and confirm with the user before creating the folder      

**Default:** Documentation lives inside the project repo at `{project-root}/documentation/`.

**Separate docs folder:** Use `/c/workarea/{project-name}-docs/` (this path assumes the user's Windows/bash workarea; check memory if unsure). The folder structure inside is identical — `projects/`, `platform/`, etc. — just rooted there instead. If that path already exists with unrelated content, stop and confirm with the user before writing.

**Per-project override:** If the project's `GEMINI.md` or personal memory specifies a docs location, use it exactly. Written overrides take precedence over both the default and any verbal instruction in the session.

**Rules still apply:** Enforcement Rules and Folder Structure below apply to whichever root is selected — the root changes location only, not structure or rules.

**Examples:**
- User says nothing → use `{project-root}/documentation/` → state it before creating
- User says "put docs in a separate folder" → use `/c/workarea/my-service-docs/` → confirm before creating

---

## Audience Per Document

Every document has a primary audience. **Match the writing voice to the reader:**

| Document | Primary Audience | Writing Voice |
|----------|-----------------|---------------|
| README.md | Developers + new team members | Technical but approachable — assume they know the language but not this project |
| INTEGRATION.md | Developers changing APIs or debugging cross-service issues | Precise — every row is a contract that can break |
| DEPLOYMENT.md | DevOps + developers running locally | Dense, copy-paste ready — resource limits, env vars, job configs |     
| API-REFERENCE.md | Developers consuming the API | Copy-paste ready, zero ambiguity — they should never need to read source code |
| FRONTEND.md | Frontend developers | Component-oriented — routes, state, API bindings |
| TECH-STACK.md | Developers + DevOps | Dense, reference-oriented, version-exact — no fluff |
| BUSINESS-CASE.md | Product managers, executives, non-technical stakeholders | Zero jargon, problem-first, value-focused — lead with the business pain |
| DATABASE.md | Developers querying, joining, or debugging data | Relationships first, business columns only — skip what's obvious from naming |
| DOMAIN.md | Developers making changes to business logic | Mental model first — entity relationships, workflows, state machines, then link to deep dives |
| domain/*.md | Developers deep in a specific domain area | Must serve four purposes: (1) **code logic** — how the implementation works, patterns, snippets, call chains; (2) **business logic** — why it does what it does, rules, edge cases; (3) **troubleshooting** — common failure modes, log patterns; (4) **future proofing** — known limitations, planned refactors |

---

## Documentation Tiers (Check Before Starting Any Project)

Documentation requirements scale with project complexity. Determine the tier before writing.

### Service Tier (Backend Services)

| Document | Minimal | Standard | Full |
|----------|---------|----------|------|
| README.md | ✓ | ✓ | ✓ |
| INTEGRATION.md | — | ✓ | ✓ |
| DEPLOYMENT.md | — | ✓ | ✓ |
| API-REFERENCE.md | — | ✓ | ✓ |
| BUSINESS-CASE.md | — | — | ✓ |
| TECH-STACK.md | — | — | ✓ |
| DATABASE.md | — | — | ✓ |
| DOMAIN.md | — | — | ✓ |

### Framework / Library Tier (Shared Code)

| Document | Framework-Minimal | Framework-Standard | Framework-Full |
|----------|-------------------|-------------------|----------------|
| README.md | ✓ | ✓ | ✓ |
| INTEGRATION.md | — | ✓ | ✓ |
| API-REFERENCE.md | — | ✓ | ✓ |
| TECH-STACK.md | — | — | ✓ |
| DOMAIN.md | — | — | ✓ |

---

## Writing Standards (Enforcement Rules for Formatting)

Consistency is the difference between documentation and a collection of notes.

### Formatting Rules

| Element | Rule | Example |
|---------|------|---------|
| **Headings** | Use sentence case. Max 3 levels (H1, H2, H3) for README. Max 4 levels for domain deep dives | `## Installation and setup` |
| **Code snippets** | Always include the language tag for syntax highlighting | ` ```bash ` |
| **File paths** | Use backticks. Use relative paths from the project root | `` `src/main.py` `` |
| **Links** | Use relative links to other markdown files in the same repo | `[Integration guide](INTEGRATION.md)` |
| **Emphasis** | Use **bold** for importance, *italics* for emphasis or terms. Use sparingly | **Important:** save before exiting |
| **Lists** | Use consistent bullet points (`-`). Use numbered lists for sequential steps | 1. Step one<br>2. Step two |
| **Tables** | Use for comparisons, configs, and mappings. Use pipes (`|`) and dashes (`-`) | `| Key | Value |` |

### Tone & Style Rules

| Principle | Rule | Correct action |
|-----------|------|----------------|
| **Problem-first** | Lead with the "why" or the problem being solved, not the implementation details | "This service handles X to prevent Y" |
| **Active voice** | Use active voice and direct addresses | "Click the button" not "The button should be clicked" |
| **Zero fluff** | Remove phrases like "it is important to note that", "please ensure you", "simply" | Just state the fact or instruction |
| **Exactness** | Use exact version numbers, environment variables, and field names | `Python 3.11.4` not `Python 3` |

---

## Folder Structure (Enforced)

Documentation is organized in a strict hierarchy. **Do not create files or folders outside this structure.**

```
documentation/
├── projects/
│   ├── README.md               <-- Global Project Index (Mandatory)
│   ├── {service-name}/         <-- Folder for a single codebase
│   │   ├── README.md           <-- Project documentation entry point
│   │   ├── INTEGRATION.md      <-- API/Event contracts
│   │   ├── DEPLOYMENT.md       <-- Env vars, secrets, job configs
│   │   ├── API-REFERENCE.md    <-- Endpoint reference (replaces Swagger)
│   │   ├── BUSINESS-CASE.md    <-- Problem-first stakeholder doc
│   │   ├── TECH-STACK.md       <-- Versions, libs, architecture decisions
│   │   ├── DATABASE.md         <-- Relationships, entity maps
│   │   ├── DOMAIN.md           <-- The mental model (entry point for logic)
│   │   └── domain/             <-- Domain deep dives (1 file per domain area)
│   │       ├── {area-1}.md
│   │       └── {area-2}.md
│   └── diagrams/               <-- Shared diagrams (Mermaid, Draw.io, Excalidraw)
│       └── images/             <-- Exported PNG/SVG files
└── platform/                   <-- Non-codebase platform documentation
    ├── system-overview.md
    └── integration-map.md
```

---

## Global Project Index (`projects/README.md`)

This file is the single source of truth for all projects in the workspace. **It must be updated every time a project folder is created or its tier changes.**

**Mandatory Columns:**
- **Name:** Clickable link to the project's folder `[Service Name]({service-name}/README.md)`
- **Type:** `Service`, `Framework`, or `Library`
- **Tier:** `Minimal`, `Standard`, or `Full` (or Framework equivalents)
- **Complete?:** `✓` if all files required by the tier exist; `partial` if any are missing
- **Description:** 1-sentence business value statement

---

## Per-Project Entry Point (`projects/{service}/README.md`)

The entry point for a single project. **It must include a Status Table at the top.**

### Status Table

| Document | Status |
|----------|--------|
| INTEGRATION.md | `✓` |
| DEPLOYMENT.md | `— missing` |
| ... | ... |

**Required Sections (in order):**
1. **Title:** `# {Service Name}`
2. **Status Table:** (see above)
3. **Overview:** 1-2 paragraphs on what it does and why it exists.
4. **Getting Started:** Quickest path to a running local environment.
5. **Key Components:** Bullet list of the 3-5 most important files/directories.
6. **Related Projects:** Links to upstream/downstream services in the workspace.

---

## Domain Deep Dives (`domain/*.md`)

These are high-density technical documents focused on a specific area of business logic. **Trigger:** write a deep dive when a single domain area (e.g., "activation workflow", "lease conflict resolution") becomes too complex for `DOMAIN.md`.

**Must serve four purposes:**
1. **Code logic** — how the implementation works, patterns, snippets, call chains.
2. **Business logic** — why it does what it does, rules, edge cases.
3. **Troubleshooting** — common failure modes, log patterns.
4. **Future proofing** — known limitations, planned refactors.

---

## Root Navigation Files

Two files are written only when their conditions are met. **Do not create these manually.**

### `LEARNING-PATH.md`
**Trigger:** When the workspace reaches 5+ projects.
**Purpose:** A curriculum for new developers to learn the platform. Includes "Read order", "First tasks", and "Key concept milestones".

### `DOC-INDEX.md`
**Trigger:** When the workspace reaches 15+ documentation files (excluding READMEs).
**Purpose:** A tag-based or theme-based index of all platform documentation (e.g., "All security docs", "All integration maps").

---

## Review Checklist (For Reviewers and Writers)

Run this checklist before finalizing any document.

- [ ] **Audience match:** is the tone right for the primary reader?
- [ ] **Template match:** does it follow the required sections and order?
- [ ] **Formatting:** language tags, sentence case, relative links, exact versions?
- [ ] **Zero fluff:** no "it is important to note", "simply", or "please"?
- [ ] **Paths & Names:** are all file paths and column names exact and backticked?
- [ ] **Index update:** is the row added/updated in `projects/README.md`?
- [ ] **Status table:** is the per-project status table current?
- [ ] **Business value:** is the "why" clear for non-technical readers?
- [ ] **Contract accuracy:** (for INTEGRATION.md) do the event/API definitions match current code?

---

## Platform-Level Documentation Mapping

The platform folder contains documentation that spans multiple projects.

| File | Primary Owner | Purpose |
|------|---------------|---------|
| platform/README.md | Parent (doc skill) | Navigation for the platform folder |
| platform/system-overview.md | agent-system-architect | High-level topology and platform goals |
| platform/INTEGRATION-MAP.md | agent-system-architect | Matrix of every project and its inbound/outbound dependencies |
| platform/INTEGRATION-PATTERNS.md | agent-system-architect | Standardized protocols (REST, Kafka, etc.) and client libraries |
| platform/SECURITY-MODEL.md | agent-system-architect | Platform-wide auth, TLS, and PII standards |
| platform/DEPLOYMENT-MAP.md | agent-system-architect --infra | Onboarding requires cross-service setup steps |
| decisions/ADR-*.md | agent-system-architect | A specific architecture decision needs to be recorded |
| diagrams/ | agent-codebase-archaeologist | Any platform-level diagram |
| domain-concepts/{concept}.md | agent-codebase-archaeologist --domain (formal) · agent-concept-tutor (draft) | General concept applies to 2+ projects |

**Rule:** Always spawn the assigned agent above when writing any platform file — never write directly in the main session.     

### Companion Doc Pattern

When a domain area serves two distinct audiences — one reading to understand, one reading to change — split it into **two consecutive numbered docs** rather than one long file.

| Doc role | Audience | Voice |
|----------|----------|-------|
| **Architecture reference** (NN) | Developers understanding the system | Comprehensive — every rule, every layer, every edge case |
| **Operations guide** (NN+1) | Developers making changes or customizations | Task-oriented — step-by-step workflows, config schemas, end-to-end walkthroughs |

**Decision checklist — split when ALL of these are true:**

1. **Two distinct reader goals exist** — "understand how X works" is a different task from "change how X behaves"
2. **Customization touches 3+ files OR requires a fixed sequence of 4+ steps** — if you can express the change in fewer steps or fewer files, it fits inside one doc as an on-demand `End-to-End Walkthrough` section
3. **The operations content will be consulted repeatedly** — a developer making routine changes will return to it more than once, making it worth maintaining as a standalone reference

If any of these are false, keep it as one doc. Use the on-demand `End-to-End Walkthrough` and `Config File Schemas` sections within that single doc instead.

**Naming the split:**
- Architecture doc: name describes the system — `NN-[area]-model.md`, `NN-[area]-architecture.md`, or just `NN-[area].md`      
- Operations doc: name describes the action — `NN+1-[area]-customization.md`, `NN+1-[area]-configuration.md`, `NN+1-[area]-guide.md`

**Deduplication rule between companion docs:**

Canonical content lives in the **architecture doc** only. The operations doc uses reference notes instead of repeating it:       

```markdown
> See [NN-topic-name.md — Section](./NN-topic-name.md#section) for framework-level rules. Below: [operation-specific subset] only.
```

Apply this to: Business Rules, Observability, Common Pitfalls — any section where the framework rules are in the architecture doc and the operations doc only adds a subset.

**Prerequisite chain:** Operations doc always lists the architecture doc as a prerequisite in `00-overview.md`.

### Observability Section Pattern

Every `domain/*.md` deep dive has an Observability section. How deep it goes depends on the domain area — use graduated enrichment, not a fixed template.

**Baseline (required for all domain docs):**
- Signal table: log messages, error classes, stack trace signatures that identify this area when it breaks
- "Check first" checklist: 2–5 items to verify immediately when the area misbehaves

**Add a diagnostic decision tree** when the domain has **3 or more distinct failure paths** that start from different user-reported symptoms (e.g., "can't see X at all" vs "can see X but can't do Y" vs "action fails after clicking"). A decision tree is not needed when the only failure mode is one thing breaking in one way.

**Add a user-facing symptoms table** when **user-reported symptoms don't map obviously to technical causes** — i.e., when a support analyst cannot guess the technical root cause from what the user describes. Skip it when symptoms are self-explanatory (e.g., "404 error on endpoint X" maps obviously to a missing route).

**Add cleanup/remediation guidance** when the domain has **DB side effects that can leave orphaned or inconsistent records** — include the identification query, cascade safety check, and ordered delete. This is not needed for read-only domains or domains where failures are fully transactional (auto-rolled-back).

**Content boundary with `issues/`:**

The Observability section is for **reusable, pattern-level content** — things that apply every time this area breaks. The `issues/` folder is for **instance-level content** — what happened on one specific ticket. Never cross the line:

| Belongs in domain Observability | Belongs in `issues/{ticket}/` only |
|---|---|
| Reusable diagnostic SQL (works for any future occurrence) | SQL with specific object IDs, timestamps, customer names |
| Log search strings and stack trace signatures | Log excerpts with specific timestamps or user sessions |
| Decision tree for any role/config combination | Steps that only apply to one customer's environment |
| Cleanup query template with placeholders | Confirmed orphan object IDs from one incident |

### Multi-Project Ownership

When documentation involves code from more than one project, apply the decision tree in order:

#### Step 1 — Is one project a framework/library and the other an application?

| Code location | App customization? | Document in |
|--------------|-------------------|-------------|
| Lives in framework module | No | Framework's `domain/` |
| Lives in framework module | Yes — app overrides or wires it | App's `domain/` |
| Lives in app module | — | App's `domain/` |

**Decision test:**
1. Where does the code live? → framework module = framework docs, app module = app docs
2. Does the app add project-specific wiring? → if yes, document in the app even if the base code is in the framework

**Examples:**
- A framework's HTTP dispatch mechanism with no app-specific overrides → document in the framework's `domain/`
- A framework's security model that the app wires to its own user/role entities → document in the app's `domain/` (app-specific wiring is the content)
- A Spring Boot auto-configuration class used as-is → Spring docs cover it; don't duplicate. If the app customizes the bean, document the customization in the app's `domain/`

**Cross-reference rule:** When the app doc covers framework behavior for app-specific reasons, add a note pointing back to the framework's doc for the canonical explanation.

---

#### Step 2 — Are both projects application-layer peers (no framework/app split)?

Ask: **does one project call or depend on the other?**

| Relationship | Where to document |
|---|---|
| Project A calls Project B (caller/consumer) | Document from **Project A's perspective** in A's `domain/`. Document from **Project B's perspective** in B's `domain/`. Each covers its own side; cross-reference the other. |
| Both projects contribute equally to a shared concept — neither is clearly the caller | Document in **`platform/`** as a cross-project concern. Each project's `domain/` has a stub entry pointing to `platform/`. |

**Decision test:**
1. Can you say "Project A uses Project B" or "Project A triggers Project B"? → caller/consumer split — each project documents its own side
2. Is the concept owned equally by both with no clear primary? → platform-level doc

**Examples:**
- `order-service` calls `payment-service` to process a charge → `order-service` documents the outbound call in its `domain/`, `payment-service` documents the inbound handler in its `domain/`; both cross-reference each other
- `api-gateway` and `auth-service` both implement halves of a shared token contract → document the contract in `platform/`, each project's `domain/` stubs point there
- An app's request handler wired into a shared framework's dispatcher → Step 1 applies (app wires into framework), not Step 2  

**Transitive dependency boundary:** When documenting Project A's integrations, only document the direct caller-to-target relationship. If A calls B, and B internally calls C, the B-to-C relationship belongs in **B's** documentation, not A's. A's docs may *mention* that B calls C (one sentence with a cross-reference link to B's docs) but must not document B-to-C's protocol, endpoints, or contract details.

**Cross-reference rule:** Every project-level doc that covers a cross-project flow must have an explicit "Related" entry pointing to the other project's doc or the platform doc.

**Stub format** (for project `domain/` entries that point to platform):
```markdown
## [Topic Name]

> This concept spans multiple projects. Full documentation: [platform/TOPIC.md](../../platform/TOPIC.md)

[1-2 sentence summary of this project's role in the shared concept.]
```

### Other Files

| File | Written By |
|------|-----------|
| projects/README.md (index) | Parent (doc skill) |
| issues/investigation.md | agent-debugger |

**Rule:** Each agent reads the relevant template from `templates/` before writing. The skill provides format/audience/conventions — the agent provides the content from its analysis.

### Root Navigation Files

Two optional files are allowed at the `documentation/` root. **Never write these proactively.** Only write when the specific trigger condition is met.

| File | Trigger | Agent | What it contains |
|------|---------|-------|-----------------|
| `LEARNING-PATH.md` | User explicitly requests an onboarding path or reading order that spans multiple projects (2+ documented) | agent-codebase-archaeologist --onboard | Ordered reading sequence with a one-line rationale for each doc — links only, no duplicated content |
| `DOC-INDEX.md` | User needs to navigate docs by topic/concern rather than by service, AND 3+ projects are documented | Parent (doc skill) | Topic-grouped cross-project index (e.g., "Security", "Data Flow", "Deployment") — links into existing docs, no new content |

**Decision rule:**
- "Help me learn this codebase" / "What order should I read the docs" / "Onboard me" → `LEARNING-PATH.md`
- "Where are all the security docs" / "Give me a topic-based index" → `DOC-INDEX.md`
- Neither trigger met → do not create either file; `projects/README.md` and `platform/` are sufficient

**Content rules:**
- Both files are navigation-only — they link to existing docs, never duplicate content
- Update both whenever a new project or major deep dive is added
- `LEARNING-PATH.md` is ordered (numbered steps); `DOC-INDEX.md` is grouped by topic (not ordered)

---

## Diagrams

Every project gets a `diagrams/` subfolder. Diagrams are first-class documentation, not afterthoughts.

**Preferred format:** ASCII box diagrams in fenced code blocks — renders in any editor, GitHub, GitLab, Gemini CLI, IntelliJ, and plain text viewers with no renderer required.
**Optional:** Mermaid syntax for diagrams that benefit from auto-layout (large ERDs, complex graphs). Never use Mermaid as the sole representation — always include an ASCII version or ensure the audience has a renderer.

### Diagram File Format

Every file in `diagrams/` follows this structure:

````markdown
# [Diagram Title]

> Referenced from: [which documents link here]

```
[ASCII diagram content]
```

## What This Shows
1-3 sentences explaining what to look at and what the key paths are.
````

If a Mermaid version is also provided, place it after the ASCII block under a `### Mermaid Source` heading.

### Rules

- One diagram per file, one concern per diagram — don't mix data flow and deployment topology
- Label every arrow (what data flows, what protocol)
- Keep diagrams to 10 or fewer boxes — split into multiple diagrams if larger
- **Dual placement:** every diagram lives as a canonical file in `diagrams/` AND is embedded inline (mermaid) where it's referenced. The `diagrams/` file is the source of truth; inline copies are for convenience. When a diagram changes, update the `diagrams/` file first, then copy the updated mermaid block to every inline reference
- Every deep dive file (`domain/NN-*.md`) must include at least one diagram
- DOMAIN.md must include at minimum: entity model diagram + one state machine or workflow diagram
- **Multi-mode state machines:** When a state machine has distinct modes (e.g., feature flag ON/OFF, accounting enabled/disabled), DOMAIN.md must show only the simplest path, labelled `> Simplified — [mode]. See [deep dive] for the full state machine.` Never show a hybrid that silently misrepresents both modes. The full state machine for each mode belongs in the relevant `domain/NN-*.md` deep dive.

### Diagram Type Selection Guide

Choose the diagram type based on the question it answers:

| Type | Question it answers | Primary doc |
|------|---------------------|-------------|
| **Topology / Architecture** | What services exist, how they connect, which are HTTP vs in-process | README, INTEGRATION |      
| **C4 — Context (L1)** | Who uses the system, what external systems does it touch | README, ARCHITECTURE |
| **C4 — Container (L2)** | What processes/services run, what is embedded vs separate | ARCHITECTURE, DEPLOYMENT |
| **C4 — Component (L3)** | What classes/modules are inside a container | DOMAIN.md, domain deep dives |
| **C4 — Code (L4)** | Methods, fields, class relationships for a specific component | domain deep dives |
| **Sequence** | How a request flows step by step, message ordering, who calls who | DOMAIN.md, API-REFERENCE |
| **State machine** | All states a thing can be in, transitions, triggers, guards | DOMAIN.md, domain deep dives |
| **Entity / ERD** | Data model, table relationships, foreign keys | DATABASE.md, DOMAIN.md |
| **Service mesh / Infra overlay** | Sidecars, mesh layer, observability, TLS, service discovery | DEPLOYMENT |
| **Event flow** | Topics, publishers, consumers, event payloads | INTEGRATION, domain deep dives |
| **Pattern comparison** | Side-by-side contrast of two approaches (e.g. orchestration vs choreography) | DOMAIN.md, BUSINESS-CASE |

**Rules of thumb:**
- Start with Topology — get oriented before going deep
- Use C4 levels as zoom: L1 for README, L2 for ARCHITECTURE, L3–L4 for domain deep dives
- Sequence diagrams belong wherever a specific flow is described — one diagram per flow, not one mega-diagram
- State machines are mandatory for any entity with lifecycle states (lease, contract, posting)
- Pattern comparison diagrams belong in DOMAIN.md when two valid approaches exist and readers may confuse them

### Minimum Diagrams by Tier

| Tier | Required diagrams |
|------|------------------|
| **Minimal** | 1 — Topology or C4 L2 (what exists and how it connects) |
| **Standard** | Topology + C4 L2 + Sequence (happy path) + 1 per deep dive |
| **Full** | Topology + C4 L1–L3 + Sequence (happy + error paths) + State machine(s) + Entity/ERD + 1 per deep dive |

### Where Diagrams Live

| Scope | Location |
|-------|----------|
| Per-project | `documentation/projects/{service}/diagrams/` |
| Platform-level | `documentation/platform/diagrams/` |

---

## Writing Standards

| Guideline | Detail |
|-----------|--------|
| **Tables for structured data** | Dependencies, endpoints, configs, metrics — anything with columns |
| **Prose for context and persuasion** | Problem statements, business case, strategic importance |
| **Code examples, not descriptions** | Show the JSON body, the bash command, the YAML config |
| **Links, not duplication** | Link to related docs instead of rewriting the same content |
| **"Last Updated" with change note** | `YYYY-MM-DD — Added auth endpoints` — always at the **bottom** of the file, never the top |
| **One file = one topic** | Don't make README 20 pages; split into INTEGRATION, DEPLOYMENT, etc. |
| **Highlight the 20%** | Show what matters most first; deep dives in separate files |
| **Document what IS, not what might be** | No roadmaps, no "we plan to add..." |
| **No internal debates** | Use git history or `decisions/` ADR files for that |
| **Implementation facts over domain theory** | Document what the code produces, not why the industry standard or domain framework requires it. "This code sets flag X which triggers downstream process Y" belongs in a deep dive. Concept explanations and domain background belong in concept-tutor. Every claim in a deep dive must be traceable to a specific class, method, or config. |     
| **No credentials in docs** | Replace any real credentials (usernames, passwords, tokens, API keys) with `<placeholder>`. Add a one-line note pointing to where the actual value is stored (env file, secrets manager, team vault). Applies to all sections including code snippets, script examples, and Data Contracts. |

---

## What NOT to Output

- Tutorials or step-by-step learning guides — that's concept-tutor's domain. Docs provide *reference*, not *lessons*.

---

## When Documentation Changes

### Integration Changes

**Pre-write verification:** Before writing any INTEGRATION.md or integration-related domain deep dive, read `platform/INTEGRATION-MAP.md` and `platform/INTEGRATION-PATTERNS.md` to confirm the protocol, client library, and pattern for every integration you plan to document. If INTEGRATION-MAP.md does not have a row for this integration, add one first — the platform map is the canonical source.

If a service gains a new dependency, endpoint, or integration:
1. Update the project's INTEGRATION.md (new outbound/inbound row)
2. Update the TARGET project's INTEGRATION.md (new consumer row)
3. Update `platform/INTEGRATION-MAP.md` (new row in the matrix)
4. If a new integration pattern is introduced, update `platform/INTEGRATION-PATTERNS.md`

### Platform File Registration
If a new file is added to `documentation/platform/` that is not listed in this skill's folder structure or platform file table, update this skill to register it before the next documentation generation run.

### Business Logic Changes
If a workflow, business rule, or state machine changes:
1. Update DOMAIN.md (affected workflow, rule table, or state machine)
2. Update the relevant `domain/NN-*.md` deep dive (if one exists for that area)
3. Update affected `diagrams/` files
4. Update the `Last Updated` line on every changed file

### Domain Deep Dive Ordering

When deciding the number (NN) to assign a new deep dive, order by learning dependency — not by importance or frequency of change:

| Position | What goes here | Signals |
|----------|---------------|---------|
| **First (01–03)** | Foundational patterns every developer must understand before any other code makes sense | "This pattern appears in every service / every entity / every workflow" |
| **Middle** | Core business workflows and domain flows | "This is what the service primarily does" |
| **Later** | Specific subsystems, integration details, edge cases | "A developer only needs this when working on [specific area]" |

**Decision rule:** Ask — "Can a developer understand deep dive N+1 without reading deep dive N?" If no, N comes first. If yes, order by business centrality (core flows before edge cases).

**Framework projects:** the first deep dive must be the extension point or base pattern that consuming services override — because that is what every application developer will look for first.

For **Framework-Standard and above**, deep dives must collectively cover every extension point category the framework provides. A framework that passes the file-count check but leaves a category undocumented has a silent gap. Omit a category only if the framework genuinely does not provide that layer:

- **CRUD lifecycle hooks** — the create/update/delete sequence that consuming services override (template methods, callbacks, interceptors)
- **Data access patterns** — repository base contract, how consuming services construct queries (specification pattern, query builder, ORM filter hooks)
- **State machine / workflow** — if provided: state/event/transition contracts and the auto-transition mechanism
- **Security / auth model** — if provided: authentication filter hooks, row-level security clauses, authorization interceptors that consuming services inherit
- **Supporting utilities** — code generation, mapping conventions, error handling contracts, annotation processors — anything consuming services depend on implicitly

### New Domain Area Discovered
If investigation or development reveals a domain area not yet documented:
1. Apply the ordering rule above to assign the right NN number
2. Create new `domain/NN-topic.md` using the deep dive template
3. Add row to DOMAIN.md "Deep Dives" table
4. Add row to `domain/00-overview.md`
5. Create supporting diagrams in `diagrams/`

### Domain Area Removed or Merged
If a deep dive is deleted or absorbed into another file:
1. Remove the row from `domain/00-overview.md`
2. Remove the row from DOMAIN.md "Deep Dives" table
3. Remove or update cross-references in sibling deep dives that linked to it
4. Remove the canonical diagram file(s) from `diagrams/` if they are not referenced elsewhere
5. Do **not** renumber surviving deep dives — gaps in numbering are acceptable and prevent broken references
6. If the content was merged into another deep dive, do not delete the row from `domain/00-overview.md` — replace it with a redirect note: `NN — [topic] merged into [MM-topic.md](./MM-topic.md)`

### Tier Promotion

Documentation is written incrementally. A project does not jump from Minimal to Full in one step — it advances one file at a time, in priority order. The tier label and `Complete?` column in `projects/README.md` only advance when ALL required files for the next tier exist.

**Rule — when to update the tier label:**
- A file from a higher tier can be written at any point; update the Documentation Status table in that project's README.md after each new file is added
- The `Tier` and `Complete?` columns in `projects/README.md` only change when the project satisfies ALL required files for the new tier — not before

**Priority order — Minimal → Standard (Service):**

Write in this order. Each file unlocks more developer productivity than the next:

| Step | File | Why first |
|------|------|-----------|
| 1 | INTEGRATION.md | Shows who talks to whom — most cross-service developers need this first |
| 2 | DEPLOYMENT.md | Enables local setup and DevOps configuration |
| 3 | domain/ deep dives | Add as domain areas are investigated or bugs are fixed |

**Priority order — Standard → Full (Service):**

| Step | File | Why this order |
|------|------|----------------|
| 1 | API-REFERENCE.md | External consumers need this before any other Full-tier doc |
| 2 | DATABASE.md | Entity relationships block developers making schema changes |
| 3 | TECH-STACK.md | Version reference — needed for upgrades and debugging |
| 4 | FRONTEND.md | UI developers need this, but less urgent than backend consumers |
| 5 | BUSINESS-CASE.md | Stakeholder-oriented — useful but not developer-critical |

**Priority order — Framework-Minimal → Framework-Standard:**

| Step | File | Why first |
|------|------|-----------|
| 1 | DOMAIN.md | Navigator — without this, deep dives are unnavigable |
| 2 | domain/ deep dives | Start with the most-used extension points and patterns |
| 3 | diagrams/ | Add one diagram per deep dive |

**After each file is written:**
1. Add or update the row in the project README.md Documentation Status table (change `— missing` to `✓`)
2. If the tier is now fully satisfied → update `Tier` column and `Complete?` → `✓` in `projects/README.md`
3. If the tier is not yet satisfied → leave `Tier` and `Complete?` unchanged; `partial` stays until the tier is complete       

### Stale Documentation
If code has changed but documentation hasn't:
- Flag stale sections with `[NEEDS VERIFICATION — code may have changed since YYYY-MM-DD]`
- Never silently leave stale docs — a wrong doc is worse than no doc

### DEPLOYMENT.md — Section Ownership

DEPLOYMENT.md has two distinct content types that require different agents. **agent-system-architect --infra is the primary owner and coordinator.** The archaeologist contributes one section only.

| Section | Owner | Why |
|---------|-------|-----|
| Container | agent-system-architect --infra | Sourced from Dockerfile and deployment config — infra domain |
| Resource Limits | agent-system-architect --infra | Sourced from deployment config (K8s manifests, docker-compose, etc.) — infra domain |
| Managed Services | agent-system-architect --infra | Sourced from deployment config — infra domain |
| Kafka / Message Queue Jobs | agent-system-architect --infra | Sourced from deployment config — infra domain |
| Cron Jobs | agent-system-architect --infra | Sourced from deployment config — infra domain |
| Environment Variables | agent-system-architect --infra | Sourced from .env / application config files — infra domain |       
| Startup Dependencies | agent-system-architect --infra | Sourced from docker-compose.yml or orchestration config — infra domain |
| APIs Exposed | agent-system-architect --infra | Sourced from deployment / API gateway config — infra domain |
| **Security + Auth Request Flow** | **agent-codebase-archaeologist** | Requires tracing filter/interceptor/security classes in source code — code reading domain |

**Handoff sequence:**
1. agent-system-architect --infra writes all infrastructure sections → delivers a complete DEPLOYMENT.md with the Security section left as a placeholder
2. agent-codebase-archaeologist reads the partially written DEPLOYMENT.md + traces the auth filter chain in source → fills in the Security and Auth Request Flow sections
3. The final file has a single `Last Updated` line — do not write separate timestamps per section

**When there is no Security section to write** (e.g., a framework JAR with no HTTP layer): agent-system-architect --infra writes the complete file; no handoff needed.

### Domain Deep Dive — Mandatory Source Verification

**Hard rule — no inferred or teaching-derived values.** Any agent writing a `domain/NN-*.md` file MUST verify the following fact categories against authoritative source before writing. If a source cannot be confirmed, mark the field `[NEEDS VERIFICATION — read {filename} to confirm]`. Do NOT present inferred or teaching-derived values as fact.

| Fact category | Must be sourced from |
|---|---|
| Port numbers | `docker-compose.yml`, `application.properties`, service integration docs, or deployment config — not from memory or teaching content |
| URL paths and proxy routes | Actual route config, servlet/handler registration code, or INTEGRATION.md — not from concept-tutor output |
| Primary API / class usage patterns | Actual source code or existing canonical docs — confirm which class/method is primary vs. secondary before stating it |
| Class and method names | Source code — exact names, exact package paths |
| Behavior descriptions ("X triggers Y") | Traceable to a specific class, method, or config file — not inferred from domain theory |
| External system contracts (BAPI names, callback paths, response shapes) | INTEGRATION.md, source code, or SAP/external system knowledge base |
| Communication protocols (REST, Kafka, embedded JAR, webhook callback, JMS) | `platform/INTEGRATION-MAP.md` Service Communication Matrix, or source code client type (Retrofit = REST, `@KafkaListener` = Kafka, Maven dependency with no HTTP = embedded JAR) — never inferred from general architectural knowledge |
| Prose descriptions of parameter behavior | Must match the code snippet in the same section. If a parameter description (e.g., "false = do not drop") and nearby prose (e.g., "indices are recreated fresh") appear contradictory, mark both with `[NEEDS VERIFICATION — prose and code appear contradictory: confirm behavior of <param> in <ClassName>]` |

**Teaching content is not a verified source.** If a domain deep dive originates from concept-tutor output, teaching session notes, or a conversation summary — treat every fact in that content as unverified draft. Run the verification table above against source files before writing anything to disk. The concept-tutor reasons from documentation; it can drift from the source. The agent writing the doc must go back to the source itself.

**Consequence of skipping this rule:** Wrong proxy paths, wrong primary API patterns, and wrong port assignments produce documentation that misleads developers and requires a full quality review cycle to detect and correct.

---

### DEPLOYMENT.md — Mandatory Source Verification

**Hard rule — no inferred values.** Any agent writing DEPLOYMENT.md (project-level or platform-level) MUST read the following actual codebase files before writing a single value. If a file does not exist, note its absence and mark the affected fields `[NEEDS VERIFICATION]`. Do NOT present inferred or guessed values as fact.

| Value type | Must be sourced from |
|---|---|
| Port numbers | `docker-compose.yml`, `server.port` in application properties, or reverse proxy config |
| Context path / URL path | `server.servlet.context-path` in application properties, or web server config |
| JVM / application property names | Actual `application.properties` / `application.yml` / `.env` — never inferred from framework defaults |
| Startup command | `pom.xml` packaging type (`war` vs `jar`) determines deploy method; `Procfile` or `Dockerfile` for runtime command |
| Environment variable names | `.env`, `.env.example`, `docker-compose.yml` `environment:` block, or `application.properties` `${VAR_NAME}` references |
| Service versions | `pom.xml` `<version>`, `docker-compose.yml` image tags, or `package.json` |
| Resource limits (memory, CPU) | `docker-compose.yml` `deploy.resources`, JVM startup scripts, or Kubernetes manifests |        

**Consequence of skipping this rule:** Wrong port numbers, wrong property names, and wrong startup commands cause silent misconfiguration or immediate startup failure. This is unacceptable for enterprise deployment documentation.

**What to do when a value cannot be confirmed:** Write `[NEEDS VERIFICATION — read {filename} to confirm]` with the specific file to check. This is honest and actionable. Presenting a guess as a fact is not.

### Cross-Location Sync (Knowledge in Multiple Places)

When the same domain knowledge exists in more than one location (e.g., a deep dive doc + a skill file + a knowledge base file + a debug investigation), there is a defined update order to prevent drift:

| Location | Role | Update when |
|----------|------|-------------|
| `documentation/projects/{service}/domain/NN-*.md` | **Canonical source** — full detail, all 4 purposes | Primary: always update this first |
| `~/.gemini/skills/{area}/SKILL.md` or knowledge base `*.md` | **Agent quick-reference** — scannable subset for agents | Secondary: update after the canonical doc; must cross-reference canonical |
| `{project-root}/issues/{ticket}/investigation.md` | **Investigation record** — point-in-time snapshot | Do NOT backport doc changes here; it is a historical record, not a living doc |

**Rule:** The canonical domain doc is the source of truth. Skill files and knowledge base files summarize it. If they conflict, the canonical doc wins. The investigation file is never updated retroactively — it reflects what was known at the time.

**Content boundary — pattern vs instance:** See **Observability Section Pattern** above for the full boundary table (reusable diagnostic content belongs in canonical docs; instance-specific content belongs in `issues/{ticket}/` only).

**Reference direction is one-way:** The issues folder references documentation. Documentation never references the issues folder — docs are self-contained. It is the investigation file's job to point at the canonical doc, not the other way around.

---

Last Updated: 2026-03-13 — Added Last Updated placement rule; deep dive section pointer; multi-mode state machine rule; hybrid Library/Service classification; framework extension point coverage categories
