# Nakisa Quasar / Vue SPA Page Maps & Verified Selectors

Cached UI architecture, container scopes, verified DOM `#id` selectors, and Quasar interaction rules extracted from live browser runs (`probe.py --active-tab --buttons --quasar`) across Nakisa products (`preview1` and `ra-env2`).

> **Rule:** Always check this file (and `<project>/scenarios/browser/pages/<product>.md`) **before** running `probe.py` on a screen. When a new screen or modal is automated, append its verified `#id` selectors and quirks here.

---

## 1. Global Quasar / Vue SPA Architecture Rules

| Pattern | Verified Behavior & Resilient Selector Strategy |
|---|---|
| **Active Dialog Scoping** | Dismissed Quasar dialogs leave their outer `.q-dialog` wrapper in the DOM and can leave an orphaned `.q-dialog__backdrop` that intercepts pointer events. Always scope open dialogs to `.q-dialog__inner:visible` (or product-specific modal classes like `.journal-dialog-body` / `.nak-dialog-template`) and call `clear_stale_overlays(page)` before top-level clicks. |
| **Portaled Dropdown Menus (`.q-menu:visible`)** | Quasar `QSelect` and `ApInputPinnedSingleSelect` render their dropdown popup inside `.q-menu:visible` attached to `document.body` (*outside* the dialog DOM tree). Click the `.q-field` trigger inside the dialog/page scope, then locate options (`.q-item`, `role="option"`, or `role="listitem"`) and server-side search inputs (`.q-menu:visible input`) inside `page.locator(".q-menu:visible").last`. |
| **Closing Open `.q-menu` Popups** | When **no dialog** is open, `page.keyboard.press("Escape")` closes `.q-menu`. When **a dialog is open** (e.g., FOS Create dialog), `Escape` closes the **entire dialog**; instead, dismiss the menu by clicking the dialog's title text (e.g., `dialog.get_by_text("Create", exact=True).click()`). |
| **Date Inputs (`fill_quasar_date`)** | Typing a `YYYY-MM-DD` date into a Quasar date input opens a floating calendar popup that blocks adjacent fields. Always press `Escape` followed by `Tab` after filling a date input. |
| **Dependent Dropdowns** | When a child `QSelect` depends on a parent `QSelect` (e.g., `Vendor *` after `Company *` in AP), wait `1000–1500ms` after selecting the parent option so the child's company-scoped lookup settles before clicking the child field. |
| **R&D Build Hash Routing (`ra-env*`)** | Always navigate `ra-env*` URLs with the `/#/` SPA hash route (e.g., `https://rnd.nakisancp.com/ra-env2/payable/#/`). Omitting `/#/` bypasses the Vue router and hits backend APIs directly, returning `403 Forbidden` JSON instead of redirecting to Keycloak. |
| **Live Tab Probing (`probe.py --active-tab --quasar`)** | Never run inline `python -c` DOM probes in PowerShell. To inspect an already-open screen or dialog in `<0.5s` without reloading, run `python ~/.gemini/skills/browser-scenarios/scripts/probe.py "<url-substring>" --active-tab --buttons --quasar --out "<scratch-dir>"` (remembering `SCENARIO_CDP_PORT=9223`). |

---

## 2. Nakisa Financial Suite (NFS — `nakisa-financial-suite`)

- **Build & Base URL:** `preview1` (`https://preview.nakisa.cloud/preview1/nakisa-financial-suite/`)
- **Reference Scenarios:** `scenarios/browser/payment-posting-t86-t87.py`, `scenarios/browser/depreciation-posting-t92-t93.py`

### Routes
- **Activation Groups Landing Page:** `#/landing_page/activation_groups`
- **Contracts Landing Page:** `#/landing_page/contracts`
- **Activation Group Wizard (Definition & Schedules):** `#/wizard/activationGroup?step=definition&activationGroupRevisionId=<revisionId>`
  - Verified `DIS1` revisions on `preview1`:
    - `10003115` (`AG-100020905`, `NLA Demo - Dunlop Tires - 23 April 2026`, Unit `UN-100030034` — Payment T86/T87)
    - `10004043` (`AG-100021499`, Unit `10013274` — Depreciation T92/T93)

