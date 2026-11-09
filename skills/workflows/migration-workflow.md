# Migration Workflow

**Dependencies:** `~/.gemini/skills/migration/SKILL.md` (rules, folder tree, templates, gates).

**Start here:** open the client's `migration/` folder; the next action is the first step whose gate is not signed.

## Flow

| # | Step | Owner | Gate (who) |
|---|---|---|---|
| 0 | Plan: type, rollback, PII, escalation | main session with the user | agent-quality-guardian reviews, then the user signs `MIGRATION_PLAN.md` |
| 1 | Discover the source (`SOURCE_ANALYSIS.md`) | agent-data-analysis-expert | "ready to send to the client"; client answers |
| 2 | Trace the target, build `FIELD_MAPPING.md` and `BUSINESS_RULES.md` | agent-codebase-archaeologist traces; main session assembles | agent-quality-guardian, then one adversarial-review pass (skill, main session) |
| 3 | Transform scripts and a target contract probe | agent-implementation-engineer | scripts are idempotent and write `transform_log.csv` |
| 4 | Pilot: Tier 1 (20 records, client verdict), Tier 2 (stress) | agent-qa-engineer runs both; the client decides Tier 1 | "ready to pilot"; client (through the main session) |
| 5 | Reconcile | agent-qa-engineer owns the verdict; agent-data-analysis-expert computes totals | "ready to reconcile"; agent-quality-guardian |
| 6 | Load and cutover (the skill's Phase 5; README Phase Status row 06) | main session | "ready for go-live"; the user's yes per write; named client go/no-go owner |

## Routing

- Pilot APPROVED -> step 5. PARTIAL -> re-pilot the failed subset (max 1). REJECTED -> step 2 (max 2), then escalate to the client sponsor.
- Reconcile fails on a transform bug -> step 3 (max 2); on a mapping or discovery gap -> step 2 or 1 (max 2). Then stop and ask the user.
- agent-quality-guardian REVISION_NEEDED at step 0, 2 or 5 -> that step's owner (max 2); BLOCKED, or a third revision -> stop and ask the user.
- An empty or failed trace in step 2 is recorded as "not traced", never "unmapped".
- A subagent that returns nothing is retried once, then the main session reports it and stops.
- A client gate pauses the workflow in the main session; the README Phase Status holds the state.
- Writing to the target environment always needs the user's yes first.
