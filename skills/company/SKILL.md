---
name: company
description: Quick lookup of Nakisa customer accounts, support sponsors, NLA product documentation, and support team activity reports. Use this when you need to find Lead/Backup Support Sponsors for LAE tickets, identify customer regions/platforms, find doc links for specific NLA versions, or generate weekly support team activity reports.
---

# Company Skill: Customer & Support Sponsor Lookup

## Purpose

Quick lookup of Nakisa customer accounts, their assigned support sponsors, and account metadata. Use this when you need to:
- Find the **Lead/Backup Support Sponsor** for a customer (e.g., to set as reporter on LAE tickets)
- Identify which **region** or **line of business** a customer belongs to
- Look up the **Customer Success Manager** or **Executive Sponsor**
- Find **support team members** for Jira query filtering

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

**Support team members list:** See the `## Support Team Members` section in the reference file, or use the table below for Jira queries (accountIds and confirmed JQL formats are pre-looked up).

## Support Team Members — Jira Reference

**Search order:** Try the "JQL Name" column first. If it returns no results, fall back to the `accountId`.

| Display Name | JQL Name (try first) | AccountId (fallback) | Email |
|---|---|---|---|
| Lorena Mosquera | `"Lorena Mosquera"` | `712020:25077a7c-f4fd-4af6-a271-b6f94b20915e` | lorena.mosquera@nakisa.com |
| Sadia Ahmad | `"sadia.ahmad"` | `629a1c952eafc9006eedd606` | sadia.ahmad@nakisa.com |
| Ahmed Aamir | `"Ahmed Aamir"` | `712020:9c56f3f7-917d-4246-81df-4bd59a02e022` | mohammadahmed.aamir@nakisa.com |
| Haffy Khayam | `"haffy.khayam"` | `62bdab61018dea0d40752e6b` | haffy.khayam@nakisa.com |
| Samra Ejaz | `"Samra Ejaz"` | `712020:d2fbc024-14ad-47fc-901f-02ef4186e0f4` | samra.ejaz@nakisa.com |
| Catalina Fulger | `"Catalina Fulger"` | `60ba747313c0e9006913d1d6` | catalina.fulger@nakisa.com |
| Samee Rehman | `"samee.rehman"` | `5b1aad653993e91965030347` | samee.rehman@nakisa.com |
| Masood Khurram Khan | `"Masood Khurram Khan"` | `712020:39e5411f-837a-4edc-a8a5-4bcea53bc2d9` | masood.khurram@nakisa.com |    
| Muhammad Farooq | `"muhammad.farooq"` | `5c7fe86a2872ab111c19d921` | muhammad.farooq@nakisa.com |
| Lionel Malonga | `"lionel.malonga"` | `5a149b5d39bd3070008000b1` | lionel.malonga@nakisa.com |
| Mohsin Ali | `"mohsin.ali"` | `5cd0559c25d61c0dc614cd5e` | mohsin.ali@nakisa.com |
| Ming Lu | `"ming.lu"` | `557058:71f88e67-1b3e-4009-a16c-c543c016a0b8` | ming.lu@nakisa.com |
| Zark Ahmed | `"zark.ahmed"` | `5a1da1e6007eb21a79e60151` | zark.ahmed@nakisa.com |
| Nauman Sohail | *(skip — name fails)* | `62da80ed4c448ca67cf41959` | nauman.sohail@nakisa.com |
| Sajjad Ali Barkat | `"Sajjad Ali Barkat"` | `5fd384db44065f013facdc90` | sajjad.barkat@nakisa.com |
| Dexter Pagkaliwangan | `currentUser()` | `60396b7af032740068924835` | dexter.pagkaliwangan@nakisa.com |

**Notes:**
- Nauman Sohail's name format fails in JQL — skip straight to accountId
- Sajjad's full Jira name is **Sajjad Ali Barkat** (not "Sajjad Barkat")

## Usage Rules

1. **Reporter fallback lookup:** When another skill needs the default reporter for a customer, the **Lead Support Sponsor** is the correct field to use. If Lead is blank, use **Backup Support Sponsor**; if also blank, use **Customer Success Manager**; if all blank, prompt the user
2. **Customer name matching:** Customer names here correspond to the "Customer Commitment" field values in Jira — use for cross-referencing
3. **Fuzzy matching:** Some Jira tickets may use abbreviations (e.g., "BP" for "British Petroleum") — match by scanning the Customer Name column

## Additional References

| File | Contents |
|------|----------|
| `~/.gemini/skills/company/nla-docs.md` | NLA product documentation links by version (URL patterns + full table for all releases 5.0 → 2025.R3) |

## Saved Reports

### Weekly Support Activity Report

**Trigger:** "weekly support report", "support team weekly", "team activity last week", "team logged stats"

**Week definition: Sunday to Saturday.** The team spans Pakistan (Sun–Thu) and Montreal (Mon–Fri) — Sunday is the earliest workday across all timezones, Saturday is the latest.

For all 16 support team members, produce:
1. **Daily hours table** — `mcp__jira__get_worklogs_by_date` (full Sun–Sat range, no assignee filter). Show all 7 columns (Sun through Sat). If a day has no entries across the whole team, the column can be omitted — but never drop a day that has at least one entry.
2. **Updated tickets count** — one `search_jira_issues` query per member: `project in (LAE, NCS) AND updated >= "{start}" AND updated <= "{end}" AND assignee = "{jql_name}"` (max_results=100). Use each member's JQL Name from the table above; for Nauman use accountId `id("62da80ed4c448ca67cf41959")`, for Dexter use `currentUser()`
3. **Key observations** — flag anomalies (bulk retroactive logging, zero-loggers with high ticket counts)

**Date ranges:**
- Current week: `{most recent Sunday}` to today
- Last week: `{Sunday 7 days before most recent Sunday}` to `{Saturday before most recent Sunday}`

## Integration with Other Skills

- **Jira skill** (`~/.gemini/skills/jira/SKILL.md`): When the LAE reporter convention says to use the NCS ticket assignee but no NCS ticket is linked, fall back to this skill's reporter fallback lookup
