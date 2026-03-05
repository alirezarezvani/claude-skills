---
name: cfo-advisor
description: "Financial leadership for startups and scaling companies. Financial modeling, unit economics, fundraising strategy, cash management, and board financial packages. Use when building financial models, analyzing unit economics, planning fundraising, managing cash runway, preparing board materials, or when user mentions CFO, burn rate, runway, fundraising, unit economics, LTV, CAC, term sheets, or financial strategy."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: c-level
  domain: cfo-leadership
  updated: 2026-03-05
  python-tools: burn_rate_calculator.py, unit_economics_analyzer.py, fundraising_model.py
  frameworks: financial-planning, fundraising-playbook, cash-management
---

# CFO Advisor

Strategic financial frameworks for startup CFOs and finance leaders. Numbers-driven, decisions-focused.

This is **not** a financial analyst skill. This is strategic: models that drive decisions, fundraises that don't kill the company, board packages that earn trust.

## Keywords
CFO, chief financial officer, burn rate, runway, unit economics, LTV, CAC, fundraising, Series A, Series B, term sheet, cap table, dilution, financial model, cash flow, board financials, FP&A, SaaS metrics, ARR, MRR, net dollar retention, gross margin, scenario planning, cash management, treasury, working capital, burn multiple, rule of 40

## Quick Start

```bash
# Burn rate & runway scenarios (base/bull/bear)
python scripts/burn_rate_calculator.py

# Per-cohort LTV, per-channel CAC, payback periods
python scripts/unit_economics_analyzer.py

# Dilution modeling, cap table projections, round scenarios
python scripts/fundraising_model.py
```

## Key Questions (ask these first)

- **What's your burn multiple?** (Net burn ÷ Net new ARR. > 2x is a problem.)
- **If fundraising takes 6 months instead of 3, do you survive?** (If not, you're already behind.)
- **Show me unit economics per cohort, not blended.** (Blended hides deterioration.)
- **What's your NDR?** (> 100% means you grow without signing a single new customer.)
- **What are your decision triggers?** (At what runway do you start cutting? Define now, not in a crisis.)

## Core Responsibilities

| Area | What It Covers | Reference |
|------|---------------|-----------|
| **Financial Modeling** | Bottoms-up P&L, three-statement model, headcount cost model | `references/financial_planning.md` |
| **Unit Economics** | LTV by cohort, CAC by channel, payback periods | `references/financial_planning.md` |
| **Burn & Runway** | Gross/net burn, burn multiple, scenario planning, decision triggers | `references/cash_management.md` |
| **Fundraising** | Timing, valuation, dilution, term sheets, data room | `references/fundraising_playbook.md` |
| **Board Financials** | What boards want, board pack structure, BvA | `references/financial_planning.md` |
| **Cash Management** | Treasury, AR/AP optimization, runway extension tactics | `references/cash_management.md` |
| **Budget Process** | Driver-based budgeting, allocation frameworks | `references/financial_planning.md` |

## CFO Metrics Dashboard

| Category | Metric | Target | Frequency |
|----------|--------|--------|-----------|
| **Efficiency** | Burn Multiple | < 1.5x | Monthly |
| **Efficiency** | Rule of 40 | > 40 | Quarterly |
| **Efficiency** | Revenue per FTE | Track trend | Quarterly |
| **Revenue** | ARR growth (YoY) | > 2x at Series A/B | Monthly |
| **Revenue** | Net Dollar Retention | > 110% | Monthly |
| **Revenue** | Gross Margin | > 65% | Monthly |
| **Economics** | LTV:CAC | > 3x | Monthly |
| **Economics** | CAC Payback | < 18 mo | Monthly |
| **Cash** | Runway | > 12 mo | Monthly |
| **Cash** | AR > 60 days | < 5% of AR | Monthly |

## Red Flags

- Burn multiple rising while growth slows (worst combination)
- Gross margin declining month-over-month
- Net Dollar Retention < 100% (revenue shrinks even without new churn)
- Cash runway < 9 months with no fundraise in process
- LTV:CAC declining across successive cohorts
- Any single customer > 20% of ARR (concentration risk)
- CFO doesn't know cash balance on any given day

## Integration with Other C-Suite Roles

| When... | CFO works with... | To... |
|---------|-------------------|-------|
| Headcount plan changes | CEO + COO | Model full loaded cost impact of every new hire |
| Revenue targets shift | CRO | Recalibrate budget, CAC targets, quota capacity |
| Roadmap scope changes | CTO + CPO | Assess R&D spend vs. revenue impact |
| Fundraising | CEO | Lead financial narrative, model, data room |
| Board prep | CEO | Own financial section of board pack |
| Compensation design | CHRO | Model total comp cost, equity grants, burn impact |
| Pricing changes | CPO + CRO | Model ARR impact, LTV change, margin impact |

## Resources

- `references/financial_planning.md` — Modeling, SaaS metrics, FP&A, BvA frameworks
- `references/fundraising_playbook.md` — Valuation, term sheets, cap table, data room
- `references/cash_management.md` — Treasury, AR/AP, runway extension, cut vs invest decisions
- `scripts/burn_rate_calculator.py` — Runway modeling with hiring plan + scenarios
- `scripts/unit_economics_analyzer.py` — Per-cohort LTV, per-channel CAC
- `scripts/fundraising_model.py` — Dilution, cap table, multi-round projections
