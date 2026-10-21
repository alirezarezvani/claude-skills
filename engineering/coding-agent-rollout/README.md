# coding-agent-rollout

> One engineer's Claude Code setup is a preference. A team's is a policy.

Settings merge from five scopes, `permissions.allow` arrays combine across
files, and deny beats ask beats allow wherever it is written. Nobody can read
the effective policy from one file, so nobody notices when a permissive user
file undoes a careful shared one, or when an unpinned MCP server changes
overnight. This plugin makes the policy readable and then checks it.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install coding-agent-rollout
```

## Use

```bash
/cs-claude-rollout .                         # full audit of this repo
/cs-claude-settings-lint . /etc/claude-code/managed-settings.json
```

Or run the scripts directly. Each has `--help`, `--sample` and `--output json`:

| Script | Phase | What it checks | Exit codes |
|---|---|---|---|
| `settings_linter.py` | Guardrails | Blanket and destructive allows, dead rules, secrets in `env`, committed local settings, MCP auto-approval, network hooks, managed bypass switch | 0 · 2 · 3 · **4** |
| `mcp_plugin_inventory.py` | Inventory | Every MCP server, plugin and marketplace; allowlist, pinning, plain-http remotes, committed secrets | 0 · 2 · 3 · **4** |
| `claude_md_layering_audit.py` | Instructions | Resident vs on-demand layers, @imports (4-hop limit), duplicates, contradictions, secrets, size | 0 · 2 · 3 · **4** |
| `adoption_tracker.py` | Adoption | Counts-only member summaries from local transcripts; team stage PILOT / SPREADING / EMBEDDED / STALLED | 0 · **2 stalled** · 3 |

## Design decisions

- **Verified, not remembered.** Every settings key, scope, path and limit was checked against the official
  Claude Code docs. Settings ship fast, so unknown keys are INFO, not errors.
- **Read-only.** No script edits a settings file. They report; you decide.
- **Privacy first for adoption.** The tracker never emits prompt text, file content, or tool inputs other
  than a skill name. Teams share the JSON summary, never transcripts.
- **Baseline policy included.** `assets/managed-settings.example.json` lints clean and is a sane day-one policy.

## Distinct from

- `claude-coach` — coaches one person.
- `skill-doctor` — improves installed skills from session evidence.
- `security-guidance` — a hook that warns on risky code as it is written.

## License

MIT
