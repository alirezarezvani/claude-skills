---
name: linkedin-strategy
description: Use when someone needs a LinkedIn plan rather than a post — content pillars, positioning for a career change or consulting or thought leadership, a sustainable posting cadence, or a newsletter decision. Triggers on "what should I post about", "how often should I post", "LinkedIn content strategy", "should I start a LinkedIn newsletter", "grow my following", "90-day plan". Validates the positioning brief, sizes the week against real hours and refuses a plan that will not survive week five, and gates a newsletter against eligibility and a six-month cadence commitment.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-08-25
---

# LinkedIn Strategy — brief, cadence, newsletter

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
| [`scripts/positioning_brief.py`](scripts/positioning_brief.py) | Validates objective, audience, 2-4 proof-backed pillars, and the exclusion list; emits observable 90-day criteria. |
| [`scripts/cadence_planner.py`](scripts/cadence_planner.py) | Prices the week in minutes, allocates by stage, refuses over-budget targets, emits the minimum viable week. |
| [`scripts/newsletter_planner.py`](scripts/newsletter_planner.py) | Eligibility + six-month sustainability gate, 12-issue arc across pillars, stop rule. |

## References and assets

- [`references/objective_to_pillars.md`](references/objective_to_pillars.md) — the six objectives and the pillar arithmetic (7 sources)
- [`references/cadence_and_consistency.md`](references/cadence_and_consistency.md) — what a post really costs and why the floor exists (7 sources)
- [`references/newsletter_playbook.md`](references/newsletter_playbook.md) — eligibility, cadence as a promise, the stop rule (7 sources)

- [`assets/positioning_brief_template.md`](assets/positioning_brief_template.md) — fillable brief
- [`assets/example_brief.json`](assets/example_brief.json) — a passing brief, for the validator

## Distinct from

- **`linkedin-content`** — drafts and lints individual posts. This decides what they are about
  and how many there are. Posts without pillars are noise; offer this first, never chain silently.
- **`linkedin-analytics`** — tells you what happened. This decides what to do next.
- **`marketing-skill/content-strategy`** — company-level content marketing. This is one
  person's own presence.

---

**Version:** 1.0.0
