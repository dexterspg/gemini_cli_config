# Jira & Data Analysis Skills

This document defines the consolidated Jira operations and data analysis standards for this workspace.

## Core Mandate: MCP Tools Only
**HARD RULE:** ALL Jira operations MUST use `mcp__jira__*` tools (or the local logic in `src/jira_mcp_server.py`). NEVER use any other Jira/Atlassian plugins.

## Jira MCP Configuration
The Jira MCP server is configured at the workspace root and is accessible from any folder.
- **Server Path (Original):** `C:/workarea/jira_manager/src/jira_mcp_server.py`
- **Server Path (Gemini Optimized):** `C:/workarea/jira_manager/src/jira_mcp_gemini.py`
- **Configuration File:** `C:/workarea/.gemini/settings.json`

---

## 1. Jira Operational Skills

### CSR Ticket Creation Skill
When creating Cloud Services (CSR) tickets, use these specific requirements:
- **Project Key:** CSR
- **Customer field (`customfield_10900`):** Array of strings, e.g., `["BP"]`.
- **Customer Approval (`customfield_13268`):** Always `{"value": "Yes"}`.
- **Environment Link (`customfield_13170`):** URL string.
- **Title Pattern:** `Enable Access, SQL pad and Remote Debugging for {CUSTOMER} {ENV} Environment`
- **Description Hello Line:** Always includes Jalil Elkarfi, Umer Shafqat, Haseeb Ashfaq.
- **Auto-Defaults:** Customer Approval (Yes), Type of Access (Other), Start Date (Today), End Date (Today + 14 days).

### NCS → LAE Ticket Workflow
1. **Fetch** the NCS ticket.
2. **Present** proposed LAE ticket fields → **wait for user confirmation**.
3. **Create** LAE ticket (with ADF description).
4. **Fix** Assignee: Development (`customfield_13004`) to Dexter Pagkaliwangan (`60396b7af032740068924835`).
5. **Add comment** (reuse wording from similar tickets) → ADF mention for reporter.
6. **Present** Resolution Path draft (5-question format) → **wait for user confirmation**.
7. **Close** via transition 801 with Root Cause + Resolution Path.
8. **Log time** using `log_work_on_issue`.

### 5-Question Analysis Format
Every ticket analysis and Resolution Path field (`customfield_12000`) **MUST** use exactly these 5 questions:
1. **What was the issue and its impact?**
2. **What caused the issue?**
3. **What troubleshooting steps should be taken?**
4. **What resolution or workaround was applied?**
5. **How can this be prevented in the future?**

### Write Confirmation Protocol
**MANDATORY** for ALL write operations:
- Show a summary of proposed changes.
- Wait for explicit confirmation.
- Each content field (description, resolution path, comment) is a separate confirmation gate.

### LAE Ticket Conventions
- **Type:** Default to **Support Request**.
- **Assignee:** Default to **Dexter Pagkaliwangan** (`60396b7af032740068924835`).
- **Post-Action Corrections:** After every creation or transition, re-fetch and ensure **Assignee** and **Assignee: Development** (`customfield_13004`) are set to Dexter.

### 2. Universal Migration & Parity Standards

#### Verbatim Copying & Compatibility Protocol
- When asked to copy a skill or agent from another system (e.g., Claude), the copy must be **verbatim, word-for-word, and line-for-line**.
- If any part of the source is suspected to be incompatible with the current environment (e.g., tool mismatches, missing dependencies):
  - Do **NOT** silently modify the content during the copy.
  - Identify and **flag the exact word and line differences** to the user for review.
  - Review compatibility **section by section** before proceeding.
  - If a dependency (like a skill or agent) is missing, propose creating a Gemini-suitable equivalent rather than omitting the instruction.

---

## 3. Data Analysis & Cleaning Skills

### Understand Before Analyzing
- Identify the **business question** behind every request.
- Confirm the target audience to calibrate output depth.

### Data Cleaning Methodology
1. **Profile:** Count rows/cols, check completeness, detect duplicates and inconsistencies.
2. **Clean:** Document every transformation. Never silently drop data. Standardize dates to ISO 8601.
3. **Validate:** Cross-check counts and aggregations against source totals.

### Jira-Specific Analysis
- **Efficient Querying:** Use JQL to filter precisely.
- **Key Metrics:** Resolution time (created→resolved), backlog health (age distribution), workflow bottlenecks, SLA compliance.
- **Normalization:** Handle status transitions (e.g., 'Replied' = resolved), normalize custom field values.

### Business-Analyst-Ready Output
- **Executive Summary:** 2-3 sentences on findings and recommended action.
- **Key Metrics:** Tables or bullets with comparisons and trends.
- **Detailed Findings:** Organized by business question (Observation, Data, Implication).
- **Format:** Use **markdown tables** for structured data and clickable ticket links: `[KEY](https://nakisa.atlassian.net/browse/KEY)`.

---

## 3. Technical Reference

### Custom Field Mapping
- **customer:** `"Customer Commitment"` (use exact match `=` not `~`).
- **Assignee: Development:** `customfield_13004`
- **Resolution Path:** `customfield_12000`

### Common JQL Patterns
- `"Customer Commitment" = Fairprice AND assignee = "Lionel Malonga" AND status = Closed`
