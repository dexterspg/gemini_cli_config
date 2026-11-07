"""Open a build's product in the scenario Chrome, signing in first when the build allows it.

Run by the USER through a terminal. The AI does not run it, read the password or type it.
  python login.py preview1            -> the build's default product, in a NEW tab
  python login.py preview1 fos        -> that product, in a NEW tab (a short name or the full one); every open is a new tab
  python login.py preview1 list       -> the products and short names of that build, with the date they were probed
The builds and products come from C:/workarea/references/nakisa-products.md (env NAKISA_PRODUCTS_FILE overrides the path).
Keycloak builds: the password is read from Windows Credential Manager (service = the build) only when the login form shows.
Username: environment variable <BUILD>_USER (hyphens become underscores), else ~/.gemini/browser-profile/<build>-user.
Manual builds (company Microsoft sign-in): the page is opened and you sign in by hand; nothing is stored or filled.
Exit: 0 opened (signed in or already), 1 login did not complete, 2 not run. The password is never printed.
"""
import os
import re
import sys


def _unexpected(kind, value, tb):
    text = str(value).splitlines()[0][:120] if str(value) else ""
    print(f"login: unexpected error: {kind.__name__}: {text}")
    sys.stdout.flush()
    os._exit(2)


sys.excepthook = _unexpected

