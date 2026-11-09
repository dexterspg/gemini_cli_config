# Mapping Workflow

Maps every field of a subject to the API endpoint and response field that carries it. The subject is an Excel report's columns, or an integration payload: the fields of an RFC or BAPI trace, or of a flat-file layout. Not a data migration: values are evidence that a mapping is right, never something to move. This file owns the method; a project supplies its paths, tools and exact vocabulary.

**Dependencies:** the project's mapping supplement. In `api-test-app`: `{project-root}/.gemini/skills/report-field-mapping/SKILL.md` (or `.claude/skills/report-field-mapping/SKILL.md` — finder paths, the closed vocabulary strings, the lint, the scripts, the artifact build) and the Hurl and core2 skills it names. Absent: stop and ask. For a report not mapped before, read the supplement's `references/discovery-playbook.md` before Source trace and pass its `references/source-trace-brief.md` to the trace subagent.

**Start here:** open the report's section in the project's finder (api-test-app: `docs/report-field-finder.md`); the next action is the first step whose gate is not met. No section yet: start at Intake.

## Flow

| Step | What happens | Owner | Gate |
|---|---|---|---|
| 1 Intake | report, parameters, what done means; classify the subject with the Subject types table | main session with the user | the project's non-client environment and key only (api-test-app: preview1, plain `API_KEY`); a client's key or environment is outside this workflow |
| 2 Headers | download one report and read the exact headers; a report with no download flow gets one built first | main session runs the confirmed flow; it creates a job, so the project's run rule applies (api-test-app: `GEMINI.md` / `CLAUDE.md` "Hurl Run Structure") | the header list and count are copied from the workbook |
| 3 Source trace | the report's row class and query, one row per column | agent-codebase-archaeologist, with the core2 brief block and the supplement's trace brief | one row per header; a partial table means stop |
| 4 Grain and sample | state what one row is and which rows are compared, with the case each covers | main session drafts from the trace's "rules to decide", user confirms | `Row grain:` and `Sample:` lines in the section |
| 5 Probe | one probe flow reads a record through each endpoint and asserts each field present, or absent with the filter that shows why (api-test-app: a Hurl flow) | main session writes and runs it (read-only on the test environment needs no yes) | each flow `CONFIRMED` |
| 6 Compare | a script rebuilds the columns from the endpoints and compares them with the report (Rules) | main session writes a new report's script from the pattern and re-runs existing ones | the project's `--run` exits 0 and records its output |
| 7 Second sample | a column compared only as empty or zero gets a filled record | main session | a filled comparison, or "filled case not proved" with the filter and its total |
| 8 Assemble | write the finder rows from the trace and the run output; register the report in the project's one registry (api-test-app: lint `REPORTS`); run the checks; stamp each script | main session | the checks pass |
| 9 Review | agent-quality-guardian, given only the path of the subject's section in the project's finder (not the rules: they anchor its findings), then the main session checks the finder against this workflow's "Rules" and the supplement's closed vocabulary and lint, where it defines them; the adversarial-review skill only for a new kind of evidence | as named | APPROVED |
| 10 Publish | Markdown first, then the artifact built from it | main session | the commit that passes the checks; a client deliverable also needs a separate run with the client's key under the project's client-environment rule (api-test-app: `GEMINI.md` / `CLAUDE.md` "Client Environment Safety"), and client confirmation lives only in the migration `FIELD_MAPPING.md` |
| 11 Change control | after a source pull or a report change, re-run the project's health set of probe flows and the comparison scripts for the changed classes, then restamp; a report change restarts at Headers | main session | the stamp matches the scripts, the mapping and the workbooks |

## Subject types

Step 1 picks one row. The subject type changes what Headers, Source trace, Grain and Compare read; it adds no step and no gate. Read only your row.

| Subject | Field list comes from | Extra columns to capture | Grain and cardinality | Compare | Top trap |
|---|---|---|---|---|---|
| Excel report | the headers of a downloaded workbook | none beyond the finder's | what one report row is | yes, as written in Rules | a computed cell rounds per line or on the sum: record the rule |
| JSON / OData response | the response schema, or a recorded response | JSON path, entity set, navigation property of each 1:N child | one row per field; a 1:N child names its parent key | yes, on records from one environment | a missing `$select` or `$expand` reads as empty: say which |
| SAP BAPI / RFC trace | the parameters the trace sends (import, export, changing, table-typed) | parameter, structure field, ABAP type and length, conversion exit, parent key of each table | one table per parameter; a 1:N table states its parent key (EBELN+EBELP) | only against a trace from the same environment | success is no `E` or `A` in RETURN (`A` aborts the whole unit); the contract names who commits or rolls back; CURR decimals come from the currency (TCURX), NUMC is zero-padded, DATS `00000000` is empty |
| Flat file | the layout spec, never a sample file | delimited: position, delimiter, quote, encoding. Fixed-width: start, end, length, padding, justification, sign position, implied decimals, end of line | one row per field; a record-type column when header and detail rows mix | only with a sample file from the same run; otherwise skipped as under Integration payload | empty, zero and spaces are three values |
| IDoc / EDI | the basic type and its segment layout | segment path, qualifier value (QUALF), segment hierarchy | one row per segment field, per qualifier | not probed read-only: skipped as for a flat file with no same-run sample | one segment type carries different fields by qualifier. Not yet exercised on a real subject |

