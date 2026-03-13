#!/usr/bin/env python3
"""
autoresearch-agent: Setup Wizard

Initializes a new research run:
1. Validates the project structure
2. Creates a git branch
3. Runs the baseline experiment
4. Initializes results.tsv

Usage:
    python scripts/setup_experiment.py [--config experiment.yaml]
    python scripts/setup_experiment.py --domain ml|prompt|code|skill
"""

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


DOMAINS = {
    "ml": {
        "target": "train.py",
        "evaluate_cmd": "uv run train.py",
        "metric": "val_bpb",
        "metric_direction": "lower",
        "time_budget_minutes": 5,
        "metric_grep": "^val_bpb:",
    },
    "prompt": {
        "target": "prompt.md",
        "evaluate_cmd": "python evaluate.py",
        "metric": "eval_score",
        "metric_direction": "higher",
        "time_budget_minutes": 2,
        "metric_grep": "^eval_score:",
    },
    "code": {
        "target": "src/module.py",
        "evaluate_cmd": "python benchmark.py",
        "metric": "p50_ms",
        "metric_direction": "lower",
        "time_budget_minutes": 10,
        "metric_grep": "^p50_ms:",
    },
    "skill": {
        "target": "SKILL.md",
        "evaluate_cmd": "python scripts/skill_evaluator.py",
        "metric": "pass_rate",
        "metric_direction": "higher",
        "time_budget_minutes": 5,
        "metric_grep": "^pass_rate:",
    },
}


def run_cmd(cmd, cwd=None, timeout=None):
    """Run a shell command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        cmd, shell=True, capture_output=True, text=True,
        cwd=cwd, timeout=timeout
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check_git_repo(path):
    """Verify we're in a git repo."""
    code, out, err = run_cmd("git rev-parse --is-inside-work-tree", cwd=path)
    if code != 0:
        print("✗ Not a git repository. Run: git init && git add . && git commit -m 'initial'")
        return False
    print("✓ Git repository found")
    return True


def check_program_md(path):
    """Check program.md exists and has content."""
    pm = Path(path) / "program.md"
    if not pm.exists():
        print("⚠ program.md not found. Creating template...")
        return False
    content = pm.read_text()
    if len(content) < 100:
        print("⚠ program.md looks empty. Fill it out before running experiments.")
        return False
    print(f"✓ program.md found ({len(content)} chars)")
    return True


def check_target_file(path, target):
    """Check target file exists."""
    tf = Path(path) / target
    if not tf.exists():
        print(f"✗ Target file not found: {target}")
        return False
    print(f"✓ Target file found: {target}")
    return True


def check_evaluate_script(path):
    """Check evaluate.py exists."""
    ev = Path(path) / "evaluate.py"
    if not ev.exists():
        print("⚠ evaluate.py not found. You need a fixed evaluation function.")
        print("  Create evaluate.py that outputs: metric_name: <value>")
        return False
    print("✓ evaluate.py found")
    return True


def create_branch(path, tag):
    """Create and checkout the experiment branch."""
    branch = f"autoresearch/{tag}"
    code, out, err = run_cmd(f"git checkout -b {branch}", cwd=path)
    if code != 0:
        if "already exists" in err:
            print(f"✗ Branch '{branch}' already exists. Use a different tag.")
        else:
            print(f"✗ Failed to create branch: {err}")
        return None
    print(f"✓ Created branch: {branch}")
    return branch


def init_results_tsv(path):
    """Create results.tsv with header."""
    tsv = Path(path) / "results.tsv"
    if tsv.exists():
        print(f"✓ results.tsv already exists ({tsv.stat().st_size} bytes)")
        return
    tsv.write_text("commit\tmetric\tstatus\tdescription\n")
    print("✓ Created results.tsv")


