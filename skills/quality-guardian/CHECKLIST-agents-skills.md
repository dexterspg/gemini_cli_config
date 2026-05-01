# Checklist: Global Agents / Skills / GEMINI.md (Bloat Prevention)

**Core principle:** Each piece of information lives at exactly one layer.

| Layer | Owns | Does NOT own |
|-------|------|-------------|
| GEMINI.md | Routing triggers, workflow definitions, cross-agent conventions (apply to ALL agents) | Individual agent behavior, flag definitions, single-agent rules |
| Generic agent | Agent-specific behavior, process, output format | Conventions already in GEMINI.md, behavior identical to another agent |
| Project agent | Project-specific paths, names, constraints — **intentionally specific, skip path checks** | Generic behavior already in a parent generic agent |
| Skill | Proprietary/project-specific knowledge Gemini cannot know natively | Standard language syntax, patterns Gemini already knows |

## For Generic Agent Files

- [ ] **[critical] Repeats Learning Preferences from GEMINI.md?** *Fail: any rule that applies to all agents appearing verbatim in an individual agent file — costs tokens on every spawn.* → Remove (add one-line reference to GEMINI.md)
- [ ] **[critical] Repeats file ignore rules or cross-agent conventions from GEMINI.md?** *Fail: same as above — cross-agent rules belong at the GEMINI.md layer only.* → Remove
- [ ] Any rule appears word-for-word in another generic agent? → Extract to shared skill, reference from both
- [ ] A folder structure tree duplicates the authoritative copy in another agent? → Remove from secondary agent, keep in the agent that owns that pipeline stage

**Project-specificity checks (generic agent files only — see exemptions below):**

- [ ] Examples use hardcoded project paths (`~/git0/`, `C:/core2/`, project names like `nakisa`, `nla`, `nfs`)? → Replace with `{project-root}` placeholder
- [ ] Examples use project-specific names (real ticket IDs, real customer names)? → Replace with generic placeholders like `PROJ-123`, `Acme Corp`
- [ ] Examples use framework-specific or stack-specific vocabulary (class names, annotations, tool names from a specific technology — e.g. `MockBean`, `@Transactional`, `pytest.fixture`)? → Replace concrete nouns with generic labels (`MockDependency`, `@TransactionBoundary`, `test-fixture`). For concepts with no generic noun equivalent, describe the behavior in plain English (e.g., "a framework-managed test double" instead of `@MockBean`).
- [ ] Examples or rules assume a specific project structure (package layout, directory conventions, config file locations)? → Replace with generic descriptions (e.g., "your configuration directory" instead of "the `config/` package").

**Do NOT flag as bloat:**

- **Project agents** (`agent-nla-*`, etc.) — specificity is intentional, skip all path/name/vocabulary checks
- **Functional workspace paths** (sandbox root, time-tracker script path, timelog path) — these are user configuration, not examples
- **Same data serving different purposes** in different agents (e.g., routing table in orchestrator + issue type definitions in quality-guardian — they are not duplicates, they serve different roles)
- **Project-specific detection rows** in generic agents (e.g., NLA row in qa-engineer) — functional guidance, not bloat        
- **Stack-specific vocabulary in stack-scoped skill files** — if a skill file is explicitly scoped to a technology (by name, path, or declared scope), framework vocabulary matching that scope is not a violation (e.g., `MockBean` in a Spring testing skill is correct)

## For GEMINI.md

- [ ] A delegation section describes flag behavior (what the flag does) beyond trigger conditions (when to use the flag)? → Move behavior to agent file, keep only triggers in GEMINI.md
- [ ] A delegation section describes agent-internal process? → Move to agent file
- [ ] A "Shared Agent Conventions" rule applies only to one specific agent, not all? → Move to that agent's file
- [ ] A workflow step re-describes behavior already defined in the target agent's file? → Trim to agent name + what context to pass

## For Skill Files

- [ ] Documents standard language syntax (Java, SQL, Python) Gemini already knows natively? → Remove
- [ ] Not referenced in GEMINI.md skill loading rules? → Verify it is still used before keeping
- [ ] Contains generic patterns not specific to the project/domain? → Remove; keep only proprietary patterns

## Token Cost Checks (all global agent and skill files)

Not all files carry the same cost — loading frequency determines trimming priority:
- **GEMINI.md** — loaded at every session start; every line costs tokens on every interaction
- **Agent definitions** — loaded each time that agent is spawned
- **Skill files** — loaded only when invoked; lowest per-session cost

Trim highest-frequency files first.

> **Hard rule — behavior must be deferred, not deleted.** Before removing any content, confirm that the behavior it encodes is already covered in a skill or agent definition that will be read when needed. If the content defines HOW something works (rules, flags, handoff instructions, ownership) and has no other home, it is load-bearing — do NOT trim it. Token savings are never worth behavior loss. The test: *"If this line disappears, will Gemini still do the right thing?"* If the answer is no or maybe, keep it.

- [ ] **[critical] GEMINI.md exceeds 200 lines?** *Fail: file length > 200 lines. Every line costs tokens on every single interaction — this is the highest-cost bloat possible.* → Audit for content that belongs in agent definitions or skill files and migrate it.
- [ ] **"Why" explanations restate the directive in different words?** → Remove. Keep rationale only when it contains information not inferrable from the directive itself (e.g., "without this, the Refiner can edit its own constraints"). If it just rephrases the check, it is noise.
- [ ] **Agent definition narrates process steps in tutorial depth?** → Trim to directives; verbose narration bloats every spawn without changing behavior.
- [ ] **Agent output instructions have no conciseness guidance?** → Add explicit direction: summaries over essays, targeted excerpts over full file contents.
- [ ] **Subagent spawn instructions include background context already in the agent definition?** → Trim spawn prompts to: task objective, input paths, output format only. Everything else the agent definition already covers.
- [ ] **A multi-agent chain is used for a task that reads fewer than 3 files and produces no intermediate artifacts?** → Consider collapsing to main session. If the subtask reads many files or produces verbose output, keep the subagent — isolation prevents that content from polluting the main session's context.

## Cross-Cutting Checks (when adding/modifying a dependency between skills/agents)

- [ ] Does the skill/agent have a `## Dependencies` section listing its direct dependencies? → Add one if missing
- [ ] Is the new direct dependency already reachable transitively through an existing dependency? → Prefer the transitive path unless: the caller uses this dependency in the majority of its execution paths *independently* of the intermediary.
- [ ] If preferring the transitive path, is the intermediate node's dependency structural (not incidental)? → Verify it would not be silently dropped during a future bloat cleanup. If fragile, document the assumption in the `## Dependencies` section.      

**Verdict guidance** (global default applies — see CHECKLISTS.md)
