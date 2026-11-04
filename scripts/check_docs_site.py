#!/usr/bin/env python3
"""Gate G14: keep the docs site honest.

Checks the hand-written pages under docs/ (the tracked files; skill, agent and
command pages are generated at build time and are not tracked):

  1. No hard-coded headline counters ("345 skills", "80 plugins"). Use the
     build-time tokens instead: {{ count.skills }}, {{ count.plugins }} ...
  2. Every `/plugin install <name>@claude-code-skills` names a plugin that
     exists in .claude-plugin/marketplace.json, and no install line uses the
     invalid `claude /plugin ...` form or omits the marketplace.
  3. With --build: `mkdocs build --strict` passes, no page is left out of
     the nav, and every scripts/docs_start_here.json pick has a page. Needs the pinned mkdocs packages from static.yml.

Exit codes: 0 clean, 1 findings, 2 usage or environment error.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"

# A number this large next to a counted noun is a headline counter; smaller
# ones ("the 20 plugins to start with", "5 releases") are editorial choices.
COUNTER_FLOOR = 25
COUNTER_RE = re.compile(
    r"\b(\d{2,4})\+?\s+(?:production-ready\s+|agent\s+|Python\s+|automation\s+|marketplace\s+)*"
    r"(skills|plugins|agents|slash commands|commands|Python tools|tools|reference guides|references|domains)\b")
TABLE_COUNTER_RE = re.compile(
    r"^\|\s*[^|]*\b(skills|plugins|domains|tools|guides|agents|commands)\b[^|]*\|\s*(\d{2,4})\s*\|\s*$", re.I)
INSTALL_RE = re.compile(r"plugin install\s+([A-Za-z0-9_.:/@-]+)")


def tracked_docs():
    out = subprocess.run(["git", "ls-files", "docs"], cwd=REPO_ROOT, capture_output=True, text=True, check=True)
    return [REPO_ROOT / p for p in out.stdout.split() if p.endswith((".md", ".txt"))]


def check_text(files, marketplace_name, plugin_names):
    findings = []
    for path in files:
        rel = path.relative_to(REPO_ROOT)
        in_fence = False
        for no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
            for m in COUNTER_RE.finditer(line):
                if int(m.group(1)) >= COUNTER_FLOOR:
                    findings.append((rel, no, f"hard-coded counter '{m.group(0)}': use a {{{{ count.* }}}} token"))
            t = TABLE_COUNTER_RE.match(line.strip())
            if t and int(t.group(2)) >= COUNTER_FLOOR:
                findings.append((rel, no, f"hard-coded counter in table row: use a {{{{ count.* }}}} token"))
            if re.search(r"\bclaude\s+/plugin\b", line):
                findings.append((rel, no, "'claude /plugin ...' is not a valid command: use /plugin inside Claude Code or `claude plugin` in a shell"))
            for m in INSTALL_RE.finditer(line):
                target = m.group(1)
                if "{{" in line or target.startswith("<") or "<" in line[m.start():m.end() + 2]:
                    continue
                name, _, market = target.partition("@")
                if not market:
                    findings.append((rel, no, f"install of '{name}' omits @{marketplace_name}"))
                elif market == marketplace_name and name not in plugin_names and name != "skill-name":
                    findings.append((rel, no, f"'{name}' is not a plugin in marketplace.json"))
    return findings


def check_build():
    proc = subprocess.run([sys.executable, "-m", "mkdocs", "build", "--strict"], cwd=REPO_ROOT,
                          capture_output=True, text=True)
    log = proc.stdout + proc.stderr
    findings = []
    if proc.returncode != 0:
        warnings = [l for l in log.splitlines() if l.startswith("WARNING")]
        findings += [("mkdocs.yml", 0, w) for w in warnings[:20]] or [("mkdocs.yml", 0, "mkdocs build --strict failed")]
    if "not included in the \"nav\"" in log:
        orphans = re.findall(r"^\s+- (\S+\.md)$", log.split("not included in the \"nav\"", 1)[1], re.M)
        findings += [("mkdocs.yml", 0, f"page not in nav: {o}") for o in orphans] or [("mkdocs.yml", 0, "pages missing from nav")]
    return findings


def check_start_here():
    """Every 'Start here' pick must name a generated skill page (run after a build)."""
    picks = json.loads((REPO_ROOT / "scripts" / "docs_start_here.json").read_text(encoding="utf-8"))
    return [("scripts/docs_start_here.json", 0, f"'{d}/{slug}' has no page in docs/skills/{d}/")
            for d, slugs in picks.items() if not d.startswith("_")
            for slug in slugs if not (REPO_ROOT / "docs" / "skills" / d / f"{slug}.md").is_file()]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--build", action="store_true", help="also run mkdocs build --strict and check nav orphans")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()

    try:
        market = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"cannot read {MARKETPLACE}: {exc}", file=sys.stderr)
        return 2
    plugin_names = {p["name"] for p in market.get("plugins", [])}
    findings = check_text(tracked_docs(), market["name"], plugin_names)
    if args.build:
        findings += check_build()
        findings += check_start_here()

    if args.json:
        print(json.dumps({"findings": [{"file": str(f), "line": n, "message": m} for f, n, m in findings]}, indent=2))
    else:
        for f, n, m in findings:
            print(f"{f}:{n}: {m}" if n else f"{f}: {m}")
        print(f"G14 docs site: {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
