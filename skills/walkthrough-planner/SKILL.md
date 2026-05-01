---
name: walkthrough-planner
description: Plans the storytelling structure for technical learning walkthroughs before any rendering. Use this skill whenever someone wants to teach a multi-step process, explain a protocol or data flow, create an animated or ASCII walkthrough, structure a flow-based explanation, evaluate a walkthrough for completeness, or choose between surface/deep/hybrid depth for a technical topic. Also use this when concept-tutor is about to explain a multi-actor flow, when learning-strategy identifies a flow-based concept, or when the user says "plan a walkthrough", "walkthrough for [topic]", "how should I teach X as a flow", "evaluate this walkthrough", "what depth for [topic]", "structure this explanation". If someone is about to write a step-visualization or fill in the animated walkthrough prompt template, this skill should run first to plan the story.
---

# Walkthrough Planner Skill

Plans the storytelling structure for technical learning walkthroughs — actors, depth, steps, zoom candidates, teaching beats — before any output is generated. Works upstream of both output formats:

- **ASCII** → routes to `step-visualization` skill for terminal diagrams
- **Animated** → routes to the walkthrough prompt template for Gemini Design / Gemini Web artifacts

This skill does the **thinking**, not the rendering. It interviews the user, maps the topic's natural layers, suggests depth mode, scores completeness, and outputs a story plan as an ASCII story map.

## When to Use

- User has a topic they want to teach but hasn't structured the walkthrough yet
- User wants to evaluate an existing walkthrough plan for completeness
- User is choosing between ASCII and animated output
- Before filling in the walkthrough prompt template or writing step-visualization ASCII
- When concept-tutor needs to plan a multi-step flow explanation

**Triggers:** "plan a walkthrough", "help me structure a walkthrough for [topic]", "evaluate this walkthrough", "what depth should I use for [topic]", "walkthrough for [topic]", "how should I teach [X] as a flow"

## When NOT to Use

- User already has a complete story plan and just needs rendering → route directly to step-visualization or walkthrough prompt 
- Single concept explanation with no actor interactions → use concept-tutor directly
- Architecture overview with no time-ordered flow → use system-architect

## Dependencies

- **agent-concept-tutor** — Planning Resource: topic knowledge, actor identification, audience difficulty assessment (consulted conditionally during Phases 2–3)
- **step-visualization** — Output target: story map is passed to this skill for ASCII rendering
- **learning-walkthrough-prompt.md** — Output target: story map is passed to this template for animated rendering

---

## Planning Resource: agent-concept-tutor

Consult `agent-concept-tutor` at specific points during planning to fill knowledge gaps and improve story quality. The planner owns the story map — concept-tutor provides information only and never generates a walkthrough plan, suggests invoking the planner, or restructures the flow.

| When | Trigger condition | What to ask |
|------|------------------|-------------|
| Before Phase 2 | Topic is outside prior context, or interview reveals surprisingly few actors for the topic's complexity | "Briefly explain [topic]: who are the key actors, what is the sequence of events, and what do people most often get wrong?" |        
| After Phase 2 cast draft | Cast feels thin for the topic's complexity, or any actor's role is unclear | "Are there actors or components in [topic] that this cast is missing: [paste cast]?" |
| After Phase 3 story map draft | Cast feels incomplete for the audience, or the zoom candidate is unclear or unjustified | "For a [audience level] learner, which step in this flow is hardest to grasp and why: [paste story map]?" |

---

## Phase 1: Topic Interview (3-5 questions)

Ask these in order. Stop early if the user's answers make later questions unnecessary.

```
Q1. TOPIC — What process or flow are you teaching?
    (e.g., "how DNS resolution works", "OAuth 2.0 authorization code flow",
    "how a Kubernetes pod gets scheduled", "purchase order approval chain")

Q2. AUDIENCE — Who is learning this?
    □ Non-technical (stakeholders, managers, new hires)
    □ Junior technical (knows basics, building mental models)
    □ Senior technical (filling a specific gap, wants precision)
    □ Mixed (overview for everyone, depth for the curious)

Q3. CONFUSION POINT — What's the #1 thing people get wrong or find confusing?
    (This becomes the zoom step candidate or the [CRACK] in a comparison arc)

Q4. TIME/SPACE BUDGET — How much room do you have?
    □ Quick (3-5 steps, ~30s animated, 1 screen ASCII)
    □ Standard (6-9 steps, ~60s animated, 2-3 screens ASCII)
    □ Deep (10+ steps, ~90s animated, 4+ screens ASCII)

Q5. COMPARISON? — Is this "how X works" or "why X is better than Y"?
    □ Linear — single flow, start to finish
    □ Comparison — two approaches contrasted (naive vs better)
    □ Hybrid — mostly linear but needs a zoom into one critical step
```

