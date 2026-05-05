---
name: persona-reviewer
description: 'Multi-persona panel review skill. Auto-detects content type, orchestrates 4 parallel subagents, and synthesizes a panel discussion. Use when a user asks for a review of code, docs, designs, or other artifacts.'
---

# Persona Reviewer Skill

Orchestration framework for assembling a diverse expert panel, collecting critiques in parallel, and synthesizing them into a panel discussion.

## Usage
Triggers: "review this [X]", "panel review on [X]", "expert opinion on [X]", "/persona-reviewer [X]".

## Do NOT Trigger For:
- Simple spelling/grammar checks -> use `agent-quality-guardian`.
- Code bug root cause analysis -> use `agent-debugger`.
- Technical documentation structure checks -> use `agent-quality-guardian`.

## Workflow
...
