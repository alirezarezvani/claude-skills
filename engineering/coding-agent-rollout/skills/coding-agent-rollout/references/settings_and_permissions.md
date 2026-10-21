# Settings and permissions for a team

How Claude Code combines settings files, how permission rules are evaluated,
and which keys only mean something in managed settings. Every key name here is
checked against the official docs; `settings_linter.py` encodes the same facts.

Confidence key: 🟢 verified on code.claude.com/docs · 🟡 observed locally, not documented · 🔴 recommendation.

## 1. Five scopes, one effective policy

| Scope | File | Who controls it |
|---|---|---|
| Managed | macOS `/Library/Application Support/ClaudeCode/managed-settings.json`, Linux/WSL `/etc/claude-code/managed-settings.json`, Windows `C:\Program Files\ClaudeCode\managed-settings.json`, plus `managed-settings.d/*.json` drop-ins | IT / MDM |
| Command line | `--settings <file-or-json>` | whoever launches |
| Project local | `.claude/settings.local.json` | one person, not committed |
| Shared project | `.claude/settings.json` | the repo, via code review |
| User | `~/.claude/settings.json` | one person |

Precedence, highest first: managed > command line > project local > shared
project > user. 🟢 [settings] Within managed, remote/server-managed beats MDM
(macOS plist domain `com.anthropic.claudecode`, Windows `HKLM\SOFTWARE\Policies\ClaudeCode`)
beats files beats `HKCU`; `managedSourcesBehavior: "merge"` combines them. 🟢 [managed-settings]
A managed file that exists but does not parse stops Claude Code from starting. 🟢 [managed-settings]

**Arrays merge, they do not override.** `permissions.allow` from user settings
is added to the project's list. 🟢 [settings] This is the single most common
team surprise: a strict shared file does not make a permissive user file stricter.

## 2. Permission evaluation

- Order: **deny, then ask, then allow; first match wins**; specificity does not
  matter. An allow cannot carve an exception out of a deny, and an ask beats a
  more specific allow. 🟢 [permissions]
- A deny at any level cannot be overridden by another level; a managed deny
  cannot be overridden by `--allowedTools`. 🟢 [permissions]
- Project `permissions.allow` and `additionalDirectories` take effect only after
  the workspace trust dialog is accepted; deny and ask apply immediately. 🟢 [permissions]

### Rule syntax that matters for linting

| Form | Meaning |
|---|---|
| `Bash(npm run test *)` | prefix match; legacy `Bash(npm run test:*)` is equivalent only at the end of the pattern 🟢 |
| `Read(./.env)` / `Read(//**/.env)` | gitignore syntax; `//` absolute, `~/` home, `/` relative to the settings file's source, `./` relative to cwd 🟢 |
| `WebFetch(domain:example.com)` | that host only; `domain:*.example.com` covers subdomains, not the apex; `domain:*` is every domain 🟢 |
| `mcp__server`, `mcp__server__*`, `mcp__server__tool` | valid MCP forms; an `mcp__` rule with parentheses is skipped 🟢 |
| `"*"` or `"mcp__*"` in **allow** | ignored; valid only in deny/ask 🟢 |

Rules that try to constrain shell arguments are documented as fragile. 🟢 [permissions]
Treat a `Bash(...)` allow as "this command family runs unprompted", not as a
sandbox, and put destructive families on `ask` or `deny`. 🔴

## 3. Modes and the switches that disable them

`permissions.defaultMode`: `default` (alias `manual`), `acceptEdits`, `plan`,
`auto`, `dontAsk`, `bypassPermissions`. 🟢 [settings-reference]
`auto` and `bypassPermissions` are **ignored** when set in project or local
files. 🟢 [settings] `settings_linter.py` reports them there as dead config.

`permissions.disableBypassPermissionsMode` and `permissions.disableAutoMode`
take the string `"disable"`. They are valid in any file, but only enforced
fleet-wide from managed settings; with bypass disabled, Claude Code rejects
`--dangerously-skip-permissions`. 🟢 [settings-reference]

## 4. Managed-only keys

Meaningful only from managed sources (selection): `allowManagedPermissionRulesOnly`,
`allowManagedHooksOnly`, `allowManagedMcpServersOnly`, `managedMcpServers`,
`strictKnownMarketplaces`, `blockedMarketplaces`, `strictPluginOnlyCustomization`
(`true` or a list of `skills`, `agents`, `hooks`, `mcp`), `disableSideloadFlags`,
`forceRemoteSettingsRefresh`, `sandbox.network.allowManagedDomainsOnly`. 🟢 [managed-settings]

Three settings for a locked-down organization, in the order to adopt them: 🔴
1. `allowManagedHooksOnly` — hooks run arbitrary commands on every tool call.
2. `allowManagedMcpServersOnly` with an `allowedMcpServers` list.
3. `allowManagedPermissionRulesOnly` — only once the managed allow list is good
   enough that nobody needs a local rule to get work done.

## 5. Secrets and telemetry from repo files

- An `env` block in project or local settings **cannot** turn telemetry on
  (`CLAUDE_CODE_ENABLE_TELEMETRY`, `OTEL_*` exporters and content flags) or set
  `CLAUDE_CONFIG_DIR`, `HOME`, `TMPDIR`, `XDG_*`; only "off" values apply. 🟢 [settings-reference]
- Opt-outs: `DISABLE_TELEMETRY` (any non-empty value), `DISABLE_ERROR_REPORTING`,
  `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` (updates, telemetry, error reporting,
  feedback, release notes, feature flags). 🟢 [env-vars]
- Credentials belong in `apiKeyHelper` or the platform's secret store, never in
  a committed `env` block. 🔴

## 6. Local-file hygiene

Claude Code adds `.claude/settings.local.json` to the global git excludes when
it writes it. 🟢 [settings] If one is tracked anyway, someone added it on
purpose or before that behaviour existed; `settings_linter.py` blocks on it.

## Sources

1. Claude Code docs — Settings. https://code.claude.com/docs/en/settings
2. Claude Code docs — Settings reference. https://code.claude.com/docs/en/settings-reference
3. Claude Code docs — Permissions. https://code.claude.com/docs/en/permissions
4. Claude Code docs — Managed settings. https://code.claude.com/docs/en/managed-settings
5. Claude Code docs — Environment variables. https://code.claude.com/docs/en/env-vars
6. Claude Code docs — Security. https://code.claude.com/docs/en/security
7. NIST SP 800-53 Rev. 5, AC-6 Least Privilege. https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
