# Gemini Validation Workflow


## Steps
1. Read `{project-root}/documentation_gem/CHANGELOG.md`
2. Compare entries against existing files in `{project-root}/documentation/`
3. Identify findings missing or not covered in `documentation/`
4. For each gap — route to the agent assigned to that specific `.md` file per `~/.gemini/skills/documentation-specialist/SKILL.md` agent-to-file mapping
5. That agent writes the addition directly into `documentation/`

## Rules
- User-triggered only — never auto-trigger
- Main session owns the comparison and routing; agent-gemini does not participate
