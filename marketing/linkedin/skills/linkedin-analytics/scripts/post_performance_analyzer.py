#!/usr/bin/env python3
"""post_performance_analyzer.py — read your own exported post stats and describe them honestly.

Input is the export LinkedIn gives you for your own content (Analytics → Post
impressions → Export, or the JSON shape below). Nothing is fetched and no other
member's data is involved.

What it does that a spreadsheet does not:

  - engagement rate per post on a consistent denominator, so posts are comparable
  - median and MAD rather than mean and standard deviation, because LinkedIn post
    performance is heavy-tailed and one breakout post drags a mean somewhere
    useless
  - percentile bands and an IQR outlier test, so "this did well" has a threshold
  - an explicit refusal to characterise a body of work under 10 posts

The last one is the point. Ten posts is not enough to conclude anything, and the
tool says so rather than producing a confident-looking table.

Input JSON: [{"date": "2026-05-04", "title": "...", "impressions": 4210,
              "reactions": 88, "comments": 21, "reposts": 4,
              "format": "text-post", "pillar": "trust-debt"}, ...]
CSV with the same column names also works.

Exit codes:
  0  analysed
  2  analysed, but below the 10-post floor — descriptive only, no conclusions
  3  unusable input (no rows, or no impressions column)

Stdlib only. No network.
"""

import argparse
import csv
import io
import json
import sys

MIN_POSTS_FOR_CONCLUSIONS = 10
REQUIRED = ("impressions",)
INTERACTION_FIELDS = ("reactions", "comments", "reposts")

SAMPLE = [
    {"date": "2026-05-04", "title": "Onboarding 6 weeks to 4 days", "impressions": 8120,
     "reactions": 214, "comments": 63, "reposts": 11, "format": "text-post", "pillar": "trust-debt"},
    {"date": "2026-05-11", "title": "dbt exposures rollout", "impressions": 3050,
     "reactions": 61, "comments": 9, "reposts": 2, "format": "text-post", "pillar": "modelling"},
    {"date": "2026-05-18", "title": "Hiring the first AE", "impressions": 2110,
     "reactions": 39, "comments": 6, "reposts": 1, "format": "text-post", "pillar": "hiring"},
    {"date": "2026-05-25", "title": "Cost teardown carousel", "impressions": 5400,
     "reactions": 132, "comments": 28, "reposts": 9, "format": "document-carousel",
     "pillar": "trust-debt"},
    {"date": "2026-06-01", "title": "Why we deleted the kickoff call", "impressions": 4300,
     "reactions": 97, "comments": 24, "reposts": 5, "format": "text-post", "pillar": "trust-debt"},
    {"date": "2026-06-08", "title": "Modelling tradeoffs", "impressions": 1780,
     "reactions": 28, "comments": 3, "reposts": 0, "format": "text-post", "pillar": "modelling"},
    {"date": "2026-06-15", "title": "Analytics eng job spec", "impressions": 2450,
     "reactions": 44, "comments": 11, "reposts": 2, "format": "text-post", "pillar": "hiring"},
    {"date": "2026-06-22", "title": "Queue time carousel", "impressions": 6900,
     "reactions": 168, "comments": 41, "reposts": 14, "format": "document-carousel",
     "pillar": "trust-debt"},
    {"date": "2026-06-29", "title": "Three dbt anti-patterns", "impressions": 3600,
     "reactions": 74, "comments": 15, "reposts": 3, "format": "document-carousel",
     "pillar": "modelling"},
    {"date": "2026-07-06", "title": "What I got wrong about capacity", "impressions": 5100,
     "reactions": 121, "comments": 33, "reposts": 6, "format": "text-post", "pillar": "trust-debt"},
    {"date": "2026-07-13", "title": "Interview loop for AEs", "impressions": 1950,
     "reactions": 31, "comments": 4, "reposts": 1, "format": "text-post", "pillar": "hiring"},
    {"date": "2026-07-20", "title": "Freshness SLAs", "impressions": 2800,
     "reactions": 52, "comments": 12, "reposts": 2, "format": "text-post", "pillar": "modelling"},
]


def median(xs):
    s = sorted(xs)
    n = len(s)
    if not n:
        return 0.0
    mid = n // 2
    return float(s[mid]) if n % 2 else (s[mid - 1] + s[mid]) / 2.0


def percentile(xs, p):
    s = sorted(xs)
    if not s:
        return 0.0
    k = (len(s) - 1) * (p / 100.0)
    lo, hi = int(k), min(int(k) + 1, len(s) - 1)
    return float(s[lo] + (s[hi] - s[lo]) * (k - lo))


def load_rows(raw: str, as_csv: bool) -> list:
    if as_csv:
        return [dict(r) for r in csv.DictReader(io.StringIO(raw))]
    data = json.loads(raw)
    if isinstance(data, dict):
        data = data.get("posts") or data.get("rows") or []
    return data


def _num(row, key):
    val = row.get(key, 0)
    if val in (None, ""):
        return 0
    try:
        return float(str(val).replace(",", "").strip())
    except ValueError:
        return 0


