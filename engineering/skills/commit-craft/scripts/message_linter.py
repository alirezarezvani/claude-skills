#!/usr/bin/env python3
"""Lint commit messages, one at a time (commit-msg hook) or as a series before push.

A good series reads as a story a reviewer and a future `git blame` can follow:
each subject says what the commit does in the imperative, and each non-trivial
commit says WHY in its body, because the diff already shows what.

Per message
  EMPTY                no subject                                             BLOCKER
  NO_BLANK_LINE        line 2 is not blank, so tools merge it into the subject BLOCKER
  SUBJECT_TOO_LONG     subject over 72 chars (over 50 warns, plain style only) BLOCKER
  VAGUE_SUBJECT        "fix", "update", "wip", "address review comments"...    BLOCKER
  BODY_MISSING         a change of --body-lines lines or --body-files files
                       or more with no body explaining why                    BLOCKER
  CONVENTIONAL_FORMAT  type(scope)!: description, when the repo uses it       BLOCKER
  NOT_IMPERATIVE       "Added", "Fixes", "Updating" instead of "Add", "Fix"   WARN
  TRAILING_PERIOD      subject ends with a period                             WARN
  WHY_MISSING          body names no reason (because, so that, previously...)  WARN
  BODY_LISTS_FILES     body is mostly file names: the diff already says that   WARN
  BREAKING_UNMARKED    body says "breaking" but no ! or BREAKING CHANGE: footer WARN
  BODY_LINE_LONG       body line over 72 chars (URLs, code and trailers exempt) WARN

Series (--range)
  FIXUP_PENDING        fixup!/squash!/amend! or WIP left in: autosquash first  BLOCKER
  DUPLICATE_SUBJECT    two commits with the same subject                      WARN
  REVERT_PAIR          a commit and its revert in the same push: drop both    WARN
  OVERSIZED_COMMIT     one commit over --max-lines changed lines              WARN

--convention auto (default) enforces Conventional Commits only when most recent
subjects on HEAD already follow it: match the repo, do not impose a style.
WHY_MISSING is a keyword heuristic and only warns. Deterministic, stdlib only.
"""
import argparse
import json
import re
import subprocess
import sys

EXIT = {"CLEAN": 0, "FINDINGS": 2, "BAD_INPUT": 3, "BLOCKED": 4}
BLOCKER, WARN = "BLOCKER", "WARN"
CC = re.compile(r"^(?P<type>[a-z]+)(?:\((?P<scope>[^()\s][^()]*)\))?(?P<bang>!)?: (?P<desc>\S.*)$")
CC_TYPES = {"feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"}
VAGUE = {"fix", "fixes", "fixed", "bugfix", "fix bug", "fix bugs", "fix stuff", "fix tests", "fix test", "small fix",
         "minor fix", "update", "updates", "updated", "wip", "changes", "change", "misc", "stuff", "cleanup",
         "clean up", "tweaks", "tweak", "minor", "minor changes", "more", "again", "final", "final fix", "test",
         "testing", "asdf", "temp", "tmp", "refactor", "refactoring", "improvements", "address review comments",
         "address comments", "address feedback", "review comments", "pr feedback", "code review", "lint", "oops",
         "typo", "save", "commit", "done", "work", "progress"}
NON_IMPERATIVE = {
    "added", "adds", "adding", "fixed", "fixes", "fixing", "updated", "updates", "updating", "changed", "changes",
    "changing", "removed", "removes", "removing", "refactored", "refactors", "refactoring", "improved", "improves",
    "improving", "implemented", "implements", "implementing", "created", "creates", "creating", "deleted",
    "deletes", "deleting", "moved", "moves", "moving", "renamed", "renames", "renaming", "bumped", "bumps",
    "bumping", "upgraded", "upgrades", "upgrading", "merged", "merges", "merging", "cleaned", "cleans",
    "cleaning", "introduced", "introduces", "introducing", "replaced", "replaces", "replacing", "converted",
    "converts", "converting", "enabled", "enables", "enabling", "disabled", "disables", "disabling",
    "made", "makes", "making", "used", "uses", "using", "allowed", "allows", "allowing", "handled", "handles",
    "handling", "prevented", "prevents", "preventing", "reverted", "reverts", "reverting", "simplified",
    "simplifies", "simplifying", "extracted", "extracts", "extracting", "documented", "documents",
    "documenting", "tested", "tests", "ensured", "ensures", "ensuring", "supported", "supports", "supporting"}
