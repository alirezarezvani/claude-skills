#!/usr/bin/env python3
"""
autoresearch-agent: Experiment Runner

Executes the autonomous experiment loop:
- Reads .autoresearch.cfg for project config
- Runs the target evaluation
- Keeps improvements (git commit) or discards failures (git reset)
- Logs everything to results.tsv
- Loops indefinitely until interrupted

Usage:
    python scripts/run_experiment.py --loop      # Run forever
    python scripts/run_experiment.py --single    # Run one experiment
    python scripts/run_experiment.py --dry-run   # Show what would happen
"""

import argparse
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def load_config(path):
    """Load .autoresearch.cfg"""
    cfg_file = Path(path) / ".autoresearch.cfg"
    if not cfg_file.exists():
        print("✗ No .autoresearch.cfg found. Run setup_experiment.py first.")
        sys.exit(1)
    config = {}
    for line in cfg_file.read_text().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            config[k.strip()] = v.strip()
    return config


def run_cmd(cmd, cwd=None, timeout=None):
    """Run shell command, return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        cwd=cwd, timeout=timeout
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def get_current_commit(path):
    _, commit, _ = run_cmd("git rev-parse --short HEAD", cwd=path)
    return commit


def get_current_metric(path, metric_grep):
    """Read the last recorded metric from results.tsv."""
    tsv = Path(path) / "results.tsv"
    if not tsv.exists():
        return None
    lines = [l for l in tsv.read_text().splitlines() if "\tkeep\t" in l]
    if not lines:
        return None
    last = lines[-1].split("\t")
    try:
        return float(last[1])
    except (ValueError, IndexError):
        return None


def run_evaluation(path, evaluate_cmd, time_budget_minutes):
    """Run evaluation with time limit."""
    hard_limit = time_budget_minutes * 60 * 2.5  # 2.5x as hard timeout
    t0 = time.time()
    try:
        code, _, _ = run_cmd(
            f"{evaluate_cmd} > run.log 2>&1",
            cwd=path,
            timeout=hard_limit
        )
        elapsed = time.time() - t0
        return code, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        return -1, elapsed  # -1 = timeout


def extract_metric(path, metric_grep):
    """Extract metric value from run.log."""
    code, out, _ = run_cmd(
        f"grep '{metric_grep}' run.log | tail -1",
        cwd=path
    )
    if not out:
        return None
    try:
        return float(out.split(":")[-1].strip())
    except ValueError:
        return None


def is_improvement(new_val, old_val, direction):
    """Check if new result is better than old."""
    if old_val is None:
        return True  # First run always "improves"
    if direction == "lower":
        return new_val < old_val
    else:
        return new_val > old_val


def log_result(path, commit, metric_val, status, description):
    """Append result to results.tsv."""
    tsv = Path(path) / "results.tsv"
    metric_str = f"{metric_val:.6f}" if metric_val is not None else "0.000000"
    with open(tsv, "a") as f:
        f.write(f"{commit}\t{metric_str}\t{status}\t{description}\n")


def get_experiment_count(path):
    """Count experiments run so far."""
    tsv = Path(path) / "results.tsv"
    if not tsv.exists():
        return 0
    lines = tsv.read_text().splitlines()
    return max(0, len(lines) - 1)  # subtract header


def run_single_experiment(path, config, exp_num, dry_run=False):
    """Run one experiment iteration."""
    direction = config.get("metric_direction", "lower")
    metric_grep = config.get("metric_grep", "^metric:")
    evaluate_cmd = config.get("evaluate_cmd", "python evaluate.py")
    time_budget = int(config.get("time_budget_minutes", 5))
    metric_name = config.get("metric", "metric")

    best_so_far = get_current_metric(path, metric_grep)
    ts = datetime.now().strftime("%H:%M:%S")

    print(f"\n[{ts}] Experiment #{exp_num}")
    print(f"  Best {metric_name} so far: {best_so_far}")

    if dry_run:
        print("  [DRY RUN] Would run evaluation and check metric")
        return "dry_run"

    # Save pre-experiment state for rollback
    code, pre_commit, _ = run_cmd("git rev-parse HEAD", cwd=path)
    if code != 0:
        print("  ✗ Can't get git state. Is this a git repo with commits?")
        return "error"

    # Run evaluation
    print(f"  Running: {evaluate_cmd} (budget: {time_budget} min)")
    ret_code, elapsed = run_evaluation(path, evaluate_cmd, time_budget)

    # Handle timeout
    if ret_code == -1:
        print(f"  ✗ TIMEOUT after {elapsed:.0f}s — discarding")
        run_cmd("git checkout -- .", cwd=path)  # revert uncommitted changes
        # Commit was already made by the agent before evaluation
        run_cmd(f"git reset --hard {pre_commit}", cwd=path)
        curr_commit = get_current_commit(path)
        log_result(path, curr_commit, None, "crash", f"timeout after {elapsed:.0f}s")
        return "crash"

    # Handle non-zero exit
    if ret_code != 0:
        # Check if it crashed
        code, tail, _ = run_cmd("tail -n 5 run.log", cwd=path)
        print(f"  ✗ CRASH (exit {ret_code}) after {elapsed:.0f}s")
        print(f"  Last output: {tail[:200]}")
        run_cmd(f"git reset --hard {pre_commit}", cwd=path)
        curr_commit = get_current_commit(path)
        log_result(path, curr_commit, None, "crash", f"exit_code_{ret_code}")
        return "crash"

    # Extract metric
    metric_val = extract_metric(path, metric_grep)
    if metric_val is None:
        print(f"  ✗ Could not parse metric from run.log")
        run_cmd(f"git reset --hard {pre_commit}", cwd=path)
        curr_commit = get_current_commit(path)
        log_result(path, curr_commit, None, "crash", "metric_parse_failed")
        return "crash"

    curr_commit = get_current_commit(path)
    delta = ""
    if best_so_far is not None:
        diff = metric_val - best_so_far
        delta = f" (Δ{diff:+.4f})"

    print(f"  {metric_name}: {metric_val:.6f}{delta} in {elapsed:.0f}s")

    # Keep or discard
    if is_improvement(metric_val, best_so_far, direction):
        print(f"  ✅ KEEP — improvement confirmed")
        log_result(path, curr_commit, metric_val, "keep",
                   f"improvement_{metric_name}_{metric_val:.4f}")
        return "keep"
    else:
        print(f"  ❌ DISCARD — no improvement")
        run_cmd(f"git reset --hard {pre_commit}", cwd=path)
        curr_commit = get_current_commit(path)
        log_result(path, curr_commit, metric_val, "discard",
                   f"no_improvement_{metric_val:.4f}_vs_{best_so_far:.4f}")
        return "discard"


def print_summary(path):
    """Print experiment summary."""
    tsv = Path(path) / "results.tsv"
    if not tsv.exists():
        return
    lines = tsv.read_text().splitlines()[1:]  # skip header
    if not lines:
        return

    keeps = [l for l in lines if "\tkeep\t" in l]
    discards = [l for l in lines if "\tdiscard\t" in l]
    crashes = [l for l in lines if "\tcrash\t" in l]

    print(f"\n{'='*50}")
    print(f"  Session Summary")
    print(f"  Experiments: {len(lines)} total")
    print(f"  ✅ Keep: {len(keeps)} | ❌ Discard: {len(discards)} | 💥 Crash: {len(crashes)}")

    if keeps:
        try:
            first_metric = float(keeps[0].split("\t")[1])
            last_metric = float(keeps[-1].split("\t")[1])
            direction = "↓" if last_metric < first_metric else "↑"
            print(f"  Best progress: {first_metric:.6f} → {last_metric:.6f} {direction}")
        except (ValueError, IndexError):
            pass
    print(f"{'='*50}\n")


def main():
    parser = argparse.ArgumentParser(description="autoresearch-agent runner")
    parser.add_argument("--loop", action="store_true", help="Run forever")
    parser.add_argument("--single", action="store_true", help="Run one experiment")
    parser.add_argument("--dry-run", action="store_true", help="Dry run only")
    parser.add_argument("--path", default=".", help="Project root")
    parser.add_argument("--max-experiments", type=int, default=0,
                        help="Max experiments (0 = unlimited)")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    config = load_config(path)

    print(f"\n🔬 autoresearch-agent")
    print(f"   Project: {path}")
    print(f"   Target: {config.get('target', '?')}")
    print(f"   Metric: {config.get('metric', '?')} ({config.get('metric_direction', '?')} is better)")
    print(f"   Budget: {config.get('time_budget_minutes', '?')} min/experiment")
    print(f"   Mode: {'loop' if args.loop else 'single'}")

    if args.single:
        exp_num = get_experiment_count(path) + 1
        run_single_experiment(path, config, exp_num, args.dry_run)
        return

    if not args.loop and not args.dry_run:
        print("\nSpecify --loop (forever) or --single (one experiment)")
        sys.exit(1)

    # Setup graceful shutdown
    def handle_interrupt(sig, frame):
        print_summary(path)
        print("\n⏹ Stopped by user.")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)

    # Main loop
    consecutive_crashes = 0
    exp_num = get_experiment_count(path) + 1

    print(f"\nStarting loop. Ctrl+C to stop and print summary.\n")

    while True:
        result = run_single_experiment(path, config, exp_num, args.dry_run)
        exp_num += 1

        if result == "crash":
            consecutive_crashes += 1
        else:
            consecutive_crashes = 0

        # Bail if 5 consecutive crashes
        if consecutive_crashes >= 5:
            print("\n⚠ 5 consecutive crashes. Pausing for investigation.")
            print("  Check run.log for the last error.")
            break

        # Check max experiments
        if args.max_experiments > 0 and exp_num > args.max_experiments:
            print(f"\n✓ Reached max experiments ({args.max_experiments})")
            break

        if args.single:
            break

    print_summary(path)


if __name__ == "__main__":
    main()
