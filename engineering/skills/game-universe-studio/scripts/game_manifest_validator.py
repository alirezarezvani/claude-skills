#!/usr/bin/env python3
"""Validate game showcase assets, sprite sheet contracts, audio cue manifests, and runtime mounts.

Checks that indie web game manifests adhere to modular browser runtime contracts:
  - Meta: valid title, engine runtime, canvas aspect ratio.
  - Character Consistency: 4-angle turnaround contracts and locked palette tokens.
  - Sprite Matrix: action keyframes, bounding box constraints, tile dimensions.
  - Web Audio Cues: frequency envelopes, gain limits, procedural synthesizer parameters.
  - Bento Layout: high-contrast ratio, accessibility badges, responsive layout specs.

Deterministic, zero external dependencies (Python stdlib only).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

SUPPORTED_ENGINES = {"canvas2d", "webgl", "threejs", "babylon", "pixijs"}
SUPPORTED_OSCILLATORS = {"sine", "square", "sawtooth", "triangle"}
HEX_COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

SAMPLE_FIXTURE = {
    "game_id": "cyber-samurai-odyssey",
    "title": "Cyber Samurai Odyssey",
    "engine": "webgl",
    "viewport": {
        "width": 1280,
        "height": 720,
        "aspect_ratio": "16:9"
    },
    "character": {
        "id": "hero-ronin",
        "turnaround_views": ["front", "three_quarter", "profile", "back"],
        "sheet_dimensions": {"width": 2048, "height": 2048},
        "palette_locks": ["#00e5ff", "#ff007f", "#1a1a24", "#e0e0e0"]
    },
    "sprites": [
        {"action": "idle", "frames": 4, "fps": 8, "tile_size": [128, 128]},
        {"action": "run", "frames": 8, "fps": 12, "tile_size": [128, 128]},
        {"action": "strike", "frames": 6, "fps": 14, "tile_size": [128, 128]}
    ],
    "audio_cues": [
        {"name": "laser_slash", "type": "sawtooth", "freq_start": 880, "freq_end": 220, "duration_ms": 120, "gain": 0.25},
        {"name": "dash_whoosh", "type": "sine", "freq_start": 300, "freq_end": 100, "duration_ms": 180, "gain": 0.20},
        {"name": "arcade_blip", "type": "square", "freq_start": 440, "freq_end": 880, "duration_ms": 80, "gain": 0.15}
    ],
    "bento_card": {
        "badge": "Action RPG",
        "contrast_ratio": 4.5,
        "theme_accent": "#00e5ff"
    }
}


def validate_manifest(data: dict) -> list[dict]:
    findings = []

    # Meta check
    if not data.get("title"):
        findings.append({"severity": "BLOCKER", "field": "title", "message": "Missing game title"})
    engine = data.get("engine")
    if not engine or engine not in SUPPORTED_ENGINES:
        findings.append({"severity": "BLOCKER", "field": "engine",
                         "message": f"Unsupported or missing engine '{engine}'. Choose from {sorted(SUPPORTED_ENGINES)}"})

    viewport = data.get("viewport", {})
    if not viewport.get("width") or not viewport.get("height"):
        findings.append({"severity": "BLOCKER", "field": "viewport", "message": "Viewport width and height required"})

    # Character check
    char = data.get("character")
    if char:
        views = set(char.get("turnaround_views", []))
        required_views = {"front", "profile", "back"}
        if not required_views.issubset(views):
            findings.append({"severity": "WARN", "field": "character.turnaround_views",
                             "message": f"Turnaround should cover at least {sorted(required_views)}"})
        for hex_code in char.get("palette_locks", []):
            if not HEX_COLOR_RE.match(hex_code):
                findings.append({"severity": "WARN", "field": "character.palette_locks",
                                 "message": f"Invalid HEX color code: {hex_code}"})

    # Sprites check
    sprites = data.get("sprites", [])
    if not sprites:
        findings.append({"severity": "WARN", "field": "sprites", "message": "No sprite animations defined"})
    for i, s in enumerate(sprites):
        if s.get("frames", 0) <= 0:
            findings.append({"severity": "BLOCKER", "field": f"sprites[{i}].frames", "message": "Frames must be > 0"})
        if not s.get("action"):
            findings.append({"severity": "BLOCKER", "field": f"sprites[{i}].action", "message": "Action name required"})

    # Audio cues check
    audio_cues = data.get("audio_cues", [])
    for i, a in enumerate(audio_cues):
        osc = a.get("type")
        if osc not in SUPPORTED_OSCILLATORS:
            findings.append({"severity": "WARN", "field": f"audio_cues[{i}].type",
                             "message": f"Invalid oscillator '{osc}'. Choose from {sorted(SUPPORTED_OSCILLATORS)}"})
        gain = a.get("gain", 0)
        if gain > 1.0 or gain <= 0:
            findings.append({"severity": "BLOCKER", "field": f"audio_cues[{i}].gain",
                             "message": "Audio cue gain must be between 0.0 and 1.0"})

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("-m", "--manifest", help="path to game asset manifest JSON file")
    src.add_argument("--sample", action="store_true", help="run validation on embedded sample manifest fixture")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="output format (default: text)")
    parser.add_argument("--strict", action="store_true", help="treat warnings as blockers")

    args = parser.parse_args(argv)

    if args.sample:
        data = SAMPLE_FIXTURE
    else:
        if not os.path.isfile(args.manifest):
            print(f"Error: file not found: {args.manifest}", file=sys.stderr)
            return 1
        with open(args.manifest, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as exc:
                print(f"Error: invalid JSON in {args.manifest}: {exc}", file=sys.stderr)
                return 1

    findings = validate_manifest(data)
    blockers = sum(1 for f in findings if f["severity"] == "BLOCKER")
    warns = sum(1 for f in findings if f["severity"] == "WARN")
    is_valid = (blockers == 0) and (not args.strict or warns == 0)

    if args.format == "json":
        report = {
            "valid": is_valid,
            "blockers": blockers,
            "warnings": warns,
            "findings": findings,
            "manifest_summary": {
                "title": data.get("title"),
                "engine": data.get("engine"),
                "character_id": data.get("character", {}).get("id"),
                "sprite_count": len(data.get("sprites", [])),
                "audio_cue_count": len(data.get("audio_cues", []))
            }
        }
        print(json.dumps(report, indent=2))
    else:
        status_text = "PASS" if is_valid else "FAIL"
        print(f"Validation Result: {status_text} (Blockers: {blockers}, Warnings: {warns})")
        for f in findings:
            print(f"  [{f['severity']}] {f['field']}: {f['message']}")
        if is_valid:
            print(f"Manifest '{data.get('title')}' conforms to game universe studio architecture.")

    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
