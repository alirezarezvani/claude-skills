"""SkillOpt-Sleep — skill/memory document manipulation.

Applies bounded EditRecords to a skill (SKILL.md body) or memory (CLAUDE.md)
document, and provides Dream-style consolidation helpers (dedup near-identical
lines, drop contradictions). All edits live inside a protected, clearly-marked
region so the sleep cycle never clobbers the user's hand-written content.
"""
from __future__ import annotations

import re
from typing import List, Tuple

from skillopt_sleep.types import EditRecord

LEARNED_START = "<!-- SKILLOPT-SLEEP:LEARNED START -->"
LEARNED_END = "<!-- SKILLOPT-SLEEP:LEARNED END -->"
_BANNER = (
    "_This block is maintained by SkillOpt-Sleep. Edits here are proposed "
    "offline, validated against your past tasks, and adopted only after you "
    "approve them. Hand-edits outside this block are never touched._"
)


def extract_learned(doc: str) -> str:
    s = doc.find(LEARNED_START)
    e = doc.find(LEARNED_END)
    if s == -1 or e == -1:
        return ""
    return doc[s + len(LEARNED_START):e].strip()


def _strip_learned(doc: str) -> str:
    while True:
        s = doc.find(LEARNED_START)
        if s == -1:
            break
        e = doc.find(LEARNED_END, s)
        if e == -1:
            doc = doc[:s]
            break
        doc = doc[:s] + doc[e + len(LEARNED_END):]
    while "\n\n\n" in doc:
        doc = doc.replace("\n\n\n", "\n\n")
    return doc.rstrip()


def set_learned(doc: str, learned_lines: List[str]) -> str:
    """Replace the protected learned region with the given bullet lines."""
    base = _strip_learned(doc)
    body = "\n".join(f"- {ln.strip().lstrip('- ').strip()}" for ln in learned_lines if ln.strip())
    block = (
        f"\n\n{LEARNED_START}\n"
        f"## Learned preferences & procedures\n\n{_BANNER}\n\n{body}\n"
        f"{LEARNED_END}\n"
    )
    return (base + block).lstrip("\n")


def current_learned_lines(doc: str) -> List[str]:
    inner = extract_learned(doc)
    lines: List[str] = []
    for ln in inner.splitlines():
        ln = ln.strip()
        if ln.startswith("- "):
            lines.append(ln[2:].strip())
    return lines


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def apply_edits(doc: str, edits: List[EditRecord]) -> Tuple[str, List[EditRecord]]:
    """Apply add/delete/replace edits to the protected learned region.

    Returns (new_doc, applied_edits). Dedups: an `add` whose content already
    exists (normalized) is skipped. `delete`/`replace` match on normalized
    anchor substring.
    """
    lines = current_learned_lines(doc)
    norm_set = {_norm(line) for line in lines}
    applied: List[EditRecord] = []

    for e in edits:
        op = (e.op or "add").lower()
        if op == "add":
            if _norm(e.content) in norm_set or not e.content.strip():
                continue
            lines.append(e.content.strip())
            norm_set.add(_norm(e.content))
            applied.append(e)
        elif op == "delete":
            anchor = _norm(e.anchor or e.content)
            keep = [line for line in lines if anchor not in _norm(line)]
            if len(keep) != len(lines):
                lines = keep
                norm_set = {_norm(line) for line in lines}
                applied.append(e)
        elif op == "replace":
            anchor = _norm(e.anchor)
            new_lines = []
            changed = False
            for line in lines:
                if anchor and anchor in _norm(line):
                    new_lines.append(e.content.strip())
                    changed = True
                else:
                    new_lines.append(line)
            if changed:
                lines = new_lines
                norm_set = {_norm(line) for line in lines}
                applied.append(e)

    return set_learned(doc, lines), applied


def ensure_skill_scaffold(doc: str, *, name: str, description: str) -> str:
    """Ensure a SKILL.md has YAML frontmatter so local agents load it."""
    if doc.lstrip().startswith("---"):
        return doc
    fm = (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "---\n\n"
        f"# {name}\n\n"
        "Preferences and procedures learned from your past local agent sessions.\n"
    )
    return fm + doc
