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
