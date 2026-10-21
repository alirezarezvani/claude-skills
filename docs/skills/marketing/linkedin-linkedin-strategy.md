---
title: "LinkedIn Strategy — brief, cadence, newsletter — Agent Skill for Landing Pages"
description: "Use when someone needs a LinkedIn plan rather than a post — content pillars, positioning for a career change or consulting or thought leadership, a. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# LinkedIn Strategy — brief, cadence, newsletter

<div class="page-meta" markdown>
<span class="meta-badge">:material-web: Marketing (Top-Level)</span>
<span class="meta-badge">:material-identifier: `linkedin-strategy`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-strategy/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install marketing-top-level-skills</code>
</div>


Three decisions, in this order. Out of order is why most LinkedIn efforts produce a feed of
unrelated observations and stop in week five.

## Workflow

**1. The brief — an editorial constitution, not a wish.** Walk the five questions one at a
time, each with a recommended answer, then validate:

```bash
python3 scripts/positioning_brief.py --input brief.json --output human
```

It refuses on the two things that make everything downstream impossible: an objective that
is not one of the six real ones (`career-change`, `consulting`, `thought-leadership`,
`hiring`, `fundraising`, `community`), and an audience too broad to exclude anyone. It also
refuses fewer than two exclusions — **a positioning that excludes nothing is availability.**

Pillars: two to four, shares summing to 100, at least one backed by proof that already
exists, at least one at 10-20% as the experimental slot. Every pillar needs a "why you"; if
anyone could post it, cut it.

The script emits observable 90-day criteria. Follower count is deliberately absent — it moves
for reasons unrelated to whether the objective is being met.

**2. The cadence — priced against a bad week.**

```bash
python3 scripts/cadence_planner.py --minutes 240 --stage starting --target-posts 3 --output human
```

Exit 0 fits / 2 below the 90-minute floor / 3 over budget with the overage named. Every
activity is priced in minutes including the reply window, which is part of the post and not
an extra. Allocation shifts with stage: from a standing start **60% of the budget belongs in
other people's comment sections**, because a post published to nobody reaches nobody.

Below 90 minutes a week it refuses to plan a posting schedule and returns a comment-only
week: a cadence abandoned in week five is worse than one never started, because the
abandonment is visible on the profile. Every plan ships with a minimum viable week.

**3. The newsletter — only if the promise can be paid.**

```bash
python3 scripts/newsletter_planner.py --followers 1800 --cadence biweekly \
  --minutes-per-month 420 --pillar "..." --output human
```

Refuses below LinkedIn's published 150-follower evaluation floor, and refuses a cadence
whose six-month cost exceeds the budget. Emits a 12-issue arc rotating issue types across
pillars, and a stop rule written before issue one.

## Rules

- **One objective.** Two objectives serve neither; the audiences overlap less than they look.
- **The exclusion list is the positioning.** Refuse to skip it.
- **Price the week from a bad week, not a good one.**
- **Consistency over volume.** A skipped week is fine; a skipped month resets you.
- **Review the brief quarterly, not weekly.** A brief revised monthly is a mood.

## Scripts

| Script | Role |
|---|---|
| [`scripts/positioning_brief.py`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-strategy/scripts/positioning_brief.py) | Validates objective, audience, 2-4 proof-backed pillars, and the exclusion list; emits observable 90-day criteria. |
| [`scripts/cadence_planner.py`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-strategy/scripts/cadence_planner.py) | Prices the week in minutes, allocates by stage, refuses over-budget targets, emits the minimum viable week. |
| [`scripts/newsletter_planner.py`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-strategy/scripts/newsletter_planner.py) | Eligibility + six-month sustainability gate, 12-issue arc across pillars, stop rule. |

## References and assets

- [`references/objective_to_pillars.md`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-strategy/references/objective_to_pillars.md) — the six objectives and the pillar arithmetic (7 sources)
- [`references/cadence_and_consistency.md`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-strategy/references/cadence_and_consistency.md) — what a post really costs and why the floor exists (7 sources)
- [`references/newsletter_playbook.md`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-strategy/references/newsletter_playbook.md) — eligibility, cadence as a promise, the stop rule (7 sources)

- [`assets/positioning_brief_template.md`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-strategy/assets/positioning_brief_template.md) — fillable brief
- [`assets/example_brief.json`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing/linkedin/skills/linkedin-strategy/assets/example_brief.json) — a passing brief, for the validator

## Distinct from

- **`linkedin-content`** — drafts and lints individual posts. This decides what they are about
  and how many there are. Posts without pillars are noise; offer this first, never chain silently.
- **`linkedin-analytics`** — tells you what happened. This decides what to do next.
- **`marketing-skill/content-strategy`** — company-level content marketing. This is one
  person's own presence.

---

**Version:** 1.0.0
