"""Probe: save a scoped snapshot of one open element and the page's data calls to files, to explore a screen cheaply.   READ-ONLY.

Opens URL in a new tab of the signed-in scenario Chrome (or attaches to a matching open tab with --active-tab without reloading),
optionally clicks to open a dialog or menu, then writes to --out (a folder outside any git repo):
  - snapshot.yml (the aria snapshot of --scope only, never the whole page)
  - calls.txt (method, path without query string, status of each fetch/xhr call, numbered by step)
  - buttons.txt (with --buttons: each button in --scope with index, disabled, id, v-css-selectors, aria-label, title, icon and text)
  - widgets.txt (with --quasar: indexed catalog of Quasar widgets in --scope: #id, v-css-selectors, .q-field, .q-expansion-item, .q-badge, inputs)
Prints only the file paths and their sizes. Never reads headers or bodies. The snapshot holds record values: own builds only; never commit or share the files.
Needs the build open and signed in via browser-login (mod-login <build> [product]). Never handles credentials.
Run:  python probe.py <url> --out <dir> [--click role:name ...] [--scope role[:name]|css:selector] [--buttons] [--quasar] [--active-tab] [--close]
      --click role:name | field:<label> | tab:name | option:name (a choice in the open menu: option or listitem) | icon:<class> (an icon-only button; opening icons only,
      list them with --buttons, which writes buttons.txt for --scope). css: and positional clicks are refused; once a dialog is
      open only field:, tab: and option: clicks run; names that save, submit, delete or act are refused. Advisory: hooks do not see Python scripts.
      --scope defaults to "dialog"; css: is for the probe only and never moves into a scenario. A Quasar menu renders outside
      the dialog: click field:<label>, then --scope css:.q-menu. A full-page baseline size: --scope css:body (file only).
      Run it from the project root (api-test-app): the allowed hosts come from scenarios/browser/allowed-hosts.txt.
Exit: 0 files written, 1 a click or the scope failed (calls.txt is still written), 2 not run (Chrome unreachable, host or args refused).
"""
import argparse
import os
import re
import sys
from collections import Counter
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

CDP_PORT = int(os.environ.get("SCENARIO_CDP_PORT", "9222"))   # Claude: 9222 (default); agy sets its own port, see docs/agent-provenance.md
DENY = re.compile(r"save|submit|delete|remove|approve|reject|post|send|confirm|apply|update|finish|generate|run|activate|callback|upload|import|publish|assign|archive|release|reverse|execute|calculate|duplicate|copy|\byes\b|\bok\b", re.I)
DIALOG = '[role="dialog"]:visible, .q-dialog__inner:visible, .journal-dialog-body:visible, .nak-dialog-template:visible'
ICON_OK = {"mdi-plus", "mdi-plus-circle", "mdi-plus-box", "mdi-dots-vertical", "mdi-pencil", "mdi-filter", "mdi-filter-variant", "mdi-magnify", "mdi-chevron-down", "mdi-menu-down", "add", "more_vert", "edit", "filter_list", "search", "expand_more"}   # icons that open things; any other icon is refused
ID_SEGMENT = re.compile(r"/(\d+|[0-9a-fA-F-]{32,36})(?=/|$)")   # record ids out of the path: fewer values, fewer distinct lines

ap = argparse.ArgumentParser(description="Save a scoped snapshot and the data calls of one screen.")
ap.add_argument("url")
ap.add_argument("--out", required=True, help="folder for snapshot.yml and calls.txt; must not be inside a git repo")
ap.add_argument("--click", action="append", default=[], metavar="ROLE:NAME")
ap.add_argument("--scope", default="dialog", metavar="ROLE[:NAME]|css:SELECTOR")
ap.add_argument("--close", action="store_true")
ap.add_argument("--buttons", action="store_true", help="also write buttons.txt: each button in --scope with index, disabled, id, v-css-selectors, aria-label, title, icon and text")
ap.add_argument("--quasar", action="store_true", help="also write widgets.txt: indexed Quasar widgets (#id, v-css-selectors, .q-field, .q-expansion-item, .q-badge, inputs) in --scope")
ap.add_argument("--active-tab", action="store_true", help="inspect an already-open tab matching url (or host/path prefix) without reloading the page")
args = ap.parse_args()   # a usage error exits 2


def inside_git_repo(folder):
    d = os.path.abspath(folder)
    norm = d.replace("\\", "/").lower()
    if "/.gemini/antigravity-cli/" in norm or "/.gemini/tmp/" in norm:
        return False   # git-ignored scratch paths inside ~/.gemini
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return True
        parent = os.path.dirname(d)
        if parent == d:
            return False
        d = parent


