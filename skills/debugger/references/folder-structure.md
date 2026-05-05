# Debugger: Folder Structure

Investigative artifacts are saved to `{issues-dir}/{issue-folder}/`.

```
{issues-dir}/
  README.md                        ← Registry of all issues
  {issue-folder}/
    _INTAKE.md                     ← Symptom, source, environment, attachments
    attachments/                   ← ALL input files (read-only intake folder)
    investigation.md               ← Findings-first report
    debugging-walkthrough.md       ← Step-by-step reasoning trace
    fix/                           ← Corrections ready to deploy
    │   README.md                      what changed, how to apply
    validation/                    ← Proof the fix works
        before/                        broken state evidence
        after/                         fixed state evidence
        notes.md                       validation metadata
```

## `attachments/` Content Types
- Config/customization files (old vs new)
- Log files (server, app)
- Screenshots (decoded text)
- Network traces (HAR, API captures)

## `_INTAKE.md` Template
```markdown
# Intake: [Ticket ID or title]

## Reported Symptom
[Verbatim user observation. Do NOT rephrase technically.]

## Source
- Ticket: [URL]
- Reported by: [name]
- Date: [YYYY-MM-DD]

## Environment
- Application/Version: [exact]
- Environment: [prod/staging/QA]

## Attachments
- [ ] [filename] — [content] — [source]

## Initial Notes
[Technical context added AFTER reading report.]
```
