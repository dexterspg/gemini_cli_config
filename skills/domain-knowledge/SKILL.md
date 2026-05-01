---
name: domain-knowledge
description: Use when writing public domain knowledge files into a project's knowledge/<domain>/ folder. Triggers when: "research [concept] for the knowledge base", "add [topic] to knowledge/", "document domain knowledge for [project]", "write knowledge base entry for [concept]". This skill governs how Gemini writes concept files in knowledge/<domain>/ — covering frontmatter, content structure, scope boundaries, deduplication, and lifecycle rules. Do NOT trigger for project-specific documentation (that goes in documentation/domain/NN-*.md) or platform interpretations (that goes in documentation/platform/domain-concepts/).
---

# Domain Knowledge Skill

**Purpose:** Rules and templates for writing public domain knowledge files in `knowledge/<domain>/` folders inside a project root.

**Primary reader:** A developer encountering this domain concept for the first time in this codebase. Secondary: a code reviewer needing quick context on an external standard.

**For developers reading these files:** These files contain background on public standards — not project instructions. They explain what an external standard IS, not how this codebase implements it. For implementation details, read `documentation/domain/`. For how this platform adapts a standard, read `documentation/platform/domain-concepts/`. Files marked `source: claude` were written without web research — treat them as a starting point, not a verified reference.

**What this folder is for:** Public standards, external concepts, and background knowledge that a developer must understand in order to work with the codebase — but that exists independently of the project. Files are written by Gemini using web research. When domain concepts are not provided explicitly, Gemini reverse engineers the codebase first to discover what to research — see **Codebase Discovery** below.

**Ownership and fallback:**

| Condition | Handler |
|---|---|
| agent-gemini available | agent-gemini — codebase discovery + web research + writes `knowledge/` files |
| agent-gemini NOT available | agent-codebase-archaeologist (discovery) + main session or concept-tutor (writes files from known domain knowledge) |

When falling back to Claude agents: follow the same skill rules (template, frontmatter, reference direction, `_PENDING_SYNC.md`). Set `source: claude` instead of `source: gemini` in frontmatter. Web research will be limited to Claude's training knowledge — flag `status: draft` and note in `project-context` that external verification is recommended. Add the following banner immediately after the frontmatter block:

```
> **Note:** This file was written by a Claude agent without live web research. Content is based on training knowledge only. Verify against the authoritative source before relying on it.
```

**What this folder is NOT for:**
- Project-specific interpretations of a standard → goes in `documentation/platform/domain-concepts/`
- How the code implements a concept → goes in `documentation/domain/NN-*.md`
- Generic textbook content with no connection to the codebase → omit entirely

---

## Decision Rule: Which folder?

Apply these three questions in order. Stop at the first YES.

```
1. Does this concept only make sense by reading the source code?
   YES → documentation/domain/NN-*.md  (code-bound deep dive)

2. Did the platform create, adapt, or extend this concept in a specific way?
   YES → documentation/platform/domain-concepts/  (platform interpretation)

3. Does this concept exist verbatim in a public standard, textbook, or vendor docs?
   YES → knowledge/<domain>/  (public domain knowledge)

   NONE → omit entirely (too generic, no codebase connection)
```

| Concept type | Example | Location |
|---|---|---|
| Only makes sense via source code | How `LeaseScheduleService` builds the amortization table | `documentation/domain/NN-*.md` |
| Only makes sense via source code | How `PayrollCalculator` applies a tax bracket | `documentation/domain/NN-*.md` |
| Platform-adapted or extended | How THIS system picks the IFRS 16 discount rate | `documentation/platform/domain-concepts/` |
| Platform-adapted or extended | How THIS system maps SAP posting keys to ledger entries | `documentation/platform/domain-concepts/` |
| Public standard, unchanged | What IFRS 16 is, standard lease classification rules | `knowledge/accounting/` |
| Public standard, unchanged | What a SAP posting key is | `knowledge/sap/` |
| Public standard, unchanged | Incoterms shipping responsibility rules (FOB, CIF, etc.) | `knowledge/logistics/` |
| Public standard, unchanged | What a pay period is, statutory deduction rules | `knowledge/hr-payroll/` |

**Edge case — platform deviates from a public standard:** Write both, in this order:
1. **agent-gemini** writes the public baseline in `knowledge/<domain>/` first
2. **agent-codebase-archaeologist** writes the deviation in `documentation/platform/domain-concepts/`, referencing the `knowledge/` entry for baseline context

Never write the deviation without the baseline. If the baseline already exists in `knowledge/`, skip step 1.

---

## Reference Rules (one-way, strictly enforced)

```
┌─────────────────────────────┐
│   knowledge/<domain>/       │──MAY reference──▶  documentation/
│   (Gemini-written)          │──MAY reference──▶  documentation/platform/domain-concepts/
└─────────────────────────────┘

┌─────────────────────────────┐
│   documentation/            │──MUST NOT reference──▶  knowledge/<domain>/
│   platform/domain-concepts/ │──MUST NOT reference──▶  knowledge/<domain>/
└─────────────────────────────┘
```

