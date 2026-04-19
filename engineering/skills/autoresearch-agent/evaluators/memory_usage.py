#!/usr/bin/env python3
"""Measure peak memory usage of a command.
DO NOT MODIFY after experiment starts — this is the fixed evaluator."""

import platform
import subprocess
import sys

# --- CONFIGURE THESE ---
COMMAND = "python src/module.py"  # Command to measure
# --- END CONFIG ---

system = platform.system()

if system == "Linux":
    # Use /usr/bin/time for peak RSS
    result = subprocess.run(
        f"/usr/bin/time -v {COMMAND}",
        shell=True, capture_output=True, text=True, timeout=300
    )
    output = result.stderr
    for line in output.splitlines():
        if "Maximum resident set size" in line:
            kb = int(line.split(":")[-1].strip())
            mb = kb / 1024
            print(f"peak_mb: {mb:.1f}")
            print(f"peak_kb: {kb}")
            sys.exit(0)
    print("Could not parse memory from /usr/bin/time output", file=sys.stderr)
    sys.exit(1)

elif system == "Darwin":
    # macOS: use /usr/bin/time -l
    result = subprocess.run(
        f"/usr/bin/time -l {COMMAND}",
        shell=True, capture_output=True, text=True, timeout=300
    )
    output = result.stderr
    for line in output.splitlines():
        if "maximum resident set size" in line.lower():
            # macOS reports in bytes
            val = int(line.strip().split()[0])
            kb = val / 1024
            mb = val / (1024 * 1024)
            print(f"peak_mb: {mb:.1f}")
            print(f"peak_kb: {int(kb)}")
            sys.exit(0)
    print("Could not parse memory from time output", file=sys.stderr)
    sys.exit(1)

else:
    print(f"Unsupported platform: {system}. Use Linux or macOS.", file=sys.stderr)
    sys.exit(1)
