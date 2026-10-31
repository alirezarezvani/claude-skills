#!/usr/bin/env python3
"""Turn a tangled working tree into a planned commit series a reviewer can read one commit at a time.

Reads `git diff HEAD` plus untracked files by default, or a unified diff file.
Each changed file gets a role from its path and its hunks, then files are grouped
into commits in an order where each one should still build:

  1 build      manifests and their lockfiles together            build(deps)
  2 move       pure renames (100% similar), apart from edits    refactor
  3 style      files whose every hunk is whitespace-only         style
  4 change     a source file with its changed test is one commit;
               other source is grouped by module                 feat|fix|refactor (you decide)
  5 test       tests with no changed source sibling              test
  6 docs       documentation                                     docs
  7 ci         pipelines                                         ci

Flags
  DO_NOT_COMMIT      .env, keys, tfstate: left out of every group              BLOCKER
  MIXED_FORMATTING   whitespace-only and real hunks in one file: git add -p    WARN
  OVERSIZED_GROUP    a group over --max-lines changed lines: split it by hunk  WARN
  TOO_MANY_GROUPS    more than --max-groups commits: merge related modules     WARN
  GENERATED          build output or minified files: should they be in git?   WARN
  MOVE_NEEDS_CALLERS a move whose callers' import edits sit in another group   WARN

The planner cannot know intent: it never picks feat vs fix, and it cannot prove
each commit builds. Run your tests at every commit before pushing
(`git rebase -x "<test command>" <upstream>`). Deterministic, stdlib only.
"""
import argparse
import json
import os
import re
import subprocess
import sys

EXIT = {"SINGLE": 0, "SPLIT": 2, "BAD_INPUT": 3, "BLOCKED": 4}
ORDER = ["build", "move", "style", "change", "test", "docs", "ci", "config", "generated"]
TYPE = {"build": "build(deps)", "move": "refactor", "style": "style", "change": "feat|fix|refactor",
        "test": "test", "docs": "docs", "ci": "ci", "config": "chore", "generated": "chore"}

LOCK_OR_MANIFEST = re.compile(
    r"(^|/)(package(-lock)?\.json|npm-shrinkwrap\.json|yarn\.lock|pnpm-lock\.yaml|bun\.lockb?|poetry\.lock|Pipfile(\.lock)?|"
    r"pyproject\.toml|uv\.lock|[\w.-]+\.lock|requirements[\w.-]*\.(txt|in|lock)|setup\.(py|cfg)|Cargo\.(toml|lock)|go\.(mod|sum)|"
    r"Gemfile(\.lock)?|composer\.(json|lock)|pom\.xml|build\.gradle(\.kts)?|gradle\.lockfile|pubspec\.(yaml|lock)|"
    r"Package\.resolved|mix\.(exs|lock))$")
CI = re.compile(r"(^|/)(\.github/workflows/|\.gitlab-ci\.yml$|Jenkinsfile$|\.circleci/|azure-pipelines\.ya?ml$|\.buildkite/|bitbucket-pipelines\.yml$)")
DOCS = re.compile(r"(\.(md|mdx|rst|adoc|txt)$|(^|/)docs?/)", re.I)
TEST = re.compile(r"((^|/)(tests?|__tests__|spec|specs|e2e)/|(^|/)test_[^/]+\.py$|_test\.(py|go|rb|exs?)$|\.(test|spec)\.[jt]sx?$|Tests?\.(java|kt|cs|swift)$|__snapshots__/)")
GENERATED = re.compile(r"((^|/)(dist|build|out|target|coverage|\.next)/|\.min\.(js|css)$|\.pb\.go$|_pb2\.py$|\.map$)")
CONFIG = re.compile(r"(^|/)\.[\w.-]+$|(^|/)[\w.-]+\.(ya?ml|toml|ini|cfg|conf)$")
DO_NOT_COMMIT = re.compile(r"((^|/)\.env(\.[\w-]+)?$|\.(pem|key|p12|pfx|jks|keystore|kdbx)$|(^|/)id_(rsa|dsa|ecdsa|ed25519)$|\.tfstate(\.backup)?$)")
SAFE_ENV = re.compile(r"\.(example|sample|template|dist|defaults?)$", re.I)
TEST_STEM = [re.compile(p) for p in (r"^test_(.+)$", r"^(.+)_test$", r"^(.+)\.(?:test|spec)$", r"^(.+?)Tests?$")]

