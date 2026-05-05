---
name: tdd
description: 'Full test-driven development workflow for implementing new features or fixing bugs. Use this whenever someone is about to write code for something new — implementing a feature, starting on a slice from the task plan, building a module, or fixing a bug properly. Trigger phrases include "implement X", "build X", "add feature", "starting on slice N", "I want to do this properly with tests first", "test driven development", "TDD", "kicking off development on", or beginning any new coding task. Also triggers when docs/task-plan.md exists and dev is starting. Do NOT trigger for reviewing existing tests, setting up test frameworks (jest, pytest config), refactoring code where tests already exist, debugging CI/CD pipelines, or explaining testing concepts.'
---

# Test-Driven Development

## The Iron Law
**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**
Delete code written before its test. No exceptions.

---

## Step 0: Planning
1. **Source:** Read `docs/task-plan.md` slice criteria.
2. **Behavior:** ID the first public behavior to test.
3. **Approve:** User confirms public interface and priority behaviors.

---

## Vertical Slicing (Tracer Bullet)
ONE test → ONE implementation → REFACTOR. Repeat.
Never write multiple tests or multiple implementations at once (Horizontal Slicing).

---

## Red-Green-Refactor

### RED — Failing Test
- Write ONE test for ONE behavior through public interface.
- **Verify:** Run test; confirm it FAILS for the right reason.

### GREEN — Minimal Code
- simplest code to pass. No YAGNI/anticipation.
- **Verify:** Run all tests; confirm all pass.

### REFACTOR — Clean Up
- Improve names, remove duplication, extract helpers.
- Never refactor while RED.

---

## Mocking Rules
Refer to `references/mocking.md` for boundary rules and test double types.

---

## Workflow Checklist
- [ ] Describes behavior, not implementation detail.
- [ ] Uses public interface only; survives internal refactors.
- [ ] Watched test FAIL before implementation.
- [ ] Minimal code only.
- [ ] Mocks at system boundaries only.
