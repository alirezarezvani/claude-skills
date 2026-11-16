#!/usr/bin/env python3
"""Lint a monetization report against the skill's own output contract.

Checks:
  - every required section (0-7, Appendix A, Appendix B) is present;
  - every item under section 7 (with its indented lines) carries a measurable
    acceptance criterion: "-> outcome", "acceptance:", or "at least N";
  - every money figure outside the appendices is labeled (estimate,
    unverified, verified, source, [n]);
  - a body that claims verified numbers has sources in Appendix A;
  - a body that mentions estimates has entries in Appendix B.

Exit codes:
  0  clean
  1  findings (details on stdout / in --json)
  2  usage error

Usage:
  python3 report_lint.py monetization-report.md
  python3 report_lint.py monetization-report.md --json
  python3 report_lint.py --sample
"""

import argparse
import json
import re
import sys

REQUIRED = [
    "## 0.", "## 1.", "## 2.", "## 3.", "## 4.",
    "## 5.", "## 6.", "## 7.", "## Appendix A", "## Appendix B",
]

PLAN_ITEM = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+\S")


def split_sections(text):
    """Return mapping heading -> body text (headings are '## '-level)."""
    out, current = {}, None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line.strip()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def section_body(sections, prefix):
    for heading, body in sections.items():
        if heading.startswith(prefix):
            return body
    return ""


# A measurable acceptance criterion: an arrow to an outcome, an explicit
# "acceptance:" label, or a counted threshold ("at least 1", ">= 3").
CRITERION = re.compile(
    r"(->|\u2192|acceptance\s*:|\bat least \d+|>=\s*\d+|\u2265\s*\d+)",
    re.IGNORECASE,
)
# A money figure: a currency symbol or code next to a number.
MONEY = re.compile(r"([$\u00a5\u20ac\u00a3]\s?\d|\d[\d,.]*\s?(?:USD|EUR|CNY|RMB|GBP)\b)")
LABEL = re.compile(r"(estimate|unverified|verified|source|\[\d+\]|appendix)", re.IGNORECASE)


def plan_items(body):
    """Group a list item with its indented continuation lines."""
    items, current = [], None
    for line in body.splitlines():
        if PLAN_ITEM.match(line) and not line.startswith((" ", "\t")):
            current = [line.strip()]
            items.append(current)
        elif current is not None and line.strip() and line.startswith((" ", "\t")):
            current.append(line.strip())
        elif not line.strip():
            current = None
    return [" ".join(parts) for parts in items]


def lint(text):
    findings = []
    sections = split_sections(text)
    for section in REQUIRED:
        if not any(h.startswith(section) for h in sections):
            findings.append(f"missing section: {section}")

    plan_body = section_body(sections, "## 7.")
    if plan_body:
        items = plan_items(plan_body)
        if not items:
            findings.append("section 7 has no checklist items")
        for item in items:
            if not CRITERION.search(item):
                findings.append(f"plan item without measurable acceptance criterion: {item[:80]}")

    for heading, body in sections.items():
        if heading.startswith("## Appendix"):
            continue
        for line in body.splitlines():
            if MONEY.search(line) and not LABEL.search(line):
                findings.append(f"money figure with no source or label in '{heading[:30]}': {line.strip()[:80]}")

    body_text = "\n".join(b for h, b in sections.items() if not h.startswith("## Appendix"))
    appendix_a = section_body(sections, "## Appendix A").strip()
    appendix_b = section_body(sections, "## Appendix B").strip()
    if re.search(r"\bverified\b", body_text.replace("unverified", ""), re.IGNORECASE) and (
        not appendix_a or appendix_a.lower().rstrip(".") == "none"
    ):
        findings.append("body claims verified numbers but Appendix A lists no sources")
    if re.search(r"\bestimate", body_text, re.IGNORECASE) and not appendix_b:
        findings.append("body mentions estimates but Appendix B is empty")

    return findings


SAMPLE = """# Monetization report - Sam · 2026-11-15
## 0. Asset snapshot
Five years of sourcing experience.
## 1. Hidden-skills audit
Supplier dispute mediation.
## 2. Opportunity scan
Sourcing diagnostic, ¥500-1,500 per session (estimate).
## 3. Productization
Diagnostic offer.
## 4. Leverage point
Publish one case study.
## 5. Salary ceiling
Category manager, ¥35,000-45,000 (verified, see Appendix A [1]).
## 6. AI side-hustle starter pack
AI-assisted supplier vetting.
## 7. 30-day plan
- Week 1: publish 3 case notes -> at least 1 inbound inquiry
## Appendix A: sources
[1] Sample salary survey page, accessed 2026-11-15 (placeholder for a real URL).
## Appendix B: unverified estimates
Range from the default market table.
"""


def main():
    parser = argparse.ArgumentParser(description="Lint a monetization report against its output contract.")
    parser.add_argument("path", nargs="?", help="path to the report markdown")
    parser.add_argument("--json", action="store_true", help="emit JSON findings")
    parser.add_argument("--sample", action="store_true", help="lint an embedded sample report")
    args = parser.parse_args()

    if args.sample:
        findings = lint(SAMPLE)
        result = {"path": "<sample>", "findings": findings, "clean": not findings}
        print(json.dumps(result, indent=2))
        return 0 if not findings else 1

    if not args.path:
        parser.print_usage(sys.stderr)
        return 2

    try:
        with open(args.path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    findings = lint(text)
    if args.json:
        print(json.dumps({"path": args.path, "findings": findings, "clean": not findings}, indent=2))
    else:
        if not findings:
            print(f"clean: {args.path}")
        for item in findings:
            print(f"- {item}")
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
