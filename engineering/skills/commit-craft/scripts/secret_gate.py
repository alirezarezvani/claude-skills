#!/usr/bin/env python3
"""Refuse to commit credentials: scan the lines a commit adds, before it exists.

Reads the staged diff (`git diff --cached`) by default, a commit range with
--range (for a pre-push hook), or a unified diff file. Only added lines are
scanned, so a secret already in history is not re-reported on every commit;
rotating that one is a separate job (see references/secret_response.md).

Findings
  SECRET            provider-shaped credential (AWS, GitHub, Slack, Stripe, Google,
                    Anthropic, OpenAI, npm, private key block, JWT, password in a URL)  BLOCKER
  GENERIC_SECRET    key/secret/token/password assigned a high-entropy literal (quoted,
                    or filling a config line)                                         BLOCKER
  SENSITIVE_FILE    .env, private keys, keystores, tfstate, credentials files            BLOCKER
  CONFLICT_MARKER   <<<<<<< or >>>>>>> left from a merge                                 BLOCKER
  DEBUG_LEFTOVER    debugger;, breakpoint(), pdb.set_trace(), binding.pry               WARN
  LARGE_FILE        staged blob over --max-kb (history keeps it forever)                 WARN
  ALLOW_NO_REASON   allowlist entry without a reason (ignored until it has one)          WARN

A finding is waived only by an allowlist entry WITH a reason, in
.commit-craft-allow at the repo root (or --allow FILE):

  <fingerprint>  <reason>          one finding, by the fingerprint this script prints
  path:<glob>    <reason>          every finding in matching files (test fixtures)

The fingerprint is a hash of the match, so the allowlist never holds the secret.
Matches are printed redacted. Deterministic, stdlib only, no network.
"""
import argparse
import fnmatch
import hashlib
import json
import math
import os
import re
import subprocess
import sys

EXIT = {"CLEAN": 0, "FINDINGS": 2, "BAD_INPUT": 3, "BLOCKED": 4}
BLOCKER, WARN = "BLOCKER", "WARN"

PATTERNS = [
    ("aws-access-key-id", re.compile(r"\b(?:AKIA|ASIA|AGPA|AIDA|AROA|ANPA)[0-9A-Z]{16}\b")),
    ("aws-secret-access-key", re.compile(r"(?i)aws.{0,20}?secret.{0,20}?[\"'=:\s]([A-Za-z0-9/+=]{40})\b")),
    ("github-token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b")),
    ("github-fine-grained-pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{60,}\b")),
    ("gitlab-pat", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}\b")),
    ("slack-webhook", re.compile(r"https://hooks\.slack\.com/services/T[A-Za-z0-9]+/B[A-Za-z0-9]+/[A-Za-z0-9]+")),
    ("stripe-live-key", re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("anthropic-api-key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("openai-api-key", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}")),
    ("npm-token", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    ("pypi-token", re.compile(r"\bpypi-[A-Za-z0-9_-]{50,}")),
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----")),
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("password-in-url", re.compile(r"\b[a-z][a-z0-9+.-]{1,20}://[^\s:/@\"']{1,64}:([^\s@/\"']{3,128})@[\w.-]+")),
]
SECRET_NAME = r"[\w.-]*(?:api[_-]?key|secret|token|passw(?:or)?d|pwd|access[_-]?key|client[_-]?secret|auth[_-]?key)[\w.-]*"
GENERIC = [
    # quoted literal anywhere: api_key = "...", "client_secret": "..."
    re.compile(r"(?i)\b(" + SECRET_NAME + r")[\"']?\s*(?::=|=>|[:=])\s*[\"']([^\"'\s]{16,})[\"']"),
    # unquoted value filling the rest of a config line: YAML, .env, ini, Dockerfile ENV
    re.compile(r"(?i)^\s*(?:export\s+|ENV\s+)?(" + SECRET_NAME + r")\s*[:=]\s*([A-Za-z0-9/+_=-]{16,})\s*$"),
]
PLACEHOLDER = re.compile(
    r"(?i)example|changeme|change[_-]?me|dummy|fake|sample|placeholder|your[_-]|xxxx|\*\*\*|redacted|"
    r"<[^>]*>|\$\{|\{\{|process\.env|os\.environ|getenv|secrets\.|vault:|^(.)\1+$|test[_-]?(?:key|token|secret)")
SENSITIVE_FILES = [
    (re.compile(r"(^|/)\.env(\.[\w-]+)?$"), "environment file"),
    (re.compile(r"\.(pem|key|p12|pfx|keystore|jks|kdbx|ppk)$", re.I), "key or keystore"),
    (re.compile(r"(^|/)id_(rsa|dsa|ecdsa|ed25519)$"), "SSH private key"),
    (re.compile(r"(^|/)(credentials|client_secrets?|service[-_]account[\w-]*)\.json$", re.I), "credentials file"),
    (re.compile(r"(^|/)\.(pypirc|netrc|git-credentials|htpasswd)$"), "credentials file"),
    (re.compile(r"\.tfstate(\.backup)?$"), "Terraform state (holds secrets in plain text)"),
]
SAFE_ENV_SUFFIX = re.compile(r"\.(example|sample|template|dist|defaults?)$", re.I)
CONFLICT = re.compile(r"^(<{7}|>{7})(\s|$)")
DEBUG = re.compile(r"^\s*(debugger;?\s*$|breakpoint\(\)|import i?pdb;\s*i?pdb\.set_trace\(\)|i?pdb\.set_trace\(\)|binding\.pry\b)")
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")

