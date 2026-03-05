# Self-Improving Agent

> Auto-memory captures. This plugin curates.

A Claude Code plugin that turns auto-memory into a structured self-improvement loop. Analyze what Claude has learned, promote proven patterns to enforced rules, and extract recurring solutions into reusable skills.

## Why

Claude Code's auto-memory (v2.1.32+) automatically records project patterns in `MEMORY.md`. But it has no judgment about what to keep, what to promote, or when entries go stale. This plugin adds the intelligence layer.

**The difference:**
- **MEMORY.md**: "I noticed this project uses pnpm" (background note, truncated at 200 lines)
- **CLAUDE.md**: "Use pnpm, not npm" (enforced instruction, loaded in full)

Promoting a pattern from memory to rules fundamentally changes how Claude treats it.

## Commands

| Command | What it does |
|---------|-------------|
| `/si:review` | Analyze auto-memory — find promotion candidates, stale entries, health metrics |
| `/si:promote` | Graduate a pattern from MEMORY.md → CLAUDE.md or `.claude/rules/` |
| `/si:extract` | Turn a recurring pattern into a standalone reusable skill |
| `/si:status` | Memory health dashboard — line counts, capacity, recommendations |
| `/si:remember` | Explicitly save important knowledge to auto-memory |

## Install

### Claude Code
```
/plugin marketplace add alirezarezvani/claude-skills
/plugin install self-improving-agent@claude-code-skills
```

### OpenClaw
```bash
clawhub install self-improving-agent
```

### Codex CLI
```bash
./scripts/codex-install.sh --skill self-improving-agent
```

## How It Works

```
Claude discovers pattern → auto-memory (MEMORY.md)
         ↓
Pattern recurs 2-3x → /si:review flags it
         ↓
You approve → /si:promote graduates it to CLAUDE.md
         ↓
Pattern becomes enforced rule, memory entry removed
         ↓
Space freed for new learnings
```

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| Skills | 5 | review, promote, extract, status, remember |
| Agents | 2 | memory-analyst, skill-extractor |
| Hooks | 1 | PostToolUse error capture (zero overhead on success) |
| Reference docs | 3 | memory architecture, promotion rules, rules directory patterns |
| Templates | 2 | rule template, skill template |

## Design Principles

1. **Don't fight auto-memory — orchestrate it.** Auto-memory captures. This plugin curates.
2. **No duplicate storage.** Reads from `~/.claude/projects/` directly. No `.learnings/` directory.
3. **Zero capture overhead.** Auto-memory handles capture. Hook only fires on errors.
4. **Promotion = graduation.** Moving a pattern from MEMORY.md to CLAUDE.md changes its priority.
5. **Respect the 200-line limit.** Actively manages MEMORY.md capacity.

## Platform Support

| Platform | Memory System | Support |
|----------|--------------|---------|
| Claude Code | Auto-memory (MEMORY.md) | ✅ Full |
| OpenClaw | workspace/MEMORY.md | ✅ Adapted |
| Codex CLI | AGENTS.md | ✅ Adapted |
| GitHub Copilot | copilot-instructions.md | ⚠️ Manual |

## Credits

Inspired by [pskoett/self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent) — a structured learning loop for AI coding agents. This plugin builds on that concept by integrating natively with Claude Code's auto-memory system.

## License

MIT — see [LICENSE](LICENSE)
