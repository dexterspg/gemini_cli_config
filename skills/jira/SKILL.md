---
name: jira
description: >-
  Jira field mappings, JQL patterns, ticket workflows, and MCP tool
  conventions. Use before any Jira operation — creating, searching,
  updating, or closing tickets. Triggers on: "create a ticket",
  "search Jira", "close this ticket", "log time", "find tickets for
  [customer]", "JQL", "LAE ticket", "NCS ticket", "filter by customer",
  "check assignee", "verify version", "find this contract owner", "comment
  on [KEY]", "post an update on [KEY]", "attach a file to [KEY]", "send
  the script to the reporter", or any mcp__jira__* tool usage.
---

# Jira Skill: Field Mappings & Conventions

> **HARD RULE:** Jira operations use `mcp__jira__*`; where it lacks the operation (an ADF description on an existing issue, transitions that set screen fields, file upload, a comment edit) use the Jira REST API as the section for that operation says. NEVER use an Atlassian connector for Jira: `mcp__plugin_atlassian_atlassian__*` or `mcp__claude_ai_Atlassian__*` (Confluence only).

**Operational Rules:**
- **NEVER write comments on NCS tickets** — all communication goes through linked LAE ticket (customer-facing only)
- **NEVER skip Mandatory Sequence** — re-fetch and verify Assignee fields after every create/transition on LAE tickets

**Do NOT trigger for:**
- Confluence operations (e.g., writing pages, creating spaces) → Atlassian plugin (`mcp__plugin_atlassian_atlassian__*`), not this skill
- Content generation from ticket data → `jira-content` skill (main session, after you fetch the ticket)
- Time tracking routing decisions → `agent-time-tracker`

## Sub-Skills

Sub-skills are not in the skill listing; this table is their only trigger.

| Sub-Skill | Path | Purpose |
|-----------|------|---------|
| CSR (Cloud Services) | [`csr/SKILL.md`](csr/SKILL.md) | Create CSR tickets with correct required fields, custom field IDs, and valid option values |
| FCO (Financial Core) | [`fco/SKILL.md`](fco/SKILL.md) | Raise FCO bugs to R&D, or a client question or requirement for R&D (Support Request): field conventions, the API-defect template, and what to leave out. Load before drafting any FCO bug or Support Request |
| API Support (NRE, NFS, ...) | [`api-support/SKILL.md`](api-support/SKILL.md) | File a client-reported API problem in its product project: project/type by environment, fields, problem-statement-only description. Load before drafting one |
| API docs tickets (any product project) | [`api-docs-tickets/SKILL.md`](api-docs-tickets/SKILL.md) | Raise the documentation Task for a release's new endpoints in each product's project (FOS, NFS, NRE, NRM, VP, GL, P2P). Load before drafting one; not for a defect or a client-reported problem |

## NCS → LAE Ticket Workflow

When the user has an NCS ticket in their time tracker and wants to create a corresponding LAE ticket, follow these steps **in order**, pausing for confirmation at each gate:

1. **Fetch** the NCS ticket via `mcp__jira__get_jira_issue`
2. **Present** proposed LAE ticket fields (summary, type, priority, assignee, reporter, versions, customer, description) → **wait for user confirmation**
3. **Create** LAE ticket via `mcp__jira__create_jira_issue` with ADF description (ADF mention for Dexter)
4. **Fix** Assignee: Development (`customfield_13004`) immediately after creation
5. **Add comment** using the same wording as the last similar ticket (re-read from Jira, do not assume) → ADF mention for reporter
6. **Present** Root Cause → **wait for user confirmation** (LAE has no Resolution Path field)
7. **Close** via REST API transition 801 with Root Cause
8. **Re-fetch** → verify and fix Assignee + Assignee: Development if overridden
9. **Log time** in Jira via `mcp__jira__log_work_on_issue` using the time from the tracker entry
10. **Update time tracker** via agent-time-tracker — `edit --id=X --field=ticket --value=<LAE key>`, then `mark-jira-logged --id=X` after step 9 is confirmed

