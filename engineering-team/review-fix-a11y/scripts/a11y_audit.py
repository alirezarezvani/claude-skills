#!/usr/bin/env python3
"""
a11y_audit.py — Static accessibility audit for front-end projects.

Scans HTML, JSX, TSX, Vue, and template files for common accessibility issues.
Stdlib-only, zero pip installs required.

Usage:
    python scripts/a11y_audit.py /path/to/project
    python scripts/a11y_audit.py /path/to/project --json
    python scripts/a11y_audit.py /path/to/project --severity critical
    python scripts/a11y_audit.py index.html
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Issue severity constants
# ---------------------------------------------------------------------------
CRITICAL = "critical"
SERIOUS = "serious"
MODERATE = "moderate"
MINOR = "minor"

SEVERITY_ORDER = {CRITICAL: 0, SERIOUS: 1, MODERATE: 2, MINOR: 3}

# ---------------------------------------------------------------------------
# Patterns to detect
# ---------------------------------------------------------------------------

RULES = [
    {
        "id": "img-alt",
        "severity": CRITICAL,
        "description": "Image missing alt attribute",
        "pattern": re.compile(r'<img(?![^>]*\balt\s*=)[^>]*>', re.IGNORECASE),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "img-empty-alt-on-meaningful",
        "severity": MODERATE,
        "description": "Image has empty alt — ensure it is truly decorative",
        "pattern": re.compile(r'<img[^>]*\balt\s*=\s*["\']["\'][^>]*>', re.IGNORECASE),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "input-label",
        "severity": CRITICAL,
        "description": "Input may be missing an accessible label (no aria-label, aria-labelledby, or id for <label for>)",
        "pattern": re.compile(
            r'<input(?![^>]*\b(?:aria-label|aria-labelledby|id)\s*=)[^>]*>',
            re.IGNORECASE,
        ),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "button-name",
        "severity": CRITICAL,
        "description": "Button may lack an accessible name (no aria-label, aria-labelledby, or visible text)",
        "pattern": re.compile(
            r'<button(?![^>]*\b(?:aria-label|aria-labelledby)\s*=)[^>]*>\s*</button>',
            re.IGNORECASE,
        ),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "outline-none",
        "severity": CRITICAL,
        "description": "outline: none / outline: 0 removes focus indicator — replace with visible custom style",
        "pattern": re.compile(r'outline\s*:\s*(none|0)\b', re.IGNORECASE),
        "extensions": {".css", ".scss", ".sass", ".less"},
    },
    {
        "id": "div-onclick",
        "severity": SERIOUS,
        "description": "<div> with onClick/onclick but no role or tabindex — not keyboard accessible",
        "pattern": re.compile(
            r'<div(?![^>]*\b(?:role|tabindex|tabIndex)\s*=)[^>]*\bon[Cc]lick\s*[=={]',
            re.IGNORECASE,
        ),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "span-onclick",
        "severity": SERIOUS,
        "description": "<span> with onClick/onclick but no role or tabindex — not keyboard accessible",
        "pattern": re.compile(
            r'<span(?![^>]*\b(?:role|tabindex|tabIndex)\s*=)[^>]*\bon[Cc]lick\s*[=={]',
            re.IGNORECASE,
        ),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "link-purpose",
        "severity": SERIOUS,
        "description": 'Ambiguous link text ("click here", "read more", "here", "more") — use descriptive text',
        "pattern": re.compile(
            r'<a[^>]*>\s*(?:click here|read more|here|more|learn more|this link)\s*</a>',
            re.IGNORECASE,
        ),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "skip-link",
        "severity": SERIOUS,
        "description": "No skip navigation link found — add a 'Skip to main content' link as first focusable element",
        "pattern": None,  # Handled by absence check below
        "check_fn": "_check_skip_link",
        "extensions": {".html"},
    },
    {
        "id": "page-title",
        "severity": SERIOUS,
        "description": "No <title> element found in HTML page",
        "pattern": None,
        "check_fn": "_check_page_title",
        "extensions": {".html"},
    },
    {
        "id": "landmark-main",
        "severity": MODERATE,
        "description": "No <main> element or role='main' found — add a <main> landmark",
        "pattern": None,
        "check_fn": "_check_main_landmark",
        "extensions": {".html"},
    },
    {
        "id": "iframe-title",
        "severity": SERIOUS,
        "description": "<iframe> missing title or aria-label attribute",
        "pattern": re.compile(
            r'<iframe(?![^>]*\b(?:title|aria-label)\s*=)[^>]*>',
            re.IGNORECASE,
        ),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "table-th-scope",
        "severity": MODERATE,
        "description": "<th> missing scope attribute — add scope='col' or scope='row'",
        "pattern": re.compile(r'<th(?![^>]*\bscope\s*=)[^>]*>', re.IGNORECASE),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "autoplay-media",
        "severity": SERIOUS,
        "description": "Media element with autoplay — provide controls and mute by default",
        "pattern": re.compile(r'<(?:video|audio)[^>]*\bautoplay\b', re.IGNORECASE),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "positive-tabindex",
        "severity": MODERATE,
        "description": "tabindex > 0 disrupts natural focus order — prefer tabindex='0' or '-1'",
        "pattern": re.compile(r'tabindex\s*=\s*["\']?[1-9]\d*["\']?', re.IGNORECASE),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "aria-hidden-focusable",
        "severity": CRITICAL,
        "description": "aria-hidden='true' on element that may be focusable — hidden content must not receive focus",
        "pattern": re.compile(
            r'<(?:button|a|input|select|textarea)[^>]*\baria-hidden\s*=\s*["\']true["\']',
            re.IGNORECASE,
        ),
        "extensions": {".html", ".jsx", ".tsx", ".vue"},
    },
    {
        "id": "heading-skip",
        "severity": MODERATE,
        "description": "Heading level skip detected (e.g. h1 → h3) — use sequential heading levels",
        "pattern": None,
        "check_fn": "_check_heading_order",
        "extensions": {".html"},
    },
]

# ---------------------------------------------------------------------------
# Absence/document-level checks
# ---------------------------------------------------------------------------

def _check_skip_link(content: str, filepath: str) -> bool:
    """Returns True (issue exists) if no skip link found."""
    return not re.search(
        r'href\s*=\s*["\']#(?:main|content|skip|main-content)["\']',
        content,
        re.IGNORECASE,
    )


def _check_page_title(content: str, filepath: str) -> bool:
    return not re.search(r'<title[^>]*>\s*\S', content, re.IGNORECASE)


def _check_main_landmark(content: str, filepath: str) -> bool:
    has_main_tag = bool(re.search(r'<main[\s>]', content, re.IGNORECASE))
    has_role_main = bool(re.search(r'role\s*=\s*["\']main["\']', content, re.IGNORECASE))
    return not (has_main_tag or has_role_main)


def _check_heading_order(content: str, filepath: str) -> bool:
    levels = [int(m) for m in re.findall(r'<h([1-6])[\s>]', content, re.IGNORECASE)]
    for i in range(1, len(levels)):
        if levels[i] > levels[i - 1] + 1:
            return True
    return False


ABSENCE_CHECKS = {
    "_check_skip_link": _check_skip_link,
    "_check_page_title": _check_page_title,
    "_check_main_landmark": _check_main_landmark,
    "_check_heading_order": _check_heading_order,
}

# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

SCAN_EXTENSIONS = {".html", ".htm", ".jsx", ".tsx", ".vue", ".css", ".scss", ".sass", ".less"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "coverage", "__pycache__", ".venv"}


def _get_line_number(content: str, match_start: int) -> int:
    return content[:match_start].count("\n") + 1


def audit_file(filepath: Path) -> list[dict]:
    issues = []
    ext = filepath.suffix.lower()
    if ext not in SCAN_EXTENSIONS:
        return issues

    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return issues

    for rule in RULES:
        if ext not in rule["extensions"]:
            continue

        if rule.get("pattern"):
            for match in rule["pattern"].finditer(content):
                issues.append({
                    "rule": rule["id"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "file": str(filepath),
                    "line": _get_line_number(content, match.start()),
                    "snippet": match.group(0)[:120].strip(),
                })
        elif rule.get("check_fn"):
            fn = ABSENCE_CHECKS.get(rule["check_fn"])
            if fn and fn(content, str(filepath)):
                issues.append({
                    "rule": rule["id"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "file": str(filepath),
                    "line": None,
                    "snippet": None,
                })

    return issues


def audit_path(target: Path, severity_filter: str | None = None) -> list[dict]:
    issues = []

    if target.is_file():
        issues.extend(audit_file(target))
    else:
        for root, dirs, files in os.walk(target):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fname in files:
                fp = Path(root) / fname
                issues.extend(audit_file(fp))

    if severity_filter:
        threshold = SEVERITY_ORDER.get(severity_filter, 3)
        issues = [i for i in issues if SEVERITY_ORDER.get(i["severity"], 3) <= threshold]

    issues.sort(key=lambda i: (SEVERITY_ORDER.get(i["severity"], 3), i["file"], i.get("line") or 0))
    return issues

# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

SEVERITY_EMOJI = {CRITICAL: "🔴", SERIOUS: "🟠", MODERATE: "🟡", MINOR: "⚪"}


def print_report(issues: list[dict], target: str) -> None:
    counts = {s: 0 for s in [CRITICAL, SERIOUS, MODERATE, MINOR]}
    for i in issues:
        counts[i["severity"]] = counts.get(i["severity"], 0) + 1

    print(f"\n{'='*60}")
    print(f"  A11Y AUDIT: {target}")
    print(f"{'='*60}")
    print(f"  Total issues: {len(issues)}")
    for sev, count in counts.items():
        if count:
            print(f"  {SEVERITY_EMOJI[sev]} {sev.upper()}: {count}")
    print(f"{'='*60}\n")

    if not issues:
        print("✅ No issues detected by static analysis.")
        print("   Run Lighthouse, axe, or pa11y for dynamic/runtime checks.\n")
        return

    current_file = None
    for issue in issues:
        if issue["file"] != current_file:
            current_file = issue["file"]
            print(f"\n📄 {current_file}")

        line_info = f"  line {issue['line']}" if issue.get("line") else ""
        print(f"  {SEVERITY_EMOJI[issue['severity']]} [{issue['severity'].upper()}] {issue['rule']}{line_info}")
        print(f"     {issue['description']}")
        if issue.get("snippet"):
            snippet = issue["snippet"].replace("\n", " ")
            print(f"     → {snippet[:100]}")

    print(f"\n{'='*60}")
    print("  Next steps:")
    print("  1. Fix critical issues first (keyboard/screen reader blocking)")
    print("  2. Run: npx @axe-core/cli <url>  for runtime checks")
    print("  3. Run: npx pa11y <url>  for full WCAG scan")
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Static a11y audit for front-end projects.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("path", help="File or directory to audit")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument(
        "--severity",
        choices=[CRITICAL, SERIOUS, MODERATE, MINOR],
        help="Only show issues at or above this severity",
    )
    args = parser.parse_args()

    target = Path(args.path)
    if not target.exists():
        print(f"Error: path not found: {target}", file=sys.stderr)
        sys.exit(1)

    issues = audit_path(target, args.severity)

    if args.json:
        print(json.dumps({"total": len(issues), "issues": issues}, indent=2))
    else:
        print_report(issues, str(target))

    # Exit code: 1 if any critical/serious issues found
    has_blocking = any(i["severity"] in {CRITICAL, SERIOUS} for i in issues)
    sys.exit(1 if has_blocking else 0)


if __name__ == "__main__":
    main()
