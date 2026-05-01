# Checklist: Any Solution or Proposed Change (Over-Engineering Guard)

Run this for any proposed solution — code, config, agent, skill, hook, workflow, or GEMINI.md addition — before approving.

**Core question: Is this the simplest solution that solves the actual, current problem?**

**Proportionality (YAGNI / KISS):**
- [ ] Does the solution solve a problem that exists today, not a hypothetical one?
- [ ] Would a simpler alternative (a note, memory entry, one-liner, or config value) solve the same problem?
- [ ] Is the number of new files / components proportional to the problem's scope?
- [ ] Can the solution be explained in one sentence without referencing its own internals?

**Complexity is justified ONLY when:**
- [ ] 3+ active, named use cases already exist (not "we might need this later")
- [ ] The cost of NOT having the infrastructure is measurable (e.g., X minutes lost per session, recurring errors)
- [ ] Long-term maintenance cost of the solution is lower than repeated manual workaround cost
- [ ] The abstraction is reused within the current project — not "someday"

**Red flags (each one is a signal, 2+ triggers REVISION_NEEDED):**
- [ ] New file type, config format, or runtime dependency introduced for a single use case
- [ ] Implementation took longer to build/debug than the problem it solves would have caused
- [ ] "Future extensibility" cited but no concrete future cases named
- [ ] Solution requires its own documentation to explain how to use it
- [ ] A simpler layer (memory, GEMINI.md line, inline comment) was skipped in favor of infrastructure
- [ ] The work has drifted from the original problem — solving a different or expanded problem than what was asked

**Verdict guidance:**
- 0 red flags + proportionality checks pass → APPROVED
- 1 red flag + clear complexity justification → APPROVED with note
- 2+ red flags → REVISION_NEEDED: propose the simpler alternative explicitly
- Complexity justified by 3+ active cases → APPROVED even if red flags present
