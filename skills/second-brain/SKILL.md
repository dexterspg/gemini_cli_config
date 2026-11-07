---
name: second-brain
description: "Architects, ingests, indexes, and retrieves knowledge and criteria at scale with minimal LLM token consumption and sub-second lookup. Use this skill whenever the user wants to manage a second brain, compress notes into atomic micro-facts, build a hierarchical routing index, design scalable criteria/rule storage, or retrieve knowledge within a strict token budget. Triggers on: \"second brain\", \"store knowledge efficiently\", \"low token knowledge\", \"compress into micro-facts\", \"atomic facts\", \"build knowledge index\", \"retrieve with minimal tokens\", \"scale knowledge base\", \"criteria storage strategy\", \"percolate rules\", \"how should I store these rules\", \"query second brain\"."
---

# Second Brain & Low-Token Knowledge Skill

Role: Knowledge architect and token-budgeted retrieval engine managing high-scale, low-token knowledge bases and criteria stores.

Purpose: Eliminate context-window bloat by storing knowledge as multi-tier indexed micro-facts (L1 Domain Router → L2 Topic Catalog → L3 Atomic YAML Triples) and selecting optimal storage/retrieval paradigms as data scales from tens to millions of items.

---

## Capabilities

- Select optimal storage and retrieval architectures based on query mode (Forward Lookup vs. Inverse Matching) and scale.
- Decompose verbose documents into dual-layer storage: compact YAML micro-facts (L3) and lightweight routing catalogs (L1/L2).
- Execute progressive-disclosure retrieval capped at a strict token budget (default ≤ 300 tokens).
- Audit and compact existing markdown knowledge bases to eliminate narrative bloat and near-duplicate chunks.

## Never

- Never dump raw unindexed prose files into the LLM context when an atomic fact suffices — `second-brain` enforces progressive disclosure.
- Never overwrite or modify full-fidelity pedagogical lessons in `C:/workarea/notebook/` — `agent-note-taker` owns full-fidelity notebook capture.
- Never write project-specific ADRs, dead ends, or operational runbooks — `engineering-journal` owns project institutional logs.
- Never teach domain concepts from scratch — `agent-concept-tutor` owns pedagogical explanations.
- Never read or write `40-references/` — `import-docs.py` owns reference imports.

## Dependencies

- MANDATORY: Load `C:/Users/dpagkaliwangan/.gemini/skills/second-brain/references/storage-paradigms.md` when designing database schemas, rule/criteria engines, or comparing scale boundaries.
- MANDATORY: Load `C:/Users/dpagkaliwangan/.gemini/skills/second-brain/references/retrieval-templates.md` when initializing a second-brain index, writing atomic fact cards, or implementing a token-budgeted retrieval pipeline.

## Do NOT trigger for:

- Full-fidelity learning capture into the 5-tier notebook → route to `agent-note-taker`.
- Teaching a concept from first principles → route to `agent-concept-tutor`.
- Project ADRs, gotchas, dead ends, or runbooks → route to `engineering-journal`.
- Public standard documentation without token-compression intent → route to `domain-knowledge`.

---

## Core Architecture Rules (Always Enforced)

1. **Dual-Mode Disambiguation:** Classify every storage request before proposing a schema:
   - `FORWARD_LOOKUP` (Group ID → Criteria/Facts): Store as self-contained AST/YAML or hierarchical summary tree.
   - `INVERSE_MATCHING` (Incoming Event/Query → Matching Groups/Facts): Store in an inverted index, metadata router, Percolator, or Roaring Bitmap.
2. **Three-Tier Progressive Disclosure (L1 → L2 → L3):**
   - `L1 (_ROUTER.yaml)`: Domain list + one-line scope (< 10 tokens/domain). Always read first.
   - `L2 (<domain>/_CATALOG.yaml)`: Entity/topic keys, tags, and token counts (< 15 tokens/entry). Filter here before reading content.
   - `L3 (<domain>/facts.yaml)`: Atomic Subject-Predicate-Object (SPO) triples and key-value assertions (15–50 tokens/fact) with a `source_ref` pointer to raw prose.
3. **Strict Token Budget:** Cap retrieved context injected into prompts at ≤ 300 tokens per query unless the user explicitly requests raw source expansion.
4. **Compact Serialization:** Project retrieved knowledge as YAML or pipe-delimited tables — never verbose prose or deeply nested JSON.

---

## Actions & Workflows

### Action 1: Architecture & Criteria Strategy Selection
- **Trigger:** "criteria storage strategy", "how should I store these rules", "scale knowledge base", "percolate rules"
- **Input:** Problem statement specifying entity volume, query pattern (forward vs. inverse), latency target, and update frequency (minimum 1 sentence).
- **Process:**
  1. MANDATORY: Load `C:/Users/dpagkaliwangan/.gemini/skills/second-brain/references/storage-paradigms.md`.
  2. Classify workload by query mode (`FORWARD_LOOKUP`, `INVERSE_MATCHING`, or `HYBRID`) and scale tier (`<10K`, `10K–1M`, `>1M`).
  3. Select primary storage engine and indexing strategy from the decision matrix.
  4. Output concrete schema and retrieval query.
- **Output:** Markdown architecture specification saved to `{project-root}/arch-knowledge-strategy-[YYYY-MM-DD].md` (or inline if requested) containing: Workload Classification, Selected Paradigm, Schema DDL, Retrieval Query, and Token/Latency Estimate.

