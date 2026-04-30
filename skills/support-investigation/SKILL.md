---
skill: support-investigation
description: Application-level support investigation methodology — use when investigating a reported issue using only logs, screenshots, Jira ticket data, and UI evidence. Covers evidence intake, log reading, Five Whys, decision tree triage, root cause confirmation, and resolution scoping. Use this BEFORE agent-debugger when the goal is to diagnose at the support/L2 level without reading source code. Triggers: "investigate this ticket", "what does this error mean", "support investigation", "triage this issue", "analyze the logs", "what caused this", "support-level diagnosis", or any issue investigation where code access is not available or not yet needed.
args: ""
user-invocable: true
---

# Support Investigation Skill

> **Distinction from agent-debugger:** This skill investigates at the *application level* — using logs, screenshots, Jira data, and UI behavior. It does NOT read source code. The goal is a support-specialist-quality diagnosis: confirm root cause, propose data/config fixes, and define a clear escalation path if a code change is needed. Use `agent-debugger` when you need to trace call chains through source code.

## Hard Boundaries — What This Skill Never Does

These are absolute rules. No exceptions.

> **Why these boundaries exist:** Support diagnoses must survive code refactors — a root cause tied to log evidence and data values is durable; one tied to a grep of a constants file is not. Clean handoffs to the right agent also preserve engineering value: when the debugger or engineer receives a well-packaged diagnosis, they add depth rather than duplicating work. These boundaries enforce that separation.

**No source code access.**
Never use the Read tool or any search tool against `.java`, `.xml`, config files, or any file under codebase roots (e.g. `leasing0/`, `vanguard0/`, `scriptmanager/`) — even for a single line, even to confirm an enum value. Evidence comes only from: logs, screenshots, Jira data, masterfile.csv (field/table names only — never to infer logic or relationships), KEDB entries, and documented knowledge in skill files. If any value, signature, or relationship cannot be confirmed from allowed inputs, mark it as "Needs Confirmation" in the output and propose routing to `agent-debugger` — with user confirmation before proceeding.

**No scripts or queries.**
Never write SQL queries, data-fix scripts, or any code as part of an investigation. When the fix requires a script or query, describe exactly what needs to be done (which table, which field, what value) and propose routing to the appropriate implementation agent — with user confirmation before that agent is spawned. The support investigation output is a diagnosis and fix proposal, never the fix itself.

These boundaries are enforced operationally in Phase 6 — see the Routing gate below.

## Allowed Inputs — What This Skill May Read

The positive mirror of the Hard Boundaries above. These are the only sources this skill draws evidence from:

| Source | What it provides | Constraint |
|--------|-----------------|------------|
| **Log files** (attached to ticket) | Error chain, thread, timestamps, class names, entity IDs | Read only what is attached — never fetch from server |
| **Screenshots** (decoded by main session) | Error text, UI state, form values, timestamps | Main session must decode before delegating |
| **Jira ticket** (description, comments, attachments) | User action, entity IDs, environment, version | Via `mcp__jira__*` tools only |
| **masterfile.csv** | Table names and column names only | Never use to infer logic, relationships, or enum values |
| **KEDB entries** (`kedb/INDEX.md`, `kedb/entries/*.md`) | Known error patterns and confirmed fixes | Knowledge-base files — not codebase reads |
| **Skill files** (`.gemini/skills/**`) | Domain patterns, error signatures, fix references | Knowledge-base files — not codebase reads |

**Why KEDB and skill files are allowed:** These live under `.gemini/skills/` — a knowledge layer maintained by the support team, not application source code. Reading them is equivalent to consulting a runbook, not grepping a constants file.

**Anything not on this list requires user confirmation before accessing.**

---

## Dependencies

Load before starting:
- This skill (general methodology — required)
- Any project-specific extension declared in the project's GEMINI.md (e.g. `nla/support-investigation/SKILL.md` for NLA tickets) — provides application-specific log signatures, known error patterns, and data/config fix reference

