# Persona-Based Agents

Pre-configured agent personas with curated skill loadouts, workflows, and communication styles.

## What's a Persona?

A **persona** is an agent definition that goes beyond "use these skills." It includes:

- **Identity** — who this agent is, how they think, what they prioritize
- **Skills** — pre-loaded skill set for their domain
- **Workflows** — step-by-step processes for common tasks
- **Communication** — how they talk, what they emphasize, what they avoid
- **Handoffs** — when they escalate and to whom

## How to Use

### Claude Code
```bash
cp agents/personas/startup-cto.md ~/.claude/agents/
# Then: "Activate startup-cto mode"
```

### Cursor
```bash
./scripts/convert.sh --tool cursor
# Personas convert to .cursor/rules/*.mdc
```

### Any Tool
```bash
./scripts/install.sh --tool <your-tool>
```

## Available Personas

| Persona | Domain | Best For |
|---------|--------|----------|
| [startup-cto](startup-cto.md) | Engineering + Strategy | Technical co-founders, first CTOs, architecture decisions |
| [growth-marketer](growth-marketer.md) | Marketing + Growth | Bootstrapped founders, indie hackers, content-led growth |
| [solo-founder](solo-founder.md) | Full Stack | One-person startups, side projects, MVP building |

## Personas vs Agents

| | Agents (`agents/`) | Personas (`agents/personas/`) |
|---|---|---|
| **Focus** | Task execution | Role embodiment |
| **Skills** | Domain-specific | Cross-domain curated set |
| **Voice** | Neutral/professional | Personality-driven |
| **Workflows** | Single-domain | Multi-step, cross-skill |
| **Use case** | "Do this task" | "Think like this person" |

Both coexist. Use agents for focused tasks, personas for ongoing collaboration.

## Creating Your Own

See the [persona template](TEMPLATE.md) for the format specification.