SAMPLE_DIFF = """diff --git a/src/billing/client.py b/src/billing/client.py
--- a/src/billing/client.py
+++ b/src/billing/client.py
@@ -1,3 +1,8 @@
 import os
+import pdb; pdb.set_trace()
+STRIPE_KEY = "sk_live_""" + "51HxQyT2eZvKYlo2C0aBcDeFgHiJ" + """"
+API_TOKEN = os.environ["API_TOKEN"]
+client_secret = "changeme-in-production-please"
+DB = "postgres://app:""" + "s3cr3tPassw0rd" + """@db.internal:5432/app"
 def charge():
     pass
diff --git a/.env b/.env
new file mode 100644
--- /dev/null
+++ b/.env
@@ -0,0 +1 @@
+DEBUG=1
diff --git a/tests/fixtures/keys/test_key.pem b/tests/fixtures/keys/test_key.pem
new file mode 100644
--- /dev/null
+++ b/tests/fixtures/keys/test_key.pem
@@ -0,0 +1 @@
+""" + "-----BEGIN RSA " + "PRIVATE KEY-----" + """
"""
SAMPLE_ALLOW = "path:tests/fixtures/keys/*  throwaway key generated for the TLS handshake tests, never used anywhere\n"


def fingerprint(text):
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()[:16]


def redact(text):
    text = text.strip()
    if len(text) <= 8:
        return "*" * len(text)
    return f"{text[:4]}…[{len(text)} chars redacted]"


def entropy(s):
    counts = {c: s.count(c) for c in set(s)}
    return -sum(n / len(s) * math.log2(n / len(s)) for n in counts.values())


def parse_diff(text):
    """Return {path: {"new": bool, "added": [(lineno, text)]}} from a unified diff."""
    files, cur, lineno = {}, None, 0
    for raw in text.splitlines():
        if raw.startswith("diff --git "):
            cur = None
        elif raw.startswith("+++ "):
            path = raw[4:].strip()
            if path == "/dev/null":
                cur = None
                continue
            path = path[2:] if path.startswith("b/") else path
            cur = files.setdefault(path, {"new": False, "added": []})
        elif raw.startswith("@@"):
            m = HUNK.match(raw)
            lineno = int(m.group(1)) if m else 0
        elif cur is not None and raw.startswith("+"):
            cur["added"].append((lineno, raw[1:]))
            lineno += 1
        elif cur is not None and not raw.startswith("-") and not raw.startswith("\\"):
            lineno += 1
    return files


def load_allow(path):
    entries, problems = [], []
    if not path or not os.path.isfile(path):
        return entries, problems
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, reason = line.partition(" ")
            reason = reason.strip()
            if len(reason) < 10:
                problems.append({"code": "ALLOW_NO_REASON", "severity": WARN, "file": path, "line": n,
                                 "detail": f"entry '{key}' has no reason (10+ chars); it is ignored"})
                continue
            entries.append((key, reason))
    return entries, problems


def waived(finding, allow):
    for key, reason in allow:
        if key.startswith("path:"):
            if fnmatch.fnmatch(finding["file"], key[5:]):
                return reason
        elif key == finding.get("fingerprint"):
            return reason
    return None


def scan(files, sizes=None, max_kb=1024):
    findings = []
    for path, info in sorted(files.items()):
        base = os.path.basename(path)
        for rx, what in SENSITIVE_FILES:
            if rx.search(path) and not SAFE_ENV_SUFFIX.search(base):
                findings.append({"code": "SENSITIVE_FILE", "severity": BLOCKER, "file": path, "line": 0,
                                 "detail": f"{what} staged; keep it out of git (.gitignore) and load it at runtime",
                                 "fingerprint": fingerprint("file:" + path)})
                break
        for lineno, line in info["added"]:
            seen = set()
            for name, rx in PATTERNS:
                for m in rx.finditer(line):
                    value = m.group(1) if m.groups() else m.group(0)
                    if name not in ("private-key-block",) and PLACEHOLDER.search(value):
                        continue
                    if (m.start(), name) in seen:
                        continue
                    seen.add((m.start(), name))
                    findings.append({"code": "SECRET", "severity": BLOCKER, "file": path, "line": lineno,
                                     "kind": name, "match": redact(m.group(0)), "fingerprint": fingerprint(m.group(0))})
            if not any(f["file"] == path and f["line"] == lineno and f["code"] == "SECRET" for f in findings):
                for m in (m for rx in GENERIC for m in rx.finditer(line)):
                    value = m.group(2)
                    if PLACEHOLDER.search(value) or PLACEHOLDER.search(line) and "environ" in line:
                        continue
                    if entropy(value) < 3.5 or not (re.search(r"\d", value) and re.search(r"[A-Za-z]", value)):
                        continue
                    findings.append({"code": "GENERIC_SECRET", "severity": BLOCKER, "file": path, "line": lineno,
                                     "kind": m.group(1), "match": redact(value), "fingerprint": fingerprint(value)})
            if CONFLICT.match(line):
                findings.append({"code": "CONFLICT_MARKER", "severity": BLOCKER, "file": path, "line": lineno,
                                 "detail": "merge conflict marker", "fingerprint": fingerprint(f"{path}:{lineno}:conflict")})
            if DEBUG.match(line):
                findings.append({"code": "DEBUG_LEFTOVER", "severity": WARN, "file": path, "line": lineno,
                                 "detail": line.strip()[:60], "fingerprint": fingerprint(f"{path}:{line.strip()}")})
        if sizes and sizes.get(path, 0) > max_kb * 1024:
            findings.append({"code": "LARGE_FILE", "severity": WARN, "file": path, "line": 0,
                             "detail": f"{sizes[path] // 1024} KB; history keeps every version (Git LFS or an artifact store?)",
                             "fingerprint": fingerprint("size:" + path)})
    return findings


