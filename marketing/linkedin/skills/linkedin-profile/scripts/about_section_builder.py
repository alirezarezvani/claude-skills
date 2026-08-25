#!/usr/bin/env python3
"""about_section_builder.py — assemble a LinkedIn About section that survives the fold.

LinkedIn collapses the About section after roughly the first 265-300 characters and
hides the rest behind "…see more". Most people spend that window on a warm-up
sentence, so the only part a stranger reads is the part that says nothing.

This tool assembles the section from named parts, then refuses the ones that break:
  - anything past the 2,600-character cap
  - a fold window that does not end on a sentence boundary (a truncated word is the
    reader's cue to stop)
  - a fold window carrying no audience and no proof
  - buzzword filler
  - a missing call to action (a profile that converts needs a next step)

It does not invent claims. Every part comes from you; the tool only orders,
measures, and refuses.

Exit codes:
  0  PASS  — assembled and clean
  2  WARN  — assembled, with non-blocking findings
  3  FAIL  — blocking findings; fix and re-run before publishing

Stdlib only. No network. Deterministic.
"""

import argparse
import json
import re
import sys

HARD_LIMIT = 2600
FOLD_SAFE = 265          # conservative end of the observed 265-300 truncation window
FOLD_OBSERVED = 300

BUZZWORDS = [
    "passionate about", "results-driven", "results driven", "detail-oriented",
    "detail oriented", "self-starter", "team player", "hard worker", "guru",
    "ninja", "rockstar", "thought leader", "seasoned professional", "dynamic",
    "proven track record", "wear many hats", "think outside the box",
    "synergy", "leverage my skills", "world-class", "cutting-edge",
]

PROOF_RE = re.compile(
    r"\d+\s*(%|x\b|×)|[$€£]\s?\d|\b\d+\s*(k|m|bn)\b|\bex-[A-Z]|"
    r"\b\d{1,3}(,\d{3})+\b|\b\d+\s*(users|customers|clients|teams|engineers|"
    r"subscribers|downloads|countries|years)\b", re.I)

AUDIENCE_RE = re.compile(
    r"\b(for|helping|i help|we help|i work with|my clients|founders|ctos?|cmos?|"
    r"engineers|designers|marketers|recruiters|startups|smbs|teams|operators|"
    r"clinicians|students|investors|product managers|data teams)\b", re.I)

SAMPLE = {
    "hook": "Most data teams do not have a data problem. They have a trust problem — "
            "nobody believes the dashboard, so everyone rebuilds the number in a spreadsheet.",
    "audience": "I work with Series A SaaS companies whose analytics stack grew faster than "
                "anyone's confidence in it.",
    "proof": [
        "Cut BigQuery spend 62% at Zendesk scale without dropping a single dashboard.",
        "Rebuilt reporting for three Series B teams; two of them retired their shadow spreadsheets inside a quarter.",
    ],
    "approach": "I start by finding the number people actually argue about, then work backwards "
                "through the dbt models to the BigQuery tables that produce it. Usually the fix "
                "is fewer models and clearer ownership, not more tooling — analytics engineering "
                "is a data governance problem wearing a modelling costume.",
    "cta": "If your team is re-deriving the same metric in three places, message me — I will tell "
           "you in one call whether it is a modelling problem or an ownership problem.",
    "keywords": ["analytics engineering", "dbt", "BigQuery", "data governance", "Series A SaaS"],
}

ORDER = ["hook", "audience", "proof", "approach", "cta"]


def assemble(parts: dict) -> str:
    blocks = []
    for key in ORDER:
        val = parts.get(key)
        if not val:
            continue
        if isinstance(val, list):
            blocks.append("\n".join(f"— {v.strip()}" for v in val if v.strip()))
        else:
            blocks.append(str(val).strip())
    body = "\n\n".join(b for b in blocks if b)
    kws = [k for k in (parts.get("keywords") or []) if k.strip()]
    if kws:
        body += "\n\nAreas I work in: " + " · ".join(k.strip() for k in kws)
    return body


def _fold_window(text: str) -> tuple:
    """Return (window, ends_cleanly, boundary_index)."""
    window = text[:FOLD_SAFE]
    if len(text) <= FOLD_SAFE:
        return window, True, len(text)
    # Last sentence-ending punctuation inside the safe window.
    boundary = max(window.rfind("."), window.rfind("!"), window.rfind("?"))
    return window, boundary >= FOLD_SAFE - 90, boundary


