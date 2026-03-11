---
title: "Product Analyst Agent"
description: "Product Analyst Agent - Claude Code agent for Product."
---

# Product Analyst Agent

<div class="page-meta" markdown>
<span class="meta-badge">:material-robot: Agent</span>
<span class="meta-badge">:material-lightbulb-outline: Product</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/agents/product/cs-product-analyst.md">Source</a></span>
</div>


## Skill Links
- [`product-analytics/SKILL.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-analytics/SKILL.md)
- [`experiment-designer/SKILL.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/experiment-designer/SKILL.md)

## Primary Workflows
1. Metric framework and KPI definition
2. Dashboard design and cohort/retention analysis
3. Experiment design with hypothesis + sample sizing
4. Result interpretation and decision recommendations

## Tooling
- [`scripts/metrics_calculator.py`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/product-analytics/scripts/metrics_calculator.py)
- [`scripts/sample_size_calculator.py`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/experiment-designer/scripts/sample_size_calculator.py)

## Usage Notes
- Define decision metrics before analysis to avoid post-hoc bias.
- Pair statistical interpretation with practical business significance.
- Use guardrail metrics to prevent local optimization mistakes.
