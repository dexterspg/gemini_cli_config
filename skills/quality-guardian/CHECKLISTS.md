# Quality Guardian Review Checklists

## Checklist Conventions

These checklists contain only:
- **Project-specific standards** — behaviors specific to this system's conventions
- **Non-obvious checks** — things Gemini would not apply by default
- **Calibration thresholds** — specific pass/fail criteria that differ from general best practice

Generic review principles (naming clarity, security basics, standard patterns) are applied by default and are NOT listed here.

**Minimum item format:** Each item is a yes/no check question. Items with non-obvious failure modes include a *Fail:* note defining what failure looks like concretely.

## Severity and Verdict

This section is the only definition of severity and verdict; checklists and agents point here.

**Severity** (one per finding):
- **Critical**: a `[critical]` item fails.
- **Major**: any other checklist item fails.
- **Minor**: a preference, style point or hypothetical risk. Listed, never changes the verdict.

**Verdict:**
- No Critical and no Major → APPROVED (list the Minor findings).
- Any Critical or Major → REVISION_NEEDED: list each failed item with its fix and name one issue type.
- BLOCKED only when (a) the artifact is missing or unreadable, (b) its type is unrecognizable, (c) the next step is a decision only a human can make, or (d) a Critical is still open at the last iteration ("iteration N of N" given by the caller). Name the escalation target and the minimum information needed to unblock.
- Iteration count not given → never BLOCKED for an open Critical.

Mark an item `[critical]` only when its failure leaves the artifact harmful or silently wrong for whoever relies on it: a secret or personal data exposed, or a requirement, claim or gate that later stages trust missing or unverified. Cost, structure and style failures are Major.

---

## Base Checklist (run for ALL content types before routing)

These checks apply universally — run them first, then load the type-specific checklist.

- [ ] **[critical] No credentials, API keys, tokens or connection strings exposed?** *Fail: any literal secret in output, examples, code snippets, config files or logs — even if commented out. Never edit one out alone: ask the user, and offer rotate and remove, an environment variable, or a `<placeholder>` that notes where the real value comes from.*
- [ ] **Scope matches what was asked?** The output solves the actual stated problem — not a subset, not an expanded version. *Fail: a requested bug fix also refactors unrelated code; a summary omits the core question.*
- [ ] **No internal contradictions?** Claims, values, or rules in one section do not contradict another section of the same document. *Fail: prose says "always X" and an example or adjacent code snippet shows not-X.* A superseded rule, status, proposal or offer left standing beside its replacement with no Superseded or Withdrawn mark also counts.
- [ ] **Claims are substantiated?** Statements of fact cite evidence, code, or source — not asserted without basis. *Fail: "this is the root cause" with no log line, test, or reference.* **Absence claims need it most** — "X doesn't exist", "undocumented", "no such endpoint" rest on a search having been exhaustive, which a single tool call rarely proves. *Fail: an absence asserted from one failed fetch, grep, or query, with no note of what was searched and how.* **Time-bound claims need a stamp.** A claim that something "is live" or "current", a version, or a status names what it was checked against (branch, commit, URL) and when. *Fail: "dev is live" with no branch or check date.* Authoring-time only.
- [ ] **Terminology is consistent?** The same concept uses the same name throughout. *Fail: "user story", "requirement", and "feature" used interchangeably for the same artifact.*
- [ ] **Output is clear to its intended reader?** Language, structure, and depth match the audience — no unexplained jargon, no gaps in logical flow. *Fail: a non-technical document uses implementation-level terms without explanation; a technical spec uses vague prose where precise definitions are needed.*
- [ ] **All required parts are present?** No sections missing, empty, or left as placeholders. *Fail: a required section heading exists with no content; a template placeholder like `[TODO]` or `TBD` remains unfilled without a noted reason.*
- [ ] **Every link, path and heading pointer resolves?** Each cross-reference names a file, project, learning plan or section that exists. *Fail: a link, a `See:` pointer or a "→ Heading" citation whose target is missing or renamed.*

### Over-Engineering Guard (run for any solution or proposed change)

Read `CHECKLIST-overengineering.md` for any proposed solution or change; its first line lists what counts.

---

## Declared Style

Review every artifact in two steps, in this order:
1. Write the `[independent]` findings from the base and family checklists, from the artifact alone. Do not open the row's spec or owner sections yet.
2. Then add `[rule: <spec check or file § heading>]` findings for conformance only: to the row's declared style (its spec and owner sections), if the row names one, and to the rules in the user's `GEMINI.md` that can be seen in an artifact (formats, paths, naming, size, forbidden lines). Rules about how Gemini routes, delegates, asks or behaves are not artifact findings. If `GEMINI.md` is not in your context, read `~/.gemini/GEMINI.md`.

Rules:
- In a row that names Declared style, wording, tone and format are never findings, and you propose no rewording. Facts, secrets and scope are still checked.
- A `[rule]` finding names the failed spec check or the heading it comes from, or it is dropped. It is Major.
- Real data is allowed: email addresses, personal identifiers and setup paths stay where the file needs them. Never raise them as a finding and never replace one without the user's answer. Ask, and suggest: keep it and mark the file with a line that says only `real-data: intentional` (best for a private setup file), mask it, or use a `<placeholder>` that notes where the real value comes from (best for anything shared outside the team).

---

## Routing Table

After the base checklist, read the matching type-specific file.

| Content type | Read this file |
|---|---|
| Jupyter notebook (`.ipynb`) | `CHECKLIST-notebook.md` |
| Code (implementation, scripts, functions) | `CHECKLIST-code.md` |
| UI design, mockup, wireframe | `CHECKLIST-design.md` |
| Documentation / notes (learning content) | `CHECKLIST-learning-content.md` |
| Note-taker output (organization review) | `CHECKLIST-organization.md` |
| Project documentation (README, INTEGRATION, etc.) | `CHECKLIST-project-docs.md` |
| Global agents / skills / GEMINI.md (bloat review) | `CHECKLIST-agents-skills.md` + `CHECKLIST-gemini-code.md`; also `EVIDENCE-agent-design.md` → "Decision guide" (the first item of the agents-skills checklist needs it) |
| Product Requirements Document (PRD) | `CHECKLIST-prd.md`. Judgment rules in `skills/product-strategist/SKILL.md` → "## Rules" and "## Output Format" |
| PRD ↔ Technical Spec sync | `CHECKLIST-prd-sync.md` |
| Support investigation output | `CHECKLIST-support.md` |
| Scheduled automation skill (autonomous pipeline) | `CHECKLIST-automation.md` |
| Migration artifact: any file in a client `migration/` folder, including its `README.md` (this row, not Project documentation) | No checklist file. `~/.gemini/skills/migration/SKILL.md` → "## Rules for Agents Using This Skill", plus by artifact: plan → "## Phase 0: Migration Planning" and Gates "Ready to send to the client"; `FIELD_MAPPING.md` and `BUSINESS_RULES.md` → "### Rules for field mapping" and Gates "Ready to send to the client" and "Ready to pilot"; pilot review → "## Phase 3: Pilot Migration" and Gates "Ready to reconcile"; reconciliation report → "## Phase 4: Reconciliation" and Gates "Ready for go-live". Cite the heading each finding fails; a gate item that fails or has no record in the artifacts is REVISION_NEEDED. |
| Decision record (ADR) | Base checklist only. Judgment rules in `skills/engineering-journal/SKILL.md` → "### 1. Decision (ADR-style)" |
| Jira LAE ticket description | Base checklist only. Judgment rules in `skills/jira/SKILL.md` → "### LAE Description Template" |
| Jira LAE investigation comment | Base checklist only. Judgment rules in `skills/jira/SKILL.md` → "### LAE Investigation Comment Template" |
| Technical specification (`docs/technical-specification.md`; a file starting `# Implementation Brief:` is a `--lite` brief) | `CHECKLIST-prd-sync.md` when a PRD exists |
| General / fallback (unrecognized type) | Apply base checklist only. Note in review output: "No type-specific checklist matched — add a new `CHECKLIST-*.md` if this content type will recur." |

All checklist files are in `~/.gemini/skills/quality-guardian/`.
