---
name: fco
description: Create FCO (Financial Core) bug tickets with the correct structure, field conventions, and evidence format; a client question or requirement for R&D (not a defect) is a Support Request, see its section
user-invocable: false
---

# FCO Ticket Skill

**Parent skill:** [`~/.gemini/skills/jira/SKILL.md`](../SKILL.md)

**Dependencies:** `../api-support/SKILL.md` → "Fields" owns the Customer Commitment spelling.

## FCO Project Overview

- **Project Key:** FCO
- **Project Name:** Financial Core
- **Purpose:** R&D-facing defects and questions in the financial core products, including FOS (Financial Org
  Structure), User Auxiliary, and related microservices. This is where API and backend defects
  found by support/services teams, and client questions only R&D can answer, get raised to the owning dev team.
- **Issue types:** Bug for a defect (the rest of this file). **Support Request** for a client question or requirement for R&D that is not a defect: see "Support Request" below, not the Bug table. **Task** for tracking the documentation of a release's new endpoints: `../api-docs-tickets/SKILL.md`, not this file.

## Fields

Verified against 15 real FCO bugs (2026-02 through 2026-09). Applies to **Bug** only.

| Field | Default | Notes |
|---|---|---|
| Type | Bug | |
| Summary | | Plain statement of the symptom. No `Bug:` prefix, and no `FOS: ` area prefix. Some existing tickets carry one because FCO also holds User Auxiliary and NLA6 defects, but do not add it: for an API defect the endpoint path in the summary already identifies the area |
| Priority | **Medium** | Raise only with a stated reason. Observed spread: Medium 13, High 3, Critical 3, Low 2 of 21 |
| Affect Version | **N2026.R1** | Confirm per ticket if the defect is known to sit in a different release |
| Fix Version | **leave empty** | Settled by the requester 2026-09-14: an unfixed defect has no fix version, and the field is R&D's to set once they target a release. Do not populate it, do not copy Affect Version into it, and do not offer `N2026.R2` as an alternative |
| Assignee | **Asad Khalid** | |
| Status | **Dev-Pending** | Transition after creating; a new bug lands in the default open status. See the transition gotcha below |
| Reporter | whoever raises it | Jira sets this automatically from the calling account; do not set it manually |
| Severity | **do not set** | `customfield_11005` exists instance-wide but is unused on FCO: 0 of 21 tickets populate it |
| Resolution Path | `customfield_12000` | The one-line ask to R&D, e.g. "R&D to investigate and fix the delete path." It lives in this field only; the description body has no section for it (the template below ends at Workaround). **It is a seed value, not a record.** Existing FCO tickets show the dev replacing it with what they fixed, which is the field's settled use on this project, so expect the ask to be overwritten and do not treat it as the durable statement of what must happen. That statement is Expected Result, which stays in the description. Not governed by the 5-question format in `../templates/CONTENT-TEMPLATES.md`, which is scoped to LAE/NCS |
| Regression Analysis | `customfield_13057` | **Required on create.** `createmeta` reports it as optional, but a server-side validator rejects the call with `Regression Analysis field must be specified`. Values: Regression / Not Regression / Investigate |

**Fix Version, and why the observed majority is not the rule.** Most unresolved FCO bugs do carry
a `N2026.R2`-style value, so the field reads there as "targeted for" rather than "fixed in". That
is R&D populating it as they schedule work, not a convention the reporter follows. **We leave it
empty on filing**, and FCO-624 confirms the field is accepted empty: it was created blank, and was
picked up, reassigned and moved to Prod-Pending within hours with no bounce. Do not re-open this
as a judgement call per ticket.

## Support Request (client question or requirement, not a defect)

Type **Support Request**, never Bug or Enhancement.

