---
name: codebase-reverse-engineer
description: Deep technical analysis and documentation generation. Triggers: "reverse engineer [project]", "analyze this project", "what does [project] do".
---
# Codebase Reverse Engineer Workflow

**Triggers:** "reverse engineer [project]", "analyze this project", "what does [project] do"

## Flow

1. archaeologist (full technical analysis)
2. concept-tutor (mandatory business case)
3. Ask user about docs generation
4. If yes: all agents read `~/.gemini/skills/documentation-specialist/SKILL.md` for templates before writing, then each agent writes its assigned files per doc skill's agent-to-file mapping

## Rules

- Distinguish from onboarding: reverse-engineer = deep analysis + business case + optional docs. Onboard = guided learning.
- For docs with quality review, suggest `documentation-generation-workflow` instead.
- Do NOT trigger for onboarding guides -> use `agent-codebase-archaeologist --onboard`.
- Do NOT trigger for debugging -> use `agent-debugger`.
- Do NOT trigger for general concept theory -> use `agent-concept-tutor`.
