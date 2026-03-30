"""Shared fixtures and configuration for the test suite."""

import os
import sys

# Repository root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def add_script_dir_to_path(script_path: str):
    """Add a script's parent directory to sys.path for imports."""
    script_dir = os.path.dirname(os.path.abspath(script_path))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    return script_dir