def locate(page, spec):
    kind, _, rest = spec.partition(":")
    if kind == "icon":   # an icon-only button with no accessible name, by its icon class or ligature text; must match exactly one
        return page.locator("button:visible").filter(has=page.locator(f"i.{rest}, i:text-is('{rest}')"))
    if kind == "field":   # Quasar q-field by its visible label: opens its menu, never submits
        return page.locator(".q-field", has_text=rest).first
    if kind == "css":
        return page.locator(rest)
    if kind == "option":   # a choice in the open pop-up menu; Quasar renders it as option or as listitem
        menu = page.locator(".q-menu:visible").last
        text = re.compile(rf"^\s*{re.escape(rest)}\s*$")
        return menu.get_by_role("option", name=rest, exact=True).or_(menu.get_by_role("listitem").filter(has_text=text))
    return page.get_by_role(kind, name=rest, exact=True) if rest else page.get_by_role(kind)


def settle(page):
    try:
        page.wait_for_load_state("networkidle", timeout=8_000)
    except Exception:
        pass


def signed_out(page):
    return "/auth/realms/" in page.url or "login.microsoftonline.com" in page.url   # a sign-in page


def refuse(msg):
    print("Refusing to run: " + msg)
    print("\nRESULT: NOT RUN")
    sys.exit(2)


HOSTS_CANDIDATES = [
    os.path.join("scenarios", "browser", "allowed-hosts.txt"),
    os.path.join("..", "api-test-app", "scenarios", "browser", "allowed-hosts.txt"),
]
HOSTS_FILE = next((p for p in HOSTS_CANDIDATES if os.path.isfile(p)), None)
if not HOSTS_FILE:
    refuse("scenarios/browser/allowed-hosts.txt not found: run from the project root or api-test-app-agy.")
ALLOWED_HOSTS = {l.strip() for l in open(HOSTS_FILE, encoding="utf-8") if l.strip() and not l.startswith("#")}   # our own builds; two builds can share a host
if urlparse(args.url).hostname not in ALLOWED_HOSTS:
    refuse("the URL's host is not one of our own builds.")
if inside_git_repo(args.out):
    refuse("--out is inside a git repo; the snapshot holds record values.")
for spec in args.click:
    kind, _, name = spec.partition(":")
    if kind == "icon" and name not in ICON_OK:
        refuse(f"--click {spec!r}: icon: takes only an opening icon ({', '.join(sorted(ICON_OK))}); list them with --buttons")
    if kind == "css" or not name or DENY.search(name):
        refuse(f"--click {spec!r}: use role:name, field:<label>, tab:name or option:name; never css:, and never a name that saves, submits, deletes or acts.")
if CDP_PORT == 9222 and "api-test-app-agy" in os.getcwd().replace("\\", "/") and not os.environ.get("ALLOW_PORT_9222"):   # agy's workspace: 9222 is Claude's Chrome
    refuse("agy must set SCENARIO_CDP_PORT=9223 (9222 is Claude's Chrome).")

os.makedirs(args.out, exist_ok=True)
snap_path = os.path.join(args.out, "snapshot.yml")
calls_path = os.path.join(args.out, "calls.txt")
buttons_path = os.path.join(args.out, "buttons.txt")
widgets_path = os.path.join(args.out, "widgets.txt")
for f in (snap_path, calls_path, buttons_path, widgets_path):   # a file left from an earlier run must not read as this run's output
    if os.path.exists(f):
        os.remove(f)
calls = Counter()   # (step, method, path, status) -> count
step_no = [0]       # 0 = page load, n = after the nth --click


def on_response(r):
    try:
        if r.request.resource_type in ("fetch", "xhr"):
            calls[(step_no[0], r.request.method, ID_SEGMENT.sub("/{id}", urlparse(r.url).path), r.status)] += 1
    except Exception:
        pass


