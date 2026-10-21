---
title: "Claude Code Team Rollout — Agent Skill for Codex & OpenClaw"
description: "Use when rolling Claude Code out to a team or organization, or auditing a rollout already under way — writing or reviewing shared and managed."
---

# Claude Code Team Rollout

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `coding-agent-rollout`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/coding-agent-rollout/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


> **Portability:** 4 stdlib scripts, no network, no LLM calls. They read config and counts; they change nothing.

One engineer's Claude Code setup is a preference. A team's is a policy. Settings
merge from five scopes, `permissions.allow` arrays combine across files, and
deny beats ask beats allow wherever it is written, so nobody can read the
effective policy from a single file. This skill makes it readable, then checks it.

## Workflow

```bash
# 1 - Guardrails: lint shared, local and managed settings together.
python scripts/settings_linter.py --repo . --managed /etc/claude-code/managed-settings.json
# 2 - Inventory: every MCP server, plugin and marketplace, against your approved list.
python scripts/mcp_plugin_inventory.py --repo . --allowlist approved.json
# 3 - Instructions: what CLAUDE.md actually loads, layer by layer.
python scripts/claude_md_layering_audit.py --repo .
# 4 - Adoption: each member runs this locally and shares only the JSON counts.
python scripts/adoption_tracker.py --member alice --output json > alice.json
python scripts/adoption_tracker.py --merge *.json --seats 12 --weeks-since-launch 6
```

Start from [`assets/managed-settings.example.json`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/coding-agent-rollout/assets/managed-settings.example.json):
bypass mode disabled, secrets denied, risky commands on `ask`, managed hooks
only, an MCP and marketplace allowlist. Ship it through MDM before the first
seat; policy added after habits form becomes a negotiation.

## What blocks (exit 4)

- Blanket shell allows (`Bash`, `Bash(*)`) and pre-approved destructive commands
  (force push, `rm -rf`, `sudo`, pipe-to-shell, publish, infra apply).
- A literal credential in a shared settings `env` block, a committed `.mcp.json`, or a committed CLAUDE.md.
- `.claude/settings.local.json` committed to git.
- An MCP server, plugin or marketplace missing from the approved list.

Warnings cover dead rules (an allow that a deny shadows, `mcp__*` in allow),
`enableAllProjectMcpServers`, unpinned `npx` servers, plain-http remotes,
network-calling hooks, broken or too-deep `@imports`, duplicated or
contradictory instructions, and resident CLAUDE.md size.

## Hard rules

1. **Policy lives in managed settings.** Project files cannot enable bypass mode
   or telemetry, and a team guardrail in a file anyone can edit is a suggestion.
2. **Approve MCP servers by name, URL or command, never by `enableAllProjectMcpServers`.**
3. **Pin what runs.** Unpinned `npx`/`uvx` servers and unpinned marketplaces change under you.
4. **Never collect transcripts.** Share the adoption JSON (counts only); transcripts are plaintext and can hold secrets.
5. **Report findings, not verdicts on people.** Adoption is a team metric; inactive seats are a rollout question, not a performance one.
6. **Settings keys change fast.** An unknown key is INFO; check the settings reference before calling it a typo.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/settings_linter.py` | S1-S12 across shared, local, user and managed scopes | 0 · 2 warn · 3 bad input · 4 blocker |
| `scripts/mcp_plugin_inventory.py` | One table of servers, plugins, marketplaces; M1-M6 | 0 · 2 · 3 · 4 |
| `scripts/claude_md_layering_audit.py` | Resident vs on-demand layers, imports (4 hops), L1-L11 | 0 · 2 · 3 · 4 |
| `scripts/adoption_tracker.py` | Member counts; team stage PILOT / SPREADING / EMBEDDED / STALLED | 0 · 2 stalled · 3 |

All support `--sample` and `--output json`.

## References and assets

- [`references/settings_and_permissions.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/coding-agent-rollout/references/settings_and_permissions.md) — scopes, precedence, rule syntax, managed-only keys (7 sources)
- [`references/mcp_and_plugin_governance.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/coding-agent-rollout/references/mcp_and_plugin_governance.md) — MCP scopes, allowlists, marketplaces, pinning (6 sources)
- [`references/memory_and_adoption.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/coding-agent-rollout/references/memory_and_adoption.md) — CLAUDE.md layering, transcripts, OpenTelemetry, adoption stages (6 sources)
- [`assets/managed-settings.example.json`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/coding-agent-rollout/assets/managed-settings.example.json) — baseline team policy
- [`assets/approved-components.example.json`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/coding-agent-rollout/assets/approved-components.example.json) — allowlist format for step 2
- [`assets/rollout_plan.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/coding-agent-rollout/assets/rollout_plan.md) — four-phase plan with exit criteria per phase
