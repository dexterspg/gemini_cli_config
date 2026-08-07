# Build Log — Entry Formats

## Entry format (one per class/file/major decision)
```
### [N] <Class or file name>
Requirement: <the PRD/tech-spec requirement or business rule — in Mode B, the derived Business trigger carrying its (derived from code — no spec: <file>:<line>) tag>
Design decision: <why this shape — options considered, trade-off, what was chosen and why>
Why this exists: <one paragraph — the role this class/object plays>
Contents: <fields/attributes and what each represents>
Methods:
  - <signature>: <why it exists, why these specific parameters, why this return type>
Algorithm: <step-by-step logic, numbered, if the method has real logic — omit for pure pass-throughs>
Key insight: <the pedagogical conclusion from this method's Socratic exchange — the "aha" statement worth carrying forward>
Implementation: <file path + round, if round discipline applied>
Change history: <one line per section that touched this file>
  - Section N: <what was added or changed>
  - Section N+1: <what was added or changed>
```

**Slice entry (items 1–2, domain definition + business requirement):** never duplicated here. Write one pointer line only: `Slice entry: see mentor-logs/domain-<slug>-all-slices.md`. The domain log is the authoritative source — Build Log entries below cite file-level design decisions, not the slice's business case.

**Change history field:** required whenever a file is modified across more than one section. Shows the reader how the file grew over time — what existed at each section boundary — rather than only what the final state is. Omit for files created and completed in a single section.

Adapt fields to domain — same principle as Live Coding Sequence's round model: "Class/file" → the artifact unit for this domain (a class, a financial model component, a workflow step); "Methods" → "Steps/Logic" outside code; "Algorithm" → the actual decision/calculation logic; "Implementation" → wherever the artifact actually lives (file, spreadsheet, document).

## Infrastructure events

Infrastructure setup (cloud services, app registrations, environment configuration, API key creation, DNS, CI/CD) are **first-class entries** in the Build Log — not footnotes or prerequisites. Use the same entry format, adapted:

```
### [N] Infrastructure: <what was set up>
Requirement: <the FR/NFR or deployment need that necessitates this>
Design decision: <why this service/config — options considered, trade-off, choice>
Why this exists: <what the system gains — a public URL, auth identity, etc.>
Contents: <resource names, IDs, regions, tiers — the actual values>
Steps: <Portal UI steps or CLI commands — numbered>
Implementation: <Azure Portal / Cloud Shell / etc. + round number>
```

## File size cap (applies to Build Log and journal)

Soft limit 300 lines, hard limit 500. On hitting the hard limit: move the oldest entries to `mentor-logs/mentor-buildlog-<artifact-slug>-archive.md` (journal: `mentor-logs/mentor-log-<artifact-slug>-archive.md`), keep the last 5 entries plus the session narrative inline, and write one pointer line: "Entries 1–N archived — see `<archive file>` for full detail."
