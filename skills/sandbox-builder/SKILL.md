---
skill: sandbox-builder
description: Full rules, process, output structure, and checklists for building learning sandboxes in --sandbox mode. Read this before starting any sandbox session.
---

# Sandbox Builder

## Process

1. **Check first** — Read `C:\workarea\sandbox\SANDBOX_INDEX.md` and `C:\workarea\sandbox\GIT-TAGS.md` for tag conventions. Search the Concepts column for the requested concept slug.
   - **Match found** → read that sandbox's `PROJECT.md` Progress section → determine if the new concept is additive (builds on existing) or alternative (different approach to same concept)
     - **Additive** → extend the existing sandbox, update `PROJECT.md`, add git tag
     - **Alternative** → create a new sandbox folder with a descriptive name suffix
   - **No match** → create a new sandbox folder, add a row to `SANDBOX_INDEX.md`
2. **Locate** — Read relevant skill files (per GEMINI.md skill loading rules) and use them to find the production code for the requested concern
3. **Trace** — Follow the code path: identify the core algorithm, its inputs/outputs, and how it connects to other layers. Delegate to agent-codebase-archaeologist if tracing requires deep multi-file investigation
4. **Decide scope** — Determine what the sandbox needs:
   - Backend logic (always) — the core algorithm/business rule, simplified
   - Frontend (if requested or if the concept involves UI interaction) — minimal page to input parameters and see results      
   - Plumbing (if the production pattern uses it) — minimal event/messaging/service calls to show how layers communicate       
5. **Simplify** — Strip framework noise (base classes, JPA boilerplate, batch infrastructure, framework lifecycle hooks) while keeping the essential pattern intact. The sandbox should mirror *how the production code thinks*, not *how the framework wraps it*
6. **Scaffold** — Generate a self-contained runnable project. Choose the simplest stack that demonstrates the pattern:
   - Java/Spring Boot backend if the production code is Java (keeps concepts transferable)
   - Vue/Quasar/React frontend — match whatever the production codebase uses, otherwise plain HTML is fine
   - In-memory data (no database required unless persistence IS the concept)
7. **Annotate** — Add "production bridge" comments that map sandbox code back to real file locations:
   ```java
   // Production: {module}/{package}/SomeClass.java:142
   // Simplified: removed X, hardcoded Y for clarity
   ```
8. **Tag** — After committing, create a namespaced git tag: `{sandbox-name}/stage-{n}/{concept}`

## Output Structure

```
{project-root}/
├── README.md              — What this teaches, how to run, what was simplified
├── PROJECT.md             — Full explanation of how the project logic works (see below)
├── backend/               — Minimal Spring Boot (or plain Java) app
├── frontend/              — Minimal Vue/HTML (if needed)
└── PRODUCTION-MAPPING.md  — Maps every sandbox file → production source
```

## PROJECT.md — Required for Every Sandbox

After writing all project files, always create or update `PROJECT.md` in the sandbox root.

`PROJECT.md` must cover:
1. **Metadata table** — Concepts (slugs), Tech Stack, Status, Source in Codebase, Prerequisites
2. **Progress section** — Current Stage (git tag), Last Studied date, Covered (bullet list), Next Steps (bullet list), Continue From (real codebase path:line)
3. **Learning Stages table** — one row per git tag: `| tag | concept added | date |`
4. **What the project does** — one paragraph summary, plain language
5. **The layers** — how the project is structured and what each layer's job is
6. **The full request flow** — step-by-step walkthrough from HTTP request to database and back
7. **How the patterns connect** — how each pattern relates to the others in this specific project
8. **What was simplified vs. real** — a table of what was left out and why

**If `PROJECT.md` already exists (resuming a session):**
- Read it first — check the Progress section
- Move completed concepts from Next Steps → Covered
- Update Current Stage to the new git tag
- Update Last Studied date
- Add a new row to the Learning Stages table
- Do not rewrite sections that are still accurate

## Rules

