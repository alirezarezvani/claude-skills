---
title: "/cs-market-research — Slash Command for AI Coding Agents"
description: "Market research methodology. Size a market as TAM/SAM/SOM computed BOTH top-down and bottoms-up (never a single number), plan a survey sample size. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-market-research

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/research-ops/commands/cs-market-research.md">Source</a></span>
</div>


Run the `market-research` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`market_sizer.py`** — Compute TAM/SAM/SOM by BOTH top-down (total market value × fractions) and bottoms-up (customers × price × adoption) methods side-by-side. Reports divergence and flags failed triangulation. Industry tuning via `--profile`. Never returns a single number.

2. **`sample_size_planner.py`** — Survey sample size from confidence, margin of error, and expected proportion, with the finite-population correction and per-segment minimums (a survey powered overall is not powered per reported segment).

3. **`segmentation_scorer.py`** — Score candidate segments against Kotler's measurable / substantial / accessible / differentiable / actionable criteria. Enforces a substantiality + accessibility gate; drops demographic slices that are too small or unreachable.

## Output

- TAM/SAM/SOM both ways + triangulation flag + assumptions
- Survey n (overall + per-segment floors)
- Segment scores with TARGET / WATCH / DROP verdicts
- Top 3 next actions

## Hard rule

**A market size always travels with its method (both ways) and assumptions — never a single unsourced number.**

## First run + optimization

- **Onboard first:** `python3 scripts/onboard.py` (market profile, survey confidence, margin of error, sizing method) — saved config pre-configures every tool. `--show` lists the questions.
- **Optimize (opt-in):** only if the user asks to reconcile the sizing/run a loop, hand off to autoresearch via `scripts/ar_evaluator.py` (`tam_divergence`, lower is better).

## Distinct from

- `marketing-skill/campaign-analytics` — that measures a live campaign. This is upstream methodology.
- `marketing-skill/marketing-strategy-pmm` — that sets positioning/GTM. This sizes and segments the market.
- `commercial/pricing-strategist` — that sets price. This sizes the market.
