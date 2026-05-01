---
name: performance-maintenance
description: Use when keeping the Gemini workspace lean and performant. Triggers when: "clean up workspace", "prune history", "workspace is slow", "run maintenance", "clear temp files", "weekly maintenance check".
---

# Performance Maintenance Skill

**Purpose:** Comprehensive maintenance of the `.gemini` workspace to ensure low latency and context efficiency.

## 1. Safety-First Pruning Protocol

ALL pruning operations must follow this sequential protocol:

1. **Dry-Run:** Execute the pruning script in dry-run mode (`-WhatIf` in PowerShell) to calculate the file count and total size of the candidates for deletion.
2. **User Disclosure:** Present the summary (File count + Total size) to the user.
3. **Explicit Confirmation:** Require the user to type "confirm" or "yes" before proceeding.
4. **Execution:** Only run the actual deletion after confirmation.
5. **Logging:** Append a record of deleted files with a timestamp to `C:/Users/dexte/.gemini/maintenance-log.md`.

## 2. Pruning Rules & Logic

- **history/**: Prune files older than **14 days**.
- **tmp/**: Prune files older than **7 days**. (Check for critical reviews; skip and flag to user if unsure).
- **Grace Period:** NEVER prune files modified within the last **60 minutes** (active session safety).
- **Error Handling:** Pre-check directories exist. Handle locked-file errors gracefully (log and skip, do not abort).

## 3. Pruning Scripts

### PowerShell (Windows)
```powershell
# Step 1: Dry Run
$targetDirs = @("C:\Users\dexte\.gemini\history", "C:\Users\dexte\.gemini\tmp")
$cutoffHistory = (Get-Date).AddDays(-14)
$cutoffTmp = (Get-Date).AddDays(-7)
$safetyMargin = (Get-Date).AddMinutes(-60)

$files = Get-ChildItem -Path $targetDirs -Recurse -File | Where-Object {
    ($_.FullName -like "*\history\*" -and $_.LastWriteTime -lt $cutoffHistory) -or
    ($_.FullName -like "*\tmp\*" -and $_.LastWriteTime -lt $cutoffTmp)
} | Where-Object { $_.LastWriteTime -lt $safetyMargin }

$summary = $files | Measure-Object -Property Length -Sum
Write-Output "Dry Run Result: $($summary.Count) files found ($($summary.Sum / 1MB) MB)"

# Step 2: Confirmation required from user...

# Step 3: Actual Deletion (after confirm)
# $files | Remove-Item -Force -ErrorAction SilentlyContinue
```

### Bash (MINGW64)
```bash
# Step 1: Dry Run
# History: older than 14 days AND not modified in last 60 minutes
find ~/.gemini/history -type f \( -mmin +20160 \) ! -mmin -60 -exec ls -l {} + | awk '{sum+=$5} END {print "History: "NR" files, "sum/1024/1024" MB"}'

# Tmp: older than 7 days AND not modified in last 60 minutes
find ~/.gemini/tmp -type f \( -mmin +10080 \) ! -mmin -60 -exec ls -l {} + | awk '{sum+=$5} END {print "Tmp: "NR" files, "sum/1024/1024" MB"}'
```

## 4. Session & Agent Maintenance

### Session Management (5MB Cap)
- **Rule:** If a single session file exceeds **5MB**, it must be compacted.
- **Action:** 
  1. Summarize the session into `C:/Users/dexte/.gemini/history/archived/YYYY-MM-DD-summary.md`.
  2. Prompt the user to start a new session (`/clear` or similar).

### Topic Compaction (Turn Counter)
- **Turn Definition:** 1 Turn = 1 User Message + 1 Agent Response.
- **Rule:** Every **20 turns**, track the exchange count in the current session context and trigger the `update_topic` compaction rule.

### Agent Integrity Check
- **Rule:** Periodically scan `C:/Users/dexte/.gemini/agents/*.md`.
- **Action:** Verify that no agent definition references skills or files that no longer exist. Flag broken links to the user.

## 5. Scope
Maintenance applies to:
- `history/` (Retention: 14 days)
- `tmp/` (Retention: 7 days)
- `agents/` (Broken reference check)
- Current Session (Size cap: 5MB)
