# Audit Examples

## Example 1 — Token Efficiency (System Prompt)

User pastes:
```
Please make sure to carefully review the following Java code and,
if you would be so kind, provide a refactored version that is
clean and readable. It is important that you do not include
any explanations or commentary. Today is May 3, 2026.
```

Output:
```
TOKEN EFFICIENCY SCORE: 28/100 — Poor

CRITICAL ISSUES
---------------
Dynamic content in static block: "Today is May 3, 2026" → move to user turn
No output contract → add "Output: code only"
No role declaration → add "Role: Java refactoring assistant"

TOP REWRITE
-----------
Original (~52 tokens):
[above text]
↓
Rewritten (~14 tokens):
Role: Java refactoring assistant.
Output: code only, no explanations.
---
[code]

Token delta: -38 tokens (-73%)

CACHING RECOMMENDATION
----------------------
Cacheable prefix: yes, after removing the date
Action: move date to user turn
```

---

## Example 2 — SKILL.md Validation

User pastes a SKILL.md with:
```
description: A skill that helps with code review tasks.
```

Output:
```
VALIDATION SCORE: 41/100 — Poor

CRITICAL ISSUES
---------------
Description too vague: no WHEN, no trigger phrases
  → "Review code for bugs, style, and performance. Use when user
     pastes code and asks for review, feedback, or improvements —
     even if they don't say 'review'."
Missing "Do NOT trigger for" section
  → Add routing alternatives (e.g. architecture questions → system-design skill)
Missing Input / Output contract in body
  → Add to each action block

STRUCTURAL GAPS
---------------
No template naming pattern for output files
  → Add: {project-root}/reviews/[prefix]-[content-name]-[YYYY-MM-DD].md
```
