# Runbook types, spine and quality gate

Load when writing, reviewing or restructuring a runbook. A runbook is **instructions to follow, in order**, like the implementation of a use case: someone with no prior knowledge can finish it without the author.

## The spine: the same headings in every type

1. **Title "How to <verb> <object>"** and nothing else: the card carries type, scope and environment, so no parentheses in the title.
2. **Card:** Type (API, UI logic, Operation, Communication or Composite; an operation runbook whose steps call endpoints is `API (operation)`), Owner (a role, never an email), Tags (topics, for search), Last verified (date, environment, and whether the scripts were run as files), **Changes** (one of: READ-ONLY, CREATES PERMANENT, CHANGES SHARED SETTINGS, SENDS OUTSIDE: SAP, email, a client).
3. **Use this when** (the trigger) and **Outcome**. **Ends with:** what exists at the end and, for a record that moves through states, ``State chain: `A` → `B` → `C` ``. **Does not:** what it leaves out, linking the runbook to use instead. A runbook that crosses hosts adds a one-line `Route:` (the calls in order, arrows between).
4. **Before you start:** access (the key's name only, how it reaches the shell), tools, an inputs table (value, where it comes from), prior runbooks and the state they must end in, environment data-blocker rows to check.
5. **Steps**, numbered in true execution order: the primary path only, start to end, no alternates inside it. A step with no call (someone else acts, or "stop here") is a note between steps, not a number.
6. **Variants** (only if there are any): each alternate path (a failure, a retry, another mode or actor) is its own `###` heading, linked by anchor from the step where it forks. It says "Branches from step N", what it needs, and "Returns to step M" or "Ends"; its steps use the same block, lettered a, b, c.
7. **Verify:** a separate read that proves the end state, not the write's own success.
8. **Undo and clean-up. Mandatory.** If no undo exists, write "none possible" and say what stays behind. Restore rule: gate 7.
9. **If stuck:** a table of symptom, cause, fix; then who to contact (a role).
10: **Links:** reference docs, the sidecar restrictions, the records registry, evidence; never copy their content. **After this:** the next runbook and the values handed to it, named as that runbook's inputs table names them.
11. **Changelog**, newest first.

Rules for every type:
- **One purpose per runbook.** A long page means two runbooks. A goal that needs several runbooks in sequence gets a Composite runbook that only links them in order and names the values handed from one to the next.
- **Order is checked, not assumed.** Every "Needs" points to an earlier "Keep" or to a "Before you start" row; nothing is produced later. Setup a reader must do (create a folder, export a variable) is a numbered step or a Before-you-start line with the exact command, never prose the author knew.
- **Names match the script.** A Keep and a Needs use the script's own `--variable` or capture name, so a reader pastes it into the next command unchanged.

## Types and what each adds to the spine (M = mandatory)

| Type | Use when | Reader | Adds or changes |
|---|---|---|---|
| **API** | a use case is driven through endpoints | tester new to the product | M: per-step API block (below), host and headers line, the script path; O: a run-all command that is identical to the script |
| **UI logic** | the work or the check happens on screens, or a rule decides what the screen shows | anyone with a UI login | M: per step the screen or URL, the click or entry, what you should see; the business rule in one line; O: screenshot; O: a paired scenario script, then every step ends `Proof: <repo-relative script> check <N>` or `Proof: none (manual)` (a check proves only what it asserts, on the build in Last verified), and the sign-in is "per the `browser-login` skill", never its path |
| **Operation** | upkeep: keys, profiles, counters, environment resets | whoever maintains the suite | M: the symptom as the trigger. If its steps call endpoints, its type is API (operation) |
| **Communication** | someone must be told or must approve (before a post to an outside system, after leaving permanent records, a client reply) | the author or a colleague | M: trigger, audience, channel, message template, the approval needed, where the sent message is recorded |
| **Composite** | one goal needs several runbooks in order | same as API | M: ordered links, handed-over values, decision points; no restated steps |

A runbook for a client's case is never written on my own: after the work, I suggest its type, audience and where it would live, and the owner decides. It goes with that client's notes, not in the shared repo, and carries no key values or client record values.

Troubleshooting is each runbook's "If stuck" table plus the data-blockers file; it gets its own page only when one symptom spans runbooks. Onboarding and access is an Operation runbook. Trace and evidence analysis is not a runbook: it is an evidence file.

## API per-step block

```
N. **<Verb> <object>.**   [WRITES | PERMANENT | SENDS OUTSIDE] when it applies
   - Do:       one action in plain words
   - Call:     METHOD {host}/path · script <path> · exact command (one call per step; split two calls that each have their own Keep, failure or write)
   - Needs:    <name> from step K, or a Before-you-start row
   - Keep:     <json path> as <script variable name>, used in step L
   - Why:      one line
   - Doc:      vendor URL#anchor, or "none found: <what was searched>"
   - Expected: status and the field or state to check; a write step names the state it reaches
   - If instead: <symptom> -> <cause and fix>; saved or not saved?
   - Undo:     exact call, or "none: leaves <record>, log it in the registry"
```

For a vendor documentation page, take the `Doc:` URL per `company` → `product-docs.md` → "## How to use a row".

## Quality gate: run before publishing

1. Title starts "How to", type set, Owner and Last verified filled. For an API runbook, scripts come first: on an environment you own, each script it cites has been run as a file and passed before the runbook is written; the card says "scripts run as files: yes", or names the unproven scripts. Other types need no scripts. If the project has a runbook-script linter, run it.
2. "Use this when" names a trigger and the end state (the state chain, if a record changes state).
3. Every Needs points to an earlier Keep or a Before-you-start row; every variant names the step it forks from and where it returns.
4. Every input says where the reader gets it; no "ask the author".
5. Every command pastes as written, and the runbook and the script agree (variable names, the run-all command); no "add this field by hand".
6. Every step that writes, persists or sends outside is flagged and has an Undo line.
7. Shared settings are restored on failure as well as success, from a value read before the change.
8. Every step has Expected; a write step, and a step with a known failure, also has If-instead; no past-tense results inside steps.
9. A why longer than a line, trace tables, created-record tables, name counters, record ids, dead ends and run logs are links, not inline.
10. Each fact is in one place and linked (data-blockers file, properties file, registry); a hook's or gate's rules are cited, not restated.
11. No key values, client names, user emails, connection strings or local download or user-home paths (use repo-relative paths); no client record values.
12. Acronyms are spelled out or linked; nothing contradicts a linked runbook.

**Test it:** a fresh session with only the repo follows it on the safest environment and logs every point where it had to guess. Zero guesses passes. Where only an environment with permanent records exists, test the read-only steps and review the writing ones.
