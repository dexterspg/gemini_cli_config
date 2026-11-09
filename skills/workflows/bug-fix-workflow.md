---
name: bug-fix
description: 'Standard loop for fixing confirmed bugs. Triggers: "fix bug in [X]", "why is [Y] broken?".'
---
# Bug Fix Workflow

## Flow

1. agent-debugger (root cause analysis)
2. agent-implementation-engineer (fix)
3. agent-qa-engineer (verify fix)
4. agent-quality-guardian (review)

## Routing

- APPROVED -> done
- CODE_ISSUE -> implementation-engineer (max 2 iterations)
- TEST_ISSUE -> qa-engineer (max 2 iterations)
- DIAGNOSIS_WRONG -> debugger (max 1 retry, then escalate to user)
- SECURITY_ISSUE -> implementation-engineer (max 1, then escalate to user)
- Any other issue type -> main session picks the route from the guardian's Issue Type table; BLOCKED -> escalate to user
- Send "iteration N of max" with every re-review; at the cap an open Critical is BLOCKED