SAMPLE_DIFF = """diff --git a/package.json b/package.json
--- a/package.json
+++ b/package.json
@@ -10,1 +10,2 @@
+    "zod": "^3.23.8",
diff --git a/package-lock.json b/package-lock.json
--- a/package-lock.json
+++ b/package-lock.json
@@ -100,0 +101,12 @@
+    "node_modules/zod": {
+      "version": "3.23.8",
+      "resolved": "https://registry.npmjs.org/zod/-/zod-3.23.8.tgz",
+      "integrity": "sha512-placeholder",
+      "license": "MIT"
+    },
+    "x": 1,
+    "y": 2,
+    "z": 3,
+    "w": 4,
+    "v": 5,
+    "u": 6
diff --git a/src/utils/format.ts b/src/lib/format.ts
similarity index 100%
rename from src/utils/format.ts
rename to src/lib/format.ts
diff --git a/src/invoices/validate.ts b/src/invoices/validate.ts
--- a/src/invoices/validate.ts
+++ b/src/invoices/validate.ts
@@ -1,4 +1,4 @@
-import {fmt} from '../utils/format'
+import {fmt} from '../lib/format'
@@ -20,3 +20,9 @@
-export function validate(inv) { return inv.total > 0 }
+export const InvoiceSchema = z.object({ total: z.number().positive(), currency: z.string().length(3) })
+export function validate(inv) {
+  const r = InvoiceSchema.safeParse(inv)
+  if (!r.success) throw new ValidationError(r.error)
+  return true
+}
diff --git a/src/invoices/validate.test.ts b/src/invoices/validate.test.ts
--- a/src/invoices/validate.test.ts
+++ b/src/invoices/validate.test.ts
@@ -5,0 +6,6 @@
+it('rejects a three-letter currency typo', () => {
+  expect(() => validate({ total: 5, currency: 'EU' })).toThrow(ValidationError)
+})
+it('accepts a valid invoice', () => {
+  expect(validate({ total: 5, currency: 'EUR' })).toBe(true)
+})
diff --git a/src/auth/session.ts b/src/auth/session.ts
--- a/src/auth/session.ts
+++ b/src/auth/session.ts
@@ -40,3 +40,3 @@
-  if(expired){
+  if (expired) {
@@ -60,1 +60,2 @@
-  return refresh(token)
+  if (!token) return null
+  return refresh(token)
diff --git a/src/api/routes.ts b/src/api/routes.ts
--- a/src/api/routes.ts
+++ b/src/api/routes.ts
@@ -1,3 +1,3 @@
-const  a = 1
+const a = 1
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -30,0 +31,2 @@
+Invoices are validated with a schema; a bad currency code now fails with a ValidationError.
+
diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -12,1 +12,1 @@
-      node-version: 18
+      node-version: 20
diff --git a/.env.local b/.env.local
new file mode 100644
--- /dev/null
+++ b/.env.local
@@ -0,0 +1 @@
+STRIPE_KEY=placeholder
"""


def parse_diff(text):
    files, cur = [], None
    for raw in text.splitlines():
        if raw.startswith("diff --git "):
            m = re.match(r"diff --git a/(.+?) b/(.+)$", raw)
            cur = {"path": m.group(2) if m else raw.split()[-1], "old_path": m.group(1) if m else None,
                   "hunks": [], "rename": False, "similarity": None, "new": False, "deleted": False, "binary": False}
            files.append(cur)
        elif cur is None:
            continue
        elif raw.startswith("similarity index"):
            cur["similarity"] = int(re.sub(r"\D", "", raw) or 0)
        elif raw.startswith("rename to "):
            cur["rename"], cur["path"] = True, raw[len("rename to "):]
        elif raw.startswith("new file mode"):
            cur["new"] = True
        elif raw.startswith("deleted file mode"):
            cur["deleted"] = True
        elif raw.startswith("Binary files"):
            cur["binary"] = True
        elif raw.startswith("@@"):
            cur["hunks"].append({"add": [], "del": []})
        elif raw.startswith(("+++", "---")):
            continue
        elif cur["hunks"] and raw.startswith("+"):
            cur["hunks"][-1]["add"].append(raw[1:])
        elif cur["hunks"] and raw.startswith("-"):
            cur["hunks"][-1]["del"].append(raw[1:])
    return files


def whitespace_only(hunk):
    squash = lambda lines: "".join("".join(l.split()) for l in lines)
    return bool(hunk["add"] or hunk["del"]) and squash(hunk["add"]) == squash(hunk["del"])


def stem(path):
    base = os.path.basename(path)
    return base.split(".")[0] if not re.search(r"\.(test|spec)\.", base) else base.rsplit(".", 1)[0]


def tested_stem(path):
    s = stem(path)
    for rx in TEST_STEM:
        m = rx.match(s)
        if m:
            return m.group(1).lower()
    return None


