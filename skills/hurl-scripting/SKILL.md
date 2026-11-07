---
name: hurl-scripting
description: >-
  Verified conventions and non-obvious gotchas for writing, running, reviewing or debugging Hurl
  (.hurl) API test/chain files. MANDATORY: Load before writing, running, reviewing or debugging
  any .hurl file. Triggers on "write a hurl file", "hurl chain", "hurl script", ".hurl", "run this
  hurl", "review this .hurl", "hurl assertion", "hurl capture", "hurl --json", "hurl --secret",
  "variables-file", "hurl verbose", "hurl output file", "why is my hurl file failing", "hurl
  variable not working", "how do I capture a value in hurl", "retry a failed hurl request". Do NOT trigger for choosing between
  Hurl and another tool in the first place (see the qa-engineer skill), or for jsonpath/HTTP
  questions unrelated to a .hurl file.
---

# Writing Hurl Scripts

Hurl is for **fixed, linear, no-branching sequences of HTTP calls with hard pass/fail assertions** — not for exploration, backoff, or conditional logic (a fixed `[Options] retry` / `retry-interval` on a read is fine — see "Repeating a failed mutating request"). The moment a "chain" needs an `if`, it belongs in a general-purpose language (pytest/httpx, etc.) that drives Hurl rather than replacing it.

**Tags:** *verified* means tested live — tool behavior on hurl 8.0.1 (Windows) unless another version is named; an untagged gotcha is an observation not re-tested; **UNVERIFIED** is a lead to test before relying on it (`rg -n UNVERIFIED` lists them).

## Variables: defaults vs. runtime-only

- `[Options] variable: name=value` sets a variable for **the rest of the file**, not just that entry.
- **Gotcha:** `[Options] variable:` silently **overwrites** a same-named variable from an earlier block or from `--variable` — no error, no warning; the last declaration wins for everything after it. Give every distinct value its own name (`service_a_host`, `service_b_host`, never a shared `host`), or a request meant for service A can silently hit service B.
- Never give a secret (API key) or a not-yet-known value an in-file default. Leave it undeclared so it must be supplied via `--variable name=value` at runtime — Hurl errors clearly if it's missing, rather than silently running with a wrong/empty value.
- **Prefer `--secret NAME=VALUE` / `--secrets-file <file>` over a plain `--variable` for real secrets** — same `{{name}}` templating, but Hurl redacts the value (prints `***`) in `--verbose` traces, including the reconstructed `curl_cmd` line.
  - **Gotcha, verified:** the `--verbose` redaction does NOT extend to `--json` output — a value passed via `--secret` still appears in **plaintext** in `--json`'s `request.headers[].value` and `curl_cmd` fields. Don't assume `--secret` makes it safe to log, save, or share `--json` output; it only protects the human-readable trace.
- **Narrow exception (hardcode the literal key):** only on an explicit, informed, per-repo decision by the repo owner (e.g. "private, never shared") — never a default, inference, or silent application. Requires a technical guard that actually blocks the push — gitignore the `.hurl` files, or a pre-commit hook; a header comment states intent but does nothing to stop `git add -A`. A committed key lives in git history forever, even after deletion.
- **Bulk external inputs via a file:** `--variables-file <file>` loads many vars at once from a plain text file (any extension) — one `name=value` per line; `#` comment lines and unquoted spaces in values both work (verified). **Values are type-inferred, so leading zeros are silently lost** — a bare `code=0001` becomes the number `1`; quote it (`code="0001"`) to keep it a string (verified). The request then goes out with a value that doesn't exist, and the error is usually about the *entity* not being found, not the coercion. Passing `--variables-file` more than once is allowed and the files merge (verified). `--secrets-file <file>` is the same format with values redacted like `--secret`; keys go there, never in a plain `--variables-file` (not redacted). An in-file `[Options] variable:` of the same name silently overrides a `--variables-file` value, so do NOT also declare file-supplied vars in the `.hurl`.

## Chaining across requests

