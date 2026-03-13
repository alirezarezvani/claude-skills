---
name: "autoresearch-agent"
description: "Autonomous experiment loop that runs overnight research without human intervention. Inspired by Karpathy's autoresearch: agent modifies a target file, runs an evaluation, keeps improvements (git commit), discards failures (git reset), and loops indefinitely. Use when the user wants to: autonomously optimize ML training code, improve prompts by eval score, benchmark-drive code performance, or run any experiment loop with a measurable metric. Requires: a target file to modify, a fixed evaluation function, and a git repo."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: engineering
  updated: 2026-03-13
---

# Autoresearch Agent

> You sleep. The agent experiments. You wake up to results.

Autonomous experiment loop inspired by Andrej Karpathy's [autoresearch](https://github.com/karpathy/autoresearch). The agent proposes changes, runs a fixed-time evaluation, keeps improvements via git, discards failures, and loops indefinitely — no human in the loop.

**Works for any domain with a measurable metric:**
- ML training optimization (original use case — optimize `train.py` by `val_bpb`)
- Prompt engineering (optimize system prompts by LLM-eval quality score)
- Code performance (optimize a module by benchmark runtime/score)
- Agent skill improvement (optimize `SKILL.md` by task completion rate)

---

## Before Starting

Check for `program.md` in the project root. If it exists, read it — it defines the experiment objectives, constraints, and what the agent should optimize. Only ask for what's missing.

If no `program.md` exists, run the **Setup Wizard** below.

---

## Setup Wizard

Answer these 5 questions to configure the experiment:

### 1. What are we optimizing?
The **target** — one file the agent is allowed to modify:
- `train.py` — ML training loop (Karpathy-style)
- `prompt.md` — system prompt for an LLM
- `src/module.py` — a specific code module
- `SKILL.md` — an agent skill definition

### 2. What's the metric?
A **single number** that defines success. Lower or higher = better:
- `val_bpb` — validation bits per byte (ML, lower is better)
- `eval_score` — LLM quality score 0-100 (higher is better)
- `p50_ms` — median latency in milliseconds (lower is better)
- `pass_rate` — test pass rate 0-1 (higher is better)

### 3. What's the time budget per experiment?
How long one experiment run takes:
- `5m` — fast iteration (Karpathy default, ~12 experiments/hour)
- `10m` — moderate (6/hour)
- `30m` — slow but thorough (2/hour)

### 4. What can the agent change?
Constraints on the target file:
- Architecture only? Hyperparameters only? Everything?
- What packages/imports are available?
- What's explicitly off-limits?

### 5. What's the evaluation function?
How we score each experiment:
- Fixed script that outputs the metric (e.g. `python evaluate.py`)
- API call that returns a score
- Test suite with a pass rate

Once answered, run: `python scripts/setup_experiment.py` to initialize.

---

## The Three Files

Every autoresearch project has the same structure:

```
project/
├── program.md       ← Human writes this: objectives, constraints, strategy
├── target.*         ← Agent modifies this: the thing being optimized
├── evaluate.py      ← Fixed: the measurement function (never touch)
├── results.tsv      ← Auto-generated: experiment log (git-tracked for continuity)
└── scripts/
    ├── setup_experiment.py   ← Initialize a new run
    ├── run_experiment.py     ← Execute one experiment iteration
    └── log_results.py        ← Record results to TSV
```

### `program.md` — Your Research Directions
Write this once. The agent reads it before every experiment. It should contain:
- **Goal:** What you want to achieve (minimize loss, maximize score, simplify code)
- **Strategy:** What directions to explore first
- **Constraints:** What the agent cannot change
- **Stopping criteria:** When a result is "good enough"

See `references/program-template.md` for domain-specific templates.

### Target File — The Only File the Agent Edits
Whatever you're optimizing. Strict scope: **one file, one metric**.

### `evaluate.py` — Fixed Evaluation (Never Modified)
The measurement function. Outputs the metric value to stdout. The agent reads this output — it cannot change how it's measured.

---

## The Experiment Loop

Run: `python scripts/run_experiment.py --loop`