def validate(text: str, parts: dict) -> list:
    findings = []
    n = len(text)
    if n > HARD_LIMIT:
        findings.append({
            "severity": "blocking", "check": "length",
            "finding": f"{n} characters — {n - HARD_LIMIT} over the {HARD_LIMIT} cap. "
                       "LinkedIn will truncate or refuse it.",
            "fix": "Cut the approach block first; it is the part a reader can infer.",
        })
    if n < 400:
        findings.append({
            "severity": "warning", "check": "length",
            "finding": f"{n} characters. Under ~400 there is not room for both a claim and its proof.",
            "fix": "Add one concrete result with a number, or one sentence about who you are for.",
        })

    window, clean, boundary = _fold_window(text)
    if not clean:
        findings.append({
            "severity": "blocking", "check": "fold",
            "finding": f"The visible window (first ~{FOLD_SAFE} chars, truncation observed at "
                       f"{FOLD_SAFE}-{FOLD_OBSERVED}) cuts mid-sentence. A reader sees a broken "
                       "thought and stops.",
            "fix": f"Rewrite the opening so a sentence ends between character "
                   f"{FOLD_SAFE - 90} and {FOLD_SAFE}.",
        })
    if not AUDIENCE_RE.search(window) and not PROOF_RE.search(window):
        findings.append({
            "severity": "blocking", "check": "fold-content",
            "finding": "The visible window names no audience and carries no proof — it is a "
                       "warm-up, and the warm-up is all most readers get.",
            "fix": "Move the sentence that names who you are for, or the one with the number, "
                   "into the first two sentences.",
        })

    low = text.lower()
    hits = [b for b in BUZZWORDS if b in low]
    if hits:
        findings.append({
            "severity": "warning", "check": "buzzwords",
            "finding": f"Filler present: {', '.join(hits)}.",
            "fix": "Delete each one. If deleting it removes meaning, replace it with the "
                   "specific thing it was standing in for.",
        })

    if not parts.get("cta"):
        findings.append({
            "severity": "blocking", "check": "cta",
            "finding": "No call to action. The section ends and the reader has nothing to do.",
            "fix": "One line naming who should get in touch and what they will get from it.",
        })

    if not PROOF_RE.search(text):
        findings.append({
            "severity": "warning", "check": "proof",
            "finding": "No number, prior company, or scale signal anywhere in the section.",
            "fix": "One real, checkable data point. A range is fine; an invented figure is not.",
        })

    first_person = len(re.findall(r"\bI\b|\bmy\b|\bme\b", text))
    if first_person < 2:
        findings.append({
            "severity": "warning", "check": "voice",
            "finding": "Written in third person or with no first-person voice. On a personal "
                       "profile that reads as a press release someone else wrote.",
            "fix": "Write it as you would say it: 'I work with…', not 'Alex is a…'.",
        })

    kws = [k.strip().lower() for k in (parts.get("keywords") or []) if k.strip()]
    # Check against the prose only — the trailing "Areas I work in" list would
    # otherwise satisfy every keyword and make this check vacuous.
    prose = low.split("\n\nareas i work in:")[0]
    missing = [k for k in kws if k not in prose]
    if missing:
        findings.append({
            "severity": "warning", "check": "keywords",
            "finding": f"Declared keywords not present in the body: {', '.join(missing)} "
                       "(they appear only in the trailing list).",
            "fix": "Work the important ones into a real sentence. A keyword list at the bottom "
                   "is weaker than the same term used in context.",
        })
    return findings


def build(parts: dict) -> dict:
    text = assemble(parts)
    findings = validate(text, parts)
    blocking = [f for f in findings if f["severity"] == "blocking"]
    warnings = [f for f in findings if f["severity"] == "warning"]
    verdict, code = (("FAIL", 3) if blocking else ("WARN", 2) if warnings else ("PASS", 0))
    window, clean, _ = _fold_window(text)
    return {
        "verdict": verdict,
        "exit_code": code,
        "about": text,
        "chars": len(text),
        "limit": HARD_LIMIT,
        "visible_before_see_more": window,
        "fold_ends_on_sentence": clean,
        "findings": blocking + warnings,
        "note": ("The 2,600-character cap and the ~265-300 truncation window are "
                 "third-party-documented, not published by LinkedIn. The tool enforces the "
                 "conservative end of the window on purpose."),
    }


def render_human(r: dict) -> str:
    lines = [f"About section: {r['verdict']}  ({r['chars']}/{r['limit']} chars)", "=" * 56,
             "", "VISIBLE BEFORE \"…see more\":",
             f"  {r['visible_before_see_more']}",
             f"  [ends on a sentence: {'yes' if r['fold_ends_on_sentence'] else 'NO'}]", ""]
    if r["findings"]:
        lines.append("Findings:")
        for f in r["findings"]:
            lines.append(f"  [{f['severity'].upper():<8}] {f['check']}: {f['finding']}")
            lines.append(f"             fix → {f['fix']}")
    else:
        lines.append("No findings.")
    lines += ["", "-" * 56, "FULL SECTION", "-" * 56, r["about"], "", r["note"]]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Assemble and validate a LinkedIn About section "
                    "(PASS=0 / WARN=2 / FAIL=3).")
    ap.add_argument("--hook", help="Opening line: the tension or observation.")
    ap.add_argument("--audience", help="Who you are for, in their words.")
    ap.add_argument("--proof", action="append", default=[],
                    help="A real, checkable result. Repeatable.")
    ap.add_argument("--approach", help="How you work — the part that is yours.")
    ap.add_argument("--cta", help="Who should reach out and what they get.")
    ap.add_argument("--keyword", action="append", default=[],
                    help="A term you want to be findable for. Repeatable.")
    ap.add_argument("--input", help="Read all parts from a JSON file ('-' for stdin).")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Build the built-in sample section.")
    ap.add_argument("--print-schema", action="store_true",
                    help="Print the input JSON shape and exit.")
    args = ap.parse_args()

    if args.print_schema:
        print(json.dumps(SAMPLE, indent=2))
        return 0
    if args.sample:
        parts = SAMPLE
    elif args.input:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        try:
            parts = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"ERROR: input is not valid JSON: {exc}", file=sys.stderr)
            return 4
    else:
        parts = {"hook": args.hook, "audience": args.audience, "proof": args.proof,
                 "approach": args.approach, "cta": args.cta, "keywords": args.keyword}
        if not any(parts.values()):
            ap.error("provide at least --hook (or use --input / --sample / --print-schema)")

    result = build(parts)
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
