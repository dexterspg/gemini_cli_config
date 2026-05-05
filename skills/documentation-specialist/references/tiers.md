# Documentation: Tiers & Requirements

Requirements scale with project complexity. Determine tier before writing.

## Service Tier (Backend Services)
| Document | Minimal | Standard | Full |
|----------|---------|----------|------|
| README.md | ✓ | ✓ | ✓ |
| INTEGRATION.md | — | ✓ | ✓ |
| DEPLOYMENT.md | — | ✓ | ✓ |
| API-REFERENCE.md | — | ✓ | ✓ |
| BUSINESS-CASE.md | — | — | ✓ |
| TECH-STACK.md | — | — | ✓ |
| DATABASE.md | — | — | ✓ |
| DOMAIN.md | — | — | ✓ |

## Framework / Library Tier (Shared Code)
| Document | Minimal | Standard | Full |
|----------|---------|----------|------|
| README.md | ✓ | ✓ | ✓ |
| INTEGRATION.md | — | ✓ | ✓ |
| API-REFERENCE.md | — | ✓ | ✓ |
| TECH-STACK.md | — | — | ✓ |
| DOMAIN.md | — | — | ✓ |

## Promotion Priority Order
1. **Minimal → Standard:** `INTEGRATION.md` > `DEPLOYMENT.md` > `domain/` deep dives.
2. **Standard → Full:** `API-REFERENCE.md` > `DATABASE.md` > `TECH-STACK.md` > `FRONTEND.md` > `BUSINESS-CASE.md`.
