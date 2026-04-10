#!/usr/bin/env python3
"""
append_log.py — Append a standardized entry to wiki/log.md.

The log is append-only and uses a consistent header so unix tools can parse it:
    ## [YYYY-MM-DD] <op> | <title>

Usage:
    python append_log.py --vault ~/vaults/research --op ingest --title "Anthropic Monosemanticity"
    python append_log.py --vault . --op query --title "interpretability vs mechinterp" --detail "3 pages touched"
    python append_log.py --vault . --op lint --title "weekly health check" --detail "2 contradictions, 5 orphans"

Valid ops: ingest, query, lint, create, update, delete, note
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

VALID_OPS = {"ingest", "query", "lint", "create", "update", "delete", "note"}


def append_log(vault: Path, op: str, title: str, detail: str | None) -> None:
    if op not in VALID_OPS:
        print(f"[error] unknown op '{op}'. Valid: {sorted(VALID_OPS)}", file=sys.stderr)
        sys.exit(1)

    log_path = vault / "wiki" / "log.md"
    if not log_path.exists():
        print(f"[error] {log_path} does not exist — is this a vault?", file=sys.stderr)
        sys.exit(1)

    today = dt.date.today().isoformat()
    header = f"## [{today}] {op} | {title}"
    body = f"\n{detail}\n" if detail else "\n"

    # Append, ensuring a blank line before the new header
    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"\n{header}\n{body}")

    print(f"[ok] appended to {log_path}")
    print(f"     {header}")


def main() -> None:
    p = argparse.ArgumentParser(description="Append a standardized entry to wiki/log.md")
    p.add_argument("--vault", required=True, help="Vault root")
    p.add_argument("--op", required=True, choices=sorted(VALID_OPS))
    p.add_argument("--title", required=True)
    p.add_argument("--detail", default=None, help="Optional body text for the entry")
    args = p.parse_args()
    append_log(Path(args.vault).expanduser().resolve(), args.op, args.title, args.detail)


if __name__ == "__main__":
    main()
