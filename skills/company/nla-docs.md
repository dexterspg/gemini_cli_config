# NLA Product Documentation

Official Nakisa Lease Administration/Accounting documentation by release.

## URL Patterns

There are 4 URL patterns depending on the release era. Use these to derive any doc link.

**Pattern A — Modern (2024.R2 → present):**
```
https://docs.nakisa.com/{VER}/{MODULE}/en/{GUIDE}/index.html
```
VER format: `2024R2`, `2024R3`, `2025R1`, `2025R2`, `2025R3` (dots removed, no slash prefix)

| Doc | MODULE | GUIDE |
|-----|--------|-------|
| Release Notes | `accounting` | `release-notes` |
| User Guide | `nla` | `user` |
| What's New | `nla` | `user/content/welcome/whats-new.html` (direct page, not `index.html`) |
| FOS Guide | `fos` | `admin` |
| NGL Guide | `ngl` | `user` |
| SAP Sync Bot | `sync-bot` | `admin` |

**Pattern B — Transitional (2022.R2-SP, 2023.R2, 2023.R4, 2024.R1):**
Same base as Pattern A: `https://docs.nakisa.com/{VER}/...`
- Release Notes → `nfs/en/release-notes/index.html` (except 2022.R2-SP uses `nla/en/release-notes`)
- Change Notes → `nfs/en/change-notes/index.html`
- User Guide → `nla/en/user/index.html`
- FOS Guide → `fos/en/admin/index.html`
- SAP Bots → `sap-bots/en/admin/index.html` (2023.R2, 2023.R4) or `sync-bot/en/admin/index.html` (2024.R1)
- 2022.R2-SP user/admin guides end in `/content/_welcome/welcome_home.html` not `index.html`

**Pattern C — Legacy finance path (2022.R1, 2022.R2, 2022.R3):**
```
https://docs.nakisa.com/finance/{VER}/{MODULE}/help/en/{GUIDE}/index.html
```
VER format: `2022R1`, `2022R2`, `2022R3`

| Doc | MODULE | GUIDE path |
|-----|--------|------------|
| Release Notes | `nfs` | `releasenotes` |
| Change Notes | `nfs` | `change-notes` (R3) or `changenotes` (R1, R2) |
| User Guide | `nla` | `app` (ends in `index.html`) |
| FOS Guide | `fos` | `admin` |
| SAP Bots | `sapbots` | `admin` |
| Admin Guide | `nla` | `admin` (user/admin guides in R1/R2 end in `/content/_welcome/welcome_home.html`) |

**Pattern D — Legacy NLA path (2020.R2, 2021.R1, 2021.R2, 5.0, 5.1, 5.2):**
```
https://docs.nakisa.com/finance/nla/{VER}/help/en/{GUIDE}/content/_welcome/welcome_home.html
```
VER format: `2021R2`, `2021R1`, `2020R2`, `52`, `51`, `50`
- Release Notes are PDFs: `https://docs.nakisa.com/finance/nla/{VER}/docs/NLA_{VER}_Release_En.pdf`
- For 5.x: PDF uses short VER `NLA52_Release_En.pdf`, `NLA51_Release_En.pdf`, etc.
- 5.0 guides use `index.html` not `welcome_home.html`

---

## Full Reference Table

### Nakisa Lease Accounting Suite (Pattern A — 2024.R2+)

