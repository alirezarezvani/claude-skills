---
name: "finance-skills"
description: "Pick the right finance skill: ratios, DCF, forecasts (financial-analyst), ARR, churn, CAC, LTV (saas-metrics-coach), month-end-close. Use whenever a finance ask is vague."
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
