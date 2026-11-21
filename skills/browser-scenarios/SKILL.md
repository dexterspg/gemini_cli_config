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

**Dependencies:** Python Playwright (`playwright==1.58.0`), Google Chrome (`start-chrome.ps1` resolves `CHROME_BIN`, `Program Files`, `Program Files (x86)`, and `LocalAppData`). Windows and PowerShell / Git Bash.

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
- **Mandatory lint check:** run `python recon/lint_browser_scenarios.py` (and verify `rg -n -i "keyring|get_password|#password" <project>/scenarios/browser ~/.gemini/skills/browser-scenarios/scripts` finds nothing) after creating or editing a scenario; it must exit `0`.

## Write one

1. **Draft the brief in the docstring:** Copy `~/.gemini/skills/browser-scenarios/scripts/scenario-template.py` into the project's `scenarios/browser/` folder and fill in the 4-line `Brief:` block (`Build/product`, `Start page`, `Steps`, `Expect`, `Data needed`; skip `Brief:` when a runbook already lists the steps), `URL`, `ALLOWED_HOSTS`, and steps.
2. **Read cached page maps first:** Check `<project>/scenarios/browser/pages/<product>.md` and `~/.gemini/skills/browser-scenarios/references/quasar-page-maps.md` before probing a screen so known selectors (`#id`, `v-css-selectors`, Quasar portals) are reused immediately.
3. **Probe in a single pass (never inline `python -c`):** Never run ad-hoc `python -c "..."` one-liners in PowerShell to guess selectors (avoids quote-escaping errors and multi-turn trial-and-error). Instead, run `python ~/.gemini/skills/browser-scenarios/scripts/probe.py <url> --out <scratch_dir>` (or `--active-tab` / `--quasar` to inspect the currently open screen/dialog in <0.5s without reloading) and read only the generated `snapshot.yml` (scoped ARIA snapshot), `buttons.txt` / `widgets.txt` (indexed `#id`, `v-css-selectors`, `.q-field`, `.q-expansion-item`, `.q-badge`, and icon buttons), or `calls.txt` (note: `calls.txt` lists the app's own internal calls as well as public API calls; check the project's `scenarios/browser/README.md` before treating a call as a public endpoint).
4. **One tab per product & screen-order discipline:** Reuse the open tab for each product (`product_tab(browser, URL)` from `_helpers.py`, never `browser.contexts[0].new_page()`). Order checks by screen: visit each screen once and run all its checks there; go back to a screen only to verify state after an action, with a `# revisit: <reason>` comment (a guard that re-opens a page so a single `--step N` can run alone is not a revisit).
5. **Number checks uniquely:** Use `1`, `2`, `3.1`, `3.2` and never renumber a published check. Scenario facts (URLs, expected values, ticket numbers) go in the project's file, never in this skill.
6. **Lint and catalog:** Add a row to `<project>/scenarios/browser/README.md`, run `python recon/lint_browser_scenarios.py` until it exits `0`, and commit only with user permission per Git Commit Rules.

## Walkthrough Scenarios, Professional Callout Highlights & `--docx` Export

