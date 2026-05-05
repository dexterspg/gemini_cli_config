# Jira MCP Server — Setup & Configuration

## How it's registered

MCP servers must be in `~/.gemini.json` under `mcpServers` (NOT `~/.gemini/settings.json` — that key is ignored for MCP loading):   

```json
// ~/.gemini.json
{
  "mcpServers": {
    "jira": {
      "command": "python",
      "args": ["C:/workarea/jira_manager/src/jira_mcp_server.py"], 
      "cwd": "C:/workarea/jira_manager"
    }
  }
}
```

## Credentials

Loaded automatically from `/c/workarea/jira_manager/.env` (path is hardcoded relative to the script, so `cwd` doesn't affect it).     

## Troubleshooting

- **Tools not available in a session:** MCP server failed to connect at startup. Restart Gemini CLI — the server will re-attempt.  
- **Works from `~/.gemini/` but not other dirs:** Previously the config was only in `~/.gemini/settings.json` (wrong) and `~/.gemini/mcp.json` (project-local). Fixed by moving to `~/.gemini.json`.     
