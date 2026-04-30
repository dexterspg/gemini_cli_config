---
skill: csr
description: Create Cloud Services (CSR) tickets with correct required fields and valid option values
args: ""
user-invocable: false
---

# CSR Ticket Creation Skill

**Parent skill:** [`~/.claude/skills/jira/SKILL.md`](../SKILL.md)

## CSR Project Overview

- **Project Key:** CSR
- **Project Name:** Cloud Services
- **Purpose:** Requests to the Cloud Services / infrastructure team (access requests, deployments, environment changes, SSO config, etc.)

## Available Issue Types

| Issue Type | Jira ID |
|-----------|---------|
| Alerts | 11840 |
| API Key | 11899 |
| Clone Build | 11802 |
| Cloud Issues | 11906 |
| Customer Block/Termination | 11900 |
| Data Wipeout | 11901 |
| Deployment | 11544 |
| Environment Restore | 11902 |
| NCC Installation | 11903 |
| Resource Change | 11833 |
| Role Mapping Update | 11904 |
| SSO Configuration | 11905 |
| Upgrade | 11545 |
| User Access | 11879 |
| Other inquiries/issues not listed | 11909 |

## Required Custom Fields

| Field | Custom Field ID | Type | Valid Values / Default |
|-------|----------------|------|----------------------|
| Customer | `customfield_10900` | array of strings | e.g., `["BP"]` — NOT option objects |
| Customer Approval | `customfield_13268` | option | **Always `{"value": "Yes"}`** (auto-default) |
| Customer Environment | `customfield_13285` | option | `{"value": "Production"}`, `{"value": "QA"}`, etc. |
| Solution | `customfield_13194` | option | `{"value": "Nakisa Lease Administration"}` |
| Type of Access | `customfield_13274` | option | **Default: `{"value": "Other - See description"}`**, `{"value": "Server"}`, `{"value": "Application"}`, `{"value": "SQL-PAD"}` |
| Issue Priority | `customfield_13326` | option | `{"value": "Medium"}`, `{"value": "High"}`, etc. |
| Environment Link | `customfield_13170` | string | URL string, e.g., `"https://bp.nakisa.cloud/leasing/prod/app/default.html"` |
| Project Start Date | `customfield_12500` | date | **Always today's date** `"YYYY-MM-DD"` (auto-default) |
| End Date | `customfield_13249` | date | **Always 2 weeks from today** `"YYYY-MM-DD"` (auto-default) |

### Auto-Defaults (set without asking the user)

- **Customer Approval** = `{"value": "Yes"}`
- **Type of Access** = `{"value": "Other - See description"}`
- **Project Start Date** = today (`YYYY-MM-DD`)
- **End Date** = today + 14 days (`YYYY-MM-DD`)

## Summary (Title) Templates

### Variant A — Access + SQL pad + Remote Debugging

```
Enable Access, SQL pad and Remote Debugging for {CUSTOMER} {ENV} Environment
```

### Variant B — Access + SQL pad only (no debugging)

```
Enable Access and SQL pad (READ) for {CUSTOMER} {ENV} Environment
```

Variables: `{CUSTOMER}` = customer name (BP, Stada, Danone, Bunge, etc.), `{ENV}` = Prod/QA/Pre-Prod

## Description Templates

### Variant A — With Remote Debugging

```
Hello @Jalil Elkarfi @Umer Shafqat @Haseeb Ashfaq

Please enable remote debugging and provide all access (manager, default, admin) to {ENV} to the following developer/consultants: 

@{DEVELOPER_NAME}

Environment url: {ENVIRONMENT_URL}

Also provide SQL pad access (READ only)
```

### Variant B — Without Remote Debugging

```
Hello @Jalil Elkarfi @Umer Shafqat @Haseeb Ashfaq

Please provide all access (manager, default, admin) to {ENV} to the following developer/consultants:

@{DEVELOPER_NAME}

Environment url: {ENVIRONMENT_URL}

Also provide SQL pad access (READ only)
```

### Description Rules

- The Hello line **ALWAYS** includes all 3 cloud team members: Jalil Elkarfi, Umer Shafqat, Haseeb Ashfaq
- The "Also provide SQL pad access (READ only)" line is **always** present
- Default developer: **Dexter Pagkaliwangan** (unless specified otherwise)
- Environment URL pattern: `https://{customer}.nakisa.cloud/leasing/{env}/app/default.html`

## MCP Tool Call Template

```python
mcp__jira__create_jira_issue(
    project_key="CSR",
    summary="{TITLE}",
    issue_type="User Access",  # Most common; change as needed
    description="{DESCRIPTION}",
    priority="Medium",
    custom_fields={
        "customfield_10900": ["{CUSTOMER}"],           # Customer (array of strings)
        "customfield_13268": {"value": "Yes"},          # Customer Approval (auto)
        "customfield_13285": {"value": "{ENV}"},        # Customer Environment
        "customfield_13194": {"value": "Nakisa Lease Administration"},  # Solution
        "customfield_13274": {"value": "Other - See description"},  # Type of Access (auto)
        "customfield_13326": {"value": "Medium"},       # Issue Priority
        "customfield_13170": "{ENVIRONMENT_URL}",       # Environment Link
        "customfield_12500": "{TODAY_YYYY-MM-DD}",      # Project Start Date (auto)
        "customfield_13249": "{TODAY+14_YYYY-MM-DD}"    # End Date (auto)
    }
)
```

## Cloud Team Members

These people are commonly tagged in descriptions and assigned to CSR tickets:

- **Jalil Elkarfi**
- **Umer Shafqat**
- **Haseeb Ashfaq**

## Conventions & Tips

- **Priority:** Use Medium unless linked to a High/Critical ticket
- **Customer field format:** Array of strings `["BP"]` — NOT option objects like `[{"value": "BP"}]`
- **Access expiry:** Tickets expire periodically (~2-3 weeks), so new tickets are needed for continued access
- **Environment URL:** Always include in BOTH the description AND the Environment Link custom field (`customfield_13170`)        
- **URL pattern:** `https://{customer}.nakisa.cloud/leasing/{env}/app/default.html`
- **Issue type for access requests:** Use `User Access` (ID: 11879)
