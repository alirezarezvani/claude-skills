#!/usr/bin/env python3
"""book_skill_validator.py — gate a generated book skill before anyone loads it.

Runs four independent check families over a generated skill folder and reports
every finding with a file, a line, and a rule id:

  frontmatter   name/description shape for the chosen host lens, tool-authority
                grants, unrecognized keys
  safety        prompt-injection phrasing, fake system prefixes, chat-template
                delimiters, exfiltration-shaped language, invisible Unicode, and
                frontmatter that widens the generated skill's own authority
  budget        SKILL.md and the supporting files against the token caps the
                converter commits to (Steps 7-9 of SKILL.md)
  index         Chapter Index and Topic Index integrity — every link resolves,
                every chapter file is indexed, no topic points at a missing
                chapter

The safety family is deliberately broad: a book about LLM security legitimately
contains the phrases it flags. Findings are review prompts, not verdicts. What
they are not is optional — a generated skill is untrusted text that an agent
will later load as instructions, so it gets read by a human before it gets read
by a model.

Severity: ERROR fails the run (exit 1). WARN is reported and does not fail
unless --strict is passed.

Exit codes:
    0  no errors (warnings may be present)
    1  at least one error (or any finding under --strict)
    2  the skill could not be inspected at all

Adapted from virgiliojr94/book-to-skill's validate_skill.py and
scan_generated_skill.py (MIT), merged into one gate and extended with the
budget and index families. See ../../../LICENSE.

Usage:
    python3 book_skill_validator.py path/to/generated-skill
    python3 book_skill_validator.py path/to/skill --lens copilot --strict
    python3 book_skill_validator.py path/to/skill --output json
    python3 book_skill_validator.py --sample
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from book_to_skill.config import (  # noqa: E402
    CHAPTER_TOKEN_CEILING,
    SKILL_FILE_BUDGETS,
)
from book_to_skill.sanitize import is_invisible_codepoint  # noqa: E402
from book_to_skill.utils import estimate_tokens  # noqa: E402

MAX_SKILL_FILES = 1_000
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 20 * 1024 * 1024

# Token caps the converter's own workflow commits to. Imported rather than
# restated: token_budget_estimator.py gates on the same numbers, and two copies
# would drift the moment a cap changes.
BUDGETS = SKILL_FILE_BUDGETS
CHAPTER_CEILING = CHAPTER_TOKEN_CEILING
SUPPORTING_FILENAMES = ("glossary.md", "patterns.md", "cheatsheet.md")

CLAUDE_CODE_TOOLS = {
    "Bash", "Read", "Write", "Edit", "Glob", "Grep",
    "WebFetch", "WebSearch", "NotebookEdit", "Task", "TodoWrite",
}
COPILOT_CLI_TOOLS = {"shell", "bash", "write"}
AMP_TOOLS = CLAUDE_CODE_TOOLS | {"shell_command"}

LENSES = {
    "claude": {
        "label": "Claude Code",
        "tools": CLAUDE_CODE_TOOLS,
        "recognized_keys": {"name", "description", "allowed-tools", "license", "metadata"},
        "reserved_name_words": {"anthropic", "claude"},
        "bash_tool_names": {"Bash"},
        "unknown_tool_severity": "error",
    },
    "copilot": {
        "label": "GitHub Copilot CLI",
        "tools": COPILOT_CLI_TOOLS,
        "recognized_keys": {"name", "description", "allowed-tools", "license"},
        "reserved_name_words": set(),
        "bash_tool_names": {"shell", "bash"},
        "unknown_tool_severity": "warn",
    },
    "amp": {
        "label": "Amp",
        "tools": AMP_TOOLS,
        "recognized_keys": {"name", "description", "allowed-tools", "license",
                            "compatibility", "argument-hint"},
        "reserved_name_words": set(),
        "bash_tool_names": {"shell_command", "Bash"},
        "unknown_tool_severity": "warn",
    },
}

_CONTENT_RULES = (
    ("prompt.ignore_previous",
     re.compile(r"\bignore\s+(?:(?:all|any|the)\s+)?(?:previous|prior)\s+"
                r"(?:instructions?|prompts?|rules?|messages?)\b", re.IGNORECASE),
     "instruction-override phrase"),
    ("prompt.disregard_system",
     re.compile(r"\bdisregard\s+(?:the\s+)?(?:system|developer)\b", re.IGNORECASE),
     "system-instruction override phrase"),
    ("prompt.role_reassignment",
     re.compile(r"\byou\s+are\s+now\b", re.IGNORECASE),
     "role-reassignment phrase"),
    ("prompt.fake_system_prefix",
     re.compile(r"^\s*(?:[-*]\s*)?(?:system|developer)\s*:", re.IGNORECASE),
     "system-like message prefix"),
    ("prompt.system_tag",
     re.compile(r"<\s*/?\s*system\b[^>]*>", re.IGNORECASE),
     "system-message tag"),
    ("prompt.chat_template_tag",
     re.compile(r"<\|\s*im_start\s*\|>|\[\s*INST\s*\]", re.IGNORECASE),
     "model chat-template delimiter"),
    ("prompt.tool_call_tag",
     re.compile(r"\btool[_ -]?call\b", re.IGNORECASE),
     "tool-call control token"),
)

_EXFILTRATION_TERM = re.compile(r"\bexfiltrat(?:e|es|ed|ing|ion)\b", re.IGNORECASE)
_OUTBOUND_TERM = re.compile(r"\b(?:curl|wget|send|post|upload|transmit)\b|https?://", re.IGNORECASE)
_SENSITIVE_TERM = re.compile(
    r"(?:\.env\b|\bbase64\b|\bsecrets?\b|\bcredentials?\b|\bapi[_ -]?keys?\b)", re.IGNORECASE)

_CHAPTER_LINK = re.compile(r"\]\(\s*(chapters/[^)\s]+\.md)\s*\)")
_TOPIC_REF = re.compile(r"→\s*(ch\d{1,3}(?:\s*,\s*ch\d{1,3})*)", re.IGNORECASE)
_CHAPTER_FILE = re.compile(r"^ch(\d{1,3})[-_]", re.IGNORECASE)


class ScanError(RuntimeError):
    """The generated skill could not be inspected completely."""


@dataclass(frozen=True)
class Finding:
    family: str
    severity: str  # "error" | "warn"
    path: str
    line: int
    rule_id: str
    message: str


def _terminal_safe(value: str) -> str:
    """Escape control and non-ASCII characters before printing untrusted paths."""
    return value.encode("unicode_escape", errors="backslashreplace").decode("ascii")


# --------------------------------------------------------------------------- collection


def _collect_skill_files(skill_dir: Path) -> tuple[Path, list[Path]]:
    requested = skill_dir.expanduser()
    if requested.name.lower() == "skill.md" and requested.is_file():
        requested = requested.parent
    if requested.is_symlink():
        raise ScanError("the generated skill directory must not be a symbolic link")
    try:
        root = requested.resolve(strict=True)
    except OSError as exc:
        raise ScanError(f"no such generated skill directory: {_terminal_safe(str(requested))}") from exc
    if not root.is_dir():
        raise ScanError("the generated skill path is not a directory")

    master = root / "SKILL.md"
    if not master.is_file() or master.is_symlink():
        raise ScanError("SKILL.md is missing or is a symbolic link")

    candidates = {master}
    for filename in SUPPORTING_FILENAMES:
        supporting = root / filename
        if supporting.is_symlink():
            raise ScanError(f"{filename} must be a real file, not a symbolic link")
        if supporting.exists():
            if not supporting.is_file():
                raise ScanError(f"{filename} must be a real file")
            candidates.add(supporting)

    chapters = root / "chapters"
    if chapters.exists():
        if chapters.is_symlink() or not chapters.is_dir():
            raise ScanError("chapters must be a real directory, not a symbolic link")
        candidates.update(chapters.glob("*.md"))

    files = sorted(candidates, key=lambda p: p.relative_to(root).as_posix().lower())
    if len(files) > MAX_SKILL_FILES:
        raise ScanError(f"generated skill has {len(files):,} Markdown files; "
                        f"maximum is {MAX_SKILL_FILES:,}")
    return root, files


def _read_skill_files(root: Path, files: list[Path]) -> dict[str, str]:
    contents: dict[str, str] = {}
    total_bytes = 0
    for path in files:
        if path.is_symlink():
            raise ScanError("generated skill contains a symbolic-link Markdown file")
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            raise ScanError(f"{_terminal_safe(path.name)} is {size:,} bytes; the per-file "
                            f"scan limit is {MAX_FILE_BYTES:,} bytes")
        total_bytes += size
        if total_bytes > MAX_TOTAL_BYTES:
            raise ScanError(f"generated skill Markdown exceeds the {MAX_TOTAL_BYTES:,}-byte scan limit")
        relative = path.relative_to(root).as_posix()
        try:
            contents[relative] = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ScanError(f"{_terminal_safe(relative)} is not valid UTF-8") from exc
        except OSError as exc:
            raise ScanError(f"could not read {_terminal_safe(relative)}") from exc
    return contents


# --------------------------------------------------------------------------- frontmatter


def parse_frontmatter(text: str) -> tuple[str | None, str]:
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return text[3:end].lstrip("\n"), text[end + 4:]


def scalar_value(fm: str, key: str) -> str | None:
    """Read a scalar frontmatter value, folding YAML continuation lines.

    A generated description often wraps: the value continues on following
    indented lines until the next top-level key. Reading only the first line
    under-reports its length (so the 1024-char cap never fires) and truncates it
    wherever it happens to have wrapped when it is copied into a manifest.
    """
    lines = fm.splitlines()
    for index, line in enumerate(lines):
        match = re.match(rf"^{re.escape(key)}:\s*(.*)$", line)
        if not match:
            continue
        parts = [match.group(1).strip()]
        for continuation in lines[index + 1:]:
            if not continuation.strip() or re.match(r"^[A-Za-z][\w-]*:", continuation):
                break
            if not continuation.startswith((" ", "\t")):
                break
            parts.append(continuation.strip())
        value = " ".join(part for part in parts if part).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        # A quoted YAML scalar escapes inner quotes; keep the text, drop the escape.
        return value.replace('\\"', '"').strip()
    return None


# Back-compat alias for the single-key reads below.
_scalar = scalar_value


def _list_items(fm: str, key: str) -> list[str]:
    items, capturing = [], False
    for line in fm.splitlines():
        if re.match(rf"^{re.escape(key)}:\s*$", line):
            capturing = True
            continue
        if capturing:
            item = re.match(r"^\s*-\s*(.+)$", line)
            if item:
                items.append(item.group(1).strip())
            elif re.match(r"^[A-Za-z][\w-]*:", line):
                break
    return items


def check_frontmatter(text: str, lens: str) -> list[Finding]:
    rules = LENSES[lens]
    label = rules["label"]
    fm, body = parse_frontmatter(text)
    out: list[Finding] = []

    def err(rule, msg, line=1):
        out.append(Finding("frontmatter", "error", "SKILL.md", line, rule, msg))

    def warn(rule, msg, line=1):
        out.append(Finding("frontmatter", "warn", "SKILL.md", line, rule, msg))

    if fm is None:
        err("fm.missing", "no valid YAML frontmatter (--- block)")
        return out

    name = _scalar(fm, "name")
    if not name:
        err("fm.name_missing", "name: missing (required)")
    else:
        if len(name) > 64:
            err("fm.name_length", f"name: {len(name)} > 64 chars")
        if not re.fullmatch(r"[a-z0-9-]+", name):
            err("fm.name_charset", f"name: '{name}' must be lowercase letters/digits/hyphens")
        if any(word in name.lower() for word in rules["reserved_name_words"]):
            err("fm.name_reserved", f"name: '{name}' contains a word reserved by {label}")

    description = _scalar(fm, "description")
    if not description:
        err("fm.description_missing", "description: missing (required)")
    else:
        if len(description) > 1024:
            err("fm.description_length", f"description: {len(description)} > 1024 chars")
        if not re.search(r"\buse\s+(?:when|before|after|while|for)\b", description, re.IGNORECASE):
            warn("fm.description_trigger",
                 "description has no explicit 'Use when ...' trigger — the agent has nothing "
                 "to match on when deciding whether to load this skill")

    tools = _list_items(fm, "allowed-tools")
    if not tools:
        inline = _scalar(fm, "allowed-tools")
        tools = inline.split() if inline else []
    if tools:
        bases = {entry.split("(", 1)[0].strip() for entry in tools}
        known = bases & rules["tools"]
        unknown = sorted(b for b in bases if b not in rules["tools"])
        uses_bash = "```bash" in body or "python3 " in body
        if uses_bash and not (bases & rules["bash_tool_names"]):
            names = " or ".join(f"'{n}'" for n in sorted(rules["bash_tool_names"]))
            err("fm.tools_missing_bash",
                f"allowed-tools declares a restriction but omits {names} while the skill runs "
                f"bash/python3 — under {label} those steps would be blocked")
        if not known and rules["unknown_tool_severity"] == "error":
            err("fm.tools_unrecognized", f"allowed-tools: no recognized {label} tool in the list")
        if unknown:
            warn("fm.tools_unknown_names",
                 f"allowed-tools: {unknown} are not {label} built-in tool names")

    for key in (m.group(1) for line in fm.splitlines()
                if (m := re.match(r"^([A-Za-z][\w-]*):", line))):
        if key not in rules["recognized_keys"]:
            warn("fm.key_unrecognized", f"frontmatter '{key}': not a recognized {label} key")

    lines = len(text.splitlines())
    if lines > 500:
        warn("fm.body_length", f"SKILL.md is {lines} lines > 500 (soft guideline)")
    return out


# --------------------------------------------------------------------------- safety


def _frontmatter_line_numbers(lines: list[str]) -> set[int]:
    if not lines or lines[0].strip() != "---":
        return set()
    for index, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return set(range(2, index))
    return set()


def check_safety(relative_path: str, text: str) -> list[Finding]:
    out: list[Finding] = []
    lines = text.splitlines()
    frontmatter_lines = _frontmatter_line_numbers(lines)

    for number, line in enumerate(lines, start=1):
        invisible = sorted({ord(c) for c in line if is_invisible_codepoint(ord(c))})
        if invisible:
            codepoints = ", ".join(f"U+{value:04X}" for value in invisible)
            out.append(Finding("safety", "error", relative_path, number, "unicode.invisible",
                               f"invisible Unicode code point(s): {codepoints} — extraction "
                               f"should have stripped these"))

        for rule_id, pattern, message in _CONTENT_RULES:
            if pattern.search(line):
                out.append(Finding("safety", "warn", relative_path, number, rule_id, message))

        if _EXFILTRATION_TERM.search(line) or (
            _OUTBOUND_TERM.search(line) and _SENSITIVE_TERM.search(line)
        ):
            out.append(Finding("safety", "warn", relative_path, number, "tool.exfiltration_shape",
                               "exfiltration-shaped tool or sensitive-data language"))

        if number in frontmatter_lines:
            if re.match(r"^\s*allowed-tools\s*:", line, re.IGNORECASE):
                out.append(Finding("safety", "error", relative_path, number,
                                   "frontmatter.allowed_tools",
                                   "generated frontmatter declares or widens tool authority"))
            if re.match(r"^\s*disable-model-invocation\s*:\s*[\"']?(?:false|no|0)[\"']?\s*(?:#.*)?$",
                        line, re.IGNORECASE):
                out.append(Finding("safety", "error", relative_path, number,
                                   "frontmatter.model_invocation_enabled",
                                   "generated frontmatter explicitly enables model invocation"))
    return out


# --------------------------------------------------------------------------- budget


def check_budgets(contents: dict[str, str]) -> list[Finding]:
    out: list[Finding] = []
    for filename, cap in BUDGETS.items():
        text = contents.get(filename)
        if text is None:
            severity = "error" if filename == "SKILL.md" else "warn"
            out.append(Finding("budget", severity, filename, 1, "budget.missing_file",
                               f"{filename} is missing — the converter's Step 8/9 output is incomplete"))
            continue
        tokens = estimate_tokens(text)
        if tokens > cap:
            # SKILL.md is the only hard cap: it is resident, and compaction
            # truncates from the end, so overflow silently drops the indexes.
            severity = "error" if filename == "SKILL.md" else "warn"
            out.append(Finding("budget", severity, filename, 1, "budget.over_cap",
                               f"~{tokens:,} tokens > {cap:,} cap"))

    for relative, text in contents.items():
        if not relative.startswith("chapters/"):
            continue
        tokens = estimate_tokens(text)
        if tokens > CHAPTER_CEILING:
            out.append(Finding("budget", "warn", relative, 1, "budget.chapter_over_ceiling",
                               f"~{tokens:,} tokens > {CHAPTER_CEILING:,} ceiling — chapters load "
                               f"on demand, but this one costs as much as the whole core"))
    return out


# --------------------------------------------------------------------------- index


def check_indexes(contents: dict[str, str]) -> list[Finding]:
    out: list[Finding] = []
    master = contents.get("SKILL.md", "")
    on_disk = {path for path in contents if path.startswith("chapters/")}

    linked: set[str] = set()
    for number, line in enumerate(master.splitlines(), start=1):
        for target in _CHAPTER_LINK.findall(line):
            linked.add(target)
            if target not in on_disk:
                out.append(Finding("index", "error", "SKILL.md", number, "index.dead_link",
                                   f"Chapter Index links {target}, which does not exist"))

    for orphan in sorted(on_disk - linked):
        out.append(Finding("index", "warn", orphan, 1, "index.unindexed_chapter",
                           "chapter file is not linked from the Chapter Index — the agent has "
                           "no way to navigate to it"))

    known_numbers = {
        int(match.group(1))
        for path in on_disk
        if (match := _CHAPTER_FILE.match(Path(path).name))
    }
    for number, line in enumerate(master.splitlines(), start=1):
        for group in _TOPIC_REF.findall(line):
            for token in re.findall(r"ch(\d{1,3})", group, re.IGNORECASE):
                if known_numbers and int(token) not in known_numbers:
                    out.append(Finding("index", "error", "SKILL.md", number, "index.topic_dangling",
                                       f"Topic Index points at ch{token}, which has no chapter file"))

    if on_disk and "## Topic Index" not in master:
        out.append(Finding("index", "warn", "SKILL.md", 1, "index.no_topic_index",
                           "no Topic Index section — topic lookup falls back to reading every "
                           "chapter, which is the cost this skill exists to avoid"))
    return out


# --------------------------------------------------------------------------- driver


def validate(skill_dir: Path, lens: str = "claude") -> list[Finding]:
    root, files = _collect_skill_files(skill_dir)
    contents = _read_skill_files(root, files)

    findings = check_frontmatter(contents["SKILL.md"], lens)
    for relative, text in contents.items():
        findings.extend(check_safety(relative, text))
    findings.extend(check_budgets(contents))
    findings.extend(check_indexes(contents))

    order = {"error": 0, "warn": 1}
    return sorted(findings, key=lambda f: (order[f.severity], f.path.lower(), f.line, f.rule_id))


SAMPLE_SKILL = {
    "SKILL.md": """---
