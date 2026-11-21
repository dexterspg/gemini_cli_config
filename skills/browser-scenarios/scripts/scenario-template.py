"""Scenario: <one line: what this checks>.   READ-ONLY (say here if it changes anything; such a scenario also needs a --write flag).

Brief (the AI drafts it from the Hurl flow or runbook; you edit; skip it when a runbook already lists the steps):
  Build/product: <build> <product>     Start page: <url>
  Steps: <1. ... 2. ...>               Expect: <what shows at the end>
  Data needed: <ids, or the Hurl script that creates them; blank = none>

Needs the build open and signed in via browser-login. Never handles credentials.
Run:  python <this file> [--step <N>] [--docx] [--cancel] [--close]
Exit: 0 all checks passed, 1 a check failed, 2 not run (Chrome unreachable, or host not allowed). RESULT is always printed.
"""
import os
import sys
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, expect
from _helpers import step, finish, results, clear_stale_overlays, product_tab
from _walkthrough import *

URL = "<page url>"
ALLOWED_HOSTS = {"<host of the build this scenario may touch>"}   # checks the start URL's host only
CDP_PORT = int(os.environ.get("SCENARIO_CDP_PORT", "9222"))   # Claude: 9222 (default); agy sets its own port, see docs/agent-provenance.md
LOAD_WAIT_MS = 15_000


def open_page(page):
    page.goto(URL)
    if "/auth/realms/" in page.url or "login.microsoftonline.com" in page.url:   # a sign-in page: fail at once
        print("signed out: run browser-login for <build>")
        finish(2)
    clear_stale_overlays(page)


if urlparse(URL).hostname not in ALLOWED_HOSTS:
    print("Refusing to run: the URL's host is not in ALLOWED_HOSTS.")
    finish(2)

if CDP_PORT == 9222 and "api-test-app-agy" in os.getcwd().replace("\\", "/"):   # agy's workspace: 9222 is Claude's Chrome
    print("Refusing to run: agy must set SCENARIO_CDP_PORT=9223 (9222 is Claude's Chrome).")
    finish(2)

try:
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
        except Exception:
            print(f"Cannot reach Chrome on port {CDP_PORT}. Start Chrome with remote debugging on port {CDP_PORT}.")
            finish(2)
        page = product_tab(browser, URL)   # one tab per product: reuse the open one, never new_page()

        # Step 1: the page is up and you are signed in.
        # exact=True on names; check inside the element you opened (a dialog, a panel), never page-wide, and wait with expect().
        # Order checks by screen; revisit only after an action with `# revisit: <reason>`. Number checks uniquely (2, 3.1, 3.2 ...).
        if wants_step("1"):
            clear_highlights(page)
            ok = step("1 page loaded", lambda: (
                open_page(page),
                ui_verify(page.get_by_role("button", name="<a button shown once signed in>", exact=True)),
                park_mouse(page),
            ))
            capture_step(page, 1, "Page Loaded", "The landing page loads and verifies the signed-in action button.")

        if "--close" in sys.argv:
            page.close()
except Exception as e:   # SystemExit passes through
    results.append(("unexpected error", False))
    print(f"FAIL unexpected error - {str(e).splitlines()[0][:120] if str(e) else type(e).__name__}")

finish()
