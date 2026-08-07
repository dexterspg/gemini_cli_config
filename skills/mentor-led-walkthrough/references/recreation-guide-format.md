# Recreation Guide — Format Reference

A third artifact — distinct from both the journal and Build Log. Created when the learner says "I want to be able to recreate this", "track how this was built live", or "give me a step-by-step guide to rebuild this."

**Purpose:** A chronological event log of the build — answering questions like "what existed before X was added?", "when was Azure set up?", "what did file Y look like before Z was changed?". Written so an AI can reenact the build sequence from it — like a crime scene reconstruction. **NOT a code dump per section.**

**File:** `{project-root}/mentor-logs/<YYYY-MM-DD>-mentor-recreate-<artifact-slug>.md`

## Structure

1. **File version index** — table mapping every file to which events created and changed it
2. **POSITION INDEX** — quick-navigation map updated after every event (see format below)
3. **Numbered event timeline (E1, E2, ...)** — in exact build order, one event per meaningful action. Includes:
   - Code events: file created or file changed
   - Infrastructure events: Azure setup, external service config, API key creation — first-class events, not footnotes
   - Stub events: explicitly note when a file was created as a stub and name the later event that implemented it
3. **Dependency graph** — shows which events depended on which (build reading order), as an ASCII diagram

## POSITION INDEX format

```
| Slice | File | Events | Status |
|---|---|---|---|
| S1 — Upload | ports/storage_port.py | E1 | done |
| S2 — Metadata Catalog | adapters/sqlite_metadata_adapter.py | E2-E4 | done |
| **CURRENT** | **services/document_service.py** | **E5** | **[active]** |
```

**Column semantics:**
- **Slice**: slice number and label (e.g. `S3 — Download`)
- **File**: relative path to the source file
- **Events**: single event (`E5`), consecutive range (`E2-E4`), or comma-separated non-consecutive (`E3, E7`)
- **Status**: `done` for completed rows; one `**CURRENT**` marker row at the bottom — bold-formatted, marks the active slice/file/method
- **Update timing**: rewrite the `**CURRENT**` row after every event write, in the same turn as the log entry

---

## Event format
```
### EN — <file name or infrastructure action>
**Date:** ~YYYY-MM-DD (use "unknown" if date cannot be estimated)
**Type:** Code | Infrastructure
**Requirement:** the business trigger this event serves — in Mode B, the derived trigger carrying its (derived from code — no spec: <file>:<line>) tag

**Added/changed:** (method names, key logic in plain language — no full code bodies)
**Why at this point:** (what prerequisite existed; what would have broken without this)
**State after:** (what the system can now do that it couldn't before)

[For files modified after their creation event:]
**BEFORE (EN-X):** what the file could/could not do
**AFTER:** exactly what changed (new params, new calls, removed stubs)
```

## Example
```
### E13 — document_service.py (upsert added)
**Date:** ~2026-07-15
**Type:** Code

**Added/changed:** `upsert_document(file, content_type, user_id)` — calls StoragePort.upload(), IndexPort.upsert(), MetadataPort.save()
**Why at this point:** StoragePort (E5), IndexPort (E10), and MetadataPort (E4) all existed; upload route (E12) needed a service method to call
**State after:** full upload pipeline complete — blob stored, vector indexed, metadata saved

**BEFORE (E8):** `document_service.py` had `get_document()` and `list_documents()` only — no indexing, no blob storage calls
**AFTER:** `upsert_document()` added; all three ports wired together in one service call
```

## Rules
- Never paste full method bodies — describe what each method does and why it exists
- Infrastructure events (Azure portal steps, Azurite, Anthropic key) belong in the timeline as events, not as footnotes or prerequisites sections
- Every modified file must record its BEFORE state — a reader must be able to answer "what was document_service.py before upsert was added?" without reading old git commits
- Stub files get two events: one when the stub was created (raise NotImplementedError), one when it was implemented — both use `Type: Code` and record what existed at that moment
- Reference runbooks for cloud config steps; never inline them
- File renames and deletions are events too — record old name, new name (or "deleted"), and why
- **Every file write is followed immediately by a recreation guide event in the same turn** — never batch multiple writes into one deferred event at session end; one write = one event (or one event per file if a section touches multiple files)
- **FILE VERSION INDEX has one row per file** — when adding a new event for an existing file, update the original row's "Changed at" column; never append a duplicate row at the bottom
