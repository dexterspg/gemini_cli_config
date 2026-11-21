---
name: api-docs-tickets
description: "Create the documentation Task that tracks a release's new API endpoints, one per product, in each product's own Jira project (FOS, NFS, NRE, NRM, VP, GL, P2P): project map, fields, description template, mention line, duplicate check and gates. Not for a defect or a client-reported API problem"
user-invocable: false
---

# API Docs Tickets Skill

**Parent skill:** [`~/.gemini/skills/jira/SKILL.md`](../SKILL.md) — its write-confirmation rules apply in full.

**Dependencies:** parent → "Creating LAE Tickets" (mention nodes); `../api-support/SKILL.md` → "What the tools cannot do"; `../fco/SKILL.md` → "Rules this template encodes".

One Task per product per release, filed after the api-doc update has produced the new-endpoint list.

**Input.** In `C:\tw\api-doc-docs`, `projects/api-doc/engineering-log/runbooks/update-from-preview-build.md`, step "Raise the Jira tickets": per product, the new endpoints by tag with counts, and `<code>-<version>-new-endpoints.json`. Repo absent or file missing → stop and ask. The user states the release version each time (for example `N2026.R2`). Never infer it, and never assume the build equals the released version.

## Project map

| Product | Project | Verified |
|---|---|---|
| FOS | FCO | FCO-699 |
| NFS | NFS | NFS-19873 |
| NRE | NRE | NRE-12146 |
| NRM | NRM | NRM-3405 |
| NVP | VP | VP-371 |
| SPB | GL | GL-746; unconfirmed, project SPB also exists: ask a GL owner |
| AP | P2P | P2P-2098 |

Any other product (NHS, UA, ...): add its row before the first ticket, never guess; method in `../api-support/SKILL.md` → "Project by environment".

## Fields

Type **Task**; a Support Request is rejected without Customer Commitment. Priority Medium. Assignee Dexter Pagkaliwangan (`60396b7af032740068924835`). Fix Version = the stated version, which must be in the project's version list (REST `project/<KEY>/versions`) before drafting. Affect Version, labels, Customer Commitment, Reporter: not set. FCO's "Fix Version: leave empty" is for Bugs only.

## Description

Plain labels with a colon, no markdown headers. No environment names, repo paths or script names (`../fco/SKILL.md` → "Rules this template encodes").

    Purpose: Track the documentation update for the endpoints that the <PRODUCT> build adds to the API definition.

    Source:
    Build: <PRODUCT> <version>
    Endpoint list: <code>-<version, lowercase>-new-endpoints.json (attached)

    Scope:
    New endpoints: <n>
    Changed method: <n> (<OLD> to <NEW> on <path>, one per method change)
    By tag (ticked when published):
    [ ] <tag>: <n> new, <m> without description    (one line per tag, most new first)

    New endpoints:
    <one line each, "METHOD path (operationId, tag, parameters)", only when the product has 10 or fewer new endpoints; otherwise "see the attached list.">

    FYI <mention Catalina Fulger> <mention Ali Harb>

"Without description" means the spec has no description for that operation. The published text comes from the generated description config, so for NRE, NRM and VP every line reads "without description". Keep the wording and do not explain it in the ticket. Changed methods are not counted in "New endpoints".

## Mentions

Build the description as ADF and pass it as `description_adf` on create, with the FYI line as the last paragraph: `FYI `, a mention node, a space, a mention node. Node: `{"type":"mention","attrs":{"id":"<id>","text":"@<Name>","accessLevel":""}}`. Ids: Catalina Fulger `60ba747313c0e9006913d1d6`, Ali Harb `557058:73373cee-8386-4eea-945c-8eef3054ae9b`. No `localId`; add one only if view mode shows a difference. Mention people only at create. Later changes go in a comment (its own gate); never re-send the mention nodes in a description update. Whether such an update notifies again is unverified, and so is delivery of the mention.

## Gates

1. **Duplicate check, per project, before any draft:** `project = <KEY> AND summary ~ "new <PRODUCT> endpoints" AND fixVersion = "<version>"`. A hit → show it and stop for that product; a later change goes in a comment, never a second ticket.
2. **Draft all products in one message:** every field, the spec's save date beside the version, the full description. One explicit yes per ticket creates only that ticket. A product with no new endpoints gets no ticket.
3. **After each create, re-fetch:** type, status To Do, assignee, Fix Version, the description and the two mention names. Do not transition. Report the keys created so far.
4. **Finish with one line per ticket:** attach `<file>` to `<KEY>` (`../api-support/SKILL.md` → "What the tools cannot do").
5. **Removals** (endpoints in the live docs but not in the new spec) get their own ticket only when the user asks.
