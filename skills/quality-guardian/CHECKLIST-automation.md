# Checklist: Scheduled Automation Skill (Autonomous Pipeline)

> **Note:** The Over-Engineering Guard's "drift from original problem" red flag does not apply here — bounded, evidence-gated pipeline evolution is expected behavior. Use checks C1 and C2 below to evaluate whether autonomous evolution is properly constrained.

Use this checklist when reviewing a `scheduled-automation-routine` skill document. These pipelines are **autonomous** — they run unattended on a schedule, self-improve via the Refiner agent, and are expected to produce output without human intervention. Do not flag healthy autonomous behavior (stage architecture changes, agent creation, constitution updates) as defects — verify instead that autonomous evolution is bounded and evidence-based.

### A. Safety & Boundaries

- [ ] **Immutable Guardrails section exists and is structurally protected?** The constitution defines a clearly demarcated section the Refiner must never modify, with explicit markers (e.g., comment delimiters). Human-only modification is stated.
  - *Why:* A Refiner that can edit its own constraints has no constraints. This is the only hard boundary between self-improving and self-unshackling.
  - *Fail:* No guardrails section; guardrails exist but no explicit Refiner prohibition; guardrails mixed into Refiner-owned sections without protection.
- [ ] **Refiner scope boundaries are explicit?** The document states what the Refiner CAN modify (constitution sections, stage architecture, local agents, local skills, automation prompt) AND what it CANNOT (global skills at `~/.gemini/skills/`, immutable guardrails, files outside project directory).
  - *Why:* Without explicit scope, "improve the pipeline" is unbounded — the Refiner could interpret it as editing global agents or creating files outside the project.
  - *Fail:* Only permitted actions listed (no prohibitions); prohibitions are vague ("don't change important things"); global/local skill boundary not addressed.
- [ ] **Prompt revision gate prevents direct prompt modification?** Prompt changes require human review before application, are backed up before overwrite, and produce a verifiable signal that application occurred. The Refiner must never write to the automation prompt directly — it proposes changes, a human reviews, and a controlled mechanism applies them. (Reference implementation: `prompt-proposal.md` → `apply-prompt.sh` → `.last-apply-timestamp`.)
  - *Why:* The automation prompt defines what the pipeline does. An autonomous agent rewriting its own mission without human review is the highest-risk mutation — more dangerous than guardrail edits because the prompt shapes every stage's behavior.        
  - *Fail:* No mention of prompt modification restrictions; Refiner can write to `automation-prompt.md` directly; no human review step; no backup mechanism before prompt changes.
- [ ] **Guardrail enforcement approach is stated?** The document specifies HOW guardrails are enforced: trust-based (Refiner instructions only), filesystem permissions, external monitoring, provider-level quotas, or a combination. For high-stakes pipelines, trust-based alone should flag for discussion.
  - *Why:* Trust-based enforcement is valid for low-stakes pipelines, but the reviewer needs to confirm it is a conscious choice, not an omission.
  - *Fail:* No mention of how guardrails are enforced; document implies enforcement without specifying the mechanism.
- [ ] **Audit trail enables post-hoc diagnosis?** The document defines log files sufficient to reconstruct what the Refiner changed, why it changed it, and what evidence it cited. At minimum: run-log (what happened), pipeline-log (what changed in the pipeline), blocked-log (what failed). Constitution includes an Improvement Log section.
  - *Why:* When an autonomous system makes a bad decision at 3 AM, logs are the only witness. Without them, the human cannot diagnose what went wrong without re-running.
  - *Fail:* No logging mechanism described; logs capture output but not Refiner reasoning/decisions; no way to trace a bad outcome back to the change that caused it.

### B. Reliability & Failure Handling

- [ ] **Error categorization distinguishes retryable from non-retryable failures?** Errors are classified into categories with different retry policies. Auth/credential errors are explicitly zero-retry. Unknown errors escalate to human, not to the Refiner.  
  - *Why:* A flat "retry N times" policy wastes compute on auth errors (which never self-resolve) and under-retries transient failures. Autonomous systems must be precise about which failures to absorb vs. escalate.
  - *Fail:* All errors treated identically; auth errors are retried; unknown errors routed to the Refiner for autonomous resolution.
