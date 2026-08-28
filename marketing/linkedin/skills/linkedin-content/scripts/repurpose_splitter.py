#!/usr/bin/env python3
"""repurpose_splitter.py — split long source material into standalone LinkedIn units.

Feed it an article, a talk transcript, a README, or your own notes. It cuts the
source into candidate post units, scores each on whether it can stand alone in a
feed, suggests a format, and refuses the ones that only make sense in context.

The part that matters is the reuse ledger. Repurposing fails in one specific way:
the same idea goes out three times over eight months and the audience notices
before the author does. `--ledger` keeps a content hash of every unit already
posted, so a unit that has run is skipped by default and shown with its date when
you ask for it.

The tool never writes the post. It hands you a unit, the reason it can stand
alone, and the gap you have to fill — which is always the same gap: the sentence
only you can write about what this cost you or taught you.

Exit codes:
  0  usable units found
  2  units found but all are weak (fix the flagged gaps before drafting)
  3  nothing in the source can stand alone — this is one post, not a series

Stdlib only. No network. Deterministic.
"""

import argparse
import hashlib
import json
import os
import re
import sys

MIN_UNIT, MAX_UNIT = 240, 2400
DANGLING_START = re.compile(
    r"^(this|these|those|that|it|they|he|she|such|as (mentioned|noted|we saw|discussed)|"
    r"the former|the latter|therefore|thus|however|but|and|so|which|meanwhile|"
    r"in conclusion|finally|next,)\b", re.I)

EVIDENCE_RE = re.compile(
    r"\d+\s*(%|x\b|×|ms\b|s\b|min\b|hours?|days?|weeks?|months?|years?)|"
    r"[$€£]\s?\d|\b\d{1,3}(,\d{3})+\b|\bversion \d|\b\d+\s*(users|customers|teams|"
    r"engineers|requests|rows|queries|tests)\b", re.I)

STORY_RE = re.compile(r"\b(i |we |my |our |the day|last (year|month|week)|when i|when we|"
                      r"turned out|i thought|we assumed|the mistake)\b", re.I)
STEP_RE = re.compile(r"(?m)^\s*(\d+[.)]|[-*•]|step \d)", re.I)
OPINION_RE = re.compile(r"\b(should|shouldn'?t|wrong|overrated|underrated|myth|"
                        r"stop |disagree|the real reason|nobody|most people)\b", re.I)

SAMPLE_SOURCE = """## Why our onboarding took six weeks

We measured it for the first time in March. Median time from contract signed to
first real use was 41 days. Nobody in the company believed the number, which is
usually the sign that it is right.

The instinct was to blame engineering capacity. We had a backlog of integration
work and it was easy to point at.

## The measurement that changed our mind

We instrumented each handoff instead of each step. Work-in-progress time was 6
days. Wait time between owners was 35 days. The work was not slow. The queue was.

That ratio — 6 to 35 — is the only number from this whole project I still quote.

## What we changed

1. One named owner for the whole path rather than one per stage.
2. Deleted the kickoff call, replaced it with a four-question form. 80% of
   accounts never needed the call at all.
3. Stopped treating the CRM stage as truth and started measuring first real use.

Median went to 4 days over the next quarter.

## What I got wrong

I spent five weeks building automation for the intake step before anyone measured
where the time went. The automation worked. It saved about four hours across the
whole quarter, against 35 days of queue time sitting untouched two steps later.
"""


def split_units(text: str) -> list:
    """Heading-aware split, falling back to paragraph accumulation."""
    heading_blocks = re.split(r"(?m)^#{1,6}\s+", text)
    if len(heading_blocks) > 2:
        units = []
        for block in heading_blocks[1:]:
            line, _, rest = block.partition("\n")
            body = rest.strip()
            if body:
                units.append({"title": line.strip(), "text": body})
        if units:
            return units

    units, buf = [], []
    for para in [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]:
        buf.append(para)
        joined = "\n\n".join(buf)
        if len(joined) >= MIN_UNIT:
            units.append({"title": "", "text": joined})
            buf = []
    if buf:
        joined = "\n\n".join(buf)
        if units and len(joined) < MIN_UNIT:
            units[-1]["text"] += "\n\n" + joined
        else:
            units.append({"title": "", "text": joined})
    return units


def suggest_format(unit_text: str) -> str:
    if STEP_RE.search(unit_text) and len(EVIDENCE_RE.findall(unit_text)) >= 2:
        return "document-carousel"
    if STORY_RE.search(unit_text):
        return "text-post"
    if OPINION_RE.search(unit_text):
        return "text-post"
    if EVIDENCE_RE.search(unit_text):
        return "image-post"
    return "text-post"


