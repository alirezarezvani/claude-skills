#!/usr/bin/env python3
"""pattern_miner.py — test whether an apparent LinkedIn pattern survives a null test.

The standard failure of LinkedIn analytics is a confident sentence built on four
posts: "carousels do 3x better for you". With post engagement as heavy-tailed as
it is, four posts will show a 3x difference between almost any two groups you
care to define.

So this tool tries to kill every candidate pattern before reporting it:

  1. Group size floor — at least 5 posts in the group and 5 outside it.
  2. Effect floor — the median engagement rate must differ by at least 15%
     relative. A statistically detectable 3% difference is not a decision.
  3. Permutation test — labels are shuffled a fixed number of times against a
     fixed seed, and the observed difference must beat at least 90% of the
     shuffles. Same data in, same verdict out.
  4. Multiple-comparisons note — every candidate tested is counted, and the
     expected number of false positives at the chosen threshold is reported
     alongside the number that passed. If you test twenty things at p<0.10, two
     will "pass" on noise alone, and the report says so.

Every rejected candidate is reported with the reason it failed, because "not
enough data yet" is the finding most of the time and it is a useful one.

Input: the same export shape as post_performance_analyzer.py.

Exit codes:
  0  at least one candidate survived
  2  nothing survived — reasons listed per candidate
  3  not enough posts to test anything (under 10)

Stdlib only. No network. Deterministic (fixed seed).
"""

import argparse
import csv
import datetime
import io
import json
import random
import sys

MIN_GROUP = 5
MIN_RELATIVE_EFFECT = 0.15
ALPHA = 0.10
SHUFFLES = 2000
SEED = 20260825
MIN_POSTS = 10

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

SAMPLE = [
    {"date": "2026-05-04", "impressions": 8120, "reactions": 214, "comments": 63, "reposts": 11,
     "format": "text-post", "pillar": "trust-debt", "chars": 1450},
    {"date": "2026-05-06", "impressions": 3050, "reactions": 61, "comments": 9, "reposts": 2,
     "format": "text-post", "pillar": "modelling", "chars": 620},
    {"date": "2026-05-11", "impressions": 2110, "reactions": 39, "comments": 6, "reposts": 1,
     "format": "text-post", "pillar": "hiring", "chars": 540},
    {"date": "2026-05-13", "impressions": 5400, "reactions": 132, "comments": 28, "reposts": 9,
     "format": "document-carousel", "pillar": "trust-debt", "chars": 900},
    {"date": "2026-05-18", "impressions": 4300, "reactions": 97, "comments": 24, "reposts": 5,
     "format": "text-post", "pillar": "trust-debt", "chars": 1610},
    {"date": "2026-05-20", "impressions": 1780, "reactions": 28, "comments": 3, "reposts": 0,
     "format": "text-post", "pillar": "modelling", "chars": 480},
    {"date": "2026-05-25", "impressions": 2450, "reactions": 44, "comments": 11, "reposts": 2,
     "format": "text-post", "pillar": "hiring", "chars": 700},
    {"date": "2026-05-27", "impressions": 6900, "reactions": 168, "comments": 41, "reposts": 14,
     "format": "document-carousel", "pillar": "trust-debt", "chars": 1100},
    {"date": "2026-06-01", "impressions": 3600, "reactions": 74, "comments": 15, "reposts": 3,
     "format": "document-carousel", "pillar": "modelling", "chars": 950},
    {"date": "2026-06-03", "impressions": 5100, "reactions": 121, "comments": 33, "reposts": 6,
     "format": "text-post", "pillar": "trust-debt", "chars": 1720},
    {"date": "2026-06-08", "impressions": 1950, "reactions": 31, "comments": 4, "reposts": 1,
     "format": "text-post", "pillar": "hiring", "chars": 510},
    {"date": "2026-06-10", "impressions": 2800, "reactions": 52, "comments": 12, "reposts": 2,
     "format": "text-post", "pillar": "modelling", "chars": 820},
    {"date": "2026-06-15", "impressions": 7400, "reactions": 181, "comments": 47, "reposts": 12,
     "format": "document-carousel", "pillar": "trust-debt", "chars": 1050},
    {"date": "2026-06-17", "impressions": 2300, "reactions": 40, "comments": 5, "reposts": 1,
     "format": "text-post", "pillar": "hiring", "chars": 560},
    {"date": "2026-06-22", "impressions": 6100, "reactions": 149, "comments": 38, "reposts": 10,
     "format": "document-carousel", "pillar": "trust-debt", "chars": 1180},
    {"date": "2026-06-24", "impressions": 2650, "reactions": 47, "comments": 9, "reposts": 2,
     "format": "text-post", "pillar": "modelling", "chars": 760},
]


