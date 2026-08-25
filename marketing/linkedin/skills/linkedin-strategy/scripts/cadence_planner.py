#!/usr/bin/env python3
"""cadence_planner.py — size a LinkedIn week against the hours that actually exist.

Content plans do not fail on ideas. They fail in week five, when the plan assumed
six hours and the person has ninety minutes. This tool prices every activity in
minutes, allocates the real budget by stage, and refuses a target it cannot pay
for — naming the overage rather than quietly shrinking the plan.

It also emits a minimum viable week: the subset to keep when the week collapses.
Consistency is the compounding variable, so the fallback matters more than the
ideal plan.

Allocation shifts with stage on purpose. From a standing start, most of the budget
belongs in other people's comment sections — a post published to nobody reaches
nobody, and a substantive comment on a well-read post is the cheapest distribution
available.

Exit codes:
  0  plan fits the budget
  2  budget is below the floor — a comment-only week is returned instead
  3  the requested target does not fit; the overage is named

Stdlib only. No network. Deterministic.
"""

import argparse
import json
import sys

# Minutes per unit of work, drafting + revision + posting included.
COST = {
    "text-post": 25,
    "document-carousel": 90,
    "native-video": 120,
    "image-post": 30,
    "article": 180,
    "newsletter-issue": 150,
    "comment": 6,
    "outreach-message": 5,
    "own-post-replies": 20,     # per published post, in the first hours after posting
}

FLOOR_MINUTES = 90

STAGES = {
    "starting": {
        "label": "Under ~1,000 followers, or restarting after a long gap",
        "engagement_share": 0.60,
        "why": "Your own posts have almost no distribution yet. Comments on posts that already "
               "have an audience are the only lever that works from zero.",
        "comment_floor_per_day": 5,
    },
    "rebuilding": {
        "label": "An audience exists but has gone quiet",
        "engagement_share": 0.45,
        "why": "Reach recovers with consistency, not with a big swing. Split the budget while "
               "the cadence re-establishes.",
        "comment_floor_per_day": 3,
    },
    "established": {
        "label": "Posts reliably reach people who are not your connections",
        "engagement_share": 0.30,
        "why": "Distribution is working; the constraint is now the quality and frequency of "
               "what you publish.",
        "comment_floor_per_day": 2,
    },
}


