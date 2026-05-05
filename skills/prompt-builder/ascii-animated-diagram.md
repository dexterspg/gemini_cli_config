# Template: Animated Communication Flow Diagram

For prompts that instruct AI to generate a self-contained animated HTML file showing a communication or sequence flow. No external JS libraries — Google Fonts is the only allowed network call.

**Triggers:** "animated diagram", "communication flow diagram", "HTML flow animation", "show me the flow with animation"

---

## Approach: DOM + SVG (Default)

**Use this unless the user explicitly asks for ASCII art.**

DOM-positioned node boxes + SVG arrow paths. More reliable output, ~30% smaller prompt, same terminal aesthetic via CSS.

- Nodes = `<div class="node">` positioned absolutely inside a relative container
- Arrows = `<svg>` overlay with `<path>` elements + `stroke-dashoffset` animation for traveling packets
- Terminal aesthetic via CSS: dark background, monospace font, glow effects, scanline overlay
- **All topology is built from JS arrays — never hardcode nodes or SVG in HTML**

### Topology Spec: NODES

```js
const NODES = {
  [nodeId]: { id, label, sub, badge, badgeColor, x, y, w, h }
}
// label     — primary box title
// sub       — smaller subtitle (port, endpoint)
// badge     — optional third line (e.g. '[HTTP — NETWORK]', '[SAME JVM]')
// badgeColor — 'orange' | 'accent' | null
// x, y, w, h — absolute px coordinates within the container
```

### Topology Spec: ARROWS

```js
const ARROWS = [
  { id, x1, y1, x2, y2, labelId, type: 'orange'|'green'|'mixed', packetMs }
]
// x1,y1 / x2,y2 — absolute px start and end tips within the container
// labelId        — id of the matching SVG <text> element
// packetMs       — packet travel duration; varies by call type:
//                  HTTP calls: 600–900ms  |  in-process calls: 100–250ms
```

### buildTopologyDOM()

Called once at boot and on mode change. Reads NODES and ARROWS arrays, generates all `<div class="node">` and SVG `<path>` + `<text>` elements. **Never place topology HTML by hand.**

SVG must include `<defs>` with named `<marker>` arrowheads for each color (orange, green, err, dim, accent) so arrow color changes can be applied by swapping `marker-end` attribute only.

---

## Approach: ASCII in `<pre>` (Secondary)

Use only when the user explicitly wants ASCII art or terminal-exact rendering.

**Risk:** Character alignment breaks across regenerations and font fallbacks. Every regeneration may need manual arrow fixes.

**Use `innerHTML` on `<pre id="diagram">`, NOT `textContent`** — spans must be injected for color.

Topology: paste exact ASCII layout. Use ONE layout only — never provide two competing layouts in the same prompt.

---

## Shared Spec (Both Approaches)

### cfg Object Pattern

The data model is approach-agnostic. Always define a typed cfg object:

```js
{
  // Node active flags (boolean) — true = glow highlight
  [nodeId]Active: boolean per node,

  // Arrow active flags (boolean) — true = animate arrow
  [arrowId]Active: boolean per arrow,

  // Arrow label text (string) — shown mid-arrow when active
  [arrowId]Text: string per arrow,

  // Failure flags (boolean) — true = red blinking on that arrow
  [arrowId]Fail: boolean per failure-capable arrow,

  // Floating label (shown below diagram)
  floatLabel: string,       // display text
  floatLabelType: string,   // style selector only: 'http'|'inprocess'|'error'|''

  // Annotation panel — per-step teaching note
  annotation: { title: string, text: string, type: 'http'|'inprocess'|'error'|'success'|'info' } | null,
}
```

`base()` returns all booleans false, all strings `''`, annotation `null`.

**Rules:**
- `floatLabel` is the exact display text
- `floatLabelType` controls color and prefix icon only — never overrides `floatLabel`
- Arrow color rules must be explicit for every arrow — never leave any arrow without a color rule
- Step counts in button descriptions must NOT be hardcoded — use `getSteps().length - 1`

### getSteps() Function

```
Returns array of {cfg, log} objects. Index 0 = idle (base(), log null).
Reads module-level `mode` variable.

Each step may have: skipOn: ['mode-name', ...]
getSteps() filters: allSteps.filter(s => !s.skipOn || !s.skipOn.includes(mode))
This makes the dot row auto-adjust — never hardcode step counts.
```

### Animation Loop

