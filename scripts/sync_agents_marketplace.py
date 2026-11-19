#!/usr/bin/env python3
"""Generate .agents/plugins/marketplace.json from the Claude marketplace.

The agent-agnostic Codex / ChatGPT Plugins Directory catalog (astryx-style
local sources) lists the plugins of `.claude-plugin/marketplace.json` that Codex can
load, with the same paths and metadata. A plugin is left out, and named by --check,
when its skills are not under skills/<name>/SKILL.md or its plugin.json name differs
from its marketplace name; scripts/check_harness_installs.py --harness codex installs
every listed plugin with the real Codex CLI and checks each skill is listed. Marketplace presentation (`name` and
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


def codex_skill_dirs(source):
    """Skill folders Codex discovers in a plugin: only <plugin>/skills/<name>/SKILL.md.

    Verified on codex-cli 0.170.0: a SKILL.md at the plugin root is not listed, whatever
    the plugin manifest's `skills` field says.
    """
    root = os.path.join(REPO_ROOT, os.path.normpath(source), "skills")
    if not os.path.isdir(root):
        return []
    return sorted(d for d in os.listdir(root)
                  if os.path.isfile(os.path.join(root, d, "SKILL.md")))


def claude_skill_files(source):
    """SKILL.md files the plugin declares to Claude Code through its plugin.json `skills`."""
    base = os.path.join(REPO_ROOT, os.path.normpath(source))
    skills = _load(os.path.join(base, ".claude-plugin", "plugin.json")).get("skills", [])
    found = set()
    for rel in skills if isinstance(skills, list) else [skills]:
        d = os.path.normpath(os.path.join(base, rel))
        if os.path.isfile(os.path.join(d, "SKILL.md")):
            found.add(os.path.join(d, "SKILL.md"))
        elif os.path.isdir(d):
            found.update(os.path.join(d, x, "SKILL.md") for x in os.listdir(d)
                         if os.path.isfile(os.path.join(d, x, "SKILL.md")))
    return sorted(found)


def unloadable_reason(entry):
    """Why Codex cannot install or load this plugin, or None when it can."""
    source = entry["source"]
    manifest = os.path.join(REPO_ROOT, os.path.normpath(source), ".claude-plugin", "plugin.json")
    try:
        name = _load(manifest).get("name")
    except (OSError, json.JSONDecodeError):
        name = None
    if name != entry["name"]:
        return f"plugin.json name {name!r} differs from the marketplace name (Codex refuses the install)"
    if not codex_skill_dirs(source):
        return "no skills/<name>/SKILL.md (Codex lists no skill from a root SKILL.md)"

    return None


def codex_hidden(source):
    """Declared SKILL.md files Codex will not list (outside skills/<name>/)."""
    codex_files = {os.path.join(REPO_ROOT, os.path.normpath(source), "skills", d, "SKILL.md")
                   for d in codex_skill_dirs(source)}
    return [f for f in claude_skill_files(source) if f not in codex_files]


def skipped(claude=None):
    """(name, reason) for every Claude marketplace plugin left out of the Codex catalog."""
    claude = claude if claude is not None else _load(CLAUDE_MARKETPLACE)
    out = []
    for entry in claude.get("plugins", []):
        reason = unloadable_reason(entry)
        if reason:
            out.append((entry["name"], reason))
    return out


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
        if unloadable_reason(entry):
            continue
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
        for name, reason in skipped():
            print(f"     not listed: {name}: {reason}")
        for p in data["plugins"]:
            hidden = codex_hidden(p["source"]["path"])
            if hidden:
                print(f"     partial: {p['name']}: Codex will not list "
                      + ", ".join(os.path.relpath(h, REPO_ROOT) for h in hidden))
        return 0

    if args.stdout:
        sys.stdout.write(render(data))
        return 0

    path = write(data)
    print(f"wrote {os.path.relpath(path, REPO_ROOT)} ({len(data['plugins'])} plugins)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
