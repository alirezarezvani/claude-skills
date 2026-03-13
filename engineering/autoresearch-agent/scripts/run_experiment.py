#!/usr/bin/env python3
"""
autoresearch-agent: Experiment Runner

Executes the autonomous experiment loop for a specific experiment.
Reads config from .autoresearch/{domain}/{name}/config.cfg.

Usage:
    python scripts/run_experiment.py --experiment engineering/api-speed --loop
    python scripts/run_experiment.py --experiment engineering/api-speed --single
    python scripts/run_experiment.py --experiment marketing/medium-ctr --loop
    python scripts/run_experiment.py --resume --loop
    python scripts/run_experiment.py --experiment engineering/api-speed --dry-run
"""

import argparse
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def find_autoresearch_root():
    """Find .autoresearch/ in project or user home."""
    project_root = Path(".").resolve() / ".autoresearch"
    if project_root.exists():
        return project_root
    user_root = Path.home() / ".autoresearch"
    if user_root.exists():
        return user_root
    return None


def load_config(experiment_dir):
    """Load config.cfg from experiment directory."""
    cfg_file = experiment_dir / "config.cfg"
    if not cfg_file.exists():
        print(f"  Error: no config.cfg in {experiment_dir}")
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
    """Get short hash of current HEAD."""
    _, commit, _ = run_cmd("git rev-parse --short HEAD", cwd=path)
    return commit


def get_best_metric(experiment_dir, direction):
    """Read the best metric from results.tsv."""
    tsv = experiment_dir / "results.tsv"
    if not tsv.exists():
        return None
    lines = [l for l in tsv.read_text().splitlines()[1:] if "\tkeep\t" in l]
    if not lines:
        return None
    metrics = []
    for line in lines:
        parts = line.split("\t")
        try:
            if parts[1] != "N/A":
                metrics.append(float(parts[1]))
        except (ValueError, IndexError):
            continue
    if not metrics:
        return None
    return min(metrics) if direction == "lower" else max(metrics)


def run_evaluation(project_root, eval_cmd, time_budget_minutes, log_file):
    """Run evaluation with time limit. Output goes to log_file."""
    hard_limit = time_budget_minutes * 60 * 2.5
    t0 = time.time()
    try:
        code, _, _ = run_cmd(
            f"{eval_cmd} > {log_file} 2>&1",
            cwd=str(project_root),
            timeout=hard_limit
        )
        elapsed = time.time() - t0
        return code, elapsed
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        return -1, elapsed


def extract_metric(log_file, metric_grep):
    """Extract metric value from log file."""
    log_path = Path(log_file)
    if not log_path.exists():
        return None
    for line in reversed(log_path.read_text().splitlines()):
        stripped = line.strip()
        if stripped.startswith(metric_grep.lstrip("^")):
            try:
                return float(stripped.split(":")[-1].strip())
            except ValueError:
                continue
    return None


def is_improvement(new_val, old_val, direction):
    """Check if new result is better than old."""
    if old_val is None:
        return True
    if direction == "lower":
        return new_val < old_val
    return new_val > old_val


def log_result(experiment_dir, commit, metric_val, status, description):
    """Append result to results.tsv."""
    tsv = experiment_dir / "results.tsv"
    metric_str = f"{metric_val:.6f}" if metric_val is not None else "N/A"
    with open(tsv, "a") as f:
        f.write(f"{commit}\t{metric_str}\t{status}\t{description}\n")


def get_experiment_count(experiment_dir):
    """Count experiments run so far."""
    tsv = experiment_dir / "results.tsv"
    if not tsv.exists():
        return 0
    return max(0, len(tsv.read_text().splitlines()) - 1)


def get_last_active(root):
    """Find the most recently modified experiment."""
    latest = None
    latest_time = 0
    for domain_dir in root.iterdir():
        if not domain_dir.is_dir() or domain_dir.name.startswith("."):
            continue
        for exp_dir in domain_dir.iterdir():
            if not exp_dir.is_dir():
                continue
            cfg = exp_dir / "config.cfg"
            if cfg.exists() and cfg.stat().st_mtime > latest_time:
                latest_time = cfg.stat().st_mtime
                latest = f"{domain_dir.name}/{exp_dir.name}"
    return latest


