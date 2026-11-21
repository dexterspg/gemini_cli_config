---
name: mapping-table-artifact
description: >-
  Builds and maintains the editable mapping-tables artifact for a client's interface or field mapping: one tab per interface, the client's own columns locked, Nakisa's columns editable and saved in the artifact's database, a private "My assumption" column that never reaches the shared workbook, column hide and show, and an approved sync into the workbook. Triggers on "mapping tables artifact", "editable mapping table", "mapping page for [client]", "interface mapping tables", "put the mapping in an artifact", "sync the mapping artifact to the workbook". Do NOT use for deciding what a field maps to (mapping-workflow), the report finder (report-field-mapping), or a read-only table (plain artifact).
---

# Mapping-table artifact

A private artifact page that holds a client's mapping tables as live, editable data. Built from `references/mapping-table-template.html`; every behaviour below is already in the template, so a new page has all of it by default. Load `artifact-capabilities` first (the page declares `db` and `user`).

## Build

1. Artifact tool `quickstart` (intent `other`), then copy the template to the scratchpad and fill the two placeholders: `{{CLIENT}}` (the client's name; escape an apostrophe inside the JS strings) and `{{SHEETS_JSON}}` (for example `["T92", "T93"]`). Change nothing else unless the user asks.
2. Publish with `capabilities: {"db": {}, "user": {}}`, an icon, and a one-sentence description. Later republishes omit `capabilities` (they carry forward).
3. Seed the data with `ArtifactData` `batch` (50 writes at most, `file_path` per entry for long text), then tell the user it is private until they share it.
4. A style or behaviour change is made in the page's file and republished; do not touch the data code (`save`, snapshots, `changed`) when restyling. Check the script parses before publishing: extract it and run `node --check`.

## Data

- `rows/<SHEET>-<NN>`: `{sheet, n, apple: [[column, value], ...], ctx: [[key, value], ...], nakisa: {endpoint, field, status, confirms, comment, assumption}, synced: {endpoint, field, status, confirms, comment}}`. The key is named `apple` for historical reasons: it holds the client's own columns, word for word from its specification, never edited.
- `meta/about`: `{items: [[title, text]], interfaces: [[name, text]]}`; `meta/sync`: `{at, note}`.
- `synced` is what the shared workbook holds at the last sync. A cell is "changed" when `nakisa` differs from `synced`. `assumption` is outside `synced` on purpose.
- Every write pins `if_version` from a read. Read many rows with `list`/`query` and `out_dir`, then edit by script.

## What the page does (the default feature set)

- A bright, single light theme (white page, saturated blue client headings, green Nakisa headings, violet private column, yellow changed cells).
- One tab per sheet from the hash (`#T92`), plus an About tab; tab counts; stats line; search (includes My assumption); filter: all, no Nakisa field yet, has a Nakisa field, changed since the last sync.
- Client columns locked on the left, first column sticky; Nakisa columns editable: endpoint, field, status (As is / Not used / To decide / Agreed), "Client confirms", comment; auto-saving.
- **My assumption**: a private working column, only on the page, never copied to the workbook. Say so in the page text.
- Headings follow the page scroll (a pinned copy of the heading rows); text boxes grow with their text, so nothing scrolls inside a cell.
- Hide and show whole columns: a × on each heading and a "Columns" menu with a count and "Show all columns"; the first column cannot be hidden; the choice is kept per viewer in the browser only (never in the data).

## Sync into the workbook

Only when the user asks. Show the differences against the workbook first (cell, old value, new value) and write only what the user approves. Sync only `endpoint`, `field`, `status`, `confirms` and `comment`; never `assumption`. After a write, set the matching `synced` cells and `meta/sync`. Never fill the client's own confirmation column. Moving text out of `comment` into `assumption` shows as a pending change against `synced`: say so.

## Local version (survives a lost page)

Artifact pages have been lost with their data. Keep the rows in a local JSON file with the client's notes (`{Client}/work/mapping-tables/rows.json`; the shape is in the header of `api-test-app/recon/mapping_page.py`) and run the same page locally: `python recon/mapping_page.py --data <rows.json> --open`. It serves the template here on 127.0.0.1 and saves every edit into the file; `python recon/test_mapping_page.py` checks it. A client's `client_api` ignores `*.json`: keep the file untracked or store it another way, never force-add without asking. When both the artifact and the file exist, the file is the copy to trust.

## Content rules

- A comment or status that the client will see states only what Nakisa proposes and what it needs confirmed: no internal ticket numbers, ids, test names, other clients or Nakisa design. Internal reasoning goes in My assumption.
- **Comment = confirmed facts. My assumption = everything not confirmed.** Never mix them in one cell. When a spec has paired interfaces (a send file and a return file), each row gets its own comment: never combine them. Say "Nakisa sends" or "Nakisa holds", never "the middleware derives". Do not edit a comment the user wrote unless told; do not save drafted text until the user approves or words it.
- **Comment order**, using only the parts the row needs (a self-explanatory field gets one line, "Map X to the company display id of the journal"):
  1. What Nakisa lacks or has ("Nakisa has no X field").
  2. What the client's own term is, when not obvious.
  3. "Map X to [plain meaning], [exact Nakisa path]". If Nakisa has no matching field, give the alternative.
  4. A format or example value (a date without time such as 2024-01-01; 10 digits).
  5. The rule that decides the value (the sign of an amount; debit positive, credit negative).
  6. What happens when it is blank.
  7. Where it applies (which interface or variant) and where it does not.
  8. The look-alike field it is not.
  9. A pointer to the related row ("see PK") instead of repeating it.
- **My assumption**: a plain-words question or open point; what Nakisa can do today, then the gap; the options as a direct question; labels "Not confirmed:", "Alternative, not tested:", "To confirm with the client:"; run evidence with its date and "(source read, not run)" where that is the case; the ask last ("Please confirm X").
- Status says whether anything must change: "As is" (Nakisa already gives the value in the form the client needs), "Not used" (the client's spec does not use the field), "To decide" (a format change, a set-up or a missing equivalent to settle), "Agreed" (only after the client confirms). Do not mark more than the evidence supports (see `mapping-workflow` for the proof rules).
