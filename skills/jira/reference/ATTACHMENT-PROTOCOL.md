# Jira Attachment Download — Fallback Protocol

Use this only when `mcp__jira__download_jira_attachments` is unavailable (MCP server not running, or working outside Gemini CLI).    

## Fallback: REST API

API **v3** is required (v2 returns 403 on this tenant as of 2026-04 — re-verify if Atlassian deprecates v3). `-L` follows the redirect from the API to S3.

```bash
source /c/workarea/jira_manager/.env

# List attachment IDs
curl -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "https://nakisa.atlassian.net/rest/api/3/issue/{TICKET_KEY}?fields=attachment" \
  | python -c "import json,sys; [print(a['id'], a['filename']) for a in json.load(sys.stdin)['fields']['attachment']]"

# Download by ID
curl -s -L -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "https://nakisa.atlassian.net/rest/api/3/attachment/content/{ATTACHMENT_ID}" \
  -o "attachments/{FILENAME}"

# Verify (HTML-as-zip is the silent failure to catch; file -b alone is not enough)
verify_attachment() {
  local f="$1"
  [ -s "$f" ] || { echo "FAIL: $f is empty"; return 1; }
  if head -c 200 "$f" 2>/dev/null | grep -qiE '<!doctype html|<html|<head'; then
    echo "FAIL: $f is HTML (auth/error page saved as expected file)"; return 1
  fi
  echo "OK: $f"
}
verify_attachment "attachments/{FILENAME}" || exit 1
```

## Failure categorization (do not blindly retry)

| Symptom | Cause | Action |
|---|---|---|
| File is HTML (`<!DOCTYPE html>`) | Auth not loaded — `.env` not sourced or vars empty | Re-source `.env`, verify `$JIRA_EMAIL` and `$JIRA_API_TOKEN` are set, retry once |
| HTTP 401/403 returned | Token expired or wrong scope | Surface the response to the user; do NOT retry — token rotation is required |
| HTTP 429 | Rate limited | Wait 30s, retry once |
| HTTP 5xx | Atlassian transient | Retry with 5s backoff, max 2 attempts |
| Network error / timeout | Connectivity | Retry once; if still failing, ask user to drop files manually |
| File is 0 bytes after success exit | Likely missing `-L` (followed redirect not honored) | Re-run with `-L` flag |

If recovery fails after the action above, **stop and surface the failure** — do not guess root cause from missing evidence.
