# Domain Knowledge Templates

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

## Frontmatter Fields Explanation

| Field | Purpose | Accepted Values |
|---|---|---|
| `source` | Identifies who wrote the content. | `gemini` (default) or `claude` (if written by Claude fallback) |
| `status` | Current readiness state of the file. | `draft` (new), `validated` (spot-checked), `stale` (snapshot > 12mo) |
| `last-updated` | The date the file was last edited. | YYYY-MM-DD |
| `snapshot-date` | The date the research was performed. | YYYY-MM-DD |
| `standard-version` | Version of the standard described. | e.g., "IFRS 16 (2023)" or "n/a" |
| `project-context` | Anchors the file to the specific codebase. | Single sentence explaining why this concept is relevant. |

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
```
