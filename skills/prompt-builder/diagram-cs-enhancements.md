# CS Teaching Enhancements — Animated Communication Flow Diagram

Extend the base `ascii-animated-diagram.md` spec with these elements when the diagram is teaching a **computer science or systems communication concept** (e.g. HTTP vs in-process, blocking I/O, circuit breakers, thread models).

These concepts make the diagram a learning artifact, not just a visualization. **Do not specify CSS values here — let the AI decide styling during generation.**

---

## Additional Legend Row: Thread State

Add a second legend row below the communication-type row:

```
Row 2: thread state — one entry: "BLOCKING (thread waits)" with a pulsing indicator
```

Teach: when a call is HTTP, the calling thread is suspended waiting for a network response. When a call is in-process, it returns synchronously without suspending.

---

## Blocking Indicator

Show below the orchestrator node when an HTTP call is in flight:

- Visible only during HTTP request steps (not in-process steps)
- Label: e.g. `[ THREAD BLOCKED — awaiting HTTP response ]`
- Disappears when the HTTP response arrives

**What it teaches:** HTTP calls block the calling thread. In-process calls do not.

**cfg field to add:**
```
isBlocking: boolean  // true during HTTP request steps, false during in-process steps
```

**getSteps annotation guide:**
- HTTP request step → `isBlocking: true`
- HTTP response step → `isBlocking: false`
- In-process call step → `isBlocking: false`
- Failure/error step → `isBlocking: false`

---

## Latency Tag

Show near the midpoint of the active arrow during transit steps:

- HTTP calls: show a simulated latency value (e.g. `~45ms`)
- In-process calls: show `~0ms` or `<1ms`
- Failure steps: show `TIMEOUT` or `CONNECTION REFUSED`

**What it teaches:** Network calls have measurable latency. In-process calls are effectively free. This contrast makes the performance trade-off tangible.

**cfg field to add:**
```
latencyLabel: string  // e.g. '~45ms', '<1ms', 'TIMEOUT'
```

---

## Variable Packet Speed

Animate the traveling packet (SVG `stroke-dashoffset`) at different speeds per call type:

- HTTP calls: slower travel (reinforces network distance)
- In-process calls: fast travel (reinforces same-JVM locality)
- Failure states: flicker or stall animation

**What it teaches:** Visual speed directly encodes the latency difference between call types.

**Implementation note for prompt:** Specify that the base animation interval `[MS]` applies to HTTP steps, and in-process steps should use a fraction of that (e.g. 0.3×).

---

## Annotation Panel

Show a short pedagogical sentence per step, separate from the log panel:

- Fades in when a step starts, fades out on transition
- 1–2 sentences max — what is happening and why it matters
- Written for a learner, not a developer reading logs

**Example annotations:**
- HTTP request step: "NFS calls FOS over HTTP — a real network socket is opened to port 8081."
- In-process step: "LeaseScheduleCalculator runs in the same JVM — no network, no serialization."
- Failure step: "FOS is down. Stage 1 has no fallback — the entire activation fails."

**cfg field to add:**
```
annotation: string  // display text for annotation panel, '' = hide panel
```

---

## Authoring Rules (CS Diagrams)

| Step type | isBlocking | latencyLabel | annotationTone |
|-----------|-----------|--------------|----------------|
| HTTP request | true | `~Nms` | Explain network overhead |
| HTTP response | false | `~Nms` | Note round-trip complete |
| In-process call | false | `<1ms` | Contrast with HTTP above |
| In-process return | false | `<1ms` | Reinforce same-JVM locality |
| HTTP failure | false | `TIMEOUT` or `CONN REFUSED` | Explain what breaks without fallback |
| Circuit breaker open | false | `OPEN — fast fail` | Explain why fast-fail is better than timeout |

---

## Which Diagrams Use This

Apply these enhancements when the flow includes any of:
- HTTP vs in-process call comparison
- Thread blocking / async patterns
- Circuit breaker states (CLOSED / OPEN / HALF-OPEN)
- Service mesh, retry, or timeout behavior
- Any pattern where latency or thread state is the lesson

Skip these enhancements for diagrams that are purely structural (e.g. data model relationships, UI component trees).
