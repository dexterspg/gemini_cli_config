---
name: issue-investigation
description: Intake and initial triage workflow for Jira or local issues. Triggers: "investigate [ticket]", "debug [issue]".
---
# Issue Investigation Workflow


## Flow (main session responsibilities only)

1. **Intake:** If Jira, fetch via `mcp__jira__get_jira_issue`. Check `{project-root}/issues/` for existing `TICKET-KEY*/_INTAKE.md` via Glob. If found, confirm resume; otherwise, create issue folder + `attachments/` + `_INTAKE.md`.
2. **Evidence:** Auto-download attachments per `~/.gemini/skills/jira/SKILL.md`. On failure, ask user for manual drop.
3. **Confirm:** Prompt for additional local files in `attachments/`.
4. **Delegate:** Spawn `agent-debugger` on issue folder.
5. **Close:** Read "Documentation Handoff" and route signal patterns to domain docs.
