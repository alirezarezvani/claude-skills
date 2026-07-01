# MCP Client Setup

Use this reference when the user explicitly asks to connect Aident Loadout through MCP.

## Server URL

```text
https://loadout.aident.ai/mcp
```

## Claude Code

```bash
claude mcp add --transport http aident https://loadout.aident.ai/mcp
```

Or add an HTTP MCP server named `aident` to the user's Claude Code config.

## GitHub Copilot In VS Code

Add to `.vscode/mcp.json` in the project:

```json
{
  "servers": {
    "aident": {
      "type": "http",
      "url": "https://loadout.aident.ai/mcp"
    }
  }
}
```

Restart VS Code or reload the MCP server list after editing.

## Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "aident": {
      "url": "https://loadout.aident.ai/mcp"
    }
  }
}
```

## Gemini CLI

Add to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "aident": {
      "httpUrl": "https://loadout.aident.ai/mcp"
    }
  }
}
```

## Other MCP Clients

Use an HTTP MCP server named `aident` with the server URL above. Follow the client's documentation for exact config keys.

## Authentication

On first connection, the client should open a browser sign-in or authorization flow. After the user authorizes Aident, use the available Aident tools to list capabilities and check Vault connection state.

Do not ask the user to paste OAuth tokens, cookies, or raw provider API keys into chat.
