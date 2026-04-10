#!/usr/bin/env python3
"""
init_vault.py — Bootstrap an LLM Wiki vault.

Creates the three-layer structure (raw/, wiki/, schema files) and seeds it with
starter templates for CLAUDE.md, AGENTS.md, index.md, log.md, and page templates.

Usage:
    python init_vault.py --path ~/vaults/research --topic "LLM interpretability"
    python init_vault.py --path ./my-wiki --topic "Book: The Power Broker" --tool codex

The --tool flag controls which schema file(s) to install:
    claude-code  → CLAUDE.md (default)
    codex        → AGENTS.md
    cursor       → AGENTS.md + .cursorrules
    antigravity  → AGENTS.md
    all          → CLAUDE.md + AGENTS.md + .cursorrules (recommended for multi-tool)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PLUGIN_DIR = SCRIPT_DIR.parent
ASSETS_DIR = PLUGIN_DIR / "assets"

VAULT_DIRS = [
    "raw",
    "raw/assets",
    "wiki",
    "wiki/entities",
    "wiki/concepts",
    "wiki/sources",
    "wiki/comparisons",
    "wiki/synthesis",
]

TOOL_FILES = {
    "claude-code": ["CLAUDE.md.template:CLAUDE.md"],
    "codex": ["AGENTS.md.template:AGENTS.md"],
    "cursor": ["AGENTS.md.template:AGENTS.md", ".cursorrules.template:.cursorrules"],
    "antigravity": ["AGENTS.md.template:AGENTS.md"],
    "opencode": ["AGENTS.md.template:AGENTS.md"],
    "gemini-cli": ["AGENTS.md.template:AGENTS.md"],
    "all": [
        "CLAUDE.md.template:CLAUDE.md",
        "AGENTS.md.template:AGENTS.md",
        ".cursorrules.template:.cursorrules",
    ],
}


def render_template(src: Path, dest: Path, variables: dict[str, str]) -> None:
    if not src.exists():
        print(f"[warn] template missing: {src}", file=sys.stderr)
        return
    text = src.read_text(encoding="utf-8")
    for key, value in variables.items():
        text = text.replace("{{" + key + "}}", value)
    dest.write_text(text, encoding="utf-8")


def init_vault(vault_path: Path, topic: str, tool: str, force: bool) -> None:
    if vault_path.exists() and any(vault_path.iterdir()) and not force:
        print(
            f"[error] {vault_path} is not empty. Use --force to overwrite.",
            file=sys.stderr,
        )
        sys.exit(1)

    vault_path.mkdir(parents=True, exist_ok=True)
    for d in VAULT_DIRS:
        (vault_path / d).mkdir(parents=True, exist_ok=True)

    today = dt.date.today().isoformat()
    variables = {
        "TOPIC": topic,
        "DATE": today,
        "VAULT_NAME": vault_path.name,
    }

    # Schema files (CLAUDE.md / AGENTS.md / .cursorrules)
    for spec in TOOL_FILES.get(tool, TOOL_FILES["claude-code"]):
        src_name, dest_name = spec.split(":", 1)
        render_template(ASSETS_DIR / src_name, vault_path / dest_name, variables)

    # Index + log seeds
    render_template(
        ASSETS_DIR / "index.md.template", vault_path / "wiki" / "index.md", variables
    )
    render_template(
        ASSETS_DIR / "log.md.template", vault_path / "wiki" / "log.md", variables
    )

    # Page templates (for reference inside the vault)
    tmpl_dest = vault_path / "wiki" / ".templates"
    tmpl_dest.mkdir(exist_ok=True)
    src_tmpl = ASSETS_DIR / "page-templates"
    if src_tmpl.exists():
        for f in src_tmpl.iterdir():
            if f.is_file():
                (tmpl_dest / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")

    # .gitignore — exclude Obsidian workspace files
    gitignore = vault_path / ".gitignore"
    gitignore.write_text(
        "\n".join(
            [
                ".obsidian/workspace*",
                ".obsidian/cache",
                ".DS_Store",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"[ok] Initialized LLM Wiki vault at: {vault_path}")
    print(f"     Topic: {topic}")
    print(f"     Tool: {tool}")
    print("     Layers:")
    print("       raw/          (your sources — immutable)")
    print("       wiki/         (LLM-maintained knowledge base)")
    print("       wiki/index.md (catalog)")
    print("       wiki/log.md   (timeline)")
    print()
    print("Next steps:")
    print("  1. Open the vault in Obsidian")
    print("  2. Drop a source into raw/")
    print("  3. Run /wiki-ingest <path> in your LLM CLI")


def main() -> None:
    p = argparse.ArgumentParser(description="Initialize an LLM Wiki vault.")
    p.add_argument("--path", required=True, help="Vault directory to create/initialize")
    p.add_argument(
        "--topic",
        required=True,
        help="Short description of what this wiki is about (e.g. 'LLM interpretability')",
    )
    p.add_argument(
        "--tool",
        default="all",
        choices=sorted(TOOL_FILES.keys()),
        help="Which schema file(s) to install (default: all)",
    )
    p.add_argument(
        "--force", action="store_true", help="Overwrite non-empty target directory"
    )
    args = p.parse_args()
    init_vault(Path(args.path).expanduser().resolve(), args.topic, args.tool, args.force)


if __name__ == "__main__":
    main()
