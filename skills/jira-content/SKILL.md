---
name: jira-content
description: >-
  Formats already-fetched Jira ticket data into a 5-question analysis, KB article, release notes, bug summary or customer-facing text, using the Jira content templates. The main session runs it after fetching the ticket (jira skill). Triggers on: "5-question analysis", "write a KB article from this ticket", "release notes from these tickets", "bug summary", "customer-facing summary of this ticket". Not for Jira operations (jira skill).
---

# Jira content from ticket data

Produce a 5-question analysis, KB article, release note, bug summary or customer-facing text from ticket data the main session has ALREADY fetched.

## Never

- Call `mcp__jira__*` tools; the main session fetches data first (`jira` skill) and passes it here
- Modify Jira tickets; return formatted text only, the main session writes back
- State a fact that is not in the ticket data; say what the ticket does not say

## Dependencies

MANDATORY: Read `~/.gemini/skills/jira/templates/CONTENT-TEMPLATES.md` before producing any content. It owns the 5-question format (exact questions, exact order) and the other templates.

## Core workflow: 5-question analysis

1. Read the fetched ticket data.
2. If linked issues are missing and seem relevant, say what is needed.
3. Produce the analysis in the template's exact format.
4. Return the formatted content in the reply.

## Writing guidelines

Clear, professional language for the target audience. Other formats on request: knowledge base article, release notes, bug summary, customer-facing communication (templates in the file above).
