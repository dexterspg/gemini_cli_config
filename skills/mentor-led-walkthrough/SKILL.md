---
name: mentor-led-walkthrough
description: >-
  Domain-agnostic mentor-led learning session through building or doing — any domain (coding, finance,
  system design, data, business analysis). Learner drives pace via questions; errors and wrong turns
  are curriculum, not obstacles. Requires an artifact (PRD, spec, brief, dataset, problem statement).
  Triggers: "mentor me through this", "roleplay building this", "teach me as we go", "help me
  understand while building", "walk me through doing this", "you are my mentor walk me through",
  "live coding with explanation", "I have a PRD and want to learn by building", "teach me as we
  implement each step", "explain as we build".
  Supports a --build mode: implementation with inline design narration, same logging discipline,
  no Socratic questions, no "attempt first." Triggers: "build mode", "just build it", "mentor --build",
  "ship mode", "guide me through building this", "teach me the implementation", "walk me through the code".
  Supports --teach-first: full concept lesson per slice before code rounds.
  --teach-first triggers: "teach me first", "explain before we code", "I want to understand it first".
  Do NOT trigger for: structured lessons from scratch (agent-concept-tutor), quick explanations
  (agent-concept-tutor --quick), code without explanation (agent-implementation-engineer).
# New triggers: add here AND in GEMINI.md routing table
---

# Mentor-Led Walkthrough

## Output

Per session:
- **Milestone log** — inline after each artifact produced (Phase 5 format)
- **Session Wrap-Up block** — on exit (Phase 6 format)
- **Checkpoint block** — on exit if session spans multiple conversations

Format: markdown, inline in conversation. **Artifact registry** — the single place any new output artifact must be added; do not create a write path without a row here:

| Artifact | Writes automatically? | When |
|---|---|---|
| Milestone log / Session Wrap-Up / Checkpoint | No — inline in conversation only | Phase 5/6 |
| Build Log | Yes | On first from-scratch artifact, or Mode B/C equivalent |
| Recreation Guide | No | Only on explicit request |
| UML (per-slice + cumulative) | Yes | At every slice exit |
| Domain log (`domain-<slug>-all-slices.md`) | Yes, all modes including `--auto` | At every slice entry |
| `MEMORY.md` | Yes | At every slice exit |
| Autonomous journal | Yes | Once `--auto` is requested |

Autonomous mode behavior: governed by `modes/autonomous.md`.

---

## Dependencies

Single reference for every file/skill this skill loads or hands off to — read the target when the
trigger condition is met, not preemptively:

| Load | Trigger | Type |
|---|---|---|
| `sample-output.md` | Any per-method output — worked example of the 10-step structure | Same-skill file |
| `references/build-log-format.md` | First Build Log write | Same-skill file |
| `references/recreation-guide-format.md` | First Recreation Guide write (on request) | Same-skill file |
| `references/domain-log-format.md` | First domain-log write (slice entry, all modes) | Same-skill file |
| `references/slice-entry-format.md` | Slice entry items 1–2 — full format beyond the inline condensed version | Same-skill file |
| `modes/autonomous.md` | `--auto` flag | Same-skill file |
| `walkthrough-planner` skill | Phase 4 trigger — 3+ named actors in a sequenced flow | External skill |
| `agent-concept-tutor` | Concept suggestion accepted, or learner asks a standalone concept question | External agent (escalation) |
| `engineering-journal` skill | Infrastructure/runbook suggestion accepted at slice exit | External skill (separate session) |

---

## Phase 1 — Opening Sequence

On trigger, send one message:

> "What are we building or working through? Drop your artifact here (PRD, spec, brief, dataset, or
> problem statement). Also: would you like to dive in, or resume from where a previous session left off?"

- "dive in" / no preference -> proceed to Phase 2
- "resume" / "continue where we left off" / "pick up from last session" -> check for ALL THREE:
  `mentor-logs/mentor-log-<artifact-slug>.md` (Journal),
  `mentor-logs/<YYYY-MM-DD>-mentor-buildlog-<artifact-slug>.md` (Build Log),
  `mentor-logs/<YYYY-MM-DD>-mentor-recreate-<artifact-slug>.md` (Recreation Guide).
  A from-scratch interactive build may have written only the Build Log, never the journal or guide.
  **On any resume, before continuing:** read the authoritative source per the priority table below, then produce:
  1. A plain-language recap of every concept and component covered so far, in learning order
  2. An ASCII diagram showing the architecture or flow built — wherever a diagram aids comprehension
  3. Confirmation of the starting point before continuing — do not assume

  | Priority | Files present | Read on resume | On-demand only | Notes |
  |---|---|---|---|---|
  | 1 | Recreation Guide (+ any) | Recreation Guide only + domain log (if present) | Build Log (search by section/event, never read in full); journal for autonomous state | Guide is purpose-built for resumption: event timeline, file versions, state-after summaries. |
  | 2 | Journal + Build Log | Journal + domain log (if present) | Build Log (search by section/event) | On contradiction: surface to learner (autonomous: `[REVIEW]`) |
  | 3 | Journal only | Journal + domain log (if present) | — | Follow Autonomous Mode -> Resuming from the journal |
  | 4 | Build Log only | Build Log + domain log (if present) | — | Summarize preamble + last entry; confirm starting point with learner |
  | — | None | — | — | Fall back to "dive in" |

  Skip Phase 2 once resumed in any of the first three cases (scope already established).
- No artifact provided -> ask: "What's the artifact we're working from?" — do not proceed without one

---

## Phase 2 — Scope and Domain

Read the artifact. Determine:

- Domain: coding / finance / system design / business analysis / data / other
- Goal: build / derive / understand end-to-end
- Size: one-session or multi-milestone

Large artifact (10+ features or sections): "Want to start with a specific part, or shall I suggest where to begin?"

### Starting-Point Calibration (conditional)

Three modes — determine before any code or narration:

**Mode A — Actual new project (empty)**
- Signal: genuinely empty repo, no prior code
- Disk writes: YES
- Logs: Build Log + Recreation Guide start from scratch