- **Mixed or unclassifiable.** A subject that spans rows (a report fed by a flat file) splits into one subject per row, each through the flow. An unclassifiable subject: ask the user; add a row only after one real subject has passed.
- **Lookups.** A value translated between source and target (enum, unit, currency, code to label) gets its own lookup rows: source value, target value, where each was read. A SAP field that maps to a different concept in the API (a key, a unit) goes through the lookup and the concept table, never straight across.
- **Example row (BAPI table):** `PO item quantity | PO_ITEMS.QUANTITY | QUAN 13,3 | parent EBELN+EBELP | <items endpoint> -> items[].quantity | CONFIRMED | matched n of m, filled k`.
- **Workbook for a client's own layout (flat file, or any structure the client specifies).** Two approaches; verbatim is the default.
  - **Verbatim (default).** Use the client's own column headers (each table's own, such as Field or Field Header in File), field names, descriptions, SAP fields, types, lengths, extra columns and remarks, word for word and in the client's row order. One row per client field: split a row the client splits, never merge, never rename. Keep the client's typo and note it in the Assumption column. Our words go only in our columns (Nakisa endpoint and field, Assumption, status), never in the client's. Where the client's structure is already clear, this is the only approach.
  - **Our own structure** only when the client gives no structure or it cannot be read as a mapping. Say so on the Read me and mark every description as ours.
  - **Layout.** The Nakisa columns start after the client's, with the client's Remarks last of its side; freeze panes just before the first Nakisa column. A shared file carries no internal tracker ids (point or ticket numbers).
  - **Check before delivery.** Compare every client-column cell with the spec text, ignoring spacing and keeping case, and the row count with the spec's. A cell the spec splits over a page break is read by eye. Authoring-time only.

## Integration payload

The flow and Rules above apply except where this section says otherwise; "report", "column" and "finder" read as the payload, its fields and the project's payload map.

- **Start here:** the project's payload map. **Headers:** the field list is what the trace or layout sends, never the target's echo, which lists every field with defaults. **Source trace:** where the payload's mapping table and builder code set each field, and the public response path that carries the same value. **Grain:** one row per payload field, one table per structure; a 1:N child names its parent key.
- **Compare** only against a trace taken from the same environment as the records read. Until one exists: no compared column, the trace's values are examples, and Second sample, the comparison-script rule and the drift guard are skipped.
- **Views beyond the field table.** A concept table for every value read at two or more stages (setup, contract, posting, reporting): the field name at each stage, the join key and the system of record. Two names are one concept only when one probe flow asserts the same id at each stage; join on that id or a natural key pair, never a display value alone. One scenario view per direction the data moves (in, out, out and back): call order, what each call returns, the write-back, and an interface contract (unit, how records not yet sent are selected, paging and rate limit, idempotency key, status states with where each was read, write-back, the key a reversal needs, errors and partial failure (BAPI/RFC: RETURN severity, success is no E or A, who commits or rolls back), batch and schedule, credential expiry, which environment matches production, owner). Authoring-time only.
- **Columns beyond the report's.** An input that changes or removes a value without being it (a category, a flag, a setting) goes in its own column. A target field's type, length, required flag and format come from the target system's own specification; none in hand means the cell says so. Authoring-time only.
- **Gap sweep** (after Source trace, again at Assemble; Publish lists what stays open). Every scenario step, contract item or target-spec cell with no doc, source read or flow behind it becomes a row `G<n>` in the payload map: Gap | Class | Route | Record | Blocks (Y/N).

  | Class | Route, in order |
  |---|---|
  | Contract: endpoint, filter, link, paging, write-back | vendor doc, test-environment probe (api-test-app: under its GEMINI.md/CLAUDE.md run rules), core2 read; still none → R&D question (jira `fco` → "Support Request") |
  | Access: credential expiry, environment parity | `ncp-api-access` |
  | Target spec: type, length, format | the colleague holding the spec; Record names who and the date asked |
  | Client input: layout, schedule, volume, same-environment trace | client question (api-test-app: `client-requirements` Q entry naming the map path and gap id); the map row says "client", never a client id |
  | Concept unproved across stages | probe flow |

  A row closes only on a `CONFIRMED` flow, an answered FCO key, a cited spec or a recorded client answer; a value seen once on test data never closes a contract item.

## Rules

- **Mapped** means findable through an endpoint, even when empty on this data; the filled case stays unproved until compared. The live-response check and the compared-with-the-report check are two columns, each with a closed vocabulary; a "matched" cell carries n of m and the filled count. Empty is not zero.
- **A claim comes from output, not inference.** Every finder row must have its own line in the comparison script's recorded output; a column the script does not compare is listed as missing (api-test-app: `lint_field_mapping.py --coverage`), never marked matched. A "not found" claim names its filter and total, or its sample size.
- **A comparison script** finds columns by header name, matches each source row to at most one report row, keeps empty apart from `0`, reports every unmatched or unbuildable row, samples the rarest combination of the report's own cells first, and exits non-zero on any difference. A cell that cannot be rebuilt from one row (a cache, an order effect) is checked for what can be checked and the rest is counted, never called matched. Total and subtotal rows are excluded by a stated rule or compared as their own rows; a computed numeric cell records its rounding rule (per line or on the sum).
- **Drift guard.** A mapping change moves the finder row, the comparison script and the probe flow together. Record a hash of the script (and the modules it imports), of the mapping columns, of every cell and of the workbooks at the last passing run; the check fails while any differs, until the script is re-run and restamped.
- Guardian REVISION_NEEDED -> the owner of the failing step (max 2); BLOCKED, or a third revision -> stop and ask the user.
- Compare finds DIFFERENT -> a script bug goes back to Compare; a row-matching or grain error goes to Grain and sample, then Compare; a trace error goes to Source trace (max 2 each). A real difference between the API and the report is written to the resource's discrepancy file, the cell stays `DIFFERENT`, nothing loops, and the user decides defect or acceptable.
- A subagent that returns nothing is retried once, then the main session reports it and stops.
