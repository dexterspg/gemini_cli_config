# Jira Skill: Field Mappings & Conventions

> **HARD RULE:** ALL Jira operations MUST use `mcp__jira__*` tools ONLY. NEVER use `mcp__plugin_atlassian_atlassian__*` for any Jira operation — no exceptions, no fallbacks. Atlassian plugin = Confluence only.

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
10. **Update time tracker** — replace NCS ticket with new LAE ticket key + set `jira_logged: true`

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

The Jira MCP server is a local Python server at `/c/workarea/jira_manager/`.

### How it's registered
MCP servers must be in `~/.claude.json` under `mcpServers` (NOT `~/.claude/settings.json` — that key is ignored for MCP loading):

```json
// ~/.claude.json
{
  "mcpServers": {
    "jira": {
      "command": "python",
      "args": ["C:/workarea/jira_manager/src/jira_mcp_server.py"],
      "cwd": "C:/workarea/jira_manager"
    }
  }
}
```

### Credentials
Loaded automatically from `/c/workarea/jira_manager/.env` (path is hardcoded relative to the script, so `cwd` doesn't affect it).

### Architecture Constraint

**MCP tools only work in the main session.** Subagents (Task tool) have zero MCP access. All `mcp__jira__*` calls must be made by the main session directly. Jira subagents (content-creator, ticket-manager) receive pre-fetched data as input and return formatted output or prepared parameters.

### Troubleshooting
- **Tools not available in a session:** MCP server failed to connect at startup. Restart Claude Code — the server will re-attempt.
- **Works from `~/.claude/` but not other dirs:** Previously the config was only in `~/.claude/settings.json` (wrong) and `~/.claude/mcp.json` (project-local). Fixed by moving to `~/.claude.json`.

### Available Tools (main session only)
`mcp__jira__search_jira_issues`, `mcp__jira__get_jira_issue`, `mcp__jira__create_jira_issue`, `mcp__jira__update_jira_issue`, `mcp__jira__copy_jira_issue`, `mcp__jira__get_custom_fields`, `mcp__jira__log_work_on_issue`, `mcp__jira__get_worklogs_by_date`, `mcp__jira__save_to_file`

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


## Downloading Attachments

**This is the canonical attachment-download protocol.** The main session, agent-debugger, and agent-support-investigator all reference this section — do not duplicate elsewhere.

### Preferred: `mcp__jira__download_jira_attachments`

The Jira MCP server exposes `download_jira_attachments(issue_key, output_dir, filename_filter="")`. It centralizes auth, follows the S3 redirect, verifies each file (size > 0 and not an HTML error page), and returns a per-file OK/FAIL/SKIP summary. Use this in almost all cases.

```
mcp__jira__download_jira_attachments(
    issue_key="LAE-44173",
    output_dir=r"C:\Users\dpagkaliwangan\git0\issues\LAE-44173-batch-posting-450-contracts\attachments",
    filename_filter="logs"   # optional: case-insensitive substring match on filename
)
```

If the MCP tool is unavailable (server not running, or working outside Claude Code), fall back to the REST API recipe below.     

### Fallback: REST API (when MCP unavailable)

API **v3** is required (v2 returns 403 on this tenant as of 2026-04 — re-verify if Atlassian deprecates v3). `-L` follows the redirect from the API to S3.

```bash
source /c/workarea/jira_manager/.env

# List attachment IDs
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "https://nakisa.atlassian.net/rest/api/3/issue/{TICKET_KEY}?fields=attachment" \
  | python -c "import json,sys; [print(a['id'], a['filename']) for a in json.load(sys.stdin)['fields']['attachment']]"

# Download by ID
curl -s -L -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "https://nakisa.atlassian.net/rest/api/3/attachment/content/{ATTACHMENT_ID}" \
  -o "attachments/{FILENAME}"

# Verify (HTML-as-zip is the silent failure to catch; file -b alone is not enough)
verify_attachment() {
  local f="$1"
  [ -s "$f" ] || { echo "FAIL: $f is empty"; return 1; }
  if head -c 200 "$f" 2>/dev/null | grep -qiE '<!doctype html|<html|<head'; then
    echo "FAIL: $f is HTML (auth/error page saved as expected file)"; return 1
  fi
  echo "OK: $f"
}
verify_attachment "attachments/{FILENAME}" || exit 1
```

### Failure categorization (do not blindly retry)

| Symptom | Cause | Action |
|---|---|---|
| File is HTML (`<!DOCTYPE html>`) | Auth not loaded — `.env` not sourced or vars empty | Re-source `.env`, verify `$JIRA_EMAIL` and `$JIRA_API_TOKEN` are set, retry once |
| HTTP 401/403 returned | Token expired or wrong scope | Surface the response to the user; do NOT retry — token rotation is required |
| HTTP 429 | Rate limited | Wait 30s, retry once |
| HTTP 5xx | Atlassian transient | Retry with 5s backoff, max 2 attempts |
| Network error / timeout | Connectivity | Retry once; if still failing, ask user to drop files manually |
| File is 0 bytes after success exit | Likely missing `-L` (followed redirect not honored) | Re-run with `-L` flag |

If recovery fails after the action above, **stop and surface the failure** — do not guess root cause from missing evidence.    

---

## Known Issues & Workarounds

- ⚠️ Field name "customer" does not exist in this Jira instance; always use `"Customer Commitment"` instead
- Values like "Fairprice", "Fair Price", "FairPrice" may be used inconsistently in descriptions; use the field value directly    
- ⚠️ `"Customer Commitment" ~ "value"` (contains) does NOT work — always use `"Customer Commitment" = "value"` (exact match)
- ⚠️ **User field fuzzy search (`~`) does NOT work** — `assignee ~ "Zark"` returns nothing. Always use exact username format: `assignee = "zark.ahmed"` (lowercase, dot-separated). To find a user's username: (1) use the company skill (`~/.claude/skills/company/SKILL.md`) to look up their full display name, (2) use `text ~ "Full Name"` to find a probe ticket, (3) confirm the display name from results. Note: `reporter = "Display Name"` does NOT work — only exact account usernames resolve in JQL
- ✅ **For the current user's own tickets**, always use `assignee = currentUser()` — more reliable than hardcoding a username 
- ⚠️ Customer names from the company skill's reference data may not reflect the exact spelling or casing stored in Jira. When unsure of the exact value, probe with a known ticket: fetch a ticket you know belongs to that customer and read the `Customer Commitment` field value directly from the result — then use that exact string in JQL


## LAE Workflow Map

> Workflows differ by ticket type. Always check the ticket type before transitioning.

### Status Quick Reference

| Status | Meaning |
|--------|---------|
| **L2Sup-NeedInfo** | Waiting on reporter/customer feedback |
| **Dev-Pending** | Actively being worked on (in development) |
| **Replied** | Ticket is closed — solution provided and verified |


### Support Request Tickets

**Full transition map (from each status):**

| From Status | Transition | ID | To Status |
|---|---|---|---|
| L2Sup-Creating | Request Support | 921 | L2Sup-NeedInfo |
| L2Sup-Creating | Request Development | 781 | Dev-Pending |
| L2Sup-Creating | Request PS | 911 | PS-Actioned |
| L2Sup-Creating | On Hold | 511 | On Hold |
| L2Sup-Creating | Reply | 801 | Replied (CLOSED) |
| L2Sup-Creating | Reject | 811 | Rejected |
| L2Sup-NeedInfo | Request Development | 931 | Dev-Pending |
| L2Sup-NeedInfo | Request Product | 941 | Prod-Pending |
| L2Sup-NeedInfo | Request SEN | 961 | COE/SEN-Pending |
| L2Sup-NeedInfo | Request PS | 911 | PS-Actioned |
| L2Sup-NeedInfo | Request Support | 921 | L2Sup-NeedInfo |
| L2Sup-NeedInfo | On Hold | 511 | On Hold |
| L2Sup-NeedInfo | Reply | 801 | Replied (CLOSED) |
| L2Sup-NeedInfo | Reject | 811 | Rejected |
| Dev-Pending | Start Development | 101 | Dev-Developing |
| Dev-Pending | Request Development | 931 | Dev-Pending |
| Dev-Pending | Request Product | 941 | Prod-Pending |
| Dev-Pending | Request SEN | 961 | COE/SEN-Pending |
| Dev-Pending | Request PS | 911 | PS-Actioned |
| Dev-Pending | Request Support | 921 | L2Sup-NeedInfo |
| Dev-Pending | On Hold | 511 | On Hold |
| Dev-Pending | Reply | 801 | Replied (CLOSED) |
| Dev-Pending | Reject | 811 | Rejected |
| On Hold | Request Development | 931 | Dev-Pending |
| On Hold | Request Product | 941 | Prod-Pending |
| On Hold | Request SEN | 961 | COE/SEN-Pending |
| On Hold | Request PS | 911 | PS-Actioned |
| On Hold | Request Support | 921 | L2Sup-NeedInfo |
| On Hold | Reply | 801 | Replied (CLOSED) |
| On Hold | Reject | 811 | Rejected |

> Note: Transitions from Dev-Developing, Prod-Pending, COE/SEN-Pending, PS-Actioned not yet mapped — no tickets currently in those statuses.

**Comment + Status Convention (when NOT closing):**

When adding a comment addressed to the reporter (using ADF mention) from Dev-Pending:
- If asking for more info or waiting on the reporter → transition to **L2Sup-NeedInfo** (ID: 921)
- If providing an update but no response needed yet → stay in **Dev-Pending**
- Always use ADF mention node for the reporter — never plain text `@Name`
- Use the LAE Investigation Comment Template (see above)

**Closure (Reply transition) — required fields:**
- **Root Cause** (`customfield_12301`) — default `{"id": "11886"}` (Platform / Environment) unless told otherwise

  | ID | Value |
  |---|---|
  | 10810 | Product Bug |
  | 16070 | Product API |
  | 10806 | Product Configuration |
  | 16071 | Missing Functionality / Perceived Bug or Gap |
  | 10809 | Product New Scope Request |
  | 11906 | Managed Services / Data / Pipelines |
  | 11886 | Platform / Environment *(default)* |
  | 16069 | Duplicate |
  | 13347 | User Error / Knowledge / Training / FAD |
  | 11394 | Not Reproducible |
- **Resolution Path** (`customfield_12000`) — ADF format, 5-question content (see "5-Question Analysis Format" below). Writing rules: business-user friendly, concise, no technical jargon, plain language only
- **KB Article** (`customfield_13264`) — leave empty (not required)

**Closure sequence:**
1. POST transition 801 with Root Cause + Resolution Path in the same call (via REST API)
2. Follow Mandatory Sequence below to re-fetch and fix assignee fields

**REST API call:**
```bash
curl -s -X POST "https://nakisa.atlassian.net/rest/api/3/issue/LAE-XXXXX/transitions" \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"transition": {"id": "801"}, "fields": {"customfield_12301": {"id": "11886"}, "customfield_12000": { ...ADF... }}}'       
```

---

## Merge Request Ticket Workflow

Merge Request tickets (PS-type) are created for upgrade conflict resolution. To close them, you must walk through the full transition chain — there is no direct "Close" shortcut.

**Full workflow to close:**
PS-Creating → Request Development → Start Development → Merge Completed → Passed/Validated

**Transition IDs:**
| Transition | ID |
|---|---|
| Request Development | 81 |
| Start Development | 11 |
| Merge Completed | 21 |
| Passed/Validated | 31 |

**No Resolution Path or Root Cause required** — PS tickets do not require these fields during any transition.

**After every transition, always verify and fix:**
- **Assignee** → must be Dexter Pagkaliwangan (`60396b7af032740068924835`)
- **Assignee: Development** (`customfield_13004`) → must be Dexter Pagkaliwangan (`60396b7af032740068924835`)

Both can be fixed in a single `update_jira_issue` call after the final transition.

---

## NCS Ticket Rules

- **NEVER write comments on NCS tickets** — Dexter is not allowed to comment on customer-facing NCS tickets. All communication goes through the linked LAE ticket.

## LAE Ticket Conventions

### Creating LAE Tickets

When creating or cloning LAE tickets:

- **Type:** Always default to **Support Request** unless explicitly told otherwise
- **Assignee:** Always default to **Dexter Pagkaliwangan** (`accountId: 60396b7af032740068924835`) unless explicitly told otherwise
- **Reporter:** Use the **assignee of the linked NCS ticket** (not the reporter), unless explicitly told otherwise. If no linked NCS ticket exists, fall back to the company skill (`~/.claude/skills/company/SKILL.md`) to look up the customer's Lead Support Sponsor as reporter
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

### 5-Question Analysis Format

Every ticket analysis and Resolution Path field (`customfield_12000`) **MUST** use exactly these 5 questions. Do NOT rephrase, reorder, or substitute.

**1. What was the issue and its impact?**
- Problem Definition: what the client was unable to do
- Specific error or symptom reported
- Business impact (halted processes, compliance risks, financial reporting delays)
- Priority classification
- Affected Users/Processes:
  - Entities affected (company codes, environments, modules)
  - System version affected
  - Technical context (currencies, configurations, etc.)

**2. What caused the issue?**
- Root Cause stated clearly
- Technical Explanation:
  - What configuration or setting was incorrect/missing
  - How the system behaved as a result (API calls, data flow issues)
  - Preceding events that triggered the issue (upgrades, migrations)
  - Technical chain of causation

**3. What troubleshooting steps should be taken?**
- Step-by-Step Diagnostic Process:
  - Verification steps (connectivity, permissions)
  - Logging configurations to enable
  - Log files and traces to review
  - Configuration areas to validate
  - Environment comparison steps
  - Post-upgrade verification checks

**4. What resolution or workaround was applied?**
- Resolution stated clearly
- Implementation Steps:
  - Navigation path in the application
  - Specific settings to configure
  - Values to add or modify
  - Verification steps after changes

**5. How can this be prevented in the future?**
- Pre-Upgrade Validation Checklist items
- Post-Upgrade Testing Protocols
- Environment gaps (e.g., missing QA environment)
- Configuration review processes

**Writing guidelines:** Be detailed and technical — incorporate all relevant information from the ticket's description, resolution path, comments, and attached files. Expand on brief entries with appropriate technical detail relevant to the product domain (SAP integration, lease accounting, asset management).

**"Not applicable" rule:** Write all answers from the perspective of application support. If a question (especially #5) asks for something outside application support's control (e.g., preventing a system-level data gap), answer with "Not applicable" and a brief explanation of why, plus a reapplication note if a script or workaround exists for recurrence. Never force an answer that implies support can prevent something they cannot.

### KB Article Format

Generate a structured Knowledge Base article based on support case details. Rules:
- Do not include specific names of individuals or customers
- Do not add visual elements, dividers, excess spacing, or new sections
- Maintain consistent formatting throughout
- Keep the article concise and scannable

**Required sections in this exact order:**
- **Title:** Brief, descriptive title of the issue
- **Issue Overview:** Issue description, error messages, impact on user or system
- **Cause of the Issue:** Root cause. If unclear or not provided, state that concisely
- **Troubleshooting Steps Taken:** Numbered list of steps that directly helped identify or resolve the issue. Exclude unproductive actions. Keep each step concise
- **Resolution & Fix:** Fix or workaround applied, follow-up actions taken
- **Prevention & Best Practices:** Recommendations if applicable. If not applicable, state "Not applicable."

## Sub-Skills

| Sub-Skill | Path | Purpose |
|-----------|------|---------|
| CSR (Cloud Services) | [`csr/SKILL.md`](csr/SKILL.md) | Create CSR tickets with correct required fields, custom field IDs, and valid option values |

## Related Agents

This skill is used by:
- **Main session** — ALL MCP calls (search, get, create, update, copy, log work). The only place MCP tools work.
- **jira-content-creator** (subagent) — Receives pre-fetched ticket data, produces formatted content (5Q analyses, KB articles, release notes). No MCP access.
