---
title: Getting Started with Claude Code Skills
description: "How to install and use Claude Code skills and plugins for Claude Code, OpenAI Codex, and OpenClaw."
---

# Getting Started

## Installation

### Claude Code (Recommended)

```bash
# Step 1: Add the marketplace
/plugin marketplace add alirezarezvani/claude-skills

# Step 2: Install the skills you need
/plugin install engineering-skills@claude-code-skills
```

### OpenAI Codex

```bash
npx agent-skills-cli add alirezarezvani/claude-skills --agent codex
# Or: git clone + ./scripts/codex-install.sh
```

### OpenClaw

```bash
bash <(curl -s https://raw.githubusercontent.com/alirezarezvani/claude-skills/main/scripts/openclaw-install.sh)
```

### Manual Installation

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
# Copy any skill folder to ~/.claude/skills/ (Claude Code) or ~/.codex/skills/ (Codex)
```

---

## Available Skill Bundles

| Bundle | Command | Skills |
|--------|---------|--------|
| Engineering Core | `/plugin install engineering-skills@claude-code-skills` | 23 |
| Engineering POWERFUL | `/plugin install engineering-advanced-skills@claude-code-skills` | 25 |
| Product | `/plugin install product-skills@claude-code-skills` | 8 |
| Marketing | `/plugin install marketing-skills@claude-code-skills` | 42 |
| Regulatory & Quality | `/plugin install ra-qm-skills@claude-code-skills` | 12 |
| Project Management | `/plugin install pm-skills@claude-code-skills` | 6 |
| C-Level Advisory | `/plugin install c-level-skills@claude-code-skills` | 28 |
| Business & Growth | `/plugin install business-growth-skills@claude-code-skills` | 4 |
| Finance | `/plugin install finance-skills@claude-code-skills` | 1 |

---

## Using Skills

Once installed, skills are available as slash commands or contextual expertise:

### Slash Command Example
```
/pw:generate   # Generate Playwright tests
/si:review     # Review auto-memory health
/cs:board      # Trigger a C-suite board meeting
```

### Contextual Example
```
Using the senior-architect skill, review our microservices architecture
and identify the top 3 scalability risks.
```

---

## Python Tools

All 160+ Python tools use the standard library only (zero pip installs). Run them directly:

```bash
# Security audit
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/

# Brand voice analysis
python3 marketing-skill/content-creator/scripts/brand_voice_analyzer.py article.txt

# RICE prioritization
python3 product-team/product-manager-toolkit/scripts/rice_prioritizer.py features.csv

# Tech debt scoring
python3 c-level-advisor/cto-advisor/scripts/tech_debt_analyzer.py /path/to/codebase
```

---

## Security

Before installing third-party skills, audit them:

```bash
python3 engineering/skill-security-auditor/scripts/skill_security_auditor.py /path/to/skill/
```

Returns **PASS / WARN / FAIL** with remediation guidance. Scans for command injection, data exfiltration, prompt injection, and more.

---

## Creating Your Own Skills

Each skill is a folder with:

- `SKILL.md` — frontmatter + instructions + workflows
- `scripts/` — Python CLI tools (optional)
- `references/` — domain knowledge (optional)
- `assets/` — templates (optional)

See the [Skills & Agents Factory](https://github.com/alirezarezvani/claude-code-skills-agents-factory) for a step-by-step guide.

---

## FAQ

**Do I need API keys?**
No. Skills work locally with no external API calls. Python tools use stdlib only.

**Can I install individual skills?**
Yes. Use `/plugin install skill-name@claude-code-skills` for any single skill.

**Do skills conflict with each other?**
No. Each skill is self-contained with no cross-dependencies.