**Rules:**
- "Yes proceed" at step 2 only triggers step 3 — NOT the full chain
- Always re-read the comment from the previous similar LAE ticket directly from Jira before reusing it — never rely on memory
- Root Cause confirmation (step 6) is a mandatory separate gate — never skip it

---

## Confirmation Before Write Operations

**MANDATORY** for ALL write operations (`create_jira_issue`, `update_jira_issue`, `copy_jira_issue`, `log_work_on_issue`) and for REST writes (attachment upload, comment edit, description `PUT`):

1. Show the user a clear summary of the proposed changes
2. Wait for explicit confirmation before executing
3. Do NOT call the write tool until the user confirms

**MANDATORY — Content fields (description, comment):**
- ALWAYS show the full draft to the user and wait for explicit confirmation before writing
- This applies to: ticket description and any comment
- Each content field is a separate confirmation gate — never bundle them into one "yes"
- A prior "yes" to create the ticket does NOT cover description or comment
- A file embedded in a comment or description is uploaded only after the explicit yes on that content; that one yes covers the upload and the post (or `PUT`)

**Preview format:**
- **Creates:** show all fields that will be set
- **Updates:** show only the fields being changed
- **Copies:** show the source ticket and any overrides
- **Long text fields:** show a truncated preview

## Commenting on a Ticket You Reported and Own

Applies when a `get_jira_issue` re-fetched right before posting shows Dexter Pagkaliwangan as both Reporter and Assignee (e.g. an FCO Support Request the user raised), in any project except NCS. The test is the fields, not who created it; on an LAE clone fix the reporter first. On LAE it replaces the Investigation Comment Template only in that case, and `workflows/LAE-WORKFLOW.md` still loads first; an LAE ticket with another reporter keeps the template. Elsewhere any other combination (reporter only, assignee only) has no fixed shape: ask the user. On FCO, `fco/SKILL.md` → "Rules this template encodes" also applies to the comment.

- **Shape:** the bold word `Update:` alone as the first paragraph, then one to three sentences on what was checked and found, then short list items for per-field or per-case outcomes. No greeting, no mention, no sign-off.
- **Content:** only what a live run confirmed, stated as observed, naming the environment. No repo paths, script names or source citations, nothing read only from source or docs. Scope statements are allowed ("every record tested"); untested claims are not. Client environment: counts and field names, never values.
- **Gate:** per "Confirmation Before Write Operations", with the runs behind each claim listed beside the draft. Post only on an explicit yes to the latest full draft; every revision re-shows it. A comment paired with a transition is its own gate, and the transition keeps its own sequence.
- **Posting:** `mcp__jira__update_jira_issue(issue_key=..., comment_adf=<ADF doc>)`; never an Atlassian connector's `addCommentToJiraIssue`. ADF body: `Update:` as a bold paragraph, `bulletList` for items, `codeBlock` for aligned content (requests, response fields, tables), a `link` mark for any URL. UNVERIFIED: `comment_adf` has not been run in this suite; read the comment back on first use. Confirm it landed by re-fetching the issue; after a timeout or error check for the comment before posting again.
- **After posting:** a comment alone changes no status or assignee, so the Mandatory Sequence does not run for it; re-fetch status and assignee once and report any change. A transition that accompanies it runs its own sequence (e.g. the FCO close through Dev-Pending).

Example body:

```
Update:
Re-tested on preview1: <what>. <result>.
- <case>: <outcome>
```

Authoring-time only.

## Quick Reference: Custom Field Names

When querying or filtering Jira tickets, use these field names instead of common aliases:

| Alias | Correct Field Name | Usage | Example |
|-------|-------------------|-------|---------|
| customer | `"Customer Commitment"` | Filter tickets by customer/account | `"Customer Commitment" = Fairprice` |

## JQL Syntax Rules

**Critical constraints:**
- Use `"Customer Commitment" = "value"` (exact match only) — fuzzy search `~` does NOT work with this field
- Use exact username format: `assignee = "zark.ahmed"` (lowercase, dot-separated) — fuzzy search `~` does NOT work for usernames
- Always verify customer name spelling against the field value directly (e.g., "Fairprice" not "Fair Price") — values are case-sensitive
- If search returns 0 results: widen filter or check spelling by fetching a known ticket belonging to that customer and reading the `Customer Commitment` field value