name: sample-book-skill
description: "Knowledge base from \\"A Sample Book\\" by A. Author. Use when applying the
  author's frameworks, studying the book, or referencing its concepts."
---

# A Sample Book

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-discovery-tax.md) | The Discovery Loop Tax | Discovery Loop Tax |
| [ch02](chapters/ch02-missing.md) | Missing On Purpose | — |

## Topic Index

- **Discovery Loop Tax** → ch01
- **Never Written** → ch07
""",
    "chapters/ch01-discovery-tax.md": "# Chapter 1\n\n## Core Idea\nStructure once, query cheaply.\n",
    "glossary.md": "**Discovery Loop Tax** — repeated navigation cost (Ch 1)\n",
}


def run_sample(lens: str, as_json: bool, strict: bool) -> int:
    """Validate a deliberately broken sample skill: a dead chapter link, a
    dangling topic reference, and two missing supporting files.

    Always exits 0. This is a demonstration of what the four families report,
    not a gate — the findings below are the point, and a smoke test that fails
    on purpose is indistinguishable from one that is broken.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "sample-book-skill"
        (root / "chapters").mkdir(parents=True)
        for relative, text in SAMPLE_SKILL.items():
            (root / relative).write_text(text, encoding="utf-8")
        findings = validate(root, lens)
        if not as_json:
            print("Sample: a deliberately broken skill — a dead chapter link, a dangling topic\n"
                  "reference, and two missing supporting files. Expected findings:\n")
        report(findings, lens, as_json, strict)
        if not as_json:
            print("\n(sample run — exit 0 regardless; on a real skill these would be exit 1)")
        return 0