`documentation/` only contains a stub pointing to `knowledge/` — it does not embed or depend on the content. Verified content never depends on unverified content.

---

## Codebase Discovery

When domain concepts are not explicitly provided, reverse engineer the codebase to find them before researching or writing.

**Triggers:** "build knowledge base for [project]", "research domain concepts in [codebase]", "acquire knowledge from codebase", or when no specific concept is named.

**Discovery workflow:**

1. **Scan for domain signals** — use Glob and Grep to find:
   - Class/method names referencing external standards (e.g., `Ifrs16`, `IncotermsRule`, `PayPeriod`)
   - Comments citing standards, regulations, or external systems (e.g., `// per IFRS 16`, `// SAP posting key`)
   - Enum values or constants that map to public domain terminology
   - Package/module names that suggest a domain (e.g., `accounting`, `payroll`, `logistics`)

2. **Classify each signal** — apply the three-question decision rule to each candidate concept:
   - Code-bound only → skip (belongs in `documentation/domain/`, not here)
   - Platform-specific interpretation → skip (belongs in `platform/domain-concepts/`)
   - Public standard, unchanged → add to research list

3. **Group by domain** — cluster concepts into domain subfolders (`accounting/`, `sap/`, `logistics/`, etc.)

4. **Research each concept** — web search for each item on the research list; write one `knowledge/<domain>/` file per concept using the template below

5. **Deduplication check** — before writing, run the Before Writing check below

