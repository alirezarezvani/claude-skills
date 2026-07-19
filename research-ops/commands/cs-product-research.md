---
description: Product / user research methodology. Select the right method for the goal (generative vs evaluative vs validation), compute method-based saturation / sample size with an explicit confidence level, and synthesize coded observations into insights while flagging single-source anecdotes. Never fabricates insight. Direct invocation of the product-research skill.
argument-hint: "<research context: goal, product stage, segments, coded observations>"
---

# /cs:product-research — Study design + saturation + insight synthesis

Run the `product-research` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`study_designer.py`** — Map (research goal × product stage) to an appropriate method and emit a plan skeleton (objective, participant criteria, guide structure, success criteria). Redirects live A/B to `product-team/experiment-designer`.

2. **`saturation_planner.py`** — Method-based sample guidance with an explicit confidence label: Nielsen problem-discovery (5/segment), Guest et al. thematic saturation (~12), evaluative coverage. Never claims a prevalence rate from a small-n usability test.

3. **`insight_synthesizer.py`** — Cluster coded observations by tag, count distinct participants, rank by cross-participant recurrence, and flag any candidate below the source threshold as an ANECDOTE — never promoting it to an insight.

## Output

- Recommended method + plan skeleton (matched to the goal)
- Sample / saturation plan with confidence + limits
- Synthesized candidates: INSIGHT vs ANECDOTE with evidence
- Top 3 next actions

## Hard rule

**Method must match the goal, and an insight requires recurrence across independent participants.** A single quote is an anecdote, not a finding.

## First run + optimization

- **Onboard first:** `python3 skills/product-research/scripts/onboard.py` (product profile, insight source-threshold, saturation method, high-stakes flag) — saved config pre-configures every tool. `--show` lists the questions.
- **Optimize (opt-in):** only if the user asks to optimize the synthesis/run a loop, hand off to autoresearch via `skills/product-research/scripts/ar_evaluator.py` (`validated_insights`, higher is better).

## Distinct from

- `product-team/ux-researcher-designer` — that produces personas/journey artifacts. This is method + repository discipline.
- `product-team/product-discovery` — that plans discovery sprints. This designs and synthesizes the research.
- `product-team/experiment-designer` — that runs live A/B. This runs qualitative/evaluative research.
- `market-research` (sibling) — that studies the market. This studies users.
