---
title: "/cs-channel-econ — Slash Command for AI Coding Agents"
description: "Direct vs partner-led channel economics — fully-loaded cost-to-serve, channel ROI, optimal channel mix. NOT partnership structure (sibling. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-channel-econ

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/commercial/commands/cs-channel-econ.md">Source</a></span>
</div>


Run the `channel-economics` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`channel_mix_optimizer.py`** — Per-channel effective LTV, payback period (CAC / monthly margin), LTV/CAC efficiency ratio. Recommends mix maximizing effective ARR subject to constraints (min_direct_pct, max_partner_concentration). Sensitivity table (what if direct CAC rises 20%?).

2. **`cost_to_serve_calculator.py`** — Fully-loaded cost-to-serve per deal AND per $ ARR. Breaks out direct costs vs allocated overhead. Computes "true gross margin" after channel-specific load. Surfaces hidden costs (partner enablement time, certification investment, conflict resolution overhead).

3. **`channel_roi_analyzer.py`** — ROI per channel with 3 lenses: cash ROI year-1, LTV ROI, marginal ROI (diminishing-returns curve). Verdict: DOUBLE-DOWN / MAINTAIN / DEFUND / EXIT + diminishing-returns inflection point.

## Hard rule

**No channel ROI computation without retention differential.** Channel CAC alone is meaningless — partner-channel customers often have different retention than direct.

## Distinct from

- Sibling `partnerships-architect` — partnership **structure** (tier, GTM, revshare). Channel-economics is the **math**.
- `business-growth/revenue-operations` — process (lead routing, SDR motion)
- `c-level-advisor/cro-advisor` — strategic
- `finance/financial-analysis` — close + report (backward-looking); channel-economics is **forward** per-channel economics
