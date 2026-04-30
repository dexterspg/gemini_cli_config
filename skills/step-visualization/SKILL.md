---
name: step-visualizer
description: Reusable ASCII template for teaching step-by-step flows between named actors or components in a monospace terminal. Use when the user asks for step-by-step visualizations, ASCII diagrams, or walkthroughs of complex flows.
---

# Step Visualization Skill

Reusable ASCII template for teaching step-by-step flows between named actors or components in Claude Code's monospace terminal. Works for any domain: software, business processes, data pipelines, organizational workflows. Both vertical (top-to-bottom) and horizontal (left-to-right) layouts are supported — choose based on the flow's complexity and node count.

## Dependencies

None — this is a rendering skill. It receives a completed story plan and produces output. Callers: walkthrough-planner (passes story map), concept-tutor (on explicit user request only), codebase-archaeologist, system-architect.

## Rendering Rule

Every step's entire content — header, topology, narration, key insight, evidence — MUST be wrapped in a single fenced code block (triple backticks). Box-drawing characters (`┌─┐│└─┘╔═╗║╚╝▓▌▼`) only align in monospace. If rendered as inline markdown text, proportional fonts break all alignment and the diagram becomes unreadable. One code fence per step — never split a step across multiple code blocks, and never output diagram elements as bare markdown.

## When to Use

- Teaching how systems or actors communicate in sequence
- Software: browser ↔ server, client ↔ API, service ↔ service, protocol flows
- Business: approval chains, procurement flows, incident escalation, onboarding steps
- Data: ETL pipelines, event streams, document routing
- Any multi-node flow where order, causality, and handoffs matter

## When NOT to Use

- Single-component explanations (just use a code block)
- Data structure or tree diagrams
- Architecture overviews with no time-ordered flow

## Teaching Completeness

Every visualization must cover ALL of these narrative beats. Missing any produces a reference diagram, not a learning artifact. These are narrative beats, not mandatory individual steps — combine adjacent beats into one step when the visual is the same.

```
PREREQUISITES   → What must the learner already know? (table of concepts + one-liners)
ANALOGY         → One concrete real-world metaphor mapping every system actor
                  to a familiar concept before any technical detail appears
FLOW STEPS      → The actual step-by-step walkthrough (see Story Arc below)
VOCABULARY      → Define every term used, AFTER the flow is understood
80/20           → Explicit "learn now" vs "skip for now" table
PRACTICE        → One hands-on exercise that touches every part of the flow
                  + 2-3 "what to learn next" pointers
```

Prerequisites and Analogy are the first two steps. Vocabulary, 80/20, and Practice are the last three closing sections. The flow steps fill the middle.

## Required Beats Per Step

Every flow step MUST include ALL of these:

| Beat | Format |
|------|--------|
| Step header | `╔══[ STEP N · TOTAL ]═╗` with `[ARC_TAG]` if using story arc |
| Topology | All nodes shown, `▓ ACTIVE ▓` vs `· idle ·`, vertical/horizontal/hybrid layout |
| Flow arrows | Labeled arrows between active nodes, numbered for multi-step |
| Narration | Bordered `┌─ ─┐` box, 3-5 lines, plain English |
| Key insight | `⚡ KEY INSIGHT` + `▌` left bar, one sentence |
| Evidence | `// EVIDENCE · TYPE` header + content |

## Story Arc

### For Comparison Visualizations