---

## Phase 0: Pattern Lookup (Run Before Phase 1 If a KEDB Exists)

If the project's GEMINI.md declares a KEDB (e.g. NLA: `kedb/INDEX.md`), run this before Phase 1. If no KEDB exists for the project, skip to Phase 1.

**Step 1 — Extract search signals**
From the Jira description and decoded screenshots, identify:
- The **error code** (most reliable signal: framework error code, application error key, HTTP status)
- The **component name** if visible (class name, service name in the stack)

> **Client-reported signal guard:** If the error code comes only from the Jira description (no log file or attachment has been read yet), tag it as "client-reported, unconfirmed." A client-reported-only KEDB hit must be treated as a **candidate at most — never a strong match** — regardless of how many signals appear to align. Defer confirmation to Phase 2 (log/attachment reading). If attachments are present, extract the error code from those first before running this KEDB lookup.

**Step 2 — Grep INDEX.md for the error code**
Use the Grep tool against `kedb/INDEX.md` (whitelisted under Allowed Inputs — this is a knowledge-base read, not a codebase read):
```
grep "<error_code>" kedb/INDEX.md
```
Collect all matching entry IDs as candidates.

**Step 3 — Score each candidate (require 2 independent signals)**

| Signal combination | Match strength |
|---|---|
| `error_code` + `signature_variant` string found in evidence | **Strong** → primary hypothesis |
| `error_code` + `component` name match only | **Weak** → candidate only |
| `error_code` alone | **Weak** → candidate only |

**Step 4 — Route by match strength**

| Result | Action |
|---|---|
| Strong match | Load full entry from `kedb/entries/K00N.md`. Carry as **primary hypothesis into Phase 4** (not Phase 5). |      
| Weak match | Note as candidate. Proceed through all phases. Use candidate to focus Phase 3 (Five Whys) direction. |
| No match | Proceed to Phase 1 normally. |

**Step 5 — Emit `kedb_check` block (mandatory regardless of match result)**

Every `support-investigation.md` must include this block:

```yaml
kedb_check:
  matched: K001           # or null
  confidence: high        # high | medium | low | null
  signals_matched:
    - error_code: JCO_ERROR_COMMUNICATION (102)
    - signature_variant: "hostname '?' unknown" found in log line 13629
  candidates_reviewed: [K001]
  action: carried into Phase 4 as primary hypothesis
  # or: "no matches — proceeded to Phase 1"
```

Missing `kedb_check` block = investigation is incomplete.

**Anti-patterns:**
- Never skip Phase 2 (log reading) based on a Phase 0 hit — logs must still be read to confirm
- Never jump to Phase 5 directly from Phase 0 — Phase 4 (hypothesis/confirm) is mandatory even on strong matches
- A Phase 0 hit is a hypothesis, never a conclusion

**Confidence rubric:**
- **High** = `error_code` + `signature_variant` confirmed in Phase 4 logs
- **Medium** = 1 signal + plausible hypothesis, not yet multi-ticket confirmed
- **Low** = weak match, not confirmed

---

## Available Evidence Types

Before starting, identify what evidence is available. Collect all of it before forming hypotheses.

| Evidence Type | What to extract |
|--------------|-----------------|
| **Jira ticket** | Error message, user action that triggered it, affected entity IDs, version, environment, attachments |       
| **Screenshots** | Exact error text, UI state, form field values, notification content, timestamps visible |
| **Log files** | Error chain, thread ID, timestamps, class/method names, user session, entity IDs |
| **Config screenshots** | Field values set, system type, dates, flags, dropdown selections |
| **User description** | What they were trying to do, what changed recently, whether reproducible |

**Screenshot rule:** The main session must read screenshots — subagents cannot see images. Extract all visible text, field values, error messages, and timestamps before delegating.

---

## Phase 1: Intake

Read everything before touching the logs. The Jira description and screenshots often contain the answer.

