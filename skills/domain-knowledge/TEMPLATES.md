# Domain Knowledge Templates

## File Template

# [Concept Name]

**What it is:** [1-2 sentence plain-language definition. No jargon.]

## Key Terms

| Term | Meaning |
|------|---------|
| [term] | [plain definition] |

## Core Rules / Key Points

[3-7 bullet points covering the most important things a developer needs to know. Focus on what is non-obvious or commonly misunderstood. Do not reproduce the full standard.]

## External Reference

[Standard name and version] — [Authoritative source link: official standard body, vendor docs, or RFC. One link only.]

## _metadata.md File Template
The central index for project context and document status.

```md
# [Domain Name] Domain - Project Context & Status

This file contains the project-specific context and document status for the public domain knowledge files in this directory.

---

### `[filename.md]`
- **Status:** [draft | validated | stale] | **Last Updated:** YYYY-MM-DD
- **Project Context:** [1-2 sentences explaining why this concept is relevant to the current project/codebase.]
- **Implementation Details:** See `[link to documentation/platform/...]`
```

## Frontmatter Fields Explanation

| Field | Purpose | Accepted Values |
|---|---|---|
| `source` | Identifies who wrote the content. | `gemini` (default) or `claude` (if written by Claude fallback) |
| `status` | Current readiness state of the file. | `draft` (new), `validated` (spot-checked), `stale` (snapshot > 12mo) |
| `last-updated` | The date the file was last edited. | YYYY-MM-DD |
| `snapshot-date` | The date the research was performed. | YYYY-MM-DD |
| `standard-version` | Version of the standard described. | e.g., "IFRS 16 (2023)" or "n/a" |

## _PENDING_SYNC.md Table Format

```md
# Pending Sync Decisions

| File | Domain | Written | Decision | Notes |
|------|--------|---------|----------|-------|
| [path/to/file.md] | [domain] | [YYYY-MM-DD] | pending | — |
```

## INDEX.md Row Template

```md
| [filename.md] | [Concept Name] | [YYYY-MM-DD] | draft |

## _keywords.md File Template
A plain text file containing a list of candidate concepts to document, with their frequency count. The file should be sorted by count in descending order.

**Format:** `keyword: count`

**Example `knowledge/accounting/_keywords.md`:**
```
asset-class: 8
depreciation-area: 5
lease-classification: 5
erp-master-data: 2
```

## _INDEX.md File Template
A domain-level index that visualizes the "Knowledge Puzzle" roadmap.

```md
# [Domain Name] Knowledge Puzzle

Build your knowledge of the [Domain Name] domain by following this tiered progression. Like a puzzle, start with the foundational anchors before moving to the logic engines and complex operations.

---

## Level 1: Anchors
*Foundational business entities. Prerequisite: None.*

| Concept | File | Summary |
|---------|------|---------|
| [Name] | [link.md] | [1-sentence summary] |

---

## Level 2: Engines
*Logic and determination systems. Prerequisite: Anchors.*

| Concept | File | Summary |
|---------|------|---------|
| [Name] | [link.md] | [1-sentence summary] |

---

## Level 3: Operations
*Complex accounting and workflows. Prerequisite: Anchors & Engines.*

| Concept | File | Summary |
|---------|------|---------|
| [Name] | [link.md] | [1-sentence summary] |
```
```