## Common JQL Patterns

### Search by Customer and Assignee
```jql
"Customer Commitment" = Fairprice AND assignee = "lionel.malonga" AND status = Closed
```

### Search by Customer Only
```jql
"Customer Commitment" = Fairprice AND status = Closed
```

### Search by Assignee with Customer Filter
```jql
assignee = "lionel.malonga" AND "Customer Commitment" = Fairprice
```


## MCP Server Configuration

For server setup, credentials, and troubleshooting see `~/.gemini/skills/jira/reference/MCP-CONFIG.md`.


## Downloading Attachments

**This is the canonical attachment-download protocol** — do not duplicate elsewhere.

### Preferred: `mcp__jira__download_jira_attachments`

The Jira MCP server exposes `download_jira_attachments(issue_key, output_dir, filename_filter="")`. It centralizes auth, follows the S3 redirect, verifies each file (size > 0 and not an HTML error page), and returns a per-file OK/FAIL/SKIP summary. Use this in almost all cases.

```
mcp__jira__download_jira_attachments(
    issue_key="LAE-44173",
    output_dir=r"C:\Users\dpagkaliwangan\git0\issues\LAE-44173-batch-posting-450-contracts\attachments",
    filename_filter="logs"   # optional: case-insensitive substring match on filename
)
```

If the MCP tool is unavailable, load `~/.gemini/skills/jira/reference/ATTACHMENT-PROTOCOL.md` for the REST API fallback and failure categorization.

---

## Known Issues & Leads

Consult before reporting "no tickets / no user found". A lead is a hypothesis: if it misses, say so and continue. Add one only after a miss then a confirmed hit, with the user's yes.

- **JQL on `customer` returns 0 or errors** → use `"Customer Commitment"`; the field "customer" does not exist in this Jira instance.
- **Customer value returns 0** → spelling is inconsistent (e.g., "Fairprice" vs "Fair Price"): probe a known ticket of that customer and use its exact `Customer Commitment` value, not the company skill's name.
- **Own tickets** → `assignee = currentUser()`, more reliable than hardcoding a username.
- **Partial name, need a username for JQL** → a support-team member: `C:/workarea/references/support-team.md` has the JQL name (file absent → ask). Anyone else: get the full display name, then `text ~ "Full Display Name"` to find any ticket, then use that ticket's `assignee` as the exact username.


## LAE Workflow Map

**MANDATORY:** Before performing any status transition, comment, or ticket closure on an LAE ticket, you MUST load `~/.gemini/skills/jira/workflows/LAE-WORKFLOW.md`. Do NOT guess transition IDs, status names, Root Cause IDs, or closure fields — all are defined in that file. Proceeding without loading it is a workflow error.

---

## LAE Ticket Conventions

### Creating LAE Tickets

When creating LAE tickets (for clones, see **Cloning LAE Tickets**):

- **Type:** Always default to **Support Request** unless explicitly told otherwise
- **Assignee:** Always default to **Dexter Pagkaliwangan** (`accountId: 60396b7af032740068924835`) unless explicitly told otherwise
- **Reporter:** Use the **assignee of the linked NCS ticket** (not the reporter), unless explicitly told otherwise. If no linked NCS ticket exists, take the reporter per the `company` skill → `customer-lookup.md` → "## Rules" 1
- **Fix/Affect Versions:** If the source or linked NCS ticket has no versions, find the latest BP (or relevant customer) ticket in NCS or LAE with those fields populated and copy from there
- **Affect Version (if name rejected):** Look up the version ID via REST API (`/rest/api/3/project/LAE/versions`) and pass it via `custom_fields` as `{"versions": [{"id": "VERSION_ID"}]}`
- **Mentions in description:** Always use Jira's built-in ADF mention node — never plain text `@Name`. Pass it as `description_adf` on `mcp__jira__create_jira_issue`; to change it later use REST `PUT /rest/api/3/issue/LAE-XXXXX` (update takes plain text only)

### LAE Description Template

The description is written **from the reporter's perspective, addressed to the assignee (Dexter)**. Default tone is **before investigation** — describe only what is visible in the UI or reported by the client. Do not include root cause, stack traces, or investigation findings unless explicitly asked.

