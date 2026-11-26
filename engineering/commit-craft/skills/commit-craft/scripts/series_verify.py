#!/usr/bin/env python3
"""Prove every commit in a series builds: run a command at each commit before you push.

A series that only passes at its tip breaks `git bisect` and every revert of a single
commit. This checks out each commit of --range, oldest first, in a throwaway detached
worktree (your working tree, index and stash are never touched), runs --cmd there, and
reports the first commit that fails. The worktree starts from the commit alone, without
node_modules, .venv or build caches, so pass --setup with your install step (e.g. npm ci) for a
project that needs installed dependencies, or every commit fails for the wrong reason.
Ignored files (node_modules, build output) are kept between commits for speed, so a stale
artifact from one commit can make the next pass; --strict wipes them at every commit
(git clean -x) and needs --setup to rebuild. On a timeout the whole process group is
killed, so no test runner or server is left behind. The last lines of a failing command's
output are printed as-is: if your tests log secrets, they appear in the report. It also scans what each commit adds for debug
leftovers that pass tests but should never land.

Findings
  SETUP_FAILED      --setup exits non-zero at this commit                      BLOCKER
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
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time

EXIT = {"CLEAN": 0, "FINDINGS": 2, "BAD_INPUT": 3, "BLOCKED": 4}
CODE_EXT = re.compile(r"\.(py|js|jsx|ts|tsx|mjs|cjs|rb|go|rs|php|java|kt|swift|vue|svelte)$")
TESTY = re.compile(r"(^|/)(tests?|__tests__|spec|specs)/|[._-](test|spec)\.\w+$|(^|/)test_[^/]+\.py$|_test\.go$")
RULES = [
    ("FOCUSED_TEST", "BLOCKER", re.compile(r"\b(it|describe|test|context)\.only\s*\(|^\s*f(it|describe)\s*\(|^\s*@focus\b")),
    ("DEBUGGER_LEFT", "BLOCKER", re.compile(r"\bbreakpoint\(\s*\)|\bpdb\.set_trace\(|\bipdb\.set_trace\(|^\s*debugger\s*;?\s*$|\bbinding\.(pry|irb)\b|^\s*byebug\s*$")),
    ("SKIP_ADDED", "WARN", re.compile(r"@pytest\.mark\.skip\b|@unittest\.skip\b|\b(it|describe|test)\.skip\s*\(|^\s*x(it|describe)\s*\(|\bt\.Skip\(")),
    ("PRINT_DEBUG", "WARN", re.compile(r"^\s*console\.(log|debug)\(|^\s*print\(|\bdbg!\(|\bvar_dump\(")),
]


def git(args, cwd, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise ValueError(f"git {' '.join(args)}: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout


def added_lines(repo, sha):
    """Yield (path, line) for every line this commit adds."""
    # Diff against the first parent, so a merge shows what it brings in (git show would print
    # a combined diff); a root commit diffs against the empty tree.
    parents = git(["rev-list", "--parents", "-n", "1", sha], repo).split()[1:]
    base = parents[0] if parents else git(["hash-object", "-t", "tree", os.devnull], repo).strip()  # empty tree, SHA-1 or SHA-256
    out = git(["-c", "core.quotepath=off", "diff", "--unified=0", "--no-color", "--no-ext-diff", base, sha], repo)
    path, in_header = None, False
    for ln in out.splitlines():
        if ln.startswith("diff --git "):
            path, in_header = None, True
        elif in_header and ln.startswith("+++ "):
            path = ln[6:].rstrip("\t") if ln.startswith("+++ b/") else None
        elif ln.startswith("@@"):
            in_header = False
        elif not in_header and ln.startswith("+") and path:
            yield path, ln[1:]


def scan(repo, sha):
    found = []
    for path, line in added_lines(repo, sha):
        if not CODE_EXT.search(path):
            continue
        for code, sev, rx in RULES:
            if code == "PRINT_DEBUG" and TESTY.search(path):
                continue
            if rx.search(line):
                found.append({"code": code, "severity": sev, "file": path, "line": line.strip()[:120]})
                break
    return found


def run_cmd(cmd, cwd, timeout):
    """Run cmd in its own process group so a timeout kills test runners and servers it started."""
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,  # noqa: SEC-AUDITOR (runs the user's own --cmd / --setup, like git rebase -x)
                         text=True, start_new_session=True)
    try:
        out, _ = p.communicate(timeout=timeout)
        return p.returncode, out or ""
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        p.communicate()
        return None, ""


def verify(repo, rng, cmd, timeout, keep_going, setup=None, strict=False):
    shas = git(["rev-list", "--reverse", rng], repo).split()
    if not shas:
        raise ValueError(f"range {rng} has no commits")
    commits, stopped = [], False
    tmp = tempfile.mkdtemp(prefix="series-verify-")
    wt = os.path.join(tmp, "wt")
    try:
        git(["worktree", "add", "--detach", "--quiet", wt, shas[0]], repo)
        for sha in shas:
            subject = git(["log", "-1", "--format=%s", sha], repo).strip()
            entry = {"sha": sha[:12], "subject": subject, "findings": scan(repo, sha)}
            if stopped:
                entry["status"] = "NOT_RUN"
                commits.append(entry)
                continue
            git(["checkout", "--detach", "--quiet", "--force", sha], wt)
            git(["clean", "-fdxq" if strict else "-fdq"], wt)  # default keeps ignored files (node_modules) between commits
            t0 = time.monotonic()
            for step, code_fail in ((setup, "SETUP_FAILED"), (cmd, "BROKEN_COMMIT")):
                if not step:
                    continue
                rc, out = run_cmd(step, wt, timeout)
                if rc == 0:
                    continue
                entry["status"] = "FAIL"
                entry["exit"] = rc
                entry["failed_step"] = "setup" if step is setup and setup != cmd else "cmd"
                if rc is None:
                    entry["findings"].insert(0, {"code": "TIMEOUT", "severity": "BLOCKER", "file": "",
                                                 "line": f"`{step}` ran past {timeout}s (process group killed)"})
                else:
                    entry["findings"].insert(0, {"code": code_fail, "severity": "BLOCKER", "file": "",
                                                 "line": f"`{step}` exited {rc}"})
                    entry["output_tail"] = out.strip().splitlines()[-15:]
                break
            else:
                entry["status"] = "PASS"
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
    first_c = next((c for c in commits if c.get("status") == "FAIL"), None)
    first = first_c["sha"] if first_c else None
    return {"verdict": verdict, "range": rng, "cmd": cmd, "commits": commits, "first_failing": first,
            "first_failing_step": first_c.get("failed_step") if first_c else None,
            "strict": strict, "passed": sum(1 for c in commits if c.get("status") == "PASS"), "total": len(commits)}


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
    return d, f"{shlex.quote(sys.executable)} check.py"


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
    if not res.get("strict") and res["passed"]:
        lines.append("  Ignored files (node_modules, build output) were kept between commits; a stale artifact can "
                     "make a broken commit pass. Use --strict --setup '...' for a hermetic run.")
    if res["first_failing"] and res.get("first_failing_step") == "setup":
        lines.append(f"  --setup failed at {res['first_failing']}: check the environment (network, toolchain, "
                     f"lockfile) before blaming the code; the commit's own test command never ran.")
    elif res["first_failing"]:
        lines.append(f"  First failing commit {res['first_failing']}: fix it there (git rebase -i, edit) "
                     f"so every commit builds, then run this again.")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog="Exit codes: 0 all pass, 2 warnings, 3 bad input, 4 a commit fails or a blocker was added.")
    ap.add_argument("--range", default="@{upstream}..HEAD", help="commits to verify (default @{upstream}..HEAD)")
    ap.add_argument("--cmd", help="command that must pass at every commit, e.g. 'npm test' or 'make check'")
    ap.add_argument("--setup", help="command run before --cmd at every commit, e.g. 'npm ci' (your project's install step): "
                    "the worktree starts without node_modules, .venv or build caches")
    ap.add_argument("--strict", action="store_true", help="wipe ignored files at every commit (hermetic; pair with --setup)")
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
        if "@{upstream}" in a.range and subprocess.run(["git", "rev-parse", "--verify", "-q", "@{upstream}"], cwd=a.repo,
                                                        capture_output=True).returncode != 0:
            raise ValueError("this branch has no upstream; pass --range, e.g. --range origin/main..HEAD")
        res = verify(a.repo, a.range, a.cmd, a.timeout, a.keep_going, a.setup, a.strict)
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
