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
