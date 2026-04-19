#!/usr/bin/env python3
"""Measure build/compile time.
DO NOT MODIFY after experiment starts — this is the fixed evaluator."""

import subprocess
import sys
import time

# --- CONFIGURE THESE ---
BUILD_CMD = "npm run build"    # or: docker build -t test .
CLEAN_CMD = ""                 # optional: npm run clean (run before each build)
RUNS = 3                       # Number of builds to average
# --- END CONFIG ---

times = []

for i in range(RUNS):
    # Clean if configured
    if CLEAN_CMD:
        subprocess.run(CLEAN_CMD, shell=True, capture_output=True, timeout=60)

    t0 = time.perf_counter()
    result = subprocess.run(BUILD_CMD, shell=True, capture_output=True, timeout=600)
    elapsed = time.perf_counter() - t0

    if result.returncode != 0:
        print(f"Build {i+1} failed (exit {result.returncode})", file=sys.stderr)
        print(f"stderr: {result.stderr.decode()[:200]}", file=sys.stderr)
        sys.exit(1)

    times.append(elapsed)

import statistics
avg = statistics.mean(times)
median = statistics.median(times)

print(f"build_seconds: {median:.2f}")
print(f"build_avg: {avg:.2f}")
print(f"runs: {RUNS}")
