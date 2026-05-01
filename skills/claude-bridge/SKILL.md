---
name: claude-bridge
description: Verbatim migration of skills and agents from ~/.claude to ~/.gemini with dependency auditing.
---

# 📜 Core Rules of Migration

### 1. The Verbatim Mandate
*   **Action:** When copying a skill or agent, you must replicate the content **word-for-word and line-for-line**.
*   **Integrity:** No paraphrasing, summarizing, or "improving" the text during the transfer.

### 2. The Conflict & Incompatibility Protocol
*   **Detection:** If a line or keyword is technically incompatible with the Gemini 2026 CLI architecture, you must detect it. Examples of known incompatibilities:
    *   Claude-specific XML tags like `<thinking>`.
    *   `model: sonnet` (or similar Anthropic models) in frontmatter must be replaced with a Gemini equivalent (e.g., `gemini-3-pro`).
    *   `color: [color]` in frontmatter is Claude-specific and should be removed.
*   **Reporting:** Flag the specific **Line Number** and the **Exact Word/Phrase** that causes the mismatch.
*   **Approval:** Present these differences to the user for manual approval before the file is written to the Gemini directory, *unless* they fall under pre-approved exceptions.

### 3. Dependency Auditing
*   **Cross-Reference:** Scan the source file for references to other Claude skills or agents (e.g., "Use @researcher-skill").
*   **Validation:** Check if a corresponding skill/agent exists in `~/.gemini`.
*   **Remediation:** If the dependency is missing, ask the user: *"This relies on [Agent/Skill Name] from Claude. Should we migrate that dependency next?"*

### 4. System Immutability
*   **Read-Only State:** You are strictly forbidden from modifying existing skills or agents in the `~/.gemini` directory unless this specific rule is explicitly rescinded by the user. 
*   **Section-by-Section Review:** For complex files, break the review into logical Markdown headers or JSON blocks to allow for granular approval.

---

# 📋 Out-of-Sync Registry

This section tracks skills and agents in `~/.gemini` that are missing content or features present in their `~/.claude` counterparts, or are pending migration.

### Pending Migration
- `agent-prompt-builder` (agent)
- `agent-time-tracker` (agent)
- `architecture-audit` (skill)
- `architecture-audit-workspace` (skill)
- `data` (skill)
- `desktop-app-storage` (skill)
- `guided-implementation-walkthrough` (skill)
- `prd-to-tasks` (skill)
- `prompt-builder` (skill)

### In-Sync / Migrated
- `jira` (skill)
- `company` (skill)
- `jira-content-creator` (agent)
- `claude-bridge` (skill)
- `agent-persona-reviewer` (agent)
- `persona-reviewer` (skill)
- `agent-quality-guardian` (agent)
- `quality-guardian` (skill)
- `documentation-specialist` (skill)
- `migration` (skill)
- `qa-engineer` (skill)
- `scheduled-automation-routine` (skill)
- `agent-data-analysis-expert` (agent)
- `agent-debugger` (agent)
- `agent-concept-tutor` (agent)
- `agent-note-taker` (agent)
- `agent-implementation-engineer` (agent)
- `agent-system-architect` (agent)
- `agent-product-strategist` (agent)
- `agent-data-doc-specialist` (agent)
- `agent-support-investigator` (agent)
- `agent-codebase-archaeologist` (agent)
- `agent-tech-detective` (agent)
- `agent-nla-implementation-engineer` (agent)
- `learning-strategy` (skill)
- `sandbox-builder` (skill)
- `step-visualization` (skill)
- `support-investigation` (skill)
- `project-estimator` (skill)
- `poc-writer` (skill)
- `grill-me` (skill)
- `requirements-discovery` (skill)
- `tdd` (skill)
- `ui-design` (skill)
- `walkthrough-planner` (skill)