def report(findings: list[Finding], lens: str, as_json: bool, strict: bool) -> int:
    errors = [f for f in findings if f.severity == "error"]
    warns = [f for f in findings if f.severity == "warn"]

    if as_json:
        print(json.dumps({
            "lens": lens,
            "errors": len(errors),
            "warnings": len(warns),
            "findings": [asdict(f) for f in findings],
        }, indent=2, ensure_ascii=False))
    else:
        label = LENSES[lens]["label"]
        for finding in findings:
            marker = "ERROR" if finding.severity == "error" else "WARN "
            print(f"  {marker} [{finding.family}] {_terminal_safe(finding.path)}:{finding.line} "
                  f"({finding.rule_id}) {finding.message}")
        if findings:
            print(f"\n{len(errors)} error(s), {len(warns)} warning(s) [{label}]")
            print("Safety rules are intentionally broad and may match legitimate security or "
                  "AI-topic prose; review each finding in context. No files were modified.")
        else:
            print(f"Generated skill passed all checks [{label}].")

    return 1 if errors or (strict and warns) else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="book_skill_validator.py",
        description="Validate a generated book skill: frontmatter, safety, budgets, indexes.",
    )
    parser.add_argument("path", nargs="?", help="generated skill directory (or its SKILL.md)")
    parser.add_argument("--lens", choices=sorted(LENSES), default="claude",
                        help="which host's rules to validate against (default: claude)")
    parser.add_argument("--strict", action="store_true",
                        help="treat warnings as failures too")
    parser.add_argument("--output", choices=("text", "json"), default="text")
    parser.add_argument("--sample", action="store_true",
                        help="validate a built-in, deliberately broken sample skill")
    args = parser.parse_args(argv)

    if args.sample:
        return run_sample(args.lens, args.output == "json", args.strict)
    if not args.path:
        parser.print_usage(sys.stderr)
        print("ERROR: give a generated skill directory (or use --sample).", file=sys.stderr)
        return 2

    try:
        findings = validate(Path(args.path), args.lens)
    except ScanError as exc:
        print(f"ERROR validation incomplete: {exc}", file=sys.stderr)
        return 2
    return report(findings, args.lens, args.output == "json", args.strict)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # `tool | head` closes the pipe while this is still writing. Exit quietly
        # instead of dumping a traceback: redirect stdout to devnull first so the
        # interpreter's shutdown flush cannot re-raise. 141 = 128 + SIGPIPE.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(141)
