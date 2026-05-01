---
name: qa-engineer
description: >
  QA automation architecture and tool selection skill. Read this before designing any test automation
  system, choosing tools, scaffolding a test suite, adding a CI pipeline, or deciding between
  Playwright and Cypress, Jest and Pytest, n8n and Prefect, or any other tool combination.
  Triggers when the user mentions: "set up testing", "automate tests", "UI testing", "E2E tests",
  "API testing", "test pipeline", "CI test setup", "test stack", "which test tool", "Playwright",
  "Cypress", "test automation", "mock data", "contract testing", "Allure", or "load testing".
  Use this even if the user has not used those exact words — any request involving test
  architecture or tooling decisions should consult this skill first.
---

## Purpose

This skill guides tool selection, stack combination, and architecture decisions before any test
code is written. The agent-qa-engineer uses its own code patterns for implementation — this skill
answers the upstream question: what to build and with which tools.

---

## Step 1 — Clarify Before Deciding

Confirm these four things before recommending anything:

1. **Primary goal** — UI testing, API testing, browser automation, scheduling, connecting services, or all of the above?       
2. **Stack** — what language/framework does the project use? (Python, Java Spring Boot, Node/JS, other)
3. **Task duration** — will any automation task run longer than 30 seconds?
4. **Team** — solo technical user, mixed team, or non-technical users who need a visual interface?

---

## Step 2 — Tool Selection by Context

### By Primary Goal

| Goal | Recommended Tool |
|------|-----------------|
| UI testing — assertions, regressions, state verification | **Playwright** (multi-browser, fast) or **Cypress** (visual reports, DX) |
| Browser automation — form filling, data entry, clicking | **Playwright** (code) or **n8n** (no code, visual) |
| API testing — automated assertions in CI | **Jest + Supertest** (JS) or **Pytest + HTTPX** (Python) |
| API testing — manual exploration | **Postman** |
| Run Postman collections in CI | **Newman** |
| Connecting apps and services | **n8n** (self-hostable visual) or **Zapier/Make** (SaaS, non-technical) |
| Scheduled/background jobs | **n8n** (visual scheduling) or **Prefect** (Python, code-based) |
| Enterprise data pipelines | **Apache Airflow** |
| Mission-critical, crash-proof long tasks | **Temporal** |
| Load/performance testing | **k6** (JS, dev-friendly), **Locust** (Python), **JMeter** (enterprise/GUI) |

### By Stack

| Project Stack | Unit/Integration | API | E2E |
|---|---|---|---|
| Python | pytest | pytest + HTTPX | Playwright (Python) |
| Java Spring Boot | JUnit 5 + Mockito | RestAssured or MockMvc | Selenium or Playwright (Java) |
| JavaScript/TypeScript | Jest or Vitest | Jest + Supertest | Playwright or Cypress |
| Any (OpenAPI spec exists) | — | Schemathesis (auto-generates from spec) | — |

### By Task Duration

```
Under 30 seconds    →  Synchronous REST call fine. Any tool.
1–30 minutes        →  Async + callback pattern. n8n or Prefect.
30 min – few hours  →  Prefect (state saved per task, survives restart)
Hours to days       →  Temporal (durable, event-history replay, used by Stripe/Uber)
Days or indefinite  →  Temporal only
```

**The async rule:** Any task over 30 seconds must NEVER use a synchronous HTTP call.
The correct pattern is always: submit → get jobId immediately → run in background → callback or poll when done.

### By Team

| Team type | Recommended |
|-----------|------------|
| Solo technical, prefer code | Playwright + Prefect |
| Solo technical, prefer visual | n8n + Playwright |
| Mixed team (some non-technical) | n8n sub-workflows + Playwright POM |
| Non-technical only | n8n or Zapier/Make |
| QA engineers / other developers | Playwright or Cypress + Newman |

---

## Step 3 — Pick a Stack Combination

| Scenario | Stack |
|----------|-------|
| Solo, simple tasks | n8n + Playwright + GitHub Actions |
| Solo, complex resumable flows | Prefect + Playwright + GitHub Actions |
| Full test suite (API + browser) | Jest/Pytest + Playwright + Newman — both in CI |
| Team sharing, mixed levels | n8n sub-workflows + Playwright POM + n8n Cloud |
| Spring Boot trigger, short task | Spring Boot webhook → n8n → Playwright |
| Spring Boot trigger, long task | Spring Boot → RabbitMQ → Prefect + Playwright |
| Mission-critical, cannot fail | Temporal + Playwright + RabbitMQ |
| API-driven browser testing | n8n + Playwright + json-server |
| Full enterprise | Prefect + Playwright + n8n + MSW + RabbitMQ |

---

## Browser Layer — Playwright vs Cypress

**Choose Playwright when:**
- Multi-browser testing is needed (Chrome, Firefox, WebKit)
- Speed matters — Playwright is faster
- Python or Java stack (Playwright supports all three languages)
- Need browser automation beyond testing (form filling, data entry)
- Team prefers code-first approach

**Choose Cypress when:**
- Visual test reports are the priority (time-travel debugger, screenshots built-in)
- Developer experience and hot reload during test writing matter most
- Project is already using Cypress

