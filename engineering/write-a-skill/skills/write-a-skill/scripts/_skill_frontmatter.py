#!/usr/bin/env python3
"""Shared frontmatter reading, trigger detection and limits for the write-a-skill scripts.

Not a script. Imported by skill_review_checklist_runner.py, skill_description_validator.py and
skill_structure_validator.py, which are the tools you actually run.

This module exists because three things were written more than once and disagreed:

  the trigger patterns   The runner and the description validator each carried an identical
                         copy of TRIGGER_PATTERNS, so widening one left the other narrow.

  the frontmatter reader Each had its OWN reader, and they mishandled YAML block scalar
                         indicators in two DIFFERENT ways. The runner compared the indicator
                         with `== ">"` and returned the indicator itself as the description, so
                         a `>-` description could never satisfy the trigger check. The validator
                         tested `!= ">"` and left `>-` or `|` prepended to the value, corrupting
                         its length check instead. One defect, two shapes, because the reading
                         was implemented twice.

  the limits             100 SKILL.md lines appeared in two scripts and 1024 description
                         characters in one, with nothing keeping them in step.

Stdlib only, so the scripts stay dependency-free.
"""

import os
import re
from typing import Dict, List

# Matt Pocock's limits, in one place so the scripts cannot disagree about them.
MAX_SKILL_MD_LINES = 100
MAX_DESCRIPTION_CHARS = 1024

# A YAML block scalar indicator introduces the value on the following lines; it is never part of
# the value. It may carry a chomping indicator ("-", "+") and/or an explicit indentation digit,
# so ">", ">-", ">+", "|", "|-", "|2" and ">-2" are all valid and all mean "the value follows".
BLOCK_SCALAR_INDICATOR = re.compile(r"[>|][0-9]*[-+]?|[>|][-+]?[0-9]*")

# A trigger phrase is an invocation verb followed by a temporal or conditional cue. Matching the
# pair, rather than enumerating two-word strings, is what lets "use when", "use whenever", "use
# this skill whenever", "should be used when", "invoke at the start of" and "load this before"
# all read as what they plainly are. Both halves must still be present, so prose such as "runs on
# macOS" or "teaches you to use design tokens" is still not a trigger.
_TRIGGER_VERB = r"(?:use|used|using|invoke|invoked|apply|applied|run|load|fire|trigger|reach\s+for)"
_TRIGGER_FILLER = r"(?:\s+(?:this|it|its|the|a|an|skill))*"
_TRIGGER_CUE = (
    r"(?:when(?:ever)?|before|after|during|while"
    r"|at\s+the\s+(?:start|point|moment)\s+of"
    r"|on\s+(?:every|any|each))"
)

TRIGGER_PATTERNS: List[re.Pattern] = [
    re.compile(rf"\b{_TRIGGER_VERB}\b{_TRIGGER_FILLER}\s+{_TRIGGER_CUE}\b", re.IGNORECASE),
    # "Use for X" carries no temporal cue but is long-standing and unambiguous in a description.
    re.compile(r"\buse\s+for\b", re.IGNORECASE),
]


def has_trigger(text: str) -> bool:
    """True when the text carries an explicit trigger phrase."""
    return any(p.search(text or "") for p in TRIGGER_PATTERNS)


def find_skill_md(folder: str) -> str:
    """Path to SKILL.md at the folder root, or an empty string."""
    candidate = os.path.join(folder, "SKILL.md")
    return candidate if os.path.isfile(candidate) else ""


def extract_frontmatter(text: str) -> Dict[str, str]:
    """Parse YAML frontmatter into a flat dict.

    A minimal parser, sufficient for SKILL.md frontmatter: `key: value` pairs, no nesting, with
    block scalars and plain multi-line values folded into a single space-separated string.
    """
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()

    out: Dict[str, str] = {}
    current_key = None
    buffer: List[str] = []
    for line in block.splitlines():
        if ":" in line and not line.startswith((" ", "\t")):
            if current_key:
                out[current_key] = " ".join(buffer).strip()
                buffer = []
            key, _, val = line.partition(":")
            current_key = key.strip()
            val = val.strip()
            # Keep the value, unless it is only a block scalar indicator announcing one.
            if val and not BLOCK_SCALAR_INDICATOR.fullmatch(val):
                buffer.append(val)
        elif current_key and line.strip():
            buffer.append(line.strip())
    if current_key:
        out[current_key] = " ".join(buffer).strip()
    return out


def extract_description(text: str) -> str:
    """The `description` value from a SKILL.md's frontmatter, or an empty string."""
    return extract_frontmatter(text).get("description", "")
