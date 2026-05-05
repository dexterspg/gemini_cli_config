# QA Engineer: Tool Selection Catalog

## By Primary Goal
| Goal | Recommended Tool |
|------|-----------------|
| UI testing | **Playwright** (fast) or **Cypress** (visual) |
| Browser automation | **Playwright** (code) or **n8n** (visual) |
| API testing (CI) | **Jest + Supertest** (JS) or **Pytest + HTTPX** (Python) |
| API testing (Manual) | **Postman** / **Newman** (CI) |
| Integrations | **n8n** (self-hosted) or **Zapier/Make** (SaaS) |
| Scheduled jobs | **n8n** (visual) or **Prefect** (code) |
| Data pipelines | **Apache Airflow** |
| Long-running tasks | **Temporal** (crash-proof) |
| Performance | **k6** (JS), **Locust** (Python), **JMeter** (GUI) |

## By Stack
| Project Stack | Unit/Integration | API | E2E |
|---|---|---|---|
| Python | pytest | pytest + HTTPX | Playwright (Python) |
| Java Spring Boot | JUnit 5 + Mockito | RestAssured / MockMvc | Selenium / Playwright |
| JS/TS | Jest / Vitest | Jest + Supertest | Playwright / Cypress |
| OpenAPI Spec | — | Schemathesis | — |

## By Task Duration
| Duration | Pattern | Recommendation |
|---|---|---|
| < 30s | Sync REST | Any |
| 1-30m | Async + Callback | n8n / Prefect |
| 30m - 2h | Resumable State | Prefect |
| 2h - Days | Durable History | Temporal |

## By Team
| Team Type | Recommendation |
|---|---|
| Solo (Code) | Playwright + Prefect |
| Solo (Visual) | n8n + Playwright |
| Mixed | n8n sub-workflows + Playwright POM |
| Non-technical | n8n or Zapier/Make |

## API Testing Layer
| Tool | Purpose |
|---|---|
| **Optic** | Break CI on breaking spec changes |
| **Schemathesis** | Find spec-code drift via fuzzing |
| **json-server** | Quick fake REST API from JSON |
| **MSW** | Intercept API calls inside browser |
| **WireMock** | Full team mock server (Docker) |

## Reporting
| Tool | Plugin |
|---|---|
| Playwright | allure-playwright |
| Cypress | allure-cypress |
| Jest | jest-circus + allure-jest |
| Pytest | allure-pytest |
| Newman | allure-newman reporter |
