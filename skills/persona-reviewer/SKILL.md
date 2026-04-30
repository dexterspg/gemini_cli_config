---
name: persona-reviewer
description: Multi-persona panel review skill. Auto-detects content type, orchestrates 4 parallel subagents, and synthesizes a panel discussion. Use when a user asks for a review of code, docs, designs, or other artifacts.
---

# Persona Reviewer Skill

Orchestration framework for assembling a diverse expert panel, collecting critiques in parallel, and synthesizing them into a panel discussion.

## Workflow

### Step 1: Detect Content Type
Analyze the input to determine content type (e.g., `code`, `documentation`, `test`, `migration`, `design`, `scheduled-automation-skill`).

### Step 2: Select Panel
Select 4 personas based on the content type. Refer to `.gemini/skills/persona-reviewer/PERSONAS.md` for definitions.

### Step 3: Parallel Review
Invoke 4 `generalist` sub-agents in parallel. Each receives:
1. The content to review.
2. Their specific persona definition.
3. Instructions to provide a 150-300 word critique.

**Reliability Rule:** Proceed as long as at least 2 sub-agents return data. If fewer than 2 succeed, report a system failure and ask for retry.

### Step 4: Synthesis
Weave the outputs into a panel discussion format:
1. **Opening Statements:** 2-4 sentences per persona.
2. **Layer/Coverage Verdict Table:** Grading dimensions (Excellent/Adequate/Gap/Missing).
3. **Cross-Examination:** Pointed challenges between personas.
4. **Shared Recommendations:** Specific, actionable steps.
5. **Panel Verdict:** Consensus, biggest gap, and next steps.

## Formatting Rule
Always use the structured Markdown format defined in the reference agent for the final output. Ensure the cross-examination reflects genuine tension.

## Usage
Triggered by: "review this [content]", "run a panel review on [file]", "/persona-reviewer [file]".
