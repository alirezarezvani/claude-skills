---
name: "finance-skills"
description: "Router/index for the finance skills bundled in this plugin: financial-analyst (ratio analysis, DCF valuation, budget variance, rolling forecasts), saas-metrics-coach (ARR/MRR, churn, CAC/LTV, NRR, quick ratio) and month-end-close (close calendar, reconciliations, flux review). Use when a finance request doesn't obviously match one skill and you need to pick the right one (e.g., 'analyze these financials', 'how healthy are my SaaS metrics')."
license: MIT
metadata:
  version: 2.9.0
  author: Alireza Rezvani
  tags:
    - finance
    - financial-analysis
    - dcf
    - valuation
    - budgeting
  agents:
    - claude-code
    - codex-cli
    - openclaw
---

# Finance Skills — Router

This plugin bundles the finance skills below plus this router. Each skill is self-contained.

## Routing table

| Request signals | Skill | Path |
|---|---|---|
| Ratio analysis, DCF valuation, budget variance, driver-based forecasts | financial-analyst | `skills/financial-analyst/` |
| ARR/MRR, churn, CAC/LTV, NRR, quick ratio, SaaS benchmarks | saas-metrics-coach | `skills/saas-metrics-coach/` |
| Month-end close, close calendar, bank or sub-ledger reconciliation, flux / variance explanations | month-end-close | `skills/month-end-close/` |

If both match (e.g., "value my SaaS company"), ask whether the user wants statement-level analysis (financial-analyst) or SaaS operating metrics (saas-metrics-coach).

## Quick start

```bash
# Example: route a statement-analysis request
cat finance/skills/financial-analyst/SKILL.md
python3 finance/skills/financial-analyst/scripts/ratio_calculator.py --help

# Or a SaaS metrics request
python3 finance/skills/saas-metrics-coach/scripts/metrics_calculator.py --help
```

## Related (packaged separately, not in this bundle)

- `finance/business-investment-advisor/` — investment thesis evaluation, ROI modeling (prompt-only skill, separate nested plugin)
- Root commands `/financial-health` and `/saas-health` wrap these skills' scripts.

## Rules

- Route to exactly one skill, then follow that skill's workflow. This router ships no tools of its own.
- Always validate financial outputs against the user's source data; outputs are analysis support, not investment advice.