When authoring or running a scenario intended for user walkthroughs, visual demonstrations, or live step-by-step UI inspections (importing from the project's `scenarios/browser/_walkthrough.py`):
1. **Default Professional Callout Overlays (Unclipped Floating Box + Numbered Pill Badge + Click-Target Beacon):**
   - Render a floating overlay container on `document.body` (`position: fixed`, `z-index: 2147483647`, `pointer-events: none`, `data-scenario-callout="true"`) using `el.getBoundingClientRect()` so `overflow: hidden` on `.q-table`, rows, or modal containers never clips the `4px solid <color>` border or `0 0 18px <color>` glow.
   - Attach a high-contrast **Numbered Callout Pill Badge** (`label="[1] ..."`, `badge_pos="top"|"bottom"|"right"`) with luminance-aware text color so every screenshot is self-documenting.
   - Include a **Scribe-style Click-Target Bullseye Beacon** (`click_target=True`) on interactive click/check targets.
   - **Zero-Token Auto-Step & Callout Generator (`ui_given`, `ui_fill`, `ui_check`, `ui_click`, `ui_verify`):** Import from `_walkthrough.py` (do not paste the helper code into a scenario) so callout labels (`[N] GIVEN: <Landmark>`, `[N] WHEN Type: '<value>'`, `[N] WHEN Check: <Label>`, `[N] WHEN Click: '<Label>'`, `[N] THEN Verify: <Field> = '<Value>'`), sequence numbers, semantic colors, and `.docx` highlight legends are introspected directly from the live DOM at runtime for 0 LLM tokens.
2. **Pre-Capture Visual Hygiene:**
   - Dismiss open search popups or dropdown menus from previous steps before capturing the next screen.
   - Scroll modal inner containers (`scroll_into_view_if_needed()`) and wide tables (`scrollIntoView({inline: 'center'})`) so target fields and right-hand status columns are visible before drawing callouts.
   - Move the mouse to `(0, 0)` (`park_mouse(page)`) before taking screenshots so floating hover tooltips never cover UI elements.
3. **State Persistence & Cleanup:**
   - Mark floating overlays with `data-scenario-callout="true"` (and any inline element styles with `data-scenario-highlight="true"`).
   - Clear previous step highlights using `clear_highlights(page)` before highlighting new elements, and remove all overlays on the final step or on `--cancel` so they never stay in the user's tab.
4. **Step-by-Step & Resumable Flags (`--step <N>`, `--pictures-from`, `--first-picture`, `SCENARIO_FAIL_SHOTS`):**
   - Provide `--step <N>` (`wants_step("N")`) so walkthroughs can run one step at a time. For multi-stage `--write` flows, support checking the last finished run when run read-only and resuming a partial run (`--invoice-id=<id>`, `--pictures-from=<step>`, `--first-picture=<N>`) without repeating completed writes, plus saving failure screenshots when `SCENARIO_FAIL_SHOTS` is set.
5. **Optional Word Document Export (`--docx` / `--doc`):**
   - Provide `--docx` support (`capture_step()` and `build_docx()`) that writes a formatted `.docx` report into `docs/runbooks/evidence/<slug>-walkthrough.docx` (own builds only; stays uncommitted until the user says so).
6. **Standard Semantic Palette:**
   - Cyan / Blue (`#00bcd4` / `#2196f3`): Structural headers, table boundaries, and navigational landmarks.
   - Orange / Amber (`#ff9800`): Selected rows, search results, and filter groups.
   - Green (`#00e676`): Confirmed/Posted state and primary action buttons.
   - Red / Orange-Red (`#ff3d00`): Open/Pending state, unacknowledged records, and alerts.
   - Pink (`#ff007f`): Checkboxes, toggles, and filter chips.
   - Gold (`#ffd700`): SAP Document numbers, external reference keys, and audit IDs.

## API-to-UI mode (check a saved API run on screen)

A scenario named `api-ui-<flow>.py` reads a `CONFIRMED` Hurl flow's saved `variables.properties` and `responses/` and checks the same values on the screens:
- **Three layers must agree:** what the flow sent (`variables.properties`), what the API stored and returned (`responses/*.json`), and what the UI screens display.
- **Scope & Bulk Cap:** check every request-body field, only the important response fields (state, ids, amounts, status), and cap lists at N items (`--cap N`, default 5, printing `"checked N of M"` via `cap_sample()`). It never calls the API or writes.
- **Shared Helpers & Negative Control:** import `Run`, `cap_sample`, `norm`, `money`, and `missing` from the project's `scenarios/browser/_apiui.py` (exits `2` if no saved run exists). After writing an `api-ui-<flow>.py` scenario, run a **negative control** (corrupt one saved value, verify the scenario fails on it, then restore the file). When a Hurl flow first turns `CONFIRMED`, offer once to add its `api-ui-<flow>.py` alongside the Postman offer.
