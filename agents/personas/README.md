# Persona-Based Agents

Pre-configured agent personas with curated skill loadouts, workflows, and distinct personalities.

## What's a Persona?

A **persona** is an agent definition that goes beyond "use these skills." Each persona includes:

- **🧠 Identity & Memory** — who this agent is, how they think, what they've learned
- **🎯 Core Mission** — what they optimize for, in priority order
- **🚨 Critical Rules** — hard constraints they never violate
- **📋 Capabilities** — domain expertise organized by area
- **🔄 Workflows** — step-by-step processes for common tasks
- **💭 Communication Style** — how they talk, with concrete examples
- **🎯 Success Metrics** — measurable outcomes that define "good"
- **🚀 Advanced Capabilities** — deeper expertise loaded on demand
- **🔄 Learning & Memory** — what they retain and patterns they recognize

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

### Any Supported Tool
```bash
./scripts/install.sh --tool <your-tool>
```

## Available Personas

| Persona | Emoji | Domain | Best For |
|---------|-------|--------|----------|
| [Startup CTO](startup-cto.md) | 🏗️ | Engineering + Strategy | Technical co-founders, architecture decisions, team building |
| [Growth Marketer](growth-marketer.md) | 🚀 | Marketing + Growth | Bootstrapped founders, content-led growth, launches |
| [Solo Founder](solo-founder.md) | 🦄 | Cross-domain | One-person startups, side projects, MVP building |

## Personas vs Task Agents

| | Task Agents (`agents/`) | Personas (`agents/personas/`) |
|---|---|---|
| **Focus** | Task execution | Role embodiment |
| **Scope** | Single domain | Cross-domain curated set |
| **Voice** | Neutral/professional | Personality-driven with backstory |
| **Workflows** | Single-step | Multi-step with decision points |
| **Use case** | "Do this task" | "Think like this person" |

Both coexist. Use task agents for focused work, personas for ongoing collaboration.

## Creating Your Own

See [TEMPLATE.md](template.md) for the format specification. Key elements:

```yaml
---
name: Agent Name
description: What this agent does and when to activate it.
color: blue          # Agent color theme
emoji: 🎯           # Single emoji identifier
vibe: One sentence personality capture.
tools: Read, Write, Bash, Grep, Glob
---
```

Follow the section structure (Identity → Mission → Rules → Capabilities → Workflows → Communication → Metrics → Advanced → Learning) for consistency with existing personas.
