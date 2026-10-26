---
title: "/cs-linkedin-analyze — Slash Command for AI Coding Agents"
description: "/cs-linkedin-analyze — Read your own exported LinkedIn post data, report medians and outlier bands rather than misleading means, test candidate. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-linkedin-analyze

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/marketing/linkedin/commands/cs-linkedin-analyze.md">Source</a></span>
</div>


**Command:** `/cs-linkedin-analyze [export path or the claim to test]`

Your own data only. Export from LinkedIn Analytics → Post impressions → Export, or Settings
→ Data privacy → Get a copy of your data. Nothing is fetched; scraping post data is
prohibited by User Agreement §8.2 and none of this needs it.

## When to run

- "Why did my reach drop?"
- "Do carousels actually do better for me?"
- "What's working?"
- Before changing strategy on the basis of one post that did well

## What you get

1. **A description** — median and MAD, percentile bands, a 1.5×IQR breakout threshold, and a
   per-post band from BREAKOUT to DUD.
2. **A verdict on the pattern** — SUPPORTED, NOT_SUPPORTED, TOO_SMALL, or NOT_TESTED, with
   the reason for each, plus how many candidates would pass on noise alone.
3. **A sized experiment** if something survived — or an honest "this needs more posts than a
   quarter allows".

## Workflow

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-analytics/scripts/post_performance_analyzer.py \
  --input export.csv --csv --output human
#   exit 2 = under 10 posts. Descriptive only. Say so and stop.

python3 ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-analytics/scripts/pattern_miner.py \
  --input export.csv --csv --output human
#   exit 2 = nothing survived. This is a real finding, not a failure.

# CV for the planner = 1.4826 * MAD / median, from step one
python3 ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-analytics/scripts/experiment_planner.py \
  --hypothesis "..." --variable "..." --cv 0.45 --effect 0.30 \
  --posts-per-week 2 --max-weeks 12 --output human
```

## Discipline

- **Under 10 posts, describe; do not conclude.** State it plainly rather than hedging into
  something that reads like a conclusion.
- **"Nothing survived" is the most common honest answer.** Report it as a finding.
- **A pattern in past posts is a hypothesis.** Retrospective data is confounded — you made
  carousels when you had structured material, on topics you knew best, in weeks you had time.
- **Never benchmark against someone else's numbers.** Different denominator, different
  audience, usually a vendor's sample.
- **Follower count is not a success metric.** Point them at the Tier 1 log instead.
- **One good post is not evidence.** It is the least informative event available.

## Stop conditions

- Description delivered and the user knows which three outcome metrics to log by hand → done.
- Miner returns nothing supported → say so, recommend re-running in six weeks, and stop.
  Do not keep slicing the data until something passes.
- Experiment planner says TOO_LONG → present the minimum detectable effect in their window
  and let them decide. Do not quietly shrink the effect to make it fit.

## Related

- Skill: [`linkedin-analytics`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-analytics/SKILL.md)
- Log: [`measurement_log_template.md`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-analytics/assets/measurement_log_template.md)
- Reference: [`evidence_thresholds.md`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-analytics/references/evidence_thresholds.md)
