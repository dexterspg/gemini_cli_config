# Template: Artifact Generation / Multi-Phase

For prompts that instruct AI to produce visualizations, interactive HTML, structured outputs, or multi-step workflows.

**Length guidance:** No word limit. Completeness of specs is more important than brevity.

**Rules:**
- Every embedded code block (CSS, JSON, etc.) is a first-class specification — preserve it exactly
- Phased prompts must have explicit confirmation gates between phases ("Do NOT proceed until user confirms")
- Include a "How to Use" section — artifact prompts need human workflow, not just AI instructions
- Include graceful degradation — what to do when input is malformed, too complex, or missing sections
- Include at least one minimal example showing both input AND expected output
- For visual artifacts: consider adding rendering levels (wireframe → styled → interactive). Include an upgrade path so the model is extracted once and re-rendered at higher fidelity on request.
- May be platform-specific (e.g., Claude artifacts). Portability is secondary to completeness.

```markdown
# [Artifact Name]

[One-sentence description of what the AI will generate.]

---

## How to Use This Prompt

[Numbered steps for the HUMAN user — what to copy, where to paste, what to fill in, what to do if output is wrong.]

---

## Modes (if applicable)

| Mode | What it produces | When to use |
|------|-----------------|-------------|
| mode-a | [description] | [when to pick this] |
| mode-b | [description] | [when to pick this] |

[Default mode. How to select a different mode.]

## Rendering Levels (if applicable)

| Level | What it renders | When to use |
|-------|----------------|-------------|
| wireframe | Layout and structure only, no color/animation | Verify correctness fast |
| styled | Adds colors, typography, dark mode — static | Documentation, reference |
| interactive | Adds animation, navigation, interactivity | Full experience |

[Default level. Upgrade path instruction.]

---

## Phase 1 — [Extract / Parse / Prepare]

[What the AI does BEFORE generating the artifact.]

[JSON schema or structured format.]

**Rules for extraction:**
- [Rule 1]
- [Rule 2]

Do NOT proceed to Phase 2 until the user confirms.

---

## Phase 2 — [Generate / Render / Build]

### Rendering level specs
- wireframe: [minimal specs]
- styled: [adds color palette, badges, legend]
- interactive: [adds animation, navigation]

Keep the same model from Phase 1 — do NOT re-extract. Just re-render at the new level.

### Shared specifications
[Color palettes (CSS variables), styling rules, layout rules.]

### If MODE = mode-a
[Mode-specific rendering rules.]

### If MODE = mode-b
[Mode-specific rendering rules.]

---

## Graceful Degradation

- [Too many components → how to simplify]
- [Missing input sections → how to infer or ask]
- [Rendering failure → fallback behavior]

---

## Minimal Example

### Input:
[Small, complete example input.]

### Expected output:
[Description or mockup of what the artifact should look like.]

---

## [Input Section Name]

[MODE: mode-a | mode-b] (default: mode-a)

[PASTE YOUR INPUT HERE]
```
