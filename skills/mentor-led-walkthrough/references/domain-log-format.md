# Domain Log — Format Reference

A fourth artifact — distinct from the journal, the Build Log, and the Recreation Guide. Created
at the first slice entry of a session and updated (upserted) at every subsequent slice entry,
across sessions.

**Purpose:** an extraction source a reader can open on its own — no code, no round bodies, no
restart history, no process log — and still be able to state, for every slice reached, what its
core business concept is and why the capability exists. This is the only file in this skill's
output built to be readable by someone who never opens the source code.

**File:** `{project-root}/mentor-logs/domain-<artifact-slug>-all-slices.md` — undated and
cumulative, same pattern as `uml-<slug>-all-slices.md`. Mode B reenactment already carries its
own slug (e.g. `...-reenact`), so a reenactment session and a real project session never share
this file.

**Extraction source only.** Promotion to a project's own permanent domain-knowledge store (if one
exists) happens in a separate session, outside this skill — never write there directly. This
mirrors CB-3's existing rule for engineering-journal runbooks: "suggests only — write happens in
a separate session."

## Write timing

Written the same turn Slice Entry items 1–2 are stated in conversation, before any file in the
slice is opened. **Upsert by slice heading** — a restarted slice rewrites its own section in
place; it never appends a second section for the same slice. Applies in all modes, including
`--auto`.

## Entry format (one section per slice)

```
## Slice <N> — <slice title>
status: complete | incomplete — item 1 pending | n/a — no business entity in this slice

**Is:** <item 1 — ≤3 lines, business vocabulary only, no fields/classes/columns/code>
**Evidence:** <file>:<line> — <what that line proves> | spec: <story/FR, if one exists>

**Without it:** <item 2 — causal template, ≤4 lines, domain-novice test applied>
**Trigger:** <entry-point file>:<line> — <route / UI action> | spec: <story/FR, if one exists>

**Done when:** <one sentence — what the user can do once the slice ships>

superseded: <prior wording + the rule it violated>   (omit this line if none)
review: <[REVIEW] note>                                (--auto only; omit otherwise)
```

## Rules

- **Business vocabulary only** in `Is:` and `Without it:` — the evidence line carries the
  `file:line`, never the definition body. The tag is a pointer, not a quotation: never reproduce
  a field, column, annotation, or class name inside `Is:`/`Without it:` themselves.
- **Degenerate cases:** two co-equal core entities in one slice → one `Is:` line each, plus one
  sentence naming the relationship between them. No identifiable business entity (pure
  infrastructure/composition slice) → `status: n/a — no business entity in this slice`, omit
  `Is:`/`Evidence:`.
- **Escalation mid-gate:** if item 1 is routed to agent-concept-tutor instead of being stated
  inline, write `status: incomplete — item 1 pending` now; on return, update to `status: complete`
  and add `covered in concept lesson: <topic>` under `Is:` rather than re-deriving it.
- **Autonomous (`--auto`):** never blocks on escalation — no learner exists to accept the offer.
  Derive inline from code evidence; if it cannot be derived, write
  `review: [REVIEW] domain definition unavailable — <entity>` and proceed regardless.
- **One violation/correct pair is enough** — do not accumulate a running list of anti-patterns in
  this file; the worked example belongs in `SKILL.md` itself (Slice entry item 2's anti-cheat
  clause), not duplicated per slice.

## Example

```
## Slice 1 — Create Vendor Agreement
status: complete

**Is:** A Vendor Agreement is the top-level contract a company signs with a supplier — the
umbrella agreement one or more individual purchase orders live under. It sits above Purchase
Order, because every purchase order must point back to exactly one vendor agreement to exist at
all. It is mandatory — without one, a purchase order has nothing to attach to.
**Evidence:** PurchaseOrder.ext:42 — its foreign-key field to the vendor agreement is declared
non-nullable, so the database refuses a purchase-order row with none attached.

**Without it:** a company has no way to record that it has entered into a supply contract with a
vendor at all — the agreement would only exist on paper or in someone's inbox, which breaks
because the company cannot track what contracts it has signed, work out what it owes and when
payments fall due, or include them in the financial statements it is legally required to publish.
**Trigger:** EntryPointController.ext:20-24 — the generic create-or-update entry point that the
Vendor Agreement's own controller inherits.

**Done when:** a user can submit a new vendor agreement through that entry point and have it
durably recorded with a system-assigned identity and a starting workflow state.

superseded: "...which breaks because nothing downstream (the order-processing engine, the
invoicing job, the reporting dashboard) can ever see or act on it" — named systems as the
consequence instead of a business one (anti-cheat violation).
```
