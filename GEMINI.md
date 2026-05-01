# Scratch Pad

**File:** `C:/Users/dpagkaliwangan/scratch.md` — global temporary notes, single file, organized by topic sections.

**Commands:** "add to scratch: ...", "show scratch", "clear scratch [topic]", "wipe scratch"

When adding from emails/messages: strip greetings and sign-offs, keep only actionable info.

---

# Jira & Data Analysis Skills

This document defines the consolidated Jira operations and data analysis standards for this workspace.

## Core Mandate: Skill Priority
**HARD RULE:** For ALL Jira operations, data cleaning, and technical migrations, prioritize the dedicated skill files over this document.
- **Jira:** `C:/Users/dpagkaliwangan/.gemini/skills/jira/SKILL.md`
- **CSR Tickets:** `C:/Users/dpagkaliwangan/.gemini/skills/jira/csr/SKILL.md`
- **Migration:** `C:/Users/dpagkaliwangan/.gemini/skills/migration/SKILL.md`

## 2. Universal Migration & Parity Standards

#### Verbatim Copying & Compatibility Protocol
- When asked to copy a skill or agent from another system (e.g., Claude), the copy must be **verbatim, word-for-word, and line-for-line**.
- If any part of the source is suspected to be incompatible with the current environment (e.g., tool mismatches, missing dependencies):
  - Do **NOT** silently modify the content during the copy.
  - Identify and **flag the exact word and line differences** to the user for review.
  - Review compatibility **section by section** before proceeding.
  - If a dependency (like a skill or agent) is missing, propose creating a Gemini-suitable equivalent rather than omitting the instruction.

---

# Git Commit Rules

- Write a single sentence describing what was done (imperative, plain English)
- Never include `Co-Authored-By` or any author attribution lines
- Always push to remote after committing
- **Always ask for user permission before committing** — never auto-commit
- **Never commit or push in:** `C:/Users/dpagkaliwangan/git0/`, `C:/Users/dpagkaliwangan/git/`, `/c/core2/`
- **Sandbox/notebook commits:** Describe what was learned/built/captured, never reference production-specific terms. Frame around the concept, not the source.
  - Good: `Add stage 5: Retrofit2 HTTP clients with factory pattern and service abstraction`
  - Bad: `Migrate to production-accurate Retrofit matching NFS codebase`
- Example: `Add login form validation` or `Fix null pointer in payment processor`

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

- If an agent cannot access its primary model, it is permitted to use a different available model to complete the task.

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
