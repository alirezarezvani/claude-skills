---
title: "Finance Skills"
description: "Finance Skills - Claude Code skill from the Finance domain."
---

# Finance Skills

<div class="page-meta" markdown>
<span class="meta-badge">:material-calculator-variant: Finance</span>
<span class="meta-badge">:material-identifier: `finance`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/finance/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install finance-skills</code>
</div>


Production-ready financial analysis skill for strategic decision-making.

## Quick Start

### Claude Code
```
/read finance/financial-analyst/SKILL.md
```

### Codex CLI
```bash
npx agent-skills-cli add alirezarezvani/claude-skills/finance
```

## Skills Overview

| Skill | Folder | Focus |
|-------|--------|-------|
| Financial Analyst | `financial-analyst/` | Ratio analysis, DCF, budget variance, forecasting |

## Python Tools

4 scripts, all stdlib-only:

```bash
python3 financial-analyst/scripts/ratio_calculator.py --help
python3 financial-analyst/scripts/dcf_valuation.py --help
python3 financial-analyst/scripts/budget_variance_analyzer.py --help
python3 financial-analyst/scripts/forecast_builder.py --help
```

## Rules

- Load only the specific skill SKILL.md you need
- Always validate financial outputs against source data
