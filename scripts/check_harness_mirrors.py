#!/usr/bin/env python3
"""Harness mirror drift guard (gate G13).

The repo commits four generated mirror trees so that other harnesses can use
the library straight from a clone:

  .codex/skills/ + .codex/skills-index.json       scripts/sync-codex-skills.py
  .gemini/skills/ + .gemini/skills-index.json     scripts/sync-gemini-skills.py
  .vibe/skills/claude-skills/                     scripts/sync-vibe-skills.py --nested
  .hermes/skills/claude-skills/                   scripts/sync-hermes-skills.py

Until this gate they were resynced by hand at release time, so a renamed skill,
a rewritten description or a new skill left them stale (v2.14.8 shipped stale
descriptions; Vibe once lagged 7 skills). The sync scripts also never re-point
an existing link, so an incremental run can leave a link on whichever copy of
a dual-published skill happened to be linked first.

This guard regenerates every mirror from scratch in a throwaway copy of the
working tree and compares the result with what is committed: link names, link
targets and generated file bytes must match exactly. It also checks that every
link resolves to a SKILL.md.

Exit codes:
  0  all mirrors match a fresh regeneration
  1  drift found (listed on stdout; run with --fix to rewrite the mirrors)
  2  a sync script failed or the repo root was not found

Usage:
  python3 scripts/check_harness_mirrors.py            # check (CI)
  python3 scripts/check_harness_mirrors.py --fix      # rewrite mirrors in place
  python3 scripts/check_harness_mirrors.py --json     # machine-readable report
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# name -> (mirror paths relative to the repo root, sync command)
MIRRORS: dict[str, tuple[tuple[str, ...], list[str]]] = {
    "codex": ((".codex/skills", ".codex/skills-index.json"),
              ["scripts/sync-codex-skills.py"]),
    "gemini": ((".gemini/skills", ".gemini/skills-index.json"),
               ["scripts/sync-gemini-skills.py"]),
    "vibe": ((".vibe/skills",),
             ["scripts/sync-vibe-skills.py", "--nested", "--target", ".vibe/skills"]),
    "hermes": ((".hermes/skills",),
               ["scripts/sync-hermes-skills.py", "--target", ".hermes/skills"]),
}
MIRROR_ROOTS = (".codex/skills", ".codex/skills-index.json", ".gemini", ".vibe", ".hermes")


def _listed_files(repo: Path) -> list[str]:
    """Tracked plus untracked-but-not-ignored files: what a commit would hold.

    Using git's view keeps gitignored maintainer folders (eval-workspace/,
    documentation/ ...) out of the copy, so a stray local SKILL.md there
    cannot make a local run disagree with CI."""
    out = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=repo, check=True, capture_output=True,
    ).stdout.decode("utf-8", "surrogateescape")
    return [p for p in out.split("\0") if p]


def _in_mirror(rel: str) -> bool:
    return any(rel == m or rel.startswith(m + "/") for m in MIRROR_ROOTS)


def _copy_tree(repo: Path, dest: Path) -> None:
    for rel in _listed_files(repo):
        if _in_mirror(rel):
            continue
        src = repo / rel
        dst = dest / rel
        if not src.exists() and not src.is_symlink():
            continue  # deleted in the working tree but still in the index
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_symlink():
            os.symlink(os.readlink(src), dst)
        else:
            shutil.copy2(src, dst)


def _snapshot(root: Path, paths: tuple[str, ...]) -> dict[str, tuple[str, str]]:
    """Map relative path -> (kind, value): ('link', target) or ('file', bytes hex digest)."""
    import hashlib

    snap: dict[str, tuple[str, str]] = {}

    def add(p: Path) -> None:
        rel = p.relative_to(root).as_posix()
        if p.is_symlink():
            snap[rel] = ("link", os.readlink(p))
        elif p.is_file():
            snap[rel] = ("file", hashlib.sha256(p.read_bytes()).hexdigest())

    for rel in paths:
        base = root / rel
        if base.is_symlink() or base.is_file():
            add(base)
        elif base.is_dir():
            for dirpath, dirnames, filenames in os.walk(base):
                d = Path(dirpath)
                for name in sorted(dirnames):
                    if (d / name).is_symlink():
                        add(d / name)
                for name in sorted(filenames):
                    add(d / name)
    return snap


def _dangling(root: Path, snap: dict[str, tuple[str, str]]) -> list[str]:
    bad = []
    for rel, (kind, _) in snap.items():
        if kind != "link":
            continue
        p = root / rel
        if p.is_dir():
            if not (p / "SKILL.md").is_file():
                bad.append(f"{rel}: no SKILL.md behind the link")
        elif not p.exists():
            bad.append(f"{rel}: link target does not exist")
    return bad


def _index_delta(have: Path, want: Path) -> str:
    """Name the skills whose entry differs between two skills-index.json files."""
    try:
        a = {s.get("name"): s for s in json.loads(have.read_text())["skills"]}
        b = {s.get("name"): s for s in json.loads(want.read_text())["skills"]}
    except (ValueError, KeyError, TypeError, OSError):
        return ""
    names = sorted(n for n in set(a) | set(b) if a.get(n) != b.get(n))
    if not names:
        return " (entry order or header fields)"
    shown = ", ".join(str(n) for n in names[:10])
    return f" (entries: {shown}{' ...' if len(names) > 10 else ''})"


def regenerate(repo: Path, work: Path) -> dict[str, str]:
    """Copy the tree into work/ and run every sync there. Returns name -> error."""
    _copy_tree(repo, work)
    errors = {}
    env = dict(os.environ, HOME=str(work / ".home"), PYTHONDONTWRITEBYTECODE="1")
    for name, (_, cmd) in MIRRORS.items():
        proc = subprocess.run([sys.executable, *cmd], cwd=work, env=env,
                              capture_output=True, text=True)
        if proc.returncode != 0:
            errors[name] = (proc.stdout + proc.stderr).strip()[-2000:]
    return errors


def compare(repo: Path, work: Path) -> dict[str, dict[str, list[str]]]:
    report = {}
    for name, (paths, _) in MIRRORS.items():
        have = _snapshot(repo, paths)
        want = _snapshot(work, paths)
        missing = sorted(set(want) - set(have))
        extra = sorted(set(have) - set(want))
        changed = sorted(k for k in set(want) & set(have) if want[k] != have[k])
        detail = []
        for k in changed:
            if have[k][0] == "link" or want[k][0] == "link":
                detail.append(f"{k}: committed {have[k][1]!r}, expected {want[k][1]!r}")
            else:
                detail.append(f"{k}: content differs from a fresh sync"
                              + _index_delta(repo / k, work / k))
        report[name] = {
            "missing": missing,
            "extra": extra,
            "changed": detail,
            "dangling": _dangling(repo, have),
        }
    return report


def fix(repo: Path, work: Path) -> None:
    for name, (paths, _) in MIRRORS.items():
        for rel in paths:
            dst = repo / rel
            if dst.is_symlink() or dst.is_file():
                dst.unlink()
            elif dst.is_dir():
                shutil.rmtree(dst)
            src = work / rel
            if src.is_dir() and not src.is_symlink():
                shutil.copytree(src, dst, symlinks=True)
            elif src.exists() or src.is_symlink():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst, follow_symlinks=False)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fix", action="store_true",
                    help="rewrite the committed mirrors from a fresh regeneration")
    ap.add_argument("--json", action="store_true", help="print a JSON report")
    args = ap.parse_args()

    if not (REPO_ROOT / ".git").exists():
        print(f"error: {REPO_ROOT} is not a git checkout", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="harness-mirrors-") as tmp:
        work = Path(tmp)
        errors = regenerate(REPO_ROOT, work)
        if errors:
            for name, err in errors.items():
                print(f"error: {name} sync failed:\n{err}", file=sys.stderr)
            return 2
        if args.fix:
            fix(REPO_ROOT, work)
        report = compare(REPO_ROOT, work)

    drift = {n: r for n, r in report.items() if any(r.values())}
    if args.json:
        print(json.dumps({"status": "drift" if drift else "ok", "mirrors": report}, indent=2))
        return 1 if drift else 0

    for name, (paths, _) in MIRRORS.items():
        r = report[name]
        n = sum(len(v) for v in r.values())
        print(f"[{'FAIL' if n else ' OK '}] {name:<7} {', '.join(paths)}"
              + (f"  ({n} problem{'s' if n != 1 else ''})" if n else ""))
        for label in ("missing", "extra", "changed", "dangling"):
            items = r[label]
            for item in items[:25]:
                print(f"         {label}: {item}")
            if len(items) > 25:
                print(f"         ... {len(items) - 25} more {label}")
    if drift:
        print("\nMirrors drifted from the source skills. Regenerate them with:\n"
              "  python3 scripts/check_harness_mirrors.py --fix\n"
              "then commit the changes under .codex/ .gemini/ .vibe/ .hermes/.")
        return 1
    if args.fix:
        print("\nMirrors regenerated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
