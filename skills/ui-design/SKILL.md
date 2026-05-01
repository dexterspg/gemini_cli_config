---
name: ui-design
description: Generate interactive HTML UI designs for frontend projects.
---

# UI Design Skill

Generate interactive HTML UI designs for frontend projects. Three fidelity levels available.

## Fidelity Levels

### Mockup (`--mockup`)

Production-grade visual design with:
- Custom fonts (Google Fonts — distinctive pairs, never generic)
- CSS custom properties design token system (colors, spacing, radius, shadows)
- Brand-aligned color palette with accent, surfaces, borders, status colors
- Refined shadows, hover states, transitions, animations
- Professional typography hierarchy (display + mono for data)
- SVG icons inline — no external icon libraries
- All UI states (empty, populated, loading, error, success)
- Responsive breakpoints

**Use when:** Presenting to stakeholders, establishing a visual direction, creating a pixel-level reference for implementation. This is the final visual design before coding.

**Output:** Single self-contained HTML file. No external JS. All styles inline via `<style>` block.

### Wireframe (`--wireframe`)

Medium-fidelity structural layout with:
- Basic fonts and simple color palette
- Layout structure, navigation, and content hierarchy
- Functional elements (buttons, forms, tables) with minimal styling
- Screen labels to annotate each screen

**Use when:** Agreeing on layout, structure, and user flow before investing in visual polish.

**Output:** Single self-contained HTML file. No external JS. All styles inline via `<style>` block.

### Sketch (`--sketch`)

Minimal black-and-white structural sketch with:
- `system-ui` font only — no custom fonts, no Google Fonts
- Black borders, white/gray backgrounds — no brand colors except one accent for active states
- No shadows, no gradients, no animations
- Simple 2px borders for structure
- Screen labels (`<div class="page-label">`) to annotate each screen

**Use when:** Quick iteration, internal discussion, presenting layout before committing to design, time-constrained.

**Output:** Single self-contained HTML file. No external JS. All styles inline via `<style>` block.

## SDLC Position

UI design sits between **Product Requirements** and **Technical Specification** in the SDLC:

1. Product Requirements (what and why)
2. **UI Design** — wireframe/mockup (how the user sees it)
3. Technical Specification (how to build it — references the UI design)

The tech spec should reference the mockup/wireframe screens so architects design APIs and components around approved UI flows.   

## Structure Rules (All Levels)

1. **One HTML file** — all screens stacked vertically, separated by dividers
2. **Screen labels** — each screen gets a visible label identifying what state it represents
3. **Real data** — use realistic placeholder data from the project domain, not "Lorem ipsum"
4. **All states** — show empty, populated, loading, error, and success states where applicable
5. **Navigation** — if the app has multiple pages, show the full nav in every screen with the active state highlighted
6. **Interactive elements** — buttons, tabs, upload zones, tables should look like their real counterparts (static, not functional)

## Process

1. **Read the product requirements** — understand user stories, functional requirements, and scope
2. **Identify all screens** — map requirements to frontend views; include every state (empty/loaded/error)
3. **Choose fidelity** — based on user request or context
4. **Build the HTML** — single file, all screens, self-contained
5. **Review against requirements** — verify all FRs with UI implications are represented
6. **Write to path decided by the main session** — do not decide filenames or versions independently

## Naming and Versioning

File names and version numbers are decided by the main session. This skill does not assign version numbers or append fidelity suffixes to filenames.

## Templates

Reusable starting points for common UI patterns. Copy the template file and adapt to the new project.

| Template | Path | Description |
|----------|------|-------------|
| Enterprise SaaS (sidebar + content) | `C:/workarea/report_generator/webapp/mockup-v1.html` | Full-screen app shell with blue gradient sidebar nav, upload zones, readiness checks, file-attached state, processing spinner with step indicators, error state with detail box, results with stat cards, config pages with card layout, history table. Outfit + IBM Plex Mono fonts, Nakisa blue palette. |

### Template Conventions

- **All states shown:** empty, file-uploaded, processing, error, success — each as a separate full-screen page stacked vertically
- **Sidebar nav** repeated on every page with correct active state
- **CSS variables** for all tokens (colors, spacing, radius, shadows) — rebrand by changing `:root` values
- **SVG icons** inline — no external icon libraries
- **Page labels** (`<div class="page-label">`) annotate each screen's purpose
- **Responsive** breakpoints at 768px and 640px

### How to Use a Template

1. Copy the template file to the new project's UI design location
2. Update `:root` CSS variables for the new brand (colors, fonts)
3. Replace page content (headings, labels, field names, sample data)
4. Add/remove pages as needed for the new project's screen set
5. Keep the same component classes (`.upload-zone`, `.card`, `.readiness-card`, `.file-attached`, `.processing-overlay`, `.error-box`, `.results-hero`, `.stat-box`) — they are pre-styled

## When to Use Which

| Signal from user | Level |
|-----------------|-------|
| "mockup", "UI design", "visual design", "polished design" | Mockup |
| "wireframe", "layout", "structure" | Wireframe |
| "quick wireframe", "sketch", "simple wireframe", "lightweight" | Sketch |
| "for presentation" / "for stakeholders" | Mockup |
| "for internal" / "for dev discussion" | Wireframe or Sketch |
| "make it less styled" / "too much" / "overkill" | Drop one level |