When contrasting two approaches (file:// vs http://, polling vs WebSocket, manual approval vs automated, batch vs stream):

```
[ANALOGY]  → Real-world metaphor mapping every actor
[NAIVE]    → The simple/common approach
[WORKS]    → Happy path demonstrated
[CRACK]    → Where it breaks under pressure
[FAIL]     → Failure made explicit and visual
[BETTER]   → Introduce the solution
[RECOVERY] → Solution handling the failure case
```

### For Linear "How X Works" Explanations

Use numbered steps without arc tags. The step count should match the topic's actual complexity — don't compress to save space. If the flow naturally has 10 steps, use 10 steps.

```
╔══[ STEP 1 · N ]═══════════════════════════════════════════════╗
║  Title describing what happens in this step                    ║
╚═══════════════════════════════════════════════════════════════╝
```

Include every actor and layer that participates in the real flow. If the OS routes traffic, the OS is a node. If TCP must be established before HTTP, TCP establishment is a step. Do not skip layers to reduce step count.

## Evidence Types

Pick whichever fits the step:

| Type | Header | When |
|------|--------|------|
| Code snippet | `// EVIDENCE · CODE` | Showing implementation |
| Data structure | `// EVIDENCE · DATA STRUCTURE` | Token, payload, DB record, tree |
| Pros/cons | `// EVIDENCE · PROS / CONS` | Contrasting approaches |
| DevTools | `// EVIDENCE · DEVTOOLS` | Browser-verifiable observation |
| Error map | `// EVIDENCE · ERROR MAP` | Symptoms → root causes |
| HTTP headers | `// EVIDENCE · HTTP HEADERS` | Request/response envelope |
| Log output | `// EVIDENCE · LOG OUTPUT` | Terminal/server log display |
| Message payload | `// EVIDENCE · MESSAGE PAYLOAD` | Queue message, event, webhook body |
| Sequence comparison | `// EVIDENCE · BEFORE / AFTER` | Version A vs B, old vs new |
| Form / document | `// EVIDENCE · DOCUMENT` | Approval form, ticket, email content |
| Decision criteria | `// EVIDENCE · DECISION` | Rules used to route or approve |

## Narration Rules

These three rules make the narration box a teaching tool, not a caption:

1. **Lead with what changed** — "The server now..." not "In this step we see..."
2. **Connect to the previous step** — "Unlike Step 2 where..." or "Now that the connection is open..."
3. **End with why it matters** — what the learner can now do or understand that they couldn't before

## Layout Selection

Pick the layout that best fits the flow's complexity. Teaching completeness (all 6 required beats) applies regardless of layout choice.

| Layout | Best for | Avoid when |
|--------|----------|------------|
| **Vertical** (top-to-bottom) | 3+ nodes, deep processing boxes, multi-machine boundaries, complex flows | Simple 2-node request/response |
| **Horizontal** (left-to-right) | 2-3 node linear flows, simple request→response, compact steps | Many nodes (wraps awkwardly), nested processing, multiple context boundaries |
| **Hybrid** (mix both) | Flows where one segment is a simple handoff (horizontal) but another segment has depth or branching (vertical) | Forcing consistency when the flow naturally changes shape |

Layouts can be combined within a single step when teaching completeness benefits. For example, a horizontal request→response at the top, then a vertical deep-dive into what the server does internally. The goal is clarity for the learner, not visual uniformity.

When in doubt, use vertical — it handles all cases and never wraps in a terminal.

## Topology Templates

### Vertical Layout

```
╔══[ STEP N · TOTAL ]═══════════════════════════════════════════╗
║  Title of this step                            [ARC_TAG]      ║
╚═══════════════════════════════════════════════════════════════╝

  ┌── CONTEXT BOUNDARY (e.g., YOUR MACHINE) ─────────────────┐
  │                                                          │
  │  ┌──────────────────────┐                                │
  │  │  NODE A   ▓ ACTIVE ▓ │                                │
  │  └──────────┬───────────┘                                │
  │             │                                            │
  │             │  arrow label (what is moving)               │
  │             ▼                                            │
  │  ┌──────────────────────┐                                │
  │  │  NODE B   ▓ ACTIVE ▓ │                                │
  │  └──────────┬───────────┘                                │
  │             │                                            │
  │             │  arrow label                               │
  │             ▼                                            │
  │  ┌──────────────────────┐                                │
  │  │  NODE C   ▓ ACTIVE ▓ │                                │
  │  └──────────────────────┘                                │
  │                                                          │
  │  ┌──────────────────────┐                                │
  │  │  NODE D   · idle ·   │  ← shown but dimmed            │
  │  └──────────────────────┘                                │
  └──────────────────────────────────────────────────────────┘

  NARRATION
  ┌────────────────────────────────────────────────────────────┐
  │ Lead with what changed. Connect to previous step.         │
  │ End with why it matters.                                  │
  └────────────────────────────────────────────────────────────┘

  ⚡ KEY INSIGHT
  ▌ One sentence the learner remembers if they forget everything else.

  // EVIDENCE · TYPE
  ┌────────────────────────────────────────────────────────────┐
  │ [content matching the evidence type]                      │
  └────────────────────────────────────────────────────────────┘
```

### Horizontal Layout

For simple 2-3 node linear flows where compactness helps readability. Same required beats apply.

```
╔══[ STEP N · TOTAL ]═══════════════════════════════════════════════╗
║  Title of this step                            [ARC_TAG]          ║
╚═══════════════════════════════════════════════════════════════════╝

  ┌──────────────────┐     request      ┌──────────────────┐
  │ NODE A ▓ ACTIVE ▓ │ ──────────────► │ NODE B ▓ ACTIVE ▓ │
  └──────────────────┘  ◄────────────── └──────────────────┘
                          response

  ┌──────────────────┐
  │ NODE C · idle ·   │  ← shown but dimmed
  └──────────────────┘

  NARRATION
  ┌────────────────────────────────────────────────────────────┐
  │ Lead with what changed. Connect to previous step.         │
  │ End with why it matters.                                  │
  └────────────────────────────────────────────────────────────┘

  ⚡ KEY INSIGHT
  ▌ One sentence the learner remembers if they forget everything else.

  // EVIDENCE · TYPE
  ┌────────────────────────────────────────────────────────────┐
  │ [content matching the evidence type]                      │
  └────────────────────────────────────────────────────────────┘
```

### Hybrid Layout

Combine horizontal and vertical within a single step when the flow naturally changes shape. For example, a simple handoff shown horizontally, then a vertical deep-dive into internal processing:

```
╔══[ STEP 3 · 5 ]═══════════════════════════════════════════════╗
║  Server Receives Request and Processes It                      ║
╚═══════════════════════════════════════════════════════════════╝

  ┌──────────────────┐    GET /health     ┌──────────────────┐
  │ BROWSER ▓ ACTIVE ▓│ ──────────────►  │ SERVER ▓ ACTIVE ▓ │
  └──────────────────┘                    └────────┬─────────┘
                                                   │
                                                   │  internal processing
                                                   ▼
                                    ┌──────────────────────────────┐
                                    │  route match → /health       │
                                    │    → auth middleware (skip)   │
                                    │    → handler returns JSON     │
                                    └──────────────────────────────┘
                                                   │
                                                   │  200 OK + JSON body
                                                   ▼
  ┌──────────────────┐   ◄──────────────   ┌──────────────────┐
  │ BROWSER ▓ ACTIVE ▓│    response        │ SERVER ▓ ACTIVE ▓ │
  └──────────────────┘                     └──────────────────┘
```

The horizontal part shows *who talks to whom*. The vertical part shows *what happens inside*. Use this when a single layout would either waste space (all vertical for a simple handoff) or hide depth (all horizontal for complex processing).

### Node States

- `▓ ACTIVE ▓` — involved in this step
- `· idle ·` — exists but not involved
- `✗ FAIL` — broken or unavailable
- `▓  NEW!  ▓` — appearing for the first time

### Arrow Rules

- Arrows follow the layout direction (vertical: top-to-bottom, horizontal: left-to-right)
- Every arrow labeled with WHAT is moving
- Multi-step flows numbered: `1.`, `2.`, `3.`
- Bidirectional: separate labeled arrows for each direction

### Multi-Machine Topology

When physical location matters, stack separate context boundaries:

```
  ┌── YOUR MACHINE ──────────────────────────────────────────┐
  │  ┌──────────────────────┐                                │
  │  │  BROWSER  ▓ ACTIVE ▓ │                                │
  │  └──────────┬───────────┘                                │
  │             │  ...nodes flow vertically...               │
  └──────────────────────────────────────────────────────────┘

  ┌── COLLEAGUE'S MACHINE ───────────────────────────────────┐
  │  ┌──────────────────────┐                                │
  │  │  BROWSER  ✗ FAIL     │                                │
  │  └──────────────────────┘                                │
  └──────────────────────────────────────────────────────────┘
```

### Processing Box (domain-specific)

When a node does internal processing worth showing, nest a processing box inside the context boundary. The content is domain-specific — adapt to the system being taught.

Browser rendering:
```
  │  ┌──────────────────────────────────────────────────┐    │
  │  │  html → DOM ──┐                                  │    │
  │  │               ├──► Render Tree → Layout → Paint  │    │
  │  │  css → CSSOM ─┘                             ✓    │    │
  │  │  js  → AST → execute → page is live ✓            │    │
  └──────────────────────────────────────────────────┘    │
```

API server processing:
```
  │  ┌──────────────────────────────────────────────────┐    │
  │  │  request → middleware → auth check               │    │
  │  │             → route handler → service layer      │    │
  │  │             → DB query → serialize → response    │    │
  │  └──────────────────────────────────────────────────┘    │
```

Worker processing:
```
  │  ┌──────────────────────────────────────────────────┐    │
  │  │  dequeue message → deserialize payload           │    │
  │  │    → validate → process → write result to DB     │    │
  │  │    → ack message                                 │    │
  │  └──────────────────────────────────────────────────┘    │
```

Approval workflow:
```
  │  ┌──────────────────────────────────────────────────┐    │
  │  │  receive request → check policy thresholds       │    │
  │  │    → under limit? → auto-approve                 │    │
  │  │    → over limit?  → escalate to senior approver  │    │
  │  └──────────────────────────────────────────────────┘    │
```

## Opening Sections (Before Flow Steps)

### Prerequisites (Step 0)

What the learner must already know. A quick self-check — if any row is fuzzy, the step ahead will make it concrete.

```
╔══[ STEP 0 · N ]═══════════════════════════════════════════════╗
║  Prerequisites                                                ║
╚═══════════════════════════════════════════════════════════════╝

  All nodes shown (all active — this is a reference frame)

  // EVIDENCE · DATA STRUCTURE
  ┌──────────────────────┬──────────────────────────────────────┐
  │ CONCEPT              │ WHAT YOU NEED TO KNOW                │
  ├──────────────────────┼──────────────────────────────────────┤
  │ concept-name         │ One-liner the learner can verify.    │
  └──────────────────────┴──────────────────────────────────────┘
```

### Analogy (Step 1)

One concrete real-world metaphor mapping every system actor to a familiar concept. Must appear before any technical detail.

```
╔══[ STEP 1 · N ]═══════════════════════════════════════════════╗
║  The Analogy — [metaphor name]                                ║
╚═══════════════════════════════════════════════════════════════╝

  All nodes shown (all active — mapping every actor)

  // EVIDENCE · DATA STRUCTURE
  ┌──────────────────────┬────┬──────────────────────────────────┐
  │ SYSTEM ACTOR         │ ↔  │ REAL-WORLD ANALOGY               │
  ├──────────────────────┼────┼──────────────────────────────────┤
  │ NODE A               │ ↔  │ familiar concept                 │
  └──────────────────────┴────┴──────────────────────────────────┘
```

## Closing Sections (After Flow Steps)

### Vocabulary — define terms AFTER the flow

```
╔══[ VOCABULARY ]═══════════════════════════════════════════════╗
║  Terms defined after context — not before                    ║
╚═══════════════════════════════════════════════════════════════╝

  ┌──────────────────────┬──────────────────────────────────────┐
  │ TERM                 │ MEANING                              │
  ├──────────────────────┼──────────────────────────────────────┤
  │ term-name            │ Plain English definition.            │
  └──────────────────────┴──────────────────────────────────────┘
```

### 80/20

```
  ┌──────────────────────────────────┬───────────────────────────┐
  │ LEARN NOW ✓                      │ SKIP FOR NOW →            │
  ├──────────────────────────────────┼───────────────────────────┤
  │ essential concept                │ advanced detail           │
  └──────────────────────────────────┴───────────────────────────┘
```

### Practice

One hands-on exercise that touches every part of the flow, plus 2-3 pointers for what to learn next.

```
╔══[ PRACTICE ]═════════════════════════════════════════════════╗
║  Hands-on exercise                                            ║
╚═══════════════════════════════════════════════════════════════╝

  NARRATION
  ┌────────────────────────────────────────────────────────────┐
  │ Step-by-step exercise description. Should touch every      │
  │ part of the flow the learner just walked through.          │
  └────────────────────────────────────────────────────────────┘

  ⚡ KEY INSIGHT
  ▌ Reading about a flow and tracing one live are different experiences.

  WHAT TO LEARN NEXT
  ┌────────────────────────────────────────────────────────────┐
  │ 1. First natural follow-up topic                           │
  │ 2. Second natural follow-up topic                          │
  │ 3. Third natural follow-up topic                           │
  └────────────────────────────────────────────────────────────┘
```

## Reference Example (API → Queue → Worker → DB)

One flow step from a non-browser system, showing all 6 required beats:

```
╔══[ STEP 2 · 5 ]═══════════════════════════════════════════════╗
║  Worker Picks Up Job from Queue                               ║
╚═══════════════════════════════════════════════════════════════╝

  ┌── BACKEND CLUSTER ───────────────────────────────────────┐
  │                                                          │
  │  ┌──────────────────────┐                                │
  │  │  API SERVER · idle · │                                │
  │  └──────────────────────┘                                │
  │                                                          │
  │  ┌──────────────────────┐                                │
  │  │  QUEUE    ▓ ACTIVE ▓ │                                │
  │  │  pending: 1 job      │                                │
  │  └──────────┬───────────┘                                │
  │             │                                            │
  │             │  dequeue job payload (JSON)                 │
  │             ▼                                            │
  │  ┌──────────────────────┐                                │
  │  │  WORKER   ▓ ACTIVE ▓ │                                │
  │  └──────────┬───────────┘                                │
  │             │                                            │
  │             │  INSERT INTO results (...)                  │
  │             ▼                                            │
  │  ┌──────────────────────┐                                │
  │  │  DATABASE ▓ ACTIVE ▓ │                                │
  │  └──────────────────────┘                                │
  └──────────────────────────────────────────────────────────┘

  NARRATION
  ┌────────────────────────────────────────────────────────────┐
  │ The API server is idle — its job ended when it enqueued    │
  │ the task in Step 1. The worker pulls the job from the      │
  │ queue, processes the payload, and writes the result to     │
  │ the database. The queue decouples the API from the work.   │
  └────────────────────────────────────────────────────────────┘

  ⚡ KEY INSIGHT
  ▌ The queue lets the API respond immediately without waiting for
  ▌ the work to finish — the worker handles it asynchronously.

  // EVIDENCE · MESSAGE PAYLOAD
  ┌────────────────────────────────────────────────────────────┐
  │  {                                                        │
  │    "job_id": "abc-123",                                   │
  │    "type": "generate_report",                             │
  │    "payload": {                                           │
  │      "account_id": 4521,                                  │
  │      "period": "2026-Q1"                                  │
  │    }                                                      │
  │  }                                                        │
  └────────────────────────────────────────────────────────────┘
```

## Agent Integration

Agents teaching multi-node communication should read this skill first. Pass `"use step-visualization skill for ASCII diagrams"` in the agent prompt when the topic involves sequential message flow between named components.

Applicable agents: concept-tutor, codebase-archaeologist, debugger, system-architect.

**Note for concept-tutor specifically:** concept-tutor uses its own lightweight inline diagram format by default (prose-first, single arrow-chain embedded mid-explanation). This skill is only invoked for concept-tutor lessons when the user explicitly requests it (e.g., "use step-visualization" or "give me the full ASCII walkthrough").