### Verified DOM `#id` & CSS Selectors (Probed Live)

| UI Area / Component | Exact DOM `#id` / Selector | Element Type & Text / Notes |
|---|---|---|
| **Top App Bar & Global Search** | `#toggle-drawer-btn` | `button` (`Menu`) — toggles left navigation drawer |
| | `#globalSearch-searchOption-dropDownBtn` | `button` (`Expand`) — entity filter dropdown for global search |
| | `input.global-search-input` | `input` (`placeholder="Search"`) — global search input box |
| | `#globalSearch-removeInput-iconBtn` | `i` (`close`) — clears global search input |
| | `#globalSearch-searchInput-btn` | `button` (`Search`) — submits global search |
| | `#suggestionsList-searchOption-arrowBtn` | `button` (`chevron_right`) — suggestion item action arrow |
| | `#language-select` / `#language-select-input` | `label.q-field` / `input[role="combobox"]` (`English`) |
| | `#action-centers-btn` | `button` (`pending_actions`) — opens Action Center drawer |
| | `#user-btn` | `button` (`account_circle`) — user profile menu |
| | `#landing-page-header-tab` | `div.q-tab[role="tab"]` (`Landing Page`) |
| **Left Hierarchy Drawer (`#main-menu-drawer`)** | `#master-agreement-selection` | `div[role="listitem"]` — current Master Agreement item |
| | `#contract-selector` / `#contract-selector-input` | `label.q-field` / `input[role="combobox"]` (`Contracts`) |
| | `#contract-nav-add-btn` | `button` (`mdi-plus`) — add Contract |
| | `#lease-component-selector` / `#lease-component-selector-input` | `label.q-field` / `input[role="combobox"]` (`Lease Components`) |
| | `#lease-component-revision-nav-add-btn` | `button` (`mdi-plus`) — add Lease Component revision |
| | `#activation-group-selector` / `#activation-group-selector-input` | `label.q-field` / `input[role="combobox"]` (`Activation Groups`) |
| | `#schedule-nav-expansion` | `div.q-expansion-item` (`Schedules`) — expands `IAS - Finance` / `GAAP - Operating` |
| | `#open-in-new-btn` | `button` (`mdi-open-in-new`) — opens schedule in new tab |
| | `#mini-state-btn` | `button` (`mdi-chevron-left`) — collapses left hierarchy drawer |
| **Wizard Context Header & Action Bar** | `#revision-btn` | `button` (`Active Inception`, `mdi-menu-down`) — revision switcher |
| | `#event-id-ag-lease-end-btn` | `a` (`Lease End`) — lease end indicator |
| | `#context-menu-event` | `button` (`Event`, `mdi-calendar-plus`) — trigger AG event |
| | `#context-menu-journals` | `button` (`View`) — **opens the Schedule / Payment Journals Dialog** |
| | `#context-menu-title-btn` | `button` (`mdi-dots-vertical`) — 3-dots overflow menu |
| | `#uploaded-files-btn` | `button` (`mdi-chevron-down`) — uploaded documents dropdown |
| **Wizard Stepper Tabs** | `#definition-step` | `div` (`Definition`) |
| | `#accounting-step` | `div` (`Accounting`) |
| | `#terms-conditions-step` | `div` (`Terms & Conditions`) |
| | `#classifications-step` | `div` (`Classifications`) |
| | `#unit-list-step` | `div` (`Unit List`) |
| | `#charge-list-step` | `div` (`Charge List`) |
| | `#notifications-step` | `div` (`Notifications`) |
| **Definition Form (`#definition-step`)** | `#activation-group-definition-general-info-form-expansion` | `div.q-expansion-item` (`General Information`) |
| | `#display-id` / `#display-id-input` | `label.q-field` / `input` (`ID *`, e.g. `AG-100020905`) |
| | `#name` / `#name-input` | `label.q-field` / `input` (`Activation Group Name *`) |
| | `#rou-start-date-input` / `#rou-start-date-input-input` | `label.q-field` / `input` (`ROU Start Date *`) |
| | `#rou-end-date-input` / `#rou-end-date-input-input` | `label.q-field` / `input` (`ROU End Date *`) |
| | `#activation-document-date-input-input` | `input` (`Document Date`) |
| | `#activation-posting-date-input-input` | `input` (`Posting Date`) |
| | `#description` / `#description-textarea` | `label.q-field` / `textarea` (`Description`) |
| | `#end-of-term-intention` / `#dfv-info-btn` | `label.q-field` (`End of Term Intention *`) / `button` (`DFV`) |
| | `#asset-definition-form-expansion` | `div.q-expansion-item` (`Asset Information`) |
| | `#fair-market-value-input` / `#residual-value-input` | `input` (`FMV / Unit *`) / `input` (`Salvage Value / Unit *`) |
| | `#transfer-of-ownership` / `#specialized-asset` | `div.q-checkbox[role="checkbox"]` |
| **Schedule Journals Dialog** | `.journal-dialog-body` | Dialog body scope opened by `#context-menu-journals` |
| | `.journal-dialog-body .q-tab, .journal-dialog-body .journal-date-tab` | Accounting standard (`IAS`, `GAAP`) and date tabs |
| | `.journal-dialog-body .q-badge` | Journal posting status badges (`Posted`, `Open`) |

