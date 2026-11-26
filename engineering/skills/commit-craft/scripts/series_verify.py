#!/usr/bin/env python3
"""Prove every commit in a series builds: run a command at each commit before you push.

A series that only passes at its tip breaks `git bisect` and every revert of a single
commit. This checks out each commit of --range, oldest first, in a throwaway detached
worktree (your working tree, index and stash are never touched), runs --cmd there, and
reports the first commit that fails. It also scans what each commit adds for debug
leftovers that pass tests but should never land.

Findings
  BROKEN_COMMIT     --cmd exits non-zero at this commit                        BLOCKER
  TIMEOUT           --cmd ran past --timeout seconds                           BLOCKER
  FOCUSED_TEST      it.only / describe.only / fit( / test.only / @focus added  BLOCKER
                    (the suite silently runs one test and goes green)
  DEBUGGER_LEFT     breakpoint() / pdb.set_trace() / debugger; / binding.pry   BLOCKER
  SKIP_ADDED        a new skip marker (@pytest.mark.skip, it.skip, xit(, t.Skip) WARN
  PRINT_DEBUG       a new console.log / print( / dbg! / var_dump line          WARN
                    (only in non-test source; may be intended)

Exit codes: 0 every commit passes, 2 warnings only, 3 bad input (no repo, empty range,
no --cmd), 4 a commit fails or a blocker is added. Deterministic, stdlib only; the only
process it runs besides git is the command you pass.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

EXIT = {"CLEAN": 0, "FINDINGS": 2, "BAD_INPUT": 3, "BLOCKED": 4}
CODE_EXT = re.compile(r"\.(py|js|jsx|ts|tsx|mjs|cjs|rb|go|rs|php|java|kt|swift|vue|svelte)$")
TESTY = re.compile(r"(^|/)(tests?|__tests__|spec|specs)/|[._-](test|spec)\.\w+$|(^|/)test_[^/]+\.py$|_test\.go$")
RULES = [
    ("FOCUSED_TEST", "BLOCKER", re.compile(r"\b(it|describe|test|context)\.only\s*\(|^\s*f(it|describe)\s*\(|@focus\b|\.only\(\s*['\"`]")),
    ("DEBUGGER_LEFT", "BLOCKER", re.compile(r"\bbreakpoint\(\s*\)|\bpdb\.set_trace\(|\bipdb\.set_trace\(|^\s*debugger\s*;?\s*$|\bbinding\.(pry|irb)\b|\bbyebug\b")),
    ("SKIP_ADDED", "WARN", re.compile(r"@pytest\.mark\.skip\b|@unittest\.skip\b|\b(it|describe|test)\.skip\s*\(|^\s*x(it|describe)\s*\(|\bt\.Skip\(")),
    ("PRINT_DEBUG", "WARN", re.compile(r"^\s*console\.(log|debug)\(|^\s*print\(|\bdbg!\(|\bvar_dump\(|\bpp\s")),
]


def git(args, cwd, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise ValueError(f"git {' '.join(args)}: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout


def added_lines(repo, sha):
    """Yield (path, line) for every line this commit adds."""
    out = git(["show", "--format=", "--unified=0", "--no-color", "--no-ext-diff", sha], repo)
    path = None
    for ln in out.splitlines():
        if ln.startswith("+++ "):
            path = ln[6:] if ln.startswith("+++ b/") else None
        elif ln.startswith("+") and not ln.startswith("+++") and path:
            yield path, ln[1:]


def scan(repo, sha):
    found = []
    for path, line in added_lines(repo, sha):
        if not CODE_EXT.search(path):
            continue
        for code, sev, rx in RULES:
            if code == "PRINT_DEBUG" and (TESTY.search(path) or path.endswith(".py") and "scripts/" in path):
                continue
            if rx.search(line):
                found.append({"code": code, "severity": sev, "file": path, "line": line.strip()[:120]})
                break
    return found


def verify(repo, rng, cmd, timeout, keep_going):
    shas = git(["rev-list", "--reverse", rng], repo).split()
    if not shas:
        raise ValueError(f"range {rng} has no commits")
    tmp = tempfile.mkdtemp(prefix="series-verify-")
    wt = os.path.join(tmp, "wt")
    git(["worktree", "add", "--detach", "--quiet", wt, shas[0]], repo)
    commits, stopped = [], False
    try:
        for sha in shas:
            subject = git(["log", "-1", "--format=%s", sha], repo).strip()
            entry = {"sha": sha[:12], "subject": subject, "findings": scan(repo, sha)}
            if stopped:
                entry["status"] = "NOT_RUN"
                commits.append(entry)
                continue
            git(["checkout", "--detach", "--quiet", "--force", sha], wt)
            git(["clean", "-fdxq"], wt)
            t0 = time.monotonic()
            try:
                r = subprocess.run(cmd, shell=True, cwd=wt, capture_output=True, text=True, timeout=timeout)  # noqa: SEC-AUDITOR (runs the user's own --cmd, e.g. 'npm test && npm run lint', like git rebase -x)
                entry["status"] = "PASS" if r.returncode == 0 else "FAIL"
                entry["exit"] = r.returncode
                if r.returncode:
                    entry["findings"].insert(0, {"code": "BROKEN_COMMIT", "severity": "BLOCKER", "file": "",
                                                 "line": f"`{cmd}` exited {r.returncode}"})
                    entry["output_tail"] = ((r.stdout or "") + (r.stderr or "")).strip().splitlines()[-15:]
            except subprocess.TimeoutExpired:
                entry["status"] = "FAIL"
                entry["findings"].insert(0, {"code": "TIMEOUT", "severity": "BLOCKER", "file": "",
                                             "line": f"`{cmd}` ran past {timeout}s"})
            entry["seconds"] = round(time.monotonic() - t0, 1)
            if entry["status"] == "FAIL" and not keep_going:
                stopped = True
            commits.append(entry)
    finally:
        git(["worktree", "remove", "--force", wt], repo, check=False)
        shutil.rmtree(tmp, ignore_errors=True)  # noqa: SEC-AUDITOR (our own mkdtemp dir)
    allf = [f for c in commits for f in c["findings"]]
    verdict = ("BLOCKED" if any(f["severity"] == "BLOCKER" for f in allf)
               else "FINDINGS" if allf else "CLEAN")
    first = next((c["sha"] for c in commits if c.get("status") == "FAIL"), None)
    return {"verdict": verdict, "range": rng, "cmd": cmd, "commits": commits, "first_failing": first,
            "passed": sum(1 for c in commits if c.get("status") == "PASS"), "total": len(commits)}


def make_sample():
    """A three-commit repo: commit 2 breaks the test and adds a focused test, commit 3 fixes the code."""
    d = tempfile.mkdtemp(prefix="series-verify-sample-")
    env_git = ["-c", "user.name=Sample", "-c", "user.email=sample@example.invalid", "-c", "commit.gpgsign=false"]
    git(["init", "-q", "-b", "main"], d)

    def commit(files, msg):
        for name, body in files.items():
            p = os.path.join(d, name)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w") as fh:
                fh.write(body)
        git(["add", "-A"], d)
        git([*env_git, "commit", "-q", "-m", msg], d)

    commit({"calc.py": "def total(xs):\n    return sum(xs)\n",
            "check.py": "from calc import total\nassert total([1, 2]) == 3\n"}, "feat: add total")
    commit({"calc.py": "def total(xs, tax=0.0):\n    return sum(xs) * tax\n",
            "spec/calc.test.js": "it.only('adds tax', () => {});\n"}, "feat: add tax to total")
    commit({"calc.py": "def total(xs, tax=0.0):\n    return sum(xs) * (1 + tax)\n"}, "fix: apply tax as a rate")
    return d, f"{sys.executable} check.py"


def render(res):
    lines = [f"series verify {res['range']} with `{res['cmd']}`: {res['verdict']} "
             f"({res['passed']}/{res['total']} commits pass)"]
    for c in res["commits"]:
        lines.append(f"  {c.get('status', '?'):7} {c['sha']} {c['subject']}")
        for f in c["findings"]:
            where = f" {f['file']}:" if f["file"] else ""
            lines.append(f"          [{f['severity']}] {f['code']}{where} {f['line']}")
        for t in c.get("output_tail", [])[-5:]:
            lines.append(f"          | {t}")
    if res["first_failing"]:
        lines.append(f"  First failing commit {res['first_failing']}: fix it there (git rebase -i, edit) "
                     f"so every commit builds, then run this again.")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog="Exit codes: 0 all pass, 2 warnings, 3 bad input, 4 a commit fails or a blocker was added.")
    ap.add_argument("--range", default="@{upstream}..HEAD", help="commits to verify (default @{upstream}..HEAD)")
    ap.add_argument("--cmd", help="command that must pass at every commit, e.g. 'npm test' or 'make check'")
    ap.add_argument("--repo", default=".", help="repository path (default .)")
    ap.add_argument("--timeout", type=int, default=900, help="seconds per commit (default 900)")
    ap.add_argument("--keep-going", action="store_true", help="run the command at every commit even after one fails")
    ap.add_argument("--sample", action="store_true", help="build a throwaway three-commit repo and verify it")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    sample_dir = None
    try:
        if a.sample:
            sample_dir, a.cmd = make_sample()
            a.repo, a.range, a.keep_going = sample_dir, "HEAD", True
        if not a.cmd:
            raise ValueError("--cmd is required: the command that must pass at every commit")
        git(["rev-parse", "--git-dir"], a.repo)
        res = verify(a.repo, a.range, a.cmd, a.timeout, a.keep_going)
    except (OSError, ValueError) as exc:
        print(json.dumps({"verdict": "BAD_INPUT", "error": str(exc)}) if a.output == "json" else f"BAD_INPUT: {exc}")
        return EXIT["BAD_INPUT"]
    finally:
        if sample_dir:
            shutil.rmtree(sample_dir, ignore_errors=True)  # noqa: SEC-AUDITOR (our own mkdtemp sample repo)
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