def run_single(project_root, experiment_dir, config, exp_num, dry_run=False):
    """Run one experiment iteration."""
    direction = config.get("metric_direction", "lower")
    metric_grep = config.get("metric_grep", "^metric:")
    eval_cmd = config.get("evaluate_cmd", "python evaluate.py")
    time_budget = int(config.get("time_budget_minutes", 5))
    metric_name = config.get("metric", "metric")
    log_file = str(experiment_dir / "run.log")

    best = get_best_metric(experiment_dir, direction)
    ts = datetime.now().strftime("%H:%M:%S")

    print(f"\n[{ts}] Experiment #{exp_num}")
    print(f"  Best {metric_name}: {best}")

    if dry_run:
        print("  [DRY RUN] Would run evaluation and check metric")
        return "dry_run"

    # Save state for rollback
    code, pre_commit, _ = run_cmd("git rev-parse HEAD", cwd=str(project_root))
    if code != 0:
        print("  Error: can't get git state")
        return "error"

    # Run evaluation
    print(f"  Running: {eval_cmd} (budget: {time_budget}m)")
    ret_code, elapsed = run_evaluation(project_root, eval_cmd, time_budget, log_file)

    commit = get_current_commit(str(project_root))

    # Timeout
    if ret_code == -1:
        print(f"  TIMEOUT after {elapsed:.0f}s — discarding")
        run_cmd("git checkout -- .", cwd=str(project_root))
        run_cmd(f"git reset --hard {pre_commit}", cwd=str(project_root))
        log_result(experiment_dir, commit, None, "crash", f"timeout_{elapsed:.0f}s")
        return "crash"

    # Crash
    if ret_code != 0:
        _, tail, _ = run_cmd(f"tail -5 {log_file}", cwd=str(project_root))
        print(f"  CRASH (exit {ret_code}) after {elapsed:.0f}s")
        print(f"  Last output: {tail[:200]}")
        run_cmd(f"git reset --hard {pre_commit}", cwd=str(project_root))
        log_result(experiment_dir, commit, None, "crash", f"exit_{ret_code}")
        return "crash"

    # Extract metric
    metric_val = extract_metric(log_file, metric_grep)
    if metric_val is None:
        print(f"  Could not parse {metric_name} from run.log")
        run_cmd(f"git reset --hard {pre_commit}", cwd=str(project_root))
        log_result(experiment_dir, commit, None, "crash", "metric_parse_failed")
        return "crash"

    delta = ""
    if best is not None:
        diff = metric_val - best
        delta = f" (delta {diff:+.4f})"

    print(f"  {metric_name}: {metric_val:.6f}{delta} in {elapsed:.0f}s")

    # Keep or discard
    if is_improvement(metric_val, best, direction):
        print(f"  KEEP — improvement")
        log_result(experiment_dir, commit, metric_val, "keep",
                   f"improved_{metric_name}_{metric_val:.4f}")
        return "keep"
    else:
        print(f"  DISCARD — no improvement")
        run_cmd(f"git reset --hard {pre_commit}", cwd=str(project_root))
        best_str = f"{best:.4f}" if best else "?"
        log_result(experiment_dir, commit, metric_val, "discard",
                   f"no_improvement_{metric_val:.4f}_vs_{best_str}")
        return "discard"