WHY = re.compile(r"(?i)\b(because|since|so|in order to|why|needs?|needed|would|could|fails?|failed|broke|broken|bug|"
                 r"can now|lets?|#\d+|issue|request(?:ed)?|to (?:avoid|prevent|allow|keep|stop|make|fix|"
                 r"support|ensure|match|reduce|unblock)|otherwise|previously|before this|caused|causes|was (?:failing|"
                 r"broken|wrong)|which meant|led to|leads to|fixes #|closes #|resolves #|refs? #|instead of|"
                 r"no longer|now (?:fails|returns|rejects|accepts)|without this|the problem|the issue|motivation|"
                 r"required by|needed (?:for|by)|regression|incident|customer|user(?:s)? (?:saw|hit|reported))")
TRAILER = re.compile(r"^[A-Za-z][\w-]*: \S|^[A-Za-z][\w-]* #\d+")
PATHLIKE = re.compile(r"^\s*[-*]?\s*`?[\w./-]+\.(\w{1,5})`?\s*:?\s*$|^\s*[-*]\s*(?:update|change|modify|edit)d?\s+`?[\w./-]+`?\s*$", re.I)
SCISSORS = "# ------------------------ >8 ------------------------"
EXEMPT_BODY = re.compile(r"^(Merge |Revert \"|revert|bump |style|chore\((?:deps|release)\)|build\(deps\)|ci|docs|test)", re.I)

SAMPLE_SERIES = [
    {"sha": "a1", "lines": 3, "files": 1, "message": "build(deps): add zod for invoice schema validation"},
    {"sha": "b2", "lines": 160, "files": 4, "message": "feat(invoices): validate invoices against a schema\n\n"
     "Invoices with a two-letter currency code reached the ledger and failed\nat month-end close, because validate() only checked the total. The\n"
     "schema rejects them at the API boundary instead.\n\nRefs #412"},
    {"sha": "c3", "lines": 90, "files": 3, "message": "Updated session handling"},
    {"sha": "d4", "lines": 12, "files": 2, "message": "fix"},
    {"sha": "e5", "lines": 4, "files": 1, "message": "fixup! feat(invoices): validate invoices against a schema"},
    {"sha": "f6", "lines": 55, "files": 5, "message": "refactor(api): move route helpers\n\n- src/api/routes.ts\n- src/api/helpers.ts\n- src/api/index.ts"},
]