### NFS Gotchas & Quirk Notes
- **Landing Grid Pagination:** The landing grid (`.q-table tbody tr, .ag-center-cols-container .ag-row`) is paginated (`1-20` sorted ascending by ID). Never assume `rows.first` is the target active contract; use Global Search or direct revision URL navigation.
- **Global Search Pointer Interception:** Quasar's `<header class="q-header">` inside `q-portal--dialog` can intercept standard `.click()` events on search popup cards. Either trigger via `res_item.evaluate("el => el.click()")` or navigate directly to `NFS_WIZARD_URL`.
- **Closing the Schedule Journals Dialog:** Press `Escape` (`nfs_page.keyboard.press("Escape")`) and assert `expect(nfs_page.locator(".journal-dialog-body")).to_be_hidden()`.
- **Schedules & Payment Schedule (checked 2026-11-13 by `lease-payment-matched-invoice.py`):**
  - From the wizard, the left navigation panel's **Schedules** lists classifications (`IAS - Finance`, `GAAP - Operating`, ...); click one to open its schedules.
  - The view selector reads **All Columns Schedule** (`.q-field, .q-select, .q-btn-dropdown` with `has_text="All Columns Schedule"`); switch it to **Payment Schedule** inside `.q-menu:visible .q-item`.
  - Payment Schedule columns: `Period`, `Payment Postings` (**View** button), `Payment Internal Status`, `Payment External Status`, `Details`, `Payment Date`, amounts. A posted row on `DIS1` reads `Posted` / `Open`.
  - **View** opens **Payment Journal(s)** (`.q-dialog__inner:visible` with `has_text="Payment Journal(s)"`): Revision and Unit selectors, a tab per classification with its status, History, Document Date and Posting Date, **Payment** and **Clearing** tabs, the entries table, and **Reverse** (posted) or **Post** (unposted); **Close** closes it.
  - **Post** in `Payment Journal(s)` keeps the pop-up open; it then shows `Internal Status` = `Posted`, an `Internal Document Number`, and **Reverse**. The **Clearing** tab shows the payment's second (`CLEARING`) record and its own `Internal Document Number`.

