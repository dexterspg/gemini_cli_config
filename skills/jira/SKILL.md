---
name: jira
description: >-
  Jira field mappings, JQL patterns, ticket workflows, and MCP tool
  conventions. Use before any Jira operation — creating, searching,
  updating, or closing tickets. Triggers on: "create a ticket",
  "search Jira", "close this ticket", "log time", "find tickets for
  [customer]", "JQL", "LAE ticket", "NCS ticket", "filter by customer",
  "check assignee", "verify version", "find this contract owner", or any
  mcp__jira__* tool usage.
---

# Jira Skill: Field Mappings & Conventions

> **HARD RULE:** ALL Jira operations MUST use `mcp__jira__*` tools ONLY. NEVER use `mcp__plugin_atlassian_atlassian__*` for any Jira operation — no exceptions, no fallbacks. Atlassian plugin = Confluence only.

**Operational Rules:**
- **NEVER write comments on NCS tickets** — all communication goes through linked LAE ticket (customer-facing only)
- **NEVER guess transition IDs or status names** — load `~/.gemini/skills/jira/workflows/LAE-WORKFLOW.md` before any status transition
- **NEVER skip Mandatory Sequence** — re-fetch and verify Assignee fields after every create/transition on LAE tickets

**Do NOT trigger for:**
- Confluence operations (e.g., writing pages, creating spaces) → Atlassian plugin (`mcp__plugin_atlassian_atlassian__*`), not this skill
- Content generation from ticket data → pass to `jira-content-creator` subagent
- Time tracking routing decisions → `agent-time-tracker`

## NCS → LAE Ticket Workflow

When the user has an NCS ticket in their time tracker and wants to create a corresponding LAE ticket, follow these steps **in order**, pausing for confirmation at each gate:

1. **Fetch** the NCS ticket via `mcp__jira__get_jira_issue`        
2. **Present** proposed LAE ticket fields (summary, type, priority, assignee, reporter, versions, customer, description) → **wait for user confirmation**
3. **Create** LAE ticket via `mcp__jira__create_jira_issue` with ADF description (ADF mention for Dexter)
4. **Fix** Assignee: Development (`customfield_13004`) immediately after creation
5. **Add comment** using the same wording as the last similar ticket (re-read from Jira, do not assume) → ADF mention for reporter  
6. **Present** Resolution Path draft (5-question format) + Root Cause → **wait for user confirmation**
7. **Close** via REST API transition 801 with Root Cause + Resolution Path
8. **Re-fetch** → verify and fix Assignee + Assignee: Development if overridden
9. **Log time** in Jira via `mcp__jira__log_work_on_issue` using the time from the tracker entry
10. **Update time tracker** → replace NCS ticket with new LAE ticket key + set `jira_logged: true`

**Rules:**
- "Yes proceed" at step 2 only triggers step 3 — NOT the full chain
- Always re-read the comment from the previous similar LAE ticket directly from Jira before reusing it — never rely on memory       
- Resolution Path confirmation (step 6) is a mandatory separate gate — never skip it

---

## Confirmation Before Write Operations

**MANDATORY** for ALL write operations (`create_jira_issue`, `update_jira_issue`, `copy_jira_issue`, `log_work_on_issue`):

1. Show the user a clear summary of the proposed changes
2. Wait for explicit confirmation before executing
3. Do NOT call the write tool until the user confirms

**MANDATORY — Content fields (description, resolution path, comment):**
- ALWAYS show the full draft to the user and wait for explicit confirmation before writing
- This applies to: ticket description, Resolution Path (`customfield_12000`), and any comment
- Each content field is a separate confirmation gate — never bundle them into one "yes"
- A prior "yes" to create the ticket does NOT cover description, resolution path, or comment

