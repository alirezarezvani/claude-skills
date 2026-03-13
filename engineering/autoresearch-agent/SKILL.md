---
name: "autoresearch-agent"
description: "Autonomous experiment loop that optimizes any file by a measurable metric. Inspired by Karpathy's autoresearch. The agent edits a target file, runs a fixed evaluation, keeps improvements (git commit), discards failures (git reset), and loops indefinitely. Use when: user wants to optimize code speed, reduce bundle/image size, improve test pass rate, optimize prompts, improve content quality (headlines, copy, CTR), or run any measurable improvement loop. Requires: a target file, an evaluation command that outputs a metric, and a git repo."
license: MIT
metadata:
  version: 2.0.0
  author: Alireza Rezvani
  category: engineering
  updated: 2026-03-13
---

# Autoresearch Agent

> You sleep. The agent experiments. You wake up to results.

Autonomous experiment loop inspired by [Karpathy's autoresearch](https://github.com/karpathy/autoresearch). The agent edits one file, runs a fixed evaluation, keeps improvements, discards failures, and loops indefinitely.

Not one guess — fifty measured attempts, compounding.

---

## When This Skill Activates

Recognize these patterns from the user:

- "Make this faster / smaller / better"
- "Optimize [file] for [metric]"
- "Improve my [headlines / copy / prompts]"
- "Run experiments overnight"
- "I want to get [metric] from X to Y"
- Any request involving: optimize, benchmark, improve, experiment loop, autoresearch

If the user describes a target file + a way to measure success → this skill applies.

---

## Setup

### First Time — Create the Experiment

Run the setup script. The user decides where experiments live:

**Project-level** (inside repo, git-tracked, shareable with team):
```bash
python scripts/setup_experiment.py \
  --domain engineering \
  --name api-speed \
  --target src/api/search.py \
  --eval "pytest bench.py --tb=no -q" \
  --metric p50_ms \
  --direction lower \
  --scope project
```

**User-level** (personal, in `~/.autoresearch/`):
```bash
python scripts/setup_experiment.py \
  --domain marketing \
  --name medium-ctr \
  --target content/titles.md \
  --eval "python evaluate.py" \
  --metric ctr_score \
  --direction higher \
  --evaluator llm_judge_content \
  --scope user
```

The `--scope` flag determines where `.autoresearch/` lives:
- `project` (default) → `.autoresearch/` in the repo root. Experiment definitions are git-tracked. Results are gitignored.
- `user` → `~/.autoresearch/` in the home directory. Everything is personal.

### What Setup Creates

```
.autoresearch/
├── config.yaml                        ← Global settings
├── .gitignore                         ← Ignores results.tsv, *.log
└── {domain}/{experiment-name}/
    ├── program.md                     ← Objectives, constraints, strategy
    ├── config.cfg                     ← Target, eval cmd, metric, direction
    ├── results.tsv                    ← Experiment log (gitignored)
    └── evaluate.py                    ← Evaluation script (if --evaluator used)
```

### Domains

| Domain | Use Cases |
|--------|-----------|
| `engineering` | Code speed, memory, bundle size, test pass rate, build time |
| `marketing` | Headlines, social copy, email subjects, ad copy, engagement |
| `content` | Article structure, SEO descriptions, readability, CTR |
| `prompts` | System prompts, chatbot tone, agent instructions |
| `custom` | Anything else with a measurable metric |

### If `program.md` Already Exists

The user may have written their own `program.md`. If found in the experiment directory, read it. It overrides the template. Only ask for what's missing.

---

## The Experiment Loop

### Starting an Experiment

```bash
# Run specific experiment
python scripts/run_experiment.py --experiment engineering/api-speed --loop

# Single iteration (test setup)
python scripts/run_experiment.py --experiment engineering/api-speed --single

# Resume last active experiment
python scripts/run_experiment.py --resume --loop

# Dry run (show what would happen)
python scripts/run_experiment.py --experiment engineering/api-speed --dry-run
```

### The Loop Protocol

```
LOOP FOREVER:

1. Read program.md for current strategy and constraints
2. Review git log: what has been tried? What worked? What crashed?
3. Review results.tsv: current best metric, trend, recent failures
4. Propose ONE change to the target file
5. Apply the change
6. git commit -m "experiment: [short description of what changed]"
7. Run evaluation: {eval_command} > .autoresearch/{domain}/{name}/run.log 2>&1
8. Parse metric from run.log (grep for metric_name: value)
9. Decision:
   - Metric improved → KEEP (advance branch, log "keep")
   - Metric equal or worse → REVERT (git reset --hard, log "discard")
   - Crash/timeout/parse failure → attempt fix once, else REVERT (log "crash")
10. Append result to results.tsv
11. Go to 1
```

### Rules

- **NEVER STOP.** The human may be asleep. Run until manually interrupted. If you run out of ideas, read papers, re-read the target, try combining previous near-misses, try radical changes.
- **One change per experiment.** Don't change 5 things at once. You won't know what worked.
- **Simplicity criterion.** A small improvement that adds ugly complexity is not worth it. Equal performance with simpler code is a win. Removing code that gets same results is the best outcome.
- **Never modify the evaluator.** `evaluate.py` is the ground truth. Modifying it invalidates all comparisons. Hard stop if you catch yourself doing this.
- **Timeout.** If a run exceeds 2.5× the time budget, kill it and treat as crash.
- **Crash handling.** If it's a typo or missing import, fix and re-run. If the idea is fundamentally broken, revert, log "crash", move on. 5 consecutive crashes → pause and alert.
- **No new dependencies.** Only use what's already available in the project.

---

## Evaluators

Ready-to-use evaluation scripts. Copied into the experiment directory during setup with `--evaluator`.

### Free Evaluators (no API cost)

| Evaluator | Metric | Use Case |
|-----------|--------|----------|
| `benchmark_speed` | `p50_ms` (lower) | Function/API execution time |
| `benchmark_size` | `size_bytes` (lower) | File, bundle, Docker image size |
| `test_pass_rate` | `pass_rate` (higher) | Test suite pass percentage |
| `build_speed` | `build_seconds` (lower) | Build/compile/Docker build time |
| `memory_usage` | `peak_mb` (lower) | Peak memory during execution |

### LLM Judge Evaluators (uses your subscription)

| Evaluator | Metric | Use Case |
|-----------|--------|----------|
| `llm_judge_content` | `ctr_score` 0-10 (higher) | Headlines, titles, descriptions |
| `llm_judge_prompt` | `quality_score` 0-100 (higher) | System prompts, agent instructions |
| `llm_judge_copy` | `engagement_score` 0-10 (higher) | Social posts, ad copy, emails |

LLM judges call the CLI tool the user is already running (Claude, Codex, Gemini). The evaluation prompt is locked inside `evaluate.py` — the agent cannot modify it. This prevents the agent from gaming its own evaluator.

The user's existing subscription covers the cost:
- Claude Code Max → unlimited Claude calls for evaluation
- Codex CLI (ChatGPT Pro) → unlimited Codex calls
- Gemini CLI (free tier) → free evaluation calls

### Custom Evaluators

If no built-in evaluator fits, the user writes their own `evaluate.py`. Only requirement: it must print `metric_name: value` to stdout.

```python
#!/usr/bin/env python3
# My custom evaluator — DO NOT MODIFY after experiment starts
import subprocess
result = subprocess.run(["my-benchmark", "--json"], capture_output=True, text=True)
# Parse and output
print(f"my_metric: {parse_score(result.stdout)}")
```

---

## Viewing Results

```bash
# Single experiment
python scripts/log_results.py --experiment engineering/api-speed

# All experiments in a domain
python scripts/log_results.py --domain engineering

# Cross-experiment dashboard
python scripts/log_results.py --dashboard

# Export formats
python scripts/log_results.py --experiment engineering/api-speed --format csv --output results.csv
python scripts/log_results.py --experiment engineering/api-speed --format markdown --output results.md
python scripts/log_results.py --dashboard --format markdown --output dashboard.md
```

### Dashboard Output

```
DOMAIN          EXPERIMENT          RUNS  KEPT  BEST         Δ FROM START  STATUS
engineering     api-speed            47    14   185ms        -76.9%        active
engineering     bundle-size          23     8   412KB        -58.3%        paused
marketing       medium-ctr           31    11   8.4/10       +68.0%        active
prompts         support-tone         15     6   82/100       +46.4%        done
```

### Export Formats

- **TSV** — default, tab-separated (compatible with spreadsheets)
- **CSV** — comma-separated, with proper quoting
- **Markdown** — formatted table, readable in GitHub/docs

---

## Proactive Triggers

Flag these without being asked:

- **No evaluation command works** → Test it before starting the loop. Run once, verify output.
- **Target file not in git** → `git init && git add . && git commit -m 'initial'` first.
- **Metric direction unclear** → Ask: is lower or higher better? Must know before starting.
- **Time budget too short** → If eval takes longer than budget, every run crashes.
- **Agent modifying evaluate.py** → Hard stop. This invalidates all comparisons.
- **5 consecutive crashes** → Pause the loop. Alert the user. Don't keep burning cycles.
- **No improvement in 20+ runs** → Suggest changing strategy in program.md or trying a different approach.

---

## Installation

### One-liner (any tool)
```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cp -r claude-skills/engineering/autoresearch-agent ~/.claude/skills/
```

### Multi-tool install
```bash
./scripts/convert.sh --skill autoresearch-agent --tool codex|gemini|cursor|windsurf|openclaw
```

### OpenClaw
```bash
clawhub install autoresearch-agent
```

---

## Related Skills

- **self-improving-agent** — improves an agent's own memory/rules over time. NOT for structured experiment loops.
- **senior-ml-engineer** — ML architecture decisions. Complementary — use for initial design, then autoresearch for optimization.
- **tdd-guide** — test-driven development. Complementary — tests can be the evaluation function.
- **skill-security-auditor** — audit skills before publishing. NOT for optimization loops.
