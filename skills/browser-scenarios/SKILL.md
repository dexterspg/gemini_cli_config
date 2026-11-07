---
name: browser-scenarios
description: >
  Run or write a replayable browser scenario as a Playwright script that attaches to an already-logged-in Chrome, instead of
  driving the browser step by step with screenshots (far fewer tokens, same checks every run). Triggers on: "run the browser
  scenario", "replay the browser scenario", "browser scenario", "script this browser flow", "Playwright replay", "attach to the
  logged-in Chrome". Do NOT trigger for a one-off look at a page (use the browser tools or /browser), for API calls (the project's API test
  tool), for a UI test suite a project already runs in CI, or for an API-flow "scenario" in a learning or evidence file.
---

# Browser scenarios

A scenario is one Python file: open a page, act, check what shows, print `PASS`/`FAIL` per step and a `RESULT` line. Exit 0 = all
passed, 1 = a check failed, 2 = not run (Chrome unreachable or host not allowed). Each project keeps its scenarios in a
`scenarios/browser/` folder; this skill holds only the technique and the rules.

**Dependencies:** Python Playwright (`playwright==1.58.0`), `keyring>=25.0.0`, Google Chrome (`start-chrome.ps1` resolves `CHROME_BIN`, `Program Files`, `Program Files (x86)`, and `LocalAppData`). Windows and PowerShell / Git Bash.

## `/browser` vs `browser-scenarios` (Decision Flow)

- **Use `/browser` (or one-off browser tools):** when you need a single interactive look at a page, visual layout inspection, or initial DOM discovery for a screen you have not scripted yet.
- **Use `browser-scenarios`:** whenever a check or UI workflow will be run more than once, cited as `Proof:` in a `UI logic` runbook, or used to verify a build regression with deterministic `PASS`/`FAIL`/`RESULT` output and zero screenshot token overhead.
- **Antigravity (`agy`) execution & model guidance:** use `/goal` when running multi-step autonomous scenario verification on `preview1` or `ra-env2`. For subagent delegation, `flash` suits fast read-only page discovery, while `pro` (or `inherit`) suits authoring multi-step stateful Playwright flows.

## Run one

1. Find the project's folder: glob `**/scenarios/browser/README.md`. None found: stop and ask.
2. The scenario Chrome is up when `curl -s http://127.0.0.1:9223/json/version` (with `SCENARIO_CDP_PORT=9223`) prints JSON. Down, or a scenario's first step
   failing: tell the user to log in via skill `browser-login` (`mod-login <build> [product]`). The AI never types, reads or stores
   credentials. A scenario never contains a login step.
3. Run the scenario with the terminal. Report only its `PASS`/`FAIL` lines and `RESULT`; screenshot only a failed step.

## Rules

- Which build a scenario runs on: per the project's README; none: ask.
- Your own builds by default. A client or production build only with the user's yes for that run, reads only. A Python script
  is not seen by any project hook that checks hurl or curl, so `ALLOWED_HOSTS` plus `python recon/lint_browser_scenarios.py` enforce the contract.
- Nothing that saves, submits or deletes by default. A scenario that must change data says so in its first docstring line, gates all writes behind a `--write`
  flag, and needs the user's yes before a mutating run. On shared R&D builds (`ra-env2`), pair `--write` with a `--cleanup` flag (for example, `Callback` → `Draft` → `Delete`) whenever the product state machine permits reversing the test record.
- A scenario leaves its tab, and any dialog it opened, open. `--cancel` cancels the dialog at the end; `--close` closes the tab.
- The scenario Chrome has a debugging port that any local process can attach to, and it holds the logins made in it. Use it only
  for the project's own builds: never sign in to email, SharePoint or other company apps in it, and close it when done. Its
  profile is `~/.gemini/browser-profile`: kept strictly local and git-ignored; never commit or copy it.
- **Selectors and Quasar / Vue SPA scoping (verified on `payable-ui` / `ra-env2`):**
  - Prefer role and visible text with `exact=True` and wait with `expect()`.
  - **Active dialog scoping:** dismissed Quasar dialogs leave their outer `.q-dialog` wrapper in the DOM and can leave an orphaned `.q-dialog__backdrop` that intercepts pointer events. Scope open dialogs to `.q-dialog__inner:visible` (never bare `.q-dialog`) and clear orphaned `.q-dialog__backdrop` nodes before clicking top-level action buttons.
  - **Portaled dropdown menus (`.q-menu:visible`):** Quasar `QSelect` and `ApInputPinnedSingleSelect` (such as `Cost Center *`) render their dropdown popup and server-side filter `<input>` inside `.q-menu:visible` attached to `document.body` *outside* the dialog DOM tree. Click the trigger inside `.q-dialog__inner:visible`, then filter and select options inside `.q-menu:visible`.
  - **Date popups and dependent selects:** typing a `YYYY-MM-DD` date into a Quasar date input opens a calendar popup that blocks adjacent fields unless dismissed with `Escape`. When a dropdown depends on a parent field (such as `Vendor *` after `Company *`), wait for the dependent field's company-scoped search to settle before opening its menu.
- **No scratch scripts in `scenarios/browser/`:** temporary probe scripts belong in `<appDataDir>/brain/<conversation-id>/scratch/` or a git-ignored `scratch/` directory, never inside `scenarios/browser/`.
- **Mandatory lint check:** run `python recon/lint_browser_scenarios.py` (and `rg -n -i "keyring|get_password|#password" <project>/scenarios/browser`) after creating or editing a scenario; it must exit `0`.

## Write one

1. Copy `~/.gemini/skills/browser-scenarios/scripts/scenario-template.py` into the project's `scenarios/browser/` folder and fill in
   the URL, `ALLOWED_HOSTS` and steps.
2. Number checks uniquely (`1`, `2`, `3.1`, `3.2`) and never renumber a published one. Scenario facts (URLs, expected values, ticket
   numbers) go in the project's file, never in this skill.
3. Add a row to `<project>/scenarios/browser/README.md`, run `python recon/lint_browser_scenarios.py` until it exits `0`, and commit the scenario and `README.md` under `scenarios/browser/` (after obtaining user permission per Git Commit Rules).
