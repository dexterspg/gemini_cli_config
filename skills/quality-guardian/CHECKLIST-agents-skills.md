# Checklist: Global Agents / Skills / GEMINI.md (Bloat Prevention)

**Core principle:** Each piece of information lives at exactly one layer.

| Layer | Owns | Does NOT own |
|-------|------|-------------|
| GEMINI.md | Routing triggers (one row per workflow), cross-agent conventions (apply to ALL agents) | A workflow's steps (they live in `skills/workflows/<name>.md` at any length), individual agent behavior, flag definitions, single-agent rules |
| Generic agent | Agent-specific behavior, process, output format | Conventions already in GEMINI.md, behavior identical to another agent |
| Project agent | Project-specific paths, names, constraints — **intentionally specific, skip path checks** | Generic behavior already in a parent generic agent |
| Skill | Proprietary/project-specific knowledge Gemini cannot know natively | Standard language syntax, patterns Gemini already knows |
| Hook (`hooks.json`) | A rule that must hold every time, enforced outside the model | Preferences and judgment calls (GEMINI.md is context, not enforcement) |

## For Generic Agent Files

- [ ] **Repeats Learning Preferences from GEMINI.md?** *Fail: any rule that applies to all agents appearing verbatim in an individual agent file — costs tokens on every spawn.* → Remove (add one-line reference to GEMINI.md)
- [ ] **Repeats file ignore rules or cross-agent conventions from GEMINI.md?** *Fail: same as above — cross-agent rules belong at the GEMINI.md layer only.* → Remove
- [ ] Any rule appears word-for-word in another generic agent? → Extract to shared skill, reference from both
- [ ] A folder structure tree duplicates the authoritative copy in another agent? → Remove from secondary agent, keep in the agent that owns that pipeline stage
- [ ] Adds any new behaviour (an agent, skill, rule, hook or route), changes an agent's role line, splits or folds an agent or skill, or sets up a reviewer panel? → Answer the Decision guide in `~/.gemini/skills/quality-guardian/EVIDENCE-agent-design.md` first, then check the change against its rules; a claim marked unverified there never decides. Predicate for the identity-line rule: `rg -n -i '^(you are|act as) ' ~/.gemini/agents` prints nothing.
- [ ] Before committing an edit under `agents/`, `skills/` or `GEMINI.md`: `python -X utf8 -I C:/Users/<username>/.gemini/skills/quality-guardian/scripts/config_check.py` exits 0. Exit 1 = problems listed with file and line; exit 2 = not checked (git, PyYAML or `agents/` unavailable), never a pass. It covers frontmatter, identity lines, removed names, unknown `agent-*` names and the agent count, and skips itself in one line when nothing is uncommitted; add `--all` to re-check committed work. When an agent or skill is removed or renamed, add its name to the `REMOVED` list at the top of the script in the same commit.

**Project-specificity checks (generic agent files only — see exemptions below):**

- [ ] Examples use hardcoded project paths (`~/git0/`, `C:/core2/`, project names like `nakisa`, `nla`, `nfs`)? → Replace with `{project-root}` placeholder
- [ ] Examples use project-specific names (real ticket IDs, real customer names)? → Replace with generic placeholders like `PROJ-123`, `Acme Corp`
- [ ] Examples use framework-specific or stack-specific vocabulary (class names, annotations, tool names from a specific technology — e.g. `MockBean`, `@Transactional`, `pytest.fixture`)? → Replace concrete nouns with generic labels (`MockDependency`, `@TransactionBoundary`, `test-fixture`).
- [ ] Examples or rules assume a specific project structure (package layout, directory conventions, config file locations)? → Replace with generic descriptions.

**Do NOT flag as bloat:**

- **Project agents** (`agent-nla-*`, etc.) — specificity is intentional, skip all path/name/vocabulary checks
- **Functional workspace paths** (sandbox root, time-tracker script path, timelog path) — these are user configuration, not examples
- **Same data serving different purposes** in different agents (e.g., routing table in orchestrator + issue type definitions in quality-guardian — they are not duplicates, they serve different roles)
- **Project-specific detection rows** in generic agents (e.g., NLA row in qa-engineer) — functional guidance, not bloat
- **Stack-specific vocabulary in stack-scoped skill files** — if a skill file is explicitly scoped to a technology, framework vocabulary matching that scope is not a violation

## For GEMINI.md

- [ ] A delegation section describes flag behavior (what the flag does) beyond trigger conditions (when to use the flag)? → Move behavior to agent file, keep only triggers in GEMINI.md
- [ ] A delegation section describes agent-internal process? → Move to agent file
- [ ] A "Shared Agent Conventions" rule applies only to one specific agent, not all? → Move to that agent's file
- [ ] GEMINI.md holds a workflow's ordered steps, or a row re-describes behavior defined in the target agent or workflow file? → Move the steps to `skills/workflows/<name>.md`; trim the row to agent/workflow name + context to pass
- [ ] **GEMINI.md exceeds 200 lines?** *Fail: file length > 200 lines. Every line costs tokens on every single interaction.* → Audit for content that belongs in agent definitions or skill files and migrate it.

## For Workflow Skill Files (`skills/workflows/`)

- [ ] Workflow skill file has only one step (a single delegation)? *Fail: it is a route, not a workflow.* → Point the GEMINI.md trigger row at the agent (with flags) and delete the file; two or more steps stay in the skill file at any length. Authoring-time only.
- [ ] Workflow skill file is missing a Steps or Flow section? *Fail: no actionable steps — file is incomplete.* → Add the steps before merging

## For Skill Files

- [ ] Documents something Gemini answers correctly with no skill loaded (language syntax, public frameworks and standards)? → Remove
- [ ] Lists an inventory of agents or skills (except `claude-bridge` registry)? → Remove; the filesystem is the source of truth
- [ ] Holds temporary task context? → Move it to project docs or the conversation
- [ ] **Does a skill's frontmatter fail to load?** *Fail: the opening `---` is not line 1, UTF-8 BOM is present, the YAML does not parse, or a key is not a documented field.* → Run `python -I ~/.gemini/skills/quality-guardian/scripts/check_frontmatter.py ~/.gemini/skills`.
