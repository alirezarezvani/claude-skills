#!/usr/bin/env python3
"""Export a hero skill as a standalone repo tree, generated from this monorepo.

A hero is one plugin that gets its own repository, its own one-line promise
and its own launch, so it can trend and be shared on its own. This repo stays
the source of truth: the hero tree is regenerated on every sync and must never
be edited by hand.

For each hero in heroes/heroes.json the export:
  - copies the plugin directory, following symlinks (vendor/ links become files)
  - adds .claude-plugin/marketplace.json so `/plugin marketplace add <owner>/<repo>` works
  - writes a README with the promise, both install paths, the trigger-test result
    and a link back, followed by the plugin's own README
  - copies the root LICENSE when the plugin has none

Usage:
  python3 scripts/export_hero.py --list
  python3 scripts/export_hero.py agent-run-forensics --out /tmp/hero
  python3 scripts/export_hero.py --all --out /tmp/heroes      # one subdir per hero
  python3 scripts/export_hero.py --check                       # validate heroes.json

Exit codes: 0 ok, 1 validation failed, 2 unknown hero. Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HEROES = ROOT / "heroes" / "heroes.json"
TRIGGER = ROOT / "audit" / "verified-tier" / "trigger_results.json"
MONOREPO = "alirezarezvani/claude-skills"


def load() -> tuple[list[dict], dict, dict]:
    heroes = json.loads(HEROES.read_text(encoding="utf-8"))["heroes"]
    market = {p["name"]: p for p in json.loads(
        (ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))["plugins"]}
    trig = {s["skill"]: s for s in json.loads(TRIGGER.read_text(encoding="utf-8"))["skills"]}
    return heroes, market, trig


def skill_results(hero: dict, trig: dict) -> list[dict]:
    prefix = hero["path"].rstrip("/") + "/"
    return [s for k, s in trig.items() if k == hero["path"] or k.startswith(prefix)]


def validate(hero: dict, market: dict, trig: dict) -> list[str]:
    errs = []
    src = ROOT / hero["path"]
    if not (src / ".claude-plugin" / "plugin.json").exists():
        errs.append(f"{hero['plugin']}: {hero['path']}/.claude-plugin/plugin.json missing")
        return errs
    pj = json.loads((src / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    if pj.get("name") != hero["plugin"]:
        errs.append(f"{hero['plugin']}: plugin.json name is {pj.get('name')!r}")
    entry = market.get(hero["plugin"])
    if not entry or entry["source"].lstrip("./").rstrip("/") != hero["path"]:
        errs.append(f"{hero['plugin']}: not a standalone marketplace entry with source ./{hero['path']}")
    results = skill_results(hero, trig)
    if not results or any(r["verdict"] != "FIRES" for r in results):
        errs.append(f"{hero['plugin']}: every skill must be FIRES in {TRIGGER.relative_to(ROOT)}")
    for k in ("repo", "promise", "pitch"):
        if not hero.get(k):
            errs.append(f"{hero['plugin']}: '{k}' is empty")
    return errs


def readme(hero: dict, pj: dict, results: list[dict], original: str) -> str:
    owner_repo = hero["repo"]
    pos = sum(r["pos_exact"] for r in results)
    pos_total = sum(r["pos_total"] for r in results)
    neg_total = sum(r["neg_total"] for r in results)
    body = original.strip()
    if body.startswith("# "):
        body = body.split("\n", 1)[1].lstrip() if "\n" in body else ""
    return f"""# {pj['name']}

**{hero['promise']}**

{hero['pitch']}

## Install

Claude Code:

```bash
/plugin marketplace add {owner_repo}
/plugin install {pj['name']}@{pj['name']}
```

Codex, Cursor, Gemini CLI, Copilot and other agents:

```bash
npx skills add {owner_repo}
```

## Does it load when you need it?

In our trigger tests it loaded on {pos} of {pos_total} plain-language prompts that didn't name it,
and stayed quiet on {neg_total} close-but-unrelated prompt{"s" if neg_total != 1 else ""}.
See [how we test](https://github.com/{MONOREPO}/blob/main/VERIFIED.md).

## Part of claude-skills

This repo is generated from [{MONOREPO}](https://github.com/{MONOREPO}/tree/main/{hero['path']}),
a library of 400+ tested skills for engineering, product, marketing, compliance and leadership.
Open issues and pull requests there; changes here are overwritten on the next sync.

---

## Details

{body}
"""


def export(hero: dict, out: Path) -> None:
    src = ROOT / hero["path"]
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(src, out, symlinks=False, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    pj = json.loads((src / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    pj["homepage"] = f"https://github.com/{hero['repo']}"
    pj["repository"] = f"https://github.com/{hero['repo']}"
    (out / ".claude-plugin" / "plugin.json").write_text(json.dumps(pj, indent=2) + "\n", encoding="utf-8")
    owner = hero["repo"].split("/")[0]
    marketplace = {
        "name": pj["name"],
        "owner": {"name": pj["author"]["name"], "url": f"https://github.com/{owner}"},
        "metadata": {"description": hero["promise"], "version": pj["version"]},
        "plugins": [{
            "name": pj["name"], "source": "./", "description": pj["description"],
            "version": pj["version"], "author": pj["author"], "license": pj.get("license", "MIT"),
        }],
    }
    (out / ".claude-plugin" / "marketplace.json").write_text(json.dumps(marketplace, indent=2) + "\n", encoding="utf-8")
    original = (src / "README.md").read_text(encoding="utf-8") if (src / "README.md").exists() else ""
    _, _, trig = load()
    (out / "README.md").write_text(readme(hero, pj, skill_results(hero, trig), original), encoding="utf-8")
    if not (out / "LICENSE").exists():
        shutil.copy(ROOT / "LICENSE", out / "LICENSE")
    (out / "SOURCE").write_text(
        f"Generated from https://github.com/{MONOREPO}/tree/main/{hero['path']}\n"
        "Do not edit by hand: the next sync overwrites every file.\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plugin", nargs="?", help="hero plugin name")
    ap.add_argument("--all", action="store_true", help="export every hero, one subdirectory each")
    ap.add_argument("--out", type=Path, help="output directory")
    ap.add_argument("--list", action="store_true", help="list heroes")
    ap.add_argument("--check", action="store_true", help="validate heroes.json and exit")
    args = ap.parse_args()

    heroes, market, trig = load()
    errs = [e for h in heroes for e in validate(h, market, trig)]
    if args.check or args.list:
        for h in heroes:
            if args.list:
                print(f"{h['plugin']:24} {h['repo']:40} {h['promise']}")
        for e in errs:
            print(f"ERROR: {e}", file=sys.stderr)
        if args.check and not errs:
            print(f"heroes.json OK ({len(heroes)} heroes)")
        return 1 if errs else 0
    if errs:
        for e in errs:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    if not args.out:
        ap.error("--out is required to export")
    chosen = heroes if args.all else [h for h in heroes if h["plugin"] == args.plugin]
    if not chosen:
        print(f"unknown hero {args.plugin!r}; see --list", file=sys.stderr)
        return 2
    for h in chosen:
        dest = args.out / h["plugin"] if args.all else args.out
        export(h, dest)
        print(f"exported {h['plugin']} -> {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
