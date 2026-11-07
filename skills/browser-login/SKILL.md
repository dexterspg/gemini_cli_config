---
name: browser-login
description: >
  How a login to a build is stored and used for the scenario Chrome: the password in Windows Credential Manager, a username
  file, and the login script. Load on "sign in to [build]", "log me in", "store my login",
  "store my password", "my session expired", "browser login", "add a build to the login". Documentation only: the user does every
  step and the AI never handles a credential. Do NOT use browser tools or any script to fill a login form with a credential;
  do NOT trigger for writing or running a browser scenario (browser-scenarios).
---

# Browser login

Opens a build's product in the **scenario Chrome** (the separate Chrome on port 9223 via `SCENARIO_CDP_PORT=9223`, profile
`~/.gemini/browser-profile`), not the user's everyday Chrome, signing in first on Keycloak builds.

**Dependencies:** the helper script `~/.gemini/skills/browser-login/scripts/login.py` (or `mod-login`, `run.ps1`, `run.sh`), `playwright==1.58.0`, `keyring>=25.0.0`, and the company file `C:/workarea/references/nakisa-products.md` (with automatic fallback to `~/workarea/references/nakisa-products.md` or env `NAKISA_PRODUCTS_FILE`). Read it for any product or build fact; missing: stop and say so.

## The rule

The AI never types, reads, stores or logs a credential, never fills a login form with one, and never runs `login.py`,
`mod-login`, `run.sh`, `run.ps1` or a `keyring.get_password` call, even when told to "just do it". Every step below is the user's, in the
user's own terminal. If a password is pasted into chat, do not use it: tell the user to store it
themselves and to change that password, since it is now in the transcript.

## You do, once per build

1. Store the password (it prompts, so nothing lands in chat or shell history; use a separate terminal):
   `python -c "import keyring, getpass; keyring.set_password('<build>', '<username>', getpass.getpass('password: ')); print('stored')"`
2. Save the username on one line in `~/.gemini/browser-profile/<build>-user` (not a secret). Environment variable
   `<BUILD>_USER` (hyphens become underscores) overrides it.
3. Check it is stored (prints only `found` or `missing`):
   `python -c "import keyring; print('found' if keyring.get_password('<build>', '<username>') else 'missing')"`

## You do, each time

Run the login command in your terminal:
- PowerShell shorthand (via `$PROFILE` function `mod-login` / alias `browser-login`): `mod-login <build> [product]`
- PowerShell script directly: `& "$env:USERPROFILE\.gemini\skills\browser-login\scripts\run.ps1" <build> [product]`
- CMD / batch shim: `"%USERPROFILE%\.gemini\skills\browser-login\scripts\mod-login.cmd" <build> [product]`
- Git Bash: `bash ~/.gemini/skills/browser-login/scripts/run.sh <build> [product]`

It starts the scenario Chrome if needed, fills the login form from Credential Manager only when the form shows, and prints `signed in.` or `already signed in`.

- No product: the build's default product. A product: that one, by short name or UI segment. `list` prints the build's products,
  short names and probe date.
- Every open is a new tab (a fresh Chrome's one blank tab is reused), so repeated runs add tabs; close the extras. One sign-in
  covers every product of a Keycloak build.
- A `manual` build (company Microsoft sign-in): the script only opens the page and says whether you still need to sign in. You sign
  in by hand; no password is stored or filled, and none is ever stored for a company account.

## Hash routing on R&D / SPA builds (ra-env*, etc.)

On R&D environments like `ra-env2`, navigating directly to `<product>/` without hash routing (`/#/`) bypasses client-side SPA routing and hits the backend API directly, returning an unauthenticated `403 Forbidden` JSON payload (`AccessDenied: Full authentication is required to access this resource`).

- Always use the hash route format: `https://rnd.nakisancp.com/<env>/<product>/#/`.
- The helper script appends `/#/` for `ra-env*` targets and catches 403 API JSON errors rather than falsely reporting "already signed in".

## Add a build

1. A row in the Builds table of the company file; follow its refresh note and header rules.
2. Steps 1 and 2 above for the new build, after looking at its login page signed out: the form ids the helper fills are
   `#username`, `#password`, `#rememberMe`, `#kc-login`.
