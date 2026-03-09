---
name: "business-growth-skills"
description: "4 production-ready business and growth skills: customer success manager with health scoring and churn prediction, sales engineer with RFP analysis, revenue operations with pipeline and GTM metrics, and contract & proposal writer. Python tools included (all stdlib-only). Works with Claude Code, Codex CLI, and OpenClaw."
version: 1.1.0
author: Alireza Rezvani
license: MIT
tags:
  - business
  - customer-success
  - sales
  - revenue-operations
  - growth
agents:
  - claude-code
  - codex-cli
  - openclaw
---

# Business & Growth Skills

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
