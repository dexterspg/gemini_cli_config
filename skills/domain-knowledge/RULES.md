# Domain Knowledge Rules

## Reader Orientation
These files contain background on public standards — not project instructions. They explain what an external standard IS, not how this codebase implements it. For implementation details, read `documentation/domain/`. Files are drafted by `agent-concept-tutor` using research provided by Gemini.

## Ownership and Delegation
This skill uses a collaborative orchestration model:
1. **Gemini (Main Session):** Orchestrator. Performs codebase discovery, web research, and fact-gathering.
2. **agent-concept-tutor (Writer):** Specialist. Receives research from Gemini and drafts the final `knowledge/` file using its pedagogical structuring expertise.
3. **agent-codebase-archaeologist (Sync):** Handles Option A (Promotion) to `documentation/platform/`.

**Workflow:** Gemini researches [Concept] -> Gemini invokes `agent-concept-tutor` with research facts -> `agent-concept-tutor` drafts file -> Gemini indexes and reviews.

## 1. File Naming and Location
- **Format:** kebab-case (e.g., `ifrs-16.md`, `sap-posting-keys.md`)
- **Quantity:** One concept per file.
- **Organization:** Place under the correct domain subfolder (e.g., `accounting/`, `sap/`, `tax/`, `logistics/`).
- **Rule:** Never put project-specific content in the domain file.
- **Purity Mandate:** Never include technical implementation details like Java classes, method names, database table/field names, or project-specific validation logic in the concept file. These details belong exclusively in the `_metadata.md` file.

## 2. Content Rules (What to write)
- Pure public standard content only.
- The 20% of the standard that explains 80% of the code behavior.
- Non-obvious rules that catch developers off guard.
- Key terms with plain-language definitions.
- Exactly ONE authoritative external link (official body, vendor docs, or RFC).

## 3. What NOT to write
- Full reproductions of the standard (link to it instead).
- Opinions or recommendations.
- Content that requires reading source code to verify.

## 4. Project Context & Metadata (_metadata.md)
To keep concept files pure, all project-specific context and document-level metadata are stored in a single index file per domain.
- **Location:** `knowledge/<domain>/_metadata.md`
- **Implementation Details:** Explicitly list proprietary terms (e.g., 'Agreement Groups') and link to the specific Java classes or entities that implement the concept.

## 5. Tiered Progression (The Knowledge Puzzle)
Every domain folder must have an `_INDEX.md` file that organizes concepts into the following tiers:
- **Level 1: Stand (Anchors):** Foundational business entities and master data (e.g., Company, Chart of Accounts).
- **Level 2: Walk (Engines):** Logic engines, determination systems, and core processes (e.g., Currency Conversion).
- **Level 3: Run (Operations):** Complex accounting treatments, specific operational workflows, and reconciliations.

## 6. The Abstraction & Bridge Pattern
Proprietary jargon must never have its own concept file.
- **Abstracting:** Map the jargon to a public concept (e.g., "Agreement Group" -> "Contract Hierarchies").
- **Bridging:** Use `_metadata.md` to link the public concept to the specific jargon used in the code.

## 7. Claude Fallback Banner
When writing a file with `source: claude` (written without live research), add this block immediately after the frontmatter:
> **Note:** This file was written by a Claude agent without live web research. Content is based on training knowledge only. Verify against the authoritative source before relying on it.

## 8. Three-Question Decision Rule (Folder Assignment)
Apply in order. Stop at the first YES.
1. Does this concept only make sense by reading the source code? -> `documentation/domain/`
2. Did the platform create, adapt, or extend this concept in a specific way? -> `documentation/platform/domain-concepts/`
3. Does this concept exist verbatim in a public standard, textbook, or vendor docs? -> `knowledge/<domain>/`

