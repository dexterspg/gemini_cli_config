# Domain Knowledge Templates

## File 1: Domain File Template (`{concept}.md`)

Pure concept content — no project specifics. Written by `agent-concept-tutor` from Gemini research. Standalone: works without any project documentation folder existing.

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

## File 2: Reference File Template (`{concept}-ref.md`)

Project-specific bridge — codebase links, documentation references, and how the platform uses this concept. Only create when the project has an actual implementation of the concept.

```md
---
project-context: [one sentence on why this concept surfaced in this codebase]
last-updated: YYYY-MM-DD
---

# [Concept Name] — Project Reference

> Public standard background: see [`{concept}.md`]({concept}.md)

## Why It Matters Here

[1-2 sentences: what breaks or becomes confusing if a developer doesn't understand this concept in context of this project?]

## How the Platform Uses This

[Direct mapping to implementation. Do not explain the standard here — that is in the domain file.]

See: `documentation/domain/NN-topic.md` or `documentation/platform/domain-concepts/concept.md`

If no direct mapping exists: omit this section entirely — do not create the reference file.

## Codebase References

- `[file or class path]` — [what it does with this concept]
```

## Frontmatter Fields Explanation

| Field | File | Purpose | Accepted Values |
|---|---|---|---|
| `source` | Domain | Identifies who wrote the content. | `gemini` (default) or `claude` (fallback) |
| `status` | Domain | Current readiness state. | `draft`, `validated`, `stale` |
| `last-updated` | Both | Date last edited. | YYYY-MM-DD |
| `snapshot-date` | Domain | Date research was performed. | YYYY-MM-DD |
| `standard-version` | Domain | Version of the standard described. | e.g., `IFRS 16 (2023)` or `n/a` |
| `project-context` | Reference | Why this concept appeared in this codebase. | Single sentence. |

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