def run_baseline(path, evaluate_cmd, metric_grep, time_budget_minutes):
    """Run the baseline experiment."""
    print(f"\nRunning baseline experiment (~{time_budget_minutes} min)...")
    timeout = time_budget_minutes * 60 * 2.5  # 2.5x budget as hard limit

    t0 = time.time()
    code, out, err = run_cmd(
        f"{evaluate_cmd} > run.log 2>&1",
        cwd=path,
        timeout=timeout
    )
    elapsed = time.time() - t0

    if code != 0:
        print(f"✗ Baseline run failed after {elapsed:.0f}s. Check run.log")
        return None

    # Extract metric
    grep_code, grep_out, _ = run_cmd(
        f"grep '{metric_grep}' run.log | tail -1",
        cwd=path
    )
    if not grep_out:
        print("✗ Could not extract metric from run.log. Check metric_grep pattern.")
        return None

    metric_value = grep_out.split(":")[-1].strip()
    print(f"✓ Baseline complete in {elapsed:.0f}s — metric: {metric_value}")
    return metric_value


def main():
    parser = argparse.ArgumentParser(description="autoresearch-agent setup")
    parser.add_argument("--domain", choices=list(DOMAINS.keys()), help="Experiment domain")
    parser.add_argument("--target", help="Target file to optimize")
    parser.add_argument("--evaluate-cmd", help="Evaluation command")
    parser.add_argument("--metric", help="Metric name")
    parser.add_argument("--direction", choices=["lower", "higher"], default="lower")
    parser.add_argument("--budget", type=int, default=5, help="Time budget in minutes")
    parser.add_argument("--tag", help="Run tag (used in branch name)")
    parser.add_argument("--path", default=".", help="Project root path")
    parser.add_argument("--skip-baseline", action="store_true")
    args = parser.parse_args()

    path = Path(args.path).resolve()
    print(f"\n🔬 autoresearch-agent setup")
    print(f"   Project: {path}")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # Get config from domain or args
    if args.domain:
        config = DOMAINS[args.domain].copy()
    else:
        config = {
            "target": args.target or "target.py",
            "evaluate_cmd": args.evaluate_cmd or "python evaluate.py",
            "metric": args.metric or "score",
            "metric_direction": args.direction,
            "time_budget_minutes": args.budget,
            "metric_grep": f"^{args.metric or 'score'}:",
        }

    tag = args.tag or datetime.now().strftime("%b%d").lower()

    # Validation checks
    checks = [
        check_git_repo(path),
        check_program_md(path),
        check_target_file(path, config["target"]),
        check_evaluate_script(path),
    ]

    if not all(checks):
        print("\n⚠ Fix the above issues before running experiments.")
        sys.exit(1)

    # Create branch
    branch = create_branch(path, tag)
    if not branch:
        sys.exit(1)

    # Init results TSV
    init_results_tsv(path)

    # Save config for run_experiment.py
    config_content = "\n".join(f"{k}: {v}" for k, v in config.items())
    (path / ".autoresearch.cfg").write_text(config_content + "\n")
    print("✓ Saved .autoresearch.cfg")

    # Run baseline
    if not args.skip_baseline:
        baseline = run_baseline(
            path,
            config["evaluate_cmd"],
            config["metric_grep"],
            config["time_budget_minutes"]
        )
        if baseline:
            # Log baseline to TSV
            code, commit, _ = run_cmd("git rev-parse --short HEAD", cwd=path)
            with open(path / "results.tsv", "a") as f:
                f.write(f"{commit}\t{baseline}\tkeep\tbaseline\n")
            print(f"✓ Baseline logged to results.tsv")

    print(f"\n✅ Setup complete!")
    print(f"   Branch: {branch}")
    print(f"   Target: {config['target']}")
    print(f"   Metric: {config['metric']} ({config['metric_direction']} is better)")
    print(f"   Budget: {config['time_budget_minutes']} min/experiment")
    print(f"\nTo start the autonomous loop:")
    print(f"   python scripts/run_experiment.py --loop")
    print(f"\nOr run a single experiment:")
    print(f"   python scripts/run_experiment.py --single")


if __name__ == "__main__":
    main()
