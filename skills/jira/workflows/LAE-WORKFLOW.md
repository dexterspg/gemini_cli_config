# LAE Ticket Workflows

> Workflows differ by ticket type. Always check the ticket type before transitioning.

---

## Support Request Tickets

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
- Use the LAE Investigation Comment Template (see SKILL.md)        

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
- **Resolution Path** (`customfield_12000`) — ADF format, 5-question content (see `~/.gemini/skills/jira/templates/CONTENT-TEMPLATES.md`). Writing rules: business-user friendly, concise, no technical jargon, plain language only
- **KB Article** (`customfield_13264`) — leave empty (not required)

**Closure sequence:**
1. POST transition 801 with Root Cause + Resolution Path in the same call (via REST API)
2. Follow Mandatory Sequence in SKILL.md to re-fetch and fix assignee fields

**REST API call:**
```bash
curl -s -X POST "https://nakisa.atlassian.net/rest/api/3/issue/LAE-XXXXX/transitions" \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"transition": {"id": "801"}, "fields": {"customfield_12301": {"id": "11886"}, "customfield_12000": { ...ADF... }}}'
```

---

## Merge Request Tickets (PS-type)

Merge Request tickets are created for upgrade conflict resolution. To close them, you must walk through the full transition chain — there is no direct "Close" shortcut.

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