**Preview format:**
- **Creates:** show all fields that will be set
- **Updates:** show only the fields being changed
- **Copies:** show the source ticket and any overrides
- **Long text fields:** show a truncated preview

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
"Customer Commitment" = Fairprice AND assignee = "Lionel Malonga" AND status = Closed
```

### Search by Customer Only
```jql
"Customer Commitment" = Fairprice AND status = Closed
```

### Search by Assignee with Customer Filter
```jql
assignee = "Lionel Malonga" AND "Customer Commitment" = Fairprice  
```


## MCP Server Configuration

**Architecture:** MCP tools only work in the main session. Subagents (Task tool) have zero MCP access. All `mcp__jira__*` calls must be made by the main session directly. Jira subagents (content-creator, ticket-manager) receive pre-fetched data as input and return formatted output or prepared parameters.

**Available Tools:** `mcp__jira__search_jira_issues`, `mcp__jira__get_jira_issue`, `mcp__jira__create_jira_issue`, `mcp__jira__update_jira_issue`, `mcp__jira__copy_jira_issue`, `mcp__jira__get_custom_fields`, `mcp__jira__log_work_on_issue`, `mcp__jira__get_worklogs_by_date`, `mcp__jira__save_to_file`

### get_worklogs_by_date Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `start_date` | string | required | Start date `YYYY-MM-DD` |     
| `end_date` | string | required | End date `YYYY-MM-DD` |
| `assignee_names` | list | optional | Filter by person names (e.g. `["Dexter Pagkaliwangan"]`) |
| `projects` | list | optional | Projects to search (default: `["LAE", "NCS"]`) |
| `filter_by` | string | `"worklog"` | `"worklog"` — finds tickets where time was logged on those dates; `"updated"` — finds tickets updated on those dates that also have worklogs in the range |   

**Use `filter_by="worklog"` (default) when:** checking who logged time, time tracking reports, verifying Jira worklogs
**Use `filter_by="updated"` when:** checking tickets updated AND worked on in a date range

For server setup, credentials, and troubleshooting see `~/.gemini/skills/jira/reference/MCP-CONFIG.md`.


## Downloading Attachments

**This is the canonical attachment-download protocol.** The main session, agent-debugger, and agent-support-investigator all reference this section — do not duplicate elsewhere.

### Preferred: `mcp__jira__download_jira_attachments`

The Jira MCP server exposes `download_jira_attachments(issue_key, output_dir, filename_filter="")`. It centralizes auth, follows the S3 redirect, verifies each file (size > 0 and not an HTML error page), and returns a per-file OK/FAIL/SKIP summary. Use this in almost all cases.

```
mcp__jira__download_jira_attachments(
    issue_key="LAE-44173",
    output_dir=r"C:\Users\dexte\git0\issues\LAE-44173-batch-posting-450-contracts\attachments",
    filename_filter="logs"   # optional: case-insensitive substring match on filename
)
```

If the MCP tool is unavailable, load `~/.gemini/skills/jira/reference/ATTACHMENT-PROTOCOL.md` for the REST API fallback and failure categorization.

---

## Known Issues & Workarounds

- Field name "customer" does not exist in this Jira instance; always use `"Customer Commitment"` instead
- Customer values may be inconsistently spelled in descriptions (e.g., "Fairprice" vs "Fair Price") — use the exact field value     
- Customer names from the company skill's reference data may not reflect exact Jira spelling — when unsure, probe a known ticket and read the `Customer Commitment` field value directly
- For the current user's own tickets, always use `assignee = currentUser()` — more reliable than hardcoding a username

## User Lookup Procedure

When you need a Jira username and only have a partial name:        
1. Look up full display name via company skill (`~/.gemini/skills/company/SKILL.md`)
2. Probe: `text ~ "Full Display Name"` to find any ticket
3. Read the `assignee` field from results → use that exact username in JQL


## LAE Workflow Map

**MANDATORY:** Before performing any status transition, comment, or ticket closure on an LAE ticket, you MUST load `~/.gemini/skills/jira/workflows/LAE-WORKFLOW.md`. Do NOT guess transition IDs, status names, Root Cause IDs, or closure fields — all are defined in that file. Proceeding without loading it is a workflow error.        

---

## LAE Ticket Conventions

### Creating LAE Tickets

When creating or cloning LAE tickets:

- **Type:** Always default to **Support Request** unless explicitly told otherwise
- **Assignee:** Always default to **Dexter Pagkaliwangan** (`accountId: 60396b7af032740068924835`) unless explicitly told otherwise   
- **Reporter:** Use the **assignee of the linked NCS ticket** (not the reporter), unless explicitly told otherwise. If no linked NCS ticket exists, fall back to the company skill (`~/.gemini/skills/company/SKILL.md`) to look up the customer's Lead Support Sponsor as reporter
- **Fix/Affect Versions:** If the source or linked NCS ticket has no versions, find the latest BP (or relevant customer) ticket in NCS or LAE with those fields populated and copy from there
- **Affect Version (if name rejected):** Look up the version ID via REST API (`/rest/api/3/project/LAE/versions`) and pass it via `custom_fields` as `{"versions": [{"id": "VERSION_ID"}]}`
- **Mentions in description:** Always use Jira's built-in ADF mention node — never plain text `@Name`. Since `mcp__jira__create_jira_issue` does not support ADF natively, always set the description via REST API (`PUT /rest/api/3/issue/LAE-XXXXX`) after creation     

### LAE Description Template

The description is written **from the reporter's perspective, addressed to the assignee (Dexter)**. Default tone is **before investigation** — describe only what is visible in the UI or reported by the client. Do not include root cause, stack traces, or investigation findings unless explicitly asked.

Write as natural flowing paragraphs. **No section labels** (never use `[CONTEXT]`, `[REQUEST]`, `[ENVIRONMENT / SCOPE]` or any bracketed headers).

```
Hi @[Assignee ADF mention],

