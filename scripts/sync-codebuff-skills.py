#!/usr/bin/env python3
"""
sync-codebuff-skills.py — Install claude-code-skills into Codebuff.

Codebuff (https://codebuff.com) discovers agent skills from ~/.agents/skills/
using the agentskills.io standard (SKILL.md with YAML frontmatter) — the same
format this repo uses, so no conversion is needed.

This is a thin wrapper around sync-vibe-skills.py: identical discovery and
flat-layout sync logic, different default target directory.

Usage:
    python scripts/sync-codebuff-skills.py                  # full sync
    python scripts/sync-codebuff-skills.py --verbose         # show each skill
    python scripts/sync-codebuff-skills.py --domain engineering  # one domain
    python scripts/sync-codebuff-skills.py --dry-run          # preview only
    python scripts/sync-codebuff-skills.py --copy             # copy instead of symlink

Codebuff skill directory: ~/.agents/skills/
Skills land flat:          ~/.agents/skills/<skill-name>/
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

CODEBUFF_SKILLS_DIR = Path.home() / ".agents" / "skills"


def load_vibe_module():
    """Load sync-vibe-skills.py (hyphenated filename) as a module."""
    path = Path(__file__).resolve().parent / "sync-vibe-skills.py"
    spec = importlib.util.spec_from_file_location("sync_vibe_skills", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    vibe = load_vibe_module()
    # Reuse the vibe CLI wholesale with a codebuff default target.
    if not any(arg.startswith("--target") for arg in sys.argv[1:]):
        sys.argv.extend(["--target", str(CODEBUFF_SKILLS_DIR)])
    vibe.VIBE_SKILLS_DIR = CODEBUFF_SKILLS_DIR
    vibe.TOOL_NAME = "Codebuff"
    vibe.main()


if __name__ == "__main__":
    main()
