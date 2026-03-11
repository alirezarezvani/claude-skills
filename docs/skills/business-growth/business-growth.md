---
title: "Business & Growth Skills"
description: "Business & Growth Skills - Claude Code skill from the Business & Growth domain."
---

# Business & Growth Skills

<div class="page-meta" markdown>
<span class="meta-badge">:material-trending-up: Business & Growth</span>
<span class="meta-badge">:material-identifier: `business-growth`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/business-growth/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install business-growth-skills</code>
</div>


4 production-ready skills for customer success, sales, and revenue operations.

## Quick Start

### Claude Code
```
/read business-growth/customer-success-manager/SKILL.md
```

### Codex CLI
```bash
npx agent-skills-cli add alirezarezvani/claude-skills/business-growth
```

## Skills Overview

| Skill | Folder | Focus |
|-------|--------|-------|
| Customer Success Manager | `customer-success-manager/` | Health scoring, churn prediction, expansion |
| Sales Engineer | `sales-engineer/` | RFP analysis, competitive matrices, PoC planning |
| Revenue Operations | `revenue-operations/` | Pipeline analysis, forecast accuracy, GTM metrics |
| Contract & Proposal Writer | `contract-and-proposal-writer/` | Proposal generation, contract templates |

## Python Tools

9 scripts, all stdlib-only:

```bash
python3 customer-success-manager/scripts/health_score_calculator.py --help
python3 revenue-operations/scripts/pipeline_analyzer.py --help
```

## Rules

- Load only the specific skill SKILL.md you need
- Use Python tools for scoring and metrics, not manual estimates
