# Docs to Notebook Workflow


## Type
Direct Delegation — no QA; use `documentation-generation-workflow` for reviewed output

## Skill
Read `~/.gemini/skills/documentation-specialist/SKILL.md` first — contains tier rules, agent-to-file mapping, and templates

## Agents
archaeologist → tech-detective → architect --infra → concept-tutor

## Tier Execution
- minimal = archaeologist only (README)
- standard = archaeologist + architect --infra
- full = all

## Finish
Run `python /c/workarea/notebook/import-docs.py {project-root} {project-name}` to copy into `40-references/`
