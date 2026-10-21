# Flaky eval cases and quarantine

Why agent evals flake, when a flaky case is a defect rather than noise, and the
quarantine policy `flake_detector.py` and `regression_gate.py` enforce.

Confidence key: 🟢 verified on the primary source · 🟡 secondary · 🔴 convention.

## 1. Definition

A flaky test is one whose outcome is non-deterministic for the same version of
the code. 🟢 [Luo et al. 2014] Google's version: "a test that exhibits both a
passing and a failing result with the same code". 🟢 [Micco 2016]
For evals: a case is flaky when `0 < c < n` across repeated trials of the same
candidate.

## 2. How common it is in ordinary software

At Google, about 1.5% of all test runs reported a flaky result, almost 16% of
tests had some flakiness, and about 84% of observed pass→fail transitions
involved a flaky test. 🟢 [Micco 2016] In Luo et al.'s study of fix commits,
async waits (45%), concurrency (20%) and test-order dependency (12%) caused 77%
of classified flakes. 🟢 [Luo et al. 2014]

Agents add three causes of their own:

| Cause | Signature | Fix |
|---|---|---|
| Sampling variance in the agent | the transcript takes a different path each trial | this is the product's reliability: track pass^k, do not quarantine it away |
| Model-graded outcome | the same trial gets different grades | grade it twice; calibrate the grader against human labels |
| Shared state between trials | later trials see earlier trials' files, git history, DB rows | a clean environment per trial |

Anthropic reports a case where Claude read git history left by earlier trials,
which is the third row exactly, and notes that failures caused by a shared
infrastructure limit are not independent. 🟢 [Anthropic]

## 3. Flaky is often the finding

In a unit test, flakiness is usually the test's fault. In an agent, run-to-run
variance is often the defect a user will hit. A 3/5 case is a 60% per-trial
reliability and a 22% pass^3. That is why:

- critical cases are **never** quarantine candidates (`flake_detector.py`
  lists them as "fix, never quarantine"; `regression_gate.py` blocks a
  quarantine entry that covers one);
- the gate compares per-case pass **rates**, so a case that drops from 5/5 to
  3/5 counts as a regression even though it still "passes sometimes".

## 4. Quarantine policy

Google's mitigations included re-running only failing tests, reporting a test
as failed only after 3 consecutive failures, and auto-quarantining very flaky
tests with a bug filed, while warning that quarantine can hide real race
conditions. Google publishes no numeric cut-off. 🟢 [Micco 2016]

This skill's policy (🔴 design choice, adjust to your team):

1. Quarantine is an entry in a file, never a deleted case.
2. Every entry has an **owner**, an **expiry date** and a **reason**. The gate
   blocks any entry missing owner or expiry.
3. Expired entries re-enter the gate on their own. Nobody has to remember.
4. Critical cases cannot be quarantined.
5. The quarantine file is reviewed like code.

## 5. Minimum trials

Stability cannot be judged from one or two trials: a 2/2 case has a Wilson 95%
interval of about 0.34-1.0. tau-bench's main results use at least 3 trials per
task. 🟢 [tau-bench] The flake detector refuses below 3 (exit 4) and the
default `k` is 3. Five trials is a better default for critical cases. 🔴

## 6. Check that trials are independent

Every statistic in this skill assumes trials of a case are independent draws.
Order-dependent tests are a named flaky-test category in Luo et al. (2014);
in agent suites the usual causes are state left behind by an earlier trial,
a warming cache, rate limiting, or a reused session. `flake_detector.py`
prints a trial-order warning when every failure lands in the later half of
the trial numbers. Fix the harness (fresh environment per trial, randomized
order) before trusting a pass rate or a gate verdict. 🔴 heuristic

## 7. Do not lower the temperature to pass

Miller: "in neither case should the sampling temperature be adjusted" to reduce
measured variance. 🟢 [Miller 2024] A suite that passes only at temperature 0
measures a configuration your users do not run.

## Sources

1. Luo, Q., Hariri, F., Eloussi, L., Marinov, D. (2014). *An Empirical Analysis of Flaky Tests.* FSE 2014 — https://huang.isis.vanderbilt.edu/cs8395/paper/flakytest.pdf
2. Micco, J. (2016). *Flaky Tests at Google and How We Mitigate Them.* Google Testing Blog — https://testing.googleblog.com/2016/05/
3. Anthropic Engineering. *Demystifying evals for AI agents.* — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
4. Yao, S. et al. (2024). *τ-bench.* arXiv:2406.12045 — https://arxiv.org/abs/2406.12045
5. Miller, E. (2024). *Adding Error Bars to Evals.* arXiv:2411.00640 — https://arxiv.org/abs/2411.00640
6. NIST/SEMATECH e-Handbook, §7.2.4.1 — https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm
