# Finance Skills — Codex CLI Instructions

When working on financial analysis tasks, use the finance skill system:

## Python Tools

All scripts in `finance/financial-analyst/scripts/` are stdlib-only and CLI-first:

```bash
python3 finance/financial-analyst/scripts/ratio_calculator.py --help
python3 finance/financial-analyst/scripts/dcf_valuation.py --help
python3 finance/financial-analyst/scripts/budget_variance_analyzer.py --help
python3 finance/financial-analyst/scripts/forecast_builder.py --help
```

## Key Skills by Task

| Task | Skill |
|------|-------|
| Financial ratios | financial-analyst |
| DCF valuation | financial-analyst |
| Budget variance | financial-analyst |
| Forecasting | financial-analyst |

## Rules

- Always validate financial outputs against source data
- Use Python tools for calculations, not manual estimates
