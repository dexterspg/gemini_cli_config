---
name: claude-bridge
description: 'Verbatim migration of skills and agents from ~/.claude to ~/.gemini with dependency auditing. Triggers on: "migrate from claude", "copy skill from ~/.claude", "bring over my claude agent", "sync with claude", "is this skill in sync with claude".'
---

# Claude Bridge

Verbatim migration protocol for porting assets from Anthropic/Claude environments to Gemini 2026 architecture.

## Trigger Conditions
- User asks to "migrate", "copy", or "sync" a skill/agent from Claude.
- User mentions the `~/.claude` directory.
- User asks if a specific Gemini skill is "in sync" or "up to date" with its Claude counterpart.

## Do NOT trigger for
- Creating new skills from scratch -> Route to `skill-creator`.
- Migrating client/business data -> Route to `migration`.
- General codebase investigation -> Route to `codebase-investigator`.

## Capabilities
- Perform verbatim (word-for-word) replication of files.
- Detect and flag technical incompatibilities (XML tags, model names, color metadata).
- Audit dependencies and prompt for migration of missing linked assets.
- Convert Claude-style workflow loading to Gemini `MANDATORY: Load [path]` format.
- Organize migrated workflows into standard `workflows/` subdirectories.

## Never
- Paraphrase, summarize, or "improve" text during transfer.
- Modify the source `~/.claude` directory.
- Commit changes without explicit user approval.
- Skip dependency validation.

## Migration Protocol

### 1. The Verbatim Mandate
- Replicate content exactly (word-for-word, line-for-line).
- Preserve all structural formatting and comments.

### 2. Conflict & Incompatibility Protocol
- Detect technically incompatible keywords/tags.
- **Reporting:** Flag exact **Line Number** and **Phrase**.
- **Gemini 2026 Mapping:**
    - Remove: Claude-specific XML tags (e.g., `<thinking>`).
    - Remove: `color: [color]` from frontmatter.
    - Replace: `model: sonnet` (or other Anthropic models) with `model: flash` or `model: pro`.
- **Approval:** Obtain user confirmation for every change before writing.

### 3. Dependency Auditing
- Scan source for `@skill` or `@agent` references.
- Verify existence in `~/.gemini`.
- If missing, ask: *"Dependency [Name] is missing. Migrate it next?"*

### 4. Workflow Conversion
- Move `workflows/` to `~/.gemini/skills/[skill]/workflows/`.
- Convert loading logic: `If [condition]: MANDATORY: Load [path]`.
- Consolidate simple flows into `WORKFLOWS.md` if possible.

---

# 📋 Out-of-Sync Registry

This section tracks assets in `~/.gemini` that are missing features from their `~/.claude` counterparts.

### Pending Migration
- None

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
- `agent-prompt-builder` (agent)
- `agent-time-tracker` (agent)
- `architecture-audit` (skill)
- `architecture-audit-workspace` (skill)
- `data` (skill)
- `desktop-app-storage` (skill)
- `guided-implementation-walkthrough` (skill)
- `prd-to-tasks` (skill)
- `prompt-builder` (skill)
