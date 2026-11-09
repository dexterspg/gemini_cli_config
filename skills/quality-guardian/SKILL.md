---
name: quality-guardian
description: 'Multi-type review checklists for code, docs, designs, and prd-sync. Triggers: "review this", "quality check", "sync check".'
---

# Quality Guardian Review Checklists

MANDATORY: Read `~/.gemini/skills/quality-guardian/CHECKLISTS.md` — it owns the Checklist Conventions, Severity and Verdict rules, Base Checklist, Over-Engineering Guard, Declared Style, and the full Routing Table mapping each content type to its `CHECKLIST-*.md` file.

## Rules
- Do NOT trigger for raw data files (CSV, Excel, JSON datasets) -> route to `agent-data-analysis-expert`.
- Do NOT trigger for live system behavior or runtime diagnostics -> route to `agent-debugger`.