### UI vs. Public API Calls
- **UI-Internal (403 with API key):** `POST ui/v1/journals/dialog` and `POST ui/v1/general-ledger-postings/accrual` require interactive UI session cookies (`@PreAuthorize`).
- **Public API Equivalents:**
  - Search unit journals: `POST /api/v1/journals/payments/{ppt}/{unitId}/search` (`hurl/nfs/crud/journals/api-read.hurl`)
  - Post depreciation journal: `POST /api/v1/general-ledger-postings/depreciation` (`hurl/nfs/flows/depreciation-posting-t92-t93/depreciation-posting-t92-t93.hurl`)

---

## 3. SAP Posting Bot / Nakisa General Ledger (SPB — `sap-posting-bot`)

- **Builds & Base URLs:**
  - `preview1`: `https://preview.nakisa.cloud/preview1/sap-posting-bot/`
  - `ra-env2`: `https://rnd.nakisancp.com/ra-env2/sap-posting-bot/`
- **Reference Scenarios:** `scenarios/browser/payment-posting-t86-t87.py`, `scenarios/browser/depreciation-posting-t92-t93.py`

### Routes
- **Transaction Listing Page:** `#/transaction-listing-page`

### Verified DOM `#id` & CSS Selectors (Probed Live)

| UI Area / Component | Exact DOM `#id` / Selector | Element Type & Text / Notes |
|---|---|---|
| **Top Toolbar & Active Filter Chips** | `#pageActionContextMenuAddJournalVoucherBtn` | `button` (`Create Journal Voucher`) |
| | `#toolbar-exportTable-btn` | `button` (`Export Table`) |
| | `#toolbar-tableFieldSelection-btn` | `button` (`settings`) — column visibility selector |
| | `#dynamicPage-toggleAggsFilterPanel-btn` | `button` (`Toggle Filter Panel`) — collapses/expands left filter drawer |
| | `#dynamicPage-removeAggFilter-chipBtn` | `div` — active filter chip in top bar (e.g., `Posting Type : Payment cancel`, `System : DIS1 cancel`) |
| | `#dynamicPage-resetAllFilters-chipBtn` | `div` (`Reset All`) — **clears all sticky filters from top chip bar** |
| **Left Filter Panel (`aggsPanelView`)** | `#aggsPanelView-resetAllFilters-btn` | `button` (`Reset Filters`) — **left panel global filter reset** |
| | `#aggsPanelView-filterProfileManager-openDialog-btn` | `button` (`collections_bookmark`) — saved filter profiles |
| | `#aggsPanelView-addNewAggFilter-btn` | `button` (`Add new Filter`) |
| | `#aggsPanelView-filterOperations-showMenu-btn` | `button` (`Toggle Filters`) |
| **Filter Facet Accordions (`<facet>`)** | `#aggsPanelView-expandFilters-<facet>-expansionBtn` | `div.q-expansion-item` — expands/collapses facet accordion. Verified `<facet>` keys:<ul><li>`accounting_standard_display_id` (`Accounting Standard`)</li><li>`posting_type` (`Posting Type`)</li><li>`ledger_type` (`Transaction Type`)</li><li>`ledger_transaction_created_by.keyword` (`Created By`)</li><li>`erp_system` (`System`)</li><li>`company` (`Company`)</li><li>`ag_display_id` (`Activation Group Display ID`)</li><li>`contract_display_id` (`Contract Display ID`)</li><li>`internal_status` (`Internal Status`)</li><li>`internal_document_number` (`Internal Document Number`)</li><li>`enrichment_status_nla` (`NLA Enrichment Status`)</li><li>`enrichment_status_nre` (`NPM Enrichment Status`)</li><li>`enrichment_status_ap` (`AP Enrichment Status`)</li><li>`external_status` (`External Status`)</li><li>`external_document_number` (`External Document Number`)</li><li>`fiscal_year` (`Fiscal Year`)</li><li>`fiscal_period` (`Fiscal Period`)</li><li>`ledger_transaction_created_at` (`Created At`)</li><li>`posting_date` (`Posting Date`)</li></ul> |
| **Per-Facet Reset & Edit Buttons** | `#aggsPanelView-resetAggFilter-<facet>-btn` | `button` (`refresh`) — resets a single facet filter (uses same `<facet>` keys above) |
| | `#aggsPanelView-EditFilter-ledger_transaction_created_at-btn` | `button` (`edit`) — opens date range picker for `Created At` |
| | `#aggsPanelView-EditFilter-posting_date-btn` | `button` (`edit`) — opens date range picker for `Posting Date` |
| **Facet Option Checkboxes** | `#aggsPanelView-checkboxAgg-<facet>-<index>-checkboxBtn` | `div.q-checkbox[role="checkbox"]` inside expanded facet (e.g., `#aggsPanelView-checkboxAgg-posting_type-0-checkboxBtn` for `Payment`, `#aggsPanelView-checkboxAgg-erp_system-0-checkboxBtn` for `FINQ8S-300`, `#aggsPanelView-checkboxAgg-erp_system-1-checkboxBtn` for `DIS1`). Prefer matching `.q-checkbox` with `has_text="<OptionText>"` inside `#aggsPanelView-expandFilters-<facet>-expansionBtn` so index shifts never break the locator. |
| **Results Table (`#searchResultsDisplayTable`)** | `#searchResultsDisplayTable` | `div.q-table__container` — main ledger transactions table container |
| | `th#searchResults-sortColumn-iconBtn` | `th` — sortable column headers (`ID`, `Accounting Document ID`, `Created At`, `Posting Type`, `Transaction Type`, `Application`, `System`, `Company`, `Internal Document Number`, `Internal Status`, `External Document Number`, `External Status`, etc.) |
| | `td#searchResultsDisplaySelectionTd<rowIdx>` | `td` — first cell in row `<rowIdx>` (`0..19`) containing row action button |
| | `button#searchResults-selectRow-customActionsBtn` | `button` (`more_vert`) — 3-dots row action button |
| | `td#searchResults-viewRowDetails-cell` | `td` — clickable data cells in each row (clicking opens the Ledger Transaction Detail Modal) |
| | `#searchResults-paginationFirstPage-btn` | `button` (`first_page`) |
| | `#searchResults-paginationPrevPage-btn` | `button` (`chevron_left`) |
| | `#searchResults-paginationNextPage-btn` | `button` (`chevron_right`) |
| | `#searchResults-paginationLastPage-btn` | `button` (`last_page`) |
| **Ledger Transaction Detail Modal** | `.nak-dialog-template, .q-dialog__inner` | Dialog container opened by clicking `td#searchResults-viewRowDetails-cell` on a target row |
| | `dialog.locator(".info-block, .q-item-label", has_text="<FieldName>").first` | Metadata info blocks (`Internal Status`, `External Status`, `Document Number`, `Enrichment Status`, `Ledger Type`, `Accounting Standard`) |
| | `dialog.locator(".q-badge", has_text="<Status>").first` | Status badge (`Posted`, `Open`, `Failed`) |
| | `dialog.locator("button:has-text('Close'), button[v-css-selectors='close'], .q-btn:has(.q-icon[name='close'])").last` | Close Modal button |