def clean(message):
    if SCISSORS in message:
        message = message.split(SCISSORS)[0]
    lines = [l.rstrip() for l in message.splitlines() if not l.startswith("#")]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def lint_message(message, lines_changed=None, files_changed=None, conventional=False, series=False,
                 body_lines=40, body_files=4, types=CC_TYPES):
    out = []
    add = lambda code, sev, detail: out.append({"code": code, "severity": sev, "detail": detail})
    lines = clean(message)
    if not lines:
        add("EMPTY", BLOCKER, "no subject line")
        return out
    subject = lines[0].strip()
    body = [l for l in lines[2:]] if len(lines) > 2 else []
    if len(lines) > 1 and lines[1].strip():
        add("NO_BLANK_LINE", BLOCKER, "put a blank line between the subject and the body")
        body = lines[1:]
    m = CC.match(subject)
    desc = m.group("desc") if m else subject
    if re.match(r"(?i)^(fixup|squash|amend)! |^wip\b|^\[wip\]", subject):
        add("FIXUP_PENDING", BLOCKER if series else WARN,
            "autosquash before pushing: git rebase -i --autosquash <upstream>" if series else "fine locally; squash it before pushing")
        return out
    if len(subject) > 72:
        add("SUBJECT_TOO_LONG", BLOCKER, f"{len(subject)} chars; keep it under 72 (50 is the target)")
    elif len(subject) > 50 and not m:
        add("SUBJECT_TOO_LONG", WARN, f"{len(subject)} chars; 50 is the target, 72 the limit")
    if desc.lower().rstrip(".!") in VAGUE or subject.lower().rstrip(".!") in VAGUE:
        add("VAGUE_SUBJECT", BLOCKER, f"'{subject}' says nothing a reviewer or bisect can use; name what changes")
    if conventional:
        if not m:
            add("CONVENTIONAL_FORMAT", BLOCKER, "expected 'type(scope): description', e.g. 'fix(auth): refresh expired sessions'")
        elif m.group("type") not in types:
            add("CONVENTIONAL_FORMAT", BLOCKER, f"type '{m.group('type')}' is not one of {', '.join(sorted(types))}")
    first = re.split(r"\s+", desc.strip())[0].lower().strip(":,") if desc.strip() else ""
    if first in NON_IMPERATIVE:
        add("NOT_IMPERATIVE", WARN, f"'{first}': write it as a command ('Fix', 'Add'): it completes 'If applied, this commit will ...'")
    if subject.endswith(".") and not subject.endswith("..."):
        add("TRAILING_PERIOD", WARN, "drop the period at the end of the subject")
    text_body = [l for l in body if l.strip() and not TRAILER.match(l.strip())]
    big = (lines_changed or 0) >= body_lines or (files_changed or 0) >= body_files
    if not text_body:
        if big and not EXEMPT_BODY.match(subject):
            add("BODY_MISSING", BLOCKER, f"{lines_changed} lines in {files_changed} files with no body: say why the change is needed")
    else:
        if all(PATHLIKE.match(l) for l in text_body):
            add("BODY_LISTS_FILES", WARN, "the body only lists files; the diff already shows them. Say why instead")
        elif not WHY.search(" ".join(body)):
            add("WHY_MISSING", WARN, "the body describes what, not why (heuristic): what broke, who needs it, what it enables")
        if re.search(r"(?i)\bbreaking\b", " ".join(body)) and not (m and m.group("bang")) and "BREAKING CHANGE:" not in message \
                and "BREAKING-CHANGE:" not in message:
            add("BREAKING_UNMARKED", WARN, "mark it with '!' after the type or a 'BREAKING CHANGE:' footer")
        for l in body:
            if len(l) > 72 and not re.search(r"https?://", l) and not l.startswith(("    ", "\t")) and not TRAILER.match(l):
                add("BODY_LINE_LONG", WARN, f"{len(l)}-char body line; wrap at 72")
                break
    return out


def lint_series(commits, conventional, max_lines, **kw):
    results, series_flags = [], []
    seen = {}
    for c in commits:
        findings = lint_message(c["message"], c.get("lines"), c.get("files"), conventional, True, **kw)
        if (c.get("lines") or 0) > max_lines:
            findings.append({"code": "OVERSIZED_COMMIT", "severity": WARN,
                             "detail": f"{c['lines']} changed lines: hard to review and to bisect; can it split?"})
        subj = (clean(c["message"]) or [""])[0].strip()
        if subj and subj in seen:
            findings.append({"code": "DUPLICATE_SUBJECT", "severity": WARN, "detail": f"same subject as {seen[subj]}"})
        seen.setdefault(subj, c["sha"][:8])
        results.append({"sha": c["sha"][:8], "subject": subj, "findings": findings})
    shas = {c["sha"] for c in commits}
    for c in commits:
        m = re.search(r"This reverts commit ([0-9a-f]{7,40})", c["message"])
        if m and any(s.startswith(m.group(1)) or m.group(1).startswith(s) for s in shas):
            series_flags.append({"code": "REVERT_PAIR", "severity": WARN,
                                 "detail": f"{c['sha'][:8]} reverts {m.group(1)[:8]} in the same push: drop both"})
    return results, series_flags


