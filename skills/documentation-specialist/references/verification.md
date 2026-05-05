# Documentation: Mandatory Source Verification

Any agent writing documentation MUST verify these facts against authoritative sources. Mark as `[NEEDS VERIFICATION]` if source is missing.

## DEPLOYMENT.md Facts
| Fact | Source |
|---|---|
| Port numbers | `docker-compose.yml`, `application.properties`, or deployment config. |
| URL / Proxy routes | Route config, servlet handler code, or `INTEGRATION.md`. |
| Env variable names | `.env`, `.env.example`, or `docker-compose.yml`. |
| Service versions | `pom.xml`, `package.json`, or image tags. |
| Resource limits | `docker-compose.yml` or JVM startup scripts. |

## Domain Deep Dive Facts
| Fact | Source |
|---|---|
| Class/Method names | Exact source code Package.ClassName.method(). |
| Behavior ("X triggers Y")| Traceable class/method or config file. |
| External contracts | `INTEGRATION.md` or external system API docs. |
| Protocols | `platform/INTEGRATION-MAP.md` or client type (e.g. Retrofit, KafkaListener). |

**Note:** Teaching content (concept-tutor) is NOT a verified source. Agents writing docs must verify against actual code.
