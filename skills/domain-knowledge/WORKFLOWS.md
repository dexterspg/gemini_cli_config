# Domain Knowledge Workflows

## Codebase Discovery Workflow
Triggered by: discover domain knowledge in [path]

1. **Scan** (archaeologist): Perform a codebase scan to identify potential domain keywords, enums, and standards-based class names.
2. **Update Backlog** (Main): Add new keywords to knowledge/<domain>/_keywords.md. Deduplicate and cap the backlog size based on the scaling formula in RULES.md.
3. **Triage & Cluster** (Main Session): Apply the 3-Question Rule. Cluster proprietary terms under broader public concepts.
4. **Propose Cluster & Confirm** (Main Session): Present the proposed concept clusters to the user for approval.
5. **Generate Pedagogical Plan** (learning-strategy): For the approved cluster, generate a structured plan (Why, Analogy, Key Terms, Scenario).

6. **Execute & Self-Review** (agent-concept-tutor):
   - **6a: Write Concept** -- Draft the {concept}.md file using the pedagogical plan.
   - **6b: Populate Metadata** -- Add project context and implementation links to _metadata.md.
   - **6c: Populate Formulas** -- Add any mathematical rules found to _formulas.md in the 5-column table format.
7. **Prune Backlog** (Main): Once documented, remove the cluster's keywords from _keywords.md.
8. **Update Index** (Main): Place the new concepts into the correct Tier (Stand, Walk, or Run) in _INDEX.md.
9. **Map Intersections** (Main): If the concept bridges domains, update knowledge/_CROSS_DOMAIN.md and knowledge/_CONCEPTUAL_THEORIES.md using the Cross-Domain Mapping Workflow.
10. **Final Validation** (Main): Perform a technical audit (Empirical Validation Mandate) to ensure all links and theories are actively reflected in the current codebase.


## Reactive Documentation Workflow
Triggered by: document [concept] or how does [X] work

1. **Research** (Main Session): Gather raw facts, snippets, and authoritative external links for the concept.
2. **Follow Steps 5, 6, 8, and 9** of the Codebase Discovery Workflow above to create and integrate the documentation.

## Cross-Domain Mapping Workflow
Used to logically intersect different domains.

1. **Revisit Concept Files:** Identify multi-domain use cases or causal chains.
2. **Categorize Intersection:** Assign to one of the 7 Archetypes (see RULES.md).
3. **Update Hubs:** Add the link to the Master Intersection Matrix in _CROSS_DOMAIN.md.
4. **Link Implementation:** Document the specific Java/Entity bridge in the relevant _metadata.md file.

## Documentation vs. Code Audit Workflow
**Trigger:** "audit knowledge base", "make knowledge consistent with code"

This workflow is used to systematically audit the conceptual documents in `/knowledge` against the source code to ensure they are accurate and non-technical.

1.  **Select Target File:** Choose the next `.md` file in the knowledge base to audit (e.g., `knowledge/accounting/lease-classification.md`).
2.  **Keyword Extraction:** Read the document and identify the key business concepts and terms.
3.  **Code Search:** Using `grep_search`, search for camelCase or constant-case versions of the keywords in the relevant source code directories (e.g., `11100-nakisa-financial-suite`).
4.  **Trace and Analyze:** Follow the code trail, starting from DTOs and entities, to find the core service or engine that implements the business logic. This may require analyzing `pom.xml` files to trace dependencies and find the correct source directories.
5.  **Compare and Identify Discrepancies:** Compare the logic implemented in the code against the description in the documentation.
6.  **Delegate Re-Drafting:**
    *   If a discrepancy is found, invoke `agent-concept-tutor`.
    *   Provide the agent with the original document, the findings from the code analysis, and a clear instruction to re-draft the document for a non-technical audience.
    *   Present the new draft from `agent-concept-tutor` to the user for approval.
7.  **Apply Approved Changes:** Use the `replace` tool to update the document with the approved content.
8.  **Repeat:** Continue to the next file.
9.  **Log New Keywords:** If significant new concepts or keywords are discovered in the code that are not present in the document being audited, add them to the `_keywords.md` backlog for the domain and inform the user of the discovery.

