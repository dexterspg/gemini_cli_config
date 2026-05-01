---
name: tdd
description: Full test-driven development workflow for implementing new features or fixing bugs. Use this whenever someone is about to write code for something new — implementing a feature, starting on a slice from the task plan, building a module, or fixing a bug properly. Trigger phrases include "implement X", "build X", "add feature", "starting on slice N", "I want to do this properly with tests first", "test driven development", "TDD", "kicking off development on", or beginning any new coding task. Also triggers when docs/task-plan.md exists and dev is starting. Do NOT trigger for reviewing existing tests, setting up test frameworks (jest, pytest config), refactoring code where tests already exist, debugging CI/CD pipelines, or explaining testing concepts.
---

# Test-Driven Development

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over. No exceptions.

---

## Step 0: Planning (ALWAYS DO FIRST)

Before writing any test:

**If `docs/task-plan.md` exists:**
- Read the current slice — note its acceptance criteria, layers touched, and HITL/AFK classification
- Use the slice acceptance criteria as the basis for your first test
- Do not start the next slice until the current one is complete and (if HITL) human-reviewed

**If `docs/task-plan.md` does not exist or has no acceptance criteria:**
- Ask the user to define the first behavior to test before proceeding

**Always confirm with user:**
- [ ] What should the public interface look like?
- [ ] Which behaviors matter most? (you cannot test everything — prioritize)
- [ ] Get user approval before writing the first test

---

## Anti-Pattern: Horizontal Slicing (NEVER DO THIS)

Writing all tests first, then all implementation is **horizontal slicing** — it produces bad tests.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5   ← all at once
  GREEN: impl1, impl2, impl3, impl4, impl5   ← all at once

RIGHT (vertical — tracer bullet):
  RED → GREEN → REFACTOR: test1 → impl1
  RED → GREEN → REFACTOR: test2 → impl2
  RED → GREEN → REFACTOR: test3 → impl3
```

**Why horizontal fails:**
- Tests written in bulk test imagined behavior, not actual behavior
- You commit to test structure before understanding implementation
- Tests pass when behavior breaks, fail when behavior is fine
- You outrun your headlights

**One test → one implementation → refactor → repeat. Always.**

---

## Red-Green-Refactor

### RED — Write a Failing Test

Write ONE test for ONE behavior through the public interface.

```typescript
// GOOD — tests behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});

// BAD — tests implementation detail
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

**Requirements:**
- One behavior per test
- Clear name that describes what the user can do
- Uses public interface only — never internal methods
- Test must survive internal refactors

**Verify RED — MANDATORY, never skip:**
- Run the test — confirm it FAILS
- Confirm it fails for the right reason (feature missing, not typo)
- Test passes immediately? You are testing existing behavior — fix the test

### GREEN — Minimal Code

Write the simplest code to make the test pass. Nothing more.

- No extra features, no over-engineering, no YAGNI
- Do not anticipate future tests
- Do not refactor other code

**Verify GREEN — MANDATORY:**
- Run all tests — confirm they ALL pass
- No errors, no warnings

### REFACTOR — Clean Up

Only after GREEN:
- Remove duplication
- Improve names
- Extract helpers
- Deepen modules (move complexity behind simple interfaces)

Never refactor while RED. Never add behavior during refactor.

---

## Behavior vs Implementation

**Tests must verify behavior through public interfaces — not implementation details.**

| Good test | Bad test |
|---|---|
| "user can log in with valid credentials" | "auth.validate() is called once" |
| Tests WHAT the system does | Tests HOW it does it |
| Survives internal refactors | Breaks when you rename a function |
| Uses public API only | Mocks internal collaborators |

**Warning sign:** your test breaks when you refactor but behavior hasn't changed → you were testing implementation.

---

## Mocking Rules

### Mock at system boundaries only

```
MOCK:                          DON'T MOCK:
[YES] External APIs            [NO] Your own classes/modules
[YES] Payment services         [NO] Internal collaborators
[YES] Email/SMS services       [NO] Anything you control
[YES] Time / randomness        [NO] Pure functions
[YES] File system (sometimes)  [NO] Domain logic
[YES] Databases (prefer test DB)
```

### Types of test doubles

| Type | What it does | When to use |
|---|---|---|
| **Stub** | Returns a fixed value, no verification | Replace slow/external dependency, don't care how it's called |
| **Mock** | Verifies it was called correctly | Assert a boundary was invoked (e.g. email was sent) |
| **Spy** | Wraps real implementation, records calls | Verify behavior while keeping real logic |
| **Fake** | Working simplified implementation (e.g. in-memory DB) | Integration tests needing realistic behavior without real infrastructure |

**Default:** Stub or Fake. Use Mock only when the call itself is the behavior being tested.

### Use dependency injection

```typescript
// GOOD — easy to mock at boundary
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// BAD — hard to mock, couples to implementation
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

### Use SDK-style interfaces over generic fetchers

```typescript
// GOOD — each function independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD — requires conditional logic inside mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

### Before mocking anything — ask:
1. What side effects does the real method have?
2. Does this test depend on any of those side effects?
3. Am I mocking at the right level (boundary) or too high?

---

## Full Workflow Per Slice

```
Read slice from task-plan.md (if exists)
        │
        ▼
Step 0: Plan
  - confirm interface and behaviors with user
  - get approval before writing first test
        │
        ▼
Tracer bullet: ONE test → ONE implementation → REFACTOR
(proves the path works end-to-end)
        │
        ▼
For each remaining behavior in the slice:
  RED      → write test (behavior, public interface, one thing)
           → verify it fails for the RIGHT reason
  GREEN    → minimal code to pass
           → verify all tests pass, no warnings
  REFACTOR → clean up after GREEN only, never while RED
        │
        ▼
Slice complete?
  HITL → complete slice, present to user, wait for approval before next slice
  AFK  → proceed to next slice autonomously
```

---

## Checklists

### Per Slice (before starting)
```
[ ] Read slice acceptance criteria (if task-plan.md exists)
[ ] Confirmed interface and behaviors with user
[ ] User approved the plan
[ ] HITL or AFK classification noted
```

### Per Cycle (RED-GREEN-REFACTOR)
```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Watched test FAIL before implementing
[ ] Wrote minimal code — nothing speculative
[ ] Watched test PASS after implementing
[ ] All other tests still pass
[ ] Mocks at system boundaries only (if any)
```

---

## Common Rationalizations — All Wrong

| Excuse | Reality |
|---|---|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll write tests after" | Tests written after pass immediately — proves nothing |
| "I already manually tested it" | Ad-hoc ≠ systematic. Can't re-run when code changes |
| "Deleting X hours of work is wasteful" | Sunk cost. Keeping unverified code is technical debt |
| "TDD will slow me down" | TDD is faster than debugging production |
| "Tests after achieve the same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |

## Red Flags — Stop and Start Over

- Code written before the test
- Test passes immediately without implementation
- Can't explain why the test failed
- Mocking everything just to make it pass
- "Just this once" thinking
