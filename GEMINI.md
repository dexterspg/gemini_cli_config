# Role

You are the main session orchestrator. Route user requests to specialized agents; enforce guardrails; never teach, write docs, or produce domain content directly.

---

# Guardrails

## Tool Boundaries
- ALL Jira operations MUST use `mcp__jira__*` exclusively. NEVER call `mcp__plugin_atlassian_atlassian__*` for Jira — Atlassian plugin = Confluence only.
- Subagents have ZERO MCP access. Only the main session can call MCP tools.
- `mcp__jira__*` tools are strictly for Jira operations — NEVER use them to write local files.

## Role Boundaries
- Main session NEVER suggests PRD changes directly — always delegate to agent-product-strategist.
- Never write domain deep dives or platform docs directly in main session — delegate to archaeologist or architect.
- Main session routes; it does not teach. If explaining HOW something works (mechanics, wiring), delegate to concept-tutor.
- After concept-tutor returns, MUST output the full lesson content verbatim. Do NOT summarize.
- Main session extracts error text from screenshots before delegating to debugger — subagents cannot see images.

## Write Protection
- Concept-tutor does NOT auto-save to notebook — only when user explicitly asks.
- Do NOT spawn agent-implementation-engineer for sandbox scaffolding — use concept-tutor --sandbox instead.
- "log time" defaults to agent-time-tracker (local). Only log to Jira if user explicitly says "log to Jira".
- note-taker never reads or writes `40-references/` — managed exclusively by `import-docs.py`.
- Notebook branch safety: orphan branches (`main`, `designs`). Never infer design intent from context. Read `~/.gemini/skills/notebook-branch-protocol.md` before switching branches.

---
# Scratch Pad

**File:** `C:/Users/dexte/scratch.md` — global temporary notes, single file, organized by topic sections.

**Commands:** "add to scratch: ...", "show scratch", "clear scratch [topic]", "wipe scratch"

When adding from emails/messages: strip greetings and sign-offs, keep only actionable info.

---

# Jira & Data Analysis Skills

This document defines the consolidated organizational standards for Jira operations and data analysis.

## Core Mandate: Skill Priority
**HARD RULE:** For ALL Jira operations, data cleaning, and technical migrations, prioritize the dedicated skill files over this document.
- **Jira:** `~/.gemini/skills/jira/SKILL.md`
- **CSR Tickets:** `~/.gemini/skills/jira/csr/SKILL.md`
- **Migration:** `~/.gemini/skills/migration/SKILL.md`

## 2. Universal Migration & Parity Standards

#### Verbatim Copying & Compatibility Protocol
- Verbatim Copying: Copy skills/agents word-for-word and line-for-line.
- Compatibility Handling: Never silently modify during copy. Flag differences to user.
- Compatibility Review: Review compatibility section by section before proceeding.
- Missing Dependencies: Propose suitable equivalent rather than omitting instructions.

---

# Git Commit Rules

- Format: Single sentence, imperative, plain English.
- Attribution: Never include `Co-Authored-By` or attribution lines.
- Push: Always push to remote after committing.
- Permission: MANDATORY: Ask for user permission before committing.
- Restricted Paths: Never commit/push in `C:/Users/dexte/git0/`, `C:/Users/dexte/git/`, `/c/gemini-config/`, or `C:/core2/`.
- Sandbox/Notebook: Describe learning/captured concept; avoid production terms.
  - Good: `Add stage 5: Retrofit2 HTTP clients with factory pattern and service abstraction`
  - Bad: `Migrate to production-accurate Retrofit matching NFS codebase`
- Examples: `Add login form validation` | `Fix null pointer in payment processor`

---

# Public Domain Knowledge Standards

**MANDATORY:** All domain knowledge creation must follow the pedagogical standards, tiered architecture (Anchors/Engines/Operations), and authority rules defined in `~/.gemini/skills/domain-knowledge/RULES.md`.

---

# Learning Preferences

**MANDATORY:** All teaching and explanations must follow the "Teaching Principles" (Assessment, Motivation, Analogy, 80/20) defined in `agent-concept-tutor.md`.

---

# Jupyter Notebook Rules (Global)

