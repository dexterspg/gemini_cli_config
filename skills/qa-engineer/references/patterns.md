# QA Engineer: Implementation Patterns

## Playwright POM (Page Object Model)
Use for non-trivial E2E suites to make steps reusable.

```python
# pages/login_page.py
class LoginPage:
    def __init__(self, page): self.page = page
    async def login(self, user, pwd):
        await self.page.fill('#username', user)
        await self.page.fill('#password', pwd)
        await self.page.click('#submit')
```

## Playwright in CI (GitHub Actions)
```yaml
- name: Run E2E tests
  run: npx playwright test
- uses: actions/upload-artifact@v3
  if: failure()
  with:
    name: playwright-report
    path: playwright-report/
```

## Spring Boot Async REST Pattern
Submit job -> Receive JobId -> Callback when done.

```java
webClient.post()
    .uri("http://automation/trigger")
    .bodyValue(Map.of("workflow", "test", "callbackUrl", "https://app/result"))
    .retrieve().toBodilessEntity()
    .subscribe();
```

## Mock/Real Switching Pattern
```
USE_MOCK = true/false (env var)
  ├── true  → Set node / MSW (mock)
  └── false → HTTP Request (real)
```
