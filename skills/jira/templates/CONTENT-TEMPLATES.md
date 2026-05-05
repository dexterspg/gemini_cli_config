# Jira Content Templates

## 5-Question Analysis Format

Every ticket analysis and Resolution Path field (`customfield_12000`) **MUST** use exactly these 5 questions. Do NOT rephrase, reorder, or substitute.

**1. What was the issue and its impact?**
- Problem Definition: what the client was unable to do
- Specific error or symptom reported
- Business impact (halted processes, compliance risks, financial reporting delays)
- Priority classification
- Affected Users/Processes:
  - Entities affected (company codes, environments, modules)       
  - System version affected
  - Technical context (currencies, configurations, etc.)

**2. What caused the issue?**
- Root Cause stated clearly
- Technical Explanation:
  - What configuration or setting was incorrect/missing
  - How the system behaved as a result (API calls, data flow issues)
  - Preceding events that triggered the issue (upgrades, migrations)
  - Technical chain of causation

**3. What troubleshooting steps should be taken?**
- Step-by-Step Diagnostic Process:
  - Verification steps (connectivity, permissions)
  - Logging configurations to enable
  - Log files and traces to review
  - Configuration areas to validate
  - Environment comparison steps
  - Post-upgrade verification checks

**4. What resolution or workaround was applied?**
- Resolution stated clearly
- Implementation Steps:
  - Navigation path in the application
  - Specific settings to configure
  - Values to add or modify
  - Verification steps after changes

**5. How can this be prevented in the future?**
- Pre-Upgrade Validation Checklist items
- Post-Upgrade Testing Protocols
- Environment gaps (e.g., missing QA environment)
- Configuration review processes

**Writing guidelines:** Be detailed and technical — incorporate all relevant information from the ticket's description, resolution path, comments, and attached files. Expand on brief entries with appropriate technical detail relevant to the product domain (SAP integration, lease accounting, asset management).

**"Not applicable" rule:** Write all answers from the perspective of application support. If a question (especially #5) asks for something outside application support's control (e.g., preventing a system-level data gap), answer with "Not applicable" and a brief explanation of why, plus a reapplication note if a script or workaround exists for recurrence. Never force an answer that implies support can prevent something they cannot.

---

## KB Article Format

Generate a structured Knowledge Base article based on support case details. Rules:
- Do not include specific names of individuals or customers        
- Do not add visual elements, dividers, excess spacing, or new sections
- Maintain consistent formatting throughout
- Keep the article concise and scannable

**Required sections in this exact order:**
- **Title:** Brief, descriptive title of the issue
- **Issue Overview:** Issue description, error messages, impact on user or system
- **Cause of the Issue:** Root cause. If unclear or not provided, state that concisely
- **Troubleshooting Steps Taken:** Numbered list of steps that directly helped identify or resolve the issue. Exclude unproductive actions. Keep each step concise
- **Resolution & Fix:** Fix or workaround applied, follow-up actions taken
- **Prevention & Best Practices:** Recommendations if applicable. If not applicable, state "Not applicable."
