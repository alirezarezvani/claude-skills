#!/usr/bin/env python3
"""Measure test suite pass rate.
DO NOT MODIFY after experiment starts — this is the fixed evaluator."""

import re
import subprocess
import sys

# --- CONFIGURE THESE ---
TEST_CMD = "pytest tests/ --tb=no -q"  # Test command
# --- END CONFIG ---

result = subprocess.run(TEST_CMD, shell=True, capture_output=True, text=True, timeout=300)
output = result.stdout + "\n" + result.stderr

# Try to parse pytest output: "X passed, Y failed, Z errors"
passed = failed = errors = 0

# pytest short format: "5 passed, 2 failed in 1.23s"
match = re.search(r"(\d+) passed", output)
if match:
    passed = int(match.group(1))
match = re.search(r"(\d+) failed", output)
if match:
    failed = int(match.group(1))
match = re.search(r"(\d+) error", output)
if match:
    errors = int(match.group(1))

total = passed + failed + errors
if total == 0:
    # Try unittest format: "Ran X tests"
    match = re.search(r"Ran (\d+) test", output)
    if match:
        total = int(match.group(1))
        if result.returncode == 0:
            passed = total
        else:
            # Count failures from output
            fail_match = re.search(r"FAILED \(failures=(\d+)", output)
            if fail_match:
                failed = int(fail_match.group(1))
                passed = total - failed

if total == 0:
    print("Could not parse test results", file=sys.stderr)
    print(f"Output: {output[:500]}", file=sys.stderr)
    sys.exit(1)

rate = passed / total

print(f"pass_rate: {rate:.4f}")
print(f"passed: {passed}")
print(f"failed: {failed}")
print(f"total: {total}")
