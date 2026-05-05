# Documentation: Controlled Vocabulary

Normative source for all standard terms and status values. Reviewers MUST cite these rows when flagging violations.

## Tier Labels
| Category | Valid Values |
|----------|-------------|
| **Service tiers** | `Minimal` · `Standard` · `Full` |
| **Framework / Library tiers** | `Framework-Minimal` · `Framework-Standard` · `Framework-Full` |

## Project Status (`projects/README.md`)
| Value | Meaning |
|-------|---------|
| `✓` | All required files for current tier exist. |
| `partial` | One or more required files are missing. |

## Document Status (per-project README.md)
| Value | Meaning |
|-------|---------|
| `✓` | File exists. |
| `— missing` | Required by tier but not yet written. |
| `n/a` | Not applicable to this project type. |
| `planned` | Intentionally deferred gap. |

## Document Types
`Service` · `Framework` · `Library`
