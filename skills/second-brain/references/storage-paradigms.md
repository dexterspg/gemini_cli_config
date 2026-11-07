# Reference: Scalable Criteria & Knowledge Storage Paradigms

Load on demand from `second-brain/SKILL.md` (Action 1: Architecture & Criteria Strategy Selection).

---

## 1. Workload Classification Matrix

### A. Criteria & Rule Storage (Forward vs. Inverse Matching)

| Paradigm | Forward Lookup (Group ID → Rules) | Inverse Matching (Event → Matching Groups) | Scale Ceiling | Best Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Relational Normalized** | 5–20 ms (join-bound) | >500 ms (poor) | <100K predicates | Strict ACID audit policies, low-frequency evaluation. |
| **PostgreSQL JSONB + Flattened Index** | **<1 ms** (B-Tree) | 5–30 ms (GIN / Compound Index) | <1M groups | Multi-tenant SaaS dynamic filters, nested boolean ASTs. |
| **Elasticsearch / OpenSearch Percolator** | 5–15 ms | **2–10 ms** (100K+ rules) | Billions (clustered) | Real-time alerting, document routing, fraud rules with range/text. |
| **In-Memory Roaring Bitmaps** | **<0.1 ms** | **<0.05 ms** (AVX-512 bitwise) | ~10M groups (2–8 GB RAM) | High-concurrency ad targeting, feature flags, categorical matching. |
| **RETE / Phreak (Drools)** | <1 ms (in-memory) | 1–10 ms (stateful joins) | Heap-bound | Multi-entity cross-joins, stateful temporal workflows. |

### B. Knowledge Storage (Token Density & Retrieval Precision)

| Paradigm | Retrieval Latency (p99) | Prompt Context Footprint | Ingest Cost | Scale Ceiling | Best Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Flat Vector Chunks** | 15–50 ms | 500–2,500 tokens (High noise) | Very Low | $10^7$ chunks | Unstructured prose prototypes. |
| **Hierarchical Tree (RAPTOR)** | 40–120 ms | 150–400 tokens | Medium-High | $10^6$ docs | Multi-resolution thematic + granular Q&A. |
| **SPO Knowledge Graph / Triples** | 20–80 ms | **20–100 tokens** | High | $10^8$ edges | Entity relationships, lineage, dependency resolution. |
| **L1→L2→L3 Metadata Catalog + YAML** | **<5 ms** | **15–150 tokens** | Low-Medium | $10^9+$ rows | Engineering specs, configurations, domain rules, second brain. |
| **Hybrid (BM25 + Vector + Reranker)** | 50–150 ms | 100–300 tokens (pruned) | Medium | $10^8$ docs | Technical corpora mixing error codes, identifiers, and prose. |

---

## 2. Production Hybrid Schema: Criteria + Knowledge (PostgreSQL + pgvector)

### A. Criteria Groups & Inverse Predicate Index

```sql
CREATE TABLE criteria_groups (
    group_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id      UUID NOT NULL,
    group_name     VARCHAR(100) NOT NULL,
    version        INT NOT NULL DEFAULT 1,
    root_logic     VARCHAR(3) NOT NULL CHECK (root_logic IN ('AND', 'OR')),
    ast_document   JSONB NOT NULL,
    is_active      BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX idx_criteria_groups_tenant ON criteria_groups (tenant_id, is_active);
CREATE INDEX idx_criteria_groups_ast ON criteria_groups USING gin (ast_document jsonb_path_ops);

CREATE TABLE criteria_predicates_index (
    predicate_id   BIGSERIAL PRIMARY KEY,
    group_id       UUID NOT NULL REFERENCES criteria_groups(group_id) ON DELETE CASCADE,
    field_name     VARCHAR(64) NOT NULL,
    operator       VARCHAR(16) NOT NULL,
    string_value   VARCHAR(255),
    numeric_value  NUMERIC(15, 4),
    is_negated     BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_pred_string_lookup ON criteria_predicates_index (field_name, operator, string_value) INCLUDE (group_id);
CREATE INDEX idx_pred_numeric_lookup ON criteria_predicates_index (field_name, numeric_value, operator) INCLUDE (group_id);
```

### B. Atomic Knowledge Nodes Table

```sql
CREATE TABLE knowledge_nodes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain          VARCHAR(64) NOT NULL,
    entity_name     VARCHAR(128) NOT NULL,
    attribute_key   VARCHAR(128) NOT NULL,
    source_prose    TEXT NOT NULL,
    compressed_fact TEXT NOT NULL,
    token_count     INT NOT NULL,
    tags            TEXT[] NOT NULL,
    search_tsv      tsvector GENERATED ALWAYS AS (to_tsvector('english', entity_name || ' ' || attribute_key || ' ' || compressed_fact)) STORED,
    embedding       vector(1536)
);

CREATE INDEX idx_kn_domain_entity ON knowledge_nodes (domain, entity_name);
CREATE INDEX idx_kn_tags ON knowledge_nodes USING GIN (tags);
CREATE INDEX idx_kn_tsv ON knowledge_nodes USING GIN (search_tsv);
CREATE INDEX idx_kn_embedding ON knowledge_nodes USING hnsw (embedding vector_cosine_ops);
```

---

## 3. Advanced Scaling Mitigations

- **Continuous Numeric Ranges in Bitmaps:** Bucketize into tiers (`[0-1k, 1k-10k]`) or combine Roaring Bitmaps (categorical) with an in-memory Interval Tree / Lucene BKD Tree (numeric ranges).
- **Zero-TTL Cache Invalidation:** Never rely on TTL alone for criteria or critical facts. Maintain an in-memory map `group_id -> version` (ETag generation number) and invalidate L1 local cache immediately on version bump.
- **Maximal Marginal Relevance (MMR):** Penalize near-duplicate retrieved facts before context packing:
  $$\text{MMR} = \arg\max_{d_i \in R \setminus S} \left[ \lambda \text{Sim}_1(d_i, Q) - (1-\lambda) \max_{d_j \in S} \text{Sim}_2(d_i, d_j) \right]$$
