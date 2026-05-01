# Checklist: Gemini CLI System Design

Use when reviewing agent definitions, skill files, GEMINI.md, or any multi-agent workflow design. Run alongside `CHECKLIST-agents-skills.md` (bloat/layer ownership) — this checklist covers execution model correctness, not organization.

---

## Token & Context Efficiency

- [ ] **Subagent output is condensed?** Subagents return summaries (1–2K tokens), not raw file contents or full conversation history. *Fail: subagent dumps entire file reads or tool output verbatim into its return value.*
- [ ] **Spawn prompts are scoped to 3 elements only?** Task objective + input paths + output format. Background context the agent definition already covers must not be repeated in the spawn prompt. *Fail: spawn prompt re-explains the agent's role, re-states conventions from GEMINI.md, or provides context the agent file already defines.*
- [ ] **No decorative diagrams in agent or skill files?** Diagrams serve human readers, not agents — they add token cost without improving agent behavior. *Fail: ASCII flow diagrams, architecture diagrams, or visual layouts embedded in agent definitions or skill files. Exception: simple structured trees that encode branching logic the agent directly acts on (e.g., a verdict decision tree).* 
- [ ] **Skills are deferred — not pre-loaded at every spawn?** Skills load only when the relevant content type or task is active. *Fail: agent definition instructs loading a skill unconditionally on every spawn regardless of task type.*
- [ ] **Subagent spawned only when justified?** Subagents are used when: (a) the subtask reads many files, or (b) it produces verbose output that would pollute the main session. Tasks reading fewer than 3 files with no intermediate artifacts should run in the main session. *Fail: subagent spawned for a simple lookup or single-file read.*
- [ ] **MCP tools used in main session only?** No agent definition assumes subagents have MCP access. Subagents use file reads, Bash, and other non-MCP tools only. *Fail: subagent workflow calls `mcp__*` tools or assumes Jira/Confluence access.*

---

## Agent Contract Clarity

- [ ] **Single clear responsibility?** The agent's purpose can be stated in one sentence without "and also". *Fail: agent definition lists 3+ unrelated responsibilities; combines orchestration with implementation.*
- [ ] **Decision boundaries declared?** The agent states what it decides autonomously vs. what it escalates to human or routes to another agent. *Fail: no escalation condition defined; agent handles all cases including unknown ones without a fallback.*      
- [ ] **Failure mode defined?** The agent specifies what to do when input is missing, malformed, or incomplete — not just what to do in the happy path. *Fail: agent definition only describes the success path; no mention of what happens if expected files don't exist or input is empty.*
- [ ] **Input/output contract explicit?** What the agent expects (file paths, format, context) and what it returns (format, length, verdict structure) are both stated. *Fail: agent spawned with "do the task" — no input format, no output format defined.*   
- [ ] **Model selection appropriate?** Use `gemini-1.5-pro` for complex reasoning/review, `gemini-1.5-flash` for implementation/writing, or simpler models for quick detection/classification. *Fail: simple model used for a nuanced multi-step review; complex model used for a simple lookup.*

---

## Skill Design Correctness

- [ ] **Trigger description is testable?** Given a user message alone, it is unambiguous whether this skill applies. *Fail: trigger says "use when relevant" or "use for X tasks" without specifying what X looks like in practice.*
- [ ] **Explicit "Do NOT trigger" cases defined?** The skill description states what it does NOT apply to, preventing over-firing. *Fail: skill has trigger conditions but no exclusions — adjacent use cases will incorrectly load it.*
- [ ] **Content is exclusively non-native knowledge?** Skill contains only what Gemini cannot know without it: project conventions, domain rules, proprietary mappings. Standard language syntax, general patterns, and common frameworks are excluded. *Fail: skill documents Python syntax, REST principles, or other knowledge Gemini already has.*
- [ ] **Local vs. global path explicitly chosen?** Project-specific skills go in `.gemini/skills/` (project root). Reusable cross-project skills go in `~/.gemini/skills/`. The choice is deliberate, not default. *Fail: skill placed in global path but references project-specific paths or names; or placed in local path but intended for all projects.*

---

## Multi-Agent Handoff Quality

- [ ] **Handoff artifact is explicit?** When agent A produces output for agent B, the exact artifact (file path, format, section name) is named — not implied. *Fail: agent A "returns findings" without specifying what file or format agent B will read.*     
- [ ] **No shared mutable state between agents?** Agents do not write to the same file concurrently. If a file is shared, one agent owns it and the other reads it only after the owner completes. *Fail: two parallel subagents both append to the same log file or update the same config.*
- [ ] **Iteration / retry limits defined for every routing loop?** Every REVISION_NEEDED routing path has a max iteration count. No loop is open-ended. *Fail: workflow says "route back to engineer until fixed" with no cap.*
- [ ] **Routing verdicts exhaustive?** Every possible agent output maps to a defined next step. There is no verdict value that leaves the workflow in an undefined state. *Fail: workflow handles APPROVED and REVISION_NEEDED but not BLOCKED; agent can return a verdict with no route.*

---

**Verdict guidance** (global default applies — see CHECKLISTS.md)
