# Checklist: Designs / UI Wireframes / Mockups

## Requirements Coverage
- [ ] [critical] All functional requirements from the PRD addressed in the design? *Fail: one or more FRs have no corresponding UI element or flow.*
- [ ] All user stories covered by at least one screen or interaction? *Fail: a user story's primary task cannot be completed using the designed screens.*
- [ ] Out-of-scope features not introduced? *Fail: design includes UI for features not in the current PRD phase.*

## Component States
- [ ] Empty state designed (no data, first-time user)? *Fail: no empty state — UI shows blank space or broken layout when a list/table has no items.*
- [ ] Loading state designed? *Fail: no loading indicator — user sees blank content while data fetches or an action processes.*
- [ ] Error state designed (network failure, validation error, permission denied)? *Fail: no error feedback — user gets no signal when an operation fails.*
- [ ] All form fields have inline validation feedback? *Fail: errors shown only on submit — user cannot correct mistakes as they type.*
- [ ] Success/confirmation state designed for key actions? *Fail: no confirmation after save/submit — user cannot tell if action completed.*

## Interaction Clarity
- [ ] Primary action is visually dominant on each screen? *Fail: primary CTA is indistinguishable from secondary actions in size, color, or placement.*
- [ ] Interaction model unambiguous enough for an engineer to implement without design questions? *Fail: hover states, click targets, navigation flows, or modal triggers are undefined.*
- [ ] Destructive actions (delete, reset, overwrite) require confirmation? *Fail: destructive action executes immediately with no confirmation step.*
- [ ] Navigation paths between screens are all defined? *Fail: a screen in the flow has no defined entry or exit path.*

## Responsiveness & Accessibility
- [ ] Layout defined for all target breakpoints (mobile, tablet, desktop)? *Fail: only desktop designed — mobile/tablet behavior unspecified.*
- [ ] Text and interactive elements meet WCAG AA contrast (4.5:1 text, 3:1 large text/icons)? *Fail: low-contrast color combinations present that fail WCAG AA.*
- [ ] Keyboard navigation path defined for all interactive elements? *Fail: modal, dropdown, or form workflow cannot be operated without a mouse.*
- [ ] Focus indicators visible on all interactive elements? *Fail: focus state not shown — keyboard users cannot see where they are.*

## Design System Consistency
- [ ] Components use the established design system (colors, typography, spacing, icons)? *Fail: one-off values not from the design system — creates inconsistency and extra implementation work.*
- [ ] Interaction patterns consistent with the rest of the product? *Fail: the same action (e.g., confirm dialog, inline edit) works differently on different screens.*

**Verdict guidance** (global default applies — see CHECKLISTS.md)