### Action 2: Low-Token Ingestion (Distill & Index)
- **Trigger:** "store in second brain", "compress into micro-facts", "atomic facts", "ingest low-token", "build knowledge index"
- **Input:** Raw text, markdown file path, or conversation excerpt (minimum 20 tokens).
- **Process:**
  1. MANDATORY: Load `C:/Users/dpagkaliwangan/.gemini/skills/second-brain/references/retrieval-templates.md`.
  2. Strip narrative filler, introductions, and syntactic glue.
  3. Extract atomic facts (`entity`, `attribute`, `compressed_fact`, `tags`, `token_count`, `source_ref`).
  4. Append atomic facts to `{project-root}/second-brain/<domain>/facts.yaml`.
  5. Update `{project-root}/second-brain/<domain>/_CATALOG.yaml` and `{project-root}/second-brain/_ROUTER.yaml`.
- **Output:** Updated YAML files in `{project-root}/second-brain/` + ingestion summary reporting raw tokens vs. compressed tokens and percentage saved.

### Action 3: Budget-Capped Retrieval (Query Second Brain)
- **Trigger:** "query second brain", "retrieve with minimal tokens", "fast lookup [topic]", "what do we know about [X] (low token)"
- **Input:** Natural-language question or attribute filter (minimum 3 words).
- **Process:**
  1. Read `{project-root}/second-brain/_ROUTER.yaml` to select target `<domain>` (0 content tokens read).
  2. Read `{project-root}/second-brain/<domain>/_CATALOG.yaml` and filter by `entity` or `tags`.
  3. Use `rg` to extract only matching `entity` blocks from `{project-root}/second-brain/<domain>/facts.yaml`.
  4. Pack highest-relevance facts into a YAML context block up to `max_tokens = 300`.
  5. Expand `source_ref` raw file only if atomic facts lack required precision.
- **Output:** Compact YAML `knowledge_context` block (≤ 300 tokens) + direct answer + token cost report (`Catalog tokens read` + `Fact tokens injected`).

### Action 4: Second Brain Compaction Audit
- **Trigger:** "compact knowledge base", "dedupe second brain", "audit knowledge token cost"
- **Input:** Target directory path containing markdown or YAML knowledge files.
- **Process:**
  1. Scan target directory using `rg --files <path>`.
  2. Identify prose files exceeding 300 tokens that lack L2/L3 YAML projections, and detect near-duplicate facts across files.
  3. Propose merge/extraction table before modifying files.
- **Output:** Audit report saved to `{project-root}/audit-second-brain-[YYYY-MM-DD].md` listing current token footprint, projected compressed footprint, and duplicate candidates.

---

## Edge Cases & Error Handling

- **Missing Index (`_ROUTER.yaml` not found):** Initialize `{project-root}/second-brain/_ROUTER.yaml` automatically during Action 2; during Action 3, fall back to `rg -i "<keyword>" {project-root}` and offer to initialize the index.
- **Ambiguous Domain Classification:** Place facts under `general` domain and flag for user confirmation if domain confidence is low.
- **Lossy Compression Risk (Formulas / Exact Constants):** Never paraphrase mathematical formulas, hex flags, error codes, or regexes — store verbatim inside `compressed_fact`.
- **Budget Overflow on Single Fact:** If a single formula or table exceeds 300 tokens, emit it intact and log a `BUDGET_OVERRIDE` warning rather than truncating mid-formula.

---

## Examples (Input → Output)

### Example 1: Low-Token Ingestion (Action 2)

**Input:**
```text
Store in second brain: When configuring the PostgreSQL cluster for Acme Corp production deployments, engineers must ensure that shared_buffers is set to 25% of total system RAM. Furthermore, work_mem should be set to 64MB per connection to prevent out-of-memory errors during high-concurrency sorting managed by PgBouncer. (Source: docs/db-tuning.md)
```

**Output:**
Appended to `{project-root}/second-brain/database/facts.yaml`:
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
`Token Report: Raw = 58 tokens → Compressed = 26 tokens (55.2% reduction).`

### Example 2: Criteria Strategy Selection (Action 1)

**Input:**
```text
How should I store 500,000 dynamic pricing criteria groups where each incoming order event {country, tier, amount} must match all qualifying groups in under 10ms?
```

**Output:**
```yaml
workload_classification:
  mode: INVERSE_MATCHING (Event -> Matching Criteria Groups)
  scale: 500,000 groups
  latency_budget: <10ms
recommended_architecture:
  system_of_record: "PostgreSQL criteria_groups table (ast_document JSONB)"
  evaluation_index: "In-Memory Roaring Bitmaps (discrete attributes) + Interval Tree (amount ranges)"
  fallback_engine: "OpenSearch / Elasticsearch Percolator query index"
```

---

## Notes

- **Scope Boundary with Notebook:** `second-brain` optimizes for **machine retrieval density** (YAML micro-facts, <50 tokens/fact). `agent-note-taker` optimizes for **human learning fidelity** (uncompressed Depth 1–5 markdown/Jupyter lessons in `C:/workarea/notebook/`). Both can coexist: raw lessons live in the notebook while their distilled L1–L3 index lives in `second-brain/`.
- **Fast Search Compliance:** Always use `rg --files` or `git ls-files` when scanning knowledge directories; never run recursive PowerShell directory scans.
