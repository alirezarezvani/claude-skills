# Measurement Log

The Tier 1 metrics — the ones tied to your objective — are not in LinkedIn's analytics. They
have to be written down as they happen, which is why almost nobody has them and why the
people who do can actually tell whether the work is working.

Five minutes a week. Keep it in the repo or wherever the positioning brief lives.

---

## Tier 1 — outcomes (count these by hand)

| Date | What happened | Traceable to | Objective advanced? |
|---|---|---|---|
| | Inbound conversation started by them | post / comment / profile / referral | |
| | Someone referenced a specific post in their first message | | |
| | Invitation (podcast, panel, guest post, talk) | | |
| | Referral or intro offered without asking | | |
| | Qualified enquiry (they named budget, timeline, or a scoped problem) | | |

Attribution is never clean. Record what they said, not what you infer.

## Tier 2 — behavioural proxies (weekly)

| Week | Posts | Median comments/post | Comment share (comments ÷ total interactions) | Notes |
|---|---|---|---|---|
| | | | | |

Comment share is the cleanest available proxy for whether the work lands with people who
care: a comment costs a reader thirty seconds and a small reputational exposure; a reaction
costs a tap.

## Tier 3 — reach (monthly, to notice large changes only)

| Month | Posts | Median impressions | Median engagement rate | Followers | What changed |
|---|---|---|---|---|---|
| | | | | | |

Do not make weekly decisions on these. They are noisy, redefined without notice, and easy to
move in ways that do not serve the objective.

## Quarterly review

Against the 90-day criteria in the positioning brief:

- [ ] Criterion 1: ______ — met / not met
- [ ] Criterion 2: ______ — met / not met
- [ ] Criterion 3: ______ — met / not met

Then three questions:

1. Which pillar produced the **outcomes**, as opposed to the engagement?
2. Did the experimental pillar earn promotion, or should it be replaced?
3. Has the audience description got vaguer? (It always drifts broader. Drag it back.)

## Re-run the tools

```bash
python3 ../scripts/post_performance_analyzer.py --input export.csv --csv --output human
python3 ../scripts/pattern_miner.py --input export.csv --csv --output human
```

Expect `NOTHING_SURVIVED` most times. That is what honest analysis of a small sample looks
like, and it is a finding — not a reason to keep slicing the data until something passes.
