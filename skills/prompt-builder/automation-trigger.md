# Template: Automation-Trigger / Cron Prompt

For recurring pipeline trigger prompts: the text passed to `/loop` or a cron scheduler that kicks off a self-improving multi-agent pipeline each cycle.

**Length guidance:** Keep under 300 words. This text runs every cycle — it must be scannable in one read.

**Rules:**
- All file paths must be absolute — cron has no working directory context
- Name the entry-point agent explicitly — do NOT enumerate all downstream stages
- State the Iron Rule verbatim — it must be in context before the orchestrator reads the constitution
- Include rate limits or budget caps if applicable
- Do NOT embed agent routing logic — that belongs in the orchestrator agent definition
- Do NOT repeat what the constitution already defines — just reference the constitution path

---

## Interview Questions (ask before building)

1. What is the project root? (absolute path)
2. What is the entry-point orchestrator agent name?
3. What are the key state files? (run-log, blocked-log, output file, dedup file — absolute paths)
4. What are the domain parameters? (targets, filters, constraints specific to this pipeline)
5. Are there rate limits or budget caps per run?
6. What is the Iron Rule fallback for this pipeline? (e.g. "use Google Search instead of direct fetch")
7. What is the output constraint? (append-only? never overwrite? max calls?)

---

## Structure

The prompt is a flat key-value block followed by a single instruction. No markdown headers inside the prompt — avoids rendering artifacts eating context each cycle.

```markdown
Project root: [absolute path]
Constitution: [absolute path]/docs/PIPELINE-CONSTITUTION.md
[Key file label]: [absolute path]
[Key file label]: [absolute path]
[Key file label]: [absolute path]

Spawn agent: [entry-point orchestrator agent name]

Instruction: Run one full pipeline cycle now. The [entry-point agent] owns all routing. Pass the current timestamp as the run ID.

[Domain parameter label]: [value]
[Domain parameter label]: [value]
[Domain parameter label]: [value]

Iron Rule: The pipeline MUST always produce something. If any stage fails, log the failure to [blocked-log absolute path], use a fallback ([specific fallback]), and continue. Never exit early or abort the run.

Output rule: [e.g. Append new rows to output/file.csv only — never overwrite. Max N WebFetch calls this run.]
```

---

## What NOT to Include

| Do not include | Reason |
|---|---|
| Stage sequence (Planner → Researcher → ...) | Orchestrator reads this from the constitution each run |
| Full agent roster | Orchestrator routes — enumerating stages in the prompt creates drift |
| Quality standards | Already in PIPELINE-CONSTITUTION.md |
| Kill switch conditions | Orchestrator reads them from the constitution |
| Site lists, query lists | These are operational parameters owned by the Planner agent |

---

## Local Agent Scaffolding — Refiner Runtime Knowledge

When the prompt-builder scaffolds local agent definitions alongside the prompt, the **Refiner agent** must include an explicit runtime section. The Refiner is the only agent that modifies pipeline behavior over time — it needs to understand how the pipeline starts, stops, and restarts to avoid making changes it cannot apply or recover from.

Add this block to the Refiner agent definition under a `## Runtime Environment` heading:

```markdown
## Runtime Environment

This pipeline runs inside **Gemini CLI** via `/loop`. Key facts that affect what you can and cannot do:

- **How it runs:** `bash run-pipeline.sh [interval]` reads `docs/automation-prompt.md` and
  passes its contents to `/loop`. The human always restarts via this script — never by pasting
  the prompt manually.
- **Session-bound:** `/loop` stops if the Gemini CLI session closes or times out. This is
  expected behavior. The human runs `bash run-pipeline.sh` to resume. Do not treat a gap in
  run-log entries as a pipeline failure — it likely means the session ended.
- **Prompt revision gate:** You MUST NOT write to `docs/automation-prompt.md` directly.
  If a PROMPT_REVISION entry is accepted: write your proposal to `docs/prompt-proposal.md`,
  mark the change-request entry `PENDING_HUMAN_REVIEW`, and stop. The human reviews the
  proposal and runs `bash apply-prompt.sh [run_N]` to apply it. You will see
  `docs/.last-apply-timestamp` updated on a future run — that is your signal to mark the
  entry `APPLIED — Run N`.
- **Subagents have no MCP access:** Any MCP tools available in the main Gemini CLI session
  are not available to agents you spawn. Design fallbacks accordingly.
```

This section belongs in every project's Refiner agent definition. Without it, the Refiner may attempt to directly edit `docs/automation-prompt.md`, misinterpret run gaps as failures, or design agent workflows that assume MCP access.

---

## Finalization

- Platform-specific to Gemini CLI `/loop`. Portability is secondary to completeness.
- Save as `docs/automation-prompt.md`. Note in the header that the Refiner may update it as the pipeline matures.
- **Restart:** Always via `bash run-pipeline.sh [interval]` — never paste the prompt manually. `/loop` is session-bound; if the session closes, `bash run-pipeline.sh` resumes it. For pipelines that must survive session restarts, recommend wiring to n8n or another persistent scheduler.
- **Prompt revision gate:** After the pipeline is running, the Refiner proposes changes via `docs/prompt-proposal.md` — it never writes to `docs/automation-prompt.md` directly. Human reviews and runs `bash apply-prompt.sh [run_N]` to apply. Tell the user about this gate at handoff.  

---

## Pedagogical Boundary Rule

For enhancement pipelines that score output with a rubric: the enhancement agent definition MUST include this boundary rule in the rubric section. Any Pedagogical dimension that rewards vocabulary tables, analogies, learning ladders, practice exercises, or "What to Learn First" tables will cause the agent to add content owned by `agent-concept-tutor`. That content adds tokens every invocation without improving agent behavior.

Include verbatim: *"Pedagogical content in a skill file must help the agent perform the task, not teach a human the tool domain. Vocabulary, analogies, practice exercises, and learning ladders are concept-tutor's domain — do not add them to skill files."*