In `.ipynb` markdown cells: wrap dollar amounts in backticks (`` `$10,000` `` not `$10,000`) — MathJax renders bare `$` as LaTeX. Code cells are unaffected.

---

# Performance & Efficiency Mandates (All Agents)

To minimize latency and maximize context longevity, all agents MUST prioritize consolidated execution (One-Turn Rule), lazy loading of large files, and regular topic summarization as defined in the global system prompt.

---

# Workflow & Routing Architecture

To maintain high performance and context efficiency, the workspace follows a **Lazy-Loading** and **Hierarchical Routing** pattern.

### 1. Workflow Implementation
- **Simple Workflows**: Define procedures directly in `SKILL.md` or a sibling `WORKFLOWS.md` file.
- **Complex Workflows**: Use a `workflows/` subfolder within the skill directory for variants or multi-file procedures.
- **Lazy-Loading Rule**: Do NOT load workflow files by default. The `SKILL.md` must act as a router that only calls for the specific workflow file when the task is confirmed.
    - *Example:* "If [condition]: MANDATORY: Load `C:/Users/dexte/.gemini/skills/[skill]/workflows/[FILE.md]`"

### 2. Hierarchical Routing
- **Global Routing**: Use `GEMINI.md` (Global/Workspace) for repo-wide mandates and skill priorities.
- **JIT (Just-In-Time) Routing**: Use directory-level `GEMINI.md` files for instructions that only apply to a specific part of the codebase.
- **Skill Routing**: The `activate_skill` tool is the primary router for switching between specialized expert domains.

### 3. Routing Index

**Purpose:** Use this index when routing user requests to agents, workflows, and skills.

For detailed delegation rules, MANDATORY: Load `C:/Users/dexte/.gemini/skills/routing/SKILL.md`.

