#!/usr/bin/env python3
"""brief_gate.py — refuse to start a film on a brief that cannot produce one.

A short film fails before the first frame when nobody decided who it is for,
where it runs, how long it is, or whether money may be spent on generated
footage. This gate reads a brief (JSON), fills what can be derived (aspect
from platform, the voice-over word budget from the length), and either passes
it on, asks the questions that are still open, or refuses.

Lanes it assigns:
  motion-only       no generated footage; the animatic is the film (free)
  previz-to-final   the animatic is approved first, then marked shots are
                    upgraded through a generation MCP the user connected,
                    each batch quoted and confirmed before any credit is spent

Exit codes:
  0  brief is complete; normalized brief printed (or written with --out)
  2  bad input (unreadable JSON)
  3  questions still open; each comes with a recommended answer
  4  refused: over the short-form scope, or AI likeness of real people
     without recorded consent

Examples:
  brief_gate.py --sample
  brief_gate.py --brief film/brief.json --out film/brief.json
  brief_gate.py --brief film/brief.json --output json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PLATFORM_ASPECT = {
    "youtube": "16:9", "youtube-shorts": "9:16", "tiktok": "9:16", "instagram-reels": "9:16",
    "instagram-feed": "4:5", "linkedin": "1:1", "x": "16:9", "website": "16:9",
    "presentation": "16:9", "other": "16:9",
}
ASPECTS = {"16:9", "9:16", "1:1", "4:5"}
MAX_SECONDS = 180
VO_WPS = 2.5

SAMPLE_BRIEF = {
    "title": "Release 2.0 teaser",
    "goal": "Get existing users to try the v2 release pipeline this week.",
    "audience": "Engineering leads already on v1",
    "platform": "linkedin",
    "duration_s": 20,
    "tone": "confident, dry, no hype",
    "cta": "example.dev/v2",
    "vo": "recorded",
    "brand": {"bg": "#0b0d12", "fg": "#f5f7fa", "accent": "#5b8cff", "font_heading": "Inter", "font_body": "Inter"},
    "upgrade_allowed": True,
    "budget_credits": 60,
    "real_people": False,
}

QUESTIONS = {
    "goal": ("What should a viewer do or believe after watching, in one sentence?",
             "Name one action, e.g. 'Book a demo after seeing the 3-step setup.'"),
    "audience": ("Who is this for, specifically?",
                 "Name a role and what they already know, e.g. 'Ops managers already on v1.'"),
    "platform": ("Where will it run first?",
                 "Pick the main platform; other aspect ratios re-render from the same scene."),
    "duration_s": ("How long, in seconds?",
                   "15-30 s for social, 45-90 s for an explainer; shorter is easier to keep tight."),
    "upgrade_allowed": ("May any shot use generated footage (it costs the user's credits)?",
                        "Start with false: approve the free animatic first, then mark shots to upgrade."),
}


def gate(brief: dict) -> tuple[int, dict]:
    b = json.loads(json.dumps(brief))
    open_q, notes, refusals = [], [], []

    goal = (b.get("goal") or "").strip()
    if len(goal.split()) < 5:
        open_q.append("goal")
    if not (b.get("audience") or "").strip():
        open_q.append("audience")
    platform = (b.get("platform") or "").strip().lower()
    if platform and platform not in PLATFORM_ASPECT:
        notes.append(f"unknown platform '{platform}', treated as 'other'")
        platform = "other"
    if not platform:
        open_q.append("platform")
    b["platform"] = platform or None

    try:
        dur = float(b.get("duration_s") or 0)
    except (TypeError, ValueError):
        dur = 0
    if dur <= 0:
        open_q.append("duration_s")
    elif dur > MAX_SECONDS:
        refusals.append(f"{dur:g}s is beyond the short-form scope ({MAX_SECONDS}s); split it into chapters "
                        "of 60-90 s and brief each one")
    b["duration_s"] = dur or None

    if "upgrade_allowed" not in b:
        open_q.append("upgrade_allowed")
    upgrade = bool(b.get("upgrade_allowed"))

    aspect = b.get("aspect")
    derived = PLATFORM_ASPECT.get(platform or "other")
    if aspect and aspect not in ASPECTS:
        notes.append(f"aspect {aspect} unsupported; using {derived}")
        aspect = None
    if aspect and derived and aspect != derived and platform not in ("other", "website", "presentation"):
        notes.append(f"{platform} is usually {derived}; keeping {aspect} as asked")
    b["aspect"] = aspect or derived

    budget = b.get("budget_credits")
    if upgrade and not budget:
        notes.append("upgrade allowed but no budget_credits cap; generation stays blocked until a cap is set")
    if b.get("real_people") and upgrade and b.get("consent") is not True:
        refusals.append("the brief allows generated footage and features real people, but no recorded consent "
                        "(consent: true); get written consent or set upgrade_allowed: false")

    if dur > 0:
        b["vo_word_budget"] = int(dur * VO_WPS)
    b["lane"] = "previz-to-final" if upgrade else "motion-only"
    b["disclosure"] = ("label generated footage as AI-generated where it is published (EU AI Act Article 50 "
                       "transparency duties for deployers; check the text that applies to you)") if upgrade else None
    b.setdefault("brand", {})
    b.setdefault("vo", "none")

    if refusals:
        return 4, {"verdict": "REFUSED", "reasons": refusals, "notes": notes}
    if open_q:
        qs = [{"field": k, "question": QUESTIONS[k][0], "recommended": QUESTIONS[k][1]} for k in open_q]
        return 3, {"verdict": "ASK", "questions": qs, "notes": notes,
                   "rule": "ask one question at a time, recommended answer first"}
    return 0, {"verdict": "READY", "brief": b, "notes": notes}


def main() -> int:
    ap = argparse.ArgumentParser(description="Gate a video brief: derive aspect and VO budget, ask open questions, refuse unsafe or out-of-scope briefs.")
    ap.add_argument("--brief", help="Path to brief JSON.")
    ap.add_argument("--sample", action="store_true", help="Gate the built-in sample brief.")
    ap.add_argument("--out", help="Write the normalized brief here when READY.")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    args = ap.parse_args()
    try:
        brief = SAMPLE_BRIEF if (args.sample or not args.brief) else json.loads(Path(args.brief).read_text(encoding="utf-8"))
        if not isinstance(brief, dict):
            raise ValueError("brief must be a JSON object")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    code, result = gate(brief)
    if code == 0 and args.out:
        Path(args.out).write_text(json.dumps(result["brief"], indent=2), encoding="utf-8")
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(result["verdict"])
        if code == 0:
            b = result["brief"]
            print(f"  lane={b['lane']} platform={b['platform']} aspect={b['aspect']} "
                  f"duration={b['duration_s']:g}s vo_budget={b['vo_word_budget']} words")
        for q in result.get("questions", []):
            print(f"  ? {q['question']}\n    recommended: {q['recommended']}")
        for r in result.get("reasons", []):
            print(f"  ✗ {r}")
        for n in result.get("notes", []):
            print(f"  · {n}")
    return code


if __name__ == "__main__":
    sys.exit(main())