Write as natural flowing paragraphs. **No section labels** (never use `[CONTEXT]`, `[REQUEST]`, `[ENVIRONMENT / SCOPE]` or any bracketed headers).

```
Hi @[Assignee ADF mention],

[Background: reference the linked NCS ticket, the customer, and what the client reported.]

[Request: what is being asked — investigate, write a script, write a SQL query, fix, etc. — with any specific conditions or criteria. When scripts are involved, Dexter **provides** the scripts; the reporter/customer **applies** them. Never say Dexter applies scripts.]

Thank you
```

**Attachments in a description:** a file or screenshot that belongs to the description is **embedded in it** (an ADF `mediaGroup` node for files, `mediaSingle` for images), never only added to the ticket's attachment list. Steps: `reference/ATTACHMENT-PROTOCOL.md` → "Upload and Embed in a Comment or Description".
- **Order:** a file can be uploaded only once the ticket exists, so create the ticket, upload, then set the description with the embed through REST `PUT /rest/api/3/issue/LAE-XXXXX`.
- **After a clone:** `copy_jira_issue` strips embedded media from a copied description. Download the file from the source ticket, upload it to the clone and use the clone's new media id (protocol steps 1-2); never reuse the source's id, Jira rejects it.
- **Gate:** the description keeps its own confirmation gate; the draft names each file to embed, and the upload waits for that yes.
- **Check:** UNVERIFIED for descriptions, so read the description's ADF back on first use.

Authoring-time only.

### LAE Investigation Comment Template

Use this template when posting investigation findings as a comment on an LAE ticket whose reporter is someone else; if the user is both reporter and assignee, use "Commenting on a Ticket You Reported and Own". Write for a business audience — no technical jargon, file paths, or stack traces.

**Rules:**
- Mention the reporter using ADF mention node at the top
- Describe root cause in plain business language
- Only suggest data fixes — never suggest code fixes (system code cannot be changed)
- Close with `Regards,` and first name only (`Dexter`)

```
Hi @[Reporter ADF mention],

[Investigation findings and resolution plan in plain business language — what was found, what will be done to fix it. Keep it conversational and clear. Reference specific AG/Contract IDs if known.]

Regards,
Dexter
```

### LAE Script Delivery Comment Template

Use when a comment hands a script or other file to the reporter on an LAE ticket whose reporter is someone else. The file is **embedded in the comment** (an ADF `mediaGroup` node), never only added to the ticket's attachment list. Upload and embed steps: `reference/ATTACHMENT-PROTOCOL.md` → "Upload and Embed in a Comment or Description".

**Rules:**
- Same shape as the Investigation template: reporter mention first, `Regards,` and `Dexter` last. Text the user dictates replaces the body sentence only; keep the greeting and closing unless the user says to drop them.
- Body is one plain sentence naming what the file is, e.g. `Please find attached the script for the Rent posting`.
- A comment that reports findings and also hands over a file: the Investigation body, then the embedded file, then the closing.
- The confirmation gate shows the full draft and the file name to embed; the upload and the post both wait for the explicit yes.
- Post with `mcp__jira__update_jira_issue(comment_adf=...)`. UNVERIFIED with a `mediaGroup` node: only the REST `PUT` on an existing comment has been run, so read the comment back on first use. To add the file to a comment already posted, edit that comment through REST; never post a second comment.
- After posting, `get_jira_issue` prints comments as text and omits embedded files, so read the comment's ADF back (protocol file) and confirm no duplicate attachment was added.

Authoring-time only.

```
Hi @[Reporter ADF mention],

Please find attached the script for [what it does].

[embedded file: mediaGroup node]

Regards,
Dexter
```

### Post-Action Field Corrections

Jira automation rules override certain fields after ticket creation and status transitions. **Always verify and fix these fields:**

#### Assignee: Development (`customfield_13004`)

- **Type:** User field
- **Required value:** Dexter Pagkaliwangan (`60396b7af032740068924835`)
- **When to check:** After every ticket **creation** AND every **status transition**
- **How to fix:** `update_jira_issue(issue_key="LAE-XXXXX", custom_fields={"customfield_13004": {"accountId": "60396b7af032740068924835"}})`

