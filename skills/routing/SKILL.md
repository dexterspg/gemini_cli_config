---
name: routing
description: >-
  Detailed delegation rules for agent routing, workflow orchestration, and
  multi-agent handoffs. Use when CLAUDE.md routing index is insufficient and
  you need handler tables, document ownership rules, multi-step delegation
  flows, or single-agent vs workflow disambiguation. Triggers on: "which agent
  should handle this", "how to delegate this", "is this a workflow", "who owns
  the PRD", "ownership of [doc]", complex multi-agent handoff questions.
---

# Routing Skill — Detailed Delegation Rules

Load this skill when you need detailed execution rules for agent delegation, workflow orchestration, or multi-agent handoffs. The compact routing index in CLAUDE.md tells you WHAT to invoke; this skill tells you HOW.

**Do NOT trigger for:**
- Simple single-agent delegations covered by CLAUDE.md routing index
- Direct Agent tool invocations where the agent description is self-sufficient
- Skill content questions (load the relevant skill file instead)

---

## Jira Integration Details

Handler routing by user intent:

| User intent | Handler | How |
|------------|---------|-----|
| Search tickets, JQL queries, fetch ticket details | **Main session directly** | Call `mcp__jira__*` tools, display results using the format in the Jira skill |
| Generate content (KB articles, 5Q analyses, release notes) | **Main session** fetches data -> passes raw text to **jira-content-creator** subagent | Subagent formats only, no MCP calls |
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

## Orchestration Logic
- **Simple:** Use agent tool description.
- **Complex:** Orchestrate via workflow files in `skills/workflows/`.
- **Handoffs:** Writer self-checks (per skill) -> Quality Guardian reviews.

## Jira Routing
- **MCP Calls:** Main session only.
- **Formatting:** Pass raw data to `jira-content-creator`. Subagent handles release notes, articles, etc.

## Ownership
| Doc | Owner | Reviewer |
|---|---|---|
| PRD | product-strategist | quality-guardian |
| Spec | system-architect | quality-guardian |
| Design | ui-design | quality-guardian |
| Code | implementation-engineer | qa-engineer |

## Shared Intent Routing
- **Learning:** Routes to `agent-concept-tutor`.
- **Troubleshooting:** Routes to `agent-debugger` (issues/) or `agent-support-investigator` (logs/data).
- **Documentation:** Read `documentation-specialist/SKILL.md` -> delegate per agent-to-file table.
- **Data:** `expert` (scan) -> `specialist --profile` (report) -> `specialist --plan` (fix rules).

