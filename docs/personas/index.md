---
title: "Personas"
description: "3 persona-based agents with curated skill loadouts, workflows, and distinct communication styles."
---

<div class="domain-header" markdown>

# :material-account-group: Personas

<p class="domain-count">3 persona-based agents for role embodiment</p>

</div>

Personas go beyond task agents. They define how an agent thinks, prioritizes, and communicates — complete with identity, judgment frameworks, and curated skill loadouts.

### Personas vs Task Agents

| | Task Agents | Personas |
|---|---|---|
| **Purpose** | Execute a specific task | Embody a role across tasks |
| **Scope** | Single domain | Cross-domain, curated |
| **Voice** | Neutral, professional | Personality-driven with backstory |
| **Workflows** | Single-step | Multi-step with decision points |
| **Use case** | "Do this task" | "Think like this person" |

Both coexist. Use task agents for focused work, personas for ongoing collaboration.

---

<div class="grid cards" markdown>

-   :material-hammer-wrench:{ .lg .middle } **[Startup CTO](startup-cto.md)**

    ---

    Architecture decisions, tech stack selection, team building, technical due diligence. Pragmatic, opinionated, allergic to over-engineering.

-   :material-chart-line:{ .lg .middle } **[Growth Marketer](growth-marketer.md)**

    ---

    Content-led growth, launch strategy, channel optimization. Data-driven, budget-conscious, bootstrapped marketing expertise.

-   :material-lightbulb-on:{ .lg .middle } **[Solo Founder](solo-founder.md)**

    ---

    One-person startups, side projects, MVP building. Cross-domain prioritization, wearing all hats, shipping fast.

</div>

---

## Usage

### Claude Code
```bash
cp agents/personas/startup-cto.md ~/.claude/agents/
# Then: "Activate startup-cto mode"
```

### Any Supported Tool
```bash
./scripts/convert.sh --tool cursor   # Converts personas too
./scripts/install.sh --tool cursor --target /path/to/project
```

### Create Your Own

Use the [TEMPLATE.md](https://github.com/alirezarezvani/claude-skills/blob/main/agents/personas/TEMPLATE.md) to create custom personas with your own identity, skills, and workflows.