## 9. Dynamic Keyword Backlog (_keywords.md)
- **Location:** `knowledge/<domain>/_keywords.md`
- **Format:** `keyword: count` (sorted by count descending).
- **Dynamic Capping:** After updating, the backlog size is capped. The maximum number of lines is calculated by the formula: `max_size = 20 + (number_of_domain_documents * 2)`.
- **Pruning:** When a concept is documented, remove its keywords from the backlog immediately.

## 10. Sync and Promotion Options
When a concept is documented in `_PENDING_SYNC.md`, the following decisions apply:

| Option | Name | Action |
|---|---|---|
| **A** | **Promote** | Content moves to `documentation/platform/domain-concepts/`. Requires verification by `agent-codebase-archaeologist`. |
| **B** | **Stub only** | A minimal signpost is added to `documentation/` (if it exists) pointing to the `knowledge/` file. |
| **C** | **Keep** | File remains exclusively in the `knowledge/` folder; used for local reference only. |

## 11. Lifecycle: Updating
- Triggered by user: "update knowledge for [concept]".
- **Action:** Re-research and rewrite the file **in place**.
- **Rule:** Never create a new file for an update.

## 12. Lifecycle: Retirement
- Before deleting a `knowledge/` file, check if it has been synced to the global notebook.
- If not synced, offer to sync before deletion.

## 13. Notebook Sync
- **Trigger:** User-triggered only ("sync to notebook").
- **Cleanup:** After successful sync, the project-level copy can be pruned if the user chooses.

## 14. Topic Interconnectivity (The Web of Topics)
Knowledge is not a flat list; it is a web. Every concept must be evaluated for its relationship to other topics.
- **Requirement:** During the "Map Intersections" step, identify at least one logical connection to another concept.
- **Goal:** A user should be able to "surf" from a physical fact to a financial liability.

## 15. Cross-Domain Archetypes
Categorize connections in `_CROSS_DOMAIN.md` using these archetypes:
1. **The Measurement Bridge:** Physical units driving financial values.
2. **The Economic Influence Loop:** External triggers causing internal accounting changes.
3. **The Compliance Guardrail:** Operational rules protecting disclosure accuracy.
4. **The Capital Lifecycle:** Physical spend becoming an accounting asset.
5. **The Accountability Path:** Organizational units ensuring 100% spend tracking.
6. **The Temporal Rhythm:** Calendars aligning events with reporting snapshots.
7. **The Trust Chain:** Provenance and audit trails proving dollar validity.

## 16. The Purity vs. Metadata Rule
- **Concept Files (.md):** Must be 100% pure business/domain logic. No Java classes, method names, or technical IDs.
- **Metadata Files (_metadata.md):** The technical "anchor." All Java paths, database fields (e.g., BUKRS), and implementation specifics found during the Code Audit must be moved here.

## 17. Integration and Theory Layer (`_CROSS_DOMAIN.md` & `_CONCEPTUAL_THEORIES.md`)
In multi-domain workspaces, these two files provide the "Glue":
- **`_CROSS_DOMAIN.md` (The "How"):** Maps technical/operational wiring between domains.
- **`_CONCEPTUAL_THEORIES.md` (The "Why"):** Defines the First Principles (Control, Risk, Value) that unify the entire system.

## 18. Empirical Validation (Code Audit) Mandate
Before finalizing any Level 2-4 document, a technical audit must be performed.
- **The Process:** Use `codebase_investigator` to find concrete evidence (Classes/Methods) for the claimed behavior.
- **The Decision:** If no code exists, the concept must be labeled as "Theoretical." If code is found, the concept is "Validated."
- **Leak Protection:** Move all technical proof discovered to `_metadata.md`.

## 19. Reader Experience (Non-Developer Focus)
The primary audience for `.md` files is non-technical stakeholders (BAs, Consultants).
- **Hierarchy:** Always use the 4-level "Puzzle" scaffolding (Anchors, Engines, Operations, Integration).
- **Traceability Flows:** Level 4 files MUST include "Business Traceability Flows" that trace an event (e.g., Rent Change) through all four levels.
- **Onboarding:** The root `_INDEX.md` must include a "How to Read This Knowledge Base" section.
