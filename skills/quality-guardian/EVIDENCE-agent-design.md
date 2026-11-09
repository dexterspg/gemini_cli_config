# Evidence: Agent and Prompt Design (Benchmark)

VERIFIED  2026-11-08 dp — sources read on that date; each claim below carries its own level.

**Use:** check any change against this file before you add or change an agent's role line, create, split or fold an agent or
skill, or set up a reviewer panel. Levels: **verbatim** (read on the page), **summary** (a fetch summary of the page, not
its words), **secondary** (someone else's write-up), **unverified** (seen, never confirmed). An unverified claim never
decides a change.

## Decision guide: main session, subagent, skill, or script

Use this before adding any agent, skill, rule, hook or route to the config. Ask in this order; the first yes decides. Levels are in the rules below.

0. **Does the model already do this without the rule?** Run the behaviour with and without the proposed text (5 runs, the model you use); if it already passes, add nothing. Local case: a one-writer clause changed nothing, 5/5 without it (rule 11).
1. **Is the sequence fixed and well defined** (parse, look up, route, draft)? A script, workflow or hook, not an agent loop (rule 13).
2. **Is the trouble picking the right tool?** Rewrite the tool descriptions and schemas first; an extra agent comes last (rule 12).
3. **Does it write shared state** (any file, ticket or record another step reads)? One writer at a time (rule 11): the main session by default; a subagent may be that single writer when its inputs are written files (PRD, spec, source) and nothing else writes at the same time, or for a permission boundary (rule 4).
4. **Would it flood the main context** (it reads far more than the answer needs)? A subagent that returns a short summary (rule 4). In Antigravity (`agy`), use the built-in read-only `research` subagent or the named specialist agent.
5. **Are the parts independent and read-only?** Parallel read-only subagents (`invoke_subagent` in a single turn); their results go to the main session to act on (rules 4, 11).
6. **Does the main session need a check on work it produced?** A fresh-context reviewer given the artifact and the rules, never the author's reasoning (rule 6).
7. **Is it team knowledge the model lacks** (your conventions, your tool's incidents)? A skill, kept short (rule 7).
8. **Otherwise, and always for small work** (one file, answer or cause evident, nothing to firewall): the main session, with the task and the tools a top practitioner would use (rules 1, 3, 9).

Raw access is bounded by this config's permission rules: client environments are read-only, write/commit gates confirm or refuse writes, keys never enter briefs.

## Gemini / Antigravity (`agy`) Native Architecture Notes

1. **Async Subagent Turn Boundary vs. Progressive Disclosure:** In Antigravity, every `invoke_subagent` call opens an asynchronous background conversation that wakes up the parent reactively on completion and re-loads global rules (`GEMINI.md`). Meanwhile, skills use progressive disclosure (only YAML `name` and `description` load until activated) and run inline in the main session with zero handoff loss. Therefore, single-agent execution in the main session is strictly superior for conversational workflows (`requirements-discovery` → `product-strategist`), formatting already-fetched data (`jira-content`), small 1-file edits, and coordinating `adversarial-review`.
2. **Platform-Enforced Sandboxing (`research` vs. `self` and `define_subagent`):** Unlike prompt-only boundaries, Antigravity's built-in `research` subagent runs in a read-only sandbox with no network access and zero MCP tools. Custom subagents defined via `define_subagent` can also set `EnableWriteTools: false`, `EnableMCPTools: false`, and `EnableSubagentTools: false` to enforce permission boundaries mechanically.
3. **Model Tiering (`flash_lite`, `flash`, `pro`, `inherit`):** Fast, deterministic gates (`agent-tech-detective`, `agent-time-tracker`) use `flash` (or `flash_lite`), while deep multi-file analysis and independent verification (`agent-debugger`, `agent-quality-guardian`, `agent-mentor`) use `pro` (or `inherit`).
4. **Workspace Modes (`Workspace: inherit | branch | share`):** Single-writer handoffs and read-only parallel subagents use `Workspace: "inherit"`. When parallel write experiments are explicitly needed, Antigravity supports `Workspace: "share"` or `"branch"` to isolate working trees without colliding on shared files.

## What we apply

1. **No identity lines.** Replace "You are a Senior X" with what to do. "Do not reliably improve accuracy" (Wharton, verbatim). The effect of a persona
   is "largely random" (EMNLP 2024, verbatim). Keep the tone and method words as instructions ("patiently, from first principles").
   Neither study measured tone.
2. **Describe the reader, never make the model the novice.** Low-knowledge personas (Toddler, Young Child, Layperson) cut
   accuracy (Wharton, verbatim). "Talk to me like I'm five" describes the reader, which that study did not test.
3. **Ask for a top professional's tools and steps, not their identity.** "tell me what tools someone top of the field…
   would use… I want you to use the same tools" (Felix, user-pasted transcript).
4. **One agent by default.** Use a separate context only for: reading far more than the main session needs, parallel
   independent work, independent verification, a permission boundary, or a bridge to an outside tool (kit README, verbatim;
   Jan 2026 blog, verbatim).
5. **Never split by job title.** "Copy of their org chart" is the anti-pattern. Each handoff "hands back a lossy summary"
   (Oct 2026 article, verbatim).
6. **Reviews: attack briefs plus a judge, not characters.** Separate threads try to break the work, and another thread judges.
   "I rarely want the current session to judge itself" (Felix, verbatim). Run a panel only for high-stakes work: one
   briefed reviewer matched a 3-critic panel on a single script, and the judge pays only when several critics run
   (it removed 5 of about 22 raw claims; local test below). The reviewer's brief carries the artifact and the rules, never
   the author's reasoning: Cognition finds a review loop works "best when the coding and review agents do not share any
   context beforehand" (verbatim, 2026-04-22).
7. **Skills hold only what the model cannot know.** "Only add context the model doesn't already
   have." Match strictness to fragility (skill authoring guide, verbatim). Felix: "if you completely remove the skill, you
   actually get better output" and "the half life of a good skill is very short" (verbatim).
8. **Fold by measurement.** Measure, then merge the agents that always run together, then fold one at a time. Keep an agent
   only if the folded version scores worse. That means about 10 tasks with 2 to 3 reps (kit README, verbatim). Build evals
   before writing a skill, with a no-skill baseline and at least 3 scenarios, tested on each model you use (skill
   authoring guide, verbatim).
9. **Cost.** Multi-agent uses 3 to 10 times more tokens than a single agent (Jan 2026 blog, verbatim). Agents use about 4 times
   and multi-agent about 15 times the tokens of chat (research-system post, verbatim). Multi-agent pays only on high-value parallel work. Part of any multi-agent gain may be extra compute: with reasoning tokens held equal, single agents "consistently match or outperform" multi-agent systems on multi-hop reasoning (Tran and Kiela, arXiv 2604.02460, abstract only; the authors flag artifacts in API budget control, and the scope is multi-hop reasoning, not all work). The one speed figure is Anthropic's: parallelism "cut research time by up to 90% for complex queries" in its research feature (verbatim; not a general figure).
10. **A one-line role is defensible but unproven.** Prompting docs say a role in the system prompt focuses
    behavior and tone, and subagent examples open with "You are a senior code reviewer." followed by the real instructions. Neither measures a role against plain instructions.
11. **Parallelize reads; one writer.** (Models already do this by default: 5/5 without any clause, so it is guidance for editors, not text for `GEMINI.md`.) Subagents may read and think in parallel; the files, tickets and records other steps depend on are changed by one agent at a time. Cognition: "Actions carry implicit decisions, and conflicting decisions carry bad results" (verbatim, 2025-06-12), and its 2026-04-22 follow-up: multi-agent systems "work best today when writes stay single-threaded" (verbatim). Coding has "fewer truly parallelizable tasks than research" (verbatim). This config already complies: `scheduled-automation-routine` parallel dispatch is limited to stages that write different files; `CHECKLIST-gemini-code.md` forbids concurrent writes to one file; Hurl runs are serial.
12. **Fix tool descriptions before adding an agent.** "Even small refinements to tool descriptions can yield dramatic improvements"; consolidate and namespace overlapping tools (writing-tools post, verbatim). It gives no tool-count threshold; "10-15 tools" stays unconfirmed.
13. **A fixed, well-defined sequence is a workflow, not an agent.** "Workflows offer predictability and consistency for well-defined tasks" (building-effective-agents, verbatim). In this config the candidates are the small agents that wrap a script (`agent-time-tracker`): kept because the input is natural language, but nothing beyond parse, call and format should be added to them.
14. **Bound every loop and keep a human checkpoint.** "It's also common to include stopping conditions (such as a maximum number of iterations) to maintain control" and "Agents can then pause for human feedback at checkpoints or when encountering blockers" (building-effective-agents, verbatim). It gives no numeric step, token or cost caps. Already practised here: `scheduled-automation-routine` attempt cap (default 3) and the Hurl retry rules. A heavy subagent result can go to a file and come back as a reference ("Subagents call tools to store their work in external systems, then pass lightweight references back to the coordinator", research-system post, verbatim); the review threads return short summaries, so nothing here needs it yet.

## Sources

| Source | Date | Level |
|---|---|---|
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | 2024-12-19 | verbatim |
| [Multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | 2025-06-13 | verbatim |
| [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 2025-09-29 | verbatim |
| [When to use multi-agent systems](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them) | 2026-01-23 | verbatim |
| [When to fold subagents into your main agent loop](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop) | 2026-10-22 | verbatim |
| [single-agent-loop-kit README](https://raw.githubusercontent.com/anthropics/single-agent-loop-kit/c43796287b83bec847db923f07131d1cc8de750d/README.md) | 2026 | verbatim; marked "Not maintained", run twice |
| [Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | undated | verbatim |
| [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) | undated | verbatim to about 40k characters, then summary |
| [Create custom subagents](https://code.claude.com/docs/en/sub-agents) | undated | verbatim to about 40k characters, then summary |
| [Cognition: Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents) | 2025-06-12 | verbatim; third-party vendor |
| [Cognition: Multi-Agents, what's actually working](https://cognition.com/blog/multi-agents-working) | 2026-04-22 | verbatim; third-party vendor |
| [Single-Agent LLMs Outperform Multi-Agent Systems Under Equal Thinking Token Budgets](https://arxiv.org/abs/2604.02460) | 2026-04 | abstract only |
| [Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | 2025-09-11 | verbatim |
| [Felix Rieseberg, Silicon Valley Girl podcast](https://marinamogilko.co/episode/D-SVFneJ_Nk/) | 2026-10-20 | verbatim to chapter 10; the persona passage is user-pasted |
| [Felix Rieseberg, Latent Space](https://latent.space/p/felix-anthropic/) | Mar 17, year not shown | verbatim to about 40k characters; auto transcript |
| [Wharton: Playing Pretend](https://gail.wharton.upenn.edu/research-and-insights/playing-pretend-expert-personas/) | 2025-12-07 | verbatim; 6 non-Claude models |
| [Personas in System Prompts (arXiv 2311.10054)](https://arxiv.org/abs/2311.10054) | EMNLP 2024 | abstract only |

## Seen but not confirmed (do not use to decide)

- "Official guidance is to be careful with skills": a search summary only. The dev.to article it rests on does not say it.
- "Quality degrades at about 25% of the context window", "keep utilization at 60 to 80%", "anchored iterative summarization": no source found. Context engineering docs describe "a performance gradient rather than a hard cliff" (verbatim) and give no percentage.
- "98% of reliability comes from harness code" and "skills cut startup tokens by up to 94%": vendor figures, sources not opened.
- "Single-agent always beats multi-agent at equal tokens": the paper's scope is multi-hop reasoning with matched reasoning tokens, and its authors flag budget-control artifacts.
- "Reviewer sees only the final diff": Cognition says only that the reviewer shares no prior context; "only the diff" is the paste's gloss.
- "8 to 15" or "10 to 15 tools degrades reasoning" (two pasted summaries): docs say past "30-50 tool definitions" and treat 20+ tools as a specialization signal.
- "2x to 5x handoff overhead", "up to 94% fewer tokens with skills", "98% of system reliability", Stripe and Shopify architectures: from pasted summaries, sources not opened.
- "10x to 15x multi-agent tokens": a PDF whose provenance was not confirmed.

## Final roster (2026-11-08): what was done to each agent, and why

- **Removed / Folded into a skill:**
  - `agent-product-strategist`: folded into the `product-strategist` skill, run in the main session right after `requirements-discovery` (the Discovery Summary is already in the main session conversation, avoiding a lossy handoff; strict Mini-PRD limits added).
  - `jira-content-creator` (`agent-jira-content-creator`): converted into the `jira-content` skill (with templates kept decoupled in `skills/jira/templates/CONTENT-TEMPLATES.md`, no subagent spawn).
  - `agent-persona-reviewer` (and `persona-reviewer` skill): replaced by the `adversarial-review` skill (main session briefs 4 parallel read-only attack threads with tasks and concern checklists, never identities, and judges claims against the work).
- **Modified with a tested or checked defect:** `agent-concept-tutor` (Never list banned the files `--sandbox` writes; two contradictory section orders; restated Capabilities; Mojibake fixed), `agent-mentor` (Never banned explaining while `--teach-first` requires it; `color:` removed), `agent-implementation-engineer` and `agent-qa-engineer` (restated Capabilities and duplicate rules; the QA engineer's framework examples), `agent-data-analysis-expert` (mandatory `python -I` compute-by-script step before writing any figure), `agent-prompt-builder` (overlapping clauses applied together, never stop at first match), `agent-quality-guardian` (`CONFIG_ISSUE` routing to main session, `BLOCKED` escalation slot, file-read exception bounds).
- **Modified, identity line only:** `agent-codebase-archaeologist`, `agent-data-doc-specialist`, `agent-debugger`, `agent-note-taker`, `agent-support-investigator`, `agent-system-architect`, `agent-tech-detective`, `agent-time-tracker` (rule 1: personas do not reliably improve accuracy).
- **Kept as all 15 global agents because of rule 4:** archaeologist and debugger (read far more code than the answer needs), note-taker (permission boundary: owns notebook writes and branch safety), support-investigator (no-source-code boundary), quality-guardian (independent check), tech-detective and time-tracker (fast Flash gates), concept-tutor (fold test: no gain), implementation and QA engineers (file-based handoffs), system-architect, prompt-builder, data-analysis-expert, data-doc-specialist, and mentor (multi-turn Socratic session).
