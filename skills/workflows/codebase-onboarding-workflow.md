# Codebase Onboarding Workflow

**Triggers:** "help me understand this codebase", "onboard me to [repo]"

## Flow

1. Check if documentation exists (`{project-root}/documentation/` or `40-references/{project}/` in notebook)
2. **If docs exist:** Skip tech-detective (redundant) -> archaeologist reads docs directly (--onboard, --domain)
3. **If no docs exist:** tech-detective (quick scan) -> archaeologist (--onboard, --domain)
4. Ask user if they want concept explanations -> optionally concept-tutor -> optionally save to notebook
