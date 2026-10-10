---
name: diagrams
description: "Lightweight 1-hop ASCII diagram templates for teaching domain knowledge."
---

# Domain Knowledge Diagram Templates

Use these lightweight, fast ASCII diagram templates to visually explain concepts inline without relying on Mermaid or complex rendering. They should be simple (max ~14 lines, 7 boxes) and use safe ASCII characters (`+`, `-`, `|`, `v`, `^`, `<`, `>`).

## 1. Neighborhood Map
Best for Entity Nodes. Shows the central entity and its direct (1-hop) dependencies or dependents.

```text
       [Parent Entity]
              ^
              | (Many-to-One)
       +------+------+
       |   [Core]    |
       |  [Entity]   |
       +------+------+
              | (One-to-Many)
              v
       [Child Entity]
```

## 2. Annotated Payload
Best for showing data structures or JSON payloads with inline explanations.

```text
{
  "id": 123,                 <-- Unique Identifier
  "status": "ACTIVE",        <-- Current state (ACTIVE, INACTIVE)
  "metadata": {              <-- Nested configuration
    "region": "US"           <-- Region code
  }
}
```

## 3. Actor Sequence
Best for Process/Engine Nodes. Shows the flow of actions between actors.

```text
[Actor A]         [Actor B]         [Actor C]
    |                 |                 |
    |---(1) Request-->|                 |
    |                 |---(2) Fetch---->|
    |                 |<--(3) Data------|
    |<--(4) Result----|                 |
    |                 |                 |
```

## 4. Pipeline
Best for Calculation or Process Nodes. Shows a linear transformation or sequence of steps.

```text
[Input Data] -> (Step 1: Validate) -> (Step 2: Transform) -> (Step 3: Save) -> [Output Data]
```

## Constraints
- **Max Lines:** ~14 lines per diagram.
- **Max Elements:** ~7 boxes/actors.
- **Characters:** Stick to standard ASCII (`+`, `-`, `|`, `v`, `^`, `<`, `>`, `[`, `]`, `(`, `)`).
- **No Mermaid:** Do not use Mermaid.js or other markdown diagram rendering blocks. Use fenced code blocks with `text` formatting.
- **Domain-First Labels:** Diagram edges and payload annotations MUST use plain business language (e.g., "signed under", "billed in"), not code annotations like `@ManyToOne` or `nullable=false`.
- **Code Detail in Legend:** If technical implementation details (like `updatable=false` or exact database field names) are necessary, place them in a one-line legend beneath the diagram or move them exclusively to Part 4 (Verification Ledger).