### SPB Sticky Filter Gotcha & Verified Rows
- **Mandatory Filter Reset:** SPB persists previous filter selections (such as `System: FINQ8S-300`) across page reloads. Always click `#dynamicPage-resetAllFilters-chipBtn` (or `#aggsPanelView-resetAllFilters-btn`) if visible before applying scenario filters.
- **Idempotent Accordion & Checkbox Helpers:**
  - Check if `#aggsPanelView-expandFilters-<facet>-expansionBtn` is already expanded via `el.classList.contains('q-expansion-item--expanded')`.
  - Check if `.q-checkbox` is already checked via `el.classList.contains('q-checkbox__inner--truthy') || el.querySelector('.q-checkbox__inner--truthy') !== null`.
- **Horizontal Scroll & Header Render Order (checked 2026-11-09 & 2026-11-13):**
  - The listing is sorted newest first by `Created At`; status columns (`Internal Status`, `External Status`, `External Document Number`) sit off-screen to the right. Scroll the header into view (`el.scrollIntoView({inline: 'center'})` or `{inline: 'start'}`) before reading or drawing callouts on cells.
  - On table refresh, `thead` renders after `tbody` rows: always wait for `thead th` visibility before reading column positions.
- **Record Details Dialog, Entries & FX Popup (`ra-env2`, `bapi-field-locations.py`):**
  - **Information Section** (`.info-block` labels): `Application`, `Created By / At`, `Ledger Type`, `Accounting Standard`, `Lease Classification Type`, `Principal Position Type`, `Posting Date`, `Document Date`, `Fiscal Year`, `Fiscal Period`, `Internal Status` (+ `Document Number`), `Enrichment Status`, `External Status` (+ `Document Number`). Failed records add **External Message** (`type - class - number - text - Field - Param`, joined with ` | `).
  - **Entries table:** `Item`, `Account Number`, `Account Name`, `Account Category`, `Cost Center`, `Profit Center`, plus `Debit` and `Credit` under `Contract Currency`, `Company Currency`, and `Second Local Currency`. Clicking **FX** beside a currency group opens a popup (`Translation Rate`, `Translation Date`, `Translation Date Type`, `Source Currency Type`).
