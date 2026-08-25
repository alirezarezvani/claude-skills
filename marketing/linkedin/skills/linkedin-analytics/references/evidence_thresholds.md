# Evidence Thresholds — why most LinkedIn "insights" are noise

The characteristic sentence of LinkedIn analytics is: "carousels do 3x better for
me." It is usually built on four posts. With engagement as heavy-tailed as it is,
four posts will show a 3x difference between almost any two groups you care to
define — including groups defined by the first letter of the first word.

`pattern_miner.py` exists to kill that sentence before it becomes a strategy.

---

## The four gates

A candidate pattern has to pass all four. Most fail at the first.

### 1. Group size floor — at least 5 in, 5 out
Below five, the median is one or two posts and any difference is a coin flip.
Reported as `NOT_TESTED`, with the counts, because "you do not have enough data
yet" is a real and useful finding.

### 2. Effect floor — 15% relative difference in medians
A statistically detectable 3% difference is not a decision. If you would not
change what you write over it, testing it is a waste of the posts. The floor is
set at the level where a rational person would actually act.

### 3. Permutation test — beat 90% of 2,000 label shuffles
The labels ("carousel" / "not carousel") are shuffled 2,000 times against a fixed
seed, the difference of medians recomputed each time, and the observed difference
must be larger than at least 90% of them.

A permutation test is the right instrument here because it makes **no
distributional assumption**. A t-test assumes something approximately normal;
engagement rate is not. The permutation null asks the only question that matters:
*given these exact numbers, how often would random labelling produce a gap this
big?*

The seed is fixed, so the same data always produces the same verdict. An analysis
tool that returns a different answer on re-run is not an analysis tool.

### 4. Multiple comparisons — count every test, report the expected false positives
This is the gate nobody else implements, and it is the one that catches the most
self-deception.

If you test twenty candidate patterns at α = 0.10, **two will pass on noise
alone**. That is not a flaw in the method; it is what the threshold means. The
miner reports how many candidates reached the test, how many you would expect to
pass by chance, and how many actually did. When those numbers are close, it says
so.

It also skips mirrored candidates: for a two-value attribute, "carousel vs rest"
and "text vs rest" are the same comparison with the sign flipped, and counting
both would double-count it in the accounting.

Gelman and Loken's "garden of forking paths" is the sharper version of the
problem: even without formally testing twenty hypotheses, an analyst who *would
have* tested a different cut had the data looked different is effectively
multiple-testing. The defence is to declare the cuts in advance — which is why
the miner takes a fixed attribute list rather than searching for whatever splits
best.

## Why a found pattern is a hypothesis, not a finding

Everything the miner reports is retrospective. It found a difference in posts you
already wrote, chosen for reasons that correlate with everything else about them:
you probably made carousels when you had structured material, on topics you knew
best, in weeks when you had time.

That is confounding, and no amount of statistics on the same dataset removes it.

The only way to get a finding is a deliberate test: decide the variable in
advance, alternate the arms, hold the confounds constant, and run the window.
`experiment_planner.py` sizes it — and will frequently tell you the test needs
more posts than you can produce in a quarter. **That is an honest answer**, and
it is more useful than a confident conclusion from retrospective data.

## The uncomfortable arithmetic

At a realistic coefficient of variation (0.35-0.6 for most accounts) and a
30% target effect, a two-arm test needs roughly 20-60 posts. At two posts a week,
that is 5-30 weeks.

Which means: **most of the LinkedIn A/B tests people describe are not runnable at
their actual posting volume.** The honest responses are to test only variables
where you expect a large effect, to accept a large minimum detectable effect and
say so, or to stop testing and write the thing you would rather write.

## Things that are not evidence

- **One post that did well.** The single most common cause of a strategy change,
  and the least informative event available. A breakout post tells you a specific
  post worked, in a specific week, with a specific audience state.
- **Comparing this month to last month.** Confounded by season, news cycle,
  audience growth, and LinkedIn product changes, all at once.
- **Someone else's benchmark.** Different denominator, different audience,
  usually a vendor's sample.
- **A pattern that appeared after you went looking for one.** See forking paths
  above.

## What to do instead of measuring more

Post consistently for a quarter against a brief. Track the Tier 1 outcome metrics
by hand — conversations, references, invitations. Re-run the miner every six
weeks and expect it to say "nothing survived" most times, because that is what
honest analysis of a small sample looks like.

The compounding comes from consistency, not from optimisation, and the
optimisation is unavailable at this sample size anyway.

---

## Sources

1. Good, P. **Permutation, Parametric, and Bootstrap Tests of Hypotheses**
   (3rd ed.) — the permutation framework and its distribution-free guarantee.
2. Gelman, A. & Loken, E. **"The Garden of Forking Paths"** (2013) — why
   researcher degrees of freedom produce false positives without any explicit
   p-hacking.
3. Cohen, J. **Statistical Power Analysis for the Behavioral Sciences** (2nd ed.)
   — the two-sample sizing formula used by `experiment_planner.py`, and the case
   for declaring a minimum effect of interest.
4. Tukey, J. **Exploratory Data Analysis** (1977) — robust summaries, and the
   distinction between exploratory and confirmatory analysis that this whole
   document rests on.
5. Ioannidis, J. **"Why Most Published Research Findings Are False."** *PLoS
   Medicine*, 2005 — the relationship between small samples, many tests, and
   false discovery.
6. Benjamini, Y. & Hochberg, Y. **"Controlling the False Discovery Rate."**
   *JRSS-B*, 1995 — the formal treatment of the multiple-comparisons accounting
   the miner reports informally.
7. Taleb, N.N. **Statistical Consequences of Fat Tails** (2020) — why sample
   means and standard deviations mislead for heavy-tailed processes, and why
   medians are used throughout.