```
LOOP FOREVER:

1. Read program.md for current strategy
2. Review git history: what has been tried? What worked?
3. Propose ONE change to the target file
4. Apply the change
5. git commit (with descriptive message)
6. Run evaluation: python evaluate.py > run.log 2>&1
7. Parse metric from run.log
8. If metric improved → ADVANCE (keep commit, log "keep")
9. If metric equal/worse → REVERT (git reset, log "discard")
10. If crash → attempt fix, if unfixable log "crash" and revert
11. Update results.tsv
12. Go to 1
```

### Rules (from Karpathy's original)

- **NEVER STOP** — once the loop starts, do not ask the human if you should continue. They may be asleep. Run until manually interrupted.
- **Simplicity criterion** — a small improvement that adds ugly complexity is not worth it. Removing code and getting equal results is a win.
- **One change per experiment** — don't change 5 things at once. You won't know what worked.
- **Crash = discard** — OOM, error, timeout → log "crash", revert, move on.
- **Time limit** — if run exceeds 2.5× the time budget, kill it and treat as crash.
- **No new dependencies** — only use what's already available.

---

## Results Log

`results.tsv` (tab-separated, not git-tracked):

```
commit  metric  status  description
a1b2c3d 0.9979  keep    baseline
b2c3d4e 0.9932  keep    increased learning rate
c3d4e5f 1.0050  discard switched to GeLU (worse)
d4e5f6g 0.0000  crash   doubled model width (OOM)
```

Run `python scripts/log_results.py --summary` for a visual summary.

---

## Domain-Specific Configurations

### ML Training (Karpathy-style)
```yaml
target: train.py
evaluate: uv run prepare.py --eval-only
metric: val_bpb (lower is better)
time_budget: 5m
git_branch: autoresearch/{date}-{tag}
```

### Prompt Engineering
```yaml
target: prompt.md
evaluate: python evaluate.py --model gpt-4o --test-cases tests/
metric: eval_score (0-100, higher is better)
time_budget: 2m
git_branch: prompt-research/{date}
```

### Code Performance
```yaml
target: src/hot_module.py
evaluate: python benchmark.py --runs 5 --warmup 1
metric: p50_ms (lower is better)
time_budget: 10m
git_branch: perf-research/{date}
```

### Agent Skill Optimization
```yaml
target: SKILL.md
evaluate: python scripts/skill_evaluator.py --task-suite tests/
metric: pass_rate (0-1, higher is better)
time_budget: 5m
git_branch: skill-research/{date}
```

See `references/experiment-domains.md` for full setup guides per domain.

---

## Scripts

| Script | Purpose |
|--------|---------|
| `setup_experiment.py` | Initialize a new research run: create branch, verify setup, baseline run |
| `run_experiment.py` | Execute the autonomous loop (single run or `--loop` for infinite) |
| `log_results.py` | Record results to TSV; `--summary` prints progress table |

---

## Installation

### One-liner (any tool)
```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cp -r claude-skills/engineering/autoresearch-agent ~/.claude/skills/
```

### Multi-tool install
```bash
# Clone the repo, then use the convert script for your tool:
./scripts/convert.sh --skill autoresearch-agent --tool codex|gemini|cursor|windsurf|openclaw
```

### OpenClaw
```bash
clawhub install autoresearch-agent
```

---

## Proactive Triggers

Flag these issues without being asked:

- **No `evaluate.py` exists** → Experiment can't run. Offer to create one from a template.
- **Target file has no git history** → `git init` and commit baseline first.
- **Metric direction unclear** → Ask: is lower or higher better? Agent must know before starting.
- **Time budget too short** → If evaluation takes longer than budget, experiments will always crash.
- **`results.tsv` in `.gitignore`** → It shouldn't be. The log must persist across sessions.
- **Agent modifying `evaluate.py`** → Hard stop. This invalidates all comparisons.

---

## Related Skills

- **self-improving-agent**: Use when improving an agent's own memory/rules over time. NOT for structured experiment loops with metrics.
- **senior-ml-engineer**: Use for ML architecture decisions and training setup. NOT for autonomous overnight loops.
- **skill-security-auditor**: Use to audit skills before publishing. NOT for optimization loops.
- **tdd-guide**: Use when you want tests to drive development. Complementary — can use tests as the evaluation function.