code = 0
with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{CDP_PORT}")
    except Exception:
        refuse(f"cannot reach Chrome on port {CDP_PORT}. Run: mod-login <build>")
    if not browser.contexts:
        refuse("no browser window open; run mod-login <build>")

    if args.active_tab:   # reuse an open tab: no new tab, no reload
        opened_new_tab = False
        base_prefix = args.url.split("#")[0]
        page = next((pg for ctx in browser.contexts for pg in ctx.pages if pg.url.startswith(base_prefix) or args.url in pg.url or base_prefix in pg.url), None)
        if page is None or urlparse(page.url).hostname not in ALLOWED_HOSTS:
            refuse(f"--active-tab: no open tab on one of our own builds matched {args.url!r}")
    else:   # one tab per product: reuse the open tab of the same product, else open one (closed again by --close)
        m = re.match(r"(https?://[^/]+/[^/]+/[^/]+/)", args.url)
        prefix = m.group(1) if m else args.url
        page = next((pg for ctx in browser.contexts for pg in ctx.pages if pg.url.startswith(prefix)), None)
        opened_new_tab = page is None
        if page is None:
            page = browser.contexts[0].new_page()

    page.on("response", on_response)
    try:
        if not args.active_tab:
            page.goto(args.url)
            if signed_out(page):
                refuse("signed out: run mod-login <build>")
            settle(page)
        else:
            if signed_out(page):
                refuse("signed out: run mod-login <build>")

        for i, spec in enumerate(args.click, 1):
            step_no[0] = i
            if page.locator(DIALOG).count() and spec.partition(":")[0] not in ("field", "tab", "option"):
                raise Exception(f"--click {spec!r}: a dialog is open; only field:, tab: or option: clicks run inside it")
            locate(page, spec).click(timeout=10_000)
            settle(page)
            if signed_out(page):
                refuse("signed out: run mod-login <build>")

        scope = locate(page, args.scope)
        scope.last.wait_for(state="visible", timeout=10_000)
        n = scope.count()
        with open(snap_path, "w", encoding="utf-8") as f:
            f.write(scope.last.aria_snapshot())

        if args.buttons:   # read-only DOM attribute read; no clicks
            rows = scope.last.locator("button, .q-btn").evaluate_all("""els => els.map((b, i) => [
                i,
                b.disabled || b.classList.contains('disabled') ? 'disabled' : '',
                b.id ? '#' + b.id : '',
                b.getAttribute('v-css-selectors') || '',
                b.getAttribute('aria-label') || '',
                b.getAttribute('title') || '',
                [...b.querySelectorAll('i')].map(e => [...e.classList].filter(c => c.startsWith('mdi-')).join(' ') || (e.textContent || '').trim()).join(' '),
                (b.innerText || '').trim().replace(/\\s+/g, ' ').slice(0, 50)
            ].join('\\t'))""")
            with open(buttons_path, "w", encoding="utf-8") as f:
                f.write("idx\tstate\tid\tv-css-selectors\taria-label\ttitle\ticon\ttext\n")
                f.write("\n".join(rows) + "\n")

        if args.quasar:   # read-only Quasar widget attribute & selector catalog
            w_rows = scope.last.evaluate("""root => {
                const out = [];
                const sel = '[id], [v-css-selectors], .q-field, .q-expansion-item, .q-badge, .q-tab, .q-checkbox, .info-block, input, [role="dialog"]';
                const nodes = root.querySelectorAll(sel);
                nodes.forEach((el, idx) => {
                    if (el.offsetParent === null && getComputedStyle(el).position !== 'fixed') return;
                    const tag = el.tagName.toLowerCase();
                    const id = el.id ? '#' + el.id : '';
                    const vcss = el.getAttribute('v-css-selectors') || '';
                    const role = el.getAttribute('role') || '';
                    const classes = [...el.classList].filter(c =>
                        c.startsWith('q-field') || c.startsWith('q-expansion') || c.startsWith('q-badge') ||
                        c.startsWith('q-tab') || c.startsWith('q-checkbox') || c === 'info-block' ||
                        c === 'global-search-input' || c === 'journal-dialog-body' || c === 'nak-dialog-template'
                    ).join('.');
                    const label = (el.getAttribute('aria-label') || el.getAttribute('placeholder') || '').trim();
                    const txt = (el.innerText || el.value || '').trim().replace(/\\s+/g, ' ').slice(0, 60);
                    if (id || vcss || classes || label) {
                        out.push([idx, tag, id, vcss, classes ? '.' + classes : '', role, label, txt].join('\\t'));
                    }
                });
                return out;
            }""")
            with open(widgets_path, "w", encoding="utf-8") as f:
                f.write("idx\ttag\tid\tv-css-selectors\tquasar-classes\trole\tlabel/placeholder\ttext\n")
                f.write("\n".join(w_rows) + "\n")

        print(f"PROBE scope={args.scope} matched={n}" + (" (used the last)" if n > 1 else ""))
    except Exception as e:   # SystemExit passes through
        code = 1
        print(f"FAIL {str(e).splitlines()[0][:160] if str(e) else type(e).__name__}")
    finally:
        with open(calls_path, "w", encoding="utf-8") as f:
            for (s, m, path, st), c in sorted(calls.items()):
                f.write(f"{s} {m} {path} {st}" + (f" x{c}" if c > 1 else "") + "\n")
    if args.close and opened_new_tab:
        page.close()

for path in (snap_path, calls_path, buttons_path, widgets_path):
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"FILE {path} chars={size} ~tokens={size // 4}")
print("\nRESULT:", "PASS" if code == 0 else "FAIL")
sys.exit(code)