1. **What was the user doing?** — The exact UI action (button clicked, form submitted, batch triggered)
2. **What entity was involved?** — IDs (contract, order, account, company code, etc.)
3. **What error appeared?** — Exact message, not a paraphrase
   > **Client-reported vs. evidence-confirmed errors:** The error in the Jira description reflects what the customer saw or was told — it may be a downstream/cascading error, from a forwarded email, or describe a different failure than what logs or attachments show. Never carry a description error code directly into Phase 0 KEDB matching or Phase 4 triage without first checking whether attachments confirm it. Mark description errors as "client-reported" until confirmed by evidence.
4. **What environment?** — Production, QA, version number
5. **What changed recently?** — Upgrade, config change, data migration, settings update
6. **Are attachments present?** — Log files, screenshots, exports

Write a one-paragraph intake summary before moving to log analysis. It forces clarity.

**No logs available?** If no log files are attached and the Jira description + screenshots are insufficient to form a hypothesis, stop here. Document what evidence is missing, ask the customer for logs (or the specific log file, date range, and timezone), and mark status as "Needs Customer Input". Do not attempt to guess root cause without log evidence.

---

## Phase 2: Log Reading Methodology

### Log Line Anatomy

Most application logs follow this structure:

```
TIMESTAMP - LEVEL - IP - USER - CLASS - [THREAD] - ENDPOINT - MESSAGE
```

Example:
```
2026-04-22 11:40:58,123 - ERROR - 10.0.8.1 - abdul.ghani - ActivationGroupService - [http-nio-exec-1794] - /services/ActivationGroupService/activate - Task failed
```

Key fields to track:
- **TIMESTAMP** — when it happened; look for clustering
- **THREAD** (`[http-nio-exec-NNNN]`) — all lines from the same thread are the same request
- **CLASS** — tells you which part of the application was running
- **USER** — confirms which user triggered it

### Reading Error Chains

Most application errors are wrapped. The first `ERROR` line is rarely the real cause. Always read the full `Caused by` chain to the bottom.

```
ERROR: ApplicationException: Something went wrong        → what the user sees
  Caused by: MiddlewareException: Connection failed      → one level deeper
    Caused by: NetworkException: Timeout after 30s      → closer to root
      Caused by: DNSException: hostname 'X' unknown     → actual root cause
```

**Rule: the last `Caused by` is always the most informative.** Work from the bottom up when reading a stack trace.

### Thread Tracking

If an error spans many lines, all lines share the same thread ID. Use the thread to isolate the complete request:

```
grep "http-nio-exec-1794" cds.log
```

This gives you the full sequence of events for that one request, in order.

### Timestamp Correlation

Events that happen within the same second or millisecond are part of the same operation. Use timestamps to:
- Confirm what the user was doing when the error fired
- Separate unrelated noise from the relevant event
- Identify retry patterns (same error 3-4 times in rapid succession = one request with retries)

---

## Phase 3: Five Whys — Applied to Logs

Start with the surface error and ask "why?" at each layer until you reach something actionable.

```
Surface error:  "Payment processing failed — internal error"
  Why?          External service call timed out after 30s
  Why?          Connection to payment gateway refused
  Why?          Firewall blocks outbound port 443 from the app server
  Why?          Network team changed the security group last week
  Actionable:   Customer IT to restore the outbound firewall rule
```

Stop when you reach a cause that is:
- A missing configuration value
- A missing data record
- An unreachable external system
- A user/process error
- Something that requires a code change (→ escalate)

Three to five "whys" is usually enough. If you are still asking after seven, you are going too deep for support level.

---

## Phase 4: Triage — Error Category Decision Tree

Classify the error before investigating further. The category tells you where to look.

