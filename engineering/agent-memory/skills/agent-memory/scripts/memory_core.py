#!/usr/bin/env python3
"""Shared core for the agent-memory tiered store (L0-L3).

Implements the contracts DESIGN.md pins:

  - normalize() / atom_id()      -- 4.1, must reproduce the doc's worked ids
  - redact()                     -- 6 rule 1, runs before ANY write
  - canonical_backpointer()      -- 3.1.1, platform-independent, de-identified
  - AtomStore                    -- 5.4 concurrency: lock-free reads, atomic
                                    os.replace writes, 5s wait / 60s stale break
  - contradiction detection      -- 4.2.1, two narrow deterministic rules

NOT a plugin-facing tool: it has no CLI of its own. Every other script and hook
in this skill imports it, which is deliberate -- redaction patterns, the id
algorithm and the lock protocol duplicated across seven files is precisely the
drift class DESIGN.md exists to prevent.

Deviation from DESIGN.md 10's planned tree: that tree lists four scripts and no
shared module. Duplicating this logic instead would have been worse. See
README.md "Deviations from the spec".

stdlib only. No LLM calls (root CLAUDE.md anti-pattern).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from datetime import datetime, timedelta, timezone

# --------------------------------------------------------------------------
# 4.1 -- identity. Pinned exactly; the ids in DESIGN.md and memory_schema.json
# are worked examples of this contract and must reproduce.
# --------------------------------------------------------------------------

CONFIDENCE_ORDER = ["observed", "stated", "verified"]
GATE_SESSIONS = {"observed": 3, "stated": 2, "verified": 1}

# 4.3 / 5.1 caps
L1_MAX_ATOMS = 500
L2_MAX_ATOMS = 60
L3_MAX_ATOMS = 30
L1_TTL_DAYS = 90
L2_MIN_AGE_DAYS = 30


def normalize(claim):
    """The algorithm DESIGN.md 4.1 publishes. Order matters: collapse
    whitespace, then casefold, then strip trailing punctuation."""
    return re.sub(r"\s+", " ", claim.strip()).casefold().rstrip(".,;:!?")


def atom_id(claim, project=None):
    """sha256 (NOT builtin hash(), which is salted per process for str and
    would produce different ids every run, breaking merges outright)."""
    key = normalize(claim) + ("\0" + project if project else "")
    return "atm_" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:8]


# --------------------------------------------------------------------------
# 6 rule 1 -- redaction. productivity/handoff's 17-pattern linter is the
# stated floor; these are re-implemented rather than imported, because root
# CLAUDE.md forbids cross-skill dependencies (2.5 applies the same rule to
# skillopt_sleep). Coverage is the contract, not the import.
# --------------------------------------------------------------------------

_REDACTIONS = [
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("aws-secret", re.compile(
        r"(?i)aws.{0,20}(secret|access).{0,20}[=:]\s*['\"]?[A-Za-z0-9/+=]{40}['\"]?")),
    ("github-token", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b")),
    ("anthropic-key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b")),
    ("slack-token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("stripe-key", re.compile(r"\b(sk|pk|rk)_(live|test)_[A-Za-z0-9]{16,}\b")),
    ("private-key-block", re.compile(
        r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("jwt", re.compile(
        r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b")),
    ("bearer-token", re.compile(
        r"(?i)\bauthorization\s*:\s*bearer\s+[A-Za-z0-9_\-\.]{20,}")),
    ("env-secret-assign", re.compile(
        r"(?i)\b(?:api[_-]?key|secret|password|passwd|token|credential)\s*[=:]\s*"
        r"['\"]?[A-Za-z0-9/+=_\-]{12,}['\"]?")),
    ("db-connection-string", re.compile(
        r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp)://"
        r"[^\s:@/]+:[^\s:@/]+@[^\s/]+")),
    ("url-token-param", re.compile(
        r"https?://[^\s'\"<>]*(?:[?&](?:token|access_token|api_key|key)=)[^\s'\"<>&]+")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("phone", re.compile(
        r"(?<![\w.])(?:\+?\d{1,3}[ .-]?)?(?:\(\d{3}\)|\d{3})[ .-]\d{3}[ .-]\d{4}(?![\w.])")),
    ("credit-card", re.compile(r"\b(?:\d[ -]?){13,19}\b")),
]


def redact(text):
    """Return (redacted_text, hit_rule_names).

    Lexical, therefore a filter and never a guarantee -- which is exactly why
    4.1 makes `redacted: true` block promotion pending human review: the flag
    firing is positive evidence the source was sensitive, and finding one thing
    is not proof of finding everything.
    """
    hits = []
    out = text
    for name, pat in _REDACTIONS:
        if pat.search(out):
            hits.append(name)
            out = pat.sub("[REDACTED:%s]" % name, out)
    return out, hits


# --------------------------------------------------------------------------
# 3.1.1 -- back-pointers. Canonical, not observed: derived to a ~/-relative
# forward-slash form from whatever the platform handed us, so a Windows
# %USERPROFILE%\.claude\... path does not produce a schema-invalid atom.
# --------------------------------------------------------------------------

_L1_PAT = re.compile(r"^~/\.claude/projects/[^/]+/[A-Za-z0-9._-]+\.jsonl#L[0-9]+$")
_COMMITTED_PAT = re.compile(r"^[A-Za-z0-9._-]+\.jsonl#L[0-9]+$")


def canonical_backpointer(transcript_path, line_no):
    """Absolute/native transcript path + line -> the L1 form the schema accepts."""
    p = str(transcript_path).replace("\\", "/")
    parts = [seg for seg in p.split("/") if seg]
    try:
        i = parts.index("projects")
        slug, fname = parts[i + 1], parts[i + 2]
    except (ValueError, IndexError):
        slug, fname = "unknown", parts[-1] if parts else "unknown.jsonl"
    return "~/.claude/projects/%s/%s#L%d" % (slug, fname, int(line_no))


def strip_backpointer(bp):
    """3.1.1 -- promotion into a committed tier drops the path prefix, which
    embeds the OS username. Strips the prefix and NOTHING else; the line
    number must survive unchanged."""
    return bp.rsplit("/", 1)[-1]


def resolve_backpointer(bp, home=None):
    """Reverse the strip for a local read. Returns (path, status) where status
    is one of ok / missing / ambiguous.

    The ambiguous row is the one worth having: without it a naive
    implementation takes the first glob match and attributes a claim to the
    wrong session -- a *wrong* citation, which 6 rule 6 treats as worse than a
    missing one.
    """
    import glob
    home = home or os.path.expanduser("~")
    fname = strip_backpointer(bp).split("#")[0]
    hits = glob.glob(os.path.join(home, ".claude", "projects", "*", fname))
    if len(hits) == 1:
        return hits[0], "ok"
    if not hits:
        return None, "missing"
    return None, "ambiguous"


# --------------------------------------------------------------------------
# time helpers
# --------------------------------------------------------------------------

def utcnow():
    return datetime.now(timezone.utc)


def iso(dt=None):
    return (dt or utcnow()).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(s):
    return datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)


def days_between(a, b):
    return abs((parse_iso(b) - parse_iso(a)).days)


# --------------------------------------------------------------------------
# 5.4 -- the store. Lock-free reads; writes take a lock, write a temp file,
# then os.replace (atomic on POSIX and Windows). 5s bounded wait, 60s stale
# break by mtime. On contention the write is dropped and logged: L1 is the
# recoverable tier by construction, so a lost observation costs one re-sighting.
# --------------------------------------------------------------------------

LOCK_WAIT_S = 5.0
LOCK_STALE_S = 60.0


class AtomStore:
    def __init__(self, root=None):
        self.root = os.path.abspath(root or os.path.join(os.getcwd(), ".memory"))
        self.path = os.path.join(self.root, "atoms.jsonl")
        self.lock = os.path.join(self.root, "atoms.lock")
        self.errors = os.path.join(self.root, "errors.log")
        self.staged = os.path.join(self.root, "staged")
        self.adopted = os.path.join(self.root, "adopted.log")

    # -- 5.3: a missing file is the normal initial state, not an error -----
    def read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as fh:
                return [json.loads(ln) for ln in fh if ln.strip()]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def _ensure_dirs(self):
        os.makedirs(self.root, mode=0o700, exist_ok=True)
        try:
            os.chmod(self.root, 0o700)  # 6 rule 3
        except OSError:
            pass

    def _acquire(self):
        deadline = time.monotonic() + LOCK_WAIT_S
        while True:
            try:
                fd = os.open(self.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return True
            except FileExistsError:
                try:
                    age = time.time() - os.path.getmtime(self.lock)
                    if age > LOCK_STALE_S:
                        # Accepted TOCTOU: two processes can both decide a lock
                        # is stale. Bounded by design -- worst case is a lost
                        # write on the recoverable tier, never a corrupt file,
                        # since the write itself is an atomic os.replace.
                        os.unlink(self.lock)
                        continue
                except OSError:
                    pass
                if time.monotonic() >= deadline:
                    return False
                time.sleep(0.05)

    def _release(self):
        try:
            os.unlink(self.lock)
        except OSError:
            pass

    def write(self, atoms):
        """Atomic replace under lock. Returns True on write, False if dropped."""
        self._ensure_dirs()
        if not self._acquire():
            self.log_error("lock contention: %d atoms dropped" % len(atoms))
            return False
        try:
            tmp = self.path + ".tmp.%d" % os.getpid()
            with open(tmp, "w", encoding="utf-8") as fh:
                for a in atoms:
                    fh.write(json.dumps(a, ensure_ascii=False, sort_keys=True) + "\n")
            try:
                os.chmod(tmp, 0o600)
            except OSError:
                pass
            os.replace(tmp, self.path)
            return True
        finally:
            self._release()

    def log_error(self, msg):
        self._ensure_dirs()
        try:
            lines = []
            if os.path.exists(self.errors):
                with open(self.errors, "r", encoding="utf-8") as fh:
                    lines = fh.readlines()
            lines.append("%s %s\n" % (iso(), msg))
            with open(self.errors, "w", encoding="utf-8") as fh:
                fh.writelines(lines[-200:])  # capped, per 6
            os.chmod(self.errors, 0o600)
        except OSError:
            pass


# --------------------------------------------------------------------------
# 4.1.3 -- confidence is monotonic. Never downgrades.
# --------------------------------------------------------------------------

def max_confidence(a, b):
    return a if CONFIDENCE_ORDER.index(a) >= CONFIDENCE_ORDER.index(b) else b


# --------------------------------------------------------------------------
# 4.2.1 -- contradiction detection. Two narrow deterministic rules over atoms
# sharing a project. Cannot reach L3 (scope=global has no project) -- see 9.6.
# Detection is a filter, never a guarantee.
# --------------------------------------------------------------------------

_NEG = {"not", "never", "no", "n't", "longer"}


def _tokens(claim):
    return normalize(claim).split()


def contradicts(a_claim, b_claim, a_kind=None, b_kind=None):
    ta, tb = _tokens(a_claim), _tokens(b_claim)
    # rule 1: explicit negation -- differ only by a negation token
    sa, sb = [t for t in ta if t not in _NEG], [t for t in tb if t not in _NEG]
    if sa == sb and ta != tb:
        return "explicit-negation"
    # rule 2: same-subject conflict -- same kind, >=3 shared leading tokens,
    # different trailing value
    if a_kind and a_kind == b_kind and len(ta) >= 4 and len(tb) >= 4:
        lead = 0
        for x, y in zip(ta, tb):
            if x != y:
                break
            lead += 1
        if lead >= 3 and ta[lead:] and tb[lead:] and ta[lead:] != tb[lead:]:
            return "same-subject-conflict"
    return None


def open_contradiction(atom, atoms):
    """4.2.1 -- the newer atom carries no flag, so this is a REVERSE JOIN:
    blocked if own `contested` is set OR own id appears in another atom's
    `contested_by`. Deliberately not a mirrored field -- that would be the same
    fact in two places with nothing able to say which copy is right. Cheap by
    construction: the store is capped at L1_MAX_ATOMS."""
    if atom.get("contested"):
        return True
    aid = atom["id"]
    return any(aid in other.get("contested_by", []) for other in atoms)


def mark_contradictions(atoms):
    """4.2.1 -- runs at merge time in SessionEnd. Groups by project, applies the
    two rules, and marks the OLDER atom `contested` + `contested_by`. The newer
    atom is not auto-blessed; both sit at L1 until a human resolves at adopt.

    Returns the list of (older_id, newer_id, rule) pairs it marked, so the
    caller can report them -- silent marking would make a claim stop promoting
    with no visible cause.
    """
    fired = []
    by_project = {}
    for a in atoms:
        if a["tier"] in ("L1", "L2") and a.get("project"):
            by_project.setdefault(a["project"], []).append(a)
    for group in by_project.values():
        group.sort(key=lambda g: g["first_seen"])
        for i, older in enumerate(group):
            for newer in group[i + 1:]:
                rule = contradicts(older["claim"], newer["claim"],
                                   older["kind"], newer["kind"])
                if not rule:
                    continue
                ids = older.setdefault("contested_by", [])
                if newer["id"] not in ids:
                    ids.append(newer["id"])
                older["contested"] = True
                fired.append((older["id"], newer["id"], rule))
    return fired


def distinct_days(atom):
    """4.1 -- first_seen and last_seen BOUND every observation, so different
    dates is equivalent to '>= 2 distinct calendar days', not a proxy for it."""
    return 2 if atom["first_seen"][:10] != atom["last_seen"][:10] else 1
