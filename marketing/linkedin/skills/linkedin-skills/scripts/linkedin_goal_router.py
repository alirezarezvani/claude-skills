#!/usr/bin/env python3
"""linkedin_goal_router.py — deterministic lane classifier for the linkedin domain.

Scores a LinkedIn goal against the five sub-skill lanes using the same two-signal
threshold discipline as the commercial / research-ops / product-team orchestrators.
Emits a routing decision an agent can branch on mechanically instead of guessing.

Exit codes:
  0  confident route emitted (route_to set)
  2  ambiguous — ask ONE clarifying question naming the top two lanes
  3  no signal — do not guess; ask the user to restate the goal with a deliverable

Stdlib only. Deterministic: same text in, same route out.
"""

import argparse
import json
import sys

SIGNALS = {
    "PROFILE": {
        "skill": "linkedin-profile",
        "path": "marketing/linkedin/skills/linkedin-profile",
        "keywords": [
            "profile", "headline", "about section", "about me", "summary section",
            "banner", "featured section", "experience section", "bio", "tagline",
            "profile photo", "skills section", "recommendations", "open to work",
            "creator mode", "custom url", "profile audit", "optimize my profile",
        ],
    },
    "STRATEGY": {
        "skill": "linkedin-strategy",
        "path": "marketing/linkedin/skills/linkedin-strategy",
        "keywords": [
            "strategy", "content pillars", "pillar", "positioning", "cadence",
            "posting schedule", "how often should i post", "calendar", "editorial calendar",
            "newsletter", "thought leadership", "career change", "career transition",
            "personal brand", "audience", "niche", "90 day", "quarter", "roadmap",
            "goals", "objective", "grow my following", "grow an audience",
        ],
    },
    "CONTENT": {
        "skill": "linkedin-content",
        "path": "marketing/linkedin/skills/linkedin-content",
        "keywords": [
            "write a post", "draft a post", "post idea", "post ideas", "hook",
            "carousel", "document post", "pdf post", "story post", "how-to post",
            "opinion post", "listicle", "caption", "video script", "poll",
            "article", "repurpose", "turn this into", "rewrite this post",
            "edit my post", "review my post", "first line", "content", "copy",
        ],
    },
    "ENGAGEMENT": {
        "skill": "linkedin-engagement",
        "path": "marketing/linkedin/skills/linkedin-engagement",
        "keywords": [
            "comment", "commenting", "reply", "replies", "dm", "message",
            "connection request", "connection note", "invite", "inmail", "outreach",
            "networking", "cold message", "follow up", "who should i engage",
            "engagement strategy", "groups", "community", "reach out", "warm intro",
        ],
    },
    "ANALYTICS": {
        "skill": "linkedin-analytics",
        "path": "marketing/linkedin/skills/linkedin-analytics",
        "keywords": [
            "analytics", "analyze my posts", "which posts", "performance",
            "impressions", "engagement rate", "reach dropped", "what's working",
            "what is working", "export", "benchmark", "pattern", "why did this post",
            "top posts", "experiment", "test", "measure", "metrics", "dashboard",
            "followers gained", "profile views",
        ],
    },
}

# Cross-lane dependencies used when the router says ASK or when a lane is chosen:
# these are stated as prerequisites, not silently chained.
PREREQS = {
    "CONTENT": ("STRATEGY", "Posts without pillars are noise. If no positioning brief exists, "
                            "offer linkedin-strategy first — but never chain silently."),
    "ANALYTICS": ("CONTENT", "Pattern mining needs a body of posts. Under ~20 posts, the honest "
                             "answer is 'not enough data yet' — say so rather than fitting noise."),
    "ENGAGEMENT": ("PROFILE", "Comments and DMs drive profile visits. A weak headline wastes "
                              "every visit engagement earns."),
}

SAMPLE_GOAL = ("I'm moving from backend engineering into developer advocacy and want to build "
               "a real audience over the next two quarters — what should I be posting about, "
               "and how often?")


def score(text: str) -> dict:
    low = text.lower()
    scores, hits = {}, {}
    for lane, spec in SIGNALS.items():
        matched = [kw for kw in spec["keywords"] if kw in low]
        scores[lane] = len(matched)
        hits[lane] = matched
    return {"scores": scores, "hits": hits}


def decide(scores: dict) -> dict:
    ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
    (top_lane, top), (second_lane, second) = ranked[0], ranked[1]
    if top == 0:
        return {"decision": "NO_SIGNAL", "exit": 3}
    if top >= 2 and (second == 0 or top >= 2 * second):
        return {"decision": "ROUTE", "lane": top_lane, "exit": 0}
    candidates = [top_lane] + ([second_lane] if second > 0 else [])
    return {"decision": "ASK", "candidates": candidates, "exit": 2}


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Deterministic lane router for LinkedIn goals "
                    "(route=0 / ask=2 / no-signal=3).")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--text", help="Goal or inquiry text to classify.")
    src.add_argument("--input", help="Read goal text from a file ('-' for stdin).")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true",
                    help="Classify a built-in sample goal and exit.")
    args = ap.parse_args()

    if args.sample:
        text = SAMPLE_GOAL
    elif args.text:
        text = args.text
    elif args.input:
        text = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    else:
        ap.error("one of --text, --input, or --sample is required")

    result = score(text)
    verdict = decide(result["scores"])
    out = {
        "goal": text.strip()[:300],
        "scores": {k: v for k, v in result["scores"].items() if v},
        "decision": verdict["decision"],
        "policy_gate": ("Run linkedin_policy_gate.py on the same text before drafting anything. "
                        "A REFUSE there outranks any route here."),
    }

    if verdict["decision"] == "ROUTE":
        lane = verdict["lane"]
        out["route_to"] = SIGNALS[lane]["skill"]
        out["skill_path"] = SIGNALS[lane]["path"]
        out["matched_signals"] = result["hits"][lane]
        if lane in PREREQS:
            prereq_lane, why = PREREQS[lane]
            out["prerequisite"] = {
                "lane": SIGNALS[prereq_lane]["skill"],
                "why": why,
                "rule": "Offer it as a question. Never chain silently.",
            }
    elif verdict["decision"] == "ASK":
        out["candidates"] = [
            {"lane": lane, "skill": SIGNALS[lane]["skill"], "score": result["scores"][lane]}
            for lane in verdict["candidates"]
        ]
        out["instruction"] = ("Ask ONE clarifying question naming both candidate lanes, with a "
                              "recommended answer and the reason. Never guess silently.")
    else:
        out["instruction"] = ("No lane signal. Ask the user what they want to walk away with — "
                              "a rewritten profile, a posting plan, a drafted post, an outreach "
                              "message, or a read on their numbers. Do not route on fuzz.")

    if args.output == "json":
        print(json.dumps(out, indent=2))
    else:
        print(f"Decision: {out['decision']}")
        if "route_to" in out:
            print(f"Route to: {out['route_to']}  ({out['skill_path']})")
            print(f"Signals : {', '.join(out['matched_signals'])}")
            if "prerequisite" in out:
                print(f"Prereq  : {out['prerequisite']['lane']} — {out['prerequisite']['why']}")
        elif "candidates" in out:
            print("Ambiguous: " + " vs ".join(c["skill"] for c in out["candidates"]))
            print(out["instruction"])
        else:
            print(out["instruction"])
        print(f"\nPolicy  : {out['policy_gate']}")
    return verdict["exit"]


if __name__ == "__main__":
    sys.exit(main())