---

## Phase 2: Layer Decomposition

After the interview, decompose the topic into its natural abstraction layers. Every technical concept has at least 2-3 layers.   

### How to Find the Layers

Ask: "If I explained this to a 5-year-old, what would I say?" → that's the surface layer.
Ask: "If I explained this to a senior engineer debugging it, what would I say?" → that's the deepest layer.
Everything in between is a middle layer.

### Output Format

```
TOPIC: [topic name]

LAYER MAP:
  ┌—————————————————————————————————————————————————————————┐
  │ SURFACE (highest abstraction)                           │
  │   Actors: [3-4 coarse entities]                         │
  │   Story: [one sentence]                                 │
  │   Audience: non-technical, beginners                    │
  ├—————————————————————————————————————————————————————————┤
  │ MIDDLE (protocol/mechanism layer)                       │
  │   Actors: [4-5 specific entities]                       │
  │   Story: [one sentence]                                 │
  │   Audience: junior-mid technical                        │
  ├—————————————————————————————————————————————————————————┤
  │ DEEP (implementation/internals layer)                   │
  │   Actors: [5-6 internal components]                     │
  │   Story: [one sentence]                                 │
  │   Audience: senior technical, debuggers                 │
  └—————————————————————————————————————————————————————————┘

RECOMMENDED DEPTH: [surface / middle / deep / hybrid]
ZOOM CANDIDATE: Step [N] — "[reason this step deserves a zoom]"
```

### Layer Examples by Domain

**Networking (DNS):**
- Surface: Browser → DNS → IP address returned
- Middle: Browser → Stub Resolver → Recursive Resolver → Root/TLD/Auth NS chain
- Deep: UDP packet construction → socket syscall → kernel routing table → NIC → wire

**Auth (OAuth 2.0):**
- Surface: User → Login → Access granted
- Middle: User → App → Auth Server → Token → Resource Server
- Deep: PKCE challenge → Authorization code → Token endpoint → JWT claims → scope validation

**Business (Purchase Order):**
- Surface: Requester → Approver → Vendor gets paid
- Middle: Requester → System → Manager → Finance → Procurement → Vendor
- Deep: Policy engine → threshold rules → delegation matrix → audit trail → ERP integration

**DevOps (K8s Pod Scheduling):**
- Surface: Developer → Cluster → Pod runs
- Middle: kubectl → API Server → Scheduler → Node → kubelet → Pod
- Deep: API Server → etcd write → Scheduler scoring → Node affinity → CRI → container runtime

---

## Phase 3: Story Map

Generate an ASCII story map showing the full walkthrough structure. This is the deliverable of the skill — it gets evaluated, revised, then handed off to the rendering format.

### Story Map Format

```
TOPIC: [topic]
DEPTH: [surface / middle / deep / hybrid]
DURATION: ~[N]s animated / [N] screens ASCII
ARC TYPE: [linear / comparison / hybrid]

CAST:
  ┌——————————┐   ┌——————————┐   ┌——————————┐   ┌——————————┐
  │ ACTOR 1  │   │ ACTOR 2  │   │ ACTOR 3  │   │ ACTOR 4  │
  │ role     │   │ role     │   │ role     │   │ role     │
  └——————————┘   └——————————┘   └——————————┘   └——————————┘

FLOW:
  Step 1: ACTOR_A ——"data label"——→ ACTOR_B              [surface]
          Artifact: [what to show]
          Teach: "[bold insight]"

  Step 2: ACTOR_B ——"data label"——→ ACTOR_C              [surface]
          Artifact: [what to show]
          Teach: "[bold insight]"

  Step 3: ZOOM INTO [what]                                [hybrid]
          Trigger: "[question that motivates the zoom]"
          Detail actors: DETAIL_A, DETAIL_B
     3.1: DETAIL_A ——"label"——→ DETAIL_B
          Teach: "[insight about the internals]"
     3.2: DETAIL_B ——"label"——→ DETAIL_A
          Teach: "[insight]"

  Step 4: ACTOR_C ——"data label"——→ ACTOR_D              [surface]
          Artifact: [what to show]
          Teach: "[bold insight]"

  ...

  Outro: Cast summary
```

