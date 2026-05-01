# Domain Knowledge Templates

## File Template

```md
---
source: gemini
status: draft
last-updated: YYYY-MM-DD
snapshot-date: YYYY-MM-DD
standard-version: [version or "n/a" if unversioned]
---

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
```