def git(args):
    proc = subprocess.run(["git", *args], capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def commits_in(rng):
    raw = git(["log", "--reverse", "--no-merges", "--format=%x1e%H%x1f%B%x1f", "--numstat", rng])
    commits = []
    for chunk in raw.split("\x1e")[1:]:
        sha, msg, stats = (chunk.split("\x1f") + ["", ""])[:3]
        lines = files = 0
        for row in stats.strip().splitlines():
            parts = row.split("\t")
            if len(parts) == 3:
                files += 1
                lines += sum(int(x) for x in parts[:2] if x.isdigit())
        commits.append({"sha": sha.strip(), "message": msg, "lines": lines, "files": files})
    return commits


def staged_size():
    lines = files = 0
    for row in git(["diff", "--cached", "--numstat"]).splitlines():
        parts = row.split("\t")
        if len(parts) == 3:
            files += 1
            lines += sum(int(x) for x in parts[:2] if x.isdigit())
    return lines, files


def repo_is_conventional():
    try:
        subjects = git(["log", "-50", "--no-merges", "--format=%s"]).splitlines()
    except RuntimeError:
        return False
    return len(subjects) >= 5 and sum(bool(CC.match(s)) for s in subjects) / len(subjects) >= 0.6


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 epilog="Exit codes: 0 clean · 2 warnings only · 3 bad input · 4 blocked",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--message-file", help="message file (commit-msg hook passes .git/COMMIT_EDITMSG)")
    src.add_argument("-m", "--message", help="message text")
    src.add_argument("--range", help="lint a series before pushing, e.g. origin/main..HEAD")
    src.add_argument("--sample", action="store_true", help="lint a built-in six-commit series")
    ap.add_argument("--staged", action="store_true", help="size the change from the index (for BODY_MISSING in a commit-msg hook)")
    ap.add_argument("--lines", type=int, help="changed lines of this commit, if known")
    ap.add_argument("--files", type=int, help="changed files of this commit, if known")
    ap.add_argument("--convention", choices=["auto", "conventional", "plain"], default="auto")
    ap.add_argument("--types", help="comma-separated Conventional Commit types to allow")
    ap.add_argument("--body-lines", type=int, default=40, help="a body is required from this many changed lines (default 40)")
    ap.add_argument("--body-files", type=int, default=4, help="... or from this many changed files (default 4)")
    ap.add_argument("--max-lines", type=int, default=800, help="series: flag a commit above this many changed lines")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)

    types = set(a.types.split(",")) if a.types else CC_TYPES
    kw = {"body_lines": a.body_lines, "body_files": a.body_files, "types": types}
    try:
        conventional = a.convention == "conventional" or (
            a.convention == "auto" and (True if a.sample else repo_is_conventional()))
        if a.sample or a.range:
            commits = SAMPLE_SERIES if a.sample else commits_in(a.range)
            if not commits:
                print(f"BAD_INPUT: no commits in {a.range}", file=sys.stderr)
                return EXIT["BAD_INPUT"]
            results, series_flags = lint_series(commits, conventional, a.max_lines, **kw)
        else:
            if a.message_file:
                with open(a.message_file, encoding="utf-8", errors="replace") as fh:
                    message = fh.read()
            elif a.message is not None:
                message = a.message
            else:
                ap.error("give --message-file, -m, --range or --sample")
            lines, files = (staged_size() if a.staged else (a.lines, a.files))
            results = [{"sha": None, "subject": (clean(message) or [""])[0],
                        "findings": lint_message(message, lines, files, conventional, False, **kw)}]
            series_flags = []
    except (OSError, RuntimeError) as exc:
        print(f"BAD_INPUT: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]

    every = [f for r in results for f in r["findings"]] + series_flags
    blockers = sum(f["severity"] == BLOCKER for f in every)
    verdict = "BLOCKED" if blockers else ("FINDINGS" if every else "CLEAN")
    result = {"verdict": verdict, "convention": "conventional" if conventional else "plain", "commits": len(results),
              "blockers": blockers, "warnings": len(every) - blockers, "results": results, "series": series_flags}
    if a.output == "json":
        print(json.dumps(result, indent=2))
        return EXIT[verdict]
    print(f"{verdict}: {len(results)} message(s), {blockers} blocking, {len(every) - blockers} warnings "
          f"(convention: {result['convention']})")
    for r in results:
        if not r["findings"]:
            continue
        print(f"\n  {r['sha'] + '  ' if r['sha'] else ''}{r['subject'][:72]}")
        for f in r["findings"]:
            print(f"    {f['severity']:7} {f['code']:19} {f['detail']}")
    for f in series_flags:
        print(f"\n  {f['severity']:7} {f['code']:19} {f['detail']}")
    return EXIT[verdict]


if __name__ == "__main__":
    sys.exit(main())
