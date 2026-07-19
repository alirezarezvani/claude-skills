---
title: "/cs-clinical-research — Slash Command for AI Coding Agents"
description: "Clinical study design. Select and classify endpoints, estimate sample size / power (means / proportions / survival), and score a study plan for a GO. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-clinical-research

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/research-ops/commands/cs-clinical-research.md">Source</a></span>
</div>


Run the `clinical-research` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`endpoint_selector.py`** — Score candidate endpoints across clinical relevance, measurability, regulatory acceptance, sensitivity-to-change, and burden. Classify PRIMARY / KEY-SECONDARY / EXPLORATORY. Flags unvalidated surrogates (cannot be primary). Industry tuning via `--profile`.

2. **`sample_size_estimator.py`** — Closed-form power / sample size for two-arm means (Cohen's d), proportions (normal approx), or survival (Schoenfeld events). Inflates for dropout. The effect/difference/HR must trace to a published or anchor-based source.

3. **`phase_gate_scorer.py`** — Score the study plan 0-100 across recruitment feasibility, endpoint readiness, statistical power, operational complexity, and budget fit. Verdict + named owners (PI, Medical Monitor, Biostatistician, Regulatory Owner).

## Output

- Endpoint classification + surrogate flags
- Sample-size estimate with assumptions block
- Phase-gate verdict with named owner chain
- Top 3 next actions

## Hard rule

**Every output is an ESTIMATE, not a protocol.** A biostatistician, medical monitor, and regulatory owner sign the final design.

## First run + optimization

- **Onboard first:** `python3 skills/clinical-research/scripts/onboard.py` (area, alpha, power, dropout, named owners) — saved config pre-configures every tool. `--show` lists the questions.
- **Optimize (opt-in):** only if the user asks to optimize/run a loop, hand off to autoresearch via `skills/clinical-research/scripts/ar_evaluator.py` (`feasibility_composite`, higher is better).

## Distinct from

- `ra-qm-team` — that's the regulatory **submission**. This designs the **study**.
- `research/grants` — that **finds funding**. This **designs the trial**.
- `product-team/experiment-designer` — that's a **product A/B**. This is a **clinical trial**.
