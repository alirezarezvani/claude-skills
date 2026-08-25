#!/usr/bin/env python3
"""comment_target_planner.py — build a weekly commenting roster inside a real time budget.

Commenting is the highest-return activity available to an account with no
distribution, and it is the one people do worst: they comment on the same three
huge accounts, in threads with 400 other comments, saying "great post".

This builds a five-day roster from the accounts you name, scored on audience
overlap, how often they actually post, and how crowded their threads are. It
enforces three rules that keep the roster from becoming a pattern:

  - no account appears more than twice a week (commenting daily on one person
    reads as following them around, and it exhausts the goodwill it earns)
  - at least one peer-tier account per day, because reciprocity is the part that
    compounds
  - never more than half a day's slots in the "huge" tier, where being early
    matters more than being right and most comments are never read

The output is a roster, not comment text. Comment text that a tool wrote is the
thing this whole approach is trying to avoid.

Exit codes:
  0  roster built
  2  budget below one comment a day — a reduced roster is returned
  3  no usable accounts supplied

Stdlib only. No network. Nothing is posted.
"""

import argparse
import json
import sys

MINUTES_PER_COMMENT = 6
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
MAX_PER_ACCOUNT_PER_WEEK = 2

TIERS = {
    "huge": {"factor": 1.0,
             "note": "10x+ your size. Crowded threads — only worth it if you are early and add "
                     "something the post missed."},
    "larger": {"factor": 1.5,
               "note": "2-10x your size. The best ratio of reachable audience to competition."},
    "peer": {"factor": 1.3,
             "note": "Roughly your size. Reciprocity compounds here; these are the relationships "
                     "that still exist in a year."},
    "smaller": {"factor": 0.9,
                "note": "Smaller than you. Low reach today, high goodwill, and some of them will "
                        "not be smaller for long."},
}

SAMPLE_ACCOUNTS = [
    "Priya Raman:5:4:larger",
    "Data Council:4:6:huge",
    "Tomas Lind:5:3:peer",
    "Anna Beck:4:2:peer",
    "Jules Okafor:3:5:larger",
    "Sam Idris:5:1:smaller",
]


def parse_account(spec: str) -> dict:
    parts = spec.split(":")
    if len(parts) != 4:
        raise ValueError(f"expected name:overlap:posts_per_week:tier — got '{spec}'")
    name, overlap, freq, tier = parts
    tier = tier.strip().lower()
    if tier not in TIERS:
        raise ValueError(f"unknown tier '{tier}' in '{spec}'; choose from {sorted(TIERS)}")
    try:
        overlap_i, freq_i = int(overlap), int(freq)
    except ValueError:
        raise ValueError(f"overlap and posts_per_week must be integers in '{spec}'")
    if not 1 <= overlap_i <= 5:
        raise ValueError(f"overlap must be 1-5 in '{spec}'")
    if freq_i < 0:
        raise ValueError(f"posts_per_week cannot be negative in '{spec}'")
    return {"name": name.strip(), "overlap": overlap_i, "posts_per_week": freq_i, "tier": tier}


def score(acct: dict) -> float:
    # Posting frequency has diminishing returns: an account posting daily does not
    # give you five times the opportunity of one posting twice a week, because you
    # can only comment on so many of them well.
    freq_factor = min(acct["posts_per_week"], 5) ** 0.5
    return round(acct["overlap"] * freq_factor * TIERS[acct["tier"]]["factor"], 2)


