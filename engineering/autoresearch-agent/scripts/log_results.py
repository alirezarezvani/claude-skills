#!/usr/bin/env python3
"""
autoresearch-agent: Results Logger

View and analyze experiment results from results.tsv.

Usage:
    python scripts/log_results.py --summary          # Print progress table
    python scripts/log_results.py --best             # Show best result
    python scripts/log_results.py --history          # Full experiment history
    python scripts/log_results.py --record commit val status desc  # Add entry manually
"""

import argparse
import sys
from pathlib import Path


def load_results(path):
    tsv = Path(path) / "results.tsv"
    if not tsv.exists():
        return []
    lines = tsv.read_text().splitlines()[1:]  # skip header
    results = []
    for line in lines:
        parts = line.split("\t")
        if len(parts) >= 4:
            results.append({
                "commit": parts[0],
                "metric": float(parts[1]) if parts[1] != "0.000000" else None,
                "status": parts[2],
                "description": parts[3]
            })
    return results


def print_summary(results, metric_name="metric", direction="lower"):
    if not results:
        print("No experiments logged yet.")
        return

    keeps = [r for r in results if r["status"] == "keep"]
    discards = [r for r in results if r["status"] == "discard"]
    crashes = [r for r in results if r["status"] == "crash"]

    print(f"\n{'─'*60}")
    print(f"  autoresearch-agent — Results Summary")
    print(f"{'─'*60}")
    print(f"  Total experiments: {len(results)}")
    print(f"  ✅ Keep:    {len(keeps):3d} ({len(keeps)/max(len(results),1)*100:.0f}%)")
    print(f"  ❌ Discard: {len(discards):3d} ({len(discards)/max(len(results),1)*100:.0f}%)")
    print(f"  💥 Crash:   {len(crashes):3d} ({len(crashes)/max(len(results),1)*100:.0f}%)")

    if keeps:
        valid = [r for r in keeps if r["metric"] is not None]
        if valid:
            baseline = valid[0]["metric"]
            best = min(r["metric"] for r in valid) if direction == "lower" else max(r["metric"] for r in valid)
            best_run = next(r for r in valid if r["metric"] == best)
            improvement = ((baseline - best) / baseline * 100) if direction == "lower" else ((best - baseline) / baseline * 100)

            print(f"\n  {metric_name}:")
            print(f"    Baseline: {baseline:.6f}")
            print(f"    Best:     {best:.6f}  (commit: {best_run['commit']})")
            print(f"    Change:   {improvement:+.2f}%")

    print(f"{'─'*60}\n")


def print_history(results):
    if not results:
        print("No experiments logged yet.")
        return

    print(f"\n{'COMMIT':8} {'METRIC':10} {'STATUS':8} DESCRIPTION")
    print("─" * 60)
    for r in results:
        metric_str = f"{r['metric']:.6f}" if r['metric'] is not None else "crash   "
        status_icon = {"keep": "✅", "discard": "❌", "crash": "💥"}.get(r["status"], "?")
        print(f"{r['commit']:8} {metric_str:10} {status_icon} {r['description'][:40]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--best", action="store_true")
    parser.add_argument("--history", action="store_true")
    parser.add_argument("--record", nargs=4, metavar=("COMMIT", "METRIC", "STATUS", "DESC"))
    parser.add_argument("--path", default=".")
    parser.add_argument("--metric", default="metric")
    parser.add_argument("--direction", default="lower", choices=["lower", "higher"])
    args = parser.parse_args()

    path = Path(args.path).resolve()

    if args.record:
        commit, metric, status, desc = args.record
        tsv = path / "results.tsv"
        if not tsv.exists():
            tsv.write_text("commit\tmetric\tstatus\tdescription\n")
        with open(tsv, "a") as f:
            f.write(f"{commit}\t{metric}\t{status}\t{desc}\n")
        print(f"✓ Logged: {commit} {metric} {status}")
        return

    results = load_results(path)

    if args.history:
        print_history(results)
    elif args.best:
        keeps = [r for r in results if r["status"] == "keep" and r["metric"]]
        if not keeps:
            print("No successful experiments yet.")
            return
        best = min(keeps, key=lambda r: r["metric"]) if args.direction == "lower" else max(keeps, key=lambda r: r["metric"])
        print(f"Best: {best['metric']:.6f} (commit: {best['commit']}) — {best['description']}")
    else:
        print_summary(results, args.metric, args.direction)


if __name__ == "__main__":
    main()
