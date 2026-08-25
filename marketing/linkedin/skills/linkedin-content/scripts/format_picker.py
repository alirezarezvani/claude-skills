#!/usr/bin/env python3
"""format_picker.py — pick the LinkedIn post format the material actually supports.

Format is usually chosen by fashion ("carousels are working right now") rather than
by what the person has to say. This scores the nine native formats against three
inputs you actually control — the goal, the raw material in hand, and the minutes
available — and returns a ranked shortlist with the constraint each format carries.

It refuses two common mistakes outright:
  - a poll with no real decision behind it (a reach trick with a two-week half-life
    and nothing to say afterwards)
  - video when you have said you will not appear on camera and have no footage

Exit codes:
  0  a format is recommended
  2  the top two are within one point — ask which, do not guess
  3  no format fits the declared material; go get material first

Stdlib only. No network. Deterministic.
"""

import argparse
import json
import sys

GOALS = ["reach", "authority", "leads", "recruiting", "community", "career-change"]
MATERIALS = ["story", "data", "opinion", "tutorial", "announcement",
             "transcript", "visual", "question", "curation"]

# fit[format][goal] and fit[format][material]: 0-3
FORMATS = {
    "text-post": {
        "label": "Plain text post",
        "goal": {"reach": 3, "authority": 3, "leads": 2, "recruiting": 2,
                 "community": 3, "career-change": 3},
        "material": {"story": 3, "data": 2, "opinion": 3, "tutorial": 2,
                     "announcement": 2, "transcript": 1, "visual": 0,
                     "question": 3, "curation": 1},
        "minutes": 25,
        "constraint": "One idea. If it needs two, it is two posts.",
    },
    "document-carousel": {
        "label": "Document post (PDF carousel)",
        "goal": {"reach": 3, "authority": 3, "leads": 2, "recruiting": 1,
                 "community": 2, "career-change": 2},
        "material": {"story": 1, "data": 3, "opinion": 1, "tutorial": 3,
                     "announcement": 0, "transcript": 1, "visual": 3,
                     "question": 0, "curation": 3},
        "minutes": 90,
        "constraint": "Every slide must survive alone — most readers swipe two and leave. "
                      "Upload a real PDF with selectable text, not exported images.",
    },
    "native-video": {
        "label": "Native video",
        "goal": {"reach": 3, "authority": 2, "leads": 2, "recruiting": 3,
                 "community": 2, "career-change": 2},
        "material": {"story": 3, "data": 1, "opinion": 2, "tutorial": 3,
                     "announcement": 2, "transcript": 3, "visual": 3,
                     "question": 1, "curation": 0},
        "minutes": 120,
        "constraint": "Captions are mandatory — most viewing is sound-off, and captions are "
                      "also the accessibility floor. Say the point in the first five seconds.",
    },
    "image-post": {
        "label": "Single image + text",
        "goal": {"reach": 2, "authority": 2, "leads": 1, "recruiting": 2,
                 "community": 2, "career-change": 2},
        "material": {"story": 2, "data": 3, "opinion": 1, "tutorial": 1,
                     "announcement": 3, "transcript": 0, "visual": 3,
                     "question": 1, "curation": 1},
        "minutes": 30,
        "constraint": "Write alt text. A chart with no alt text excludes readers and says nothing "
                      "to anyone who cannot load it.",
    },
    "poll": {
        "label": "Poll",
        "goal": {"reach": 2, "authority": 1, "leads": 1, "recruiting": 1,
                 "community": 3, "career-change": 1},
        "material": {"story": 0, "data": 1, "opinion": 1, "tutorial": 0,
                     "announcement": 0, "transcript": 0, "visual": 0,
                     "question": 3, "curation": 0},
        "minutes": 10,
        "constraint": "Only if you will publish what the answers changed. A poll you do not follow "
                      "up on is a reach trick, and readers have learned to spot it.",
    },
    "article": {
        "label": "Long-form article",
        "goal": {"reach": 1, "authority": 3, "leads": 2, "recruiting": 1,
                 "community": 1, "career-change": 2},
        "material": {"story": 2, "data": 3, "opinion": 3, "tutorial": 3,
                     "announcement": 0, "transcript": 2, "visual": 1,
                     "question": 0, "curation": 3},
        "minutes": 180,
        "constraint": "Articles reach far fewer people than posts. Write one when the artifact "
                      "matters more than this week's impressions — it is a durable link.",
    },
    "newsletter-issue": {
        "label": "Newsletter issue",
        "goal": {"reach": 2, "authority": 3, "leads": 3, "recruiting": 1,
                 "community": 3, "career-change": 1},
        "material": {"story": 2, "data": 3, "opinion": 3, "tutorial": 3,
                     "announcement": 1, "transcript": 2, "visual": 1,
                     "question": 0, "curation": 3},
        "minutes": 150,
        "constraint": "Subscribers are notified every issue. That is a standing promise about "
                      "cadence and topic — do not start one you cannot hold for six months.",
    },
    "comment-as-content": {
        "label": "Substantive comment on someone else's post",
        "goal": {"reach": 3, "authority": 3, "leads": 2, "recruiting": 2,
                 "community": 3, "career-change": 3},
        "material": {"story": 2, "data": 3, "opinion": 3, "tutorial": 1,
                     "announcement": 0, "transcript": 0, "visual": 0,
                     "question": 2, "curation": 1},
        "minutes": 10,
        "constraint": "It has to add something the original missed. Agreement is not a comment. "
                      "This is the fastest route to visibility from a standing start.",
    },
    "repost-with-take": {
        "label": "Repost with your own take",
        "goal": {"reach": 1, "authority": 2, "leads": 1, "recruiting": 1,
                 "community": 2, "career-change": 1},
        "material": {"story": 0, "data": 2, "opinion": 3, "tutorial": 0,
                     "announcement": 1, "transcript": 0, "visual": 1,
                     "question": 1, "curation": 3},
        "minutes": 15,
        "constraint": "Your take must be longer than 'this'. A bare repost spends your credibility "
                      "on someone else's idea and returns nothing.",
    },
}


