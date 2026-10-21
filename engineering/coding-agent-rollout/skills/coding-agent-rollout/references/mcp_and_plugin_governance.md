# MCP servers, plugins and marketplaces

Every MCP server is code that runs with an engineer's credentials, and every
plugin can bring hooks, agents and its own MCP servers. This is what
`mcp_plugin_inventory.py` reads and why each check exists.

Confidence key: 🟢 verified on code.claude.com/docs or the cited source · 🔴 recommendation.

## 1. Where MCP servers come from

| Scope | Location | Committed? |
|---|---|---|
| Local (default for `claude mcp add`) | `~/.claude.json` → `projects["<path>"].mcpServers` | no |
| Project | `.mcp.json` at the repo root, key `mcpServers` | yes |
| User | `~/.claude.json` → `mcpServers` | no |
| Managed | `managedMcpServers`, or `managed-mcp.json` beside `managed-settings.json` | IT |

Precedence: managed > local > project > user > plugin > claude.ai connectors;
same-name entries are not merged. 🟢 [mcp] `.mcp.json` expands `${VAR}` and
`${VAR:-default}`, so a committed file never needs a literal secret. 🟢 [mcp]
`managed-mcp.json` takes exclusive control; `{"mcpServers": {}}` disables MCP. 🟢 [managed-mcp]

## 2. Approval

- Project servers need approval. `enabledMcpjsonServers` / `disabledMcpjsonServers`
  approve by name; `enableAllProjectMcpServers: true` approves **everything**
  in `.mcp.json`, including the server a teammate adds next week. A committed
  `enable*` value is ignored in an untrusted folder. 🟢 [settings-reference]
- `allowedMcpServers` / `deniedMcpServers` entries take exactly one of
  `serverUrl` (supports `*`), `serverCommand` (exact array) or `serverName`
  (exact; the docs note a name alone is not a security control). Unset allowlist
  = everything allowed; `[]` = nothing. Deny always wins and merges from every
  scope; allowlists also merge unless `allowManagedMcpServersOnly: true`. 🟢 [managed-mcp]

**Recommendation:** approve by `serverUrl` or `serverCommand` in managed
settings, and keep the human-readable allowlist file (`approved-components.json`)
for the inventory diff. 🔴

## 3. Pinning

An `npx -y some-mcp-server` entry runs whatever version the registry serves
that day. OWASP lists supply-chain compromise and excessive agency among the
top risks for LLM applications; an unpinned server with broad tool access is
both. 🟢 [OWASP] Pin the package (`pkg@1.4.2`, `pkg==0.6.2`) and update it on
purpose. 🔴

## 4. Plugins and marketplaces

- `enabledPlugins` maps `"name@marketplace"` to a boolean; a managed `false`
  blocks the plugin everywhere. 🟢 [settings-reference]
- `extraKnownMarketplaces` (alias `additionalMarketplaces`) registers sources;
  from a repo file it applies only after trust. 🟢 [settings-reference]
- `strictKnownMarketplaces` (managed) is the source allowlist; `[]` blocks every
  marketplace, the official one included. `blockedMarketplaces` (managed) takes
  the same source objects, including `"owner/*"`. 🟢 [settings-reference]
- `strictPluginOnlyCustomization` locks skills, agents, hooks and/or MCP to
  plugin and managed sources, so customization ships only through reviewed
  plugins. 🟢 [managed-settings]

Pin a git or GitHub marketplace with `ref` so its contents cannot change between
review and install. 🔴

## 5. Review checklist for a new server or plugin

1. Who maintains it, and is the source readable? (Open source or internal.)
2. What credentials does it receive? Scope them to read-only where possible.
3. Which tools does it expose? Deny the destructive ones with `mcp__server__tool` rules.
4. Is it pinned?
5. Does it send data off the machine, and is that allowed by your data policy?
6. Who owns it on your side, and when is it re-reviewed?

A plugin or server that fails 5 is a data-protection question before it is an
engineering one. 🔴

## Sources

1. Claude Code docs — MCP. https://code.claude.com/docs/en/mcp
2. Claude Code docs — Managed MCP. https://code.claude.com/docs/en/managed-mcp
3. Claude Code docs — Settings reference. https://code.claude.com/docs/en/settings-reference
4. Claude Code docs — Managed settings. https://code.claude.com/docs/en/managed-settings
5. Claude Code docs — Permissions (MCP rule forms). https://code.claude.com/docs/en/permissions
6. OWASP Top 10 for LLM Applications. https://genai.owasp.org/llm-top-10/
