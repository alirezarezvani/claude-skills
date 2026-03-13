# Autoresearch Agent — Claude Code Instructions

This plugin runs autonomous experiment loops that optimize any file by a measurable metric.

## Commands

Use the `/ar:` namespace for all commands:

- `/ar:setup` — Set up a new experiment interactively
- `/ar:run` — Run a single experiment iteration
- `/ar:loop` — Start an autonomous loop with user-selected interval
- `/ar:status` — Show dashboard and results
- `/ar:resume` — Resume a paused experiment

## How it works

You (the AI agent) are the experiment loop. The scripts handle evaluation and git rollback.

1. You edit the target file with ONE change
2. You commit it
3. You call `run_experiment.py --single` — it evaluates and prints KEEP/DISCARD/CRASH
4. You repeat

Results persist in `results.tsv` and git log. Sessions can be resumed.

## When to use each command

### Starting fresh
```
/ar:setup
```
Creates the experiment directory, config, program.md, results.tsv, and git branch.

### Running one iteration at a time
```
/ar:run engineering/api-speed
```
Read history, make one change, evaluate, report result.

### Autonomous background loop
```
/ar:loop engineering/api-speed
```
Prompts for interval (10min, 1h, daily, weekly, monthly), then creates a recurring job.

### Checking progress
```
/ar:status
```
Shows the dashboard across all experiments with metrics and trends.

### Resuming after context limit or break
```
/ar:resume engineering/api-speed
```
Reads results history, checks out the branch, and continues where you left off.

## Agents

- **experiment-runner**: Spawned for each loop iteration. Reads config, results history, decides what to try, edits target, commits, evaluates.

## Key principle

**One change per experiment. Measure everything. Compound improvements.**

The agent never modifies the evaluator. The evaluator is ground truth.
