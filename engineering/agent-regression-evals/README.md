# agent-regression-evals

> "The pass rate went from 82% to 79%" is not a finding until you know whether
> three points is outside the noise.

Agents are non-deterministic. One trial per case cannot tell a regression from
a coin flip, and a correct final answer can hide a tool call that should never
have happened. This plugin turns repeated-trial eval results into a merge
decision with the statistics behind it.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install agent-regression-evals
```

## Use

```bash
/cs-agent-evals baseline.jsonl candidate.jsonl cases.json   # full pass
/cs-eval-gate baseline.jsonl candidate.jsonl                # just the gate
```

Or run the scripts directly. Each has `--help`, `--sample` and `--output json`:

```bash
cd skills/agent-regression-evals
python scripts/trajectory_checker.py --sample
python scripts/flake_detector.py --sample
python scripts/regression_gate.py --sample
```

## The three scripts

| Script | Question | Exit codes |
|---|---|---|
| `trajectory_checker.py` | Did the agent take an acceptable path? strict / unordered / subset / superset, argument matching, **forbidden tools block in every mode** | 0 · 2 deviations · 3 bad input · **4 forbidden tool** |
| `flake_detector.py` | Which cases are stable and which flip between identical trials? pass@k, **pass^k**, Wilson intervals, quarantine stubs | 0 · 2 flaky · 3 · **4 too few trials** |
| `regression_gate.py` | Is the candidate measurably worse? Per-case averaging, paired t-based CI, exact one-sided McNemar, critical cases, dropped cases, quarantine validity, cost | 0 PASS · 2 WARN · 3 · **4 BLOCK** |

## Design decisions

- **pass^k, not just pass@k.** A user meets every trial, not the best one. tau-bench showed a model at 61%
  pass^1 falling below 25% at pass^8.
- **Average within a case, compare across cases.** Treating 5 trials x 40 cases as 200 independent samples
  overstates confidence (Miller 2024).
- **Missing cases block.** Deleting a failing case is the cheapest way to "fix" a regression.
- **Quarantine expires.** Every entry needs an owner and a date; expired entries re-enter the gate by themselves.
- **Outcome first, path where it matters.** Trajectory checks default to `superset`, following Anthropic's
  warning that strict path checks fail valid alternatives.

See `skills/agent-regression-evals/references/` for every formula and its source.

## Distinct from

- `prompt-governance` — versions and registers prompts; this gates a change.
- `self-eval` — grades one session's work.
- `agenthub` eval — ranks parallel agents inside one session.

## License

MIT
