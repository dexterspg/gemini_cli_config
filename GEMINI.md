# Scratch Pad

**File:** `C:/Users/dpagkaliwangan/scratch.md` — global temporary notes, single file, organized by topic sections.

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
- When asked to copy a skill or agent from another system, the copy must be **verbatim, word-for-word, and line-for-line**.
- If any part of the source is suspected to be incompatible with the current environment:
  - Do **NOT** silently modify the content during the copy.
  - Identify and **flag the exact word and line differences** to the user for review.
  - Review compatibility **section by section** before proceeding.
  - If a dependency is missing, propose creating a suitable equivalent rather than omitting the instruction.

---

# Git Commit Rules

- Write a single sentence describing what was done (imperative, plain English)
- Never include `Co-Authored-By` or any author attribution lines
- Always push to remote after committing
- **Always ask for user permission before committing** — never auto-commit
- **Never commit or push in:** `C:/Users/dpagkaliwangan/git0/`, `C:/Users/dpagkaliwangan/git/`, `/c/gemini-config/`
- **Sandbox/notebook commits:** Describe what was learned/built/captured, never reference production-specific terms. Frame around the concept, not the source.
  - Good: `Add stage 5: Retrofit2 HTTP clients with factory pattern and service abstraction`
  - Bad: `Migrate to production-accurate Retrofit matching production codebase`
- Example: `Add login form validation` or `Fix null pointer in payment processor`

---

# Public Domain Knowledge Standards

This section defines the mandatory standards for domain knowledge bases and architectural documentation across all projects.

## 1. Domain Knowledge Architecture (`knowledge/`)

The `knowledge/` directory is a pure, public-domain library. It must adhere to the following rules:

### 1.1. The Purity Rule (Standalone Concepts)
- **No Project Jargon:** Use of proprietary terms, project names, or internal service names is strictly prohibited in concept files.
- **Zero Frontmatter:** Concept files must not contain YAML frontmatter, technical metadata, or dates at the top. They must start immediately with the `<h1>` title.
- **Pedagogical Structure:** All concept documents must follow a 3-part pedagogical plan:
    1.  **The Problem:** Explain the business "Why" before the "What."
    2.  **The Analogy:** Use a non-technical comparison to build intuition.
    3.  **Key Terms:** Define industry-standard vocabulary in plain language.

### 1.2. The Metadata Bridge (`_metadata.md`)
- All project-specific context, implementation links, and technical metadata (Status, Last Updated) must reside exclusively in the domain's `_metadata.md` file.
- This file acts as the bridge connecting pure public concepts to the specific project implementation.

### 1.3. The Knowledge Puzzle (`_INDEX.md`)
- Concepts must be organized into a tiered roadmap:
    - **Level 1: Anchors:** Foundational business entities.
    - **Level 2: Engines:** Logic systems and core processes.
    - **Level 3: Operations:** Complex workflows and specific calculations.

## 2. Ownership and Authority

### 2.1. Strict Agent Authority
- **The Specialized Tutor:** Only a specialized `agent-concept-tutor` is authorized to generate or revise the content of the `knowledge/` folder.
- **No Fallback:** If the specialized tutor is unavailable, writing or revising knowledge files is strictly prohibited. The main session must halt the process and inform the user.

---

# Learning Preferences
When explaining new concepts:
- Gauge the learner first — adapt depth, vocabulary, and examples to their level and context
- Start with WHY — if this concept solves a problem or improves something, explain that problem first
- Build core understanding gently — use easy analogies, visual models, diagrams, or first principles before any technical depth
- Introduce vocabulary AFTER understanding is established — never front-load jargon
- Check understanding before advancing — pause to verify before adding complexity
- Include prerequisites as a bridge — after the core idea lands, mention what helps go deeper
- End with the 80/20 — highlight the 20% that matters most AND explicitly state what can be safely ignored for now

---

# Performance & Efficiency Mandates (All Agents)

To minimize latency (Turn Overhead) and maximize context longevity (Token Economy), all agents MUST adhere to these rules:

### 1. Consolidated Execution (The "One-Turn" Rule)
- ALWAYS combine related shell commands into a single `run_shell_command` call using chain operators (`;` for PowerShell).
- **Example:** `git add .; git commit -m "fix"; git push` instead of three separate turns.
- Batch independent read/search operations in parallel within the same turn whenever possible.

### 2. Lazy Loading & Search-First Policy
- NEVER read a file in its entirety unless it is under 200 lines or critically necessary for a surgical edit.
- ALWAYS use `grep_search` or `glob` to identify relevant sections of a file before calling `read_file` with specific `start_line` and `end_line`.
- If a file is over 500 lines, provide a technical justification in the thoughts before reading it.

### 3. Topic Summarization (Checkpointing)
- Use `update_topic` at the end of every major phase (Research, Execution, Validation) to provide a concise summary.
- These summaries act as "checkpoints" that allow the model to maintain state without needing to re-read every detailed tool output in the session history.

---

# Shared Agent Conventions

## Path Output Rules (All Agents)

**MANDATORY — no exceptions, no excuses.**

- ALWAYS write full absolute paths — never use `~`, `$HOME`, relative paths, or any shorthand
- ALWAYS expand to the full path e.g. `C:/Users/dpagkaliwangan/...`
- ALWAYS show the base directory on its own line FIRST, then the full file path on its own line SECOND
- NEVER inline a path within a sentence — paths always go on their own lines
- This rule applies every single time a path or file is mentioned, including in follow-up replies

Example: `C:/Users/dpagkaliwangan/.../folder/` on its own line, then `C:/Users/dpagkaliwangan/.../folder/filename.ext` on the next — never inline, never `~` or relative paths.

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
1. Apply the bloat checklist: `C:/Users/dpagkaliwangan/.gemini/skills/quality-guardian/CHECKLISTS.md` → "For Global Agents / Skills / GEMINI.md"
2. **SCOPE:** This rule applies ONLY to `GEMINI.md` and any agents/skills that are NOT available in Claude (as tracked in the `claude-bridge` skill).
3. Project agents (`agent-nla-*`, etc.) are exempt — their specificity is intentional.

## Memory vs Skill Routing Rule

Before saving anything to auto-memory, check if it belongs in a skill first:

- **Conventions, field mappings, workflow rules, domain knowledge** → edit the relevant skill file instead
- **User behavioral overrides** (e.g. "always do X instead of Y") → memory
- **Personal/project-specific data** (file locations, project paths) → memory
- **Reference data used globally across projects** (team lists, account IDs) → relevant skill
- **Jira-related items specifically**: check `C:/Users/dpagkaliwangan/.gemini/skills/jira/SKILL.md` first

Saving to memory is faster but the wrong default. Skills are the right home for anything that would apply to anyone using the same system.
