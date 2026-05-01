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
5. **Logging:** Append a record to `C:/Users/dexte/.gemini/maintenance-log.md` using this format:
   ```md
   | Timestamp | Action | Count | Size (MB) | Status |
   |-----------|--------|-------|-----------|--------|
   | YYYY-MM-DD HH:MM | Prune history/tmp | 42 | 12.5 | Success |
   ```

## 2. Pruning Rules & Logic

- **history/**: Prune files older than **14 days**.
- **tmp/**: Prune files older than **7 days**. 
- **Critical File Protection (tmp/):** Do NOT prune files containing `gemini-quality-` or `review-` in the filename if they were modified within the last **24 hours**. These are "critical reviews" in progress. If unsure, skip and flag to user.
- **Grace Period:** NEVER prune files modified within the last **60 minutes** (active session safety).
- **Error Handling:** 
  - Pre-check that `history/`, `tmp/`, and `history/archived/` exist; create them if missing.
  - Handle locked-file errors gracefully (log and skip, do not abort).

## 3. Pruning Scripts

### PowerShell (Windows)
```powershell
# Step 1: Directory Check
$dirs = @("C:\Users\dexte\.gemini\history", "C:\Users\dexte\.gemini\tmp", "C:\Users\dexte\.gemini\history\archived")
foreach ($dir in $dirs) { if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir } }

# Step 2: Dry Run
$cutoffHistory = (Get-Date).AddDays(-14)
$cutoffTmp = (Get-Date).AddDays(-7)
$criticalMargin = (Get-Date).AddDays(-1)
$safetyMargin = (Get-Date).AddMinutes(-60)

$files = Get-ChildItem -Path $dirs[0..1] -Recurse -File | Where-Object {
    (($_.FullName -like "*\history\*" -and $_.LastWriteTime -lt $cutoffHistory) -or
     ($_.FullName -like "*\tmp\*" -and $_.LastWriteTime -lt $cutoffTmp)) -and
    !($_.Name -match "quality|review" -and $_.LastWriteTime -gt $criticalMargin)
} | Where-Object { $_.LastWriteTime -lt $safetyMargin }

$summary = $files | Measure-Object -Property Length -Sum
Write-Output "Dry Run Result: $($summary.Count) files found ($([Math]::Round($summary.Sum / 1MB, 2)) MB)"
```

### Bash (MINGW64)
```bash
# Step 1: Directory Check
mkdir -p ~/.gemini/history ~/.gemini/tmp ~/.gemini/history/archived

# Step 2: Dry Run
# History + Tmp combined summary (Count + MB)
find ~/.gemini/history ~/.gemini/tmp -type f \( \( -path "*/history/*" -mmin +20160 \) -o \( -path "*/tmp/*" -mmin +10080 \) \) ! -mmin -60 ! \( \( -name "*quality*" -o -name "*review*" \) -mmin -1440 \) -exec ls -l {} + | awk '{sum+=$5} END {print "Dry Run Result: "NR" files found, "sum/1024/1024" MB"}'
```

## 4. Session & Agent Maintenance

### Session Management (5MB Cap)
- **Rule:** If the current session context (visible in tool outputs or history) exceeds **5MB**, it must be compacted.
- **Action:** 
  1. Use `read_file` to capture the current session history if available.
  2. Write a summary to `C:/Users/dexte/.gemini/history/archived/YYYY-MM-DD-summary.md`.
  3. Inform the user: "Session size limit reached (X MB). A summary has been archived. Please start a new session to maintain performance."

### Topic Compaction (Turn Counter)
- **Turn Definition:** 1 Turn = 1 User Message + 1 Agent Response.
- **Rule:** Every **20 turns**, the agent must call `update_topic` with a comprehensive `summary` of the session's achievements and pending tasks. 
- **Compaction Intent:** The agent should state: "We have reached turn 20. I have summarized our progress to keep the context lean. Strategic intent: [Summary]."

### Agent Integrity Check
- **Trigger:** During every **Weekly Maintenance Check** or when the user says "clean up workspace".
- **Action:** Scan `C:/Users/dexte/.gemini/agents/*.md`. Verify that all referenced skills in the `activate_skill` instructions exist in `C:/Users/dexte/.gemini/skills/`. Flag broken links.

## 5. Scope
Maintenance applies to:
- `history/` (Retention: 14 days)
- `tmp/` (Retention: 7 days)
- `agents/` (Broken reference check)
- Current Session (Size cap: 5MB)
