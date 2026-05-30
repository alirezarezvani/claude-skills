---
description: Pricing model selection (subscription / usage / value / hybrid), Van Westendorp WTP analysis, packaging design. Recommends a model + range, never a specific number. Direct invocation of the pricing-strategist skill.
argument-hint: "<pricing context: industry, deal size, customer count, value drivers>"
---

# /cs:pricing-strategy — Pricing model + WTP + packaging

Run the `pricing-strategist` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`pricing_model_picker.py`** — Rank 5 pricing models (subscription seat-based, usage-based, value-based, freemium, hybrid) with fit-score 0-100 each. Industry tuning via `--profile {saas,api,ai-tools,enterprise-software,marketplace}`. Deterministic logic — consumption pattern + value drivers map to model fit.

2. **`wtp_analyzer.py`** — Van Westendorp Price Sensitivity Meter. Takes survey responses (4 prices per respondent: too cheap, bargain, getting expensive, too expensive). Computes OPP / IDP / PMC / PME intersections. Outputs **Range of Acceptable Prices** + **Optimal Price Point** (with N<30 sample-size warning).

3. **`packaging_designer.py`** — 3-tier (Good/Better/Best) packaging recommendation with feature-to-tier assignment based on importance + segment fit. Flags anti-patterns: "no differentiation", "Best > 2x price with < 1.5x value".

## Output

- Pricing model recommendation (model + range)
- WTP analysis (4 price points + RAP + OPP)
- Packaging design (3-tier feature map)

## Hard rule

**This skill never recommends a specific price.** It recommends a **model and a range**. The human picks the number.

## Distinct from

- `cs-deal-desk` — that's **per-deal** discount approval.
- `c-level-advisor/cmo-advisor` — that's **positioning + brand**.
- `c-level-advisor/cro-advisor` — that's **strategic revenue motion**.
