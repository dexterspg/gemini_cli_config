# Jira Attachments — Download Fallback, Upload and Embed

The download sections below are a fallback for when `mcp__jira__download_jira_attachments` is unavailable (MCP server not running, or working outside Gemini CLI). The section "Upload and Embed in a Comment or Description" is the primary path: no MCP tool uploads files.

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

## Upload and Embed in a Comment or Description

Used by SKILL.md → "LAE Script Delivery Comment Template" and "LAE Description Template". Run from Bash; `.env` holds the credentials. Four steps:

```bash
source /c/workarea/jira_manager/.env

# 1. Upload (the X-Atlassian-Token header is required; the response lists the attachment id)
curl -s -X POST "https://nakisa.atlassian.net/rest/api/3/issue/{TICKET_KEY}/attachments" \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -H "X-Atlassian-Token: no-check" -F "file=@{ABSOLUTE_FILE_PATH}" \
  | python -c "import json,sys; [print(a['id'], a['filename']) for a in json.load(sys.stdin)]"

# 2. Media UUID: the 303 Location (no -L) holds /file/<uuid>/binary?token=...; print only the UUID, never the URL
curl -s -o /dev/null -D - -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "https://nakisa.atlassian.net/rest/api/3/attachment/content/{ATTACHMENT_ID}" \
  | python -c "import re,sys; print(re.search(r'/file/([0-9a-f-]{36})/', sys.stdin.read()).group(1))"
```

If step 1 prints no id, stop and report; never re-run step 1 without first listing the ticket's attachments, because a blind retry uploads a duplicate.

3. Put this node in the comment ADF where the file should appear (`collection` stays an empty string):

```json
{"type":"mediaGroup","content":[{"type":"media","attrs":{"type":"file","id":"<UUID>","collection":""}}]}
```

   New comment: `mcp__jira__update_jira_issue(issue_key, comment_adf=<doc>)` (UNVERIFIED with a media node). Existing comment (the MCP has no edit tool): `PUT /rest/api/3/issue/{TICKET_KEY}/comment/{COMMENT_ID}` with `{"body": <doc>}`; list comment ids with `GET /rest/api/3/issue/{TICKET_KEY}?fields=comment`.

   Description (the MCP takes plain text only): `PUT /rest/api/3/issue/{TICKET_KEY}` with `{"fields": {"description": <doc>}}`, where `<doc>` is the whole description ADF with the node placed in it. An image uses `{"type":"mediaSingle","attrs":{"layout":"center"},"content":[<the media node>]}` instead of `mediaGroup`.

4. Verify: a comment: `GET /rest/api/3/issue/{TICKET_KEY}/comment/{COMMENT_ID}`; a description: `GET /rest/api/3/issue/{TICKET_KEY}?fields=description`. The ADF must show the node with the same UUID, and the ticket must still list one copy of the file. For a REST comment `PUT`, its 200 response body counts as the read-back; the MCP path still needs the `GET`.

Verified on this tenant: the REST `PUT` of a comment with a `mediaGroup` node (LAE-44301, 2026-11-06: HTTP 200, body round-tripped). UNVERIFIED: the MCP `comment_adf` path with that node, descriptions, and `mediaSingle` images. Read the ADF back on first use and report if Jira rejects it. A failure at step 2 (no `/file/<uuid>/` in the Location) means stop and report, not guess an id.