| Version | Release Notes | User Guide | FOS Guide | NGL Guide | SAP Sync Bot |
|---------|--------------|------------|-----------|-----------|--------------|
| **2025.R3** | [↗](https://docs.nakisa.com/2025R3/accounting/en/release-notes/index.html) | [↗](https://docs.nakisa.com/2025R3/nla/en/user/index.html) | [↗](https://docs.nakisa.com/2025R3/fos/en/admin/index.html) | [↗](https://docs.nakisa.com/2025R3/ngl/en/user/index.html) | [↗](https://docs.nakisa.com/2025R3/sync-bot/en/admin/index.html) |
| **2025.R2** | [↗](https://docs.nakisa.com/2025R2/accounting/en/release-notes/index.html) | [↗](https://docs.nakisa.com/2025R2/nla/en/user/index.html) | [↗](https://docs.nakisa.com/2025R2/fos/en/admin/index.html) | [↗](https://docs.nakisa.com/2025R2/ngl/en/user/index.html) | [↗](https://docs.nakisa.com/2025R2/sync-bot/en/admin/index.html) |
| **2025.R1** | [↗](https://docs.nakisa.com/2025R1/accounting/en/release-notes/index.html) | [↗](https://docs.nakisa.com/2025R1/nla/en/user/index.html) | [↗](https://docs.nakisa.com/2025R1/fos/en/admin/index.html) | [↗](https://docs.nakisa.com/2025R1/ngl/en/user/index.html) | [↗](https://docs.nakisa.com/2025R1/sync-bot/en/admin/index.html) |
| **2024.R3** | [↗](https://docs.nakisa.com/2024R3/accounting/en/release-notes/index.html) | [↗](https://docs.nakisa.com/2024R3/nla/en/user/index.html) | [↗](https://docs.nakisa.com/2024R3/fos/en/admin/index.html) | [↗](https://docs.nakisa.com/2024R3/ngl/en/user/index.html) | [↗](https://docs.nakisa.com/2024R3/sync-bot/en/admin/index.html) |
| **2024.R2** | [↗](https://docs.nakisa.com/2024R2/accounting/en/release-notes/index.html) | [↗](https://docs.nakisa.com/2024R2/nla/en/user/index.html) | [↗](https://docs.nakisa.com/2024R2/fos/en/admin/index.html) | [↗](https://docs.nakisa.com/2024R2/ngl/en/user/index.html) | [↗](https://docs.nakisa.com/2024R2/sync-bot/en/admin/index.html) |

### Nakisa Lease Administrator (Patterns B/C/D — 2024.R1 and earlier)

| Version | Pattern | Release Notes | Change Notes | User Guide | Admin/FOS Guide | SAP Bots |
|---------|---------|--------------|--------------|------------|-----------------|----------|
| **2024.R1** | B | [↗](https://docs.nakisa.com/2024R1/nfs/en/release-notes/index.html) | — | [↗](https://docs.nakisa.com/2024R1/nla/en/user/index.html) | [↗](https://docs.nakisa.com/2024R1/fos/en/admin/index.html) | [↗](https://docs.nakisa.com/2024R1/sync-bot/en/admin/index.html) |
| **2023.R4** | B | [↗](https://docs.nakisa.com/2023R4/nfs/en/release-notes/index.html) | [↗](https://docs.nakisa.com/2023R4/nfs/en/change-notes/index.html) | [↗](https://docs.nakisa.com/2023R4/nla/en/user/index.html) | [↗](https://docs.nakisa.com/2023R4/fos/en/admin/index.html) | [↗](https://docs.nakisa.com/2023R4/sap-bots/en/admin/index.html) |
| **2023.R2** | B | [↗](https://docs.nakisa.com/2023R2/nfs/en/release-notes/index.html) | [↗](https://docs.nakisa.com/2023R2/nfs/en/change-notes/index.html) | [↗](https://docs.nakisa.com/2023R2/nla/en/user/index.html) | [↗](https://docs.nakisa.com/2023R2/fos/en/admin/index.html) | [↗](https://docs.nakisa.com/2023R2/sap-bots/en/admin/index.html) |
| **2022.R2-SP** | B | [↗](https://docs.nakisa.com/2022R2-SP/nla/en/release-notes/index.html) | [↗](https://docs.nakisa.com/2022R2-SP/nla/en/change-notes/index.html) | [↗](https://docs.nakisa.com/2022R2-SP/nla/en/user/content/_welcome/welcome_home.html) | [↗](https://docs.nakisa.com/2022R2-SP/nla/en/admin/content/_welcome/welcome_home.html) | — |
| **2022.R3** | C | [↗](https://docs.nakisa.com/finance/2022R3/nfs/help/en/releasenotes/index.html) | [↗](https://docs.nakisa.com/finance/2022R3/nfs/help/en/change-notes/index.html) | [↗](https://docs.nakisa.com/finance/2022R3/nla/help/en/app/index.html) | [↗](https://docs.nakisa.com/finance/2022R3/fos/help/en/admin/index.html) | [↗](https://docs.nakisa.com/finance/2022R3/sapbots/help/en/admin/index.html) |
| **2022.R2** | C | [↗](https://docs.nakisa.com/finance/2022R2/nla/help/en/releasenotes/index.html) | [↗](https://docs.nakisa.com/finance/2022R2/nla/help/en/changenotes/index.html) | [↗](https://docs.nakisa.com/finance/2022R2/nla/help/en/app/content/_welcome/welcome_home.html) | [↗](https://docs.nakisa.com/finance/2022R2/nla/help/en/admin/content/_welcome/welcome_home.html) | — |
| **2022.R1** | C | [↗](https://docs.nakisa.com/finance/2022R1/nla/help/en/releasenotes/index.html) | [↗](https://docs.nakisa.com/finance/2022R1/nla/help/en/changenotes/index.html) | [↗](https://docs.nakisa.com/finance/2022R1/nla/help/en/app/content/_welcome/welcome_home.html) | [↗](https://docs.nakisa.com/finance/2022R1/nla/help/en/admin/content/_welcome/welcome_home.html) | — |
| **2021.R2** | D | [↗](https://docs.nakisa.com/finance/nla/2021R2/help/en/releasenotes/index.html) | [↗](https://docs.nakisa.com/finance/nla/2021R2/help/en/changenotes/index.html) | [↗](https://docs.nakisa.com/finance/nla/2021R2/help/en/app/content/_welcome/welcome_home.html) | [↗](https://docs.nakisa.com/finance/nla/2021R2/help/en/admin/content/_welcome/welcome_home.html) | — |
| **2021.R1** | D | [↗](https://docs.nakisa.com/finance/nla/2021R1/help/en/releasenotes/index.html) | [↗](https://docs.nakisa.com/finance/nla/2021R1/help/en/changenotes/index.html) | [↗](https://docs.nakisa.com/finance/nla/2021R1/help/en/app/content/_welcome/welcome_home.html) | [↗](https://docs.nakisa.com/finance/nla/2021R1/help/en/admin/content/_welcome/welcome_home.html) | — |
| **2020.R2** | D | [PDF](https://docs.nakisa.com/finance/nla/2020R2/docs/NLA_2020R2_Release_En.pdf) | — | [↗](https://docs.nakisa.com/finance/nla/2020R2/help/en/app/content/_welcome/welcome_home.html) | [↗](https://docs.nakisa.com/finance/nla/2020R2/help/en/admin/content/_welcome/welcome_home.html) | — |
| **5.2** | D | [PDF](https://docs.nakisa.com/finance/nla/52/docs/NLA52_Release_En.pdf) | — | [↗](https://docs.nakisa.com/finance/nla/52/help/en/app/content/_welcome/welcome_home.html) | [↗](https://docs.nakisa.com/finance/nla/52/help/en/admin/content/_welcome/welcome_home.html) | — |
| **5.1** | D | [PDF](https://docs.nakisa.com/finance/nla/51/docs/NLA51_Release_En.pdf) | — | [↗](https://docs.nakisa.com/finance/nla/51/help/en/app/content/_welcome/welcome_home.html) | [↗](https://docs.nakisa.com/finance/nla/51/help/en/admin/content/_welcome/welcome_home.html) | — |
| **5.0** | D | [PDF](https://docs.nakisa.com/finance/nla/50/docs/NLA50_Release_En.pdf) | — | [↗](https://docs.nakisa.com/finance/nla/50/help/en/app/index.html) | [↗](https://docs.nakisa.com/finance/nla/50/help/en/admin/index.html) | — |

> **Note:** 4.0.3 and earlier not included in source list.

---

## SharePoint: Finance Product Documentation Folder Index

**Root folder:** [Finance Product Documentation](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation&p=true&ga=1)

**URL pattern:**
```
https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2F{ENCODED_FOLDER}&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true
```
Encoding rules: spaces → `%20`, dots → `%2E`, hyphens → `%2D`, parentheses → `%28`/`%29`

### Folders

**Accounting Portfolio**
- [2024.R2](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FAccounting%20Portfolio%202024%2ER2%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2024.R3](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FAccounting%20Portfolio%202024%2ER3%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2025.R1](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FAccounting%20Portfolio%202025%2ER1%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2025.R2](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FAccounting%20Portfolio%202025%2ER2%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2025.R3](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FAccounting%20Portfolio%202025%2ER3%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2025.R4](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FAccounting%20Portfolio%202025%2ER4%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)

**CIB NLA (CA-Nestle)**
- [2021R6](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FCIB%20NLA%202021R6%20%28CA%2DNestle%29%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2022-R2-SP](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FCIB%20NLA%202022%2DR2%2DSP%20%28CA%2DNestle%29%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)

**IWMS Portfolio**
- [2024.R2](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FIWMS%20Portfolio%202024%2ER2%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2024.R3](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FIWMS%20Portfolio%202024%2ER3%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2025.R1](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FIWMS%20Portfolio%202025%2ER1%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2025.R2](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FIWMS%20Portfolio%202025%2ER2%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2025.R3](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FIWMS%20Portfolio%202025%2ER3%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2025.R4](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FIWMS%20Portfolio%202025%2ER4%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)

**NFS (Nakisa Financial Suite)**
- [2022.R3](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNFS%202022%2ER3%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)  
- [2023.R2](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNFS%202023%2ER2%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)  
- [2023.R4 (CA-Walmart-Pfizer)](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNFS%202023%2ER4%20%28CA%2DWalmart%2DPfizer%29%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2023.R4 (GA)](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNFS%202023%2ER4%20%28GA%29%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [2024.R1](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNFS%202024%2ER1%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)  

**NLA (Nakisa Lease Administration)**
- [2021.R1](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNLA%202021%2ER1%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)  
- [2021.R2](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNLA%202021%2ER2%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)  
- [2022.R1](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNLA%202022%2ER1%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)  
- [2022.R2](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNLA%202022%2ER2%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)  
- [2022.R2-SP](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNLA%202022%2ER2%2DSP%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [4.0.3](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNLA%204%2E0%2E3%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)    
- [5.0 Consultation Package](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNLA%205%2E0%20Consultation%20Package&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [5.0 Product Documentation](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNLA%205%2E0%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [5.1 Consultation Package](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNLA%205%2E1%20Consultation%20Package&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [5.1 Product Documentation](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNLA%205%2E1%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
- [5.2 Product Documentation](https://nakisainc.sharepoint.com/sites/Content/Public/Forms/AllItems.aspx?id=%2Fsites%2FContent%2FPublic%2FFinance%20Product%20Documentation%2FNLA%205%2E2%20Product%20Documentation&viewid=6dd29729%2D0019%2D4850%2D9cbc%2D639463ad81f8&p=true)
