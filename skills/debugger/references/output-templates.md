# Debugger: Output Templates

## `investigation.md`

Structure findings so the most actionable information comes first.

# Bug Investigation: [Brief Description]

## TL;DR
**Bug:** [One sentence — what is broken and why]
**Fix:** [One sentence — what to change]
**Files:** [exact file paths and line numbers]
**Status:** [Investigating / Root Cause Found / Fixed] | **Severity:** [Critical / High / Medium / Low]

## Fix
[Before/after code with `// [ADDED]` / `// [REMOVED]` markers on changed lines only.]

```
// before
[broken code]

// after
[fixed code]
```

## Root Cause
[One paragraph — why it occurs, what triggers it, consequence. No hypothesis trail.]

## Reproduction Steps
Environment: [exact version / env]
1. [Step]
2. [Step]
Expected: [what should happen]
Actual: [what happens instead]

## Ruled Out
- **[Theory]:** [one-sentence elimination]

## Investigation Trail
[Full hypothesis-by-hypothesis walkthrough for reference.]

---

## `debugging-walkthrough.md`

A teaching document showing the reasoning path from error to root cause.

# Debugging Walkthrough: [Brief Description]
**Error:** [verbatim error message]

## Step 1 — Read the error message literally
[What does it tell you directly? What are the branch points?]

## Step 2 — Find where the message is thrown
[Grep command and result.]

## Step 3 — Read the throwing code
[Paste code block. What triggers it?]

## Step 4 — Read the key method / validation logic
[Paste method. Break down data sources and checks.]

## Step 5 — Cross-reference with the logs
[Log lines confirming/ruling out the theory.]

## Conclusion
[Decisive evidence and what it proved.]

## Quick Reference for Future Debuggers
- Search term: `[exact grep string]`
- Key method: `[ClassName.methodName()]`
- Fastest confirmation: `[one SQL or log search string]`
