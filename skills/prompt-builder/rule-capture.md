# Template: Rule-Capture

For business logic, decision trees, domain knowledge, process capture.

**Length guidance:** Keep under 500 words for portability.

**Rules:**
- Strip implementation details, keep rules and examples
- Make portable — should work in Claude, ChatGPT, Gemini, or any AI
- Include minimum 2 examples: typical + edge case

```markdown
# Prompt: [Topic Name]

## Purpose
[One sentence: what this prompt helps accomplish]

## Domain
[Code / Finance / Legal / Engineering / Operations / etc.]

## Context
[Background paragraph explaining the subject matter]

## Rules
1. [Rule in plain English]
2. [Rule in plain English]
3. [Rule in plain English]

## Examples

**Example 1: [Scenario Name]**
Input: [example input]
Expected Output: [example output]

**Example 2: [Edge Case]**
Input: [example input]
Expected Output: [example output]

---

## Copy-Paste Prompt

You are a [role with domain expertise]. Your task is to [specific goal].

Context:
[Brief background the AI needs to know]

Rules:
- [Rule 1]
- [Rule 2]
- [Rule 3]

When given [input type], you should [expected action/output].

Examples:
Input: [example]
Output: [example]

Now handle the following:
{user_input}
```