**Skip Puppeteer** — Playwright does everything Puppeteer does and adds multi-browser support.

### Playwright Page Object Model (POM) — use for any non-trivial E2E suite

```python
# pages/login_page.py
class LoginPage:
    def __init__(self, page):
        self.page = page

    async def login(self, user: str, password: str):
        await self.page.fill('#username', user)
        await self.page.fill('#password', password)
        await self.page.click('#submit')

# tests/test_checkout.py
async def test_checkout(page):
    login = LoginPage(page)
    await login.login('user@test.com', 'pass')
    # continues with checkout steps
```

POM makes browser steps reusable — teammates import and compose them without touching the underlying selectors.

### Playwright in CI (GitHub Actions — recommended starting point)

```yaml
# .github/workflows/e2e.yml
- name: Install Playwright
  run: npx playwright install --with-deps
- name: Run E2E tests
  run: npx playwright test
- uses: actions/upload-artifact@v3
  if: failure()
  with:
    name: playwright-report
    path: playwright-report/
```

Playwright runs headless — no display server needed. Free tier: 2000 min/month for private repos.

For managed cloud browser execution, connect to **Browserless.io**:
```js
await chromium.connect('wss://chrome.browserless.io?token=YOUR_TOKEN')
```

---

## API Testing Layer

### Two separate layers — test independently

```
Layer 1: API (no browser)
  Tools:  Jest + Supertest  /  Pytest + HTTPX  /  RestAssured
  Tests:  status codes, response shape, error handling, auth, edge cases
  Speed:  milliseconds per test — run on every commit

Layer 2: Browser (uses the API)
  Tools:  Playwright  /  Cypress
  Tests:  user flows, UI state, form submissions, end-to-end scenarios
  Speed:  seconds per test — run on every commit or scheduled
```

When a test fails, knowing which layer failed immediately tells you where the problem is.

### Contract Testing — catching breaking API changes

Use when your project has an OpenAPI/Swagger spec. Catches breaking changes before they reach production.

| Tool | What It Catches | When to Use |
|------|----------------|-------------|
| **Optic** | spec v1 vs spec v2 — classifies breaking vs non-breaking. Best CI integration. | Add now if OpenAPI spec exists |
| **Schemathesis** | spec vs live API behavior — finds spec-code drift, auto-generates edge case inputs | Add now if OpenAPI spec exists |
| **openapi-diff** | raw diff of two specs, no classification | Lightweight alternative to Optic |
| **Pact** | what consumers use vs what provider offers — consumer-driven | Later, at team scale, both sides must adopt |      

**CI pipeline order for contract testing:**
1. Optic (breaks pipeline on breaking spec change — fast gate)
2. Schemathesis (finds live API drift against staging)
3. Pact verification (if adopted)
4. Jest/Pytest/Newman (regular assertions)
5. Playwright/Cypress (browser layer)

### Mock Data Tools

| Tool | Use When |
|------|----------|
| **json-server** | Quick fake REST API from a JSON file — `npx json-server db.json` |
| **MSW (Mock Service Worker)** | Intercept API calls inside the browser — Playwright test looks identical for real and mock | 
| **WireMock** | Full team mock server via Docker — all teammates point apps at it |
| **n8n Set node** | Static mock values inline inside a workflow — no extra tool needed |

**Critical mock rule:** Mock data MUST have the same shape as the real API response. Shape mismatches cause tests that pass on mock and break on real API.

**Mock/real switching pattern:**
```
USE_MOCK = true/false  (environment variable)
    ├── true  →  Set node / json-server / MSW (mock data)
    └── false →  HTTP Request (real API)
              both feed the same downstream nodes unchanged
```

---

## Orchestration Layer

Only add orchestration when tests need scheduling, resumability, team sharing, or Spring Boot integration. For a pure test suite running in CI, the test runner (Playwright, Jest, pytest) is sufficient.

| Tool | Use When |
|------|----------|
| **n8n** | Visual scheduling, webhook triggers, non-technical team sharing, 400+ integrations |
| **Prefect** | Python-native, resumable flows, task caching, survives server restart |
| **Apache Airflow** | Team or enterprise scale, batch pipelines, complex DAG scheduling |
| **Temporal** | Tasks running hours to days, must survive crashes and server restarts |
| **Zapier / Make** | Non-technical users, SaaS-to-SaaS connections, zero setup |

### Sharing workflows with teammates

```
Non-technical colleagues reuse steps   →  n8n sub-workflows (Execute Workflow node)
Technical colleagues import steps      →  Prefect subflows (imported as Python functions)
Colleagues reuse browser steps         →  Playwright POM (imported as classes)
Colleagues trigger runs from dashboard →  n8n or Prefect UI (click-to-run)
Colleagues reuse cached output         →  Prefect task cache (skips already-completed steps)
```

---

## Spring Boot Integration

### Which pattern to use

