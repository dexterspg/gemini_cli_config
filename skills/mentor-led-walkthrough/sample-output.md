# Sample Output — Required Output Structure Per Method

Concrete worked example of all 10 required steps, in order.
Domain: Python. Method: `put_file` in `StoragePort` (Protocol class).

---

## 1. File Narration *(first method in file only)*

`ports/storage_port.py`

**Business trigger** — Without this, the upload handler would import the Azure SDK directly, which breaks because no upload can be tested without a live Azure account, no local run is possible without one, and swapping backends means editing the same code that holds the business logic.

**What it is** — One file, three method signatures, no logic: `StoragePort`. It is the contract that says: whoever stores files must be able to put bytes in (`put_file`), get bytes out (`get_file`), and delete bytes on request (`delete_file`) — three signatures, three promises, mapped one-to-one onto Azure Blob Storage's own put/get/delete operations.

**Why separate** — It exists as its own file so the upload-handling code never has to know it's talking to Azure specifically; it talks to this abstraction instead, and Azure is just one possible thing behind it.

**Junior trap** — Assuming a `Protocol` class does something at runtime. It doesn't — it only constrains types at check time. The real behavior lives in whichever adapter implements it.

---

## 2. State Briefing

`StoragePort` has no constructor, no instance fields, and no injected objects — it is a `Protocol`. What we are briefing is the contract: three async methods, one responsibility each.

- `put_file` — store bytes, return the location
- `get_file` — retrieve bytes by location
- `delete_file` — remove bytes by location

Any class that implements all three satisfies this contract. `AzureBlobAdapter` will be the first to do so.

---

## 3. Concept Suggestion *(optional — fires when a qualifying mid-session question arises)*

*(Skipped here — no qualifying architectural question arose. When it fires: "Want me to save this to a concept doc?")*

---

## 4. Design Decision *(first method in file only)*

**Business requirement (PRD FR-04):** An admin uploads a file — the system must store those bytes somewhere durable so they survive server restarts. An employee downloads it — the system retrieves those exact bytes.

What breaks if the upload code imports the Azure SDK directly: you can't test an upload without a live Azure account. You can't run locally with a fake file store. You can't swap to S3 without editing the same code that contains your business logic.

**Option A** — import `azure-storage-blob` directly. Zero indirection. But infrastructure and business logic become one entangled thing.
**Option B** — depend on a `Protocol` with three method signatures. Azure in production. A fake in tests. The upload logic never changes when the backend changes.

Going with B — the system is explicitly designed so the storage backend is swappable.

---

## 5. Rounds

### Round 1 — Stub

```python
async def put_file(
    self,
    content_id: str,
    filename: str,
    data: bytes,
    content_type: str,
) -> str: ...
```

Still serving: bytes survive a server restart.

Purpose: accept raw file bytes from the upload handler and return the location string where they were stored.

| Parameter | Type | Meaning |
|---|---|---|
| `content_id` | `str` | Stable identifier for the file (UUID); used to build the blob path |
| `filename` | `str` | Original filename from the upload; preserved for `Content-Disposition` on download |
| `data` | `bytes` | Raw file bytes — content, not a stream |
| `content_type` | `str` | MIME type (e.g. `application/pdf`); passed to storage so download headers are correct |
| **return** | `str` | The blob URL or path; only the adapter knows the format — callers store it opaquely |

Say **continue** when ready.

---

### Round 2 — Happy Path *(Protocol stub — body is the contract itself)*

```python
async def put_file(
    self,
    content_id: str,
    filename: str,
    data: bytes,
    content_type: str,
) -> str: ...
```

`...` is intentional — a Protocol body means "this signature must exist." The implementation is the adapter's responsibility. `AzureBlobAdapter` will provide the real body.

*(Round 3 — Error handling: N/A for Protocol stubs.)*
*(Round 4 — Refactor: N/A — no implementation to clean up.)*

Say **continue** when ready.

---

## 6. Key Insights

`StoragePort` is a promise made in both directions: the upload handler promises to call only these three methods; the adapter promises to implement them. Neither side can drift without breaking the contract at the type level — not at runtime.

---

## 7. Architecture Connection

```
ports/storage_port.py        ← EXISTS (just written)
    StoragePort (Protocol)
        put_file / get_file / delete_file
            ▲ will implement:
            adapters/azure_blob_adapter.py    (not yet written)
```

Nothing calls `StoragePort` yet. Nothing implements it. This is the shared language — a promise the upload logic and the storage backend will honor from opposite sides.

---

## 8. Pattern Tidbit *(optional)*

**Dependency Inversion Principle** — high-level logic must not depend on low-level infrastructure. Both depend on an abstraction. Trade-off: a layer of indirection and a wiring step at startup where the concrete adapter is injected.

---

## 9. Log Writes *(parallel tool calls — same turn, not shown to learner)*

- **Recreation Guide** (`mentor-logs/<date>-mentor-recreate-<slug>.md`): E1 — Created `StoragePort` Protocol with `put_file`, `get_file`, `delete_file` signatures. BEFORE: file did not exist. AFTER: 3 method stubs defined.
- **Build Log** (`mentor-logs/<date>-mentor-buildlog-<slug>.md`): entry for `put_file` — business req (FR-04), Option B design decision, Round 1 parameter table, Round 2 Protocol contract confirmed.

*One completed method = one write to both logs in the same turn. NEVER batch at session end.*

---

## 10. Continue Gate

Say **continue** when ready.
