"""SkillOpt-Sleep — Stage 5/6: staging and adoption.

Implements the Dreams safety contract: the cycle never mutates the user's
live CLAUDE.md / SKILL.md. It writes proposals + a human-readable report into
a staging directory; a separate, explicit `adopt` step copies them over the
live files after taking a backup.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import time
from typing import Any, List, Optional

from skillopt_sleep.types import SleepReport

# Secret patterns scrubbed from any free-text we persist to the staging dir
# (diagnostics, reports). Kept here so every on-disk artifact shares one
# redaction pass; harvest_codex reuses these for session text too.
_SECRET_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    # "sk-" is not OpenAI-specific: Anthropic (sk-ant-...) and other vendors
    # share the prefix, so the placeholder names the shape, not one vendor.
    (re.compile(r"sk-[A-Za-z0-9_-]{10,}"), "[REDACTED_API_KEY]"),
    # Distinctive vendor token prefixes (low false-positive: these prefixes do
    # not occur in normal diagnostic prose).
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED_AWS_KEY]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "[REDACTED_GITHUB_TOKEN]"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "[REDACTED_SLACK_TOKEN]"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"), "[REDACTED_GOOGLE_KEY]"),
    # Bare JWT (three base64url segments) — e.g. a leaked bearer body without
    # the "Authorization:" prefix.
    (re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
     "[REDACTED_JWT]"),
    (re.compile(r"(?i)(Authorization:\s*Bearer\s+)[^\s\"']+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(Authorization:\s*Basic\s+)[^\s\"']+"), r"\1[REDACTED]"),
    (
        re.compile(r"(?i)\b(api[_-]?key|token|password|secret)\b(\s*[:=]\s*)[^\s\"']+"),
        r"\1\2[REDACTED]",
    ),
    (
        re.compile(r"(?i)\b(api[_-]?key|token|password|secret)\b(\s+)[^\s\"']+"),
        r"\1\2[REDACTED]",
    ),
    (
        re.compile(
            r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
            re.DOTALL,
        ),
        "[REDACTED_PRIVATE_KEY]",
    ),
)


def redact_secrets(value: Any) -> Any:
    """Scrub secret-looking substrings (API keys, bearer tokens, private keys)
    from a string, or recursively from the string leaves of a list/dict.

    Used before writing backend stderr / optimizer replies / task responses to
    on-disk diagnostics: those are surfaced for debugging, but the underlying
    text (e.g. a codex 401 stderr dump) can carry credentials. Non-string
    scalars pass through unchanged.
    """
    if isinstance(value, str):
        out = value
        for pattern, replacement in _SECRET_PATTERNS:
            out = pattern.sub(replacement, out)
        return out
    if isinstance(value, list):
        return [redact_secrets(v) for v in value]
    if isinstance(value, dict):
        return {k: redact_secrets(v) for k, v in value.items()}
    return value


def _ts_dir() -> str:
    return time.strftime("%Y%m%d-%H%M%S", time.localtime())


def _secure_dir(path: str) -> None:
    """Restrict to owner-only. These directories hold real harvested session
    content (task intents, code excerpts, project context) in plaintext,
    which lands world-readable by default on a typical multi-user box unless
    we tighten it ourselves."""
    try:
        os.chmod(path, 0o700)
    except OSError:
        pass


def _secure_file(path: str) -> None:
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass


def staging_root(project: str) -> str:
    return os.path.join(project, ".skillopt-sleep", "staging")


def latest_staging(project: str) -> Optional[str]:
    root = staging_root(project)
    if not os.path.isdir(root):
        return None
    subs = sorted(
        (os.path.join(root, d) for d in os.listdir(root)),
        key=lambda p: os.path.getmtime(p),
        reverse=True,
    )
    return subs[0] if subs else None


def write_staging(
    project: str,
    *,
    report: SleepReport,
    proposed_skill: Optional[str],
    proposed_memory: Optional[str],
    live_skill_path: str,
    live_memory_path: str,
    report_md: str,
    redact: bool = True,
) -> str:
    """Write proposals + report into staging/<ts>/ and return that path.

    ``redact`` mirrors the config's ``redact_secrets`` flag (default True).
    Disabling it is honored — the user asked for it — but never silently:
    the caller is expected to have already logged a loud warning (see
    cycle.py) before passing False.
    """
    root = staging_root(project)
    out = os.path.join(root, _ts_dir())
    # mode= closes the create-then-chmod race window for this leaf dir on a
    # first run (intermediate parents and pre-existing dirs still need the
    # explicit chmod below -- mode= only governs mkdir()'s own leaf, and is
    # itself subject to umask).
    os.makedirs(out, mode=0o700, exist_ok=True)
    # secure both the per-run leaf dir and the shared .skillopt-sleep root
    # (root may already exist from a prior night; still worth tightening).
    _secure_dir(os.path.dirname(root))  # <project>/.skillopt-sleep
    _secure_dir(out)

    # reflect()'s prompt is built from real harvested session text, which can
    # carry anything a user pasted while debugging (an API key, a .env dump).
    # These are the files `adopt()` copies over the LIVE CLAUDE.md / SKILL.md
    # (with --auto-adopt, with no human in the loop) — scrub them the same as
    # every other on-disk artifact rather than only the diagnostics dump.
    #
    # report.md / report.json carry the same risk: EditRecord.content /
    # .rationale come from the optimizer's reflect() output over real failing
    # task responses, and report.md is the file the SKILL.md's own workflow
    # tells a human to read FIRST ("show the user the exact proposed edits").
    # Redact both — report_md as the already-rendered string, report.to_dict()
    # recursively (redact_secrets walks dict/list/str) before it hits JSON.
    if redact:
        proposed_skill = redact_secrets(proposed_skill)
        proposed_memory = redact_secrets(proposed_memory)
        report_md = redact_secrets(report_md)
        report_dict = redact_secrets(report.to_dict())
    else:
        report_dict = report.to_dict()

    manifest = {
        "live_skill_path": live_skill_path,
        "live_memory_path": live_memory_path,
        "has_skill": proposed_skill is not None,
        "has_memory": proposed_memory is not None,
        "accepted": report.accepted,
    }
    if proposed_skill is not None:
        p = os.path.join(out, "proposed_SKILL.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(proposed_skill)
        _secure_file(p)
    if proposed_memory is not None:
        p = os.path.join(out, "proposed_CLAUDE.md")
        with open(p, "w", encoding="utf-8") as f:
            f.write(proposed_memory)
        _secure_file(p)
    p = os.path.join(out, "report.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(report_dict, f, ensure_ascii=False, indent=2)
    _secure_file(p)
    p = os.path.join(out, "report.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write(report_md)
    _secure_file(p)
    p = os.path.join(out, "manifest.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    _secure_file(p)
    return out


def _backup(path: str, backup_dir: str) -> None:
    if os.path.exists(path):
        os.makedirs(backup_dir, mode=0o700, exist_ok=True)
        _secure_dir(backup_dir)
        shutil.copy2(path, os.path.join(backup_dir, os.path.basename(path)))


def _adopt_one(staged_path: str, live: str, backup_dir: str) -> None:
    os.makedirs(os.path.dirname(live), exist_ok=True)
    _backup(live, backup_dir)
    # Defense-in-depth: write_staging() already redacted this content, but
    # re-scrub here too rather than trust that nothing touched the staged
    # file between `stage` and `adopt` (a human editing the proposal by hand
    # is exactly the case the staging step exists to allow).
    with open(staged_path, encoding="utf-8") as f:
        content = redact_secrets(f.read())
    with open(live, "w", encoding="utf-8") as f:
        f.write(content)


def adopt(staging_dir: str) -> List[str]:
    """Copy staged proposals over the live files, backing up first.

    Returns the list of live paths that were updated.
    """
    with open(os.path.join(staging_dir, "manifest.json")) as f:
        manifest = json.load(f)
    backup_dir = os.path.join(staging_dir, "backup")
    updated: List[str] = []

    if manifest.get("has_skill"):
        live = manifest["live_skill_path"]
        _adopt_one(os.path.join(staging_dir, "proposed_SKILL.md"), live, backup_dir)
        updated.append(live)
    if manifest.get("has_memory"):
        live = manifest["live_memory_path"]
        _adopt_one(os.path.join(staging_dir, "proposed_CLAUDE.md"), live, backup_dir)
        updated.append(live)
    return updated
