---
name: routing
description: >-
  Detailed delegation rules for agent routing, workflow orchestration, and
  multi-agent handoffs. Use when GEMINI.md routing index is insufficient and
  you need handler tables, document ownership rules, multi-step delegation
  flows, or single-agent vs workflow disambiguation. Triggers on: "which agent
  should handle this", "how to delegate this", "is this a workflow", "who owns
  the PRD", "ownership of [doc]", "two skills both fit", "where does [X] live", complex multi-agent handoff questions.
---

# Routing Skill — Detailed Delegation Rules

Load this skill when you need detailed execution rules for agent delegation, workflow orchestration, or multi-agent handoffs. The compact routing index in GEMINI.md tells you WHAT to invoke; this skill tells you HOW.

**Do NOT trigger for:**
- Simple single-agent delegations covered by GEMINI.md routing index
- Direct subagent invocations where the agent description is self-sufficient
- Skill content questions (load the relevant skill file instead)

---

## When two skills or agents both fit

If two skills or agents plausibly fit a request, or a loaded skill says the job belongs to another,
tell the user in one line and continue with the best fit: "Heads-up: `A` and `B` both fit; I used `A`.
The overlap is the phrase '…'." The user decides whether to fix a description.

---

## Jira Integration Details

Handler routing by user intent:

| User intent | Handler | How |
|------------|---------|-----|
| Search tickets, JQL queries, fetch ticket details | **Main session directly** | Call `mcp__jira__*` tools, display results using the format in the Jira skill |
| Generate content (KB articles, 5Q analyses, release notes) | **Main session** fetches data, then loads the **jira-content** skill and formats it | The skill formats only; no MCP calls inside it |
| Create/copy/update/manage tickets | **Main session directly** | Call `mcp__jira__*` tools, follow confirmation rules in the Jira skill |

**Rules:**
- The main session MUST read `~/.gemini/skills/jira/SKILL.md` before any Jira operation
- Agent definitions at `/c/workarea/jira_manager/.gemini/agents/` must stay in sync with `~/.gemini/agents/`

---

## Document Ownership

| Document | Written by | Self-checks (before/during writing) | Reviewed by (after writing) |
|---|---|---|---|
| PRD (`docs/product-requirements.md`) | product-strategist | For Product Requirements checklist | quality-guardian |
| Tech Spec (`docs/technical-specification.md`) | system-architect | PRD <-> Tech Spec Sync checklist (mandatory, all modes) | quality-guardian |
| UI Design (mockup/wireframe) | ui-design skill | Against PRD functional requirements | quality-guardian (For Designs checklist) |
| Code | implementation-engineer | Tests pass | quality-guardian (For Code checklist) |

**Rule:** The writer self-checks alignment while writing. The guardian reviews independently after. Both use the same checklists but at different stages -- do not skip either.

---

## Single-Agent Delegation Table

| User intent | Agent | Notes |
|------------|-------|-------|
| Bug, error, unexpected behavior | agent-debugger | Saves to `{project-root}/issues/` |
| Debug registry/past investigations | agent-debugger | Reads `{project-root}/issues/README.md` registry |
| Write a PoC / Proof of Concept | Main session reads poc-writer skill -> gathers info from user -> writes `docs/POC.md` | Triggers: "write a PoC", "create a proof of concept", "PoC for [project]", "justify this idea", "should we build [X]" |
| Audit existing code architecture | Main session reads architecture-audit skill -> follows skill workflow -> writes `docs/architecture-audit.md` -> routes to quality-guardian | See architecture-audit-workflow |
| Add/edit/define/refine features or requirements | Run `requirements-discovery` skill first -> product-strategist skill (main session) | Pass Discovery Summary + project size hint (mini/standard/enterprise). For mini projects suggest mini-project-workflow; otherwise suggest feature-development-workflow. Triggers: "add feature", "define requirements", "review user stories", "refine user stories", "revisit the product requirement", "update requirements". |
| Review PRD for quality/completeness | agent-quality-guardian | Triggers: "QA the PRD", "check if PRD is complete", "review PRD for quality". Returns APPROVED / REVISION_NEEDED / BLOCKED. If REVISION_NEEDED -> route back to the product-strategist skill (max 2 iterations) |
| Create UI mockup, wireframe, or visual design | `ui-design` skill | Runs BEFORE system-architect; output path decided by main session |
| Write or implement code | Small change (one file, no spec needed): main session, with its test. Feature work from a spec (several files, or much code to read): agent-implementation-engineer | For feature work, follow with agent-qa-engineer unless user explicitly skips. Small work never goes through an agent chain (`quality-guardian/EVIDENCE-agent-design.md` → Decision guide, rule 9) |
| Write tests or test automation | Adding or fixing tests in one file: main session. A new suite or framework setup: agent-qa-engineer | Auto-detects stack; --unit for scripts/libraries, --e2e for UI, --api for APIs, --perf for load, --data for fixtures |
| Review content against requirements | agent-quality-guardian | Reads product-requirements.md + technical-specification.md; returns APPROVED/REVISION_NEEDED/BLOCKED |
| Understand business logic in code | agent-codebase-archaeologist --domain | |
| Create/update technical architecture | agent-system-architect | Reads product-requirements.md, creates/updates docs/technical-specification.md |
| Sync tech spec after PRD changes | agent-system-architect --sync | Pass PRD path + existing spec path |
| Verify implementation follows spec | agent-quality-guardian | With technical-specification.md as reference |
| Infrastructure, Docker, CI/CD, cloud | agent-system-architect --infra | |
| Extract logic into reusable AI prompt | agent-prompt-builder | |
| Create/update documentation | Read `~/.gemini/skills/documentation-specialist/SKILL.md` FIRST -> delegate to assigned agent per skill's agent-to-file table. Main session may only write after agent returns if minor edits are needed. | |
| Unknown/unfamiliar codebase | agent-tech-detective first | Then suggest archaeologist or onboarding workflow |
| Analyze/profile raw data (Excel, CSV) | agent-data-analysis-expert | Initial analysis and insights |
| Write data profiling report | agent-data-doc-specialist --profile | Observations only -- what's in the data |
| Write data cleaning plan | agent-data-doc-specialist --plan | Transformations and target schema |
| Full data pipeline (profile -> plan -> code) | Suggest data-cleaning-workflow | Or data-cleaning-reviewed-workflow for QA |
| Audit prompt/skill/agent for token efficiency | Load `~/.gemini/skills/token-efficiency-auditor/SKILL.md` | Triggers: "audit my prompt", "is this token efficient", "too verbose?", "optimize my system prompt", "check my SKILL.md" |

