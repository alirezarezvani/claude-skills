#!/usr/bin/env python3
"""beat_board.py — time a beat list against the brief and emit a scene.v1 animatic.

You (or the model) write the beats: what is said, what is on screen, what the
viewer sees, and whether the shot stays motion graphics or is a candidate for
generated footage. This tool does the arithmetic people skip:

  * each beat gets the time its voice-over needs (150 wpm) and the time its
    on-screen text needs to be read (180 wpm plus 0.5 s), never under 1.5 s
  * if the beats need more time than the brief allows, it refuses and says how
    many words to cut, instead of silently cramming them
  * if they need less, the slack is spread across beats so the cut breathes
  * the result is a scene.v1 file that timeline_compiler.py renders as-is

Beat fields: vo, on_screen, visual, kind ("motion" | "upgrade"), and optional
stat {"to": 68, "prefix": "", "suffix": " min"} or chart {"kind": "bar",
"data": [[label, value], ...]} or csv (path to a two-column file).

Exit codes: 0 scene written, 2 bad input, 4 beats do not fit the brief.

Examples:
  beat_board.py --sample
  beat_board.py --brief film/brief.json --beats film/beats.json --out film/scene.json
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

VO_WPS = 2.5
READ_WPS = 3.0
READ_LEAD = 0.5
MIN_SHOT = 1.5
STRETCH_WARN = 1.6
CAMERA_CYCLE = [("push-in", 0.06), ("drift", 0.04), ("static", 0.0), ("pull-out", 0.05)]

SAMPLE_BRIEF = {
    "title": "Release 2.0 teaser", "platform": "linkedin", "aspect": "1:1", "duration_s": 16,
    "lane": "previz-to-final",
    "brand": {"bg": "#0b0d12", "fg": "#f5f7fa", "accent": "#5b8cff", "font_heading": "Inter", "font_body": "Inter"},
}
SAMPLE_BEATS = [
    {"vo": "Your release notes are a wall of text.", "on_screen": "Release notes nobody reads",
     "visual": "dense changelog scrolling", "kind": "motion"},
    {"vo": "Version two turns them into a two-minute brief.", "on_screen": "v2: the release brief",
     "visual": "engineer at a desk at night, laptop glow, calm", "kind": "upgrade"},
    {"vo": "Teams save over an hour per release.", "stat": {"to": 68, "suffix": " min"},
     "on_screen": "saved per release", "visual": "counter", "kind": "motion"},
    {"vo": "Try it today.", "on_screen": "example.dev/v2", "visual": "end card", "kind": "motion"},
]


def words(text: str) -> float:
    """Word count for timing; a long token (URL, product code) counts as one word per 6 characters."""
    return sum(max(1.0, len(w) / 6) if len(w) > 12 else 1.0 for w in re.split(r"\s+", text or "") if w)


END_CARD = 3.0


def need(beat: dict, last: bool = False) -> float:
    vo = words(beat.get("vo", "")) / VO_WPS + 0.3 if beat.get("vo") else 0.0
    text = " ".join(x for x in (beat.get("on_screen"),) if x)
    read = READ_LEAD + 0.3 + words(text) / READ_WPS if text else 0.0
    extra = 1.6 if beat.get("stat") or beat.get("chart") or beat.get("csv") else 0.0
    return max(END_CARD if last else MIN_SHOT, vo, read + extra)


def layers_for(beat: dict, i: int, n: int) -> list:
    out = []
    kind = beat.get("kind", "motion")
    if kind == "upgrade":
        out.append({"type": "plate", "label": beat.get("visual", "")})
    if beat.get("stat"):
        st = beat["stat"]
        out.append({"type": "counter", "from": st.get("from", 0), "to": st["to"], "prefix": st.get("prefix", ""),
                    "suffix": st.get("suffix", ""), "decimals": st.get("decimals", 0),
                    "x": 0.5, "y": 0.42, "style": "title", "in": 0.2, "dur": 1.4})
        if beat.get("on_screen"):
            out.append({"type": "text", "text": beat["on_screen"], "style": "subtitle", "x": 0.5, "y": 0.6,
                        "in": 0.7, "anim": "rise"})
        return out
    if beat.get("chart") or beat.get("csv"):
        ch = dict(beat.get("chart") or {})
        if beat.get("csv"):
            ch["csv"] = beat["csv"]
        out.append({"type": "chart", "kind": ch.get("kind", "bar"), "x": 0.5, "y": 0.56, "w": 0.7, "h": 0.5,
                    **({"data": ch["data"]} if ch.get("data") else {}), **({"csv": ch["csv"]} if ch.get("csv") else {}),
                    "title": beat.get("on_screen", ""), "in": 0.3, "anim": "grow"})
        return out
    if beat.get("on_screen"):
        last = i == n - 1
        style = "title" if i == 0 or last else "subtitle"
        out.append({"type": "text", "text": beat["on_screen"], "style": style, "x": 0.5,
                    "y": 0.5 if kind != "upgrade" else 0.78, "in": 0.3, "anim": "words" if i == 0 else "rise",
                    **({"box": True} if kind == "upgrade" else {})})
    return out


def build(brief: dict, beats: list, fps: int) -> tuple[int, dict]:
    if not beats:
        return 2, {"error": "no beats"}
    target = float(brief.get("duration_s") or 0)
    if target <= 0:
        return 2, {"error": "brief.duration_s missing; run brief_gate.py first"}
    needs = [need(b, i == len(beats) - 1) for i, b in enumerate(beats)]
    total_need = sum(needs)
    if total_need > target + 0.25:
        over = total_need - target
        cut = math.ceil(over * VO_WPS)
        return 4, {"verdict": "DOES-NOT-FIT", "needs_s": round(total_need, 2), "target_s": target,
                   "over_s": round(over, 2),
                   "fix": f"cut about {cut} voice-over words or drop a beat, or raise duration_s to {math.ceil(total_need)}",
                   "per_beat": [round(x, 2) for x in needs]}
    factor = target / total_need
    raw = [x * factor for x in needs]
    step = 1.0 / fps
    durs = [max(step, round(x / step) * step) for x in raw]
    durs[-1] = round(target - sum(durs[:-1]), 6)
    allow_upgrade = brief.get("lane") == "previz-to-final"
    shots = []
    for i, (b, d) in enumerate(zip(beats, durs)):
        move, amt = CAMERA_CYCLE[i % len(CAMERA_CYCLE)]
        is_up = b.get("kind") == "upgrade" and allow_upgrade
        bb = dict(b, kind="upgrade" if is_up else "motion")
        shot = {"id": f"s{i + 1}", "duration": round(d, 4),
                "transition": "cut" if i == 0 else ("dip" if i == len(beats) - 1 else ("fade" if is_up else "cut")),
                "camera": {"move": move, "amount": amt, "ease": "ease-in-out"},
                "vo": b.get("vo", ""), "beat": b.get("visual", ""),
                "layers": layers_for(bb, i, len(beats))}
        if is_up:
            shot["upgrade"] = True
            shot["upgrade_prompt"] = b.get("visual", "")
        shots.append(shot)
    brand = brief.get("brand") or {}
    scene = {
        "schema": "scene.v1",
        "meta": {"title": brief.get("title", "Untitled"), "aspect": brief.get("aspect", "16:9"), "fps": fps,
                 "target_duration": target, "mode": "greybox", "captions": False},
        "theme": {k: v for k, v in brand.items() if k in ("bg", "fg", "accent", "muted", "font_heading", "font_body")},
        "shots": shots,
    }
    warn = []
    if factor > STRETCH_WARN:
        warn.append(f"beats need only {total_need:.1f}s of {target:g}s; each is stretched {factor:.2f}x. "
                    "Add a beat or shorten the brief so the cut does not drag.")
    dropped = [f"s{i + 1}" for i, b in enumerate(beats) if b.get("kind") == "upgrade" and not allow_upgrade]
    if dropped:
        warn.append(f"lane is motion-only, so upgrade beats {dropped} stay motion graphics")
    return 0, {"verdict": "FITS", "needs_s": round(total_need, 2), "target_s": target, "stretch": round(factor, 3),
               "warnings": warn, "scene": scene}


def main() -> int:
    ap = argparse.ArgumentParser(description="Time beats against a brief and emit a scene.v1 animatic (refuses beats that do not fit).")
    ap.add_argument("--brief", help="Normalized brief JSON (from brief_gate.py).")
    ap.add_argument("--beats", help="Beats JSON: a list, or {\"beats\": [...]}.")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--out", help="Write scene.v1 here.")
    ap.add_argument("--sample", action="store_true", help="Use the built-in sample brief and beats.")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    args = ap.parse_args()
    try:
        if args.sample or not (args.brief and args.beats):
            brief, beats = SAMPLE_BRIEF, SAMPLE_BEATS
        else:
            brief = json.loads(Path(args.brief).read_text(encoding="utf-8"))
            beats = json.loads(Path(args.beats).read_text(encoding="utf-8"))
            if isinstance(beats, dict):
                beats = beats.get("beats", [])
            if isinstance(brief, dict) and "brief" in brief and "verdict" in brief:
                brief = brief["brief"]
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    code, res = build(brief, beats, args.fps)
    if code == 2:
        print(f"error: {res['error']}", file=sys.stderr)
        return 2
    if code == 0 and args.out:
        Path(args.out).write_text(json.dumps(res["scene"], indent=2), encoding="utf-8")
    if args.output == "json":
        print(json.dumps(res, indent=2))
    elif code == 4:
        print(f"DOES-NOT-FIT: beats need {res['needs_s']}s, brief allows {res['target_s']:g}s (over {res['over_s']}s)")
        print(f"  fix: {res['fix']}")
        print(f"  per beat: {res['per_beat']}")
    else:
        sc = res["scene"]
        print(f"FITS: {len(sc['shots'])} shots, needs {res['needs_s']}s of {res['target_s']:g}s (stretch {res['stretch']}x)")
        for s in sc["shots"]:
            tag = "  [upgrade]" if s.get("upgrade") else ""
            print(f"  {s['id']:>4} {s['duration']:5.2f}s {s['transition']:<4} {s['camera']['move']:<9} {s['vo'][:50]}{tag}")
        for w in res["warnings"]:
            print(f"  · {w}")
        if args.out:
            print(f"scene: {args.out}")
    return code


if __name__ == "__main__":
    sys.exit(main())