- **Verified `preview1` `DIS1` Transaction Rows:**
  - Payment (`Posting Type: Payment`, `System: DIS1`): `10254378` (T86 `Internal: Posted` / `2026079331`, `External: Open`), `10254383` (T87 `Internal: Posted` / `2026079336`, `External: Posted`, SAP Doc `1900042188`)
  - Depreciation (`Posting Type: Periodic Posting`, `System: DIS1`): `10260309` (T92 `External: Open`), `10260310` (T93 `External: Posted`, SAP Doc `8888888801`)

### Public API Pointers
- **Search Ledger Transactions:** `POST /api/v1/general-ledger/ledger-transactions/search` (`hurl/sap-posting-bot/crud/ledger-transactions/`)
- **Read Ledger Transaction by ID:** `GET /api/v1/general-ledger/ledger-transactions/{id}`
- **Write-Back External SAP Info (T87 / T93):** `PUT /api/v1/general-ledger/ledger-transactions/external-info` (`hurl/sap-posting-bot/crud/ledger-transactions/write-back-external-info.hurl`)

---

## 4. Nakisa Accounts Payable Automation (AP — `payable`)

- **Builds & Base URLs:**
  - `ra-env2`: `https://rnd.nakisancp.com/ra-env2/payable/#/`
  - `preview1`: `https://preview.nakisa.cloud/preview1/payable/#/`
- **Reference Scenario:** `scenarios/browser/create-invoice.py`

### Routes
- **Invoices List:** `#/invoices`
- **Invoice Detail (Details Tab):** `#/invoices/<id>` (e.g., `#/invoices/432` Approved, `#/invoices/434` Posted, `#/invoices/481`)
- **Invoice Detail (Line Items Tab):** `#/invoices/<id>?tab=lineItems`
- **Invoice Detail (Invoice Postings Tab):** `#/invoices/<id>?tab=invoicePostings`

### Scopes & Selectors
- **Invoices Management List:**
  - Create button: `page.get_by_role("button", name="New Invoice", exact=True)`
