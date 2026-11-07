"""Scenario: <one line: what this checks>.   READ-ONLY (say here if it changes anything; such a scenario also needs a --write flag).

Needs the build open and signed in via browser-login. Never handles credentials.
Run:  python <this file> [--cancel] [--close]
Exit: 0 all checks passed, 1 a check failed, 2 not run (Chrome unreachable, or host not allowed). RESULT is always printed.
"""
import os
import sys
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright, expect

URL = "<page url>"
ALLOWED_HOSTS = {"<host of the build this scenario may touch>"}   # checks the start URL's host only
CDP_PORT = int(os.environ.get("SCENARIO_CDP_PORT", "9222"))   # Claude: 9222 (default); agy sets its own port, see docs/agent-provenance.md
LOAD_WAIT_MS = 15_000
results = []


def step(name, fn):
    """Run fn; any exception is a FAIL with its first line. Returns True on PASS."""
    try:
        fn()
        results.append((name, True))
        print("PASS " + name)
        return True
    except Exception as e:
        results.append((name, False))
        print(f"FAIL {name} - {str(e).splitlines()[0] if str(e) else type(e).__name__}")
        return False


def finish(code=None):
    failed = [r for r in results if not r[1]]
    if code is None:
        code = 1 if failed else 0
    label = {0: "PASS", 1: f"FAIL ({len(failed)} of {len(results)} checks)", 2: "NOT RUN"}[code]
    print("\nRESULT:", label)
    sys.exit(code)


def open_page(page):
    page.goto(URL)
    if "/auth/realms/" in page.url or "login.microsoftonline.com" in page.url:   # a sign-in page: fail at once
        raise Exception("signed out: run browser-login for <build>")


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
        page = browser.contexts[0].new_page()

        # Step 1: the page is up and you are signed in.
        # exact=True on names; check inside the element you opened (a dialog, a panel), never page-wide, and wait with expect().
        # Number checks uniquely (2, 3.1, 3.2 ...) and never renumber a published one.
        ok = step("1 page loaded", lambda: (
            open_page(page),
            expect(page.get_by_role("button", name="<a button shown once signed in>", exact=True)).to_be_visible(timeout=LOAD_WAIT_MS),
        ))

        if ok:
            # ok2 = step("2 dialog opened", lambda: (
            #     page.get_by_role("button", name="...", exact=True).click(),
            #     expect(page.get_by_role("dialog")).to_be_visible(timeout=10_000)))
            # if ok2:
            #     step("3.1 option shown", lambda: expect(page.get_by_role("dialog").get_by_text("...", exact=True)).to_be_visible(timeout=5_000))
            # if "--cancel" in sys.argv:
            #     step("4 cancelled", lambda: (page.get_by_role("button", name="Cancel").click(),
            #                                  expect(page.get_by_role("dialog")).to_be_hidden(timeout=10_000)))
            pass

        if "--close" in sys.argv:
            page.close()
except Exception as e:   # SystemExit passes through
    results.append(("unexpected error", False))
    print(f"FAIL unexpected error - {str(e).splitlines()[0][:120] if str(e) else type(e).__name__}")

finish()