```
Module-level: stepIndex, timer, paused, speedMultiplier (default 1), BASE_INTERVAL.

tick():
  1. Render getSteps()[stepIndex] via buildDiagram(cfg)
  2. Append log line → fade in via double-rAF (opacity 0 → shown class)
  3. updateDots(stepIndex)
  4. After 200ms delay: pulseArrowAndLog(activeArrowId, logLineEl)  [focus sync]
  5. stepIndex++
  6. If more steps and not paused: scheduleNextTick()
  7. If last step: onAnimationComplete()

scheduleNextTick(): setTimeout(tick, Math.round(BASE_INTERVAL / speedMultiplier))
  — higher multiplier = faster playback (divide, not multiply)

onAnimationComplete(): append blinking cursor line to log → showSummary()

startAnimation(): clearTimeout, stepIndex=0, paused=false, clear log, hide summary, setTimeout(tick, 500)
```

### Focus Sync

```
getActiveArrowId(cfg):
  Checks cfg flags in priority order — failure states first, then response arrows,
  then request arrows — returns the id of the single active arrow for this step.

pulseArrowAndLog(arrowId, logLineEl):
  Remove + re-add animation class on the SVG path (force reflow between).
  Same on the log line element. Both pulse together.
```

### Packet Animation (per arrow)

```
triggerPacketAnimation(pathEl, durationMs):
  totalLen = pathEl.getTotalLength()
  Set stroke-dasharray = 'packetLen gap' where gap = totalLen - packetLen
  Set stroke-dashoffset = totalLen  (packet at start)
  rAF loop: interpolate dashoffset from totalLen → 0 over durationMs
  On complete: clear dasharray and dashoffset

Uses ARROWS[n].packetMs — NOT BASE_INTERVAL — so HTTP arrows travel slowly
and in-process arrows travel fast, visually encoding the latency difference.
```

### Learner Controls (include in all prompts)

- **Pause/play toggle** — sets `paused` flag; resume calls `scheduleNextTick()`
- **Clickable step dots** — only `.done` and `.current` dots are clickable; clicking calls `jumpToStep(n)` which renders that step's cfg (no packet animation) and resumes from n+1
- **Speed control** — 0.5× / 1× / 2× buttons set `speedMultiplier`; active button visually highlighted
- **Focus sync** — active arrow and corresponding log line pulse together (see Focus Sync above)

### Layout (top to bottom)

```
1. Header — title + subtitle
2. Controls row — scenario buttons + learner controls (pause, speed) right-aligned
3. Legend bar — always visible, never animated (color encoding IS the lesson)
4. Step dots row — one per step, skip index 0; recalculate on mode change via rebuildDots()
5. Diagram panel — node boxes + SVG arrows (DOM) or <pre> (ASCII)
6. Float label — fades in below diagram when floatLabel is set
7. Annotation panel — fades in/out per step (slide + opacity transition)
8. Log panel — "─── [LOG HEADER] ───" + <div id="log">
9. Summary panel — appears after last step
10. Replay button row
```

### Summary Line

Two lines after final step:
```
SUCCESS: "✓ {Flow} complete — {N} calls: {breakdown}"
         "  Next stage: {one sentence on architectural improvement}"
FAILURE: "✗ {Flow} failed at step {N} — {reason}"
         "  Next stage: {pattern that fixes this}"
```

Keyed per mode in a `msgMap` object — not generated dynamically.

### Log Lines

```
Format: [HH:MM:SS] STEP n  msg  STATUS
Append as <div class="log-line"> with opacity 0.
Fade in: double-rAF → add class "shown" (CSS transition handles opacity + translateY).
Scroll log container to bottom after each append.
Error STATUS spans blink.
```

### Boot

```
DOMContentLoaded → buildTopologyDOM() → render idle state → setTimeout(startAnimation, 600)
```

---

## Fill-in Guide

| Placeholder | DOM+SVG | ASCII |
|-------------|---------|-------|
| NODES array | `{id, label, sub, badge, badgeColor, x, y, w, h}` per node | — |
| ARROWS array | `{id, x1, y1, x2, y2, labelId, type, packetMs}` per arrow | Paste exact ASCII layout (one layout only) |
| Container size | e.g. 700×430px | `<pre>` width in characters |
| `[SYSTEM NAME]` | e.g. "NFS Lease Activation" | same |
| `[FONT NAME]` | e.g. "Share Tech Mono" | same |
| `[BASE_INTERVAL]` | Base delay, e.g. 1400 | same |
| `cfg` keys | One per node/arrow + annotation | same |
| Steps | `{cfg, log, skipOn?}` per frame | same |
| Mode values | e.g. `'all-up'`, `'fos-down'` | same |
| msgMap | One summary string per mode | same |

---

## CS Teaching Enhancements

For diagrams that teach systems communication concepts (HTTP vs in-process, blocking I/O, circuit breakers), extend with `diagram-cs-enhancements.md`:
- Blocking indicator (thread state)
- Latency tag (per call type)
- Variable packet speed (packetMs per arrow)
- Annotation panel content guidelines
