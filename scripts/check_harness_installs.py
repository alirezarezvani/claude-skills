#!/usr/bin/env python3
"""Clean-install check for the non-Claude harnesses.

For each harness this runs the documented install path into a throwaway HOME,
then asks the real, open-source harness which skills it discovered and
compares that with what was installed. Nothing here calls a model or needs an
API key: every harness is queried through an offline listing.

  codex   scripts/codex-install.sh --category <c>, one fresh CODEX_HOME per
          category (the documented way; the full library overflows Codex's
          skill budget). Listing: `codex debug prompt-input`, which renders
          the skill catalog the model would see.
  gemini  the committed .gemini/skills mirror, read as a trusted workspace.
          Listing: `gemini skills list`. Name conflicts fail the check.
  hermes  scripts/sync-hermes-skills.py into ~/.hermes/skills.
          Listing: `hermes skills list`.
  vibe    scripts/vibe-install.sh into ~/.vibe/skills. Vibe has no listing
          command, so this loads Vibe's own SkillManager (the code its
          sessions use) and fails on any skill it rejects or reports an
          issue for.

A harness whose CLI is not on PATH is reported as SKIP (exit 0) unless
--require is given, so the script is safe to run locally.

Exit codes:
  0  every checked harness discovered every installed skill
  1  at least one harness missed, rejected or conflicted on a skill
  2  a harness was required but its CLI is missing, or a tool crashed

Usage:
  python3 scripts/check_harness_installs.py                      # all, skip missing CLIs
  python3 scripts/check_harness_installs.py --harness gemini --require
  python3 scripts/check_harness_installs.py --vibe-python /path/to/venv/bin/python
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
HARNESSES = ("codex", "gemini", "hermes", "vibe")


class Missing(Exception):
    """The harness CLI is not installed."""


def _fm_name(skill_md: Path) -> str | None:
    """Frontmatter `name:` of a SKILL.md, or None."""
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    for line in text[3:end if end > 0 else len(text)].splitlines():
        m = re.match(r"^name:\s*['\"]?([^'\"#]+?)['\"]?\s*$", line)
        if m:
            return m.group(1).strip()
    return None


def _installed_names(skills_dir: Path) -> dict[str, str]:
    """Map frontmatter name -> install dir name for every skill under skills_dir."""
    out = {}
    for d in sorted(skills_dir.iterdir()):
        if d.name.startswith(".") or not d.is_dir():
            continue
        name = _fm_name(d / "SKILL.md")
        out[name or d.name] = d.name
    return out


def _run(cmd: list[str], env: dict, cwd: Path | None = None, timeout: int = 300) -> str:
    proc = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, text=True,
                          timeout=timeout)
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:3])} exited {proc.returncode}:\n"
                           f"{(proc.stdout + proc.stderr)[-3000:]}")
    return proc.stdout + proc.stderr


def _env(home: Path, **extra: str) -> dict:
    env = {k: v for k, v in os.environ.items()
           if not k.endswith(("_API_KEY", "_TOKEN"))}  # never hand a key to a harness
    # Wide COLUMNS keeps table-printing CLIs (hermes) from truncating names.
    env.update(HOME=str(home), NO_COLOR="1", COLUMNS="400", **extra)
    return env


def _which(binary: str) -> str:
    path = shutil.which(binary)
    if not path:
        raise Missing(binary)
    return path


# ── codex ────────────────────────────────────────────────────────────────────

def check_codex(tmp: Path, _: argparse.Namespace) -> list[str]:
    codex = _which("codex")
    index = json.loads((REPO_ROOT / ".codex/skills-index.json").read_text())
    categories = sorted({s["category"] for s in index["skills"]})
    problems = []
    total = 0
    for cat in categories:
        home = tmp / f"codex-{cat}"
        codex_home = home / ".codex"
        env = _env(home, CODEX_HOME=str(codex_home),
                   CODEX_SKILLS_DIR=str(codex_home / "skills"))
        _run(["bash", str(REPO_ROOT / "scripts/codex-install.sh"), "--category", cat], env)
        installed = _installed_names(codex_home / "skills")
        rendered = _run([codex, "debug", "prompt-input"], env, cwd=home, timeout=120)
        text = rendered.replace("\\n", "\n")
        seen = set(re.findall(r"^- ([^:\n]+): .*?\(file: [^)\n]*SKILL\.md\)", text, re.M))
        missing = sorted(set(installed) - seen)
        total += len(installed)
        for name in missing:
            problems.append(f"category {cat}: Codex did not list {name} "
                            f"(installed as {installed[name]})")
        print(f"    {cat:<22} installed {len(installed):>3}, listed "
              f"{len(installed) - len(missing):>3}")
    print(f"    codex total: {total} skills across {len(categories)} categories")
    return problems


# ── gemini ───────────────────────────────────────────────────────────────────

def check_gemini(tmp: Path, _: argparse.Namespace) -> list[str]:
    gemini = _which("gemini")
    home = tmp / "gemini"
    (home / ".gemini").mkdir(parents=True)
    # A fresh clone is an untrusted folder; Gemini skips workspace skills then.
    (home / ".gemini/trustedFolders.json").write_text(
        json.dumps({str(REPO_ROOT): "TRUST_FOLDER"}))
    out = _run([gemini, "skills", "list"], _env(home), cwd=REPO_ROOT, timeout=180)
    index = json.loads((REPO_ROOT / ".gemini/skills-index.json").read_text())
    expected = {s["name"] for s in index["skills"]}
    mirror = (REPO_ROOT / ".gemini/skills").resolve()
    seen = set()
    for loc in re.findall(r"Location:\s+(\S+)", out):
        p = Path(loc)
        try:
            seen.add(p.relative_to(mirror).parts[0])
        except ValueError:
            try:
                seen.add(p.resolve().relative_to(mirror).parts[0])
            except ValueError:
                pass  # a skill from outside the repo mirror
    problems = [f"Gemini did not load .gemini/skills/{n} (check its frontmatter `name:`)"
                for n in sorted(expected - seen)]
    problems += [f"Gemini: {line.strip()}" for line in out.splitlines()
                 if "conflict" in line.lower()]
    print(f"    indexed {len(expected)}, discovered {len(seen & expected)}")
    return problems


# ── hermes ───────────────────────────────────────────────────────────────────

def check_hermes(tmp: Path, _: argparse.Namespace) -> list[str]:
    hermes = _which("hermes")
    home = tmp / "hermes"
    home.mkdir()
    env = _env(home)
    _run([sys.executable, str(REPO_ROOT / "scripts/sync-hermes-skills.py")], env)
    target = home / ".hermes/skills/claude-skills"
    index = json.loads((target / "skills-index.json").read_text())
    expected = set()
    for entries in index["domains"].values():
        for s in entries:
            md = target / s["path"] / "SKILL.md"
            expected.add(_fm_name(md) or Path(s["path"]).name)
    out = _run([hermes, "skills", "list"], env, cwd=home, timeout=180)
    seen = set(re.findall(r"^│\s*(\S+)\s*│\s*claude-skills\s*│", out, re.M))
    summary = re.search(r"(\d+)\s+local", out)
    problems = [f"Hermes did not list {n}" for n in sorted(expected - seen)]
    if summary and int(summary.group(1)) < len(expected):
        problems.append(f"Hermes reports {summary.group(1)} local skills, "
                        f"{len(expected)} were installed")
    print(f"    installed {len(expected)}, listed {len(seen & expected)}")
    return problems


# ── vibe ─────────────────────────────────────────────────────────────────────

VIBE_PROBE = r"""
import json, sys
from types import SimpleNamespace
from vibe.core.config.harness_files._harness_manager import init_harness_files_manager
from vibe.core.skills.manager import SkillManager
init_harness_files_manager("user")
cfg = SimpleNamespace(skill_paths=[], enabled_skills=[], disabled_skills=[],
                      experimental_enable_registry_skills=False)