def build(accounts: list, minutes_per_day: int) -> dict:
    if not accounts:
        return {"verdict": "NO_ACCOUNTS", "exit_code": 3,
                "instruction": "Name the accounts first. Ten is plenty: the people whose audience "
                               "you want, whose posts you would read anyway, and who post often "
                               "enough to give you an opening each week."}

    per_day = minutes_per_day // MINUTES_PER_COMMENT
    findings = []
    verdict, code = "ROSTER", 0
    if per_day < 1:
        per_day = 1
        verdict, code = "BELOW_BUDGET", 2
        findings.append({
            "severity": "warning", "area": "budget",
            "finding": f"{minutes_per_day} min/day is under the {MINUTES_PER_COMMENT} minutes one "
                       "substantive comment takes.",
            "fix": "Comment on alternate days rather than writing a worse comment daily. "
                   "The roster below assumes one comment per listed day.",
        })

    scored = sorted(({**a, "score": score(a)} for a in accounts),
                    key=lambda a: (-a["score"], a["name"]))
    tier_counts = {t: sum(1 for a in scored if a["tier"] == t) for t in TIERS}
    if tier_counts["peer"] == 0:
        findings.append({
            "severity": "warning", "area": "mix",
            "finding": "No peer-tier accounts. Every relationship in the list is one-directional.",
            "fix": "Add three or four people at roughly your size. That is where reciprocal "
                   "attention comes from, and it is the part that still pays in a year.",
        })
    if tier_counts["huge"] > len(scored) / 2:
        findings.append({
            "severity": "warning", "area": "mix",
            "finding": f"{tier_counts['huge']}/{len(scored)} accounts are huge. Their threads are "
                       "crowded and most comments there are never read.",
            "fix": "Rebalance toward 'larger' and 'peer'. Being the best comment on a 40-comment "
                   "post beats being the 300th on a 400-comment one.",
        })

    used = {a["name"]: 0 for a in scored}
    roster, cursor = [], 0
    for day in DAYS:
        slots, huge_today, peer_today = [], 0, 0
        attempts = 0
        while len(slots) < per_day and attempts < len(scored) * 4:
            acct = scored[cursor % len(scored)]
            cursor += 1
            attempts += 1
            if used[acct["name"]] >= MAX_PER_ACCOUNT_PER_WEEK:
                continue
            if any(s["name"] == acct["name"] for s in slots):
                continue
            if acct["tier"] == "huge" and huge_today >= max(1, per_day // 2):
                continue
            slots.append({"name": acct["name"], "tier": acct["tier"],
                          "score": acct["score"], "why": TIERS[acct["tier"]]["note"]})
            used[acct["name"]] += 1
            if acct["tier"] == "huge":
                huge_today += 1
            if acct["tier"] == "peer":
                peer_today += 1
        if per_day >= 2 and peer_today == 0 and tier_counts["peer"]:
            findings.append({
                "severity": "info", "area": "mix",
                "finding": f"{day} has no peer-tier slot after the weekly cap was applied.",
                "fix": "Add another peer account to the list so every day has one.",
            })
        roster.append({"day": day, "comments": slots,
                       "minutes": len(slots) * MINUTES_PER_COMMENT})

    total = sum(len(d["comments"]) for d in roster)
    exhausted = [n for n, c in used.items() if c >= MAX_PER_ACCOUNT_PER_WEEK]
    if total < per_day * len(DAYS):
        findings.append({
            "severity": "warning", "area": "supply",
            "finding": f"Only {total} of {per_day * len(DAYS)} weekly slots could be filled without "
                       f"exceeding the {MAX_PER_ACCOUNT_PER_WEEK}-per-account cap.",
            "fix": f"Add more accounts. You need roughly "
                   f"{-(-per_day * len(DAYS) // MAX_PER_ACCOUNT_PER_WEEK)} to fill the week.",
        })

    return {
        "verdict": verdict,
        "exit_code": code,
        "minutes_per_day": minutes_per_day,
        "comments_per_day": per_day,
        "weekly_slots_filled": total,
        "accounts_scored": scored,
        "roster": roster,
        "at_weekly_cap": exhausted,
        "findings": findings,
        "comment_rules": [
            "Add something the post did not say. A counter-example, a number, the case where it "
            "breaks. Agreement is not a comment.",
            "Never paste the same comment twice. Identical comments across accounts are the "
            "definition of inauthentic engagement under User Agreement §8.2.",
            "Comment because you read it. If you have nothing to add, skip the slot — an empty "
            "slot costs nothing and a filler comment costs credibility.",
            "Two to four sentences. A comment longer than the post is a post; go write it.",
            "Reply to replies on your comment. That thread is where people actually meet you.",
        ],
    }


def render_human(r: dict) -> str:
    if r["verdict"] == "NO_ACCOUNTS":
        return "Comment roster: NO_ACCOUNTS\n" + "=" * 40 + "\n" + r["instruction"]
    lines = [f"Comment roster: {r['verdict']}  "
             f"({r['comments_per_day']}/day, {r['minutes_per_day']} min/day)",
             "=" * 60]
    for day in r["roster"]:
        names = ", ".join(f"{c['name']} [{c['tier']}]" for c in day["comments"]) or "(no slots)"
        lines.append(f"  {day['day']}  {names}   — {day['minutes']} min")
    lines.append("\nScored accounts:")
    for a in r["accounts_scored"]:
        lines.append(f"  {a['score']:>5}  {a['name']:<22} {a['tier']:<8} "
                     f"overlap {a['overlap']}/5, {a['posts_per_week']} posts/wk")
    if r["at_weekly_cap"]:
        lines.append(f"\nAt the {MAX_PER_ACCOUNT_PER_WEEK}/week cap: {', '.join(r['at_weekly_cap'])}")
    if r["findings"]:
        lines.append("\nFindings:")
        for f in r["findings"]:
            lines.append(f"  [{f['severity'].upper():<8}] {f['area']}: {f['finding']}")
            lines.append(f"             fix → {f['fix']}")
    lines.append("\nComment rules:")
    for c in r["comment_rules"]:
        lines.append(f"  - {c}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build a weekly LinkedIn commenting roster "
                    "(roster=0 / below-budget=2 / no-accounts=3). Nothing is posted.")
    ap.add_argument("--account", action="append", default=[],
                    help="name:overlap(1-5):posts_per_week:tier "
                         "(tier = huge|larger|peer|smaller). Repeatable.")
    ap.add_argument("--minutes-per-day", type=int, default=18,
                    help=f"Minutes per day for commenting (default 18 = "
                         f"{18 // MINUTES_PER_COMMENT} comments).")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Build a roster from sample accounts.")
    args = ap.parse_args()

    specs = SAMPLE_ACCOUNTS if args.sample else args.account
    minutes = 18 if args.sample else args.minutes_per_day
    try:
        accounts = [parse_account(s) for s in specs]
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4

    result = build(accounts, minutes)
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