After completing the story map draft, check the consultation table above before proceeding to Phase 4.

### Comparison Arc Format (for "why X is better than Y")

When the arc type is **comparison**, use the step-visualization's story arc tags instead of numbered steps:

```
TOPIC: [topic]
DEPTH: [depth]
ARC TYPE: comparison

CAST:
  [same format as above]

FLOW:
  [ANALOGY]  ACTOR_A ——"simple version"——→ ACTOR_B
             Teach: "Here's the familiar way this works."

  [NAIVE]    ACTOR_A ——"request"——→ ACTOR_B (simple approach)
             Artifact: [show the simple implementation]
             Teach: "This works... until it doesn't."

  [WORKS]    ACTOR_B ——"response"——→ ACTOR_A (happy path)
             Teach: "Under normal conditions, this is fine."

  [CRACK]    ACTOR_A ——"request"——→ ACTOR_B (stress/edge case)
             Artifact: [show what breaks — timeout, race condition, data loss]
             Teach: "[The specific failure mode]"

  [FAIL]     ACTOR_B ——✗——→ ACTOR_A (failure explicit)
             Artifact: [error output, corrupted state, lost message]
             Teach: "[Why the naive approach can't handle this]"

  [BETTER]   Introduce ACTOR_C (the solution)
             ACTOR_A ——"request"——→ ACTOR_C ——"request"——→ ACTOR_B
             Teach: "[What the better approach adds]"

  [RECOVERY] ACTOR_C handles the same stress case
             Artifact: [show the solution working where naive failed]
             Teach: "[Why this approach survives]"

  Outro: Cast summary + "when to use naive vs better"

TEACHING BEATS (from step-visualization):
  □ Prerequisites — [list what learner must know]
  □ Analogy — "[real-world metaphor]"
  □ Vocabulary — [terms to define AFTER the flow]
  □ 80/20 — [learn now vs skip for now]
  □ Practice — [hands-on exercise idea]
  □ Misconception — "[common wrong belief this busts]"
```

---

## Phase 4: Completeness Evaluation

Score the story map against 5 dimensions. Each dimension has 5 checks scored 1-5.

### Cast (actors)

| # | Check | Question |
|---|-------|----------|
| 1 | Coverage | Does every entity that touches the data have a named actor? |
| 2 | Minimality | Could any actors be merged without losing clarity? |
| 3 | Role clarity | Can each actor's job be described in one sentence? |
| 4 | State richness | Does each actor have 2+ distinct states across the walkthrough? |
| 5 | Screen time | Does every actor appear in 2+ steps? |

### Narrative (story arc)

| # | Check | Question |
|---|-------|----------|
| 1 | Origin | Does Step 1 show what triggers the whole process? |
| 2 | Chain | Does each step's output become the next step's input? |
| 3 | No teleportation | Is every data hop between actors shown explicitly? |
| 4 | Resolution | Does the final step show the system at rest / goal achieved? |
| 5 | Reconstructability | Could the learner retrace the flow from memory after one viewing? |

### Teaching (callouts + artifacts)

| # | Check | Question |
|---|-------|----------|
| 1 | One concept per step | Does each step teach exactly ONE new idea? |
| 2 | Insight quality | Is the key insight something non-obvious, not just restating the action? |
| 3 | Artifact relevance | Does each artifact show something the flow diagram alone cannot? |
| 4 | Misconception | Does at least one step bust a common wrong belief? |
| 5 | Vocab after visual | Are technical terms introduced AFTER the visual shows the concept? |

### Depth (layer model)