#### Assignee (main field)

- **Trigger:** Jira automatically reassigns after status transitions
- **How to fix:** `update_jira_issue(issue_key="LAE-XXXXX", assignee_id="60396b7af032740068924835")`

#### Mandatory Sequence

After every **create** or **status transition** on an LAE ticket:

1. Perform the action (create ticket or transition status)
2. Re-fetch the ticket: `get_jira_issue(issue_key="LAE-XXXXX")`
3. Check **Assignee** — if not Dexter, update it back
4. Check **Assignee: Development** (`customfield_13004`) — if not Dexter, update it back
5. Both fixes can be combined in a single update call

### Pre-Creation Validation

Before executing any create/clone operation, present ALL proposed fields in a table: Summary, Type, Priority, Assignee, Reporter, Fix Version, Affect Version. Then follow the global confirmation rules above (description is a separate confirmation gate).

### Cloning LAE Tickets (`copy_jira_issue`)

Three tool defaults are wrong and must be corrected on every clone:

- **Summary:** the tool prefixes `[Copy] ` when `summary` is omitted. Always pass `summary` explicitly — the source text verbatim, unless the user asks for different wording.
- **Reporter:** the tool does not forward the source reporter, so Jira defaults it to the calling credentials (Dexter). For a clone, the source ticket's reporter wins over the default in **Creating LAE Tickets**. Fix after creation:
  1. `get_jira_issue` returns display names only, never accountIds — fetch it via `GET /rest/api/3/issue/LAE-XXXXX?fields=reporter` (curl shape and credentials: **Updating LAE Tickets via REST API**) and read `.fields.reporter.accountId`. If the Bash permission classifier blocks the curl, ask the user to run it with `!` and paste back the accountId — never work around the block.
  2. `update_jira_issue(issue_key="LAE-NEW-KEY", reporter_id="<accountId>")`
- **Description media:** embedded files and screenshots are stripped from the copied description. Re-embed per **LAE Description Template** → "Attachments in a description".

Cloning counts as a create — run the **Mandatory Sequence** (above) afterward.

### Updating LAE Tickets via REST API

When `mcp__jira__update_jira_issue` cannot set a field (e.g., description with mentions, assignee not applying), use the Jira REST API directly:
```bash
source /c/workarea/jira_manager/.env
curl -s -X PUT "https://nakisa.atlassian.net/rest/api/3/issue/LAE-XXXXX" \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": { ... }}'
```

## LAE Custom Fields

- **Customer Commitment:** `customfield_13981` (array type, e.g., `[{"value": "Zoetis"}]`)
- **Resolution Path:** not offered on LAE (absent from the Reply and edit screens) — never draft or set it. `customfield_12000` exists on NCS only.
- Use `get_custom_fields` to look up other field IDs by name
- Fields auto-skipped when cloning (read-only/board-managed): Rank (`customfield_10007`, `customfield_10019`), Sprint (`customfield_10016`)

## Display Formats

### Search Results Display

When displaying results from `mcp__jira__search_jira_issues`, always use the **table format** below.

**Format:**

| # | Key | Status | Priority | Reporter | Summary | Fix Version | Affect Version | Created | Updated |
|---|-----|--------|----------|----------|---------|-------------|----------------|---------|---------|
| 1 | [LAE-44095](https://nakisa.atlassian.net/browse/LAE-44095) | L2Sup-Creating | Medium | Samee Rehman | Create a query to identify BP contracts ending in 2026 | UnPlanned | NLA 2022.R1.03 | 2026-02-24 | 2026-02-24 |

- Always format ticket keys as clickable links: `https://nakisa.atlassian.net/browse/TICKET-KEY`
- If a field is `N/A`, display it as `N/A`
- Customer Commitment is NOT included (requires extra per-ticket fetch) — only show it when using `get_jira_issue` on a single ticket

## Content Templates

See `~/.gemini/skills/jira/templates/CONTENT-TEMPLATES.md` — 5-Question Analysis Format and KB Article Format. Load this file when generating content (5Q analyses, KB articles, NCS resolution paths).