m = SkillManager(lambda: cfg)
print(json.dumps({
    "skills": {n: str(i.skill_path) for n, i in m.available_skills.items()},
    "issues": [f"{i.file}: {i.message}" for i in m.config_issues],
}))
"""


def check_vibe(tmp: Path, args: argparse.Namespace) -> list[str]:
    py = args.vibe_python or shutil.which("python3")
    probe_env_ok = subprocess.run([py, "-c", "import vibe"], capture_output=True).returncode == 0
    if not probe_env_ok:
        raise Missing("vibe (python package mistral-vibe)")
    home = tmp / "vibe"
    home.mkdir()
    env = _env(home)
    _run(["bash", str(REPO_ROOT / "scripts/vibe-install.sh")], env)
    skills_dir = home / ".vibe/skills"
    installed = _installed_names(skills_dir)
    out = _run([py, "-c", VIBE_PROBE], env, cwd=home, timeout=120)
    data = json.loads(out.strip().splitlines()[-1])
    problems = [f"Vibe did not load {n} (installed as {installed[n]})"
                for n in sorted(set(installed) - set(data["skills"]))]
    problems += [f"Vibe issue: {i}" for i in data["issues"]]
    print(f"    installed {len(installed)}, loaded {len(set(installed) & set(data['skills']))}")
    return problems


CHECKS = {"codex": check_codex, "gemini": check_gemini,
          "hermes": check_hermes, "vibe": check_vibe}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--harness", choices=(*HARNESSES, "all"), default="all")
    ap.add_argument("--require", action="store_true",
                    help="fail (exit 2) when a harness CLI is not installed")
    ap.add_argument("--vibe-python", help="python interpreter that has mistral-vibe installed")
    args = ap.parse_args()

    names = HARNESSES if args.harness == "all" else (args.harness,)
    failed = crashed = False
    for name in names:
        print(f"[{name}]")
        with tempfile.TemporaryDirectory(prefix=f"harness-{name}-") as tmp:
            try:
                problems = CHECKS[name](Path(tmp), args)
            except Missing as e:
                print(f"    SKIP: {e} not installed")
                crashed |= args.require
                continue
            except (RuntimeError, subprocess.TimeoutExpired, OSError, ValueError) as e:
                print(f"    ERROR: {e}")
                crashed = True
                continue
        for p in problems:
            print(f"    FAIL: {p}")
        print(f"    {'FAIL' if problems else 'OK'}")
        failed |= bool(problems)
    if crashed:
        return 2
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