def module_of(path, depth):
    parts = path.split("/")[:-1]
    return "/".join(parts[:depth]) or "(root)"


def classify(f):
    p = f["path"]
    churn = sum(len(h["add"]) + len(h["del"]) for h in f["hunks"])
    f["lines"] = churn
    if DO_NOT_COMMIT.search(p) and not SAFE_ENV.search(p):
        return "do_not_commit"
    if f["rename"] and (f["similarity"] or 0) == 100 and not f["hunks"]:
        return "move"
    if GENERATED.search(p):
        return "generated"
    if LOCK_OR_MANIFEST.search(p):
        return "build"
    if CI.search(p):
        return "ci"
    if TEST.search(p):
        return "test"
    if DOCS.search(p):
        return "docs"
    ws = [whitespace_only(h) for h in f["hunks"]]
    f["mixed_formatting"] = bool(ws) and any(ws) and not all(ws)
    if ws and all(ws):
        return "style"
    if CONFIG.search(p):
        return "config"
    return "change"


def plan(files, depth=2, max_lines=400, max_groups=7):
    groups, flags, held = {}, [], []
    for f in files:
        role = classify(f)
        f["role"] = role
        if role == "do_not_commit":
            held.append(f["path"])
            flags.append({"code": "DO_NOT_COMMIT", "severity": "BLOCKER", "file": f["path"],
                          "detail": "secrets file: add it to .gitignore; it is left out of every group"})
            continue
        key = (role, module_of(f["path"], depth)) if role == "change" else (role, "")
        groups.setdefault(key, []).append(f)
        if f.get("mixed_formatting"):
            flags.append({"code": "MIXED_FORMATTING", "severity": "WARN", "file": f["path"],
                          "detail": "whitespace-only hunks next to real ones: stage with `git add -p` and commit the reformat as style first"})
        if role == "generated":
            flags.append({"code": "GENERATED", "severity": "WARN", "file": f["path"],
                          "detail": "build output or minified file: commit it only if the repo deliberately tracks it"})

    # tests ride with the source they test
    sources = {}
    for (role, mod), fs in groups.items():
        if role == "change":
            for f in fs:
                sources.setdefault(stem(f["path"]).lower(), (role, mod))
    # a source file with its own changed test is a unit of change: it gets its own commit
    for f in list(groups.get(("test", ""), [])):
        target = sources.get(tested_stem(f["path"]) or "")
        if not target:
            continue
        src = next(g for g in groups[target] if stem(g["path"]).lower() == tested_stem(f["path"]))
        unit = ("change", target[1] + "::" + stem(src["path"]))
        groups[("test", "")].remove(f)
        if src in groups[target]:
            groups[target].remove(src)
            groups.setdefault(unit, []).append(src)
        groups.setdefault(unit, []).append(f)
        f["attached"] = True
    groups = {k: v for k, v in groups.items() if v}

    # a move commit that leaves callers importing the old path breaks the build at that commit
    for f in files:
        if f.get("role") != "move" or not f.get("old_path"):
            continue
        old = re.sub(r"\.[^./]+$", "", f["old_path"])
        tail = "/".join(old.split("/")[-2:])
        needles = {old, tail, old.replace("/", "."), tail.replace("/", ".")}  # path and dotted (Python, Java) imports
        callers = [g["path"] for g in files if g is not f and any(
            n in line for h in g["hunks"] for line in h["del"] for n in needles)]
        if callers:
            flags.append({"code": "MOVE_NEEDS_CALLERS", "severity": "WARN", "file": f["path"],
                          "detail": "callers still import the old path in this commit; stage their import hunks with the move "
                                    "(`git add -p` " + " ".join(callers) + ") or the build breaks between commits"})

    ordered = sorted(groups.items(), key=lambda kv: (ORDER.index(kv[0][0]), kv[0][1]))
    out = []
    for i, ((role, mod), fs) in enumerate(ordered, 1):
        lines = sum(f["lines"] for f in fs)
        base_mod = mod.split("::")[0]
        scope = base_mod.split("/")[-1] if role == "change" and base_mod != "(root)" else ""
        typ = TYPE[role]
        whole, stage = [], []
        for f in fs:
            if f.get("mixed_formatting"):
                stage.append(f"git add -p -- {f['path']}")
            elif f["rename"] and f.get("old_path"):
                whole += [f["old_path"], f["path"]]
            else:
                whole.append(f["path"])
        if whole:
            stage.insert(0, "git add -A -- " + " ".join(whole) if any(f["rename"] for f in fs) else "git add -- " + " ".join(whole))
        g = {"n": i, "role": role, "module": mod or None, "type": typ,
             "subject_stub": f"{typ.split('|')[0] if role != 'change' else '<feat|fix|refactor>'}{'(' + scope + ')' if scope else ''}: <why, in the imperative>",
             "files": [{"path": f["path"], "lines": f["lines"], "with_source": bool(f.get("attached"))} for f in fs],
             "lines": lines, "stage": stage}
        if lines > max_lines:
            flags.append({"code": "OVERSIZED_GROUP", "severity": "WARN", "group": i,
                          "detail": f"{lines} changed lines (> {max_lines}): split by hunk with `git add -p` or by sub-feature"})
        out.append(g)
    if len(out) > max_groups:
        flags.append({"code": "TOO_MANY_GROUPS", "severity": "WARN",
                      "detail": f"{len(out)} commits (> {max_groups}): merge modules that only make sense together; each commit must still be reviewable alone"})
    return out, flags, held