def median(xs):
    s = sorted(xs)
    n = len(s)
    if not n:
        return 0.0
    mid = n // 2
    return float(s[mid]) if n % 2 else (s[mid - 1] + s[mid]) / 2.0


def _num(row, key, default=0):
    val = row.get(key, default)
    if val in (None, ""):
        return default
    try:
        return float(str(val).replace(",", "").strip())
    except ValueError:
        return default


def prepare(rows: list) -> list:
    out = []
    for r in rows:
        imp = _num(r, "impressions")
        if imp <= 0:
            continue
        inter = sum(_num(r, f) for f in ("reactions", "comments", "reposts"))
        rec = {"er": inter / imp,
               "format": str(r.get("format") or "unspecified"),
               "pillar": str(r.get("pillar") or "unspecified")}
        date = str(r.get("date") or "")
        try:
            rec["weekday"] = WEEKDAYS[datetime.date.fromisoformat(date[:10]).weekday()]
        except (ValueError, IndexError):
            rec["weekday"] = "unspecified"
        chars = _num(r, "chars", 0)
        if chars:
            rec["length"] = ("short (<800)" if chars < 800 else
                             "medium (800-1500)" if chars <= 1500 else "long (>1500)")
        else:
            rec["length"] = "unspecified"
        links = _num(r, "links_in_body", -1)
        rec["link_in_body"] = "unspecified" if links < 0 else ("yes" if links else "no")
        out.append(rec)
    return out


def permutation_p(group_ers, other_ers, observed, rng) -> float:
    pool = group_ers + other_ers
    k = len(group_ers)
    extreme = 0
    for _ in range(SHUFFLES):
        rng.shuffle(pool)
        diff = median(pool[:k]) - median(pool[k:])
        if abs(diff) >= abs(observed):
            extreme += 1
    return (extreme + 1) / (SHUFFLES + 1)


def mine(rows: list, attributes: list) -> dict:
    data = prepare(rows)
    if len(data) < MIN_POSTS:
        return {"verdict": "INSUFFICIENT_DATA", "exit_code": 3, "posts": len(data),
                "floor": MIN_POSTS,
                "finding": f"{len(data)} usable posts. Under {MIN_POSTS} there is nothing to test: "
                           "the between-post variance on LinkedIn swamps any group difference this "
                           "small a sample could show.",
                "instead": "Keep posting on the plan you have and re-run this in six weeks. "
                           "Changing strategy on eight posts is how people end up rewriting their "
                           "approach every month and compounding nothing."}

    rng = random.Random(SEED)
    candidates = []
    mirrored = []
    for attr in attributes:
        values = sorted({d[attr] for d in data if d[attr] != "unspecified"})
        # A two-value attribute is one test, not two: "carousel vs rest" and
        # "text vs rest" are the same comparison with the sign flipped. Testing
        # both would double-count it in the multiple-comparisons accounting.
        if len(values) == 2:
            mirrored.append(f"{attr}: only '{values[0]}' tested — '{values[1]}' is the same "
                            "comparison mirrored")
            values = values[:1]
        for val in values:
            group = [d["er"] for d in data if d[attr] == val]
            other = [d["er"] for d in data if d[attr] != val and d[attr] != "unspecified"]
            entry = {"attribute": attr, "value": val,
                     "n_group": len(group), "n_other": len(other)}
            if len(group) < MIN_GROUP or len(other) < MIN_GROUP:
                entry.update({"verdict": "NOT_TESTED",
                              "reason": f"needs {MIN_GROUP} in and {MIN_GROUP} out; "
                                        f"has {len(group)} and {len(other)}"})
                candidates.append(entry)
                continue
            m_g, m_o = median(group), median(other)
            observed = m_g - m_o
            rel = (m_g - m_o) / m_o if m_o else 0.0
            entry.update({"median_group": round(m_g, 5), "median_other": round(m_o, 5),
                          "relative_effect": round(rel, 3)})
            if abs(rel) < MIN_RELATIVE_EFFECT:
                entry.update({"verdict": "TOO_SMALL",
                              "reason": f"{rel:+.1%} relative difference is under the "
                                        f"{MIN_RELATIVE_EFFECT:.0%} floor — real or not, it is "
                                        "not a reason to change anything"})
                candidates.append(entry)
                continue
            p = permutation_p(list(group), list(other), observed, rng)
            entry["p_value"] = round(p, 4)
            if p < ALPHA:
                entry.update({"verdict": "SUPPORTED",
                              "reason": f"{rel:+.1%} median difference, beat {1 - p:.0%} of "
                                        f"{SHUFFLES} label shuffles"})
            else:
                entry.update({"verdict": "NOT_SUPPORTED",
                              "reason": f"{rel:+.1%} difference, but {p:.0%} of random shuffles "
                                        "produced one as large — this is noise"})
            candidates.append(entry)

    tested = [c for c in candidates if "p_value" in c]
    supported = [c for c in candidates if c["verdict"] == "SUPPORTED"]
    expected_false = round(len(tested) * ALPHA, 1)

    return {
        "verdict": "PATTERNS_FOUND" if supported else "NOTHING_SURVIVED",
        "exit_code": 0 if supported else 2,
        "posts": len(data),
        "method": {"min_group": MIN_GROUP, "min_relative_effect": MIN_RELATIVE_EFFECT,
                   "alpha": ALPHA, "shuffles": SHUFFLES, "seed": SEED,
                   "statistic": "difference of medians, permutation test"},
        "candidates_generated": len(candidates),
        "candidates_tested": len(tested),
        "supported": supported,
        "all_candidates": candidates,
        "mirrored_candidates_skipped": mirrored,
        "independence_note": (
            "Candidates within one attribute are not independent of each other — each group is "
            "tested against the rest of the same posts. Read them as one question about that "
            "attribute, not as several separate findings."),
        "multiple_comparisons_note": (
            f"{len(tested)} candidate(s) reached the test at alpha {ALPHA}. On noise alone you "
            f"would expect about {expected_false} to pass. {len(supported)} did. "
            + ("Treat these as hypotheses to test deliberately, not as conclusions."
               if len(supported) <= max(1, expected_false)
               else "More passed than chance predicts, which is mild evidence something real is "
                    "here — still worth confirming with a deliberate experiment.")),
        "next_step": "Feed a supported candidate to experiment_planner.py. A pattern found in "
                     "past data is a hypothesis; a pattern that survives a planned test is a "
                     "finding.",
    }


