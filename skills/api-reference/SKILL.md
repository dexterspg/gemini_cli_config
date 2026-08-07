---
name: api-reference
description: >
  Governs creation of API reference files that bridge an external public REST API
  with internal implementation and domain concepts.
  Triggers on: "document [product] API", "create API reference for [endpoint]",
  "map [endpoint] to internal code", "add [resource] to api reference",
  "reconcile API docs", "check API drift", "write API docs for [resource]".
---

# API Reference Skill

**Purpose:** Produces markdown API reference files that link three layers:
external public REST contract → internal implementation → domain concept.

**Output location:** `{project-root}/api/{product}/{version}/{resource}.md`
Exact product names, version labels, and external docs URL are defined in the
project supplement — see Project Configuration below.

## Never:
- Document internal-only endpoints not published externally — use `documentation-specialist`.
- Teach how an API works conceptually — use `agent-concept-tutor`.
- Document domain concepts without an API anchor — use `domain-knowledge`.
- Embed internal implementation details in the file body — link only, never inline.

## Project Configuration (MANDATORY — load before any workflow)

Check for a project-level supplement at `{project-root}/.claude/skills/api-reference/SKILL.md`.
If it exists, load it first — it defines:
- External docs base URL
- Product names and folder mapping
- API version(s) in use
- Any project-specific rules that extend or override this skill

If no supplement exists, ask the user for the external docs URL and product names before proceeding.

## Routing Index

| Trigger | Action |
|---|---|
| "document [product] API", "add [resource] to api reference" | New Endpoint Workflow |
| "reconcile API docs", "check API drift" | Reconciliation Workflow |
| "map [endpoint] to internal code" | New Endpoint Workflow — skip WebFetch step |

## Orchestration Model

1. **Claude (Main Session):** Fetches external docs via WebFetch, orchestrates, writes the final file.
2. **agent-codebase-archaeologist:** Traces the endpoint to its internal controller and service.
3. **Claude (Main Session):** Resolves applicable `knowledge/` concept and applies the link contract.

## Folder Structure

```
api/
├── _common/              # Cross-product: authentication, pagination, error codes, webhooks
├── {product}/
│   └── {version}/        # e.g. v1/, v2/ — add version folders as published
│       └── {resource}.md # one file per resource group
└── README.md             # index of all documented products and resources
```

Product names and version labels are defined in the project supplement.

## Mandatory Link Contract

Every endpoint file MUST carry all three links. A file without all three is incomplete.

```
Implementation: documentation/projects/{service}/domain/{file}.md#{section}
Applies concept: knowledge/{domain}/{concept}.md
last-verified-against-source: YYYY-MM-DD
```

- No applicable concept → write: `Applies concept: none identified`
- Implementation not yet traced → write: `Implementation: untraced — pending`

## File Template

```md
---
product: {product}
version: {version}
last-verified-against-source: YYYY-MM-DD
external-ref: {external-docs-url-for-this-resource}
---

# [Resource Name] — [product] [version]

**What it does:** [1-2 sentence plain-language description.]

**External reference:** [URL]

---

## Endpoints

### [METHOD] /api/{version}/path

**Description:** [One sentence.]

**Query Parameters:**
| Param | Type | Required | Description |
|---|---|---|---|

**Request Body:**
```json
{}
```

**Response 200:**
```json
{}
```

**Error Responses:**
| Status | Code | When |
|---|---|---|

---

## Implementation
- **Controller:** `[ClassName#methodName]` → [link to documentation/projects/{service}/domain/]
- **Service:** `[ServiceClass#method]`

## Applies Concept
- [Concept Name] → [link to knowledge/{domain}/]
```

## New Endpoint Workflow

1. **Load supplement** (Main Session): Read project supplement for external docs URL and product config.
2. **Fetch** (Main Session via WebFetch): Fetch the relevant external docs page. Extract paths, parameters, request/response shapes.
3. **Trace** (agent-codebase-archaeologist): Find the controller and service handling the endpoint.
4. **Link concept** (Main Session): Check `knowledge/` for an applicable concept. Apply link contract.
5. **Write** (Main Session): Create or update `api/{product}/{version}/{resource}.md` using the template above.
6. **Register** (Main Session): Ensure `api/README.md` has a row for this file.

## Reconciliation Workflow

1. **Select** (Main Session): Find files where `last-verified-against-source` is > 3 months old or blank.
2. **Fetch** (Main Session via WebFetch): Re-fetch the external docs page for that resource.
3. **Trace** (agent-codebase-archaeologist): Verify controller/service mapping is still accurate.
4. **Update** (Main Session): Apply changes and bump `last-verified-against-source`.
5. **Repeat** until all files are current.

## Rules

1. **One file per resource group** — top-level REST resource only (e.g., `/contracts`, `/invoices`).
2. **Public contract only** — file body reflects the external API contract. Internal details live in `documentation/`; concept background in `knowledge/`. Link; never embed.
3. **`_common/` for cross-product concerns** — authentication, pagination, error codes, and webhooks are documented once in `api/_common/` and linked from all product folders.
4. **Drift stamp is mandatory** — `last-verified-against-source` must be updated on every edit. Re-verify at >3 months; mark stale at >6 months.
5. **Reference direction** — `api/` may link into `documentation/` and `knowledge/`. Neither `documentation/` nor `knowledge/` links back into `api/`.
6. **Project supplement takes precedence** — any rule in the project supplement overrides the matching rule here.
7. **Skill meta-management:** Direct edits to this skill file may be made without confirmation when the user gives explicit instruction.

## Notes

- If external docs return 404 or require auth: write `external-ref: unavailable` and document from source code only.
- If an endpoint has no external API page (internal-only): do not create a file here — use `documentation-specialist`.
- If no applicable `knowledge/` concept exists: write `Applies concept: none identified` — do not leave blank.
