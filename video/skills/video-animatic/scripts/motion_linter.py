#!/usr/bin/env python3
"""motion_linter.py — check a scene.v1 file before anything is rendered or spent.

The checks are the ones that make a short film fail in review even when every
shot looks good on its own: text that leaves before it can be read, voice-over
crammed into a shot too short for it, cuts that flash, text off the safe area,
low-contrast type, layers timed outside their shot, and AI-upgrade shots with
no prompt to send.

Blocking (exit 4):
  ML1  timing      shot durations do not add up to meta.target_duration (±0.5 s)
  ML2  readability on-screen text leaves before it can be read
                   (0.5 s + words ÷ 3.0 words/s, i.e. 180 wpm, the top of Ofcom's
                   160-180 wpm subtitle guidance)
  ML3  vo-fit      voice-over needs more time than the shot gives
                   (words ÷ 2.5 words/s, a 150 wpm narration pace)
  ML4  flashes     more than 3 bright/dark flashes in any 1 s (WCAG 2.2 SC 2.3.1,
                   approximated from shot background luminance)
  ML5  contrast    text on a flat background below 4.5:1 (WCAG 2.2 SC 1.4.3)
  ML6  layer-time  a layer starts at or after its shot ends, or ends before it starts
  ML7  upgrade     a shot marked upgrade:true has no upgrade_prompt to send
Warnings (exit 0, listed):
  ML8  safe-area   estimated text box crosses a 5% edge margin (9:16 also keeps
                   clear of the top 12% and bottom 20%, where platform UI sits)
  ML9  pacing      a shot under 0.75 s, or a scene with no cut for over 8 s
  ML10 type        more than two font families

Exit codes: 0 no blocking findings, 2 bad input, 4 blocking findings.

Examples:
  motion_linter.py --sample
  motion_linter.py --scene film/scene.json --output json
  motion_linter.py --scene film/scene.json --aspect 9:16     # lint the vertical cut
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scene_model import (ASPECTS, SAMPLE_SCENE, SceneError, normalize,  # noqa: E402
                         total_duration)

READ_WPS = 3.0
READ_LEAD = 0.5
VO_WPS = 2.5
STYLE_SIZE = {"title": 0.085, "subtitle": 0.048, "body": 0.038, "caption": 0.032, "kicker": 0.026}
HEX = re.compile(r"^#?([0-9a-fA-F]{6})$")


def words(text: str) -> float:
    """Word count for timing; a long token (URL, product code) counts as one word per 6 characters."""
    return sum(max(1.0, len(w) / 6) if len(w) > 12 else 1.0 for w in re.split(r"\s+", text or "") if w)


def rel_lum(hex_color: str) -> float | None:
    m = HEX.match((hex_color or "").strip())
    if not m:
        return None
    rgb = [int(m.group(1)[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a: float, b: float) -> float:
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def resolve(theme: dict, c: str | None, default: str) -> str:
    c = c or default
    return theme.get(c, c)


def has_backdrop(shot: dict) -> bool:
    return bool(shot.get("upgrade")) or any(l["type"] in ("plate", "image") and
                                             l.get("w", 1) * l.get("h", 1) >= 0.5 or l["type"] == "plate"
                                             for l in shot["layers"])


def lint(scene: dict) -> list[dict]:
    f = []
    meta, theme = scene["meta"], scene["theme"]
    W, H = meta["width"], meta["height"]
    short = min(W, H)

    def add(rule, sev, shot, msg, fix):
        f.append({"rule": rule, "severity": sev, "shot": shot, "message": msg, "fix": fix})

    target = meta.get("target_duration")
    total = total_duration(scene)
    if target is not None and abs(total - float(target)) > 0.5:
        add("ML1", "block", None, f"shots add up to {total:.2f}s, target is {float(target):.2f}s",
            "trim or extend shot durations, or change meta.target_duration on purpose")

    fonts = {theme.get("font_heading"), theme.get("font_body")}
    t = 0.0
    lum_events = []
    for shot in scene["shots"]:
        sid, dur = shot["id"], shot["duration"]
        bg = resolve(theme, shot.get("bg"), "bg")
        bg_l = rel_lum(bg)
        lum_events.append((t, bg_l))
        backdrop = has_backdrop(shot)

        if dur < 0.75:
            add("ML9", "warn", sid, f"shot is {dur:.2f}s; under 0.75 s reads as a flash cut",
                "lengthen it or merge it with a neighbour unless the cut is deliberate")
        if dur > 8.0:
            add("ML9", "warn", sid, f"shot holds {dur:.1f}s with no cut",
                "split it or give the camera a move so the frame keeps changing")

        vo_need = words(shot.get("vo", "")) / VO_WPS
        if vo_need > dur + 1e-6:
            add("ML3", "block", sid, f"voice-over needs {vo_need:.1f}s at 150 wpm, shot is {dur:.1f}s",
                f"cut the line to {int(dur * VO_WPS)} words or lengthen the shot to {math.ceil(vo_need * 10) / 10}s")

        if shot.get("upgrade") and not (shot.get("upgrade_prompt") or "").strip():
            add("ML7", "block", sid, "upgrade:true but no upgrade_prompt",
                "write the plate prompt (subject, action, setting, light) or set upgrade:false")

        for j, L in enumerate(shot["layers"]):
            ref = f"{sid}.L{j}"
            if L["in"] >= dur or L["out"] <= L["in"]:
                add("ML6", "block", ref, f"layer timing in={L['in']} out={L['out']} does not fit a {dur}s shot",
                    "set 0 <= in < out <= duration")
                continue
            if L["type"] not in ("text", "counter", "lower_third"):
                continue
            text = L.get("text") or " ".join(str(x) for x in (L.get("title"), L.get("subtitle")) if x) \
                or f"{L.get('prefix', '')}{L.get('to', '')}{L.get('suffix', '')}"
            visible = min(L["out"], dur) - L["in"]
            need = READ_LEAD + words(text) / READ_WPS
            if L.get("style") != "caption" and visible + 1e-6 < need:
                add("ML2", "block", ref, f"'{text[:40]}' is on screen {visible:.1f}s, needs {need:.1f}s to read",
                    "show it earlier, keep it longer, or cut words")
            fg = resolve(theme, L.get("color"), "accent" if L["type"] == "counter" else "fg")
            fg_l = rel_lum(fg)
            if fg_l is not None and bg_l is not None and not backdrop and not L.get("box"):
                ratio = contrast(fg_l, bg_l)
                if ratio < 4.5:
                    add("ML5", "block", ref, f"text {fg} on {bg} is {ratio:.2f}:1",
                        "raise contrast to at least 4.5:1 or put the text on a box")
            elif backdrop and L["type"] == "text" and not L.get("box"):
                add("ML5", "warn", ref, "text over an image or AI plate; contrast cannot be checked before render",
                    "add box:true or check the rendered frame")
            if L["type"] == "text":
                size = (L.get("size") or STYLE_SIZE.get(L.get("style", "body"), 0.038)) * short
                maxw = (L.get("w") or 0.82) * W
                raw_w = len(text) * 0.52 * size
                lines = max(1, math.ceil(raw_w / maxw))
                bw, bh = min(raw_w, maxw), lines * 1.12 * size
                cx, cy = L.get("x", 0.5) * W, L.get("y", 0.5) * H
                left, right, top, bottom = cx - bw / 2, cx + bw / 2, cy - bh / 2, cy + bh / 2
                m = 0.05
                tmin, bmax = (0.12, 0.80) if H > W else (m, 1 - m)
                if left < m * W or right > (1 - m) * W or top < tmin * H or bottom > bmax * H:
                    add("ML8", "warn", ref, f"'{text[:30]}' box ~({left/W:.2f},{top/H:.2f})-({right/W:.2f},{bottom/H:.2f}) leaves the safe area",
                        "move it inward, shrink it, or set w to wrap it")
        t += dur

    for i, (start, lum) in enumerate(lum_events):
        window = [e for e in lum_events if start <= e[0] < start + 1.0]
        flips = sum(1 for a, b in zip(window, window[1:])
                    if a[1] is not None and b[1] is not None and abs(a[1] - b[1]) >= 0.1
                    and min(a[1], b[1]) < 0.8)
        if flips > 6:
            add("ML4", "block", scene["shots"][i]["id"], f"{flips} large luminance changes within 1 s",
                "space the cuts out or keep backgrounds close in brightness (WCAG 2.3.1)")
            break

    if len({x for x in fonts if x}) > 2:
        add("ML10", "warn", None, "more than two font families", "use one heading and one body face")
    return f


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint a scene.v1 film for readability, timing, flashes, contrast and safe areas.")
    ap.add_argument("--scene", help="Path to scene.v1 JSON.")
    ap.add_argument("--sample", action="store_true", help="Lint the built-in sample scene.")
    ap.add_argument("--aspect", choices=sorted(ASPECTS), help="Lint as if re-framed to this aspect.")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    args = ap.parse_args()
    try:
        raw = json.loads(json.dumps(SAMPLE_SCENE)) if (args.sample or not args.scene) else \
            json.loads(Path(args.scene).read_text(encoding="utf-8"))
        if args.aspect:
            raw.setdefault("meta", {})["aspect"] = args.aspect
            raw["meta"].pop("width", None)
            raw["meta"].pop("height", None)
        scene = normalize(raw)
    except (SceneError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    findings = lint(scene)
    blocking = [x for x in findings if x["severity"] == "block"]
    verdict = "BLOCKED" if blocking else ("PASS-WITH-WARNINGS" if findings else "PASS")
    if args.output == "json":
        print(json.dumps({"verdict": verdict, "blocking": len(blocking), "warnings": len(findings) - len(blocking),
                          "aspect": scene["meta"]["aspect"], "findings": findings}, indent=2))
    else:
        print(f"{verdict}: {len(blocking)} blocking, {len(findings) - len(blocking)} warnings "
              f"({scene['meta']['aspect']}, {total_duration(scene):.2f}s)")
        for x in findings:
            print(f"  [{x['severity']:5}] {x['rule']:4} {x['shot'] or '-':>8}  {x['message']}\n"
                  f"{'':23}fix: {x['fix']}")
    return 4 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