| Field | Value |
|---|---|
| Assignee | the requester, unless told otherwise (not the Bug default) |
| Customer Commitment | the client, spelled as in `../api-support/SKILL.md` → Fields |
| Priority | Medium |
| Affect / Fix Version | empty |
| Resolution Path, Regression Analysis | not set |
| Status | on creation, leave at the default open status; closing has its own sequence (see "Creation and transition gotchas") |

These values created FCO-657 without a bounce.

Description: the client's own words verbatim, with a one-line source tag (email subject and date).
No paraphrase, no findings, no API key. Findings go in a later
comment, which is its own confirmation gate; shape and posting per SKILL.md → "Commenting on a Ticket You Reported and Own". Show Summary, every field and the complete description
before creating (the "Show the full draft" bullet under "Before filing").

## Two description formats

FCO uses two shapes. Pick by defect type, not by habit.

**UI defects** use numbered navigation steps:

```
<one-line statement>

Steps to Reproduce:
1. Log in to the build.
2. Navigate to <screen>.
...

Actual Result:
...
Expected Result:
...
```

**API / spec defects** use the template below. There is no UI path to walk, so the structure
states the contradiction instead. Reference example: FCO-426.

Plain labels with colons throughout. No markdown headers, no bracketed section names.

## API bug template

```
Issue
<What the endpoint does, in one or two sentences. Observed behaviour only.>
<How it was confirmed, e.g. "Confirmed by a separate follow-up GET after every attempt".>

API reference:
<full docs URL WITH the section anchor, not the page root>

Observed on <environment>.

Steps to Reproduce
1. <numbered, each step one API call, named by method and path>
2. ...

Actual Result
<verbatim status and the identifying fields of the response body>

Expected Result
<what should have happened instead. Never omit this.>

<Optional: a coverage table when a variable was swept, e.g. status or field presence.
State the observed outcome per case and nothing more.>

Reproducibility
<"Fails every time, on every record tested" plus any dimension deliberately varied.>

Related Endpoints
<Optional. Other endpoints observed returning the same response. State the shared
 observation ONCE as a lead-in, then list the endpoints under it, each with any
 qualifier that narrows it. Nothing further.>

Workaround
<One line, or "None known.">
```

The description ends at Workaround. What R&D is being asked to do goes in the **Resolution Path**
field, not in the body.

## Rules this template encodes

Each of these came from a real correction or a real rejection. They are not style preferences.

- **No root-cause analysis, and no code citations.** Investigating the cause is R&D's job, and
  a services-team source read is typically against a stale checkout. Offering a diagnosis risks
  sending the dev down the wrong path and costs credibility when it is wrong. State observed
  behaviour and stop.
- **Never assert design intent.** Do not write "behaving as designed", "intended", or "correctly
  rejects". Whether a given response is intended is R&D's call. Report the response, not its
  legitimacy.
- **No repo paths, script names or internal filenames.** The assignee cannot open our repo, so a
  path is an instruction they cannot follow, and it invites them to ask us to run something instead
  of reproducing it themselves. Name the endpoint and the request; that is reproducible from any
  machine. This applies to the reproduction collection's descriptions too, which is why that rule
  is stated here rather than in the Postman conventions.
- **No log-correlation or trace-id sections.** R&D reproduces on their own build and gets their
  own stack trace, so preview-environment timestamps and trace ids are close to useless to them.
- **No counts that go stale.** "Across 10 records over 3 weeks" is wrong the moment another test
  runs. Say "every record tested" instead.
- **No observation date in the body.** Jira stamps creation date. Keep the environment name,
  which Jira does not capture and which distinguishes a shared test env from a client env or a
  local build.
- **Do not reference attachments in the text** ("see attached screenshot"). The requester pastes
  images inline where they want them. Keep identifying response fields as text anyway, since
  text is searchable in Jira and survives an image failing to render.
- **Keep a coverage table when one variable was swept.** It is evidence, not diagnosis, and it
  preempts the most likely bounce ("did you try it on an active record?").
