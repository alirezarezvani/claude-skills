---
name: "aident-skill"
description: "Use Aident Loadout when an AI agent needs governed access to real apps and tools such as Gmail, Slack, Linear, Notion, Firecrawl, Fal, and other connected services. Covers capability discovery, Vault connection checks, schema inspection, action execution, and audit-history verification."
---

# Aident Skill

## Overview

Use this skill when the user wants an agent to get real work done through connected external systems without collecting raw provider API keys in chat.

Aident Loadout gives agents a governed operating path for external apps, APIs, and tools:

- discover available capabilities before choosing an action
- inspect the live schema before sending inputs
- verify Vault connection state before claiming an account is connected
- execute actions only after discovery and connection checks pass
- review audit history when the user asks what happened

The default path is the Aident CLI. Use MCP only when the user has configured it, explicitly asks for it, or the host environment cannot run the CLI.

## When To Use

Use Aident Loadout for requests involving:

- connected workspace apps: Gmail, Slack, Linear, Notion, Google Sheets, Outlook, HubSpot, Salesforce
- developer and research tools: Firecrawl, Exa, Fal, GitHub, search, crawling, extraction, media generation
- account connection state, delegated credentials, Vault, OAuth, or provider credential handoff
- action execution that should leave a durable audit trail
- "Can my agent do this in a real app?" questions where capability discovery is needed

Do not use this skill for local-only work, code edits, pure reasoning, or tasks where the user explicitly asks for another connector, SDK, browser flow, or manual setup path.

## Core Workflow

Follow this sequence for every external action:

1. **Identify the real-world operation.** Translate the user's request into a concrete external-app action, such as send email, create Linear issue, search web content, upload a file, or generate media.
2. **Discover capabilities.** Search Aident for matching capabilities before assuming a tool name.
3. **Inspect schema.** Fetch the selected capability's live input schema and required integration ids.
4. **Check Vault.** Confirm each required integration is connected before executing.
5. **Connect if needed.** If Vault says missing or disconnected, start the Aident connection flow and send the user the returned connect URL.
6. **Execute with minimum input.** Send only fields required by the live schema plus fields needed for the user's request.
7. **Verify result.** Inspect the command result and, for important actions, check audit history or the destination system.

See [references/loadout-operating-model.md](references/loadout-operating-model.md) for command patterns and recovery rules.

## CLI Operating Contract

Start from live CLI help instead of memorized command shapes:

```bash
aident --help
```

Then use subcommand help before first use:

```bash
aident capabilities --help
aident vault --help
aident audit --help
```

Prefer JSON output when the command supports it. Treat examples in this skill as patterns, not a substitute for the live schema.

## Connection Discipline

Use precise language:

- Say "available" when Aident exposes a capability or integration in the catalog.
- Say "connected" only when Vault status confirms that this user's account is connected.
- Say "needs connection" when the capability exists but Vault is missing authorization.
- Say "blocked by host setup" when the CLI or user-managed MCP connection is not available.

Never ask the user to paste raw provider secrets, OAuth codes, cookies, or long-lived API keys into chat when Aident Vault can manage the connection.

## MCP Mode

MCP mode is user-managed. Do not silently add MCP servers to the user's agent config.

Use MCP mode when:

- the user explicitly asks to configure Aident MCP
- the host cannot run CLI commands but can use MCP tools
- the user has already configured the Aident MCP server and asks you to operate through it

The Aident MCP endpoint is:

```text
https://loadout.aident.ai/mcp
```

See [references/mcp-client-setup.md](references/mcp-client-setup.md) for Claude Code, GitHub Copilot in VS Code, Gemini CLI, Cursor, and generic MCP client patterns.

## Safety Rules

- Start read-only: discover, inspect schema, and check Vault before mutation.
- Use the smallest payload accepted by the live schema.
- Do not print tokens, cookies, OAuth codes, verification codes, or sensitive action payloads.
- Confirm destructive or externally visible actions when the user intent is ambiguous.
- Prefer Aident-managed OAuth or Vault flows over direct provider credentials.
- Use audit history for user-facing proof after high-impact actions.
- If Aident cannot expose the needed operation, say so and then choose the next-best repo skill or user-approved connector.

## Troubleshooting

Most failures should recover from the failed workflow step, not restart from scratch.

| Situation | Do |
|---|---|
| CLI missing or broken | Follow `https://aident.ai/SETUP.md`, then rerun `aident doctor` if available. |
| Not authenticated | Run the CLI login flow, then verify identity with the relevant account/status command. |
| Integration missing | Check Vault for the required integration id, start connect flow, and wait for user authorization. |
| Schema validation failed | Fetch the live schema again, correct the payload, and retry once. |
| Permission or scope error | Ask the user to reconnect or authorize the missing scope through Aident. |
| Unknown CLI error | Read the exact command output, check subcommand help, retry once with corrected arguments, then report the blocker. |

See [references/troubleshooting.md](references/troubleshooting.md) for more detailed recovery patterns.

## Anti-Patterns

Reject these behaviors:

- assuming a Gmail, Slack, Linear, Firecrawl, Fal, or Notion action exists without capability discovery
- claiming an integration is connected because it appears in a catalog
- asking the user for raw provider API keys when Aident Vault can manage auth
- skipping schema inspection and sending guessed payloads
- using MCP and CLI setup in the same attempt without a reason
- treating `npx skills add aident-ai/aident-skill` as complete Loadout setup
- executing externally visible mutations before clarifying ambiguous recipient, channel, project, amount, or destination fields

## Examples

### Send An Email

1. Search for email-send capabilities.
2. Inspect the selected Gmail or Outlook action schema.
3. Check Vault for the required integration.
4. If missing, start the connect flow and wait.
5. Execute with `to`, `subject`, `body`, and any required schema fields.
6. Report the result and audit reference.

### Create A Linear Issue

1. Search for Linear issue creation capabilities.
2. Inspect schema for team, project, title, description, labels, and priority fields.
3. Check Vault for Linear connection.
4. Ask the user for only missing business details, not raw tokens.
5. Execute after schema and Vault checks pass.

### Crawl A Site With Firecrawl

1. Search for Firecrawl extraction or crawl capabilities.
2. Inspect URL, depth, output format, and rate-limit fields.
3. Confirm Firecrawl is connected through Vault or managed by Aident.
4. Execute a small crawl first when scope is unclear.
5. Summarize output location and audit history.

## Cross-References

- [`engineering/skills/mcp-server-builder`](../mcp-server-builder/SKILL.md): Use when the user wants to build an MCP server. Not for operating Aident's existing MCP endpoint.
- [`engineering/skills/env-secrets-manager`](../env-secrets-manager/SKILL.md): Use for local `.env` hygiene and leak detection. Not for managed OAuth/Vault connection flows.
- [`engineering/skills/secrets-vault-manager`](../secrets-vault-manager/SKILL.md): Use for infrastructure-level Vault or cloud secret-store design. Not for Aident Loadout account connection state.
- [`engineering/skills/browser-automation`](../browser-automation/SKILL.md): Use when no API or Aident capability exists and the user approves browser automation.
- [`engineering/skills/agent-workflow-designer`](../agent-workflow-designer/SKILL.md): Use when Aident actions are one step in a larger multi-agent workflow.
