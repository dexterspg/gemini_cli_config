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
Guide tool selection, stack combination, and architecture before implementation. Implementation details belong in `references/patterns.md`.

---

## Step 1 — Clarification
Confirm before deciding:
1. **Goal:** UI, API, automation, or service connection?
2. **Stack:** Language/framework (Python, Java, Node)?
3. **Duration:** Any task > 30s? (Mandates async/callback pattern).
4. **Team:** Solo (code/visual), mixed, or non-technical?

---

## Step 2 — Selection Logic
Use `references/tools.md` to map context to recommendations.

**Key Decision Points:**
- **UI:** Playwright (fast/multi-browser) vs. Cypress (reports/DX).
- **Async Rule:** Tasks > 30s must use: Submit -> JobId -> Background -> Callback/Poll.
- **API Layer:** Test Milliseconds (independent) vs. User Flow Seconds (browser).

---

## Step 3 — Advanced Layers
Refer to `references/tools.md` for specific tools:
- **Contract Testing:** Catch breaking changes with Optic/Schemathesis.
- **Orchestration:** Use n8n (visual), Prefect (resumable), or Temporal (durable).
- **Reporting:** Use Allure for multi-layer unified dashboards.

---

## 80/20 — Priority Build
1. **HTTP Basics:** JSON request/response foundation.
2. **Playwright Core:** goto, click, fill, expect.
3. **n8n Core:** Trigger, IF, HTTP, Execute nodes.
4. **Data Mapping:** Passing Node A output to Node B.
5. **Async Pattern:** JobId + Callback (for > 30s tasks).

---

## Reference Locations
- **Tool Catalog:** `references/tools.md`
- **Code Patterns:** `references/patterns.md`
