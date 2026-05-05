# Documentation: Diagrams

Diagrams are first-class reference material. Preferred: ASCII box diagrams. Optional: Mermaid (include ASCII version).

## General Rules
- One concern per diagram.
- Label every arrow (data + protocol).
- Max 10 boxes per diagram; split if larger.
- Dual placement: canonical file in `diagrams/` + embedded inline in docs.
- DOMAIN.md requires Entity Model + 1 Flow (Sequence or State).

## Minimum Diagrams by Tier
| Tier | Requirements |
|------|--------------|
| **Minimal** | 1 — Topology or C4-L2. |
| **Standard** | Topology + C4-L2 + Sequence + 1 per deep dive. |
| **Full** | L1–L3 + Sequence + State machine + Entity/ERD + 1 per deep dive. |

## Type Selection Guide
| Question | Diagram Type | Location |
|---|---|---|
| What services exist? | Topology | README |
| Who uses the system? | Context (C4-L1) | ARCHITECTURE |
| How do components interact? | Container (C4-L2) | ARCHITECTURE |
| Inside the service? | Component (C4-L3) | DOMAIN / deep dive |
| Request flow? | Sequence | DOMAIN / API-REF |
| State transitions? | State Machine | DOMAIN / deep dive |
| Data relationships? | Entity / ERD | DATABASE / DOMAIN |
