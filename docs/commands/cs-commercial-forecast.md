---
title: "/cs-commercial-forecast — Slash Command for AI Coding Agents"
description: "Forward bookings / billings / ARR forecast with funnel + cohort math + conversion-assumption disclosure. NOT financial close (finance). Direct. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-commercial-forecast

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/commercial/commands/cs-commercial-forecast.md">Source</a></span>
</div>


Run the `commercial-forecaster` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`bookings_forecaster.py`** — Stage-conversion based bookings forecast using last-4-quarters weighted (most recent heavier). Outputs commit / best-case / pipe-only. Industry tuning `--profile {saas,api,enterprise-software,marketplace,services}`.

2. **`cohort_arr_projector.py`** — NRR + GRR projection by acquisition cohort. Surfaces leaky cohorts before they show up in the consolidated NRR number.

3. **`funnel_confidence_scorer.py`** — Confidence band per stage: how stable is the conversion rate q-over-q? High variance = low confidence forecast.

## Hard rule

**Conversion assumption ALWAYS surfaced explicitly.** Forecasts without disclosed assumptions are theatre. The output names the conversion rate used and the data window it's based on.

## Distinct from

- `finance/financial-analysis` — **close + report** (backward-looking). Commercial-forecaster is **forward** commercial pipeline.
- `c-level-advisor/cfo-advisor` — strategic financial planning. Commercial-forecaster is tactical, per-quarter.
- `c-level-advisor/cro-advisor` — strategic CRO. Commercial-forecaster feeds CRO judgment.
- Sibling `pricing-strategist` — sets prices; commercial-forecaster projects revenue at those prices.