def analyse(rows: list) -> dict:
    clean = []
    for r in rows:
        imp = _num(r, "impressions")
        if imp <= 0:
            continue
        inter = sum(_num(r, f) for f in INTERACTION_FIELDS)
        clean.append({
            "date": str(r.get("date", "")),
            "title": str(r.get("title", ""))[:80],
            "impressions": int(imp),
            "reactions": int(_num(r, "reactions")),
            "comments": int(_num(r, "comments")),
            "reposts": int(_num(r, "reposts")),
            "interactions": int(inter),
            "engagement_rate": round(inter / imp, 5),
            "comment_share": round(_num(r, "comments") / inter, 3) if inter else 0.0,
            "format": str(r.get("format", "") or "unspecified"),
            "pillar": str(r.get("pillar", "") or "unspecified"),
        })

    if not clean:
        return {"verdict": "UNUSABLE", "exit_code": 3,
                "finding": "No rows with a positive impressions value.",
                "fix": "Export from LinkedIn Analytics → Post impressions → Export, or supply "
                       "JSON with an 'impressions' field per post."}

    ers = [p["engagement_rate"] for p in clean]
    imps = [p["impressions"] for p in clean]
    med = median(ers)
    mad = median([abs(e - med) for e in ers])
    q1, q3 = percentile(ers, 25), percentile(ers, 75)
    iqr = q3 - q1
    hi_fence, lo_fence = q3 + 1.5 * iqr, q1 - 1.5 * iqr

    for p in clean:
        e = p["engagement_rate"]
        if e >= hi_fence:
            p["band"] = "BREAKOUT"
        elif e >= q3:
            p["band"] = "STRONG"
        elif e >= q1:
            p["band"] = "TYPICAL"
        elif e > lo_fence:
            p["band"] = "WEAK"
        else:
            p["band"] = "DUD"

    n = len(clean)
    below_floor = n < MIN_POSTS_FOR_CONCLUSIONS
    result = {
        "verdict": "DESCRIPTIVE_ONLY" if below_floor else "ANALYSED",
        "exit_code": 2 if below_floor else 0,
        "posts_analysed": n,
        "floor": MIN_POSTS_FOR_CONCLUSIONS,
        "engagement_rate": {
            "median": round(med, 5),
            "mad": round(mad, 5),
            "p10": round(percentile(ers, 10), 5),
            "p25": round(q1, 5), "p75": round(q3, 5),
            "p90": round(percentile(ers, 90), 5),
            "breakout_threshold": round(hi_fence, 5),
        },
        "impressions": {"median": round(median(imps)), "p90": round(percentile(imps, 90)),
                        "total": int(sum(imps))},
        "bands": {b: sum(1 for p in clean if p["band"] == b)
                  for b in ("BREAKOUT", "STRONG", "TYPICAL", "WEAK", "DUD")},
        "posts": sorted(clean, key=lambda p: -p["engagement_rate"]),
        "reading_notes": [
            "Median and MAD, not mean and standard deviation: one breakout post makes a mean "
            "describe a distribution nobody's posts belong to.",
            "Impressions are not unique people, and LinkedIn's definition has changed over time. "
            "Compare posts from the same period, not across a year.",
            "Comment share is worth watching separately: comments are the costlier signal for a "
            "reader to give, and the one most closely tied to distribution.",
        ],
    }
    if below_floor:
        result["warning"] = (
            f"{n} posts is below the {MIN_POSTS_FOR_CONCLUSIONS}-post floor. Everything above is "
            "description, not evidence. Do not change strategy on it — the variance between two "
            "posts on the same topic is routinely larger than the difference this would 'show'.")
    return result


def render_human(r: dict) -> str:
    if r["verdict"] == "UNUSABLE":
        return f"Post analysis: UNUSABLE\n{'=' * 40}\n{r['finding']}\nfix → {r['fix']}"
    e = r["engagement_rate"]
    lines = [f"Post analysis: {r['verdict']}  ({r['posts_analysed']} posts)", "=" * 60]
    if "warning" in r:
        lines += [f"! {r['warning']}", ""]
    lines += [
        f"Engagement rate  median {e['median']:.2%}  (MAD {e['mad']:.2%})",
        f"                 p10 {e['p10']:.2%} · p25 {e['p25']:.2%} · p75 {e['p75']:.2%} · "
        f"p90 {e['p90']:.2%}",
        f"Breakout above   {e['breakout_threshold']:.2%}",
        f"Impressions      median {r['impressions']['median']:,} · "
        f"p90 {r['impressions']['p90']:,} · total {r['impressions']['total']:,}",
        f"Bands            " + " · ".join(f"{k} {v}" for k, v in r["bands"].items()),
        "", "Posts by engagement rate:"]
    for p in r["posts"]:
        lines.append(f"  {p['band']:<9} {p['engagement_rate']:>7.2%}  "
                     f"{p['impressions']:>7,} imp  {p['comments']:>3}c  "
                     f"{p['date']:<11} {p['title']}")
    lines.append("\nReading notes:")
    for note in r["reading_notes"]:
        lines.append(f"  - {note}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Describe your own LinkedIn post export honestly "
                    "(analysed=0 / below-floor=2 / unusable=3).")
    ap.add_argument("--input", help="Post export file ('-' for stdin).")
    ap.add_argument("--csv", action="store_true", help="Input is CSV rather than JSON.")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Analyse a built-in 12-post sample.")
    ap.add_argument("--print-schema", action="store_true", help="Print the input shape and exit.")
    args = ap.parse_args()

    if args.print_schema:
        print(json.dumps(SAMPLE[:2], indent=2))
        return 0
    if args.sample:
        rows = SAMPLE
    elif args.input:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        try:
            rows = load_rows(raw, args.csv)
        except (json.JSONDecodeError, csv.Error) as exc:
            print(f"ERROR: could not parse input: {exc}", file=sys.stderr)
            return 4
    else:
        ap.error("--input or --sample is required (see --print-schema)")

    result = analyse(rows)
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