[Background: reference the linked NCS ticket, the customer, and what the client reported.]

[Request: what is being asked — investigate, write a script, write a SQL query, fix, etc. — with any specific conditions or criteria. When scripts are involved, Dexter **provides** the scripts; the reporter/customer **applies** them. Never say Dexter applies scripts.]

Thank you
```

### LAE Investigation Comment Template

Use this template when posting investigation findings as a comment on an LAE ticket. Write for a business audience — no technical jargon, file paths, or stack traces.

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

**This is mandatory. Do NOT skip steps 2-4.**

### Pre-Creation Validation

Before executing any create/clone operation, present ALL proposed fields in a table: Summary, Type, Priority, Assignee, Reporter, Fix Version, Affect Version. Then follow the global confirmation rules above (description is a separate confirmation gate).

### Updating LAE Tickets via REST API

When `mcp__jira__update_jira_issue` cannot set a field (e.g., description with mentions, assignee not applying), use the Jira REST API directly:
```bash
curl -s -X PUT "https://nakisa.atlassian.net/rest/api/3/issue/LAE-XXXXX" \
  -u "dexter.pagkaliwangan@nakisa.com:{token}" \
  -H "Content-Type: application/json" \
  -d '{"fields": { ... }}'
```
Credentials are in `/c/workarea/jira_manager/.env`.

## LAE Custom Fields

- **Customer Commitment:** `customfield_13981` (array type, e.g., `[{"value": "Zoetis"}]`)
- **Resolution Path:** `customfield_12000` (rich text, use the 5-question format below)
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

See `~/.gemini/skills/jira/templates/CONTENT-TEMPLATES.md` — 5-Question Analysis Format and KB Article Format. Load this file when generating content (5Q analyses, KB articles, resolution paths).    

## Sub-Skills

| Sub-Skill | Path | Purpose |
|-----------|------|---------|
| CSR (Cloud Services) | [`csr/SKILL.md`](csr/SKILL.md) | Create CSR tickets with correct required fields, custom field IDs, and valid option values |

## Related Agents

This skill is used by:
- **Main session** — ALL MCP calls (search, get, create, update, copy, log work). The only place MCP tools work.
- **jira-content-creator** (subagent) — Receives pre-fetched ticket data, produces formatted content (5Q analyses, KB articles, release notes). No MCP access.
