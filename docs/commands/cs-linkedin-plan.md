---
title: "/cs-linkedin-plan — Slash Command for AI Coding Agents"
description: "/cs-linkedin-plan — Build the positioning brief (objective, audience, 2-4 proof-backed pillars, exclusion list), size a weekly cadence against the. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-linkedin-plan

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/marketing/linkedin/commands/cs-linkedin-plan.md">Source</a></span>
</div>


**Command:** `/cs-linkedin-plan [your 90-day goal]`

Three decisions in order. Out of order is why most LinkedIn efforts produce a feed of
unrelated observations and stop in week five.

## When to run

- "What should I post about?" / "How often should I post?"
- "Should I start a LinkedIn newsletter?"
- Before drafting anything — posts without pillars are noise

## What you get

1. **A validated positioning brief** — one of six real objectives, an audience specific
   enough to exclude someone, two to four pillars with shares summing to 100, and at least
   two exclusions.
2. **Observable 90-day criteria.** Follower count is deliberately not among them.
3. **A weekly plan priced in minutes**, allocated by stage, plus the minimum viable week that
   survives a bad week.
4. **A newsletter verdict** — green, thin, or refused, with a 12-issue arc and a stop rule.

## Workflow

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-strategy/scripts/positioning_brief.py --input brief.json --output human
#   exit 3 = objective or audience too vague to proceed. Fix that before anything else.

python3 ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-strategy/scripts/cadence_planner.py \
  --minutes 240 --stage starting --target-posts 3 --output human
#   exit 2 = below the 90-minute floor -> comment-only week returned
#   exit 3 = over budget, with the overage named

python3 ${CLAUDE_PLUGIN_ROOT}/skills/linkedin-strategy/scripts/newsletter_planner.py \
  --followers 1800 --cadence biweekly --minutes-per-month 420 --output human
```

## Discipline

- **One objective.** Two serve neither; sequence instead of blending.
- **The exclusion list is the positioning.** Do not skip it because it feels negative.
- **Price the week from a bad week.** The plan has to survive week five, not week one.
- **From a standing start, most of the budget belongs in other people's comments.**
- **Review quarterly, not weekly.** A brief revised monthly is a mood.

## Stop conditions

- Brief at exit 0 and the cadence plan fits → done; hand over the minimum viable week.
- Cadence over budget twice on the same target → the target is the problem, not the plan.
  Say so and cut it.
- Newsletter refused → say why once, recommend posts on a fixed day instead, and stop.

## Related

- Skill: [`linkedin-strategy`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-strategy/SKILL.md)
- Next: [`/cs-linkedin-post`](cs-linkedin-post.md) once the brief exists
