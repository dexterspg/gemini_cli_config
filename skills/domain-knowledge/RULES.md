# Domain Knowledge Rules

## Reader Orientation
These files contain background on public standards — not project instructions. They explain what an external standard IS, not how this codebase implements it. For implementation details, read `documentation/domain/`. Files are drafted by `agent-concept-tutor` using research provided by Gemini. Files marked `source: claude` were written without live web research and should be treated as unverified drafts.

## Ownership and Delegation
This skill uses a collaborative orchestration model:
1. **Gemini (Main Session):** Orchestrator. Performs codebase discovery, web research, and fact-gathering.
2. **agent-concept-tutor (Writer):** Specialist. Receives research from Gemini and drafts the final `knowledge/` file using its pedagogical structuring expertise.
3. **agent-codebase-archaeologist (Sync):** Handles Option A (Promotion) to `documentation/platform/`.

**Workflow:** Gemini researches [Concept] -> Gemini invokes `agent-concept-tutor` with research facts -> `agent-concept-tutor` drafts file -> Gemini indexes and reviews.

## 1. Standalone Rule
`knowledge/` files must work on their own. Never assume a `documentation/` folder exists in the project.
- The "How the Platform Uses This" section in each file is **optional**.
- The stub-creation step in the write workflow is **conditional** — only perform it if a `documentation/` folder already exists in the project root.

## 2. File Naming
- **Format:** kebab-case (e.g., `ifrs-16.md`, `sap-posting-keys.md`)
- **Quantity:** One concept per file.
- **Organization:** No numbering. Place under the correct domain subfolder (e.g., `accounting/`, `sap/`, `tax/`, `logistics/`).

## 3. Content Rules
**What to write:**
- The 20% of the standard that explains 80% of the code behavior.
- Non-obvious rules that catch developers off guard.
- Key terms with plain-language definitions.
- Exactly ONE authoritative external link (official body, vendor docs, RFC).

**What NOT to write:**
- Full reproductions of the standard (link to it instead).
- Project implementation details (belongs in `documentation/domain/`).
- Opinions or recommendations.
- Content that requires reading source code to verify.

## 4. Sync Options
Sync is always user-triggered. The user reviews `_PENDING_SYNC.md` to decide.

| Option | Name | Action | Gate |
|---|---|---|---|
| **A** | **Promote** | Content moves to `documentation/platform/domain-concepts/`. | `agent-codebase-archaeologist` re-verifies; Quality Guardian gate. |
| **B** | **Stub only** | Minimal plain-text signpost added to `documentation/` (if it exists). | No action needed. |
| **C** | **Keep** | File stays in `knowledge/` only; available for notebook sync. | **Default Option.** |

## 5. Minimum Viable Path
Under delivery pressure:
- Write the stub in `documentation/` (if folder exists) with a `NOT YET WRITTEN` note.
- The full `knowledge/` file can be written later by Gemini when time allows.

## 6. Lifecycle: Updating
- Triggered by user: "update knowledge for [concept]".
- **Action:** Re-research and rewrite the file **in place**.
- **Rule:** Never create a new file for an update.
- **Update:** Refresh `last-updated` and `standard-version` in frontmatter.

## 7. Lifecycle: Retirement
- Before deleting a `knowledge/` file, check if it has been synced to the notebook.
- If not synced, offer to sync before deletion.

## 8. Notebook Sync
- **Trigger:** User-triggered only ("sync to notebook").
- **Metadata:** Include `source_type: domain-knowledge`.
- **Cleanup:** After successful sync, the project-level copy can be pruned if the user chooses.

## 9. Claude Fallback Banner
When writing a file with `source: claude`, add this block immediately after the frontmatter:

> **Note:** This file was written by a Claude agent without live web research. Content is based on training knowledge only. Verify against the authoritative source before relying on it.

## 10. Three-Question Decision Rule (Folder Assignment)
Apply in order. Stop at the first YES.
1. Does this concept only make sense by reading the source code? -> `documentation/domain/NN-*.md`
2. Did the platform create, adapt, or extend this concept in a specific way? -> `documentation/platform/domain-concepts/`
3. Does this concept exist verbatim in a public standard, textbook, or vendor docs? -> `knowledge/<domain>/`
