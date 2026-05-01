# Checklist: Code Review

## Correctness
- [ ] [critical] All requirements from the spec fully implemented? *Fail: one or more FRs have no corresponding implementation.*
- [ ] Edge cases handled? *Fail: boundary values (empty, null, zero, max), concurrent access, or invalid state combinations not addressed.*
- [ ] Error handling surfaces failures to the caller? *Fail: exceptions caught but swallowed silently — caller has no way to know an operation failed.*
- [ ] Logic correct for the stated requirements? *Fail: algorithm produces wrong output for valid inputs; off-by-one errors; incorrect conditionals.*

## Security
- [ ] No secrets hardcoded or logged? *Fail: API keys, passwords, tokens, or connection strings appear in source code, config files, or log output.*
- [ ] User input validated at entry points? *Fail: raw user input passed directly to queries, file paths, commands, or serializers without sanitization.*
- [ ] Injection risks addressed? *Fail: SQL/command/template injection possible via string concatenation — use parameterized queries and safe APIs.*
- [ ] Auth/authorization enforced on all protected operations? *Fail: a caller can reach a protected resource or action without a valid identity or permission check.*
- [ ] Sensitive data protected in transit and at rest? *Fail: PII or credentials stored in plaintext, transmitted unencrypted, or included in error messages.*

## Testing
- [ ] [critical] New logic paths have test coverage? *Fail: a new branch, function, or behavior change has zero tests — no way to detect future regressions.*
- [ ] Tests assert on outcomes, not implementation details? *Fail: tests break when internal method names or structure changes but observable behavior is identical.*
- [ ] Tests cover failure paths, not just happy path? *Fail: only the success case is tested; error conditions and edge cases are untested.*

## Performance & Resources
- [ ] No obvious inefficiencies for the expected data scale? *Fail: O(n²) operation on potentially large inputs; repeated full-table scans; unnecessary re-computation in loops.*
- [ ] Resources properly cleaned up? *Fail: file handles, DB connections, or network sockets opened but not closed in error paths.*

## Conventions
- [ ] Follows project patterns established in the codebase? *Fail: deviates from naming conventions, file structure, or framework usage visible in adjacent files without documented reason.*
- [ ] No unnecessary duplication of existing logic? *Fail: implements logic already available in a utility or service in the same codebase.*

**Verdict guidance** (global default applies — see CHECKLISTS.md)