def score_unit(unit: dict) -> dict:
    text = unit["text"].strip()
    first = text.split("\n", 1)[0].strip()
    gaps, score = [], 0

    if MIN_UNIT <= len(text) <= MAX_UNIT:
        score += 25
    elif len(text) < MIN_UNIT:
        gaps.append({"gap": "too-thin",
                     "detail": f"{len(text)} chars — not enough to make a claim and back it.",
                     "fix": "Merge with the neighbouring section or drop it."})
    else:
        score += 10
        gaps.append({"gap": "too-long",
                     "detail": f"{len(text)} chars — over the {MAX_UNIT}-char working ceiling.",
                     "fix": "Split again at the strongest internal boundary; two posts beat one crammed one."})

    if DANGLING_START.match(first):
        gaps.append({"gap": "dangling-reference",
                     "detail": f"Opens with '{first.split()[0]}' — it refers to something the "
                               "reader never saw.",
                     "fix": "Rewrite the first sentence to name the thing outright."})
    else:
        score += 25

    ev = EVIDENCE_RE.findall(text)
    if ev:
        score += 25
    else:
        gaps.append({"gap": "no-evidence",
                     "detail": "No number, duration, or measurable detail.",
                     "fix": "Either add the real figure from the source, or route this to an "
                            "opinion post where the argument does the work."})

    sentences = [s for s in re.split(r"[.!?](?:\s|$)", text) if len(s.strip()) > 15]
    if len(sentences) >= 3:
        score += 25
    else:
        gaps.append({"gap": "fragment",
                     "detail": f"{len(sentences)} substantive sentence(s) — reads as a note, "
                               "not a post.",
                     "fix": "Expand or merge."})

    return {
        "title": unit["title"],
        "chars": len(text),
        "standalone_score": score,
        "suggested_format": suggest_format(text),
        "hook_candidate": first[:140],
        "gaps": gaps,
        "text": text,
        "author_gap": ("Every unit here is source material, not a post. Add the first-person "
                       "sentence only you can write: what it cost, what you assumed, or what "
                       "you would do differently."),
    }


def unit_hash(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.strip().lower())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def load_ledger(path: str) -> dict:
    if path and os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Split long source material into standalone LinkedIn units "
                    "(usable=0 / all-weak=2 / not-splittable=3).")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--input", help="Source file to split ('-' for stdin).")
    ap.add_argument("--ledger", help="JSON file tracking units already posted "
                                     "(created on --record if absent).")
    ap.add_argument("--record", action="append", default=[],
                    help="Mark a unit index as posted in the ledger. Repeatable.")
    ap.add_argument("--posted-on", default="",
                    help="Date string stored with --record entries (e.g. 2026-08-25).")
    ap.add_argument("--show-used", action="store_true",
                    help="Include units already in the ledger instead of skipping them.")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Split a built-in sample article.")
    args = ap.parse_args()

    if args.sample:
        text = SAMPLE_SOURCE
    elif args.input:
        text = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    else:
        ap.error("--input or --sample is required")

    ledger = load_ledger(args.ledger) if args.ledger else {}
    raw_units = split_units(text)
    scored = []
    for idx, u in enumerate(raw_units):
        s = score_unit(u)
        s["index"] = idx
        s["hash"] = unit_hash(s["text"])
        prev = ledger.get(s["hash"])
        s["already_posted"] = bool(prev)
        s["posted_on"] = prev.get("posted_on") if isinstance(prev, dict) else prev
        scored.append(s)

    if args.record:
        if not args.ledger:
            print("ERROR: --record requires --ledger", file=sys.stderr)
            return 4
        try:
            wanted = {int(i) for i in args.record}
        except ValueError:
            print("ERROR: --record takes unit indexes (integers)", file=sys.stderr)
            return 4
        for s in scored:
            if s["index"] in wanted:
                ledger[s["hash"]] = {"title": s["title"] or s["hook_candidate"][:60],
                                     "posted_on": args.posted_on or "unspecified"}
        with open(args.ledger, "w", encoding="utf-8") as fh:
            json.dump(ledger, fh, indent=2)

    visible = scored if args.show_used else [s for s in scored if not s["already_posted"]]
    # A unit with a structural gap is not usable however well it scores elsewhere:
    # a dangling opener or a fragment fails in the feed regardless of its evidence.
    disqualifying = {"too-thin", "dangling-reference", "fragment"}
    usable = [s for s in visible
              if s["standalone_score"] >= 75
              and not any(g["gap"] in disqualifying for g in s["gaps"])]
    skipped = len(scored) - len(visible)

    if not scored or (len(scored) == 1 and scored[0]["standalone_score"] < 75):
        decision, code = "NOT_SPLITTABLE", 3
    elif usable:
        decision, code = "USABLE", 0
    else:
        decision, code = "ALL_WEAK", 2

    result = {
        "decision": decision,
        "exit_code": code,
        "units_found": len(scored),
        "units_skipped_as_already_posted": skipped,
        "usable_units": len(usable),
        "units": sorted(visible, key=lambda s: -s["standalone_score"]),
        "ledger_path": args.ledger,
        "rule": ("A unit is source material, not a post. The tool never fabricates the "
                 "first-person line — that is the author's job and it is the only part "
                 "of a repurposed post that is actually new."),
    }

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Repurpose: {decision} — {len(scored)} unit(s), {len(usable)} usable"
              + (f", {skipped} skipped as already posted" if skipped else ""))
        print("=" * 64)
        for s in result["units"]:
            flag = "  [ALREADY POSTED %s]" % s["posted_on"] if s["already_posted"] else ""
            print(f"\n#{s['index']}  score {s['standalone_score']}/100  "
                  f"{s['chars']} chars  → {s['suggested_format']}{flag}")
            if s["title"]:
                print(f"   title: {s['title']}")
            print(f"   hook : {s['hook_candidate']}")
            for g in s["gaps"]:
                print(f"   gap  : [{g['gap']}] {g['detail']}")
                print(f"          fix → {g['fix']}")
        print(f"\n{result['rule']}")
    return code


if __name__ == "__main__":
    sys.exit(main())