- **A related endpoint is named by its shared OBSERVATION, and the observation says WHICH
  response.** "`DELETE /bulk` returns the same 500 and the same rollback-only message" is a
  response we recorded; "`DELETE /bulk` is probably affected by the same bug" is a root-cause
  claim wearing a hedge. Quote the distinguishing part of the message and name the status code:
  a ticket carrying a coverage table holds more than one error, so "the same error text" makes
  the reader scroll back and guess. Worth including because it tells the dev what else to
  re-test after fixing, which is how a fix gets verified beyond the one endpoint on the ticket.
- **Naming a related endpoint does not cover it, and the record that says so is repo-side.** The
  section is a pointer, not scope: each endpoint still needs its own ticket (see "Before filing").
  **Do not annotate the lines with raised/not-raised status** (tried on FCO-624 2026-09-14 and
  removed): it reads as project tracking inside a defect report and goes stale the moment the
  sibling is filed. What records an endpoint as uncovered is its row in the evidence repo's defect
  register under "Evidenced, not yet raised" (for `api-test-app`, `hurl/TICKETS.md`) — that row
  exists precisely while no ticket does, which is when the information is needed. A Jira issue link
  is the *second* step, available only once both tickets exist: add it then and move the row up.
- **No em dashes in the description body.** A ticket or collection *name* may contain one.

## Creation and transition gotchas

Each observed on FCO-624 (2026-09-14), except the closing rule, which is the requester's.

- **Closing goes through Dev-Pending first.** Never close from the opening status. Transition to
  Dev-Pending, then close from there, setting Root Cause (`customfield_12301`) to **Product API** on
  the closing transition. Fetch both transition ids from the issue each time (a Support Request in
  `L2Sup-Creating` offers "Request Development" to Dev-Pending and "Reply" to close, as on FCO-657),
  confirm each transition before it runs, and re-read the assignee after each one. Set Resolution
  Path (`customfield_12000`) in the same call as the closing transition. For a ticket about an API it is
  one line, `Tested on <environment>: <METHOD /path> <outcome>.`, followed by one observed fact. Never
  "." and not the 5-question format.
- **Resolution Path on a transition must be an ADF document.** A plain string returns HTTP 400
  `Operation value must be an Atlassian Document` and the transition does not run (FCO-659, 2026-10-16).
  Send `{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"text","text":"..."}]}]}`.
- **Fix Version auto-populates from Affect Version.** Setting Affect Version `N2026.R1` on create
  silently produced Fix Version `N2026.R1` as well. Check and clear it after creating if the
  defect is unfixed.
- **A status transition can silently reassign the ticket.** Transitioning to Dev-Pending
  moved the assignee from Asad Khalid to a different account. Re-read the
  assignee after every transition and restore it with a REST `PUT` if it moved. Fetch transition
  ids from the issue rather than reusing an id seen elsewhere.
- **Links are only clickable if the description is ADF.** The MCP `description` parameter takes
  plain text, which stores a bare string with no `link` mark, so a pasted URL renders as dead
  text. Build the description as an Atlassian Document Format document and PUT it via
  `rest/api/3/issue/<key>`, giving the URL a `link` mark.
- **ADF paragraphs collapse leading whitespace.** Anything alignment-dependent (numbered
  reproduction steps, a `errorCode`/`message` block, a status coverage table) must be a
  `codeBlock` node or it reflows into a single run-on line.

## Reproduction collection in Postman

Settled 2026-09-14 dp on FCO-624.

**Every FCO bug gets a Postman collection that reproduces it.** The assignee has to reproduce the
defect to fix it, re-run it to verify the fix, and PQA runs it again after that, so a collection
with real ids and a working key already filled in is the cheapest form of the Evidence rule below.

**Order: collection first, ticket second.** Build it while the evidence is still being gathered.
Naming it before the key exists is the only wrinkle:

