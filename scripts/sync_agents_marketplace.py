#!/usr/bin/env python3
"""Generate .agents/plugins/marketplace.json from the Claude marketplace.

The agent-agnostic Codex / ChatGPT Plugins Directory catalog (astryx-style
local sources) must list the same plugins, paths, and plugin metadata as
`.claude-plugin/marketplace.json`. Marketplace presentation (`name` and
`interface.displayName`) is taken from `.codex-plugin/plugin.json` so Codex
metadata stays single-sourced and does not drift.

  python3 scripts/sync_agents_marketplace.py           # write the file
  python3 scripts/sync_agents_marketplace.py --check   # exit 1 on drift
  python3 scripts/sync_agents_marketplace.py --stdout  # print JSON only
"""
from __future__ import annotations

import argparse
import json
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLAUDE_MARKETPLACE = os.path.join(REPO_ROOT, ".claude-plugin", "marketplace.json")
CODEX_PLUGIN = os.path.join(REPO_ROOT, ".codex-plugin", "plugin.json")
AGENTS_MARKETPLACE = os.path.join(REPO_ROOT, ".agents", "plugins", "marketplace.json")

DEFAULT_POLICY = {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL",
}


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_agents_marketplace(claude=None, codex=None):
    claude = claude if claude is not None else _load(CLAUDE_MARKETPLACE)
    codex = codex if codex is not None else _load(CODEX_PLUGIN)

    name = codex.get("name") or claude.get("name")
    display = (codex.get("interface") or {}).get("displayName") or name

    plugins = []
    for entry in claude.get("plugins", []):
        source = entry.get("source")
        if not isinstance(source, str) or not source.startswith("./"):
            raise ValueError(
                f"plugin {entry.get('name')!r}: source must be a ./-prefixed path, "
                f"got {source!r}"
            )
        plugin = {
            "name": entry["name"],
            "source": {"source": "local", "path": source},
            "policy": dict(DEFAULT_POLICY),
            "category": entry.get("category") or "Coding",
        }
        # Preserve Claude marketplace metadata so both catalogs stay aligned.
        for key in ("description", "version", "author", "keywords"):
            if key in entry:
                plugin[key] = entry[key]
        plugins.append(plugin)

    return {
        "name": name,
        "interface": {"displayName": display},
        "plugins": plugins,
    }


def render(data):
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def write(data, path=AGENTS_MARKETPLACE):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render(data))
    return path


def check(data, path=AGENTS_MARKETPLACE):
    expected = render(data)
    if not os.path.isfile(path):
        return [f"missing {os.path.relpath(path, REPO_ROOT)}"]
    with open(path, encoding="utf-8") as f:
        actual = f.read()
    if actual != expected:
        try:
            on_disk = json.loads(actual)
        except json.JSONDecodeError as exc:
            return [f"{os.path.relpath(path, REPO_ROOT)} is not valid JSON: {exc}"]
        errs = []
        if on_disk.get("name") != data.get("name"):
            errs.append(f"name: disk={on_disk.get('name')!r} expected={data.get('name')!r}")
        if on_disk.get("interface") != data.get("interface"):
            errs.append("interface differs from .codex-plugin/plugin.json displayName")
        disk_plugins = {p.get("name"): p for p in on_disk.get("plugins", [])}
        exp_plugins = {p.get("name"): p for p in data.get("plugins", [])}
        missing = sorted(set(exp_plugins) - set(disk_plugins))
        extra = sorted(set(disk_plugins) - set(exp_plugins))
        if missing:
            errs.append(f"missing plugins: {', '.join(missing[:10])}"
                        + ("…" if len(missing) > 10 else ""))
        if extra:
            errs.append(f"extra plugins: {', '.join(extra[:10])}"
                        + ("…" if len(extra) > 10 else ""))
        if not errs:
            errs.append(
                f"{os.path.relpath(path, REPO_ROOT)} drifts from "
                ".claude-plugin/marketplace.json (run scripts/sync_agents_marketplace.py)"
            )
        return errs
    return []


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true",
                   help="exit 1 if .agents/plugins/marketplace.json is missing or drifts")
    g.add_argument("--stdout", action="store_true", help="print generated JSON to stdout")
    args = ap.parse_args(argv)

    try:
        data = build_agents_marketplace()
    except (OSError, json.JSONDecodeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.check:
        problems = check(data)
        if problems:
            print("FAIL .agents/plugins/marketplace.json")
            for p in problems:
                print(f"  - {p}")
            return 1
        print(
            f"OK   .agents/plugins/marketplace.json "
            f"({len(data['plugins'])} plugins, mirrors Claude marketplace)"
        )
        return 0

    if args.stdout:
        sys.stdout.write(render(data))
        return 0

    path = write(data)
    print(f"wrote {os.path.relpath(path, REPO_ROOT)} ({len(data['plugins'])} plugins)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
