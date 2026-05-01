# Performance Maintenance Skill

**Purpose:** Automated and manual routines for keeping the `.gemini` workspace lean and fast.

## Maintenance Checklist (Weekly)

1. **Prune History:** Delete files in `~/.gemini/history/` older than 14 days.
2. **Clear Temp:** Delete files in `~/.gemini/tmp/` older than 7 days (especially `gemini-quality-*.md`).
3. **Session Check:** Ensure no single session file exceeds 5MB (high context cost).

## Pruning Script (PowerShell)

```powershell
# Prune History (14 days)
Get-ChildItem -Path "$HOME\.gemini\history\*" -Include *.* -Recurse | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-14) } | Remove-Item -Force

# Prune Temp (7 days)
Get-ChildItem -Path "$HOME\.gemini\tmp\*" -Include *.* -Recurse | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) } | Remove-Item -Force
```

## Strategy

- **Lazy Indexing:** Only index `knowledge/` and `documentation/` folders. Never let the agent index the full project root unless explicitly asked.
- **Topic Compaction:** Every 20 turns, the agent should summarize the entire session and suggest starting a new one to "clear the air" and reduce token pressure.
