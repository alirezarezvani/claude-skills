#!/usr/bin/env python3
"""Lint a monetization report against the skill's own output contract.

Checks:
  - every required section (0-7, Appendix A, Appendix B) is present;
  - every item under section 7 carries an acceptance criterion;
  - when the body mentions estimates, Appendix B is not empty.

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
    lines = text.splitlines()
    out, current = {}, None
    for line in lines:
        if line.startswith("## "):
            current = line.strip()
            out[current] = []
        elif current is not None:
            out[current].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def lint(text):
    findings = []
    for section in REQUIRED:
        if not any(h.startswith(section) for h in split_sections(text)):
            findings.append(f"missing section: {section}")

    sections = split_sections(text)
    plan_body = ""
    for heading, body in sections.items():
        if heading.startswith("## 7."):
            plan_body = body
            break
    if plan_body:
        items = [ln for ln in plan_body.splitlines() if PLAN_ITEM.match(ln)]
        for ln in items:
            if not re.search(r"(acceptance|→|->|verify|check)", ln, re.IGNORECASE):
                findings.append(f"plan item without acceptance criterion: {ln.strip()[:80]}")
        if not items:
            findings.append("section 7 has no checklist items")

    body_text = text
    appendix_b = ""
    for heading, body in sections.items():
        if heading.startswith("## Appendix B"):
            appendix_b = body.strip()
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
Category manager, ¥35,000-45,000 (verified, sample data).
## 6. AI side-hustle starter pack
AI-assisted supplier vetting.
## 7. 30-day plan
- Week 1: publish 3 case notes -> at least 1 inbound inquiry
## Appendix A: sources
None.
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