def render_human(r: dict) -> str:
    if r["verdict"] == "INSUFFICIENT_DATA":
        return (f"Pattern mining: INSUFFICIENT_DATA\n{'=' * 46}\n{r['finding']}\n\n"
                f"Instead: {r['instead']}")
    lines = [f"Pattern mining: {r['verdict']}  ({r['posts']} posts)", "=" * 62,
             f"Method: {r['method']['statistic']}, {r['method']['shuffles']} shuffles, "
             f"seed {r['method']['seed']}, alpha {r['method']['alpha']}, "
             f"min effect {r['method']['min_relative_effect']:.0%}, "
             f"min group {r['method']['min_group']}", ""]
    if r["supported"]:
        lines.append("SUPPORTED:")
        for c in r["supported"]:
            lines.append(f"  {c['attribute']}={c['value']}  n={c['n_group']} vs {c['n_other']}  "
                         f"{c['relative_effect']:+.1%}  p={c['p_value']}")
            lines.append(f"    {c['reason']}")
        lines.append("")
    lines.append("All candidates:")
    for c in r["all_candidates"]:
        lines.append(f"  [{c['verdict']:<14}] {c['attribute']}={c['value']:<20} {c['reason']}")
    if r.get("mirrored_candidates_skipped"):
        lines.append("\nSkipped as mirrored:")
        for m in r["mirrored_candidates_skipped"]:
            lines.append(f"  - {m}")
    lines += ["", r["independence_note"], "", r["multiple_comparisons_note"], "", r["next_step"]]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Test candidate LinkedIn patterns against a permutation null "
                    "(found=0 / nothing-survived=2 / insufficient-data=3).")
    ap.add_argument("--input", help="Post export file ('-' for stdin).")
    ap.add_argument("--csv", action="store_true", help="Input is CSV rather than JSON.")
    ap.add_argument("--attribute", action="append", default=[],
                    choices=["format", "pillar", "weekday", "length", "link_in_body"],
                    help="Attribute to test. Repeatable. Default: all five.")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Mine a built-in 16-post sample.")
    args = ap.parse_args()

    if args.sample:
        rows = SAMPLE
    elif args.input:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        try:
            rows = ([dict(r) for r in csv.DictReader(io.StringIO(raw))] if args.csv
                    else json.loads(raw))
        except (json.JSONDecodeError, csv.Error) as exc:
            print(f"ERROR: could not parse input: {exc}", file=sys.stderr)
            return 4
        if isinstance(rows, dict):
            rows = rows.get("posts") or rows.get("rows") or []
    else:
        ap.error("--input or --sample is required")

    attrs = args.attribute or ["format", "pillar", "weekday", "length", "link_in_body"]
    result = mine(rows, attrs)
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
