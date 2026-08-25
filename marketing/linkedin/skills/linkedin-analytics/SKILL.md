---
name: linkedin-analytics
description: Use when someone wants to understand their own LinkedIn numbers — which posts worked, why reach dropped, whether a pattern is real, or how to test a hypothesis. Triggers on "why did my reach drop", "what's working on my LinkedIn", "analyze my posts", "do carousels do better for me", "should I test this", "LinkedIn analytics". Reads your own exported post data, reports medians and outlier bands, tests candidate patterns against a permutation null, and sizes a real experiment — refusing to conclude anything below 10 posts.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-08-25
---

# LinkedIn Analytics — describe honestly, then refuse to over-conclude

The characteristic sentence of LinkedIn analytics is "carousels do 3x better for me", built
on four posts. With engagement as heavy-tailed as it is, four posts will show a 3x difference
between almost any two groups you care to define. These three scripts stop that sentence
becoming a strategy.

**Your own data only.** Nothing is fetched; scraping post or profile data is prohibited by
User Agreement §8.2 and none of this analysis needs it.

## Workflow

**1. Get the export.** LinkedIn Analytics → Post impressions → Export, or Settings → Data
privacy → Get a copy of your data. CSV and JSON both work.

**2. Describe it.** Exit 0 analysed / 2 below the 10-post floor, descriptive only / 3
unusable. Reports median and MAD rather than mean and standard deviation — one breakout post
makes a mean describe a distribution none of your posts belong to — plus Tukey percentile
bands and a 1.5×IQR breakout threshold, so "this did well" has a number behind it.

```bash
python3 scripts/post_performance_analyzer.py --input posts.csv --csv --output human
```

**3. Test the pattern they think they see.**

```bash
python3 scripts/pattern_miner.py --input posts.json --output human
```

Exit 0 something survived / 2 nothing survived / 3 under 10 posts. Four gates: 5 posts in and
5 out; a 15% relative difference in medians; beating 90% of 2,000 seeded label shuffles; and
a multiple-comparisons accounting of how many candidates would pass on noise alone.

**"Nothing survived" is the most common honest answer and it is a real finding.** Report it
as one. Do not soften it into a hedge that reads like a conclusion.

**4. Turn a survivor into a test.**

```bash
python3 scripts/experiment_planner.py --hypothesis "..." --variable "..." \
  --cv 0.45 --effect 0.30 --posts-per-week 2 --max-weeks 12 --output human
```

CV comes from step 2: `1.4826 * MAD / median`. Exit 0 feasible / 2 too long, with the minimum
detectable effect in their window / 3 refused. It will frequently say the test needs more
posts than a quarter allows — **that is the honest answer**, and more useful than a confident
conclusion from retrospective data.

## Rules

- **Under 10 posts, describe; do not conclude.** Say so plainly.
- **A pattern in past posts is a hypothesis.** Retrospective data is confounded — you made
  carousels when you had structured material, on topics you knew best, in weeks you had time.
  No statistics on the same data removes that.
- **Never benchmark against someone else's numbers.** Different denominator, different
  audience, usually a vendor's sample.
- **Follower count is not a success metric.** Track inbound conversations, specific
  references, invitations — the Tier 1 metrics you count by hand.
- **Report the confidence level.** LinkedIn-official 🟢, third-party study 🟡, folklore 🔴.
- **One good post is not evidence.** It is the most common cause of a strategy change and the
  least informative event available.

## Scripts

| Script | Role |
|---|---|
| [`scripts/post_performance_analyzer.py`](scripts/post_performance_analyzer.py) | Median/MAD, percentile bands, IQR outlier fence, per-post BREAKOUT→DUD classification; refuses conclusions below 10 posts. |
| [`scripts/pattern_miner.py`](scripts/pattern_miner.py) | Four-gate permutation test with multiple-comparisons accounting; reports why every rejected candidate failed. |
| [`scripts/experiment_planner.py`](scripts/experiment_planner.py) | Sizes a two-arm posting experiment, names the confounds to hold constant, and writes the falsification condition before the first post. |

## References and assets

- [`references/linkedin_metrics_canon.md`](references/linkedin_metrics_canon.md) — what each number is, what it is not, and which three tiers to track (7 sources)
- [`references/evidence_thresholds.md`](references/evidence_thresholds.md) — the four gates, forking paths, and the uncomfortable arithmetic of LinkedIn A/B tests (7 sources)

- [`assets/example_post_export.csv`](assets/example_post_export.csv) — a 12-post export in the expected shape
- [`assets/measurement_log_template.md`](assets/measurement_log_template.md) — the Tier 1 outcome log you keep by hand

## Distinct from

- **`marketing-skill/social-media-analyzer`** — cross-platform brand campaign reporting. This
  is one person's own LinkedIn export, with refusals attached.
- **`linkedin-strategy`** — decides what to do next. This says what happened.
- **`product-team/experiment-designer`** — product A/B tests with real traffic; here n is
  posts, and usually too small.

---
**Version:** 1.0.0