def _resolve_products_file():
    env_path = os.environ.get("NAKISA_PRODUCTS_FILE", "").strip()
    if env_path:
        return env_path
    candidates = [
        "C:/workarea/references/nakisa-products.md",
        os.path.expanduser("~/workarea/references/nakisa-products.md").replace("\\", "/"),
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    return candidates[0]


PRODUCTS_FILE = _resolve_products_file()
PRODUCT_HEADER = ["Product", "Short names", "UI segment", "API segment"]
BUILD_HEADER = ["Build", "Base URL", "Sign-in", "Default", "Products"]
# The Keycloak form, seen on preview1 and ra-env2: #username, #password, #rememberMe, #kc-login.


def fail(message):
    print(f"login: {message}: {PRODUCTS_FILE} (set env NAKISA_PRODUCTS_FILE to override)")
    sys.exit(2)


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table(lines, header):
    """The rows of the table whose header cells equal `header` exactly; every row must have that many cells."""
    start = next((i for i, ln in enumerate(lines) if ln.startswith("|") and cells(ln) == header), None)
    if start is None:
        fail("table with columns " + " | ".join(header) + " not found")
    rows = []
    for ln in lines[start + 2:]:   # skip the |---| line
        if not ln.startswith("|"):
            break
        row = cells(ln)
        if len(row) != len(header):
            fail(f"a row has {len(row)} cells, expected {len(header)} ({ln[:40]})")
        rows.append(dict(zip(header, row)))
    return rows


try:
    _lines = open(PRODUCTS_FILE, encoding="utf-8").read().splitlines()
except OSError:
    fail("products file missing or unreadable")
ALIASES = {}
for _r in table(_lines, PRODUCT_HEADER):
    for _s in _r["Short names"].split(","):
        if _s.strip():
            ALIASES[_s.strip()] = _r["UI segment"]
BUILDS = {}
for _r in table(_lines, BUILD_HEADER):
    _products = [x.strip() for x in _r["Products"].split(",") if x.strip()]
    if _r["Sign-in"] not in ("keycloak", "manual") or not _r["Base URL"].endswith("/") or _r["Default"] not in _products:
        fail(f"build {_r['Build']} has a bad Sign-in, Base URL or Default")
    BUILDS[_r["Build"]] = {"base": _r["Base URL"], "default": _r["Default"], "manual": _r["Sign-in"] == "manual", "products": _products}
AS_OF = next((ln.split(":", 1)[1].strip() for ln in _lines if ln.startswith("As of (builds):")), "undated")

args = [a for a in sys.argv[1:] if a != "--url"]
want_url = "--url" in sys.argv[1:]
build = args[0] if args else ""
product = args[1] if len(args) > 1 else ""
if build not in BUILDS:
    print(f"Unknown build '{build}'. Known builds: {', '.join(BUILDS)}.")
    sys.exit(2)
cfg = BUILDS[build]
if product == "list":
    short = ", ".join(f"{k}={v}" for k, v in ALIASES.items() if v in cfg["products"])
    print(f"{build} products: {', '.join(cfg['products'])}. Short names: {short}. Probed {AS_OF}.")
    sys.exit(0)
name = ALIASES.get(product, product) if product else cfg["default"]
if name not in cfg["products"]:
    print(f"Unknown product '{product}' on {build}. Available: {', '.join(cfg['products'])}. Probed {AS_OF}.")
    sys.exit(2)
target_base = cfg["base"] + name + "/"
target = target_base + "#/" if build.startswith("ra-") or build == "ra-env2" else target_base
if want_url:
    print(target)
    sys.exit(0)
label = f"{build} {name}"

import keyring
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    try:
        cdp_port = int(os.environ.get("SCENARIO_CDP_PORT", "9223"))
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{cdp_port}")
    except Exception:
        print(f"Cannot reach Chrome on port {cdp_port}.")
        sys.exit(2)
    ctx = browser.contexts[0]
    # Every open is a NEW tab; the one blank tab a fresh Chrome starts with is reused.
    blank = [pg for pg in ctx.pages if pg.url in ("about:blank", "chrome://newtab/")]
    page = blank[0] if len(ctx.pages) == 1 and blank else ctx.new_page()
    page.goto(target, timeout=20_000)
    page.bring_to_front()   # show the tab; the window itself may still need a click
    if page.url.startswith(target):   # still on the product: allow a late redirect to a sign-in page (up to 2 s)
        try:
            page.wait_for_url(lambda u: not u.startswith(target), timeout=2000)
        except Exception:
            pass
    page.wait_for_load_state("domcontentloaded")

    if cfg["manual"]:
        if "login.microsoftonline.com" in page.url:
            print(f"{label}: sign in with your company account in the Chrome window (not stored or automated).")
        else:
            print(f"{label}: already signed in.")
        sys.exit(0)

    body_text = page.locator("body").inner_text() if page.locator("body").count() else ""
    if "AccessDenied" in body_text or '"code":403' in body_text or '"status":"FORBIDDEN"' in body_text:
        # If hit with 403 API JSON, retry once with hash route /#/
        if not page.url.endswith("/#/"):
            page.goto(page.url.rstrip("/") + "/#/", timeout=20_000)
            page.wait_for_load_state("domcontentloaded")
            body_text = page.locator("body").inner_text() if page.locator("body").count() else ""

    if page.locator("#username").count() == 0:
        if "AccessDenied" in body_text or '"code":403' in body_text or '"status":"FORBIDDEN"' in body_text:
            print(f"{label}: HTTP 403 Forbidden received. Verify user has assigned roles for this environment.")
            sys.exit(1)
        print(f"{label}: already signed in.")
        sys.exit(0)

    env_name = build.upper().replace("-", "_") + "_USER"
    user = os.environ.get(env_name, "").strip()
    user_file = os.path.expanduser(f"~/.gemini/browser-profile/{build}-user")
    if not user and os.path.exists(user_file):
        user = open(user_file, encoding="utf-8").read().strip()
    if not user:
        print(f"No username: set {env_name} or put it on one line in ~/.gemini/browser-profile/{build}-user.")
        sys.exit(2)
    password = keyring.get_password(build, user)
    if not password:
        print(f'No stored password for service "{build}" and that username. Store it first (keyring.set_password).')
        sys.exit(2)

    page.locator("#username").fill(user)
    page.locator("#password").fill(password)
    if page.locator("#rememberMe").count():
        page.locator("#rememberMe").check()
    page.locator("#kc-login").click()
    signed_in = re.compile(re.escape(target_base.split("//", 1)[1]) + r"(?!auth)")   # the product's pages, not the auth callback
    try:
        page.wait_for_url(signed_in, timeout=30_000)
        print(f"{label}: signed in.")
        sys.exit(0)
    except Exception:
        print(f"{label}: login did not complete (wrong password, or the page changed). Check the Chrome window.")
        sys.exit(1)