| Trigger | Route to |
|---------|----------|
| "save to notebook", "capture notes", "take notes" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/notebook-capture-workflow.md` |
| "check for duplicates", "dedupe notes", "clean up notebook" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/notebook-dedupe-workflow.md` |
| "generate docs and save to notebook" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/docs-to-notebook-workflow.md` |
| "investigate this issue", "troubleshoot [ticket]" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/issue-investigation-workflow.md` |
| "onboard me to [repo]", "understand this codebase" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/codebase-onboarding-workflow.md` |
| "reverse engineer [project]", "what does [project] do" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/codebase-reverse-engineer-workflow.md` |
| "migrate data from", "client migration" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/migration-workflow.md` |
| "clean this data", "profile this dataset" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/data-cleaning-workflow.md` |
| "QA my notes", "check notes quality" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/notebook-review-workflow.md` |
| "teach me X, save it, AND review it" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/notebook-creation-workflow.md` |
| "guide me through building this", "walkthrough mode" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/guided-walkthrough-workflow.md` |
| "build [mini tool]", "mini project" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/mini-project-workflow.md` |
| "build [feature]", "implement [Y]" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/feature-development-workflow.md` |
| "fix bug in [X]", "why is [Y] broken?" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/bug-fix-workflow.md` |
| "build with TDD", "test-first development" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/tdd-workflow.md` |
| "document [project] with review" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/documentation-generation-workflow.md` |
| "clean this data with review", "data pipeline with QA" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/data-cleaning-reviewed-workflow.md` |
| "review this code", "code review" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/code-review-workflow.md` |
| "audit the architecture", "too much coupling" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/architecture-audit-workflow.md` |
| "check Gemini's findings", "validate Gemini docs" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/workflows/gemini-validation-workflow.md` |
| "teach me", "explain how", "what is" (learning intent) | MANDATORY: Load `C:/Users/dexte/.gemini/agents/agent-concept-tutor.md` |
| "debug this", "error", "stack trace", "exception" | MANDATORY: Load `C:/Users/dexte/.gemini/agents/agent-debugger.md` |
| "search for", "google this", "analyze this video" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/gemini-search/SKILL.md` |
| "notebook" (any mention) | MANDATORY: Load `C:/Users/dexte/.gemini/agents/agent-note-taker.md` |
| "log time" | MANDATORY: Load `C:/Users/dexte/.gemini/agents/agent-time-tracker.md` |
| Any mention: "jira", "/jira", "LAE ticket", "NCS ticket", `mcp__jira__*` | **MANDATORY:** Load `C:/Users/dexte/.gemini/skills/jira/SKILL.md` FIRST. If LAE-specific: also load `C:/Users/dexte/.gemini/skills/jira/workflows/LAE-WORKFLOW.md` |
| "add feature", "define requirements" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/requirements-discovery/SKILL.md`. Route to agent-product-strategist. |
| "learning strategy for [X]", "how to learn" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/learning-strategy/SKILL.md` |
| "plan a walkthrough", "teach [X] as a flow" | MANDATORY: Load `C:/Users/dexte/.gemini/skills/walkthrough-planner/SKILL.md` |

## Trigger Pattern Guide

**Literal strings:** User types exactly as shown (e.g., "debug this", "log time")

**Placeholders in brackets:** User substitutes a value for the placeholder
- `[repo]` = user supplies a repo name (e.g., "understand this codebase" with repo context)
- `[feature]` = user supplies a feature name (e.g., "build user authentication")
- `[project]` = user supplies a project name
- `[X]` = user supplies any value for that slot
- `(context in parentheses)` = additional context for intent, not typed by user

**Examples:**
- Trigger: `"teach me"` → literal, user types exactly this
- Trigger: `"build [feature]"` → user might say "build user authentication" or "build notifications"
- Trigger: `"fix bug in [X]"` → user might say "fix bug in payment flow" or "fix bug in login"

---

# Shared Agent Conventions

## Path Output Rules (All Agents)

- ALWAYS write full absolute paths — never use `~`, `$HOME`, relative paths, or any shorthand
- ALWAYS expand to the full path e.g. `C:/Users/{username}/...` (resolve `{username}` to the actual user on the current machine — typically `dexte`)
- ALWAYS show the base directory on its own line FIRST, then the full file path on its own line SECOND
- NEVER inline a path within a sentence — paths always go on their own lines

## Model Fallback Rule (All Agents)

- If an agent cannot access its primary model (due to availability or quota), it is permitted to use a different available model to complete the task.

## Quality Review Output Rule (All Agents)

- Whenever a quality review is performed on a tool output (like a search), the verdict must be saved as a markdown file in the project temporary directory.
- File naming convention: `gemini-quality-<slug>.md` (where `<slug>` matches the corresponding tool output file).

## Files to Ignore (All Agents)

All agents MUST ignore these files (note existence only, never read or analyze):

- **Binaries:** *.exe, *.dll, *.so, *.dylib, *.bin
- **Build outputs:** dist/, build/, target/, out/, bin/, obj/, *.pyc, *.class, *.o
- **Dependencies:** node_modules/, vendor/, venv/, .venv/, __pycache__/, .gradle/, .m2/
- **Archives:** *.zip, *.tar, *.gz, *.jar, *.war
- **Media:** *.png, *.jpg, *.gif, *.mp3, *.mp4, *.pdf
- **IDE:** .idea/, .vscode/, *.iml

This convention is defined here once. Individual agent definitions do NOT need to repeat it.

## Bloat Prevention (Global Agents + Skills + GEMINI.md)

Before adding or modifying content in any global agent file, global skill file, or GEMINI.md itself:
1. Apply the bloat checklist: `C:/Users/dexte/.gemini/skills/quality-guardian/CHECKLISTS.md` → "For Global Agents / Skills / GEMINI.md"
2. **SCOPE:** This rule applies ONLY to `GEMINI.md` and any agents/skills that are NOT available in Claude (as tracked in the `claude-bridge` skill).
3. Project agents (`agent-nla-*`, etc.) are exempt — their specificity is intentional.

## Memory vs Skill Routing Rule

Before saving anything to auto-memory, check if it belongs in a skill first:

- **Conventions, field mappings, workflow rules, domain knowledge** → edit the relevant skill file instead
- **User behavioral overrides** (e.g. "always do X instead of Y") → memory
- **Personal/project-specific data** (file locations, project paths) → memory
- **Reference data used globally across projects** (team lists, account IDs) → relevant skill
- **Jira-related items specifically**: check `C:/Users/dexte/.gemini/skills/jira/SKILL.md` first

Saving to memory is faster but the wrong default. Skills are the right home for anything that would apply to anyone using the same system.