```
Does Spring Boot need the result back?
    ├── YES, task < 30s    →  Synchronous REST POST (Spring Boot waits)
    ├── YES, task > 30s    →  Async REST + callbackUrl
    │                          Step 1: POST, receive jobId immediately
    │                          Step 2: automation runs in background
    │                          Step 3: automation POSTs to callbackUrl when done
    ├── NO, low volume     →  Webhook → n8n Webhook Trigger (zero code on n8n side)
    ├── NO, high volume    →  RabbitMQ or Kafka message queue
    └── Batch / large data →  Shared DB — Spring Boot writes, automation polls
```

### Spring Boot code patterns

```java
// Async REST — fire and forget, result comes back via callback
webClient.post()
    .uri("http://automation-service/trigger")
    .bodyValue(Map.of(
        "workflow",    "loginTest",
        "callbackUrl", "https://myapp/automation/result"
    ))
    .retrieve().toBodilessEntity()
    .subscribe();  // does not block Spring Boot thread

// Webhook to n8n — simplest option
webClient.post()
    .uri("https://n8n-instance/webhook/run-automation")
    .bodyValue(payload)
    .retrieve().toBodilessEntity()
    .subscribe();

// RabbitMQ (Spring AMQP)
rabbitTemplate.convertAndSend("automation.exchange", "workflow.loginTest", payload);

// Receive callback result
@PostMapping("/automation/result")
public ResponseEntity<Void> receiveResult(@RequestBody AutomationResult result) {
    resultRepository.save(result);
    notificationService.notify(result);
    return ResponseEntity.ok().build();
}
```

---

## Cloud Deployment

### Fastest option per tool

| Tool | Fastest Cloud Option | Time | Cost |
|------|---------------------|------|------|
| n8n | n8n Cloud (SaaS) | 5 min | ~$20/mo |
| n8n | Railway.app (self-hosted Docker) | 15 min | Free / ~$5/mo |
| Prefect | Prefect Cloud (SaaS) | 5 min | Free tier |
| Playwright | GitHub Actions | 20 min | Free (2000 min/mo) |
| Playwright | Browserless.io (managed browser) | 10 min | Free tier |
| Cypress | Cypress Cloud (SaaS) | 10 min | Free tier |
| Airflow | Astronomer.io | 30 min | Paid |
| Temporal | Temporal Cloud | 30 min | Usage-based |
| RabbitMQ | CloudAMQP | 10 min | Free tier |

### Recommended starting stack (solo, $0)

1. Sign up at n8n Cloud free trial — builds workflows visually, runs 24/7, no server
2. Push Playwright scripts to GitHub, add GitHub Actions workflow file
3. n8n triggers GitHub Actions via webhook when needed

### Self-hosted cloud options (when you want control)

| Platform | Best For | Cost |
|----------|---------|------|
| Railway.app | n8n Docker, json-server, custom services | Free / ~$5/mo |
| Render.com | Small APIs, free tier | Free tier |
| Fly.io | Containers needing more config | Free tier |
| Hetzner VPS | Full Linux control, lowest cost | ~$5/mo |
| DigitalOcean | Beginner-friendly, good docs | ~$6/mo |

---

## CI/CD Pipeline Architecture

Full recommended pipeline order (add layers as the project grows):

```
1. Optic               — spec v1 vs v2 breaking change gate (fast, blocks everything else)
2. Schemathesis         — spec vs live API, edge case fuzzing
3. Pact verification   — consumer contracts (if adopted)
4. Jest / Pytest / Newman  — regular API assertions
5. Playwright / Cypress    — browser layer E2E
6. Allure report        — unified dashboard from all layers above
```

---

## Reporting — Allure

Add Allure when running multiple test layers. Single-tool projects don't need it — the tool's own report is enough.

Allure provides: pass rate trend (30 days), flaky test detection, slowest tests, screenshots on failure, one shareable URL for the whole team.

| Tool | Allure Plugin |
|------|--------------|
| Playwright | allure-playwright |
| Cypress | allure-cypress |
| Jest | jest-circus + allure-jest |
| Pytest | allure-pytest |
| Newman | allure-newman reporter |
| Schemathesis | `--report allure` flag (built-in) |

---

## 80/20 — What to Learn or Build First

| Priority | What | Why |
|----------|------|-----|
| 1st | HTTP request/response — what an API returns (JSON) and how to pass it forward | Foundation for everything else |       
| 2nd | Playwright: `page.goto()`, `page.click()`, `page.fill()`, `expect()` | Covers 80% of browser automation |
| 3rd | n8n core: Trigger, IF, HTTP Request, Execute Workflow nodes | These 4 nodes handle most visual workflows |
| 4th | Data mapping between nodes — output of Node A becomes input of Node B | Biggest source of bugs |
| 5th | Async pattern: submit → get jobId → poll or callback | Required the moment any task exceeds 30 seconds |
| 6th | `USE_MOCK=true/false` environment switch | Real vs mock pattern used everywhere |
| 7th | Prefect `@task`, `@flow`, `cache_key_fn` | Unlocks resumable and cached workflows |
| 8th | Page Object Model (POM) in Playwright | Reusable browser components for team sharing |
| 9th | Message queues: publish → consume | Required for high volume or Spring Boot integration |
| 10th | OpenAPI spec basics | Required before using Schemathesis or Optic |
