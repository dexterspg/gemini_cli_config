---
name: ncp-api-access
description: >
  Client-agnostic answers about how API access is provisioned and managed on the Nakisa Cloud Platform (NCP Cockpit
  API Management): access policies, API keys, environments, key expiry, notification, renewal and rotation, who does
  what. Load before answering any client or colleague question about API keys or access, drafting a question to the
  Cloud team or support about them, or recording an answer from them.
  Triggers on: "API key", "key expiry", "key renewal", "rotate the key", "provision an API key", "access policy",
  "Cockpit API Management", "how long is the key valid". Do NOT trigger for one client's own key dates, tickets or
  holders (that client's own requirements notes), for what an endpoint accepts (api-reference), or for a
  failing API call (jira/api-support).
---

# NCP API Access

**Dependencies:** none. Detail and screenshots: `C:/Users/dpagkaliwangan/workarea/api_ncp/NCP-API-Key-Provisioning-Guide.md`
(file absent → answer from this page only and say the detail was not checked).

Every line is tagged: **NAKISA-STATED** (a named team said it, with the date), **WALKTHROUGH** (seen in the recorded
product walkthrough, 2026-07-24, no one confirmed it for customers), **OPEN** (no answer). Say a statement is
**OPEN** instead of filling it in. Nothing here is client-specific; keep a client's key dates, tickets and holders in
`C:/Users/dpagkaliwangan/workarea/client_api/{Client}/README.md` → "## API keys".

## Model

- Two steps in the NCP Cockpit → API Management, per customer and environment: create an **access policy**, then
  generate an **API key** that references it. No key without a policy. (WALKTHROUGH)
- A policy selects the solutions, the endpoints and the HTTP methods (GET, POST, PUT, DELETE) the key may call. A key
  is bound to one policy and one environment, not to a user. A separate policy and key are needed per environment.
  (WALKTHROUGH)
- The key is sent in the `x-api-key` header. Its value is shown once at creation; a lost key is replaced, never
  recovered. (WALKTHROUGH)

## Key lifecycle

| Question | Answer | Source |
|---|---|---|
| Does a key expire? | Yes. An expiry date is set at creation; the key stops on that date | WALKTHROUGH; Cloud team, 2026-10-05 |
| Is the date fixed? | No. Any date can be set at creation. Cloud recommends at most 1 year, so a person who left the company cannot keep using a key | NAKISA-STATED, Cloud team, 2026-10-05 |
| Where is the date visible? | In the Cockpit; the Cloud team can check it at any time. Whether the API consumer can see it is OPEN | NAKISA-STATED, Cloud team, 2026-10-05 |
| Is anyone warned before expiry? | No. There is no notification feature, so the client must track the date | NAKISA-STATED, Cloud team, 2026-10-05 |
| How is a key renewed? | The customer raises a support ticket in the Nakisa customer support portal, any time. It is not automatic | NAKISA-STATED, Cloud team, 2026-10-05 |
| Is the old key extended? | No. Cloud creates a new key with a new date, so the client receives a different key | NAKISA-STATED, Cloud team, 2026-10-05 |
| What happens to the old key? | Cloud disables the old key once the new one is provided | NAKISA-STATED, Cloud team, 2026-10-05 |
| Can the customer drop a key? | Yes. The customer owns the key and can ask at any time to drop it and get a new one | NAKISA-STATED, Cloud team, 2026-10-05 |
| Does the old key work until the new one arrives? | **OPEN.** Cloud did not say. It holds only if the request is made before the old key's expiry; a request made after leaves a gap. No turnaround time was given | OPEN |
| Does editing a policy reach keys already issued from it? | **OPEN** | OPEN |

When a client asks about renewal, tell them to request it well before their key's date and to track the date
themselves. Do not promise a lead time or a warning email.

## Recording a new answer

1. Add it to the table above as NAKISA-STATED with the team and date, or turn an OPEN row into an answer. This table is its only home.
2. If it closes a row in `api_ncp/NCP-API-Key-Provisioning-Guide.md` → "Open Questions for Product", strike that row and point it here.
3. If it concerns one client's key, record it in that client's own requirements notes, not here.