1. Name it after the symptom alone, no key: `Cost Center DELETE returns 500`. Never invent, guess
   or reserve a ticket key.
2. File the ticket. Its Steps to Reproduce falls straight out of the request list.
3. Rename the collection in place to prepend the key. **Rename, never recreate** - the collection
   id is what any already-shared link points at.
4. Record it in the evidence repo's defect register, in the same pass. A ticket recorded nowhere
   local is findable only by remembering its key.

The requester may ask for the collection on its own, before deciding whether to raise a ticket at
all. That is step 1, and it commits to nothing further.

**The collection's descriptions carry the same keep-outs as the ticket body** ("Rules this
template encodes" above): observed request, observed response, stop.

**Everything about the collection itself** - which Postman workspace, how it is named and shaped,
hardcoded values over variables, per-request doc deep links, pairing every mutation with a
confirming read, and which register row to add - is owned by the evidence repo's own conventions,
not restated here. For `api-test-app`: `.gemini/skills/hurl-conventions/references/postman-handoff.md`
-> "Naming — a fourth pattern: bug-reproduction collections", and `references/repo-files.md` -> "hurl/TICKETS.md".
This section owns only where those steps sit in the ticket workflow.

## Before filing

- **Triage severity before raising.** Raise now: an operation that does not do its job (a delete that
  deletes nothing), or a write that reports success without persisting. Flag but do not raise yet: a
  call that is rejected, but with the wrong status or an internal message (a 500 where a field error
  is expected). Record it in the evidence repo's register as a minor row (for `api-test-app`:
  `hurl/TICKETS.md` → "Evidenced, not yet raised", Symptom starting `**Minor.**`), and raise it only
  when asked, when a client hits it, or as its own ticket filed together with a related one.
- **Build the reproduction collection first** (see the section above), so the draft's Steps to
  Reproduce describes requests that already exist and run.
- **Every endpoint named in `Related Endpoints` has a register row before this ticket is filed.**
  Without it the siblings are recorded nowhere: the ticket deliberately does not say they are
  unraised, and no Jira link can exist yet. Filing without the rows is how a sibling gets closed
  as collateral when this ticket's fix lands.
- **Show the full draft and wait for explicit approval before creating anything.** Never call
  `create_jira_issue` (or update an existing FCO ticket) off the back of "draft me a ticket" or
  "that looks good" on an earlier fragment. Show Summary, every field value, and the complete
  description body as it will appear, then stop.
- **Search FCO for duplicates first.** FCO-426 was rejected by the assignee as a duplicate of an
  existing ticket. Search on the endpoint path and on the symptom wording.
- **Arbitrate ambiguous defects with R&D before raising.** A defect that could plausibly be read
  as intended behaviour will be closed working-as-designed. Confirm it is actually wrong first.
- **One ticket per endpoint, not per suspected cause.** Naming a sibling in `Related Endpoints` is
  never an alternative to filing its ticket. The test between the two mechanisms: a shared
  *observation* (same status and message) goes in `Related Endpoints`; a parent bug is for when
  the narrative itself is the deliverable, and each endpoint still gets its own linked sub-bug. Grouping several endpoints under one
  shared cause breaks the closure model: each route has its own fix scope, may go to a different
  assignee, and needs independent version targeting and PQA verification. When several endpoints
  genuinely share a narrative, raise a parent bug carrying the narrative plus one linked sub-bug
  per endpoint.

## Evidence

- Copy-pasteable requests beat screenshots, because the assignee has to reproduce the defect to
  fix it, then re-run it to verify the fix, and PQA runs it again after that. FCO-428 put its
  entire reproduction in eight screenshots and a three-line description; treat that as the
  anti-pattern.
- Screenshots are still good supporting evidence that the behaviour was really observed. Use both
  where available: text for reproduction, image for proof.
- **Check screenshots for credentials before attaching.** An API key visible in a request headers
  pane is the same exposure as pasting it in text, and harder to notice.
