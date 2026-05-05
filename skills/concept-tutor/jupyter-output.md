---
name: concept-tutor-jupyter
description: Generates Depth 1-5 structured cells (markdown + code) for Jupyter notebooks. Triggers: "Create interactive notebook", "Generate .ipynb".
---
# Concept Tutor: Jupyter Notebook Output

Load this file only when generating Jupyter notebook content (`.ipynb`).

## When to generate Jupyter content

When told "Create interactive notebook for [concept]" or "Generate .ipynb for [topic]".

## Rules

- Generate teaching content structured for Depth Levels 1-5 progression
- Include executable Python code examples, visualizations, and interactive exercises
- Provide content as structured cells (markdown + code) that agent-note-taker will write to .ipynb
- concept-tutor **generates** the content; agent-note-taker **writes** the .ipynb file to disk and handles file placement, registry, and metadata
- Follow the Depth 1-5 progression from the Output Format (Markdown) section, using Jupyter cells (markdown + code) instead of plain markdown
- **Dollar signs in markdown cells:** Wrap all monetary values in backticks to prevent MathJax rendering them as math.
  - Wrong: `$10,000` → renders as broken math
  - Correct: `` `$10,000` `` → renders as `$10,000`
  - Applies to any dollar amount. Code cells are unaffected.       

## Cell Structure

| Content | Cell type |
|---|---|
| Explanation, analogy, vocabulary | Markdown |
| Working example, exercise, demo | Code |
| Section header / depth transition | Markdown |
| Output expectations ("should print...") | Markdown, before the code cell |

One concept per code cell. Keep cells independently runnable where possible.

## Metadata (for note-taker to place in first cell)

```
# Topic Title
**Tier:** 20-domains/domain/subdomain
**Depth Levels:** 1-5 (complete)
**Prerequisites:** [list requirements]
**Applications:** [real-world uses]
**Kernel:** Python 3.9
**Last Updated:** YYYY-MM-DD
```