def git(args):
    proc = subprocess.run(["git", *args], capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def working_tree_diff():
    """git diff HEAD plus untracked files; a plain `mv` (delete + untracked copy) is reported as a rename."""
    deleted = {}
    for path in git(["diff", "HEAD", "--name-only", "--diff-filter=D"]).splitlines():
        try:
            deleted[git(["show", f"HEAD:{path}"])] = path
        except RuntimeError:
            pass
    untracked, renames = [], []
    for path in git(["ls-files", "--others", "--exclude-standard"]).splitlines():
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                body = fh.read()
        except OSError:
            body = ""
        if body in deleted:
            renames.append((deleted.pop(body), path))
        else:
            untracked.append((path, body.splitlines()))
    exclude = [f":(exclude){old}" for old, _ in renames]
    text = git(["diff", "HEAD", "--no-color", "--no-ext-diff", "-M", "-U0", "--", ".", *exclude])
    for old, new in renames:
        text += f"diff --git a/{old} b/{new}\nsimilarity index 100%\nrename from {old}\nrename to {new}\n"
    for path, body in untracked:
        text += f"diff --git a/{path} b/{path}\nnew file mode 100644\n--- /dev/null\n+++ b/{path}\n@@ -0,0 +1,{len(body)} @@\n"
        text += "".join(f"+{l}\n" for l in body)
    return text


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 epilog="Exit codes: 0 one coherent commit · 2 split proposed · 3 bad input · 4 secrets file in the tree",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--diff", help="unified diff file ('-' for stdin) instead of the working tree")
    src.add_argument("--sample", action="store_true", help="plan a built-in tangled diff")
    ap.add_argument("--depth", type=int, default=2, help="path depth that defines a module (default 2: src/invoices)")
    ap.add_argument("--max-lines", type=int, default=400, help="flag a group above this many changed lines")
    ap.add_argument("--max-groups", type=int, default=7, help="flag a plan with more commits than this")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        if a.sample:
            text = SAMPLE_DIFF
        elif a.diff:
            text = sys.stdin.read() if a.diff == "-" else open(a.diff, encoding="utf-8", errors="replace").read()
        else:
            text = working_tree_diff()
    except (OSError, RuntimeError) as exc:
        print(f"BAD_INPUT: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    files = parse_diff(text)
    if not files:
        print("BAD_INPUT: no changes to plan", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    groups, flags, held = plan(files, a.depth, a.max_lines, a.max_groups)
    verdict = "BLOCKED" if held else ("SPLIT" if len(groups) > 1 else "SINGLE")
    result = {"verdict": verdict, "files": len(files), "commits": len(groups), "groups": groups,
              "held_back": held, "flags": flags,
              "verify": "git rebase -x '<your test command>' <upstream>  # runs the tests at every commit"}
    if a.output == "json":
        print(json.dumps(result, indent=2))
        return EXIT[verdict]
    print(f"{verdict}: {len(files)} files -> {len(groups)} commit(s)" + (f"; {len(held)} file(s) held back" if held else ""))
    for g in groups:
        print(f"\n[{g['n']}] {g['subject_stub']}   ({g['lines']} lines)")
        for f in g["files"]:
            print(f"     {f['path']}" + ("   (test for this change)" if f["with_source"] else ""))
        for s in g["stage"]:
            print(f"     $ {s}")
    if flags:
        print("\nFlags")
        for fl in flags:
            where = fl.get("file") or (f"group {fl['group']}" if fl.get("group") else "plan")
            print(f"  {fl['severity']:7} {fl['code']:18} {where}: {fl['detail']}")
    print("\nPick feat, fix or refactor from what each change does; the planner cannot. "
          "Before pushing, run the tests at every commit:\n  " + result["verify"])
    return EXIT[verdict]


if __name__ == "__main__":
    sys.exit(main())