- [ ] **Kill switch conditions are defined with concrete thresholds?** Pipeline-level HALT conditions abort the entire run (not just a stage) when the system is fundamentally broken. At least 2 conditions with numeric thresholds (e.g., N consecutive empty runs, N repeated actions, duration exceeding Nx expected). On HALT: log, mark as halted, wait for human — no autonomous recovery. Kill switch thresholds should reside in the immutable guardrails section or be otherwise protected from Refiner modification.   
  - *Why:* Without kill switches, an autonomous pipeline can loop indefinitely, burn API quotas, or run for hours. The Refiner cannot fix a broken pipeline from inside the broken pipeline. If thresholds are Refiner-editable, a capable Refiner could cite evidence to raise its own halt thresholds — effectively disabling its safety valves.
  - *Fail:* No kill switch conditions; conditions are vague ("if something seems wrong"); pipeline attempts autonomous recovery after a HALT; kill switch thresholds are in Refiner-owned sections without protection.
- [ ] **The Iron Rule (never block) is stated and operationalized?** An explicit rule that no missing dependency halts the pipeline. A concrete fallback pattern: log the block, use an alternative (template, placeholder, offline method), continue to next stage. Blocked-log format specified.
  - *Why:* The defining characteristic of this pipeline type is that it always produces something. Allowing early exit on missing API keys defeats the architecture's purpose.
  - *Fail:* No fallback strategy; fallbacks mentioned but no logging mechanism; stages can exit early and halt the pipeline.     
- [ ] **Non-interactive execution rule is stated?** All commands must run without interactive prompts (no `sudo`, no `--with-deps`, no UAC triggers, no interactive confirmations). Commands requiring elevated privileges must use alternative flags or be documented as one-time manual prerequisites.
  - *Why:* The pipeline runs autonomously with no human present. A command blocking on a permission dialog is a silent halt — downstream stages never execute, and no error is logged because the process is waiting, not failing.
  - *Fail:* No mention of non-interactive execution; commands use privilege-escalating flags without alternatives; interactive prompts treated as normal errors rather than pipeline design violations.

### C. Autonomous Evolution

- [ ] **Refiner changes are evidence-gated and rate-limited?** Modifications to the pipeline (constitution, stage architecture, agent creation) must cite specific evidence from run logs. Scope per run is limited (e.g., one targeted fix per run). Stage architecture changes are logged with evidence.
  - *Why:* An autonomous improver without evidence requirements makes speculative changes. Without rate limiting, it can restructure the entire pipeline in one run, making rollback impossible.
  - *Fail:* Refiner can make unlimited changes per run; changes do not require evidence; document says "improve as needed" without constraints.
- [ ] **Suspension/escalation policy exists for persistent failures?** A numeric threshold defines when the Refiner stops retrying a blocked item and marks it SUSPENDED for human resolution (e.g., 3 consecutive failures). When the primary path is blocked, the Refiner redirects to alternative productive work (self-directed work queue).
  - *Why:* Without a suspension threshold, the Refiner spends its budget retrying the same broken thing forever. The pipeline becomes an expensive retry loop instead of a productive worker.
  - *Fail:* No suspension policy; Refiner retries indefinitely; suspension exists but Refiner has no alternative work when the primary path is blocked.
- [ ] **Constitution starts empty — the Refiner fills it through observation?** Constitution sections (except Immutable Guardrails) begin as empty scaffolding with headers only. The document states the Refiner fills them after observing real output and failures.
  - *Why:* Pre-filled quality standards are assumptions, not learnings. The Refiner's value comes from discovering what matters for THIS specific pipeline through evidence.
  - *Fail:* Constitution sections pre-filled with generic standards; no clarification that the Refiner owns section content; no distinction between human-written (guardrails) and Refiner-written (everything else) sections.

### D. Human Communication

- [ ] **Feedback channels exist with distinct routing rules and complete status lifecycle?** The document defines separate channels for human input with distinct routing: quality/process fixes (Refiner acts autonomously) vs. prompt/mission changes (Refiner proposes, human applies). Status values cover the full lifecycle: OPEN → ACCEPTED/REJECTED/CONFLICTS/REROUTE → ADDRESSED/APPLIED/PENDING_HUMAN_REVIEW/PARTIALLY_ADDRESSED. Each status specifies who sets it (human or Refiner).
  - *Why:* Without channel separation, the Refiner cannot distinguish "fix a rendering bug" (act immediately) from "change the pipeline's goal" (propose only). Without complete status lifecycle, entries get stuck in limbo — blocking the Refiner or getting prematurely closed.
  - *Fail:* Single feedback file for all input types; no distinct routing rules; fewer than 5 status values; no rejection states; no intermediate states for entries requiring user action.
