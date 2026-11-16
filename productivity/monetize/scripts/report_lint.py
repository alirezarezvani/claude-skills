#!/usr/bin/env python3
"""Lint a monetization report against the skill's own output contract.

Checks:
  - every required section (0-7, Appendix A, Appendix B) is present;
  - every item under section 7 (with its indented lines) carries a measurable
    acceptance criterion: "-> outcome" or "acceptance: outcome";
  - every money figure outside the appendices ($, CNY 500, 500元, 2万, 5k/month)
    carries a [n] citation or an "estimate" label;
  - every [n] citation resolves to an entry in Appendix A;
  - every Appendix A entry is cited somewhere in the body;
  - a body that mentions estimates has a non-empty Appendix B (not "n/a").

The money pattern is best-effort (symbols, ISO codes, 元/万/块, "5k/month");
spelled-out amounts such as "2,000 dollars" are not caught. The linter checks
form, not truth: an invented number with an invented Appendix A entry passes.

Exit codes:
  0  clean
  1  findings (details on stdout / in --json)
  2  usage error

Usage:
  python3 report_lint.py monetization-report.md
  python3 report_lint.py monetization-report.md --json
  python3 report_lint.py --sample
  python3 report_lint.py --sample-bad   # every finding path, exits 1
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
            out.setdefault(current, [])
        elif current is not None:
            out[current].append(line)
        # a repeated heading keeps appending to the first occurrence
    return {k: "\n".join(v) for k, v in out.items()}


def section_body(sections, prefix):
    for heading, body in sections.items():
        if heading.startswith(prefix):
            return body
    return ""


# A measurable acceptance criterion: an arrow to an outcome, or an explicit
# "acceptance:" label.
CRITERION = re.compile(r"(->|\u2192|acceptance\s*:)\s*\S", re.IGNORECASE)
# A money figure: currency symbol or code before or after a number, or a
# Chinese amount (500\u5143, 2\u4e07, 300\u5757), or a shorthand like 5k/month.
MONEY = re.compile(
    r"([$\u00a5\u20ac\u00a3]\s?\d"
    r"|\b(?:USD|EUR|CNY|RMB|GBP)\s?\d"
    r"|\d[\d,.]*\s?(?:USD|EUR|CNY|RMB|GBP)\b"
    r"|\d[\d,.]*\s?[\u5143\u4e07\u5757]"
    r"|\b\d+(?:\.\d+)?k\s?/\s?(?:mo|month|hr|hour|session|week)\b)",
    re.IGNORECASE,
)
# A figure counts as labeled only with an estimate label or a [n] citation.
ESTIMATE = re.compile(r"estimate", re.IGNORECASE)
CITATION = re.compile(r"\[(\d+)\]")
EMPTY = {"", "none", "n/a", "na", "-", "tbd"}


def is_empty(text):
    return text.strip().lower().rstrip(".") in EMPTY


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
            findings.append(f"missing section: expected a heading starting '{section}' (level-2, e.g. '{section} Title')")

    plan_body = section_body(sections, "## 7.")
    if plan_body:
        items = plan_items(plan_body)
        if not items:
            findings.append("section 7 has no checklist items")
        for item in items:
            if not CRITERION.search(item):
                findings.append(f"plan item without measurable acceptance criterion: {item[:80]}")

    appendix_a = section_body(sections, "## Appendix A")
    appendix_b = section_body(sections, "## Appendix B")
    sources = set(CITATION.findall(appendix_a))
    body_text = []
    for heading, body in sections.items():
        if heading.startswith("## Appendix"):
            continue
        body_text.append(body)
        for line in body.splitlines():
            cited = CITATION.findall(line)
            for ref in cited:
                if ref not in sources:
                    findings.append(f"citation [{ref}] in '{heading[:30]}' has no entry in Appendix A")
            if MONEY.search(line) and not cited and not ESTIMATE.search(line):
                findings.append(
                    f"money figure without a [n] citation or 'estimate' label in '{heading[:30]}': {line.strip()[:80]}"
                )
    body_text = "\n".join(body_text)
    used = set(CITATION.findall(body_text))
    for ref in sorted(sources - used, key=int):
        findings.append(f"Appendix A entry [{ref}] is never cited in the body")
    if re.search(r"\bestimate", body_text, re.IGNORECASE) and is_empty(appendix_b):
        findings.append("body mentions estimates but Appendix B is empty")

    return findings


BAD_SAMPLE = """# Monetization report - Bad · 2026-11-15
## 0. Asset snapshot
## 1. Hidden-skills audit
Supplier mediation earns ¥800 per case from this source.
## 2. Opportunity scan
Consulting at 5k/month [2].
## 3. Productization
## 4. Leverage point
## 5. Salary ceiling
Category manager, about 3万 (estimate).
## 6. AI side-hustle starter pack
## 7. 30-day plan
- Week 1: do things, at least 3
## Appendix A: sources
[1] Unused source.
## Appendix B: unverified estimates
n/a
"""

SAMPLE = """# Monetization report - Sam · 2026-11-15
## 0. Asset snapshot
Five years of sourcing experience.
## 1. Hidden-skills audit
Supplier dispute mediation.
## 2. Opportunity scan
Sourcing diagnostic, ¥500-1,500 per session (estimate, unverified).
## 3. Productization
Diagnostic offer.
## 4. Leverage point
Publish one case study.
## 5. Salary ceiling
Category manager, ¥35,000-45,000 [1].
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
    parser.add_argument("--sample", action="store_true", help="lint an embedded clean sample report")
    parser.add_argument("--sample-bad", action="store_true", help="lint an embedded report that breaks every rule")
    args = parser.parse_args()

    if args.sample or args.sample_bad:
        findings = lint(BAD_SAMPLE if args.sample_bad else SAMPLE)
        name = "<sample-bad>" if args.sample_bad else "<sample>"
        result = {"path": name, "findings": findings, "clean": not findings}
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
