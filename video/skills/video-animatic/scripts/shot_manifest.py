#!/usr/bin/env python3
"""shot_manifest.py — turn the approved animatic into a provider-neutral shot list for AI upgrades.

For every shot marked upgrade:true it writes one request a video model can
take: the plate prompt, the shot's exact duration, the aspect ratio, a camera
intent sentence derived from the animatic's camera move, and (when keyframes
were rendered with frame_renderer.py --keyframes from a --mode final page,
and the plate has a storyboard still as its src) the clean first and last
frames to condition on. A greybox placeholder carries no framing, so its
frames are never sent. It also totals the generated seconds, which is the
number a credit quote is built on.

The manifest names no provider and calls nothing. Sending it to a generation
MCP is a separate, explicit step that starts with a cost quote and waits for
a yes. Text, charts and logos stay in the animatic as code layers and are
composited over the generated plate, so they are never in the prompt.

Exit codes: 0 manifest written, 2 bad input, 3 no shot is marked for upgrade.

Examples:
  shot_manifest.py --sample
  shot_manifest.py --scene film/scene.json --keyframes film/keyframes --out film/shots.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scene_model import SAMPLE_SCENE, SceneError, normalize, timeline  # noqa: E402

MOVE_WORDS = {
    "static": "locked-off static camera",
    "push-in": "slow dolly push-in",
    "pull-out": "slow dolly pull-out",
    "pan-left": "smooth pan left",
    "pan-right": "smooth pan right",
    "tilt-up": "slow tilt up",
    "tilt-down": "slow tilt down",
    "drift": "gentle handheld-style drift",
}
SPEED_WORDS = [(0.04, "subtle"), (0.10, "moderate"), (9.9, "strong")]


def camera_intent(cam: dict, duration: float) -> str:
    move = cam.get("move", "static")
    if move == "static":
        return f"{MOVE_WORDS['static']} for {duration:g}s"
    amt = float(cam.get("amount", 0.06))
    speed = next(word for limit, word in SPEED_WORDS if amt <= limit)
    ease = cam.get("ease", "ease-in-out").replace("-", " ")
    return f"{speed} {MOVE_WORDS.get(move, move)} over {duration:g}s, {ease}"


def build(scene: dict, keyframes: Path | None) -> dict:
    rows = {r["id"]: r for r in timeline(scene)}
    shots = []
    for shot in scene["shots"]:
        if not shot.get("upgrade"):
            continue
        sid = shot["id"]
        kf = {}
        has_still = any(l["type"] in ("plate", "image") and l.get("src") for l in shot["layers"])
        if keyframes and has_still:
            for edge in ("first", "last"):
                p = keyframes / f"{sid}_{edge}.png"
                kf[edge] = str(p.resolve()) if p.exists() else None
        overlays = [l["type"] for l in shot["layers"] if l["type"] not in ("plate", "image")]
        shots.append({
            "id": sid,
            "start": rows[sid]["start"],
            "duration": shot["duration"],
            "aspect_ratio": scene["meta"]["aspect"],
            "prompt": (shot.get("upgrade_prompt") or "").strip(),
            "camera_intent": camera_intent(shot["camera"], shot["duration"]),
            "start_image": kf.get("first"),
            "end_image": kf.get("last"),
            "conditioning": "first+last keyframe" if kf.get("first") and kf.get("last") else
                            ("first keyframe" if kf.get("first") else "text only"),
            "keyframe_note": None if has_still else
                "the plate is a greybox placeholder, so its frames carry no framing; add a storyboard "
                "still as the plate src and render keyframes from a --mode final page to condition on it",
            "vo": shot.get("vo", ""),
            "code_overlays": overlays,
            "negative": "no on-screen text, no captions, no logos, no watermarks",
            "status": "needs-quote",
        })
    total = round(sum(s["duration"] for s in shots), 3)
    return {
        "schema": "shots.v1",
        "title": scene["meta"]["title"],
        "canvas": [scene["meta"]["width"], scene["meta"]["height"]],
        "fps": scene["meta"]["fps"],
        "upgrade_shots": len(shots),
        "generated_seconds": total,
        "motion_only_shots": len(scene["shots"]) - len(shots),
        "shots": shots,
        "next": "quote every shot with the provider's cost preflight, show the total against the budget cap, "
                "and generate only after an explicit yes",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a provider-neutral upgrade manifest (shots.v1) from an approved scene.")
    ap.add_argument("--scene", help="Path to scene.v1 JSON.")
    ap.add_argument("--keyframes", help="Directory written by frame_renderer.py --keyframes.")
    ap.add_argument("--out", help="Write the manifest here (default: print only).")
    ap.add_argument("--sample", action="store_true", help="Use the built-in sample scene.")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    args = ap.parse_args()
    try:
        raw = SAMPLE_SCENE if (args.sample or not args.scene) else json.loads(Path(args.scene).read_text(encoding="utf-8"))
        scene = normalize(raw)
    except (SceneError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    manifest = build(scene, Path(args.keyframes) if args.keyframes else None)
    if not manifest["shots"]:
        print("error: no shot has upgrade:true; the film is motion-only and needs no generation", file=sys.stderr)
        return 3
    if args.out:
        Path(args.out).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if args.output == "json":
        print(json.dumps(manifest, indent=2))
    else:
        print(f"{manifest['upgrade_shots']} shot(s) to upgrade, {manifest['generated_seconds']:g}s of generated video; "
              f"{manifest['motion_only_shots']} stay motion graphics")
        for s in manifest["shots"]:
            print(f"  {s['id']:>6}  {s['duration']:g}s  {s['aspect_ratio']}  [{s['conditioning']}]  {s['camera_intent']}")
            print(f"{'':10}prompt: {s['prompt']}")
        if args.out:
            print(f"manifest: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
