#!/usr/bin/env python3
"""scene_model.py — the scene.v1 model shared by the animatic tools.

A scene.v1 file is the single source of truth for one film: canvas, theme,
shots, and the layers inside each shot. Coordinates are normalized (0..1) so
one scene renders at 16:9, 9:16 or 1:1 without rewriting it.

This module loads and validates a scene, computes the shot timeline (where
each shot starts and ends once transitions are counted), and carries the
sample scene the other tools use for --sample. Stdlib only.

Run it directly to print the sample scene or the timeline of a scene file:
  scene_model.py --sample
  scene_model.py --scene my-film/scene.json --timeline
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

SCHEMA = "scene.v1"

LAYER_TYPES = {"text", "shape", "image", "chart", "counter", "lower_third", "plate"}
CAMERA_MOVES = {"static", "push-in", "pull-out", "pan-left", "pan-right",
                "tilt-up", "tilt-down", "drift"}
TRANSITIONS = {"cut", "fade", "dip"}
EASINGS = {"linear", "ease-in", "ease-out", "ease-in-out", "back-out", "expo-out"}
ANIMS = {"none", "fade", "rise", "scale", "type", "words", "draw", "grow",
         "kenburns", "slide"}

ASPECTS = {
    "16:9": (1920, 1080),
    "9:16": (1080, 1920),
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
}

DEFAULT_THEME = {
    "bg": "#0b0d12",
    "fg": "#f5f7fa",
    "accent": "#5b8cff",
    "muted": "#8a93a6",
    "font_heading": "Inter",
    "font_body": "Inter",
}

SAMPLE_SCENE = {
    "schema": SCHEMA,
    "meta": {
        "title": "Release 2.0 teaser",
        "aspect": "16:9",
        "fps": 30,
        "target_duration": 12.0,
        "mode": "greybox",
        "captions": False,
    },
    "theme": dict(DEFAULT_THEME),
    "shots": [
        {
            "id": "s1",
            "duration": 3.5,
            "transition": "cut",
            "camera": {"move": "push-in", "amount": 0.08, "ease": "ease-in-out"},
            "vo": "Your release notes are a wall of text.",
            "layers": [
                {"type": "text", "text": "Release notes nobody reads", "style": "title",
                 "x": 0.5, "y": 0.45, "in": 0.2, "anim": "words"},
                {"type": "text", "text": "v1.9 · 214 changes", "style": "kicker",
                 "x": 0.5, "y": 0.6, "in": 0.9, "anim": "fade", "color": "muted"},
            ],
        },
        {
            "id": "s2",
            "duration": 4.0,
            "transition": "fade",
            "camera": {"move": "drift", "amount": 0.04},
            "vo": "Version two ships three things that matter.",
            "upgrade": True,
            "upgrade_prompt": "Slow dolly across a dark desk, laptop screen glowing blue, shallow depth of field",
            "layers": [
                {"type": "plate", "label": "Desk at night, laptop glow"},
                {"type": "chart", "kind": "bar", "x": 0.5, "y": 0.55, "w": 0.6, "h": 0.45,
                 "data": [["Build", 41], ["Deploy", 18], ["Review", 9]],
                 "title": "Minutes saved per release", "in": 0.4, "anim": "grow"},
            ],
        },
        {
            "id": "s3",
            "duration": 4.5,
            "transition": "dip",
            "camera": {"move": "static"},
            "vo": "Ship faster. Try it today.",
            "layers": [
                {"type": "counter", "from": 0, "to": 68, "suffix": " min", "x": 0.5, "y": 0.42,
                 "style": "title", "in": 0.2, "dur": 1.6},
                {"type": "text", "text": "saved on every release", "style": "subtitle",
                 "x": 0.5, "y": 0.58, "in": 0.8, "anim": "rise"},
                {"type": "lower_third", "title": "example.dev/v2", "subtitle": "Available now",
                 "in": 1.6},
            ],
        },
    ],
}


class SceneError(ValueError):
    """Raised when a scene file cannot be used at all."""


def load_scene(path: str | Path) -> dict:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SceneError(f"scene file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SceneError(f"scene file is not valid JSON: {exc}") from exc
    return normalize(data)


def canvas_size(meta: dict) -> tuple[int, int]:
    if meta.get("width") and meta.get("height"):
        return int(meta["width"]), int(meta["height"])
    return ASPECTS.get(meta.get("aspect", "16:9"), ASPECTS["16:9"])


def normalize(scene: dict) -> dict:
    """Fill defaults and raise SceneError on structural problems."""
    if not isinstance(scene, dict):
        raise SceneError("scene must be a JSON object")
    if scene.get("schema") != SCHEMA:
        raise SceneError(f'scene.schema must be "{SCHEMA}"')
    shots = scene.get("shots")
    if not isinstance(shots, list) or not shots:
        raise SceneError("scene.shots must be a non-empty list")
    out = copy.deepcopy(scene)
    meta = out.setdefault("meta", {})
    meta.setdefault("title", "Untitled")
    meta.setdefault("aspect", "16:9")
    if meta["aspect"] not in ASPECTS and not (meta.get("width") and meta.get("height")):
        raise SceneError(f"meta.aspect must be one of {sorted(ASPECTS)} or give width and height")
    meta.setdefault("fps", 30)
    meta.setdefault("mode", "greybox")
    if meta["mode"] not in ("greybox", "final"):
        raise SceneError('meta.mode must be "greybox" or "final"')
    meta.setdefault("captions", False)
    w, h = canvas_size(meta)
    meta["width"], meta["height"] = w, h
    theme = out.setdefault("theme", {})
    for key, val in DEFAULT_THEME.items():
        theme.setdefault(key, val)
    seen = set()
    for i, shot in enumerate(out["shots"]):
        shot.setdefault("id", f"s{i + 1}")
        if shot["id"] in seen:
            raise SceneError(f"duplicate shot id {shot['id']}")
        seen.add(shot["id"])
        try:
            shot["duration"] = float(shot["duration"])
        except (KeyError, TypeError, ValueError) as exc:
            raise SceneError(f"shot {shot['id']}: duration (seconds) is required") from exc
        if shot["duration"] <= 0:
            raise SceneError(f"shot {shot['id']}: duration must be > 0")
        shot.setdefault("transition", "cut")
        if shot["transition"] not in TRANSITIONS:
            raise SceneError(f"shot {shot['id']}: transition must be one of {sorted(TRANSITIONS)}")
        shot.setdefault("transition_duration", 0.5 if shot["transition"] != "cut" else 0.0)
        cam = shot.setdefault("camera", {})
        cam.setdefault("move", "static")
        if cam["move"] not in CAMERA_MOVES:
            raise SceneError(f"shot {shot['id']}: camera.move must be one of {sorted(CAMERA_MOVES)}")
        cam.setdefault("amount", 0.06)
        cam.setdefault("ease", "ease-in-out")
        shot.setdefault("vo", "")
        shot.setdefault("upgrade", False)
        shot.setdefault("layers", [])
        for j, layer in enumerate(shot["layers"]):
            ltype = layer.get("type")
            if ltype not in LAYER_TYPES:
                raise SceneError(f"shot {shot['id']} layer {j}: type must be one of {sorted(LAYER_TYPES)}")
            layer.setdefault("in", 0.0)
            layer.setdefault("out", shot["duration"])
            layer.setdefault("anim", "fade" if ltype not in ("plate", "chart") else
                             ("grow" if ltype == "chart" else "none"))
            if layer["anim"] not in ANIMS:
                raise SceneError(f"shot {shot['id']} layer {j}: anim must be one of {sorted(ANIMS)}")
            layer.setdefault("ease", "expo-out")
            if layer["ease"] not in EASINGS:
                raise SceneError(f"shot {shot['id']} layer {j}: ease must be one of {sorted(EASINGS)}")
    return out


def timeline(scene: dict) -> list[dict]:
    """Start/end of every shot. A fade or dip overlaps nothing: shots run back
    to back, and the incoming shot's transition plays over its own first
    `transition_duration` seconds (a crossfade keeps the outgoing shot's last
    frame underneath)."""
    t = 0.0
    rows = []
    for shot in scene["shots"]:
        start = t
        end = t + shot["duration"]
        rows.append({"id": shot["id"], "start": round(start, 4), "end": round(end, 4),
                     "duration": shot["duration"], "transition": shot["transition"],
                     "upgrade": bool(shot.get("upgrade"))})
        t = end
    return rows


def total_duration(scene: dict) -> float:
    return round(sum(s["duration"] for s in scene["shots"]), 4)


def main() -> int:
    ap = argparse.ArgumentParser(description="scene.v1 model: print the sample scene or a scene's timeline.")
    ap.add_argument("--scene", help="Path to a scene.v1 JSON file.")
    ap.add_argument("--timeline", action="store_true", help="Print shot start/end times.")
    ap.add_argument("--sample", action="store_true", help="Use the built-in sample scene.")
    ap.add_argument("--output", choices=["text", "json"], default="json")
    args = ap.parse_args()
    try:
        scene = normalize(SAMPLE_SCENE) if (args.sample or not args.scene) else load_scene(args.scene)
    except SceneError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.timeline:
        rows = timeline(scene)
        if args.output == "json":
            print(json.dumps({"total": total_duration(scene), "shots": rows}, indent=2))
        else:
            for r in rows:
                print(f"{r['id']:>6}  {r['start']:7.2f} → {r['end']:7.2f}  {r['transition']}"
                      f"{'  [upgrade]' if r['upgrade'] else ''}")
            print(f"total {total_duration(scene):.2f}s")
        return 0
    print(json.dumps(scene, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
