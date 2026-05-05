---
name: documentation-specialist
description: 'Master skill for writing professional project and platform documentation.'
---

# Documentation Specialist Skill

Standard templates, conventions, and guidelines for professional microservice documentation.

## How to Use
1. **Consult:** Read `references/vocabulary.md` for tier labels and status values.
2. **Select:** Match project complexity to a tier in `references/tiers.md`.
3. **Voice:** Adopt the document-specific tone from `references/audience.md`.
4. **Draft:** Follow formatting rules in `references/standards.md`.
5. **Diagram:** Follow ASCII/Mermaid rules in `references/diagrams.md`.
6. **Verify:** Check facts against authoritative source per `references/verification.md`.

## Enforcement Rules
- **No Root Clutter:** unauthorized files at `documentation/` root will be moved.
- **Registry:** `projects/README.md` MUST be updated for every folder change.
- **Ownership:** One codebase = one folder. Link in global index is mandatory.

## Folder Structure
```
documentation/
├── projects/
│   ├── README.md               <-- Global Index
│   └── {service}/              <-- Project Root
│       ├── README.md           <-- Entry Point (Status Table)
│       ├── INTEGRATION.md      <-- API Contracts
│       ├── DEPLOYMENT.md       <-- Infrastructure
│       ├── API-REFERENCE.md    <-- Endpoint Details
│       ├── TECH-STACK.md       <-- Versions/ADRs
│       ├── DATABASE.md         <-- Data Model
│       ├── DOMAIN.md           <-- Logical Model
│       └── domain/             <-- Deep Dives (NN-*.md)
└── platform/                   <-- Cross-project docs
```

## Navigation Files (Auto-generated)
- `LEARNING-PATH.md`: Onboarding reading order (trigger: 5+ projects).
- `DOC-INDEX.md`: Theme-based tag index (trigger: 15+ docs).
