# TDD: Mocking Rules

## System Boundaries Only
```
MOCK:                          DON'T MOCK:
[YES] External APIs            [NO] Your own modules
[YES] Payment/Email services   [NO] Domain logic
[YES] Time / randomness        [NO] Pure functions
[YES] Databases (sometimes)    [NO] Anything you control
```

## Double Types
| Type | Use Case |
|---|---|
| **Stub** | Return fixed value (replace slow dependency) |
| **Mock** | Verify boundary call (e.g. email sent) |
| **Spy** | Record calls while keeping real logic |
| **Fake** | Simplified working impl (e.g. in-memory DB) |

## Dependency Injection
```typescript
// GOOD — mockable boundary
function pay(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// BAD — coupled implementation
function pay(order) {
  const client = new StripeClient(env.KEY);
  return client.charge(order.total);
}
```
