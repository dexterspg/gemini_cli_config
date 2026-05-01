# Checklist: Project Documentation

**Step 0 — Pre-flight (run before scoring anything):**
- [ ] Loaded `~/.gemini/skills/documentation-specialist/SKILL.md` → **Controlled Vocabulary** section? Tier labels, status values, and document types are only valid as written there. Do not flag a term until you have found (or failed to find) its row in that table. If no row exists prohibiting it, do not flag it.

**Before reviewing:** Read `~/.gemini/skills/documentation-specialist/SKILL.md` for templates, audience definitions, and the agent-to-file mapping.

## Template Adherence
- [ ] File follows the correct template from the doc skill?
- [ ] All required sections present (no empty placeholders left)?
- [ ] "Last Updated" line with change note at bottom?
- [ ] `domain/*.md` deep dives — navigation header (`> Part of ... | Parent: DOMAIN.md | Index: 00-overview.md`) present at line 1?
- [ ] `domain/*.md` deep dives — all Core sections present as defined in the Section inclusion guide in the deep dive template (Overview, Key Concepts, How It Works, Integration Points, Business Rules, Observability, Diagrams, Source Files, Related)?      

## Audience Match (critical — each file has a different reader)
- [ ] README.md — technical but approachable for new team members?
- [ ] INTEGRATION.md — precise, every row is a contract?
- [ ] DEPLOYMENT.md — dense, copy-paste ready for DevOps?
- [ ] API-REFERENCE.md — zero ambiguity, no need to read source?
- [ ] BUSINESS-CASE.md — zero jargon, problem-first for executives?
- [ ] TECH-STACK.md — dense, version-exact, no fluff?

## Content Quality
- [ ] Diagrams present where 3+ components interact?
- [ ] All `diagrams/*.md` files have a `> Referenced from:` line after the title and a `## What This Shows` section at the bottom?
- [ ] Tables used for structured data (not prose)?
- [ ] Code examples are real (not placeholder `[TODO]`)?
- [ ] Cross-references link to related docs (INTEGRATION ↔ README)?
- [ ] No future tense / roadmap ("we plan to...") — document what IS?
- [ ] Consistent naming with actual codebase (class names, paths)?
- [ ] DOMAIN.md state machine diagrams — if the diagram covers only one mode or simplified path, is it labelled "Simplified" with a link to the relevant deep dive for full coverage?
- [ ] No real credentials, API keys, tokens, or passwords in prose, code snippets, or examples? (Replace with `<placeholder>` and note where the actual value is stored)
- [ ] Prose descriptions consistent with adjacent code snippets? (Flag contradictions: e.g., "false = do not drop" alongside "recreated fresh")
- [ ] Procedures described in How It Works completable from the doc alone? (If an external artifact is required — license file, certificate, seed data — is acquisition documented?)
- [ ] Observability section lean? (Max 5 "check first" items; detailed diagnostic flows and reproduction steps belong in `issues/`, not here)

## Completeness Per Tier
- [ ] Minimal tier: README.md present?
- [ ] Standard tier: + INTEGRATION.md + DEPLOYMENT.md?
- [ ] Full tier: + API-REFERENCE + TECH-STACK + FRONTEND + BUSINESS-CASE + DATABASE?
- [ ] Framework-Minimal tier: README.md + DOMAIN.md + at least one diagram?
- [ ] Framework-Standard tier: + `domain/` deep dives covering all applicable extension point categories (CRUD hooks, data access, state machine/workflow, security model, supporting utilities)?
- [ ] Framework-Full tier: + TECH-STACK + FRONTEND (if UI layer is present)?

**Verdict guidance** (global default applies — see CHECKLISTS.md)
