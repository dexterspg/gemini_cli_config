# Nakisa Product Documentation Index (docs.nakisa.com)

Where each product's official documentation lives, so a link is taken from here and never guessed. The site holds user and admin guides, release notes and the vendor API reference. Lease Accounting by release: `nla-docs.md` (this folder).

## How to use a row

| Status | Meaning | What the agent does |
|--------|---------|---------------------|
| `LISTED` | Seen on the site's home page only; the page itself was not read | Give the link as "unverified"; never cite it as proof that a page exists. An API reference anchor in a runbook `Doc:` field stands on its own `id=` proof (api-test-app: `hurl-conventions` → `references/postman-handoff.md` → "## Porting rules"), whatever this row's status |
| `VERIFIED` | Opened in a browser; the proof line says when and where | May cite it |
| `CONFLICT` | The page contradicts itself or another row | Show both URLs, say they conflict, ask the user; never pick one |
| no row | Nothing listed for that product | Say `none found: this index (one automated home-page fetch, 2026-10-30)`; never invent a path or product code |

Proof line for `VERIFIED`: `VERIFIED <date> <initials> — opened in browser at <final URL after redirects>`. Copy the product name and release label word for word from the page footer. Mark a row `VERIFIED` only after a browser read, which is the user's, or the agent's when the browser extension is connected.

## Index

Read 2026-10-30 from the home page by an automated fetch. Landing pages are relative links on that page; resolve them against `https://docs.nakisa.com/` (base URL assumed; no landing page has been opened yet).

| Portfolio | Product (as listed) | Landing page | User guide | Release | Status |
|-----------|---------------------|--------------|------------|---------|--------|
| Workforce Planning | Org Chart Suite, Org Design Suite | `nakisa-hr-suite-latest-product-documentation.html` | not seen | not seen | `LISTED` |
| Workforce Planning | Workforce Planning Suite | `nakisa-wfp-suite-latest-product-documentation.html` | not seen | not seen | `LISTED` |
| Accounting | Lease Accounting Suite | `nla-latest-product-documentation.html` | see `nla-docs.md` | see `nla-docs.md` | `LISTED` |
| Accounting | Accounts Payable Automation | `ap-latest-product-documentation.html` | `npa/en/user/content/app-overview/application-overview.html` (given by the user) | 2026.R2 (page footer) | `CONFLICT` |
| Accounting | Investment Management | `nim-latest-product-documentation.html` | not seen | not seen | `LISTED` |
| IWMS (integrated workplace management) | Portfolio Management Suite | `nre-latest-product-documentation.html` | not seen | not seen | `LISTED` |
| IWMS | Capital Projects Suite | `nss-latest-product-documentation.html` | not seen | not seen | `LISTED` |
| IWMS | Facilities Management Suite | `fms-latest-product-documentation.html` | not seen | not seen | `LISTED` |
| Developer | API Documentation (vendor API reference) | `https://docs.nakisa.com/developer/v1/index.html` | same | not seen (URL path says v1) | `LISTED` |

Lease Accounting and Accounts Payable Automation also appear under IWMS on the home page.

**Accounts Payable conflict:** the user-guide page fetched only partly (about 667 characters). Its footer says "Accounts Payable Automation 2026.R2" but its body says "General Ledger", and its path code `npa` differs from the landing page's `ap-`. Settle it with a browser read before citing.

## Rules

- **Fetching:** page content, and any claim that a page or section does not exist, need a browser read. An automated fetch comes back partial, and a short or mismatched result means it could not be read, not that the page is missing. Whether an API anchor exists: in api-test-app, the raw-HTML `id=` search per `hurl-conventions` → `references/postman-handoff.md` → "## Porting rules"; outside that repo, call the anchor unverified and ask.
- **Releases:** the `latest` landing pages move with each release. A question about one release goes through `nla-docs.md` for lease products (its links carry no status, so treat them as `LISTED`; a release missing from its table is "release unconfirmed", never derived from its URL patterns); for any other product say "release unconfirmed" and do not guess a path.
- **Delegating:** put the row's URL and its status (`LISTED`, `VERIFIED` with its proof line, or `CONFLICT` with both URLs) into the brief.
- **Adding a product:** add a row at `LISTED` with the date and how it was seen; promote it only through the proof line.
