#!/usr/bin/env python3
"""Audit what Claude Code actually loads from CLAUDE.md files, layer by layer.

A team's instructions to Claude live in several layers that are concatenated
at session start: managed policy, the user's ~/.claude/CLAUDE.md, every
CLAUDE.md from the filesystem root down to the working directory, CLAUDE.local.md,
.claude/rules/*.md, and whatever those files pull in with @imports (at most four
hops deep). Nobody reads the concatenation, so nobody sees the duplicated rule,
the import that silently points nowhere, or the API key pasted into a shared file.

This script resolves the layers for one repository and reports:

  L1  [WARN]    a file longer than 200 lines (the docs' recommended ceiling)
  L2  [WARN]    an @import that does not resolve (the instruction silently disappears)
  L3  [WARN]    an @import chain deeper than 4 hops (not loaded past the limit)
  L4  [WARN]    an @import cycle
  L5  [BLOCKER] a credential in a committed memory file
  L6  [WARN]    CLAUDE.local.md tracked by git (personal notes shipped to the team)
  L7  [WARN]    the same instruction repeated in two or more files
  L8  [WARN]    resident instructions above --budget tokens (heuristic, chars/4)
  L9  [WARN]    machine-specific paths (/Users/name, /home/name, C:\\Users) in a shared file
  L10 [WARN]    possible contradiction: "always X" in one file, "never X" in another
  L11 [INFO]    AGENTS.md present next to CLAUDE.md (Claude Code reads AGENTS.md only
                when there is no CLAUDE.md, so the two can drift)

Deterministic, stdlib only. Runs `git ls-files` for L6 and nothing else.

Exit codes:
    0  clean
    2  warnings
    3  invalid input
    4  blocker
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import defaultdict

MAX_HOPS = 4
IMPORT_RE = re.compile(r"(?<![\w`@])@((?:~|\.{1,2})?/?[\w.-]+(?:/[\w.-]+)*\.?[\w-]*)")
SECRET_RE = re.compile(r"(sk-ant-[A-Za-z0-9_-]{10,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"
                       r"|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY"
                       r"|(?i:(password|api[_-]?key|secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9/+_-]{12,}))")
PERSONAL_PATH = re.compile(r"(/Users/[A-Za-z0-9._-]+|/home/(?!claude\b)[A-Za-z0-9._-]+|C:\\\\?Users\\\\?[A-Za-z0-9._-]+)")
POLARITY = re.compile(r"\b(always|never|do not|don't|must not|must)\s+([a-z][a-z-]+(?:\s+[a-z][a-z-]+){0,2})", re.I)

STOP = {"use", "the", "a", "an", "to", "any", "run", "be", "include", "add", "make", "keep", "do", "write", "commit", "create", "change"}

SAMPLE_TREE = {
    "CLAUDE.md": "# Project\nRun the full test suite before every commit.\nAlways use pnpm for installs.\nSee @docs/style.md and @docs/missing.md\n"
                 "Local DB lives at /Users/alice/dev/db.sqlite\n",
    "docs/style.md": "Prefer named exports.\nRun the full test suite before every commit.\n@style.md\n",
    ".claude/rules/api.md": "---\npaths: src/api/**\n---\nNever use pnpm in the api package.\n",
    "CLAUDE.local.md": "staging token: api_key = 'abcd1234efgh5678ijkl'\n",
    "AGENTS.md": "# Agents\nUse npm.\n",
    "packages/web/CLAUDE.md": "Web package uses Vite.\n",
}


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return None


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def frontmatter_paths(text):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    return bool(m and re.search(r"^paths\s*:", m.group(1), re.M))


def resolve_imports(path, text, home, findings, chain, loaded):
    for raw in IMPORT_RE.findall(strip_code(text)):
        if "/" not in raw and "." not in raw:
            continue  # an @mention, not a path
        target = os.path.expanduser(raw) if raw.startswith("~") else os.path.normpath(
            os.path.join(os.path.dirname(path), raw))
        if target in chain:
            findings.append(("L4", "WARN", path, f"import cycle via @{raw}"))
            continue
        body = read(target)
        if body is None:
            findings.append(("L2", "WARN", path, f"@{raw} does not resolve; that instruction is never loaded"))
            continue
        if len(chain) >= MAX_HOPS:
            findings.append(("L3", "WARN", path, f"@{raw} is beyond {MAX_HOPS} import hops and is not loaded"))
            continue
        loaded.append(("import", target, body))
        resolve_imports(target, body, home, findings, chain + [target], loaded)


def tracked(repo, rel):
    try:
        return subprocess.run(["git", "-C", repo, "ls-files", "--error-unmatch", rel],
                              capture_output=True, timeout=10).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def audit(repo, user_md, managed_md, budget, use_git=True):
    repo = os.path.abspath(repo)
    if not os.path.isdir(repo):
        _fail(f"not a directory: {repo}")
    findings, resident, on_demand = [], [], []
    layers = [("managed", managed_md), ("user", user_md),
              ("project", os.path.join(repo, "CLAUDE.md")), ("project", os.path.join(repo, ".claude", "CLAUDE.md")),
              ("local", os.path.join(repo, "CLAUDE.local.md"))]
    for layer, path in layers:
        body = read(path) if path else None
        if body is not None:
            resident.append((layer, path, body))
    rules_dir = os.path.join(repo, ".claude", "rules")
    for dirpath, _, files in os.walk(rules_dir):
        for f in sorted(files):
            if f.endswith(".md"):
                p = os.path.join(dirpath, f)
                body = read(p) or ""
                (on_demand if frontmatter_paths(body) else resident).append(("rule", p, body))
    for dirpath, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "vendor", "dist", "build")]
        if dirpath != repo and "CLAUDE.md" in files:
            p = os.path.join(dirpath, "CLAUDE.md")
            on_demand.append(("subdir", p, read(p) or ""))

    loaded = []
    for layer, path, body in resident:
        resolve_imports(path, body, os.path.expanduser("~"), findings, [path], loaded)
    resident += loaded

    shared = {p for layer, p, _ in resident + on_demand if layer in ("project", "rule", "subdir", "import") and p.startswith(repo)}
    lines_seen = defaultdict(set)
    polarity = defaultdict(set)
    for layer, path, body in resident + on_demand:
        n = body.count("\n") + 1
        if n > 200:
            findings.append(("L1", "WARN", path, f"{n} lines; split into .claude/rules/ or imports"))
        if SECRET_RE.search(body) and (path in shared or path.endswith("CLAUDE.local.md")):
            sev = "BLOCKER" if path in shared or tracked(repo, os.path.relpath(path, repo)) else "WARN"
            findings.append(("L5", sev, path, "looks like a credential; memory files are plaintext context"))
        if path in shared and PERSONAL_PATH.search(body):
            findings.append(("L9", "WARN", path, f"machine-specific path {PERSONAL_PATH.search(body).group(0)} in a shared file"))
        for line in strip_code(body).splitlines():
            if line.lstrip().startswith("#") or "updated" in line.lower():
                continue
            norm = " ".join(re.sub(r"[^\w\s]", " ", line.lower()).split())
            if len(norm.split()) >= 5:
                lines_seen[norm].add(path)
            for word, obj in POLARITY.findall(line):
                words = [w for w in obj.lower().split() if w not in STOP]
                if words:
                    polarity[words[0]].add((word.lower() in ("always", "must"), path))
    resident_paths = {p for _, p, _ in resident}
    for norm, paths in lines_seen.items():
        if len(paths) > 1 and paths & resident_paths:  # on-demand files rarely load together
            findings.append(("L7", "WARN", sorted(paths)[0], f"repeated in {len(paths)} files: \"{norm[:70]}\""))
    for obj, marks in polarity.items():
        pos_files = {p for pos, p in marks if pos}
        neg_files = {p for pos, p in marks if not pos}
        if pos_files and neg_files and pos_files != neg_files:
            findings.append(("L10", "WARN", sorted(pos_files)[0], f"'always/must {obj}' vs 'never {obj}' in {os.path.basename(sorted(neg_files)[0])}; scope it or pick one"))

    if use_git and tracked(repo, "CLAUDE.local.md"):
        findings.append(("L6", "WARN", os.path.join(repo, "CLAUDE.local.md"), "tracked by git; add it to .gitignore"))
    if os.path.exists(os.path.join(repo, "AGENTS.md")) and os.path.exists(os.path.join(repo, "CLAUDE.md")):
        findings.append(("L11", "INFO", os.path.join(repo, "AGENTS.md"), "ignored while CLAUDE.md exists; import it (@AGENTS.md) or keep them in sync"))

    resident_tokens = sum(len(b) for _, _, b in resident) // 4
    if resident_tokens > budget:
        findings.append(("L8", "WARN", repo, f"~{resident_tokens} tokens load every session (budget {budget})"))

    rel = lambda p: os.path.relpath(p, repo) if p and p.startswith(repo) else p
    out = [{"id": i, "severity": s, "file": rel(f), "message": m} for i, s, f, m in findings]
    order = {"BLOCKER": 0, "WARN": 1, "INFO": 2}
    out.sort(key=lambda f: (order[f["severity"]], f["id"]))
    sev = [f["severity"] for f in out]
    verdict, code = ("BLOCKED", 4) if "BLOCKER" in sev else (("WARNINGS", 2) if "WARN" in sev else ("CLEAN", 0))
    return {"verdict": verdict, "resident_tokens_estimate": resident_tokens, "budget": budget,
            "resident_files": [{"layer": l, "file": rel(p), "lines": b.count("\n") + 1, "tokens": len(b) // 4} for l, p, b in resident],
            "on_demand_files": [{"layer": l, "file": rel(p), "tokens": len(b) // 4} for l, p, b in on_demand],
            "findings": out}, code


def render(r):
    out = [f"CLAUDE.md layering: {r['verdict']}  (~{r['resident_tokens_estimate']} resident tokens, budget {r['budget']})",
           "  loaded at session start:"]
    out += [f"    {f['layer']:<8} {f['file']}  ({f['lines']} lines, ~{f['tokens']} tok)" for f in r["resident_files"]]
    if r["on_demand_files"]:
        out.append("  loaded on demand: " + ", ".join(f["file"] for f in r["on_demand_files"]))
    out += [f"  [{f['severity']}] {f['id']} {f['file']}: {f['message']}" for f in r["findings"]]
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Resolve CLAUDE.md layers and @imports for a repo; flag broken imports, duplicates, conflicts, secrets and bloat.")
    p.add_argument("--repo", help="repository root (the working directory Claude Code starts in)")
    p.add_argument("--user-md", default=os.path.expanduser("~/.claude/CLAUDE.md"), help="user memory file (default ~/.claude/CLAUDE.md)")
    p.add_argument("--managed-md", help="managed CLAUDE.md, e.g. /etc/claude-code/CLAUDE.md")
    p.add_argument("--budget", type=int, default=6000, help="resident token budget before L8 warns (default 6000, heuristic)")
    p.add_argument("--sample", action="store_true", help="audit an embedded sample tree with known problems")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()
    if a.sample:
        with tempfile.TemporaryDirectory() as tmp:
            for rel_path, body in SAMPLE_TREE.items():
                full = os.path.join(tmp, rel_path)
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "w", encoding="utf-8") as fh:
                    fh.write(body)
            report, code = audit(tmp, None, None, a.budget, use_git=False)
    elif a.repo:
        report, code = audit(a.repo, a.user_md, a.managed_md, a.budget)
    else:
        p.error("give --repo, or --sample")
    print(json.dumps(report, indent=2) if a.output == "json" else render(report))
    return code


if __name__ == "__main__":
    sys.exit(main())
