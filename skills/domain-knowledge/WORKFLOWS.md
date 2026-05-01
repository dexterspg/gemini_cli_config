# Domain Knowledge Workflows

## Codebase Discovery Workflow

Use this when domain concepts are not explicitly provided.

1. **Scan for domain signals** — use Glob and Grep to find:
   - Class/method names referencing external standards (e.g., `Ifrs16`, `IncotermsRule`, `PayPeriod`)
   - Comments citing standards, regulations, or external systems (e.g., `// per IFRS 16`, `// SAP posting key`)
   - Enum values or constants that map to public domain terminology
   - Package/module names that suggest a domain (e.g., `accounting`, `payroll`, `logistics`)

2. **Classify each signal** — apply the three-question decision rule (see RULES.md) to each candidate concept:
   - Code-bound only → skip
   - Platform-specific interpretation → skip
   - Public standard, unchanged → add to research list

3. **Group by domain** — cluster concepts into domain subfolders (`accounting/`, `sap/`, `logistics/`, etc.)

4. **Research each concept** — web search for each item on the research list; write one `knowledge/<domain>/` file per concept using the template in `TEMPLATES.md`.

5. **Deduplication check** — check if the concept already exists in the project or the notebook.
   - Step 2 must be deterministic: check `/c/workarea/notebook/20-domains/` first.
   - ONLY ask the user if that path is inaccessible.

6. **Create stub in documentation/** — add a minimal stub to the relevant `documentation/` file.
   - **Condition:** Only perform this step if a `documentation/` folder already exists in the project root.
   ```md
   ## [Concept Name]
   [1-2 sentence summary of what it is.]
   See: knowledge/<domain>/filename.md
   ```

## Edge Case: Platform Deviations

When a platform deviates from a public standard, write BOTH in this order:
1. **Gemini** writes the public baseline in `knowledge/<domain>/` first.
2. **agent-codebase-archaeologist** writes the deviation in `documentation/platform/domain-concepts/`, referencing the `knowledge/` entry for baseline context.
- **Rule:** Never write the deviation without the baseline.

## Signal Identification Table

| Signal type | Example | Action |
|---|---|---|
| Class name with standard acronym | `Ifrs16AmortizationSchedule` | Research IFRS 16 |
| Comment citing a rule | `// discount rate per IAS 36` | Research IAS 36 |
| Enum mapping to external codes | `INCOTERM_FOB`, `INCOTERM_CIF` | Research Incoterms |
| Package name | `com.company.payroll.statutory` | Research statutory deduction rules |
| String constant with external code | `"SAP_BAPI_VENDOR_FIND"` | Research SAP BAPI |