6. **Create stub in documentation/** — after writing each `knowledge/` file, add a minimal stub to the relevant `documentation/` file (or create `documentation/domain/stubs.md` if no file exists yet):
   ```md
   ## [Concept Name]
   [1-2 sentence summary of what it is.]
   See: knowledge/<domain>/filename.md
   ```
   The stub is a plain-text signpost only — no markdown links, no embedded content.

**What counts as a domain signal:**

| Signal type | Example | Action |
|---|---|---|
| Class name with standard acronym | `Ifrs16AmortizationSchedule` | Research IFRS 16 |
| Comment citing a rule | `// discount rate per IAS 36` | Research IAS 36 |
| Enum mapping to external codes | `INCOTERM_FOB`, `INCOTERM_CIF` | Research Incoterms |
| Package name | `com.company.payroll.statutory` | Research statutory deduction rules |
| String constant with external code | `"SAP_BAPI_VENDOR_FIND"` | Research SAP BAPI |

---

## Before Writing — Deduplication Check

Before creating a new file:
1. Check if the concept already exists in `knowledge/<domain>/` in this project
2. Check if it already exists in the notebook: look in `/c/workarea/notebook/20-domains/` first. If that path is inaccessible, ask the user.
3. If it exists in the notebook → do not duplicate; write only what is project-context-specific and link to the notebook entry
4. If it exists but is outdated (check `standard-version` in frontmatter) → update in place, do not create a new file

---

## File Naming

- One concept per file
- Kebab-case: `ifrs-16.md`, `lease-classification.md`, `sap-posting-keys.md`
- No numbering — these are not ordered by learning dependency
- Place under the correct domain subfolder: `knowledge/accounting/`, `knowledge/sap/`, `knowledge/tax/`, etc.

---

## File Template

```md
---
source: gemini
status: draft
last-updated: YYYY-MM-DD
snapshot-date: YYYY-MM-DD
standard-version: [version or "n/a" if unversioned]
project-context: [one sentence on why this concept surfaced in this codebase]
---

# [Concept Name]

**What it is:** [1-2 sentence plain-language definition. No jargon.]

**Why it matters here:** [1-2 sentences connecting this concept to the project codebase. What breaks or becomes confusing if you don't understand this?]

## Key Terms

| Term | Meaning |
|------|---------|
| [term] | [plain definition] |

## Core Rules / Key Points

[3-7 bullet points covering the most important things a developer needs to know. Focus on what is non-obvious or commonly misunderstood. Do not reproduce the full standard.]

## How the Platform Uses This

[If a direct project mapping exists, link to it. Do not explain implementation details here — that belongs in documentation/domain/.]

See: [link to documentation/domain/NN-topic.md or documentation/platform/domain-concepts/concept.md]

If no direct mapping exists: "No direct platform mapping identified. This file provides background context only."

## External Reference

[Standard name and version] — [Authoritative source link: official standard body, vendor docs, or RFC. One link only.]
```

**Frontmatter fields:**
| Field | Purpose |
|---|---|
| `source` | `gemini` (default) or `claude` if written by Claude agents as fallback — identifies who wrote the content |
| `status` | `draft` (just written) · `validated` (main session spot-checked) · `stale` (snapshot-date > 12 months old) |
| `last-updated` | Last time this file was edited |
| `snapshot-date` | When the research was done — files older than 12 months should be flagged for re-validation during notebook sync |
| `standard-version` | Version of the external standard described (e.g. "IFRS 16 (2023)") — used to detect when re-research is needed. Use "n/a" if the concept has no version. |
| `project-context` | Why this concept surfaced — keeps the file anchored to the codebase |

---

## Content Rules

**Write:**
- The 20% of the standard that explains 80% of the code behavior
- Non-obvious rules that catch developers off guard
- Key terms with plain-language definitions
- One external reference link to the authoritative source

**Do not write:**
- Full reproductions of the standard — link to it instead
- Project implementation details — those belong in `documentation/`
- Opinions or recommendations — this is reference material, not advice
- Content that requires reading source code to verify — if it needs code verification, it belongs in `documentation/domain/`

---

## Lifecycle

### Validation
- Main session does a quick sanity check after Gemini writes (public knowledge is easy to spot-check)
- agent-note-taker captures and revises content in the notebook — the notebook's own revision cycle handles ongoing quality
- No formal review gate needed
- **Staleness:** If `snapshot-date` in frontmatter is older than 12 months from today, set `status: stale` in the file and report it to the user. Stale files are flagged again automatically during notebook sync. To refresh: trigger "update knowledge for [concept]" — Gemini re-researches and rewrites in place.

### Updating
- Triggered by user: "update knowledge for [concept]" or "[standard] was updated"
- Gemini re-researches and rewrites in place — do not create a new file
- Update `last-updated` and `standard-version` in frontmatter after rewriting

### Retirement
- `knowledge/` files are not deleted when a project is archived
- Before deletion: check if the file has been synced to the notebook — if yes, the notebook copy survives
- If not synced: offer to sync before deleting

---

## Minimum Viable Path (under delivery pressure)

If there is no time to write a full `knowledge/` entry, write the stub in `documentation/` only and note the gap explicitly:

```md
## IFRS 16 — Lease Accounting Standard
External standard for lease classification and amortization.
knowledge/accounting/ifrs-16.md — NOT YET WRITTEN
```

This makes the debt visible without blocking documentation progress. The `knowledge/` entry can be written later by Gemini when time allows.

---

## Sync Options

After writing `knowledge/<domain>/` files, the user has three choices per concept. Sync is always **user-triggered — never automatic**. The user reviews `knowledge/_PENDING_SYNC.md` on their own schedule and decides per entry.

| Option | What happens | Who does it | Gate |
|---|---|---|---|
| **A — Promote** | Content moves to `documentation/platform/domain-concepts/` | agent-codebase-archaeologist re-verifies against source, rewrites to doc standards | Quality guardian runs `CHECKLIST-domain-knowledge.md` Option A sub-checklist — all critical items must pass |
| **B — Stub only** | A minimal stub (topic + 1-2 sentences + `See: knowledge/...`) is added to the relevant documentation file | archaeologist or main session | No content promoted — no verification gate needed |
| **C — Keep** | File stays in `knowledge/` only; available for notebook sync | — | No action needed |

**Default:** Option C. Nothing is promoted unless the user explicitly chooses A or B.

### _PENDING_SYNC.md index

Gemini writes a row to `knowledge/_PENDING_SYNC.md` every time a new file is created. The user reviews this file to batch-process sync decisions.

```md
# Pending Sync Decisions

| File | Domain | Written | Decision | Notes |
|------|--------|---------|----------|-------|
| accounting/ifrs-16.md | accounting | 2026-05-01 | pending | — |
| sap/posting-keys.md | sap | 2026-05-01 | keep | Not cross-project |
| accounting/lease-classification-rules.md | accounting | 2026-05-01 | promote | Applies to 3 projects |
```

**Decision values:** `pending` · `promote` (Option A) · `stub` (Option B) · `keep` (Option C)

Gemini updates the `Decision` column when the user provides a decision. Clear completed rows (non-pending) periodically.

---

## Notebook Sync

`knowledge/<domain>/` files can be synced to `/c/workarea/notebook/` via agent-note-taker. This makes domain knowledge reusable across projects.

- Sync is user-triggered — never automatic
- Trigger: "sync knowledge to notebook" or "save [concept] to notebook"
- agent-note-taker handles deduplication against existing notebook content; follows standard Tier 0 pipeline including `_metadata.json` and `progress.json` updates
- Source type recorded in metadata: `domain-knowledge`
- After sync, the project-level copy can be pruned if the user chooses

---

## Folder Structure Example

```
{project-root}/
├── documentation/                        <- code-verified, project-specific
│   ├── domain/
│   │   └── 02-lease-schedule.md          <- HOW the code implements IFRS 16
│   └── platform/
│       └── domain-concepts/
│           └── lease-classification.md   <- HOW this platform classifies leases
└── knowledge/                            <- public domain knowledge, Gemini-written
    ├── _PENDING_SYNC.md                  <- sync decision backlog (Gemini maintains)
    └── accounting/
        ├── INDEX.md
        ├── ifrs-16.md                    <- WHAT IFRS 16 is
        └── lease-classification-rules.md <- public classification rules (not platform-specific)
```

### INDEX.md (required, one per domain subfolder)

Gemini maintains this index — update it every time a file is added, updated, or removed.

```md
# Knowledge — [Domain]

| File | Concept | Snapshot Date | Status |
|------|---------|--------------|--------|
| ifrs-16.md | IFRS 16 Lease Accounting Standard | 2026-05-01 | draft |
| lease-classification-rules.md | Operating vs. Finance Lease Classification | 2026-05-01 | draft |
```