**Data triggers:** "profile this data", "clean this data", "what's in this CSV", "analyze this export", "data profiling", "cleaning plan", "data pipeline"

---

## Debugger Delegation Details

**Triggers:** "debug this", "I get this error", "check this error", "investigate this", "troubleshoot", "why is this broken", "this is failing", "console error", "stack trace", "exception", "something is wrong with", or when user presents a screenshot of errors or describes unexpected behavior.

**Handler:** Main session extracts error text and identifiers from screenshots (subagents cannot see images) -> spawns agent-debugger with extracted text + codebase paths, plus the canonical doc path if one exists. For multi-step workflows, suggest bug-fix-workflow instead.

---

## Concept-Tutor Delegation Details

**Triggers:** "teach me", "explain how", "what is", "how does", "walk me through", "help me understand", "continue teaching me", "where did we leave off", "resume my lessons on", "pick up where we left off" (when intent is LEARNING)

**Flags:**
- `--quick`: Triggers: "just explain quickly", "TL;DR", "short version"
- `--sandbox`: Triggers: "build me a sandbox", "runnable example of", "mini-app for X"
- `--walkthrough`: Routes to `agent-mentor --build` via `mentor-led-walkthrough` (not a concept-tutor mode). Triggers: "guide me through building this", "walk me through each phase", "teach me the implementation"

**Rules:**
- Multiple independent questions -> launch parallel concept-tutor instances (read-only teaching only; with `--notebook` run them one after another, since each hands a lesson to agent-note-taker and notebook writes have one writer at a time)
- Distinguish from archaeologist: structural map of unknown codebase -> archaeologist. Understand a topic -> concept-tutor
- Knowledge files as input: when user points to a knowledge directory, pass it to concept-tutor

---

## API Reference Delegation Details

**Triggers:** "document [product] API", "add [resource] to api reference", "map [endpoint] to internal code", "write API docs for [resource]", "reconcile API docs", "check API drift"

**Handler:** Main session loads `~/.gemini/skills/api-reference/SKILL.md` → checks for project supplement at `{project-root}/.gemini/skills/api-reference/SKILL.md` (or `.claude/skills/api-reference/SKILL.md`) → loads supplement if present → follows workflow.

**Agent roles:**
- Main Session — fetches external public API docs
- `agent-codebase-archaeologist` — traces endpoint to internal controller and service
- Main Session — applies the mandatory link contract and writes the file

**Do NOT trigger for:** Internal-only endpoints not in external docs (use `documentation-specialist`), conceptual API explanations (use `agent-concept-tutor`), domain concepts without an API anchor (use `domain-knowledge`).

---

## Domain Knowledge Delegation Details

**Triggers:** "discover domain knowledge in [path]", "document [concept]", "map intersections between [A] and [B]", "audit knowledge base", "update knowledge for [concept]"

**Handler:** Main session loads `~/.gemini/skills/domain-knowledge/SKILL.md` → consults routing index inside skill → delegates to the appropriate workflow.

**Agent roles:**
- Main Session (`search_web`) — live web research (research step in all documentation workflows)
- `agent-concept-tutor` — writes the concept `.md` file
- `agent-codebase-archaeologist` — codebase scan (discovery) and promotion to `documentation/platform/` (Option A)

**Do NOT trigger for:** Project-specific implementation details (use `documentation-specialist`) or general teaching without intent to create a permanent file (use `agent-concept-tutor` directly).

---

## Note-Taker Delegation Details

**CATCH-ALL:** Any mention of "notebook" routes to agent-note-taker in the appropriate mode.
Modes and triggers are defined in `agent-note-taker.md`.

**Routing exceptions:**
- "teach me X and save it" -> concept-tutor first, then note-taker fast capture (background)
- "teach me X, save it, and review it" -> notebook-creation-workflow (orchestrated)

Branch protocol: Read `~/.gemini/skills/notebook-branch-protocol.md` before any notebook write or branch switch.