def plan(minutes: int, stage: str, target_posts: int, formats: list,
         outreach_per_week: int) -> dict:
    spec = STAGES[stage]
    findings = []

    if minutes < FLOOR_MINUTES:
        return {
            "verdict": "BELOW_FLOOR",
            "exit_code": 2,
            "minutes_available": minutes,
            "floor": FLOOR_MINUTES,
            "recommendation": {
                "posts_per_week": 0,
                "comments_per_week": max(1, minutes // COST["comment"]),
                "note": "Under 90 minutes a week, publishing on a schedule will break before it "
                        "compounds. Spend the whole budget on substantive comments in other "
                        "people's threads: it builds the same recognition, costs a fraction of "
                        "the time, and stops cleanly when a week disappears.",
            },
            "when_to_revisit": "Come back to publishing when you can protect 2 hours a week for "
                               "eight consecutive weeks.",
            "rule": "A cadence you abandon in week five is worse than a cadence you never started, "
                    "because the abandoned one is visible on your profile.",
        }

    engagement_budget = round(minutes * spec["engagement_share"])
    creation_budget = minutes - engagement_budget

    outreach_cost = outreach_per_week * COST["outreach-message"]
    if outreach_cost > engagement_budget * 0.5:
        findings.append({
            "severity": "warning", "area": "outreach",
            "finding": f"{outreach_per_week} outreach messages cost {outreach_cost} min — over "
                       f"half the {engagement_budget}-min engagement budget.",
            "fix": "Outreach converts far better after someone has seen you in their feed or "
                   "comments. Shift the balance toward comments until then.",
        })
    comment_budget = max(0, engagement_budget - outreach_cost)
    comments = comment_budget // COST["comment"]
    comments_per_day = round(comments / 7, 1)

    chosen = [f for f in formats if f in COST] or ["text-post"]
    avg_create = sum(COST[f] for f in chosen) / len(chosen)
    cost_per_post = avg_create + COST["own-post-replies"]
    affordable = int(creation_budget // cost_per_post)

    verdict, code = "FITS", 0
    if target_posts:
        if target_posts > affordable:
            need = round(target_posts * cost_per_post + engagement_budget)
            findings.append({
                "severity": "blocking", "area": "capacity",
                "finding": f"{target_posts} posts/week in {', '.join(chosen)} costs about "
                           f"{round(target_posts * cost_per_post)} min of creation "
                           f"({round(cost_per_post)} min each including replying to your own "
                           f"comments). With engagement, the week needs ~{need} min; you have "
                           f"{minutes}.",
                "fix": f"Either drop to {affordable} post(s)/week, move to a cheaper format "
                       f"(text-post at {COST['text-post']} min), or find {need - minutes} more "
                       "minutes. Do not solve it by skipping the reply window — replying to "
                       "early comments is part of the post, not an extra.",
            })
            verdict, code = "OVER_BUDGET", 3
        else:
            affordable = target_posts

    if affordable == 0 and verdict == "FITS":
        findings.append({
            "severity": "warning", "area": "capacity",
            "finding": f"The chosen formats ({', '.join(chosen)}) cost more than the "
                       f"{creation_budget}-min creation budget allows for even one post.",
            "fix": "Add text-post to the format mix, or accept a fortnightly cadence for the "
                   "expensive format.",
        })

    if comments_per_day < spec["comment_floor_per_day"]:
        findings.append({
            "severity": "warning", "area": "engagement",
            "finding": f"{comments_per_day} comments/day is below the {spec['comment_floor_per_day']} "
                       f"floor for the '{stage}' stage. {spec['why']}",
            "fix": "Shift one post's worth of time into comments. At this stage comments buy "
                   "more reach per minute than publishing does.",
        })

    minimum_week = ["1 substantive comment per weekday (30 min total)"]
    if affordable >= 1:
        minimum_week.insert(0, "1 text post, published on the same day each week")
    minimum_week.append("Reply to every comment on your own post within 24 hours")

    return {
        "verdict": verdict,
        "exit_code": code,
        "stage": stage,
        "stage_label": spec["label"],
        "minutes_available": minutes,
        "budget_split": {"creation": creation_budget, "engagement": engagement_budget,
                         "engagement_share": spec["engagement_share"], "why": spec["why"]},
        "weekly_plan": {
            "posts": affordable,
            "formats": chosen,
            "minutes_per_post_including_replies": round(cost_per_post),
            "comments": int(comments),
            "comments_per_day": comments_per_day,
            "outreach_messages": outreach_per_week,
        },
        "minimum_viable_week": minimum_week,
        "findings": findings,
        "rules": [
            "Same day, same time, every week. The schedule is the product; the topic varies.",
            "Reply time is post time. Block the 60-90 minutes after publishing — early comments "
            "are where a post either travels or dies.",
            "A skipped week is fine. A skipped month resets you to the starting stage.",
        ],
    }


def render_human(r: dict) -> str:
    if r["verdict"] == "BELOW_FLOOR":
        rec = r["recommendation"]
        return "\n".join([
            f"Cadence: BELOW_FLOOR ({r['minutes_available']} min/week, floor {r['floor']})",
            "=" * 56, rec["note"], "",
            f"This week: {rec['comments_per_week']} substantive comments, 0 posts.",
            f"Revisit  : {r['when_to_revisit']}", "", r["rule"]])
    w = r["weekly_plan"]
    b = r["budget_split"]
    lines = [f"Cadence: {r['verdict']}  ({r['minutes_available']} min/week, stage: {r['stage']})",
             "=" * 56,
             f"{r['stage_label']}",
             f"Split: {b['creation']} min creating / {b['engagement']} min engaging "
             f"({int(b['engagement_share'] * 100)}% engagement)",
             f"  why: {b['why']}", "",
             "Weekly plan:",
             f"  posts            : {w['posts']}  ({', '.join(w['formats'])}, "
             f"~{w['minutes_per_post_including_replies']} min each incl. replies)",
             f"  comments         : {w['comments']}  (~{w['comments_per_day']}/day)",
             f"  outreach msgs    : {w['outreach_messages']}"]
    if r["findings"]:
        lines.append("\nFindings:")
        for f in r["findings"]:
            lines.append(f"  [{f['severity'].upper():<8}] {f['area']}: {f['finding']}")
            lines.append(f"             fix → {f['fix']}")
    lines.append("\nMinimum viable week (what survives a bad week):")
    for m in r["minimum_viable_week"]:
        lines.append(f"  - {m}")
    lines.append("\nRules:")
    for rule in r["rules"]:
        lines.append(f"  - {rule}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Size a sustainable LinkedIn week (fits=0 / below-floor=2 / over-budget=3).")
    ap.add_argument("--minutes", type=int, help="Minutes per week you will actually protect.")
    ap.add_argument("--stage", choices=sorted(STAGES), default="starting")
    ap.add_argument("--target-posts", type=int, default=0,
                    help="Posts per week you want. Omit to be told what fits.")
    ap.add_argument("--format", action="append", default=[], choices=sorted(
        k for k in COST if k not in ("comment", "outreach-message", "own-post-replies")),
        help="Format(s) you intend to publish. Repeatable. Default text-post.")
    ap.add_argument("--outreach", type=int, default=0,
                    help="Manual outreach messages per week (default 0).")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Run a built-in example week.")
    args = ap.parse_args()

    if args.sample:
        minutes, stage, target, formats, outreach = 240, "starting", 3, ["text-post"], 10
    else:
        if args.minutes is None:
            ap.error("--minutes is required (or use --sample)")
        minutes, stage = args.minutes, args.stage
        target, formats, outreach = args.target_posts, args.format, args.outreach

    result = plan(minutes, stage, target, formats, outreach)
    result["inputs"] = {"minutes": minutes, "stage": stage, "target_posts": target,
                        "formats": formats or ["text-post"], "outreach": outreach}
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