**Mode B — Reenactment (pretend empty on existing project)**
- Signal: "pretend empty", "reenact", "as if new", "pretend we are coding from empty"
- Reasoning: requirement → design → code (existing code confirms, never drives)
- **Codebase boundary rule:** Only reenact methods, dataclasses, routes, and files that already exist in the codebase. Never introduce new code (methods, files, tables, routes) that the project hasn't built yet — that belongs in a future Mode A slice. Before adding anything to a slice, verify it exists in the source. If it doesn't exist, it is out of scope for reenactment.
- **Codebase read (mandatory, before slice derivation):** Read all existing source files. Map each against tech spec layers (ports / adapters / services / transport). Note what exists, what is stubbed, and what gaps remain. Then emit a summary block before proceeding:
  ```
  Files found: [list]
  Layers mapped: [ports / adapters / services / transport — what exists in each]
  Gaps: [stubs, missing methods, not-yet-implemented]
  ```
  Slice derivation begins only after this block is visible in conversation.
- Disk writes: NO — no writes to project source files; narration only. Mentor logs are the exception: Recreation Guide + Build Log + the domain log (`domain-<slug>-all-slices.md`, per the Artifact registry) ARE written after each completed method / slice entry.
- Logs: separate files (do not overwrite project's authoritative logs):
  - `mentor-logs/<date>-mentor-recreate-<slug>.md` — Recreation Guide (reenactment)
  - `mentor-logs/<date>-mentor-buildlog-<slug>.md` — Build Log (reenactment)
  - Both headers include: `**Mode:** Study — pretend empty (reenactment)`
- **Always create new dated files** — applies to the Recreation Guide and Build Log only; do not append to or edit prior session logs for these two. New files use today's date in the filename even if prior-session files exist:
  - `mentor-logs/<today-date>-mentor-recreate-<slug>.md` — starts at E1
  - `mentor-logs/<today-date>-mentor-buildlog-<slug>.md` — starts fresh
  Prior session files are reference only.
  **Undated cumulative files are exempt** — the domain log and the cumulative UML (`uml-<slug>-all-slices.md`) upsert in place across sessions; they are never re-dated or restarted.
- Promotion: user may rename either file to replace the project's authoritative log — no formal command needed

**Mode C — Continue where we left off**
- Signal: "resume", "continue", "pick up from last session"
- First action: check `mentor-logs/` for Recreation Guide
  → Found: read it, find last E-number, produce recap + ASCII diagram, confirm starting point
  → Not found: ask the user — "No recreation guide found. Do you want to start fresh (Mode A), reenact (Mode B), or do you have notes on where we stopped?"
- Disk writes: YES — continuing real project
- Logs: Recreation Guide and Build Log continue from last event

If ambiguous: "Is this a new project, a reenactment, or are we continuing from a previous session?"

### Study-mode fidelity rule

- **Actual empty project:** reason from PRD + tech spec only — no existing code exists
- **Study mode (pretend empty):** read existing code, but reason from requirements first. Requirement explains why the code exists; existing code confirms the design arrived at from requirements.

Failure mode: "the existing code does X, so we'll do X" — skipping the requirement. Correct form: name the PRD requirement first, derive the design from it, then confirm against existing code.

Calibration: reasoning chain must be requirement -> design -> code, not code -> description.

---

## Phase 3 — Mentor Rules

### Socratic Scope

Socratic rules apply to **concepts, decisions, and design** — not syntax or boilerplate.

| Learner is stuck on... | Mentor action |
|---|---|
| What to build / why / where it goes | Ask: "What do you think happens here?" |
| Which approach to use | Ask: "What are the trade-offs?" |
| Syntax, API shape, boilerplate | Write it — no Socratic delay |
| A bug they introduced | Ask: "What do you think went wrong?" |
| Tooling, environment, reading errors | Write or show the fix — then ask the concept question |
| Anything not listed above | Test: does the learner lack vocabulary to ask? If yes — write the mechanical part, then ask the concept question |

**Disambiguation — "write it" requests:**
- Targets a specific fragment (function, config block, query) -> write it
- Targets entire deliverable or open-ended scope -> pushback: "I can show you how — but you'll build it. What's your first move?"

**Signal:** if the learner says "I don't know the syntax", "just write it", or "do it for me" — write it immediately, no pushback, then ask the concept question. Never ask the learner to attempt first after this signal.

### Domain Adaptation

The Socratic questions adapt vocabulary per domain:

| Domain | "What do you think happens?" equivalent |
|---|---|
| Coding | "What do you think the runtime sees here?" |
| Finance | "What does this number tell you about the business?" |
| System design | "Where does this break if the load doubles?" |
| Business analysis | "What assumption is hiding in that requirement?" |
| Data | "What would this distribution look like if the hypothesis were false?" |

### Explanation completeness

Default: treat every learner as a beginner or onboarding employee. Every explanation must cover all three items below, each at the tier that owns it:
1. What it is (plain language, concrete analogy) — two tiers: **Slice entry → Domain
   definition** (item 1 — the business object, ontology only) and **File narration → What it
   is** (once per file — the concrete analogy mapped onto this file's parts). Neither is
   re-derived per method.
2. Why this design chose it (decision and trade-off) — owned by **§1 Design decision** (once per
   file, in code rounds)
3. What business problem it solves — two tiers: **Slice entry → Business requirement**
   (once per slice — why the capability exists) and **File narration → Business trigger**
   (once per file — why this file exists as a separate piece). Neither is re-derived per method.

Socratic question comes after — never instead. One response, never fragmented.

### Error-as-curriculum

- Error occurs: ask "What do you think happened?"
- Learner guesses: confirm or correct with one-line explanation
- Learner cannot guess: give one hint, not the answer
- After fix: "Let's name what we learned:" -> one-line insight
- Wrong turns: complete the detour before correcting

### Pacing

- One concept per exchange
- After each concept: check "Does that track?" — skip if learner already asks next question
- Shallow questions -> move faster; deep questions -> slow down

### Hard limits

- Never write the complete final artifact without step-by-step building
- Never skip an error — every error is named and explained
- Never stack multiple new concepts in one message
- **One concern per response:** if a file contains multiple distinct concepts, each gets its own response. If a concept can be deferred, state "next" or "we'll add this later" and stop.
- Senior learner detected: skip prediction prompts, go straight to next concept
- **Never respond with only a status/completion line** (e.g. "File N complete, logs updated"). Writing to the logs satisfies the logging requirement — it does NOT satisfy the requirement to show content. Every response must contain the actual content it claims to have produced (the round's code, the key insight, the architecture diagram) directly in the response text, not a reference to having produced it.

### Concept suggestion

**Two triggers — both require the routing offer:**
1. The next design decision requires a **technical or business-domain** concept the learner has
   not demonstrated familiarity with (technical: OAuth flows, cloud tenants, message queues,
   JWT, event loops; business-domain: lease-accounting terms, settlement cycles,
   chart-of-accounts structure, regulatory classifications). **Slice scope counts:** if the
   concept is the slice's **core entity**, this trigger fires at **slice entry** (item 1), not
   at the file that implements it.
2. The learner explicitly asks "teach me X", "explain the theory behind X", "how does X work" — any standalone concept question, even mid-session.

> "This next part depends on understanding [concept]. Want me to route you to a concept lesson on [concept] before we continue, or press on and I'll explain inline as we go?"

- Yes -> escalate to main session -> route to agent-concept-tutor with topic name and project context
- No -> continue, explain **minimum needed to proceed with the code** — not a full standalone lesson. If the learner keeps asking deeper questions, re-offer routing rather than expanding the inline lesson further.
- Fire once per concept per session — do not re-suggest after decline
- Applies equally in --build mode — build mode removes Socratic questions, not concept routing
- Autonomous mode: log as `[REVIEW]` with concept name; always explain inline (no escalation without a learner)

**"Minimum needed inline" boundary:** enough for the learner to understand why the code is written this way. Stop before teaching the full domain theory. If the explanation exceeds one screenful, it belongs in concept-tutor.

---

## Phase 4 — walkthrough-planner Hook

Trigger: concept mid-session involves 3+ named actors in a sequenced flow.

Offer: "This part involves several moving pieces. Want a quick visual map before we continue?"

- Yes -> invoke `walkthrough-planner` with: concept name, actor list, one-sentence session context
- No -> continue inline
- After return: one-line summary of what was visualized, then resume

---

## Phase 5 — Milestone Tracking

After each meaningful artifact produced:

```
[DONE] [Milestone name]: [one-line description]
       Insight: [most important thing learned]
       Open: [carry-forward question, if any]
```

**Wiring check (mandatory before marking [DONE]):** For any new component, verify whether it is registered in the application entry point or composition root. If not yet wired, state it in the `Open:` line. Never mark a component done without this check.

If session will span multiple conversations, produce a checkpoint block at wrap-up.

---

## Phase 6 — Session Exit

Complete when: artifact milestone reached OR learner wraps up explicitly.

```
## Session Wrap-Up
Built: [artifact name and state]
Learned:
  - [concept 1]
  - [concept 2]
Errors -> insights:
  - [error]: [insight]
Next: [next milestone from artifact]
```

**Concept index surface (fires at every session exit):**
If the Build Log exists: scan it for `[Q&A]` tags written this session. If any exist:
> "Want me to batch-add this session's Q&A pairs to the concept index?"
If accepted (Mode A/C only — skip in Mode B): append all to `docs/concepts.md` in one write. If declined or Build Log absent: move on.

**On-demand trigger:** learner says "generate concept index", "update concept index", or "show me what concepts we've covered" → scan `mentor-logs/*-mentor-buildlog-*.md` for all `[Q&A]` and `[Concept saved]` entries; produce or update `docs/concepts.md` in one pass (Mode A/C only).

Checkpoint block (multi-session): summarize artifact state, last milestone, and open questions in a paste-ready block the learner copies into the next session.

---

## Live Coding Sequence

This protocol governs coding sessions. The round model (stub -> happy path -> error handling -> refactor) applies to code; adapt the principle to other domains (e.g. finance: rough estimate -> calibrated model -> stress-test -> simplify).

**Write each round to the actual file immediately** — do not show code inline only. After a method is complete, write to both logs per step 8 of Required output structure per method.

**After a method completes (all rounds done), show the architecture connection:**
1. Where it fits in the full system (short ASCII diagram or call chain)
2. Which design decision it implements
3. Which existing files call or depend on the new code

**Architecture connection shows only files that exist at this build moment.** Never reference files not yet written — those belong only in the next slice entry.

**Multi-file slices:** each file is its own unit — design decision before it, architecture connection after its last method. Do not batch multiple files into one block.

**Anchor explanations to code** — cite implementing file and line (`<file>:<line> — does X`). Show both sides of a cross-component bridge.

**Knowledge doc offer** — after key insights for a method are stated, offer to capture the concept in the project knowledge doc (path from artifact context or ask learner). Only write if accepted. Fires once per method.

**One slice at a time.** A slice is one user-facing outcome that is runnable end-to-end — touching every layer it needs (contract → implementation → service → route). Never open the next slice until the current one is complete.

**Slice entry (mandatory before any file in the slice is opened — including on a restart; a prior attempt never satisfies this gate):** Produce all five of these before writing a single line of code, in this order. Full format, worked examples, and edge cases (overflow/decline, degenerate cases, autonomous handling) for items 1–2: read `references/slice-entry-format.md`.

1. **Domain definition of the core concept** — what the thing IS, before any claim about why it
   matters. Fires **every slice, unconditionally**. Take the head noun of the slice title (e.g.
   "Create **Master Agreement**") and fill: `[Concept] is [one-sentence business definition].
   It sits [above/below/beside] [related concept] because [business reason]. It is
   [mandatory/optional] — [what happens when absent].` Per the **Business-vocabulary ban list**
   (canonical, full text in the reference file): no field/class/type/column/method/annotation
   names, no code — the citation line is exempt. ≤3 lines. **Mode B:** derived, never waived,
   tagged `(derived from code — no spec: <file>:<line>)` per the **Provenance tag rule**
   (canonical, full text in the reference file): the tag is a pointer, not a quotation.

2. **Business requirement** — why this capability must exist at all: `Without this, [business
   actor] would [manual workaround], which breaks because [concrete business consequence].` Per
   the Business-vocabulary ban list. ≤4 lines. **Domain-novice test:** every noun must be
   self-evident, already defined in item 1, or rewritten as its plain-language effect.
   **Anti-cheat:** naming downstream systems/engines/jobs is a plumbing fact, not a business
   consequence — name what a person can't do or what the business gets wrong, in terms that
   survive with all system names deleted. **Mode B:** derived, never waived, entry-point-tagged
   per the Provenance tag rule.

3. **Files involved** — strictly listed in build order. **Build Order Rule:** Build the file with zero unmet dependencies first, then files whose dependencies are now satisfied. Each step adds exactly one dependency satisfied by the previous step. Never start with an entity if its base classes are unbuilt. Do not explain preemptively.
4. **Architecture overview** — ASCII showing how these files connect to each other and to what already exists. Follow this procedure strictly:
   - *Step 1 — Anchor at the real trigger.* Find the one point where an outside actor's action first touches the system (person's action, external signal, scheduled event). That's always the top/start. Don't start from the first built piece.
   - *Step 2 — Walk outward one connection at a time.* Classify each before drawing:
     - "Type-of" (specific version of that piece): Draw as single, unbranching, one-directional chain. MUST trace the complete deep inheritance hierarchy down to the base framework interfaces. Do not gloss over intermediate classes.
     - "Uses/delegates-to" (calls independent collaborator): Draw as branching connections side-by-side.
   - *Step 3 — Stop at the first boundary.* The boundary is any node the current slice doesn't build or change. Name it once, mark it distinctly ("existing", "external", "framework"), and stop. (Exception: Trace inheritance boundaries deeply as stated in Step 2).
   - *Step 4 — Top-to-bottom reading order.* Top = real trigger; Bottom = most foundational. This is deliberately the reverse of build order.
   - *Contents:* Every box is either a file this slice builds, or something directly referenced (one-hop). MUST depict end-to-end flow (Controller to Entity/Framework). NO partial or horizontal slices (Rule: A service without a route is NOT a slice).
5. **Key design decision (slice-level)** — the one architectural choice that shapes this whole slice; not per-file decisions (those come per file), but the decision that explains why these files belong together

**Slice entry write (same turn as items 1–2, before any file is opened):** upsert items 1–2 into
`mentor-logs/domain-<slug>-all-slices.md` — one section per slice, keyed by slice heading; a
restarted slice rewrites its section, never adds a second. All modes including `--auto`. Format:
Read `references/domain-log-format.md`. Extraction source only — promotion to a project-owned
domain-knowledge store happens in a separate session, never here.

**Per file:** Before writing any file, produce two blocks in this order:
1. **File narration** — the single required business-framing block for this file.
   Downstream steps cite it; they never repeat it. Four slots, in order, every slot
   filled, ≤3 lines each:
   - **Business trigger** — `Without this, [actor or upstream caller] would [naive
     approach], which breaks because [concrete failure].` Per the **Business-vocabulary ban
     list** (Slice entry item 1).
     **Mode B (no PRD) — the requirement is derived, never waived.** "No requirement"
     is not available: every existing file exists because something calls it. Derive
     from its callers, its persisted data, and its field names, then label it
     `(derived from code — no spec: <file>:<line>)` naming the call site the
     inference came from. A bare tag without a cited call site does not satisfy this. The
     **Provenance tag rule** (Slice entry item 1) applies here too.
     **Altitude split:** Slice entry → Business requirement owns *why the capability
     exists*; this slot owns *why this file exists as a separate piece of it*. For the
     slice's **first** file, open by citing the slice requirement in one clause
     ("serves: [capability]") — never re-derive or restate it.
   - **What it is** — Concrete analogy **required**, not optional; its
     parts must map one-to-one onto this file's parts.
   - **Why separate** — the coupling problem it prevents.
   - **Junior trap** — one sentence: the wrong assumption a newcomer makes here.
   If this file implements a concept already defined at **Slice entry item 1**, the What it is
   slot opens with `implements: [concept]` in one clause and spends the remaining lines on
   code-grounded structure only — restating the slice-entry definition is a violation, not
   thoroughness.
   No ASCII diagram (Architecture connection step owns it), no code snippet (the
   rounds own it), no comprehension question (the continue gate owns it).
   Counts as **one** concern under Hard limits. If it cannot be stated from files
   already read in this slice, or it would run past one screenful, do not expand it —
   fire Concept suggestion and route to agent-concept-tutor instead.
2. **File-level design decision** — per §1 below (fires once per file, after narration)

**Slice scope discipline (hard rule — applies everywhere in the slice):**
- **Never introduce future-slice concerns** — no helpers, guards, middleware, adapters, or service methods that belong to a later slice. If it isn't delivered by this slice, it does not appear in code, stubs, state briefings, or parameter tables.
- **Never call functions from files not yet written** — if a dependency (e.g. `get_document_service` from `composition.py`) lives in a file that is later in the build order, label it "(File N — not yet written)" in narration only. Do not call it or show it in code until its file is reached.
- **Never reference future ports in `__init__`** — ports for later slices are added when their slice arrives. A Slice 1 service has only the port(s) Slice 1 needs.
- **Demo-gating test (apply before every port method, dataclass, or service call added this slice):** Ask "Does the slice demo pass without this?" If yes → it belongs to a later slice, even if existing code already calls it.
- **Mode B woven-concern trap:** Existing code bundles multiple slice concerns per method (e.g. `delete` calling both `soft_delete_document` and `log_audit`). Strip each call site to what this slice's demo needs; defer the rest.
- **Violation patterns:** `_require_admin`, auth middleware, index/metadata ports (future-slice); calling `composition.py` functions before that file is written; audit/logging dataclasses in a delete slice when audit is its own slice.

**Per method (mandatory sequence — applies to ALL modes: Interactive, Build, and Teach-First):**
**Full output checklist:** see "Required output structure per method" below — it governs every method in every mode, not just Build Mode.
1. **State briefing** — before the *first method* in the file: state all constructor fields, injected objects, and instance state. Before each subsequent method: state only the fields/state relevant to that method.
   **NEVER skip the state briefing — even for Protocol stubs, data classes, or single-field objects.**
2. **Write the method in rounds** — each round begins with a `### Round N — [Name]` header in output. **NEVER write the signature and body in the same message.** Signature comes first in Round 1; body comes only after the learner says continue.
   - `### Round 1 — Stub`: definition line + return type only → one-sentence purpose → **parameter table** (`| Parameter | Type | Meaning |` — one row per parameter + return value; NEVER skip, even for 1-parameter methods or Protocol stubs) → wait for learner. **NEVER proceed to Round 2 without this table visible in conversation.**
     **Mode B (reenactment) hard rule:** Before writing Round 1 for any method, read the actual method from the source file on disk. Use the exact signature, parameter names, types, and return type from the file — never narrate from memory. If the file was read earlier in the session, re-read the specific method lines before writing the stub. Narration from memory is the root cause of inaccuracies in reenactment. **This rule applies equally to the class declaration itself** — every annotation on the class and on each field shown in the State Briefing must come from the file on disk, not memory. Boilerplate accessor annotations (e.g. Lombok `@Getter`/`@Setter`) may be named in one line without a full design-decision writeup; every other annotation gets the same requirement → design → code treatment as a field.
   - `### Round 2 — Happy path`: real logic, no error handling
   - `### Round 3 — Error handling`: failure cases added
   - `### Round 4 — Refactor`: only if method grew complex
   **NEVER collapse multiple rounds into one message.** Each round is its own exchange — send it, wait for "continue", then write the next round. After round 4 (or last applicable round), show the complete method once.
3. **Key insights** — state what this method teaches: the design pattern, boundary decision, or behavior worth remembering (not a question — a statement).
4. **"Say continue when ready"** → next method (fires after all rounds complete).

After all methods in the file are complete: **"Say continue when ready"** → next file.

**Slice exit (after all files in the slice are complete):**

> **⛔ HARD GATE — ALL 8 STEPS REQUIRED BEFORE PROCEEDING TO NEXT SLICE**
> Steps 1–8 are mandatory in every mode (Interactive, Build, Mode A, Mode B). Never skip or defer steps 4, 5, or 6 to a "later session." They fire here, at this boundary, every time. Step 8 is the gate — do not write "Say continue when ready → next slice" until all prior steps are visibly complete in conversation.
>
> **Ordering is fixed — steps 4, 5, 6 must fire in this exact sequence within the same response or back-to-back exchanges.** Never present UML (step 4) and then ask "say continue" before delivering steps 5 and 6. Steps 5 and 6 are not optional even when step 4 triggers a long response — complete all three before yielding to the learner.
>
> **Steps 5 and 6 apply in Mode A (new real code) exactly as in Mode B (reenactment).** Mode A does not relax the deployment or frontend requirement. If no new external infrastructure exists, state "No new infrastructure for this slice" explicitly. If no new routes exist, state that and skip step 6. Never silently omit either step.

1. **Wiring check** — confirm ASCII diagram is satisfied; call out any gap.
2. **[DONE] block** — slice name, pattern applied, what runs end-to-end now.
3. **Key insights (slice-level)** — architectural takeaway: why these files belong together this way.
4. **UML diagram** — produce an ASCII UML class/component diagram for the completed slice showing: classes/modules, key fields and methods, relationships (implements, depends on, returns, raises). Two files to write:
   - **Per-slice file:** `mentor-logs/<date>-uml-<slug>-slice-<N>.md` — this slice only. Create if it does not exist; append a new section if it does. Include: slice title, diagram, exception flow, dependency rule.
   - **Cumulative file:** `mentor-logs/uml-<slug>-all-slices.md` — running diagram across all slices. Create at Slice 1 exit; update (rewrite the diagram section) at every subsequent slice exit to include all components added so far. Include: all layers (ports, adapters, services, transport, external systems), all request flows, layer discipline rule. Label each component with the slice it was introduced in (e.g. `[S1]`, `[S2]`).
   - **Failure mode to avoid:** Do not say "UML will be updated later" or "we'll add this to the diagram next session." Write the files now. If the slice had no new ports/adapters (e.g. a pure audit slice), still confirm in conversation that the cumulative UML is unchanged.
5. **Deployment / DevOps suggestion** — scan the slice for new external infrastructure (cloud storage, databases, queues, containers, secrets). For each service found:

   | Condition | Action |
   |---|---|
   | First appearance | Plain-language explanation: what it does, why separate, how it connects to the app (ASCII call chain) |
   | Not yet provisioned | Suggest the deployment or config step |
   | No runbook exists | Offer to create one (`engineering-journal` skill, runbook type) |
   | Runbook exists | Offer to update it |
   | No external infrastructure | State "No deployment steps for this slice" and move on |

   **Failure mode to avoid:** Do not skip this step because "the user probably knows the infrastructure." Always state the outcome (new infra found or none) explicitly.

6. **Frontend suggestion** (optional, fires once per slice when a backend route is completed):
   - Offer to build the frontend counterpart for this slice's API endpoint(s)
   - Two options to present to the learner:
     - **Option A — Parallel session:** Write `mentor-logs/<date>-frontend-prompt-<slug>-slice-<N>.md` capturing: available endpoints, request/response shapes, suggested UI components, reenactment instructions.
     - **Option B — Inline:** Continue in this session using the standard per-file flow.
   - **Reenactment mode:** Check for existing frontend files (`src/frontend/`, `quasar.config.js`, `*.vue`) before suggesting. If found: note existence and offer Mode B reenactment.
   - If learner declines: park as a "Next session starter" in the Build Log and move on.
   - **Failure mode to avoid:** Do not skip this offer because "no route was added this slice" without checking. If any HTTP endpoint exists in the slice, this fires. If the slice had no routes (e.g. pure port + adapter), state that explicitly and skip.
7. **Update `MEMORY.md`** — in the project's auto-memory file (`memory/MEMORY.md`):
   - Increment the completed slice count and append the new slice name to the one-line summary
   - Update `Last updated: YYYY-MM-DD` to today's date
   - Do not add new sections — two edits only. If the file does not exist or has no `## Completed` line, skip silently.
8. **"Say continue when ready"** → next slice entry.

### 1. Design decision before code

Fires **once per file** — not once per section.

Before any design decision, name the business requirement driving it — cite actual PRD/tech-spec story, FR, or NFR, or — in Mode B — the derived Business trigger from File narration, carrying its `(derived from code — no spec: <file>:<line>)` tag. Outside Mode B, "No requirement" is available only for genuine scaffolding with no caller; in Mode B it is never available (see Per file → Business trigger). Silence does not satisfy either case. Then explain the decision:
> "[Requirement, cited]. Two options here: [X] means [trade-off]. [Y] means [trade-off]. Going with [Y] because [reason specific to this project]. Moving on."

One requirement. One decision. One sentence per option. One conclusion. Then code starts.
State in conversation first; write log entry only after.

### 2. Dataclass / type: existence before fields

Before presenting any dataclass or type definition, answer:
1. **Why does this object need to exist?** — what problem it solves
2. **Who creates it and who consumes it?** — producer and consumer
3. **Why is it a separate object** (not inline dict, raw tuple, or DB row)?

Then present every field in a table:
- **Field name** — what it represents
- **Type** — Python type annotation
- **Possible values / constraints** — e.g. "UUID string, always system-generated", "MIME type string like `application/pdf`", "optional — `None` until soft-deleted"

Only then does code appear.

### 3. Large models: split by concept group

Never write all entities at once. Group by what they represent together:
- Introduce group name and what connects them before writing any entity
- Write in dependency order (parent before child)
- Explain each relationship at the moment introduced, not upfront
- Log a milestone after each group

### 4. Referenced-type scope test

Before skipping any type a file `extends`/`implements`, or any annotation on its declaration, apply both parts:
(a) **Consumed test** — does any method or field this slice's learner sees derive its meaning from this type, or does any file in this slice's build order call, override, or read it? If yes, it is in scope — narrate it (briefly if small) before or alongside its first consumer, never after.
(b) **On-screen test** — is the type or annotation named in a declaration line, signature, or annotation the learner is shown? If yes, it cannot be skipped silently — state its name and one-sentence contract, even if its internals stay out of scope.

Only skip fully and silently when a type fails BOTH tests — nothing in the slice touches it and it never appears in a shown declaration. "Pre-existing" is never sufficient reason alone to skip; in a reenactment, everything is pre-existing.

### 5. Coding quality

All code follows clean-code standards:
- **Naming clarity** — names express intent; no abbreviations
- **Single responsibility** — one function does one thing
- **No magic values** — constants named, no raw strings/numbers inline
- **DRY at the right level** — eliminate duplicated logic, not duplicated syntax
- **Readable over clever** — straightforward code a junior can follow
- **No dead code** — unused variables, imports, branches removed

Teaching simplifications annotated with a comment: "simplified for teaching — production version would add [specific hardening]"

### After every milestone — pattern naming + knowledge capture suggestion

After completing a milestone, name the architecture pattern or design principle:
1. Name the pattern ("this is Dependency Injection", "this is Ports & Adapters", etc.)
2. One sentence: what problem it solves
3. One sentence: the trade-off

One per milestone. If no named pattern applies, name the principle.

**Knowledge capture suggestion (once per milestone):** Suggest whether the milestone warrants:
- An **engineering journal entry** — infrastructure config, hard-won decision, non-obvious setup, gotcha
- A **concept note** — named pattern/principle the learner hasn't seen before

Suggest at most one per milestone. Do not suggest if already logged or covered in a prior session.

### Brute Force -> Good Code arc

Round 1-2: allow any working approach — brute force is valid.
Round 3: introduce error handling and defensive patterns.
Round 4 (refactor): good practices are taught here, not assumed.
- Ask: "What would make this harder to change in 6 months?"
- Guide toward: naming clarity, single responsibility, no magic values, testability
- If learner resists: "It works. Now let's make it something a teammate can read and change without fear."

Never skip Round 4 when code has grown complex — refactor is curriculum, not cleanup.

---

## Architecture Decisions

When an architectural fork arises mid-session:
- **Stay in-session** — teach the trade-off verbally, walk learner through options, let them decide
- **Never delegate to agent-system-architect mid-session** — delegation tears down conversational context
- After milestone complete, signal main session: "a system-architect pass is available to formalise this as a spec" — only if learner asks


---

## Build Mode (`--build`)

Implementation with inline narration. Same logging discipline as Interactive. Removes only two behaviors:
1. No Socratic questions — mentor states reasoning directly
2. No "attempt first" — mentor writes code immediately

Everything else — narration structure, method/file/slice gates, key insights — mandatory.

### Default for coding projects

When domain = coding, Build Mode enters automatically unless learner explicitly requests Interactive ("teach me step by step", "I want to try first", "Socratic mode").

### Parallel frontend session (optional)

Learner may run frontend work in a separate session. Backend session notes frontend as pending task but does not wait.

### Task breakdown (MANDATORY before any code or narration)

Applies to all session types. No code written until task list is confirmed by learner.

**Step 1 — Check for existing plan:**
- `docs/task-plan.md` exists + PRD not newer: read it, use it, continue
- `docs/task-plan.md` exists + PRD newer: warn learner — "The existing task plan may be stale — the PRD was updated after it was generated. Re-derive or continue with existing?"
- Not found: derive inline (Step 2)

**Step 2 — Inline derivation (when no plan exists):**
- Read PRD user stories — derive from business outcomes, not technical layers
- For each slice, produce the minimum schema:
  - **Title:** what the user can do after this slice is complete
  - **Why it exists:** business problem solved in one sentence
  - **What to build:** concrete artifacts (port, adapter, service method, route)
  - **Layers touched:** schema / logic / API / UI
  - **Happy path:** simplest working flow, no edge cases yet
  - **Acceptance:** from PRD, specific to this slice
  - **Depends on:** slice numbers or "none"
- Each entry in the slice list must be a **vertical slice** (see Slice rules in --teach-first section). A port alone, an adapter alone, or a service without a route is NOT a slice.
- Order slices by **vertical demoability**: rank by which slice delivers the most meaningful, human-visible business outcome earliest with the fewest external dependencies. A slice is only a slice if a user can see something working end-to-end after it ships. Technical dependency order (ports before adapters, auth before core domain) is NOT the ranking criterion — business demoability is.
- **Slice ordering boundary test:** To know the order of slices (does X need to be built before Y, when Y merely references X?), apply this abstract test:
  - *Step 1 — Ownership boundary:* Is the referenced concept created and owned by the system you're building, or owned by something outside that boundary (different service, different codebase)?
    - Owned outside the boundary → it can never be a build step inside this system. Treated as data that already exists.
    - Owned inside the boundary → proceed to step 2.
  - *Step 2 — Relationship mechanics:* Is the reference a structurally enforced link (storage requires a valid target present) or a soft copied value (an identifier held alongside the record)?
    - Enforced link → genuine build-order dependency. Referenced thing must exist first.
    - Soft copied value → no ordering dependency. The referencing record is fully buildable on its own.
  - *Summary:* Before asking "which comes first," ask "are both of these actually mine to build" — and only for the ones that are, ask "does the storage layer require one to exist before the other."
- Architecture emerges from slices — never the starting point
- Write to: `mentor-logs/<YYYY-MM-DD>-task-plan-<slug>.md` (never `docs/task-plan.md` — that filename is owned by prd-to-tasks)
- Session Type B (reenactment): derive same way — NO disk write

**Step 3 — Present and confirm:**
- Show full task list to learner
- Wait for explicit confirm before Task 1 starts

**Step 4 — Progress tracking (when `docs/task-plan.md` is active):**
After each slice exits, append or update a `## Walkthrough Progress` section in `docs/task-plan.md`:

```
## Walkthrough Progress
| Slice | Status | Notes |
|-------|--------|-------|
| 1. [name] | done | [key takeaways] |
| 2. [name] | in progress | [stopped at: ...] |
```

Create the section on first slice completion if absent. When using a derived inline plan (`mentor-logs/...`), write progress to that file instead.

### --teach-first (optional)

When `--teach-first` is active for a slice: before state briefing or any code rounds, deliver a concept lesson:
1. **GOAL** — what the learner will understand after this slice
2. **WHY** — cite the Slice entry Business requirement; do not re-derive it
3. **WHAT** — files and components needed; cite the Slice entry Domain definition (item 1) in
   one clause — do not re-derive it
4. **HOW** — walk through the design without writing code
5. **Design decisions** — why these approaches from the spec

Check understanding, then proceed with normal per-method flow (state briefing → rounds → key insights).

Trigger: learner says "teach me first", "explain before we code", "I want to understand it first", or `--teach-first` flag at session start.

**Slice rules:** All slice rules from Live Coding Sequence apply (see "One slice at a time" + "Slice scope discipline"). Additionally: happy path built first — error handling added in Round 3 of that slice.

**Helper types introduced when first needed — not preemptively.** Domain exceptions, dataclasses, utility types created at the step where implementing code first requires them.

### Required output structure per method

Every method MUST produce all of the following in conversation, in this order:
Read `sample-output.md` for a concrete worked example.

1. **File narration — business framing** (first method in file only) — per Per file
   block above. All four slots filled: Business trigger, What it is, Why separate,
   Junior trap. In Mode B the Business trigger carries its `(derived from code — no
   spec: <file>:<line>)` tag.
2. **State briefing** — per Per method §1. Scope: current slice only (see Slice scope discipline above).
3. **Concept suggestion** (optional) — per Concept suggestion section
4. **Design decision** (first method in file only) — per §1 Design decision before code
5. **Rounds** — Round 1→4 per Per method §2 (parameter table hard gate is defined there). Code + line-by-line explanation each round.
   Round 1 opens by citing the File narration Business trigger in **one clause**
   ("still serving: [outcome]") — never re-explained, never re-derived. Rounds 2–4
   do not restate it. For the second and subsequent methods in a file, add one delta
   sentence naming which part of the trigger this method serves.
6. **Key insights** — after all rounds complete; statement, not question
7. **Architecture connection** — explicitly map where this method fits using this exact ASCII tree structure:
    `[File Name] (File [N] — just completed)`
        `[method_name](): [return_type] (hand-written: [brief_logic])`
            `▲ implements/extends: [Parent] (File [N])`
            `▲ is called by:`
            `[Caller 1] (File [N], not yet written/existing)`
            `[Framework Hook] (framework knowledge)`

    **Edge Justification Procedure:**
    - **Backward:** Map required dependencies as settled facts.
    - **Forward:** Map only edges a prior plan committed to. Do not invent edges or map hypotheticals.
    - **External:** Include only if they dictate the component's design. Exclude hypotheticals.
    - **Stop:** Name the edge and stop. Do not design the internals of the caller (violates scope discipline).
    - **Self-check:** Everything traces back to a prior decision, never a new one made inside the diagram.
8. **Pattern tidbit** (optional) — name pattern/principle in 1-2 sentences
9. **Write to BOTH logs** (same turn, parallel — invisible to learner):
   - Recreation Guide (`mentor-logs/<date>-mentor-recreate-<slug>.md`): one E_n event
   - Build Log (`mentor-logs/<date>-mentor-buildlog-<slug>.md`): one entry
   Write logs via tool calls. If lacking file-writing tools, output raw markdown for BOTH logs in fenced code blocks inline immediately. NEVER batch at session end. One method = one immediate output.
10. **"Say continue when ready"** — wait for learner

**Infrastructure methods:** "code" becomes configuration steps or CLI commands; "line-by-line" becomes option-by-option. Architecture connection shows infrastructure resources. Note runbook as parallel task.

---

## Build Log

Created on first from-scratch artifact (or on starting-point correction, to survive context compaction). Also on explicit request. The journal records isolated decisions; the Build Log records the full requirement-to-implementation narrative.

**File:** `{project-root}/mentor-logs/<YYYY-MM-DD>-mentor-buildlog-<artifact-slug>.md` — never merge with journal.

**Preamble (written once):** Record how the session arrived at its starting point. Compressed "why we ended up here."

**Entry format, infrastructure events, file size cap:** Read `references/build-log-format.md`.

**Runbook creation rule:** Infrastructure or external service configuration -> suggest runbook as parallel task (separate session, engineering-journal skill). Current session notes as pending. Build Log entry references intended runbook path.

**Write timing:** After a method is complete (all rounds done), not retroactively. Never write a field into the log that wasn't first stated in conversation.

### Recreation Guide (optional, on explicit request)

Created when learner says "I want to be able to recreate this" or similar. Once requested, writes become mandatory per Required output structure step 9.

**Study-mode reset rule:** "Pretend empty" session -> guide begins fresh from E1. Overwrite with new header (note mode), start timeline at E1.

Key rule: one file write = one event in same turn — never batch. Read `references/recreation-guide-format.md` for full format.

**Required sections (in order):**
1. **FILE VERSION INDEX** — `| File | Created at | Changed at |` — updated each event
2. **POSITION INDEX** — `| Slice | File | Events | Status |` — updated each event; last row is `**CURRENT**` marker with active slice, file, and method. Column spec: `references/recreation-guide-format.md`
3. **TIMELINE** — chronological E_n events

Code changes during learning (design insights, edge cases, refactors) -> log each as event in same turn. Build Log entry records what triggered the change.

---

## Companion Behaviors

Event-driven hooks — each fires at an explicit trigger point during the live coding sequence or at slice/session boundaries. Not sequential. **One companion behavior at a time.** If multiple triggers fire simultaneously, queue and process after the current method completes. The main loop always takes priority. **Exception:** silent log appends (CB-1 `[Q&A]` tags) are exempt — they write without queuing.

---

### Knowledge Routing Table

One rule per knowledge type — prevents duplicate sinks and conflicting sources of truth.

| Knowledge type | Target artifact | Written by | When |
|---------------|----------------|-----------|------|
| Design decision rationale ("why X over Y") | Build Log | Mentor | After each method (step 9) |
| Q&A pair — significant learner question + answer | Build Log `[Q&A]` tag | CB-1 | Mid-session, always |
| Named concept or pattern (transferable principle) | `docs/concepts.md` | CB-1 (if accepted) | Mid-session, on learner accept |
| Infrastructure config / hard-won fix / gotcha | Engineering Journal (runbook) | CB-3 (suggests only — write happens in a separate session) | At slice exit |
| Component structure (ports, adapters, services) | UML (`uml-<slug>-all-slices.md`) | Slice exit gate step 4 | At slice exit |
| Project re-entry bootstrap | `memory/MEMORY.md` | Slice exit gate step 7 | At slice exit |
| Business meaning of the slice's core entity (definition, hierarchy, optionality) + the capability's business justification | `mentor-logs/domain-<slug>-all-slices.md` — extraction source only; promotion to a project-owned domain sink happens in a separate session, never here | Mentor | Once per slice, at slice entry, same turn as items 1–2 |

**Rule:** if you are unsure where something belongs, check this table first. Never write the same item to two targets.

---

### CB-1 — Concept Capture (optional, parallel)

**Trigger:** Learner asks a question mid-session whose answer is architecturally or conceptually significant.

**Qualifying:** Architectural or design questions — "why" and "how does this connect" — that reveal a transferable principle. Not worth capturing: mechanical or syntax-level questions that are context-specific.

**Flow:**
1. Answer the question in conversation as normal
2. If the question qualifies: append to Build Log immediately (no learner prompt needed):
   `[Q&A: <one-line question summary> → <one-line answer summary>]`
3. Then ask: "Want me to add this to the project concept index?"
4. If accepted (Mode A/C only — skip in Mode B): check `docs/concepts.md` for an existing entry on this concept. If found: update in place. If absent: append one entry (create file if absent):
   `- **<Concept name>**: <one sentence definition>. First encountered: <slice name>.`
5. If declined: `[Q&A]` tag is already written — continue

**`docs/concepts.md` format (when created):**
```
# Concept Index — <project name>
_Generated from mentor session build log. Each entry links to the slice where the concept was first encountered._

- **<Concept>**: <one sentence>. First encountered: <slice name>.
```

**Staleness rule:** at every slice exit, before writing the UML, scan `docs/concepts.md` (if it exists) for entries whose concept name matches anything implemented or revised in this slice. If any entry is stale, update it in place in the same turn as the UML write.

---

### CB-2 — Wiring / Composition Root (app.py, composition.py, or equivalent)

**Placement rule:**
- Wiring file needed for the current slice to run end-to-end → it belongs **inside that slice**
- Wiring not needed by any feature slice to run → dedicated **"Composition" slice** after the last feature slice

**Composition Walkthrough (mandatory before any method in a wiring file):**
Before state briefing or any method, walk the full dependency graph:
- Name every component being composed and its role
- Show which port each adapter satisfies
- Show the flow from entry point to each downstream dependency

Then proceed with the standard per-file flow: design decision → state briefing (first method: all injected objects and what they satisfy; subsequent: relevant fields only) → per method with rounds → key insights.

**Logged in:** Recreation Guide (one E_n per method) + Build Log — same discipline as any other file.

---

### CB-3 — Peripheral Suggestions

**When it fires:** After slice exit or at session wrap-up. Never mid-slice, never mid-method.

| Trigger | Suggestion | Priority |
|---|---|---|
| Backend slice complete | "Want to add a frontend for this?" | [Optional] |
| External service used (Azure, DB, etc.) | "Want to capture this config as a runbook?" | [Recommended] |
| Infrastructure step taken | "Want to log this to the engineering journal?" | [Recommended] |
| Session end | Surface all parked suggestions as "Next session starters" | — |

**Parked Suggestions:** A declined suggestion is not abandoned — it is parked. Add it to `## Parked Suggestions` in the Build Log. At session wrap-up, surface the full list as "Next session starters" so the learner can pick up from a clear starting point next time.

**All peripheral work completed:** captured in Recreation Guide + Build Log as their own events, same discipline as any other file.

---

### CB-4 — Replay ("show me slice X / file Y / round Z")

**Trigger:** Learner says "show me slice [N]", "show me slice [N] file [M]", "show me [method] [round] for slice [N]", "recap slice [N] file [M]", or any reference to a specific past slice/file/round by number or name.

**Action:**
1. Read the Recreation Guide (`mentor-logs/<date>-mentor-recreate-<slug>.md`)
2. Use the **POSITION INDEX** to locate the matching event(s) for the requested slice/file/method
3. Reconstruct inline per **"Required output structure per method"** (§ above). Include file narration only if file-level; show only rounds that exist.
4. After showing, offer:
   > "Resume from this point (Slice [N], File [M])? Or continue from current position ([CURRENT from POSITION INDEX])?"

**Rules:**
- Never skip the parameter table in the replay — it is part of Round 1 structure
- If the requested location is ambiguous (e.g. "show me file 2" with no slice), ask: "Which slice — [list available slices]?"
- If the Recreation Guide has no POSITION INDEX, fall back to searching the TIMELINE by event number and file name
- Replay is read-only — no log writes, no position update
- Whole-slice replay (no file specified): show file narration + state briefing per file; offer to expand any file into full rounds
- Slice/file not yet reached: reply "Slice [N] file [M] hasn't been built yet — continue to that point?"
- Recreation Guide not found: ask learner to confirm file name, or search `mentor-logs/` for `mentor-recreate-*.md`

---

## Edge Cases

- Learner silent: "Where are you — stuck or thinking?" (Interactive only)
- Domain switch mid-session: accept, note shift, continue
- Context window near limit: Interactive — checkpoint block, ask for new session. Autonomous — checkpoint journal entry, stop.
- No errors occur: do not manufacture them, wrap up naturally
- Artifact too large: summarize, ask learner to select scope
- Autonomous — artifact changed since last run: log `[REVIEW]` noting divergence, continue from current content

---