```
Error in logs?
├─── Connectivity error (timeout, connection refused, hostname unknown)
│   └─── → Check: external system reachability, hostnames, network config, credentials
│
├─── Missing data / null pointer / "not found"
│   └─── → Check: required config tables, reference data, entity relationships
│
├─── Validation / business rule failure
│   └─── → Check: data values against business rules, required fields, date ranges
│
├─── Permission / authentication error
│   └─── → Check: user roles, system user credentials, API tokens
│
├─── Performance (timeout, slow query, OutOfMemory)
│   └─── → Check: query execution time in logs, data volume, index usage
│
├─── Unexpected state (wrong status, wrong value, workflow stuck)
│   └─── → Check: entity status in database, recent changes to the record
│
└─── Expected behavior / user expectation mismatch (no error in logs, feature works as designed)
    └─── → Confirm intended behavior from product documentation or release notes
        → User education, workflow correction, or feature request
```

Use the category to focus the investigation. Do not try to investigate all categories at once.

---

## Phase 5: Hypothesis → Evidence → Confirm

Never state a root cause without confirming it against evidence.

**Hypothesis format:**
> "I believe the error is caused by [X] because [log line / config value / missing data]."

**Confirmation checklist:**
- [ ] Can I trace the error directly to the hypothesized cause in the logs?
- [ ] Does the timeline make sense? (cause happened before the error)
- [ ] Is there a config value or data record that is missing, wrong, or mismatched?
- [ ] If I fix the hypothesized cause, does the error go away logically?
- [ ] Are there alternative explanations I haven't ruled out?

If you cannot confirm against evidence, mark the hypothesis as unconfirmed and list what information would confirm or rule it out — then ask the customer for it.

---

## Phase 6: Resolution Routing

The support investigation ends with a diagnosis and a routing proposal — not a fix. Route to the right team, with the right context package, and wait for user confirmation before any agent is spawned.

| Fix Type | Route to | What to include in the handoff |
|----------|----------|-------------------------------|
| **Data / config correction** | Implementation agent (e.g. `agent-nla-implementation-engineer`) | Table name, field name, current value, required value, affected entity IDs |
| **SQL query needed** | Implementation agent | Entity, fields to return, filter conditions, join chain — no code, just the specification |
| **Script needed** | Implementation agent | What entity to update, what field, what condition — full spec, no code |
| **User guidance** | Document in output — no agent needed | Correct workflow steps, what the user did wrong, how to avoid it |
| **Infrastructure fix** | Document for customer IT — no agent needed | DNS entry, firewall rule, hostname, network access details |
| **Code-level investigation** | `agent-debugger` | Evidence package: log lines, thread ID, entity IDs, reproduction steps, data/config fixes ruled out |
| **Code bug confirmed** | `agent-debugger` | Same as above, plus confidence level and what specifically in the code is suspected |

**Rules:**
- **Hard stop before every routing action.** Present the routing proposal and wait for explicit user confirmation. Do not spawn any agent until the user says yes.
- The proposal must include: which agent, why it was chosen, and the full context package that will be passed.
- Do not write the fix yourself — describe what needs to be done and let the routed agent execute.
- If multiple fix types apply (e.g. data fix + code fix), present them in priority order (least disruption first) and confirm each routing action separately.
- One confirmation = one agent spawn. Do not chain multiple agent calls from a single approval.

**Routing proposal format:**
> **Proposed: Route to [agent-name]**
> Reason: [why this agent, what fix type was identified]
> Will pass: [summary of context package — entity IDs, table/field names, log lines, reproduction steps]
> Confirm to proceed?

**Before routing, confirm:**
- Root cause is documented with evidence in `support-investigation.md`
- The fix type is clearly identified
- The context package for the target agent is complete

---

## Output Format

### `support-investigation.md` — Root Cause Document

```markdown
# Support Investigation: [Ticket] — [Short title]

## TL;DR
[Root cause in 2 sentences. Fix in 1 sentence.]

## kedb_check
```yaml
kedb_check:
  matched: K001       # or null
  confidence: high    # high | medium | low | null
  signals_matched:
    - error_code: ...
    - signature_variant: "..." found at log line N
  candidates_reviewed: [K001]
  action: carried into Phase 4 as primary hypothesis