def git(args, cwd=None):
    proc = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"git {' '.join(args)} failed")
    return proc.stdout


def staged_sizes(paths):
    sizes = {}
    for p in paths:
        try:
            sizes[p] = int(git(["cat-file", "-s", f":{p}"]).strip())
        except (RuntimeError, ValueError):
            pass
    return sizes


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                 epilog="Exit codes: 0 clean · 2 warnings only · 3 bad input · 4 blocked",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--diff", help="unified diff file to scan ('-' for stdin) instead of the staged changes")
    src.add_argument("--range", help="commit range to scan, e.g. origin/main..HEAD (pre-push)")
    src.add_argument("--sample", action="store_true", help="scan a built-in tangled diff")
    ap.add_argument("--allow", help="allowlist file (default: .commit-craft-allow at the repo root)")
    ap.add_argument("--max-kb", type=int, default=1024, help="warn on staged files larger than this (default 1024)")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)

    sizes, allow_path, source = None, a.allow, "staged"
    try:
        if a.sample:
            text, source = SAMPLE_DIFF, "sample"
        elif a.diff:
            text = sys.stdin.read() if a.diff == "-" else open(a.diff, encoding="utf-8", errors="replace").read()
            source = a.diff
        else:
            root = git(["rev-parse", "--show-toplevel"]).strip()
            allow_path = allow_path or os.path.join(root, ".commit-craft-allow")
            if a.range:
                text, source = git(["diff", "--no-color", "--no-ext-diff", "-U0", a.range]), a.range
            else:
                text = git(["diff", "--cached", "--no-color", "--no-ext-diff", "-U0"])
                names = git(["diff", "--cached", "--name-only", "--diff-filter=AM"]).split()
                sizes = staged_sizes(names)
    except (OSError, RuntimeError) as exc:
        print(f"BAD_INPUT: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]

    files = parse_diff(text)
    findings = scan(files, sizes, a.max_kb)
    if a.sample:
        allow, problems = [(k, r.strip()) for k, _, r in (l.partition("  ") for l in SAMPLE_ALLOW.splitlines())], []
    else:
        allow, problems = load_allow(allow_path)
    for f in findings:
        reason = waived(f, allow)
        if reason:
            f["waived"] = reason
    active = [f for f in findings if not f.get("waived")]
    blockers = [f for f in active if f["severity"] == BLOCKER]
    verdict = "BLOCKED" if blockers else ("FINDINGS" if active or problems else "CLEAN")
    result = {"verdict": verdict, "source": source, "files_scanned": len(files),
              "added_lines": sum(len(v["added"]) for v in files.values()),
              "blockers": len(blockers), "warnings": len(active) - len(blockers) + len(problems),
              "waived": [f for f in findings if f.get("waived")], "findings": active + problems}

    if a.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"{verdict}: {result['files_scanned']} files, {result['added_lines']} added lines scanned ({source}); "
              f"{result['blockers']} blocking, {result['warnings']} warnings, {len(result['waived'])} waived")
        for f in active + problems:
            where = f"{f['file']}:{f['line']}" if f.get("line") else f["file"]
            what = f.get("detail") or f"{f.get('kind')}: {f.get('match')}"
            fp = f"  [fp {f['fingerprint']}]" if f.get("fingerprint") else ""
            print(f"  {f['severity']:7} {f['code']:16} {where}  {what}{fp}")
        for f in result["waived"]:
            print(f"  waived  {f['code']:16} {f['file']}  ({f['waived']})")
        if blockers:
            print("\nNothing is committed. Remove the value, load it from the environment or a secret store, "
                  "and unstage the file. If it was ever pushed, rotate it first: deleting it does not un-leak it. "
                  "A real false positive gets an allowlist line with its fingerprint and a reason.")
        if not files and source == "staged":
            print("  (nothing staged)")
    return EXIT[verdict]


if __name__ == "__main__":
    sys.exit(main())