def print_summary(experiment_dir, config):
    """Print session summary."""
    tsv = experiment_dir / "results.tsv"
    if not tsv.exists():
        return
    lines = tsv.read_text().splitlines()[1:]
    if not lines:
        return

    keeps = [l for l in lines if "\tkeep\t" in l]
    discards = [l for l in lines if "\tdiscard\t" in l]
    crashes = [l for l in lines if "\tcrash\t" in l]
    metric_name = config.get("metric", "metric")
    direction = config.get("metric_direction", "lower")

    print(f"\n{'=' * 55}")
    print(f"  autoresearch — Session Summary")
    print(f"  Experiments: {len(lines)} total")
    print(f"  Keep: {len(keeps)} | Discard: {len(discards)} | Crash: {len(crashes)}")

    if keeps:
        try:
            valid = []
            for l in keeps:
                parts = l.split("\t")
                if parts[1] != "N/A":
                    valid.append(float(parts[1]))
            if len(valid) >= 2:
                first, last = valid[0], valid[-1]
                best = min(valid) if direction == "lower" else max(valid)
                pct = ((first - best) / first * 100) if direction == "lower" else ((best - first) / first * 100)
                print(f"  {metric_name}: {first:.6f} -> {best:.6f} ({pct:+.1f}%)")
        except (ValueError, IndexError):
            pass
    print(f"{'=' * 55}\n")


def main():
    parser = argparse.ArgumentParser(description="autoresearch-agent runner")
    parser.add_argument("--experiment", help="Experiment path: domain/name (e.g. engineering/api-speed)")
    parser.add_argument("--resume", action="store_true", help="Resume last active experiment")
    parser.add_argument("--loop", action="store_true", help="Run forever")
    parser.add_argument("--single", action="store_true", help="Run one experiment")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--max-experiments", type=int, default=0, help="Max experiments (0 = unlimited)")
    parser.add_argument("--path", default=".", help="Project root")
    args = parser.parse_args()

    project_root = Path(args.path).resolve()
    root = find_autoresearch_root()

    if root is None:
        print("No .autoresearch/ found. Run setup_experiment.py first.")
        sys.exit(1)

    # Resolve experiment
    experiment_path = args.experiment
    if args.resume:
        experiment_path = get_last_active(root)
        if not experiment_path:
            print("No experiments found to resume.")
            sys.exit(1)
        print(f"Resuming: {experiment_path}")

    if not experiment_path:
        print("Specify --experiment domain/name or --resume")
        sys.exit(1)

    experiment_dir = root / experiment_path
    if not experiment_dir.exists():
        print(f"Experiment not found: {experiment_dir}")
        print("Run: python scripts/setup_experiment.py --list")
        sys.exit(1)

    config = load_config(experiment_dir)

    domain, name = experiment_path.split("/", 1)
    print(f"\n  autoresearch-agent")
    print(f"  Experiment: {experiment_path}")
    print(f"  Target: {config.get('target', '?')}")
    print(f"  Metric: {config.get('metric', '?')} ({config.get('metric_direction', '?')} is better)")
    print(f"  Budget: {config.get('time_budget_minutes', '?')} min/experiment")
    print(f"  Mode: {'loop' if args.loop else 'single'}")

    if args.single or args.dry_run:
        exp_num = get_experiment_count(experiment_dir) + 1
        run_single(project_root, experiment_dir, config, exp_num, args.dry_run)
        return

    if not args.loop:
        print("\nSpecify --loop (forever) or --single (one experiment)")
        sys.exit(1)

    # Graceful shutdown
    def handle_interrupt(sig, frame):
        print_summary(experiment_dir, config)
        print("\nStopped by user.")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)

    consecutive_crashes = 0
    exp_num = get_experiment_count(experiment_dir) + 1

    print(f"\nStarting loop. Ctrl+C to stop.\n")

    while True:
        result = run_single(project_root, experiment_dir, config, exp_num, False)
        exp_num += 1

        if result == "crash":
            consecutive_crashes += 1
        else:
            consecutive_crashes = 0

        if consecutive_crashes >= 5:
            print("\n  5 consecutive crashes. Pausing.")
            print("  Check .autoresearch/{}/run.log".format(experiment_path))
            break

        if 0 < args.max_experiments < exp_num:
            print(f"\n  Reached max experiments ({args.max_experiments})")
            break

    print_summary(experiment_dir, config)


if __name__ == "__main__":
    main()