| # | Check | Question |
|---|-------|----------|
| 1 | Layer fit | Does the chosen depth match the audience? |
| 2 | Zoom justification | If hybrid, does the zoom step target the #1 confusion point? |
| 3 | No layer mixing | Are surface steps consistently surface, deep steps consistently deep? |
| 4 | Zoom transition | Is there a clear "why are we zooming in?" cue? |
| 5 | Return to surface | After a zoom, does the walkthrough cleanly return to the previous level? |

### Pedagogical Completeness (from step-visualization)

| # | Check | Question |
|---|-------|----------|
| 1 | Prerequisites | Are assumed knowledge items listed? |
| 2 | Analogy | Is there a concrete real-world metaphor before any technical detail? |
| 3 | Vocabulary | Are terms defined after (not before) the flow demonstrates them? |
| 4 | 80/20 | Is there a clear "learn now" vs "skip for now" split? |
| 5 | Practice | Is there a hands-on exercise that touches every part of the flow? |

### Scoring

```
COMPLETENESS SCORE:
  Cast:        ████░ [N]/5  [notes if below 4]
  Narrative:   █████ [N]/5
  Teaching:    ███░░ [N]/5  [notes if below 4]
  Depth:       ████░ [N]/5
  Pedagogical: ██░░░ [N]/5  [notes if below 4]
  —————————————————————
  Total:       [N]/25

  20-25: Ready to render
  15-19: Revise weak dimensions, then render
  Below 15: Needs significant rework
```

### Suggestions Format

After scoring, output actionable fixes:

```
SUGGESTIONS:
  → [specific fix for the weakest dimension]
  → [specific fix for second weakest]
  → [optional: creative enhancement idea]
```

---

## Phase 5: Output Routing

After the story map is complete and scores 20+, recommend the output format:

```
OUTPUT ROUTING:
  ┌—————————————————————————————————————————————————————————┐
  │ CONTEXT                          │ RECOMMENDED FORMAT    │
  ├—————————————————————————————————————————————————————————┤
  │ Terminal / Gemini CLI session    │ ASCII (step-viz skill)│
  │ Gemini Design                    │ Animated HTML         │
  │ Gemini Web (artifact)            │ Animated React        │
  │ Documentation / README           │ ASCII (step-viz skill)│
  │ Presentation / demo              │ Animated HTML         │
  │ Quick sketch / planning          │ ASCII (step-viz skill)│
  │ Notebook / learning capture      │ ASCII (step-viz skill)│
  └—————————————————————————————————————————————————————————┘
```

Then hand off:
- **ASCII** → instruct: "Use step-visualization skill. Here is the story map: [paste]"
- **Animated** → instruct: "Fill in the walkthrough prompt template at `C:/Users/dexte/.gemini/skills/walkthrough-planner/learning-walkthrough-prompt.md` using this story map: [paste]"

---

## Evaluation-Only Mode

If the user already has a walkthrough plan (in any format — ASCII, filled template, prose notes, or even just a topic + bullet points), skip the interview and jump to Phase 4 (Completeness Evaluation).

**Triggers:** "evaluate this walkthrough", "score my walkthrough plan", "is this walkthrough complete", "check my flow diagram"  

Input can be:
- An ASCII step-visualization diagram → extract actors, steps, teaching beats, score
- A filled walkthrough prompt template → extract cast, scenes, callouts, score
- Prose notes or bullet points → infer actors + steps, score, suggest structure

Always output the completeness score + suggestions, regardless of input format.

---

## Quick Reference: Skill Comparison

| Dimension | This skill (planner) | step-visualization | walkthrough prompt |
|-----------|---------------------|-------------------|-------------------|
| **Role** | Plans the story | Renders as ASCII | Renders as animation |
| **Input** | Topic + audience | Completed story plan | Completed story plan |
| **Output** | Story map + score | Terminal diagrams | HTML/React artifact |
| **Depth model** | Full (surface/middle/deep/hybrid) | Processing boxes for depth | Zoom steps for depth |
| **Teaching beats** | All 6 required | All 6 required | Callout only (partial) |
| **Evaluation** | Built-in (25-point rubric) | None (assumes plan is good) | Checklist (in template doc) |
| **Platform** | Any (text output) | Terminal / monospace | Gemini Design / Web / browser |

The planner ensures both output formats get a complete, well-structured story. Without it, users tend to jump straight to rendering and discover gaps mid-output.