def pick(goal: str, materials: list, minutes: int, on_camera: bool,
         has_real_decision: bool) -> dict:
    if goal not in GOALS:
        raise ValueError(f"goal must be one of {GOALS}")
    bad = [m for m in materials if m not in MATERIALS]
    if bad:
        raise ValueError(f"unknown material(s): {bad}; choose from {MATERIALS}")

    ranked, excluded = [], []
    for key, spec in FORMATS.items():
        if key == "native-video" and not on_camera and "transcript" not in materials \
                and "visual" not in materials:
            excluded.append({"format": key, "reason":
                             "You said no camera and supplied no footage or transcript."})
            continue
        if key == "poll" and not has_real_decision:
            excluded.append({"format": key, "reason":
                             "No real decision behind it. A poll without a follow-up post is a "
                             "reach trick; declare --has-decision if you will publish what "
                             "the answers changed."})
            continue
        if spec["minutes"] > minutes:
            excluded.append({"format": key, "reason":
                             f"Needs about {spec['minutes']} min; you have {minutes}."})
            continue
        mat_scores = [spec["material"][m] for m in materials] or [0]
        score = spec["goal"][goal] * 2 + max(mat_scores) + (sum(mat_scores) / len(mat_scores))
        ranked.append({
            "format": key, "label": spec["label"], "score": round(score, 2),
            "goal_fit": spec["goal"][goal],
            "best_material_fit": max(mat_scores),
            "effort_minutes": spec["minutes"],
            "constraint": spec["constraint"],
        })

    ranked.sort(key=lambda r: (-r["score"], r["effort_minutes"]))
    if not ranked:
        return {"decision": "NO_FIT", "exit_code": 3, "ranked": [], "excluded": excluded,
                "instruction": "Nothing fits. Either the time budget is too small or the material "
                               "does not exist yet. Go get the material — the format is the easy part."}
    if len(ranked) > 1 and ranked[0]["score"] - ranked[1]["score"] < 1.0:
        return {"decision": "ASK", "exit_code": 2, "ranked": ranked[:3], "excluded": excluded,
                "instruction": f"'{ranked[0]['label']}' and '{ranked[1]['label']}' score within a "
                               "point. Ask which the person would actually enjoy making — the one "
                               "they will repeat beats the one that scores higher once."}
    return {"decision": "RECOMMEND", "exit_code": 0, "recommended": ranked[0],
            "runners_up": ranked[1:3], "ranked": ranked, "excluded": excluded}


def render_human(r: dict) -> str:
    lines = [f"Format decision: {r['decision']}", "=" * 52]
    if r["decision"] == "RECOMMEND":
        rec = r["recommended"]
        lines += [f"→ {rec['label']}  (score {rec['score']}, ~{rec['effort_minutes']} min)",
                  f"  constraint: {rec['constraint']}", ""]
        if r["runners_up"]:
            lines.append("Runners-up:")
            for u in r["runners_up"]:
                lines.append(f"  - {u['label']} ({u['score']}) — {u['constraint']}")
    else:
        lines.append(r["instruction"])
        for u in r.get("ranked", []):
            lines.append(f"  - {u['label']} ({u['score']}) — {u['constraint']}")
    if r.get("excluded"):
        lines.append("\nRuled out:")
        for e in r["excluded"]:
            lines.append(f"  - {e['format']}: {e['reason']}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Rank LinkedIn post formats against goal, material, and time "
                    "(recommend=0 / ask=2 / no-fit=3).")
    ap.add_argument("--goal", choices=GOALS, help="What this post is for.")
    ap.add_argument("--material", action="append", default=[], choices=MATERIALS,
                    help="What you actually have. Repeatable.")
    ap.add_argument("--minutes", type=int, default=45,
                    help="Minutes you will realistically spend (default 45).")
    ap.add_argument("--on-camera", action="store_true",
                    help="You are willing to appear on camera.")
    ap.add_argument("--has-decision", action="store_true",
                    help="A poll would settle a real decision you will report back on.")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Run a built-in example.")
    args = ap.parse_args()

    if args.sample:
        goal, materials, minutes = "authority", ["data", "tutorial"], 120
        on_camera, decision = False, False
    else:
        if not args.goal or not args.material:
            ap.error("--goal and at least one --material are required (or use --sample)")
        goal, materials, minutes = args.goal, args.material, args.minutes
        on_camera, decision = args.on_camera, args.has_decision

    try:
        result = pick(goal, materials, minutes, on_camera, decision)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 4
    result["inputs"] = {"goal": goal, "materials": materials, "minutes": minutes,
                        "on_camera": on_camera, "has_real_decision": decision}
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
