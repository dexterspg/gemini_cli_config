# Reference: L1–L3 Second Brain Schemas & Token-Budgeted Retrieval Templates

Load on demand from `second-brain/SKILL.md` (Action 2: Low-Token Ingestion & Action 3: Budget-Capped Retrieval).

---

## 1. Local File-Based Second Brain Layout (`{project-root}/second-brain/`)

```text
{project-root}/second-brain/
├── _ROUTER.yaml                  # L1: Domain registry (<10 tokens per domain)
├── <domain-a>/
│   ├── _CATALOG.yaml             # L2: Entity & tag index (<15 tokens per entry)
│   └── facts.yaml                # L3: Atomic YAML micro-facts (15–50 tokens per fact)
└── <domain-b>/
    ├── _CATALOG.yaml
    └── facts.yaml
```

### L1: `_ROUTER.yaml` Schema
```yaml
version: 1
updated_at: "YYYY-MM-DD"
domains:
  database:
    scope: "RDBMS tuning, connection pooling, indexing, migrations"
    fact_count: 14
    catalog_path: "database/_CATALOG.yaml"
  auth:
    scope: "OAuth2, JWT lifetimes, RBAC policies, session storage"
    fact_count: 9
    catalog_path: "auth/_CATALOG.yaml"
```

### L2: `<domain>/_CATALOG.yaml` Schema
```yaml
domain: database
entries:
  - id: fact-pg-memory-001
    entity: PostgreSQL
    attribute: memory_tuning
    tags: [postgres, memory, pgbouncer, oom]
    tokens: 26
  - id: fact-pg-index-002
    entity: PostgreSQL
    attribute: jsonb_gin_indexing
    tags: [postgres, jsonb, gin, indexing]
    tokens: 31
```

### L3: `<domain>/facts.yaml` Schema
```yaml
- id: fact-pg-memory-001
  entity: PostgreSQL
  attribute: memory_tuning
  tags: [postgres, memory, pgbouncer, oom]
  token_count: 26
  source_ref: "{project-root}/docs/db-tuning.md#L12-L24"
  compressed_fact:
    shared_buffers: "25% of total RAM"
    work_mem: "64MB/conn"
    pooler: "PgBouncer"
    failure_mode: "OOM during high-concurrency sort"
```

---

## 2. Progressive-Disclosure Retrieval CLI Commands (`rg`)

Execute these commands in order during Action 3 to guarantee minimal token consumption:

1. **Step 1 — Read L1 Router (~50 tokens):**
   Read `{project-root}/second-brain/_ROUTER.yaml`.
2. **Step 2 — Filter L2 Catalog by Tag/Entity (~30 tokens):**
   `rg -n -C 3 "<entity_or_tag>" {project-root}/second-brain/<domain>/_CATALOG.yaml`
3. **Step 3 — Fetch Target L3 Fact Block by ID (~25–50 tokens):**
   `rg -n -A 10 "id: <fact-id>" {project-root}/second-brain/<domain>/facts.yaml`

---

## 3. Database-Backed Hybrid Retrieval & Budget Packer (Python Reference)

```python
from dataclasses import dataclass

@dataclass
class PackedContext:
    yaml_payload: str
    tokens_used: int
    fact_ids: list[str]

def pack_token_budget(candidates: list[dict], max_tokens: int = 300, min_score: float = 0.65) -> PackedContext:
    """Packs reranked atomic facts into a compact YAML string within a strict token cap."""
    used = 0
    lines = ["knowledge_context:"]
    included_ids = []

    for item in sorted(candidates, key=lambda x: x["score"], reverse=True):
        if item["score"] < min_score:
            continue
        cost = int(item["token_count"])
        if used + cost > max_tokens and included_ids:
            break
        lines.append(f"  {item['entity']}.{item['attribute_key']}: {item['compressed_fact']}")
        used += cost
        included_ids.append(item["id"])

    return PackedContext(
        yaml_payload="\n".join(lines),
        tokens_used=used,
        fact_ids=included_ids
    )
```
