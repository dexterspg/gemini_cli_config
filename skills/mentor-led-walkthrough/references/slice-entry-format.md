# Slice Entry — Items 1–2 Full Format Reference

Full detail for Slice entry items 1 (Domain definition) and 2 (Business requirement) — the
condensed version lives inline in `SKILL.md` under Live Coding Sequence → Slice entry. Read this
file for worked examples, edge cases, and mode-specific handling that don't fit inline.

## Item 1 — Domain definition of the core concept

Fires **every slice, unconditionally** — it is not gated on build order, because items 2–5 are
unreadable without it. Take the head noun of the slice title (e.g. "Create **Master Agreement**")
and fill:

`[Concept] is [one-sentence business definition — what kind of real-world thing it is].
It sits [above / below / beside] [related concept] because [business reason].
It is [mandatory / optional] — [what happens when it is absent].`

**Business-vocabulary ban list** (canonical — cited by name from every other site that needs it):
no field names, no class names, no types, no column names, no method names, no annotation names,
and no code — those belong to that file's "What it is" slot when it is reached. The citation line
(Evidence / Trigger / provenance tag) is exempt — naming the construct it cites is that line's
job. ≤3 lines here. No diagram (item 4 owns it).

**Mode B (no PRD) — derived, never waived.** Derive from the code's own structure — the entity's
parent/child relationships, the nullability of its links, or the UI label a user sees — and tag
`(derived from code — no spec: <file>:<line>)`. **Anti-cheat:** naming the class and its `extends`
clause is not a definition, and a tag pointing at the entity's own declaration line does not
satisfy this — cite the line that evidences the *relationship or optionality* you claim.

**Provenance tag rule** (canonical — cited by name from every other site that needs it): the tag
is a *pointer, not a quotation* — cite `<file>:<line>` as evidence for the claim; never reproduce
that line's field, column, annotation, or class name inside the claim itself. The citation line
may name the construct; the claim line may not.

**Overflow:** if the definition cannot be stated in three lines of business vocabulary without
naming fields, do not expand it — fire **Concept suggestion** (Phase 3) and route to
agent-concept-tutor. On escalation, record the gate in the pre-escalation session-state summary as
`SLICE ENTRY INCOMPLETE — item 1 pending`; on return, close item 1 as
`covered in concept lesson: <topic>` and never re-teach it.

**On decline** (learner chooses to press on instead of escalating): write the shortest
business-vocabulary statement achievable, log it as `status: incomplete — item 1 declined` in the
domain log, and do not expand into the full inline lesson Phase 3's Concept-suggestion decline
branch would otherwise invite — that branch is superseded here by this one.

**Degenerate cases:** two co-equal core entities → define both, one line each, and name the
relationship between them. No identifiable business entity (pure infrastructure or composition
slice) → write `Domain definition: n/a — no business entity in this slice.`

**Autonomous (`--auto`):** never escalate. Produce the item inline from code evidence and log
`[REVIEW] domain definition derived without spec: <entity>`. If it cannot be derived, emit
`[REVIEW] domain definition unavailable — <entity>` and proceed — this gate must never block a run
with no learner to unblock it.

**Altitude split (enforced):** this item defines the *business object*; the per-file "What it is"
defines the *class*. When that file is reached, its "What it is" opens `implements: [concept]` and
goes straight to code-grounded structure — restating this definition is a violation, not
thoroughness.

## Item 2 — Business requirement

Why this capability must exist at all, stated before any file is named:
`Without this, [business actor] would [manual workaround, or have no way to do it], which breaks
because [concrete business consequence].` Per the Business-vocabulary ban list (item 1) — those
names belong to items 3–5. Then one sentence on what the user can do when done. ≤4 lines total.

**Domain-novice test** (apply to every noun in this slot before moving on). A reader with no
training in this business domain must be able to understand every term used. Each term must pass
one of three:
(a) plain-language self-evident on its own (`invoice`, `monthly payment`, `signed agreement`);
(b) already defined in item 1; or
(c) replaced by its plain-language *effect* rather than its name.
Any term failing all three is rewritten, not footnoted.

**Anti-cheat — naming downstream systems is not a consequence.** A list of components, engines,
jobs, or modules that "cannot see the data" states a *plumbing* fact, not a business one. The
consequence clause must name what a **person** cannot do, or what the **business** gets wrong, in
terms that survive with all system names deleted.
- Violation: `…which breaks because nothing downstream (the order-processing engine, the
  invoicing job, the reporting dashboard) can ever see or act on it.`
- Correct: `…which breaks because the company cannot track what it has agreed to, what it owes,
  or when payments fall due.`
Domain-specific component names are reintroduced later at items 4–5 and in File narration, where
they map onto real files — never here.

**Mode B (no PRD) — derived, never waived.** Derive from the slice's entry point — the route, UI
action, or external trigger a user actually hits — and tag
`(derived from code — no spec: <entry-point file>:<line>)`. A bare tag without a cited entry point
does not satisfy this; neither does citing an internal collaborator or a persisted table. Cite a
PRD story/FR instead only when one genuinely exists. The Provenance tag rule (item 1) governs this
tag too — the tag names the entry point; the causal sentence itself never does.