- **Create New Invoice Dialog (`.q-dialog__inner:visible`):**
  - Dialog title check: `dialog.get_by_text("Create New Invoice", exact=True)`
  - Fields (via `_helpers.py`):
    - `Company *`: `select_quasar_option(page, dialog, "Company *", "FINQ8S-300 - CA - 1000", filter_text="1000")`
    - `Vendor *` (wait `1000ms` after Company): `select_quasar_option(page, dialog, "Vendor *", "0000100005 - TEST LENDER CANADA", filter_text="0000100005", settle_ms=1500, filter_settle_ms=1800)`
    - `Invoice Type *`: `select_quasar_option(page, dialog, "Invoice Type *", "Vendor Invoice", filter_text=None)`
    - `Invoice Name *`: `fill_quasar_input(page, dialog, "Invoice Name *", "<Name>")`
  - Buttons: `dialog.get_by_role("button", name="Add", exact=True)`, `dialog.get_by_role("button", name="Cancel", exact=True)`
- **Invoice Detail Page & Tabs:**
  - Header fields on Details tab: `External Invoice ID *`, `Invoice Date *` (`fill_quasar_date`), `Due Date *` (`fill_quasar_date`), `Currency *`, `Payment Method *`, `Payment Term *`, `Payment Block *`
  - Navigation tabs: `page.get_by_role("tab", name="Line Items", exact=True)` (`Details`, `Line Items`, `Invoice Postings`, `Credits & Payments`, `Hyperlinks`)
  - Line Items Add Modal:
    - Open button: `page.get_by_role("button", name="Add", exact=True).first`
    - Fields inside `dialog`: `Expense Category *` (note non-breaking space in `"Base\u00a0Rent"`), `Quantity *`, `Unit Price *`, `Description`, `Cost Center *` (server-filtered `ApInputPinnedSingleSelect` inside `.q-menu:visible input`)
    - Save line button: `dialog.get_by_role("button", name="Add & Close", exact=True)`
  - Workflow Action Buttons:
    - `Send for Approval`, `Approve`, `Reject`, `Callback` (`page.get_by_role("button", name="<Action>", exact=True)`)
  - Delete Draft Invoice (Cleanup):
    - 3-dots menu button: `page.locator("button").filter(has=page.locator(".mdi-dots-vertical")).first`
    - Delete menu item: `page.locator(".q-menu:visible .q-item", has_text="Delete").first`
    - Confirm modal button: `dialog.get_by_role("button", name="Delete", exact=True)`
  - Posted Invoice Journal Modal:
    - Open button: `page.get_by_role("button", name="View Journal", exact=True)`
    - Modal title: `dialog.get_by_text("Invoice Posting", exact=True).first`
    - Close button: `dialog.locator("button", has_text="close").first` (or `Cancel` button)
  - **Invoice Write, SP Matching & Direct Posting Path (checked 2026-11-13 by `lease-payment-matched-invoice.py`):**
    - Details fields auto-save as filled (no Save button). A new Draft's header has no `External Invoice ID` field until filled on `Details`.
    - **Line Items Add (`#invoice-line-items-add-btn`):** Inside **Add New Line Item**, `Escape` closes the entire dialog — select options by typing and clicking `.q-menu:visible .q-item` without pressing `Escape`. An expense category whose FOS determination is not `ACTIVE` appears as `... - No GL Account` (disabled).
    - **SP Matching (`Match Scheduled Payments`):** A new line's `SP Matching` column reads `Match` (first `Match` is SP Matching; second is GR Matching). Clicking it opens `Match Scheduled Payments` listing open lease payments of the same vendor, company, currency, and category; ticking `.q-checkbox` allocates the amount (`Fully funded`); `Save` closes it and the row reads `1 Payment Matched`.
    - **Invoice Postings (`#invoice-payments-tab-make-payment-btn` — "Create a Posting"):** Opens `Create Invoice Posting` (`Document Date *`, `Posting Date *`, `Save`, `Generate Journal`; do not press `Escape` after filling dates). Clicking **Generate Journal** turns the dialog in place into **Edit Invoice Posting Draft** (`Status: Review`, with `Close` / `Recall` / `Post`); clicking **Post** inside that dialog keeps it open at `Status: Posted` until **Close** is clicked.
    - **Row `has_text` regex gotcha:** Table row `innerText` concatenates cells without spaces (`"1" + "0000200500"`), so `\b` word boundaries at cell edges fail; match `0000\d{6}` without `\b` when filtering rows.

