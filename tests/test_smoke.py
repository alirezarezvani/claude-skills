"""Smoke tests: syntax compilation and --help for all Python scripts.

These tests verify that every Python script in the repository:
1. Compiles without syntax errors (all scripts)
2. Runs --help without crashing (argparse-based scripts only)
"""

import glob
import os
import py_compile
import subprocess
import sys

import pytest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories to skip (sample/fixture code, not real scripts)
SKIP_PATTERNS = [
    "assets/sample_codebase",
    "__pycache__",
    ".venv",
    "tests/",
]


def _collect_all_python_scripts():
    """Find all .py files in the repo, excluding test/fixture code."""
    all_py = glob.glob(os.path.join(REPO_ROOT, "**", "*.py"), recursive=True)
    scripts = []
    for path in sorted(all_py):
        rel = os.path.relpath(path, REPO_ROOT)
        if any(skip in rel for skip in SKIP_PATTERNS):
            continue
        scripts.append(path)
    return scripts


def _has_argparse(path):
    """Check if a script imports argparse (heuristic)."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return "ArgumentParser" in content or "import argparse" in content
    except Exception:
        return False


ALL_SCRIPTS = _collect_all_python_scripts()
ARGPARSE_SCRIPTS = [s for s in ALL_SCRIPTS if _has_argparse(s)]


def _short_id(path):
    """Create a readable test ID from a full path."""
    return os.path.relpath(path, REPO_ROOT)


class TestSyntaxCompilation:
    """Every Python file must compile without syntax errors."""

    @pytest.mark.parametrize(
        "script_path",
        ALL_SCRIPTS,
        ids=[_short_id(s) for s in ALL_SCRIPTS],
    )
    def test_syntax(self, script_path):
        py_compile.compile(script_path, doraise=True)


class TestArgparseHelp:
    """Every argparse-based script must run --help successfully."""

    @pytest.mark.parametrize(
        "script_path",
        ARGPARSE_SCRIPTS,
        ids=[_short_id(s) for s in ARGPARSE_SCRIPTS],
    )
    def test_help_flag(self, script_path):
        result = subprocess.run(
            [sys.executable, script_path, "--help"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"--help failed for {os.path.relpath(script_path, REPO_ROOT)}:\n"
            f"STDOUT: {result.stdout[:500]}\n"
            f"STDERR: {result.stderr[:500]}"
        )
