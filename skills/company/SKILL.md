---
name: company
description: >-
  Customer & support sponsor lookup, NCP DB dump / SFTP access instructions, and the
  docs.nakisa.com index. Triggers on: "find the support sponsor for", "which region is",
  "customer success manager", "look up the support team for [customer]", "weekly support
  report", "how do I get a db dump", "access the sftp/ftp server", "db dump for [customer] env",
  "Nakisa docs", "official documentation for [product]", "user guide for [product]",
  "where are the release notes for [product]". Not for endpoint fields (api-reference, hurl-conventions).
---

# Company Skill: Customer & Support Sponsor Lookup

**Dependencies:** the weekly report reads `~/.gemini/skills/jira/reference/SUPPORT-TEAM.md` (team JQL names). File absent → stop and ask.

## Purpose

Quick lookup of Nakisa customer accounts, their assigned support sponsors, and account metadata. Use this when you need to:
- Find the **Lead/Backup Support Sponsor** for a customer (e.g., to set as reporter on LAE tickets)
- Identify which **region** or **line of business** a customer belongs to
- Look up the **Customer Success Manager** or **Executive Sponsor**

## Data Source

**Reference file:** `C:/workarea/references/customers-and-support-sponsors.md`
**Original source:** `C:/workarea/Customers_and_Support_Sponsors.xlsx`

The reference file contains 120 Nakisa customers. Fields:

| Field | Description |
|-------|-------------|
| Customer Name | Account name as used in Jira ("Customer Commitment" field) |
| Account Region | North America, EMEA, LATAM, APJ |
| Account Area | Country/state within the region |
| Line of Business | Financial Suite, HR Suite, Real Estate, Cross-line customer |
| Platform | Cloud or On Premise |
| Lead Support Sponsor | Primary support contact — default reporter on LAE tickets |
| Backup Support Sponsor | Secondary support contact |
| Customer Success Manager | CSM for the account |
| Nakisa Executive Sponsor | Executive sponsor (may be blank) |
| HR-PM & SE Sponsor | HR/PM sponsor (may be blank) |
| NCP Version | NCP platform version (informational) |
| PROD Version | Production release version (informational) |
| PROD Patch | Production patch level (informational) |
| Integration | SAP integration type (informational) |
| Account Time Zone | Customer's local time zone (informational) |

## Triggers

This skill loads when you ask to:
- Find a Lead/Backup support sponsor (for reporter fallback)
- Identify customer region, line of business, or account metadata
- Look up customer success manager or executive sponsor
- Generate weekly support activity report
- Find how to access a customer's NCP DB dump over SFTP/FTP
- Find a product's official documentation page (user guide, release notes): read `product-docs.md` first

## Do NOT trigger for

- General company information beyond Nakisa — use company employee directory
- Real-time support team capacity — check team calendars or Slack status
- Customer billing/contract details — see Finance team resources

## Usage Rules

1. **Reporter fallback lookup:** When another skill needs the default reporter for a customer, the **Lead Support Sponsor** is the correct field to use. If Lead is blank, use **Backup Support Sponsor**; if also blank, use **Customer Success Manager**; if all blank, prompt the user
2. **Customer name matching:** Customer names here correspond to the "Customer Commitment" field values in Jira — use for cross-referencing
3. **Fuzzy matching:** Some Jira tickets may use abbreviations (e.g., "BP" for "British Petroleum") — match by scanning the Customer Name column

## Additional References

| File | Contents |
|------|----------|
| `~/.gemini/skills/company/nla-docs.md` | NLA product documentation links by version (URL patterns + full table for all releases 5.0 → 2025.R3) |
| `~/.gemini/skills/company/product-docs.md` | Index of docs.nakisa.com by product, with a status per row and the rules for citing it |

## NCP DB Dump / SFTP Access

Use when someone needs to pull a DB dump from an NCP cloud environment (CS/CSR ticket requests, or local dev setup).

- **Portal:** https://ftp.nakisa.com/#/
- **Credentials & full steps:** Confluence page ["Getting NCP DB dumps"](https://nakisa.atlassian.net/wiki/spaces/RD1/pages/24340693135/Getting+NCP+DB+dumps) (RD1 space). Login is a shared team credential — always pull the current password from that page rather than from here, since it can rotate.
- **Flow:** log in → find the customer's environment folder by env ID (e.g. `master-env1`, `ra-env1`, `rb-env1`) → download the relevant dump (nre, fos, nfs, or rem).
- If a CSR/CLOUD ticket says a dump was already "placed" on the server but the requester can't find it, don't assume the general portal flow covers it — confirm the exact env ID/folder with whoever placed it (see e.g. CLOUD-88683 / CSR-28330, Fairprice).

## Saved Reports

### Weekly Support Activity Report

**Trigger:** "weekly support report", "support team weekly", "team activity last week", "team logged stats"

**Week definition: Sunday to Saturday.** The team spans Pakistan (Sun–Thu) and Montreal (Mon–Fri) — Sunday is the earliest workday across all timezones, Saturday is the latest.

For every member listed in `~/.gemini/skills/jira/reference/SUPPORT-TEAM.md`, produce:
1. **Daily hours table** — Query worklog data for the full Sun–Sat range, no assignee filter. Show all 7 columns (Sun through Sat). If a day has no entries across the whole team, the column can be omitted — but never drop a day that has at least one entry.
2. **Updated tickets count** — Query tickets per member: `project in (LAE, NCS) AND updated >= "{start}" AND updated <= "{end}" AND assignee = {jql_name}` (max_results=100). Paste each member's "JQL Name" cell from that file verbatim: it already carries its quotes, `id()` or `currentUser()` form.
3. **Key observations** — flag anomalies (bulk retroactive logging, zero-loggers with high ticket counts)

**Date ranges:**
- Current week: `{most recent Sunday}` to today
- Last week: `{Sunday 7 days before most recent Sunday}` to `{Saturday before most recent Sunday}`