---

## 5. Financial Organization Structure (FOS — `financial-org-structure`)

- **Build & Base URL:** `preview1` (`https://preview.nakisa.cloud/preview1/financial-org-structure/`)
- **Reference Files:** `scenarios/browser/pages/fos.md`, `scenarios/browser/create-cost-center.py`, `scenarios/browser/lease-payment-matched-invoice.py`
- **Route:** `#/master_data?type=costCenter` (note: `?type=` in the URL does **not** switch the entity when reloading — FOS reopens the last entity used).
- **Scopes & Selectors:**
  - **Erp System Selector (top left):** Sticky across page loads; names systems as `<name> - <type>` (`DIS1` is `Disconnected System - Nakisa`). Its `combobox` input is covered — click `fos.locator(".q-field").filter(has=fos.get_by_role("combobox", name="Erp System", exact=True)).first`.
  - **Determinations Navigation (checked 2026-11-13):** Expand **Determinations** (`button` `'Expand "Determinations"'`), type into the search input below it (`Collapse "Determinations"` -> `xpath=following::input[1]`), and click **Vendor General Ledger Determination** or **Expense Account Determination**.
  - Table scope: `page.locator(".q-table__container").first` (two `.q-table__container` elements exist; the main entity list is first and relations is second; avoid `--scope main` which includes 9.9k chars of entity tabs). Each text column has a `Search` textbox in column order (`Vendor GL Determination`: Display ID, Company, Partner; `Expense Account Determination`: Display ID, Status, Company, Expense Category, Expense Account).
  - Toolbar & row icon-only buttons (no accessible name):
    - Create (`+`): `table.get_by_role("button").filter(has=page.locator("i.mdi-plus"))`
    - Refresh: `i.mdi-refresh`
    - Row Edit: `row.locator("button").filter(has=page.locator(".mdi-pencil-outline")).first`
    - Delete (never click): `i.mdi-delete-forever`
  - Create / Edit Dialog (`page.get_by_role("dialog")` or `.q-dialog__inner:visible`):
    - Fields: `Display ID *` (`textbox`), `Status *` (`combobox` — check value with `expect(status).to_have_value("Created")`, options rendered as `listbox` > `listitem`), `Name *` (`textbox`), `Blocked` (`combobox`).
    - Menu dismissal quirk: `Escape` closes the whole dialog; click `dialog.get_by_text("Create", exact=True)` to close only the `.q-menu`.

---

## 6. Nakisa Real Estate (NRE — `real-estate`)

- **Build & Base URL:** `preview1` (`https://preview.nakisa.cloud/preview1/real-estate/`)
- **Reference Files:** `scenarios/browser/pages/nre.md`, `scenarios/browser/create-contract.py`, `scenarios/browser/open-create-dashboard.py`
- **Routes:**
  - Leases List: `#/leases` (`#/contracts` returns 500)
  - Dashboards Overview: `#/dashboard/overview`
- **Scopes & Selectors:**
  - Rows-per-page selector: `page.get_by_role("combobox", name="20", exact=True)` -> opens `.q-menu` with `role="option"` values `5, 10, 15, 20, 35, 50`.
  - Create Contract button: `page.get_by_role("button", name="Create Contract", exact=True)`
  - Create Contract Dialog (`page.get_by_role("dialog")`):
    - Fields: `Premises *` (`combobox`), `Principal Position *` (`combobox`), `Display ID *` (`textbox`, disabled), `File Number *` (`textbox`, disabled).
    - Dual Cancel buttons: Header and footer both have `Cancel`; use `dialog.get_by_role("button", name="Cancel", exact=True).last`.
  - Dashboards Overview:
    - `page.get_by_role("button", name="Create", exact=True)` opens `"Create dashboard"` dialog offering `"Dashboard"`, `"List"`, `"Dashboard & List"`, `"Pivot Table"`.
