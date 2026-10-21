---
title: "Agent Regression Evals — prove the change did not make it worse — Agent Skill for Codex & OpenClaw"
description: "Use when an agent, prompt, model or tool change needs proof it did not make the agent worse — setting up a regression eval suite, deciding whether a. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Agent Regression Evals — prove the change did not make it worse

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `agent-regression-evals`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/agent-regression-evals/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


> **Portability:** 3 stdlib scripts, no APIs, no LLM calls. You run the agent; these grade, count and gate.

"Pass rate went from 82% to 79%" is not a finding until you know whether three
points is outside the noise. Agents are non-deterministic, so one trial per
case cannot tell a regression from a coin flip, and a final answer can be right
while the path to it called a tool it never should have.

## Workflow

```bash
# 0 - Run every case k times (k >= 3) on baseline and candidate, from a clean
#     environment per trial. Write one JSONL row per trial:
#     {"case_id": "refund-lookup", "trial": 1, "passed": true, "critical": true,
#      "cost_usd": 0.012, "trajectory": [{"tool": "get_order", "args": {...}}]}
# 1 - Grade the path where the path matters (safety, required lookups).
python scripts/trajectory_checker.py --spec cases.json --results candidate.jsonl
# 2 - Separate flaky cases from stable ones before trusting any comparison.
python scripts/flake_detector.py --results candidate.jsonl --k 3 --quarantine-out q.json
# 3 - Gate: paired per-case comparison against baseline. Exit 4 blocks the merge.
python scripts/regression_gate.py --baseline baseline.jsonl --candidate candidate.jsonl --quarantine q.json
```

Step 1 uses match modes `strict | unordered | subset | superset`. Default to
`superset` (required steps present, harmless exploration allowed); grade the
outcome, not the path, unless order is the requirement. `forbidden` tools block
in every mode.

Step 2 reports **pass@k** (succeeds at least once in k) and **pass^k** (succeeds
all k times). A user meets every trial, so pass^k is the reliability number.
Cases marked critical are never quarantine candidates.

Step 3 averages trials within each case first (trials of one case are
correlated), then tests paired per-case differences with a t-based 95% CI and a
one-sided exact McNemar test. When the drop is real but the sample is too small
to show it, the gate says how many cases it would take.

## The gate blocks on

1. A statistically significant drop (CI upper bound below zero, or McNemar p < 0.05).
2. A critical case that passed every baseline trial and failed any candidate trial.
3. A baseline case missing from the candidate run. Dropping a case is the cheapest fake fix.
4. A quarantine entry with no owner or expiry, or covering a critical case.
5. A forbidden tool call (trajectory checker, exit 4).

It warns, and a human decides, on an underpowered drop above `--tolerance` or a
cost rise above `--max-cost-increase`.

## Hard rules

- **Never compare single trials.** Under 3 trials per case the flake detector refuses (exit 4).
- **Never pool trials as independent samples.** Average per case, then compare cases.
- **Never quarantine without owner and expiry.** An expired entry re-enters the gate automatically.
- **Never delete a failing case to go green.** The gate counts what is missing.
- **Never call "no significant drop" a pass on 8 cases.** Report the power note with the verdict.
- **Start the suite from real failures** (20-50 cases), balanced between "should do" and "should not do".

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/trajectory_checker.py` | Grades tool-call paths: match modes, args modes, forbidden tools, call ceilings | 0 · 2 deviations · 3 bad input · 4 forbidden tool |
| `scripts/flake_detector.py` | STABLE_PASS / STABLE_FAIL / FLAKY per case, Wilson CI, pass@k, pass^k, quarantine stubs | 0 · 2 flaky · 3 · 4 too few trials |
| `scripts/regression_gate.py` | Paired CI, exact McNemar, critical cases, dropped cases, quarantine validity, cost | 0 PASS · 2 WARN · 3 · 4 BLOCK |

All support `--sample` and `--output json`.

## References and assets

- [`references/eval_statistics.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/agent-regression-evals/references/eval_statistics.md) — pass@k vs pass^k, per-case averaging, paired CI, McNemar, power (7 sources)
- [`references/trajectory_grading.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/agent-regression-evals/references/trajectory_grading.md) — outcome vs path, match modes, grader types (6 sources)
- [`references/flaky_cases_and_quarantine.md`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/agent-regression-evals/references/flaky_cases_and_quarantine.md) — flake causes, quarantine with expiry, clean trials (6 sources)
- [`assets/eval_case_spec.example.json`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/agent-regression-evals/assets/eval_case_spec.example.json) — trajectory spec for step 1
- [`assets/sample_baseline.jsonl`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/agent-regression-evals/assets/sample_baseline.jsonl), [`assets/sample_candidate.jsonl`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/agent-regression-evals/assets/sample_candidate.jsonl) — results format
- [`assets/ci_eval_gate.example.yml`](https://github.com/alirezarezvani/claude-skills/tree/main/engineering/skills/agent-regression-evals/assets/ci_eval_gate.example.yml) — CI job that runs the gate and fails on exit 4
