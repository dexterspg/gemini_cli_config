# Quality Guardian Review Checklists

## Checklist Conventions

These checklists contain only:
- **Project-specific standards** — behaviors specific to this system's conventions
- **Non-obvious checks** — things Gemini would not apply by default
- **Calibration thresholds** — specific pass/fail criteria that differ from general best practice

Generic review principles (naming clarity, security basics, standard patterns) are applied by default and are NOT listed here.

**Minimum item format:** Each item is a yes/no check question. Items with non-obvious failure modes include a *Fail:* note defining what failure looks like concretely.

**Verdict guidance:** Each checklist ends with a verdict block. Global default if not overridden:
- All items pass → APPROVED
- 1–2 non-critical items fail → REVISION_NEEDED (list failed items + suggested fix)
- Any [critical] item fails, OR 3+ items fail → BLOCKED with rationale

Mark load-bearing items with `[critical]` when a single failure should block regardless of other results.

---

## Base Checklist (run for ALL content types before routing)

These checks apply universally — run them first, then load the type-specific checklist.

- [ ] **[critical] No credentials, API keys, tokens, or PII exposed?** *Fail: any literal secret, real email address, or personal identifier in output, examples, or code snippets — even if commented out.*
- [ ] **Scope matches what was asked?** The output solves the actual stated problem — not a subset, not an expanded version. *Fail: a requested bug fix also refactors unrelated code; a summary omits the core question.*
- [ ] **No internal contradictions?** Claims, values, or rules in one section do not contradict another section of the same document. *Fail: prose says "always X" and an example shows not-X.*
- [ ] **Claims are substantiated?** Statements of fact cite evidence, code, or source — not asserted without basis. *Fail: "this is the root cause" with no log line, test, or reference.*
- [ ] **Terminology is consistent?** The same concept uses the same name throughout. *Fail: "user story", "requirement", and "feature" used interchangeably for the same artifact.*
- [ ] **Output is clear to its intended reader?** Language, structure, and depth match the audience — no unexplained jargon, no gaps in logical flow. *Fail: a non-technical document uses implementation-level terms without explanation; a technical spec uses vague prose where precise definitions are needed.*
- [ ] **All required parts are present?** No sections missing, empty, or left as placeholders. *Fail: a required section heading exists with no content; a template placeholder like `[TODO]` or `TBD` remains unfilled without a noted reason.*

### Over-Engineering Guard (run for any solution or proposed change)

Run these when the output is a proposed design, code, workflow, agent, skill, or GEMINI.md addition. For the full checklist with red flag details, read `CHECKLIST-overengineering.md`.

**Core question: Is this the simplest solution that solves the actual, current problem?**

- [ ] **Solves a problem that exists today** — not a hypothetical future need? *Fail: "we might need this later" cited as justification.*
- [ ] **Simpler alternative ruled out?** Would a note, memory entry, one-liner, or config value solve the same problem? *Fail: infrastructure introduced where a single file edit would suffice.*
- [ ] **Number of new files/components proportional to problem scope?** *Fail: new abstraction layer, skill file, or agent created for a single use case with no other callers.*
- [ ] **No drift from original problem?** The work solves what was asked — not an expanded or different version of it. *Fail: requested bug fix also refactors surrounding code; requested skill addition becomes a framework.*

**Red flags (2+ triggers REVISION_NEEDED — propose simpler alternative):**
- [ ] New file type, config format, or runtime dependency for a single use case
- [ ] "Future extensibility" cited but no concrete future cases named
- [ ] Solution requires its own documentation to explain how to use it
- [ ] A simpler layer (memory, GEMINI.md line, inline comment) was skipped in favor of infrastructure

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
| Global agents / skills / GEMINI.md (bloat review) | `CHECKLIST-agents-skills.md` + `CHECKLIST-claude-code.md` |
| Product Requirements Document (PRD) | `CHECKLIST-prd.md` |
| PRD ↔ Technical Spec sync | `CHECKLIST-prd-sync.md` |
| Support investigation output | `CHECKLIST-support.md` |
| Scheduled automation skill (autonomous pipeline) | `CHECKLIST-automation.md` |
| General / fallback (unrecognized type) | Apply base checklist only. Note in review output: "No type-specific checklist matched — add a new `CHECKLIST-*.md` if this content type will recur." |

All checklist files are in `~/.gemini/skills/quality-guardian/`.
