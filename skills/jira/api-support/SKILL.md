---
name: api-support
description: Create product-project tickets (NRE, NFS, ...) for a client-reported API problem — project/type routing by environment, field conventions, problem-statement-only description, confirmation gates
user-invocable: false
---

# API Support Ticket Skill

**Parent skill:** [`~/.gemini/skills/jira/SKILL.md`](../SKILL.md) — its write-confirmation rules apply in full.

A client reports an API problem (usually by email or a CSR thread) and it is filed in the owning
**product** project for support investigation. **Diagnosis comes before filing, not instead of
it** — for `api-test-app`, that means
`.gemini/skills/hurl-conventions/references/authorization.md` → "Judging An Endpoint — Doc Before
Verdict": check repo coverage, the vendor doc and preview1, only then touch the client's
environment/key. This skill governs the ticket once that's done, not a
shortcut around it.

Not this skill:

| The ticket is... | Use |
|---|---|
| A confirmed defect raised to R&D to fix | [`../fco/SKILL.md`](../fco/SKILL.md) |
| An API key / access provisioning request to Cloud Services | [`../csr/SKILL.md`](../csr/SKILL.md) |
| A client-reported API problem to investigate in the product project | **this file** |

## Project by environment

Pick the project from the product segment of the client's URL (`https://{client}.nakisa.cloud/{env}/{product}/...`).

| URL segment | Project | Issue type | Verified |
|---|---|---|---|
| `/real-estate/` | NRE | Support Request | 2026-09-24 dp, NRE-11997 |

**Any other product (NFS, ...): add its row before the first ticket, never guess.** Find a recent
ticket in that project with `search_jira_issues` (JQL on the project key plus
`"Customer Commitment"`), then `get_jira_issue` on its key to read the field shape and copy it. If
none exists to copy, ask the user. Record the row here with the verifying ticket key.

## Fields

| Field | Default | Notes |
|---|---|---|
| Summary | `{Client} {env} API key returns {status} on {Product} API endpoints` | State the symptom as the client reported it |
| Priority | ask | NRE-11746 and NRE-11997 used High (client blocked); do not assume |
| Assignee | Dexter Pagkaliwangan (`60396b7af032740068924835`) | Unless told otherwise |
| Reporter | whoever creates it | **NRE rejects `reporter` on create** (`Field 'reporter' cannot be set`); omit it — Jira sets the caller. To make someone else reporter, update after creating |
| Customer Commitment | `customfield_13981`: `[{"value": "<Client>"}]` | Exact spelling — confirm with `"Customer Commitment" = <Client>` JQL first |
| Fix / Affect Version | none | Neither NRE ticket above carries one |

## Description — problem statement only, from the source only

- Only what the source (email, client report) states. No paraphrased asks, no inferred cause, no
  control/comparison endpoints the user didn't ask for. Quote the client's own ask.
- Details visible only in attachments or screenshots stay out unless the user asks for them.
- **No investigation findings.** They go in a later comment (below).
- Endpoints listed exactly as the client wrote them, including any wrong ones.
- Never include an API key, even one printed in the source.
- A requirement or question in the same source stays out of the ticket. Tell the user it belongs in
  that client's own requirements notes, not in the ticket, and, if
  R&D must answer it, in an FCO Support Request ([`../fco/SKILL.md`](../fco/SKILL.md) → "Support Request").
- Use `description_adf` (bullet list for endpoints).

Before showing the draft, check every line against the source text and drop anything not in it.

## Investigation comment — a separate gate

Written later, from evidence gathered in the evidence repo (for `api-test-app`, the `.hurl` runs).
Draft it in full, show it, and wait for its own confirmation; approval of the ticket does not cover
it. Endpoint paths and observed responses only — no repo paths, no keys.

## Confirmation gates

1. Fields table + full description draft → explicit confirmation → `create_jira_issue`.
2. Re-fetch with `get_jira_issue`; check Assignee, Reporter, Customer Commitment, description.
3. Comment → its own draft → explicit confirmation → `update_jira_issue(comment_adf=...)`.
4. Every later field change → show the change → confirm → update.

## What the tools cannot do

- **Attach files.** The Jira MCP tools download attachments but cannot upload. Email inline images
  can be viewed via `mcp__claude_ai_Microsoft_365__read_resource` on the attachment URI but not
  saved to disk. Tell the user which images are relevant and let them attach them.
- **Link issues.** Not settable via MCP `custom_fields`; see the REST call in
  [`../csr/SKILL.md`](../csr/SKILL.md) → "Conventions & Tips", or leave it to the user.