- `[Captures]` only carries variables forward **within a single file, in a single invocation**. Two separate `.hurl` files run as two separate CLI calls do NOT share captured state — each run gets a fresh variable slate. If step B needs a value captured in step A, both steps must live in the same file.
- Keep every chained request also runnable on its own, so one call can be debugged without running the whole chain.
- Before writing an assertion or capture path, verify the actual response shape — don't assume the payload sits at the document root. Some APIs wrap the real payload one level down (e.g. under a literal key like `"object"` or `"data"`); others don't. Read one real captured response before writing the path.
- **A capture whose jsonpath matches nothing is a HARD FAILURE, not a null.** The whole entry fails with `No query result`. This bites on **optional** response fields: the script works on record A and dies on record B. Capture only fields present on *every* record you'll target; read genuinely-optional ones out of the saved `[Options] output:` file instead, or give the optional case its own dedicated `.hurl`.
- **Gotcha, verified: `[Captures]` are evaluated BEFORE `[Asserts]`, regardless of the order they appear in the file.** So you **cannot** guard a capture with an assert in the same entry — a `jsonpath "$.x" exists` placed above the captures never fires; the capture's `No query result` error surfaces first and blames the capture line. (`exists` works when no capture in the same entry fails.) To get a readable failure, split the check into its own entry, or accept the raw capture error and document the expected failure mode in the header.

## jsonpath in Hurl — non-obvious behavior

`[*]` wildcards over every array element (returns a **list** — except at exactly one match, where it collapses to a scalar; see the gotcha below); `[?(@.field=='x')]` filters to matching elements only, `@` meaning "the element currently being tested."

- **Gotcha:** `count(...)` on top of a filter expression **errors** rather than cleanly returning `0`/`1` — it fails one way when the filter collapses to a single match and a different way on zero matches. Don't use `count` to check filter-match existence.
- **Membership check via wildcard + `contains`:** `jsonpath "$.items[*].someField" contains "{{value}}"` — but see the single-element trap below before relying on it (loud on a number; on a string see the UNVERIFIED note below).
- **Gotcha, verified: `[*]` over a SINGLE-element array collapses to a scalar, and `contains` then fails on a type mismatch,** not a clean pass/fail (`types between actual and expected are not consistent`). So the wildcard+`contains` idiom is **not** safe for 0, 1, or many — it breaks at exactly 1, the common case for a filtered lookup. Where the count is knowable, assert it first and index directly instead — `jsonpath "$.page.totalElements" == 1` then `jsonpath "$.items[0].someField" == {{value}}` — and say in a comment that the count assert is what licenses the `[0]`. **UNVERIFIED (combines the collapse above with the string rule below; test before relying on it): on a STRING field the collapse is silent, not loud** — one match becomes a string, `contains` turns into a substring check, and `"100123"` contains `"1001"` passes with no error. Same fix: assert the count, then `==` on `[0]` — or filter on a unique key (below).
- **UNVERIFIED (documented Hurl behavior; test before relying on it): `==` is type-strict** — the string `"123"` does not equal the number `123`, so a quoted `{{var}}` against a numeric field (or the reverse) fails or passes for the wrong reason.
- `contains` behaves differently by the left side's type: against a **list**, it checks membership; against a **string**, it checks substring match. Know which one applies before relying on it.
- **Verified (2026-10-16): a filter matching exactly one element collapses to that scalar in `[Captures]` and `[Asserts]` alike** (the same collapse as `[*]` above), unlike `count`. In `[Asserts]` that is the order-free way to check one known row: `jsonpath "$.content[?(@.code=='X-{{v}}')].status" == "ACTIVE"`. Filter on a key unique in the response, and make sure the row is on the page fetched (`size` ≥ `totalElements`). **UNVERIFIED:** zero matches and 2+ matches under `==` (expected to fail, never run).
- A `[Captures]` filter matching **multiple** elements silently returns a **list**, not an error. Used inline in a scalar field (`"id": {{captured_id}}`) OR as an array body (`"idsIn": {{captured_list}}`), Hurl fails loudly at render time (`Unrenderable expression ... value [a,b,c] can not be rendered`) naming the value. `{{name}}` substitution is scalar-only, even when the captured value is a list. For the scalar case, verify uniqueness of the field you're filtering on. For a real array body, there is no single-file way to feed "N ids from step 1" into step 2 — build the body with an external script (Python/bash reading step 1's `[Options] output:` JSON) and source it as the request body with `file,body.json;`.

## Output and debugging — pick the right one, don't default to the noisiest

| Need | Use |
|---|---|
| CI-gate, pass/fail only | `--test` (by itself shows no response body or captures) |
| See exactly one response body, nothing else | plain `hurl file.hurl` (no flags) — prints only the last response's body by default |
| Save one specific request's response body to disk, isolated from others in the same file | `[Options] output: <file>` on that request — but ONLY written if that entry fully succeeds; see the two gotchas below |
| Full request/response trace incl. captured variable names+values | `-v` / `--verbose` — note captures print to **stderr**, so isolate one value with `2>&1 1>/dev/null \| grep <name>` |
| Structured, scriptable output (multiple named fields, programmatic use) | `--json` — top level is an object with an `entries` array, not a bare list; each entry has its own `captures` array |