```

## Root Cause
[What caused the error, confirmed by evidence.]

## Evidence
[Log lines, config values, screenshots decoded — the specific evidence that confirms the root cause.]

## Five Whys
[The chain from surface error to root cause.]

## Fix Options
[Ordered by least disruption. Data/config fixes first. Escalation last.]

## Ruled Out
[Hypotheses that were considered and why they were eliminated.]

## Questions for Customer
[Specific, answerable questions needed to proceed — only if fix cannot be determined yet.]
```

### `support-walkthrough.md` — Narrative for Knowledge Sharing

A readable story of the investigation: what was reported, what the evidence showed, why it happened, and what to do. Written so someone unfamiliar with the ticket can pick it up cold. Include:
- Ticket summary
- Screenshots decoded
- Log error chain (annotated)
- Plain-English explanation of why the error occurred
- Fix options with pre-requisites
- What was ruled out

---

## Customer Response Language Rules

Apply these rules whenever drafting any customer-facing reply — interim status updates, question batches sent during Phase 3 (Five Whys), or final findings communicated in Phase 6 (Resolution Routing).

The confidence label you assign in your **Escalation Package** (`Confirmed / Probable / Suspected`) directly determines which language tier to use below. These two systems are intentionally aligned — do not use stronger language in the customer reply than your investigation confidence justifies.

### Root cause confidence language

Never say "we have identified the root cause" unless **all competing hypotheses have been ruled out and the cause is directly confirmed by evidence**. Overstating confidence damages credibility — if the follow-up contradicts the claim, trust is lost.      

Use the following language tiers instead:

| Confidence level | What it means | Language to use |
|---|---|---|
| **Confirmed** | Single hypothesis, all others ruled out, evidence is direct and unambiguous | "The logs confirm that..." / "The failure is caused by..." |
| **Probable** | Strong hypothesis, 1–2 competing explanations, needs one customer-side confirmation | "Our investigation points to..." / "The logs suggest the failure is caused by..." / "We've traced the failure to..." |
| **Suspected** | Plausible hypothesis, multiple competing explanations, significant evidence still missing | "We believe this may be related to..." / "A possible cause is..." / "We're investigating whether..." |

The questions you send to the customer exist precisely because the confidence is **Probable** or **Suspected** — the response must reflect that, not paper over it.

### Hedging principles

- **Commit to update timing, not resolution certainty.** "We will have an update by EOD" is a promise you can keep. "This will be resolved shortly" is one you can't guarantee.
- **Separate what is confirmed from what is still being investigated.** State facts first, then hypotheses. Never blend them into a single claim.
- **Avoid over-promising to reduce pressure.** Under-confidence that later proves accurate builds more trust than over-confidence that turns out wrong.

### What to avoid

- "We have identified the root cause" — unless confidence is **Confirmed**
- "The issue is caused by X" — unless confidence is **Confirmed**
- "This will be resolved once you do X" — unless your Fix Options block contains a single recommended fix with no competing explanations
- Stating a hypothesis as fact to sound more authoritative

---

## Questions to Always Ask the Customer

Before closing or escalating, ensure you can answer these:

1. What exactly were you doing when the error appeared? (step by step)
2. Is this happening for all users or a specific user?
3. Is this happening for all records or a specific one? (provide the ID)
4. When did this start? Did anything change before it started? (upgrade, config change, data import)
5. Can you reproduce it consistently, or is it intermittent?
6. Does it happen in all environments (prod, QA) or only one?

---

## Escalation Package (if code-level investigation needed)

If escalating, always provide:
- Ticket link
- Root cause hypothesis (what you believe, with evidence)
- Log file with the relevant section highlighted (line numbers)
- Screenshots decoded into text
- Entity IDs affected
- Reproduction steps
- What data/config fixes have already been ruled out and why
- Your confidence level: Confirmed / Probable / Suspected
