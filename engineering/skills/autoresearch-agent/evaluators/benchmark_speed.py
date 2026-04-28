#!/usr/bin/env python3
"""Measure execution speed of a target function or command.
DO NOT MODIFY after experiment starts — this is the fixed evaluator."""

import statistics
import subprocess
import sys
import time

# --- CONFIGURE THESE ---
COMMAND = "python src/module.py"  # Command to benchmark
RUNS = 5                          # Number of runs
WARMUP = 1                        # Warmup runs (not counted)
# --- END CONFIG ---

times = []

# Warmup
for _ in range(WARMUP):
    subprocess.run(COMMAND, shell=True, capture_output=True, timeout=120)

# Benchmark
for i in range(RUNS):
    t0 = time.perf_counter()
    result = subprocess.run(COMMAND, shell=True, capture_output=True, timeout=120)
    elapsed = (time.perf_counter() - t0) * 1000  # ms

    if result.returncode != 0:
        print(f"Run {i+1} failed (exit {result.returncode})", file=sys.stderr)
        print(f"stderr: {result.stderr.decode()[:200]}", file=sys.stderr)
        sys.exit(1)

    times.append(elapsed)

p50 = statistics.median(times)
p95 = sorted(times)[int(len(times) * 0.95)] if len(times) >= 5 else max(times)

print(f"p50_ms: {p50:.2f}")
print(f"p95_ms: {p95:.2f}")
print(f"runs: {RUNS}")
