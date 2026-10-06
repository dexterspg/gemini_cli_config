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
- **The Process:** Use `agent-codebase-archaeologist` to find concrete evidence (Classes/Methods) for the claimed behavior.
- **The Decision:** If no code exists, the concept must be labeled as "Theoretical." If code is found, the concept is "Validated."
- **Leak Protection:** Move all technical proof discovered to `_metadata.md`.

## 19. Reader Experience (Non-Developer Focus)
The primary audience for `.md` files is non-technical stakeholders (BAs, Consultants). All documentation must be written as a **pure concept document**.

- **Hierarchy:** Always use the 4-level "Puzzle" scaffolding (Anchors, Engines, Operations, Integration).
- **Traceability Flows:** Level 4 files MUST include "Business Traceability Flows" that trace an event (e.g., Rent Change) through all four levels.
- **Onboarding:** The root `_INDEX.md` must include a "How to Read This Knowledge Base" section.
- **Clarity and Tone:**
    - **Use Analogies:** Explain complex topics with simple, real-world analogies (e.g., "Car Rental vs. Taxi Ride").
    - **Use Q&A Flow:** Describe decision logic as a series of questions a business person would ask.
    - **AVOID TECHNICAL JARGON:** Strictly avoid code snippets, Java class names, variable names (e.g., `hasIdentifiedAsset`), and implementation-specific details. These belong in `_metadata.md`.

## 20. Skill Meta-Management
- **Direct Edit Mandate:** When updating the `domain-knowledge` skill files (`RULES.md`, `WORKFLOWS.md`, etc.) based on a direct user instruction, the `replace` tool may be used without a secondary confirmation prompt. The user's instruction to modify the skill is considered pre-approval.


## 2. Source of Truth for Business Logic
- **Code over Concept:** For business logic, you MUST rely on the actual source code (in `C:\core2\`) as the ultimate source of truth, rather than general theoretical or conceptual assumptions. 
- **Anti-Drift:** When understanding business logic, ensure the explanation does not drift away from the actual codebase, unless no codebase is provided.
- **Discrepancy Tracking:** If a domain lesson or conceptual explanation conflicts with the actual codebase implementation, document the discrepancy in the lesson file under a specific "Codebase Discrepancies" section.

## 3. Brand & Company Name Prohibitions
- **No Proprietary Brand Names:** NEVER include company or brand names (e.g., "Nakisa", "Dell", "Costco", etc.) in lessons or conceptual documentation. 
- **Use Generic Placeholders:** Use generic role-based or entity placeholders instead (e.g., "Enterprise Financial Engine", "Hardware Supplier", "Wholesale Retailer", "The Vendor").

## 4. Mandatory Mathematical Calculations & Full Pedagogical Depth
- **Mandatory Math Section:** Every financial or accounting entity lesson MUST include "Part 5: The Math (Formula & Calculation)" containing LaTeX formulas, exponent behavior (e.g., IN_ADVANCE vs IN_ARREARS discounting shifts), step-by-step numerical examples, and theoretical vs. engine discrepancy checks.
- **Uncompressed Explanations:** Never reduce or compress domain field breakdowns into shallow summaries. Detailed sub-classifications (e.g., PAYMENT_TERM vs INITIAL_DIRECT_COST vs NON_LEASE_TERM) must be explicitly explained with their distinct real-world financial and balance sheet impacts.

## 5. Structure Check Exit Gate (Quality Control Mandate)
- **Mandatory Exit Gate Audit:** Before completing any lesson turn or prompting the user to proceed to the next topic, an explicit self-audit MUST verify that ALL 8 required sections are present in order:
  1. `Part 1: Top-Down (The 'Why' & Core Idea)`
  2. `Part 2: Topological Sort (The 'How' - Step-by-Step Build)`
  3. `Part 3: Minimal Example (The Payload - Representative JSON)`
  4. `Part 4: Codebase Discrepancies (Intuition vs. Reality)`
  5. `Part 5: The Math (Formula & Calculation)`
  6. `Part 6: Common Confusions (Session Learnings)`
  7. `Flow Summary & Key Takeaways`
  8. `Appendix: Advanced Operational Fields`
- **Auto-Remediation:** If any section is missing, the generator MUST fill in and insert the missing section BEFORE concluding the turn or asking for user confirmation to proceed.

## 6. Non-Domain-Expert Pedagogical Anchors & Foundation Bridge Rule
- **Mandatory Non-Expert Assumption:** All domain lessons generated by `agent-concept-tutor` MUST assume the learner is NOT a domain expert (e.g., non-accountant, non-logistics specialist, non-tax auditor).
- **Intuitive First-Principles Framing:** Before presenting specialized domain mechanics (e.g., SAP posting keys, journal entries, T-accounts, tax jurisdictions), the lesson MUST ground the topic in plain-English everyday analogies (e.g., house mortgages, credit card swipes, shoebox cash counting).
- **Reusable Across All Domains:** This non-expert pedagogical bridge applies permanently across all current and future domain learning tracks (Accounting, Tax, Logistics, SAP Integration, HR Data Core, Real Estate Management) to guarantee that non-specialist learners can build deep mental models without getting blocked by domain jargon.