- The sandbox must actually compile and run — never generate pseudo-code
- Keep it minimal: if the concept needs 3 classes, don't scaffold 30
- Preserve the production algorithm's logic faithfully — simplify the surroundings, not the core
- Default output location: `C:\workarea\sandbox\{sandbox-name}\`
- Git tag convention: `{sandbox-name}/stage-{n}/{concept}` — see `C:\workarea\sandbox\GIT-TAGS.md`. **Tags always use `stage-{n}` even when the sandbox uses "slice" terminology internally.** The stage counter is sequential starting at 1 regardless of the internal slice label (Slice 0 = stage-1, Slice 1a1 = stage-2, etc.). Never use `slice-{n}` in a git tag.
- **Sandbox structure types** — pick one at the start of a new sandbox and stick with it:
  - **In-place evolution** — each stage MODIFIES the same files (e.g. RestTemplate → Feign → Retrofit in one codebase). Tags are MANDATORY because they are the only way to recover a past stage's state.
  - **Side-by-side folders** — each stage lives in its own subfolder (`stage-1-foo/`, `stage-2-bar/`) and earlier stages are never overwritten. Tags are OPTIONAL because folder layout already preserves history.
- **Scope boundary:** Your scope is `C:\workarea\sandbox\{sandbox-name}\` only. Do NOT inspect, modify, or ask the user about files outside your sandbox folder — including untracked files in the parent repo, branch state, merge conflicts, or other sandboxes. Repo housekeeping belongs to the main session, not to you.
- **Canonical source of truth:** The Progress section of `{sandbox-name}/PROJECT.md` is the single source of truth for stage status (current stage, covered, next steps). The top-level `README.md` stage table and the `SANDBOX_INDEX.md` row must mirror it. If they ever diverge, PROJECT.md wins and the others get updated.

## Definition of "Stage Complete"

A stage is only complete when ALL of these exist:
- [ ] Stage folder under `{sandbox-name}/stage-{n}-{slug}/` containing every code file for the stage
- [ ] Stage-level `README.md` with WHY this stage exists, HOW to run it, an ASCII diagram, the production analog (or an explicit note that none exists yet), and a checking question
- [ ] Production-bridge comments in code files mapping back to real source locations
- [ ] Git tag created and pushed: `{sandbox-name}/stage-{n}/{concept}` — **mandatory for in-place evolution sandboxes, optional for side-by-side folder sandboxes**
- [ ] New row added to the Learning Stages table in `PROJECT.md`
- [ ] `PROJECT.md` Progress section updated (move concept from Next Steps → Covered, update Current Stage and Last Studied)    
- [ ] `SANDBOX_INDEX.md` row reflects the new status if it changed

**Stage completion rule:** For multi-stage walkthroughs, do NOT stop in the middle of a stage. Every item above must be done before stopping. The only valid mid-stage stop is if you genuinely cannot proceed without learner input about the LEARNING content itself (e.g. "should we use approach A or B for this stage?").

## Pre-Return Checklist (Hard Requirement)

Before returning control to the main session for ANY sandbox session, verify ALL of:
- [ ] `{sandbox-name}/README.md` exists, lists every stage with its current status, and explains how to run each
- [ ] `{sandbox-name}/PROJECT.md` exists and contains all 8 sections with REAL content (not stubs): Metadata table, Progress section, Learning Stages table, What the project does, The layers, The full request flow, How the patterns connect, What was simplified vs. real
- [ ] `{sandbox-name}/PRODUCTION-MAPPING.md` exists and cites REAL file paths with line numbers — never placeholders like `???`, `TODO`, or `(stage X)`
- [ ] `SANDBOX_INDEX.md` has a row for this sandbox whose status mirrors PROJECT.md
- [ ] At least one stage is "complete" per the definition above

If any item is missing or contains stub content, complete it before returning. Do NOT defer these to "next session" or ask the user about them.

## Clarifying Questions Are Scoped

Any question you ask the user must be about the LEARNING TASK only.

**Allowed:** concept scope, pacing, cadence, prerequisites, what they already know, which direction to take a lesson, related concepts they may also want to cover, alternative paths through the material.

**Forbidden:** repo housekeeping, file cleanup, branch state, untracked files, commit decisions, anything outside the sandbox folder. If you encounter something outside scope, ignore it and continue your task.
