---
title: "/saas-health"
description: "/saas-health — Claude Code slash command."
---

# /saas-health

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/saas-health.md">Source</a></span>
</div>


Calculate SaaS financial health metrics from raw business numbers, benchmark against industry standards, and project forward.

## Usage

```
/saas-health metrics --mrr <amount> [--customers <n>] [--churned <n>] [--json]
/saas-health quick-ratio --new-mrr <amount> --churned <amount> [--expansion <amount>]
/saas-health simulate --mrr <amount> --growth <pct> --churn <pct> --cac <amount> [--json]
```

## Examples

```
/saas-health metrics --mrr 80000 --customers 200 --churned 3 --new-customers 15 --sm-spend 25000
/saas-health quick-ratio --new-mrr 10000 --expansion 2000 --churned 3000 --contraction 500
/saas-health simulate --mrr 50000 --growth 10 --churn 3 --cac 2000
```

## Scripts
- `finance/saas-metrics-coach/scripts/metrics_calculator.py` — Core SaaS metrics (ARR, MRR, churn, CAC, LTV, NRR, payback)
- `finance/saas-metrics-coach/scripts/quick_ratio_calculator.py` — Growth efficiency ratio
- `finance/saas-metrics-coach/scripts/unit_economics_simulator.py` — 12-month forward projection

## Skill Reference
→ `finance/saas-metrics-coach/SKILL.md`

## Related Commands
- `/financial-health` — Traditional financial analysis (ratios, DCF, budgets)
