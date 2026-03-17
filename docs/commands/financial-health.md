---
title: "/financial-health — Slash Command for AI Coding Agents"
description: "Run financial ratio analysis, DCF valuation, budget variance analysis, and rolling forecasts. Usage: /financial-health <ratios|dcf|budget|forecast>. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /financial-health

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/financial-health.md">Source</a></span>
</div>


Analyze financial statements, build valuation models, assess budget variances, and construct forecasts.

## Usage

```
/financial-health ratios <financial_data.json> [--format json|text]
/financial-health dcf <valuation_data.json> [--format json|text]
/financial-health budget <budget_data.json> [--format json|text]
/financial-health forecast <forecast_data.json> [--format json|text]
```

## Examples

```
/financial-health ratios quarterly_financials.json --format json
/financial-health dcf acme_valuation.json
/financial-health budget q1_budget.json --format json
/financial-health forecast revenue_history.json
```

## Scripts
- `finance/financial-analyst/scripts/ratio_calculator.py` — Profitability, liquidity, leverage, efficiency, valuation ratios
- `finance/financial-analyst/scripts/dcf_valuation.py` — DCF enterprise and equity valuation with sensitivity analysis
- `finance/financial-analyst/scripts/budget_variance_analyzer.py` — Actual vs budget vs prior year variance analysis
- `finance/financial-analyst/scripts/forecast_builder.py` — Driver-based revenue forecasting with scenario modeling

## Skill Reference
→ `finance/financial-analyst/SKILL.md`

## Related Commands
- `/saas-health` — SaaS-specific metrics (ARR, MRR, churn, CAC, LTV, Quick Ratio)