Don't reach for `--verbose` or `--json | jq/python` by default — they're for active debugging. `--test` is the everyday default once a chain is working.

**Mutating batches: `--jobs 1`, and never `--continue-on-error` (one teardown exception, below) or `--retry`.** `hurl --help` says `--test` uses parallel execution, `--jobs <NUM>` caps it (`1` disables it), `--continue-on-error` keeps running requests after a failure, and `--retry <NUM>` is a run-wide flag — it would reach write entries too, so treat it like `[Options] retry` on a write (see "Repeating a failed mutating request"). **UNVERIFIED:** whether parallel mutating scripts that share records interfere — set `--jobs 1` regardless. A mutating chain must stop at its first failure, because later writes assume the earlier state. The one exception is a final teardown group that must run after a failed wait (a flow that switches off what it created); the script's header says why.

**Gotcha, verified — `output:` is NOT written when the entry fails.** If the `HTTP <status>` assert fails OR any `[Captures]` jsonpath finds nothing, no output file is produced — in `--test` AND plain mode alike (tested across all 6 combinations). `--verbose` and `--json` also showed no response body on a failing entry. **Verified 2026-10-27 (hurl 8.0.1, Windows): to see a failing read-only entry's body, copy that one entry alone to a scratch file with its status line set to `HTTP *` and no asserts or captures, then run it plain with `--include`; it prints the status line, headers and body.** A plain run prints only the LAST response of a file, so probe one entry per file; `--json` gives per-entry status but no body field. Never for a mutating request (see "Repeating a failed mutating request"). **UNVERIFIED:** `--very-verbose` or `--error-format long` may print the body in one run. Corollary for mutating requests — a write can succeed server-side while you're left with no record of what came back.

**Gotcha, verified:** Hurl does **not** create the `output:` directory. A missing directory fails with `can not be written (... os error 3)` (Windows wording) — and that failure happens *after* the request has already been sent, so for a mutating call the change lands and the response is lost. Create output directories up front (and in a repo, commit a `.gitkeep` so a fresh clone's first run doesn't hit this).

**Gotcha, verified:** no mode reveals which file an `[Options] output:` line wrote to — not `--test`, plain output, or `--json`. (`--json` has `cookies`/`entries`/`filename`/`success`/`time` at top level and `asserts`/`calls`/`captures`/`curl_cmd`/`index`/`line`/`time` per entry; `filename` is the `.hurl` source, so no output-file field exists.) To know where a response landed, read the source's own `output:` line.

## Safety pattern for any mutating request (PUT/PATCH/POST that changes real data)

Capture the response **before** the mutation and **after** it, each to its own file via `[Options] output:`. This is not an automatic rollback — Hurl has no undo. It's an audit trail: if the update turns out wrong, a human reads the "before" file's original values and manually re-issues an update with those values to revert. Give the "after" entry a status-only assert and put field checks in a separate entry: a failed entry writes no `output:` file (see Output and debugging), so a field assert on the same entry would erase the "after" snapshot exactly when the write went wrong.

Two further things a mutating request needs beyond that audit trail: **proof the write actually landed** (the next three paragraphs) and **the ability to run the script twice** (the duplicate-create gotcha); read asserts added after the first run go in a separate script (the last paragraph).

