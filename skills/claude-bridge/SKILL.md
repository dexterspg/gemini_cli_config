---
name: claude-bridge
description: 'Domain-parity migration and native Gemini/Antigravity adaptation of skills and agents from ~/.claude to ~/.gemini with dependency auditing. Triggers on: "migrate from claude", "copy skill from ~/.claude", "bring over my claude agent", "sync with claude", "is this skill in sync with claude".'
---

# Claude Bridge

Migration protocol for porting assets from Anthropic/Claude environments (`~/.claude`) to Gemini / Antigravity (`~/.gemini`) while preserving **100% domain parity** and adapting **platform mechanics to Gemini's native identity**.

## Trigger Conditions
- User asks to "migrate", "copy", or "sync" a skill/agent from Claude.
- User mentions the `~/.claude` directory.
- User asks if a specific Gemini skill is "in sync" or "up to date" with its Claude counterpart.

## Do NOT trigger for
- Creating new skills from scratch -> Route to `skill-creator`.
- Migrating client/business data -> Route to `migration`.
- General codebase investigation -> Route to `codebase-investigator`.

## Capabilities
- Replicate domain logic, safety rules, and output contracts verbatim.
- Adapt Claude Code platform mechanics to native Gemini / Antigravity (`agy`) tooling and identity.
- Detect and flag technical incompatibilities (XML tags, model names, color metadata, Claude-only mods).
- Audit dependencies and prompt for migration of missing linked assets.
- Convert Claude-style workflow loading to Gemini `MANDATORY: Load [path]` format.
- Track intentional Gemini-native adaptations so future syncs never overwrite them.

## Never
- Paraphrase, weaken, or alter domain rules, safety gates, or output contracts during transfer.
- Modify the source `~/.claude` directory or touch `~/.claude/browser-profile`.
- Commit changes without explicit user approval.
- Skip dependency validation.

## Migration Protocol

### 1. The Encoding Mandate (UTF-8 No BOM)
- ALL files MUST be saved as **UTF-8 without BOM**. 
- A BOM (Byte Order Mark) will cause YAML frontmatter parsing failures in the Gemini CLI.

### 2. Domain Parity + Native Gemini Adaptation Mandate
- **Verbatim Domain Parity:** Keep business rules, domain logic, Nakisa build mappings (`preview1`, `ra-env2`), security boundaries (`ALLOWED_HOSTS`, zero AI credential handling), and output schemas (`PASS`/`FAIL`/`RESULT`, exit codes `0/1/2`) word-for-word identical to `~/.claude`.
- **Native Gemini Platform & Persona Adaptation:** Adapt platform-specific mechanics so the skill operates natively in Gemini / Antigravity rather than mimicking Claude Code:
    - **Config & Orchestrator Identity:** Map `CLAUDE.md` references to `GEMINI.md` and preserve Gemini's Main Session Orchestrator role (lazy-loading via `MANDATORY: Load [path]` and subagent delegation).
    - **Windows PowerShell First:** Provide and prioritize native PowerShell scripts (`.ps1`) and invocations alongside Git Bash (`.sh`), instead of assuming Claude's `Bash` tool.
    - **Native Antigravity Surfaces & Commands:** Map Claude-only plugin commands (e.g., `/mod-login`) to Gemini's native helpers (`run.ps1` / `run.sh`) and integrate Antigravity's native slash commands (`/browser` for one-off DOM discovery, `/goal` for autonomous execution, `/artifact` & Auxiliary Side Pane for visual reports).
    - **Profile & State Isolation:** Always use `~/.gemini/browser-profile` (never `~/.claude/browser-profile`) so Gemini and Claude sessions never log each other out.

### 3. Conflict & Incompatibility Protocol
- Detect technically incompatible keywords/tags.
- **Reporting:** Flag exact **Line Number** and **Phrase**.
- **Gemini 2026 Mapping:**
    - Remove: Claude-specific XML tags (e.g., `<thinking>`).
    - Remove: `color: [color]` from frontmatter.
    - Replace: `model: sonnet` (or other Anthropic models) with `model: flash` or `model: pro`.
    - Adapt: `/mod-*` plugin references, `CLAUDE.md` pointers, and `Bash tool` phrasing per Section 2.
- **Approval:** Obtain user confirmation for every change before writing.

### 4. Dependency Auditing
- Scan source for `@skill` or `@agent` references.
- Verify existence in `~/.gemini`.
- If missing, ask: *"Dependency [Name] is missing. Migrate it next?"*

### 5. Workflow Conversion
- Move `workflows/` to `~/.gemini/skills/[skill]/workflows/`.
- Convert loading logic: `If [condition]: MANDATORY: Load [path]`.
- Consolidate simple flows into `WORKFLOWS.md` if possible.

---

# 📋 Out-of-Sync & Adaptation Registry

This section tracks assets in `~/.gemini` relative to `~/.claude`, separating missing features from intentional Gemini-native adaptations.

### Pending Migration
- None

### Intentional Gemini-Native Adaptations (Do Not Overwrite on Sync)
`~/.gemini` is the source of truth for the platform adaptations below; only sync domain rules from `~/.claude`:
- `browser-scenarios` (skill):
    - Uses `~/.gemini/browser-profile` (isolated from `~/.claude/browser-profile` and ignored in `~/.gemini/.gitignore`).
    - Includes Windows PowerShell launcher `scripts/start-chrome.ps1` alongside `start-chrome.sh`, with Chrome path fallback detection (`CHROME_BIN`, `Program Files`, `Program Files (x86)`, `LocalAppData`).
    - Disambiguates Antigravity's native `/browser` command (one-off page inspection) from replayable Playwright scripts (`browser-scenarios`), and documents `/goal` and `flash`/`pro` model guidance.
    - Documents live-verified Quasar / Vue SPA UI automation rules (`payable-ui` on `ra-env2`): scoping active dialogs to `.q-dialog__inner:visible`, clearing orphaned `.q-dialog__backdrop` overlays, interacting with portaled `.q-menu:visible` server-filtered dropdowns (`ApInputPinnedSingleSelect`), dismissing date popups with `Escape`, and pairing `--write` with `--cleanup` (`Callback` -> `Draft` -> `Delete`).
    - Enforces scenario conventions via `recon/lint_browser_scenarios.py` and prohibits scratch scripts inside `scenarios/browser/`.
- `browser-login` (skill):
    - Uses `~/.gemini/browser-profile` and `<build>-user` files inside `~/.gemini/browser-profile/`.
    - Includes `scripts/login.py`, `scripts/run.ps1`, `scripts/run.sh`, `scripts/mod-login.ps1`, and `scripts/mod-login.cmd` directly in the skill, plus the user-run `mod-login` PowerShell `$PROFILE` function (replacing Claude's `~/.claude/mods/mod-login` plugin).
    - Resolves `nakisa-products.md` across `NAKISA_PRODUCTS_FILE`, `C:/workarea/references/nakisa-products.md`, and `~/workarea/references/nakisa-products.md`.
    - Adds R&D / SPA hash-route (`/#/`) handling and 403 JSON retry logic in `login.py` and `SKILL.md` for `ra-env*` builds.

### In-Sync / Migrated
- `browser-scenarios` (skill — domain parity + Gemini-native adaptation above)
- `browser-login` (skill — domain parity + Gemini-native adaptation above)
- `engineering-journal` (skill)
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