- [ ] **Phase 1 triage protocol is defined and runs before other Refiner work?** The Refiner reads feedback channels as its first action each run. Each OPEN entry passes through checks: REROUTE (wrong channel), guardrail conflict, learning conflict, then ACCEPTED. Triage results are logged to `pipeline-log.md` every run.
  - *Why:* Without triage, the Refiner might act on feedback that contradicts a guardrail, duplicates an existing learning, or was filed in the wrong channel. Triage is the Refiner's intake filter — skipping it makes the feedback system unreliable.        
  - *Fail:* No triage protocol; triage exists but is not logged; REROUTE check missing (wrong-channel entries are acted on); triage does not run before other Refiner work.

### E. Operational Completeness

- [ ] **Setup steps produce a runnable pipeline from zero state?** The document defines a setup sequence covering: permissions/settings, directory structure with seed files, agent definitions for core roles, empty constitution with guardrails, prompt generation via `agent-prompt-builder`, and the schedule command. A "first run with nothing built" scenario is described.
  - *Why:* An autonomous pipeline that cannot bootstrap itself is not autonomous. If Run 1 requires tribal knowledge not in the document, the skill fails its primary purpose.
  - *Fail:* Setup steps incomplete (e.g., no directory structure); first-run scenario not addressed; document assumes pre-existing agents/files without specifying how to create them.
- [ ] **Local vs. global skill boundary is enforced?** The document explicitly states the Refiner creates skills only in the project's `.gemini/skills/` directory, never in `~/.gemini/skills/`.
  - *Why:* Global skills are shared across all projects and human-managed. An autonomous Refiner writing to global skills would contaminate other projects' behavior. This is a blast radius control.
  - *Fail:* No mention of local vs. global skill paths; Refiner can create skills without specifying where; boundary implied but not stated.
- [ ] **Refiner agent definition includes runtime environment knowledge?** The Refiner agent must know: the pipeline runs via Gemini CLI (session-bound), `run-pipeline.sh` is the only valid restart mechanism, gaps in run-log mean session ended (not pipeline failure), and subagents have no MCP access.
  - *Why:* Without runtime knowledge, the Refiner misinterprets session gaps as failures, attempts direct prompt edits (bypassing `apply-prompt.sh`), or designs agent workflows assuming MCP availability. These are the most common Refiner miscalibrations.    
  - *Fail:* No `## Runtime Environment` section in Refiner agent definition; runtime facts are mentioned but incomplete; Refiner agent assumes persistent execution.

### F. Pipeline-Generated Artifact Quality

Applies when the pipeline produces local agent or skill files (e.g., an enhancement pipeline that creates or modifies `.gemini/agents/*.md` or `enhanced-skills/**/*.md`).

- [ ] **Pipeline-generated skill/agent files pass `CHECKLIST-gemini-code.md` before promotion?** Any local file created or enhanced by the pipeline must be verified against `CHECKLIST-gemini-code.md` — especially the "No decorative diagrams" check — before being promoted to global via `promote.sh`.
  - *Why:* Enhancement pipelines systematically produce ASCII state machines, sequence diagrams, and handoff diagrams because their rubrics reward visual cast/handoff sections. These diagrams are decorative for agent consumption and export bloat into global files shared across all projects.
  - *Fail:* No promotion gate defined; `promote.sh` copies files without a QG check; the constitution or skill describes promotion as purely human-gated without specifying what the human must verify.

- [ ] **Append-only constitution sections have a defined rotation policy?** The constitution's `What I Have Learned`, `Improvement Log`, and any periodic-sync log must specify a rolling window (recommended: keep last 10 runs inline) and an archive file path for older entries.
  - *Why:* These sections grow at ~10–20 lines/run. At 38 runs the constitution reached 272KB — approximately 68K tokens read by the Refiner every run. Without rotation, the constitution becomes the dominant token cost in the pipeline within 50–100 runs.
  - *Fail:* No archival strategy defined; sections say "append each run" with no rotation or archive rule; archive files are not defined or are read by the Refiner during normal runs.

- [ ] **Log files (run-log, pipeline-log) have entry format caps?** `run-log.md` entries must have a line cap (recommended: 15 lines max). Pipeline-log entries follow a structured format, not open-ended prose.
  - *Why:* Without format caps, log entries grow to 50+ lines of dense prose — duplicating information already in `proposals/` — and the Refiner reads the full file every run.
  - *Fail:* No line cap defined for run-log entries; pipeline-log entries are open-ended prose; the orchestrator or refiner has no instruction limiting entry length.

**Verdict guidance** (global default applies — see CHECKLISTS.md)