**`HTTP 200` alone proves nothing about a mutation (the "200-can-lie" rule).** Many APIs return 200 for a no-op, a partially-applied change, or a silently-ignored field. Always add an `[Asserts]` jsonpath check on the specific field the mutation was supposed to change (read it back from a follow-up GET in a **separate** request — never from the mutating call's own response, see "Worse" below), not just the status code.

**Verified (2026-10-01, 2026-10-16): a bulk write or batch read can return `200` with per-item failures in the body** (seen: `errors.all[]` on a bulk create-or-update that saved nothing for those rows; `hasError: true` per item on a batch lookup). Assert the error list is empty (or each item's flag) and the item count — never the status alone.

**Worse, verified: even the response BODY can echo a value that never persisted.** Some frameworks build the PATCH/PUT response from the client's own in-memory patched object, not a fresh database read. Seen: `200` with the new value in the body, while a separate `GET` showed the old value — the write never persisted. An `[Asserts]` on that same response would have passed on the echo. The only reliable confirmation is a **follow-up GET in a separate request**, however specific the asserted field. **Also seen on a plain `POST` create:** fields the server never persists still came back `200`, all echoed, until a separate `GET` showed none of them. Check every mutating verb the same way, including create.

**Gotcha, verified: a "duplicate create" can be REJECTED, not merged.** Seen: a plain create endpoint returned `400` ("entity with the same unique fields already exists") on a second POST with an unchanged natural key, while a *sibling* create-or-update endpoint on the same resource does merge. **Test which behavior a specific endpoint has — don't infer it from an upsert endpoint elsewhere in the API.** A script that hardcodes a "new record" body is safe to re-run only on a confirmed upsert; otherwise every re-run needs a fresh, never-used natural key (see Explore mode in "Repeating a failed mutating request").

**After a mutating script's first run, put new read asserts in a separate read-only script that reads the records back by natural key; never re-run the write for them** — a re-run overwrites the first run's `output:` files and resends a write that a non-upsert or state-gated endpoint may reject. The Skeleton below is for the first run. Authoring-time only.

## Skeleton — create, capture, verify in a separate request

Illustrative shape, not a tested script:

```hurl
# new_code is supplied at run time (--variable) and is fresh each run
POST {{host}}/things
[Options]
output: responses/create-thing.json
{ "code": "{{new_code}}" }
HTTP 201
# $.id always present; else split the capture out
[Captures]
thing_id: jsonpath "$.id"

# a separate request: the create's own response proves nothing about persistence
GET {{host}}/things/{{thing_id}}
HTTP 200
[Asserts]
jsonpath "$.code" == "{{new_code}}"
```

## Repeating a failed mutating request

Repeat through Hurl, never by hand-replaying with `curl`, so every attempt is recorded. The loop and the decision live in the driver (the AI or a script), never in the `.hurl` file. Pick the mode from how the first attempt failed:

| First attempt ended with | Data written? | Do |
|---|---|---|
| `400`/`422` validation rejection | Probably not (a convention — confirm per endpoint) | **Explore**; if the endpoint is unconfirmed, read back by natural key first, as in the next row |
| Timeout, `5xx`, or `2xx` with a failed assert/capture | Unknown, or yes | Follow-up GET by natural key; **Probe** only if no such read exists |

- **Explore:** change the payload and use a fresh natural key each attempt (`{{newUuid}}` inside the key — **UNVERIFIED:** a documented template function, not in `hurl --help`), so attempts never collide.
- **Probe is only safe on an endpoint confirmed to reject a repeated natural key, or to return the existing record for it** (see the duplicate-create gotcha above): test it once on a non-production environment and record "uniqueness: rejects / returns existing / neither". On a "neither" endpoint a probe creates a duplicate. Match the status plus a loose body check, never exact message text (see Notes).
- **Probe:** resend the **same** natural key exactly once and read the answer. `409`, or `400`/`422` "already exists" → the first attempt landed, nothing new was created. `2xx` with a new id → the first did not persist. `2xx` with the same id → the create is idempotent. Anything else → still ambiguous: stop and report.
- **To wait for state to appear, poll the read, not the write:** send the write once, then put `[Options] retry` / `retry-interval` on a GET entry that reads it. **UNVERIFIED:** `retry` is documented to re-send the entry it sits on, so never put it on a POST/PATCH — confirm on a GET.
- **Autonomous runs:** set an attempt cap (default 3), keep a ledger (attempt, key, status, any visible body — a failed entry writes no `output:` file), stop and report on any ambiguous result, and run only against an environment the run is authorized for. Authorization is the project's, not this skill's.

## Notes

- **Verified 2026-10-07: `hurl --test` sends the requests; it is not a parse check.** To check that a file parses without sending anything, run `hurlfmt --out json <file> > /dev/null`.
- Error strings quoted above are observed behavior, not a stable contract: trust the behavior, treat the exact wording as illustrative.
- This skill covers Hurl syntax/tool behavior, plus the API traps below that a Hurl assert must defend against; general API-testing discipline applies regardless of tool.
- A search filter with a wrong or unsupported name is usually ignored, not rejected: `200` and the full unfiltered set. Prove a filter narrows by comparing `totalElements` with and without it, and read the filtered field back off a returned element (a count check catches an ignored filter but not one that always returns zero). Copy filter names from a confirmed script: a `...IdIn` filter can be ignored where `...IdEqual` is honored.
- A relationship endpoint returning zero results for one candidate ID does not prove the link is broken — that record may simply have no children. State how many candidates you checked and which, and treat "all empty" as a finding only after sweeping several. The same holds for a comparison where both sides are always empty or `0`: it proves nothing about the filled case, so find a row where the value is filled. Empty (absent or null) is not `0`.

## Dependencies

None; routes Hurl-vs-other-tool selection to the `qa-engineer` skill.
