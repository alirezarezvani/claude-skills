# Eval statistics for agents

What the numbers in `flake_detector.py` and `regression_gate.py` mean, where
each formula comes from, and the mistakes they are built to prevent.

Confidence key: 🟢 verified on the primary source · 🟡 secondary source or
formula rebuilt from the paper · 🔴 convention, not sourced.

## 1. pass@k and pass^k answer different questions

With `n` trials of a case and `c` successes:

```
pass@k = 1 - C(n-c, k) / C(n, k)     at least one of k tries succeeds
pass^k = C(c, k) / C(n, k)           all k tries succeed
```

- pass@k is the unbiased estimator from the Codex paper; it is 1.0 when
  `n - c < k`. 🟢 [Chen et al. 2021]
- pass^k is tau-bench's reliability metric, averaged over tasks and defined
  only for `k <= n`. In tau-bench, a model scoring 61.2 at pass^1 on the retail
  domain fell below 25 at pass^8. 🟢 definition / 🟡 estimator form [Yao et al. 2024]
- Anthropic's guidance: use pass^k "when consistency matters", e.g.
  customer-facing agents; a 75% per-trial rate gives about 42% pass^3. 🟢 [Anthropic]

**Rule:** a demo is graded on pass@k, a product on pass^k. Report both; the
gap between them is the flakiness.

## 2. Average within a case, then compare cases

Trials of the same case share difficulty, so they are correlated. Pooling
5 trials x 40 cases as 200 independent observations understates the standard
error. Miller recommends resampling each question K times and using the
per-question mean as the observation, never pooling all answers into one
standard error, and not lowering temperature to fake lower variance. 🟢 [Miller 2024]

`regression_gate.py` therefore reduces each case to its pass rate per run
before any test.

## 3. Pair the comparison

Baseline and candidate run the same cases, so compare per-case differences
`d_i = candidate_i - baseline_i`:

```
mean_d ± t(0.975, n-1) · sd(d) / sqrt(n)
```

Pairing removes case difficulty from the noise: the variance of a paired
difference is `(Var_A + Var_B - 2·Cov)/n`, smaller whenever the two runs agree
on which cases are hard. Miller's recommendation 4 is exactly this:
"question-level paired differences" rather than population summaries. 🟢 [Miller 2024]

The gate uses a t critical value below 31 cases and 1.96 above. 🔴 standard practice.

## 4. McNemar on flipped cases

Reduce each case to a majority outcome per run. Only discordant cases carry
information: `b` = pass→fail, `c` = fail→pass. The exact test is binomial with
p = 0.5 on `b + c` trials; the exact form is preferred when `b + c < 25`. 🟡 [MedCalc]
The gate is one-sided, `P(X >= b)`, because it asks only "did it get worse?". 🔴 standard result.

## 5. Wilson intervals for a single case

`flake_detector.py` prints a Wilson score interval for each case's pass rate:

```
[ p + z²/2n ± z·sqrt( p(1-p)/n + z²/4n² ) ] / (1 + z²/n)
```

NIST notes normal approximations are poor with few failures or small n; Wilson
behaves better at the edges than `p ± 1.96·sqrt(p(1-p)/n)`. 🟢 [NIST]
With 5 trials, a 4/5 case has a 95% interval of roughly 0.38-0.96. That width
is the honest answer to "is this case reliable?".

## 6. Power: how many cases you need

To detect a mean per-case drop `δ` with per-case difference SD `σ` at 5%
two-sided significance and 80% power:

```
n ≈ ((1.96 + 0.84) · σ / δ)²
```

Miller's Eq. 9 generalises this with within-question variance terms. 🟡 [Miller 2024]
The gate prints this `n` whenever a drop exceeds `--tolerance` but the CI
still includes zero. "No significant regression" on 8 cases means "we could
only have seen a large one".

## 7. Many cases, many metrics

Gating on many per-case tests at α = 0.05 raises false blocks. The gate
avoids per-case significance tests entirely: it tests the mean difference once,
McNemar once, and treats critical cases as a policy rule (any failure blocks),
not a test. If you add per-segment gates, correct with Holm-Bonferroni. 🔴 standard practice

## Sources

1. Chen, M. et al. (2021). *Evaluating Large Language Models Trained on Code.* arXiv:2107.03374 — https://arxiv.org/abs/2107.03374
2. Yao, S., Shinn, N., Razavi, P., Narasimhan, K. (2024). *τ-bench: A Benchmark for Tool-Agent-User Interaction.* arXiv:2406.12045 — https://arxiv.org/abs/2406.12045
3. Miller, E. (2024). *Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations.* arXiv:2411.00640 — https://arxiv.org/abs/2411.00640
4. Anthropic Engineering. *Demystifying evals for AI agents.* — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
5. NIST/SEMATECH e-Handbook of Statistical Methods, §7.2.4.1 Confidence intervals for proportions — https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm
6. MedCalc. *McNemar test.* — https://www.medcalc.org/en/book/mcnemar-test.php
7. Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics* 6(2), 65-70.
