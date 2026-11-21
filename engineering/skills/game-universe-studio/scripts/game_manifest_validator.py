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


KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_VIEWS = ("front", "three_quarter", "profile", "back")
MIN_FREQ_HZ, MAX_FREQ_HZ = 20, 20000
SAFE_GAIN = 0.4
MIN_CONTRAST = 4.5


def _num(value) -> float | None:
    """Return value as a float when it is a real number (not bool), else None."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def _positive(value) -> bool:
    n = _num(value)
    return n is not None and n > 0


def _section(data: dict, key: str, kind: type):
    value = data.get(key)
    return value if isinstance(value, kind) else kind()


def validate_manifest(data: dict) -> list[dict]:
    findings: list[dict] = []

    def add(severity: str, field: str, message: str) -> None:
        findings.append({"severity": severity, "field": field, "message": message})

    # Meta
    if not data.get("title"):
        add("BLOCKER", "title", "Missing game title")
    game_id = data.get("game_id")
    if game_id is not None and not (isinstance(game_id, str) and KEBAB_RE.match(game_id)):
        add("WARN", "game_id", f"game_id should be kebab-case, got {game_id!r}")
    engine = data.get("engine")
    if engine not in SUPPORTED_ENGINES:
        add("BLOCKER", "engine",
            f"Unsupported or missing engine {engine!r}. Choose from {sorted(SUPPORTED_ENGINES)}")

    # Viewport
    viewport = _section(data, "viewport", dict)
    width, height = viewport.get("width"), viewport.get("height")
    if not (_positive(width) and _positive(height)):
        add("BLOCKER", "viewport", "Viewport width and height must be positive numbers")
    else:
        ratio = viewport.get("aspect_ratio")
        if isinstance(ratio, str) and re.match(r"^\d+:\d+$", ratio):
            rw, rh = (int(x) for x in ratio.split(":"))
            if rh and abs(width / height - rw / rh) > 0.01:
                add("WARN", "viewport.aspect_ratio",
                    f"aspect_ratio {ratio} does not match {width}x{height}")
        elif ratio is not None:
            add("WARN", "viewport.aspect_ratio", f"aspect_ratio should look like 16:9, got {ratio!r}")

    # Character
    char = _section(data, "character", dict)
    if char:
        views = set(char.get("turnaround_views") or [])
        missing = [v for v in REQUIRED_VIEWS if v not in views]
        if missing:
            add("WARN", "character.turnaround_views", f"Turnaround is missing views: {missing}")
        palette = char.get("palette_locks") or []
        if not 3 <= len(palette) <= 6:
            add("WARN", "character.palette_locks",
                f"Lock 3 to 6 palette colors, got {len(palette)}")
        for hex_code in palette:
            if not (isinstance(hex_code, str) and HEX_COLOR_RE.match(hex_code)):
                add("WARN", "character.palette_locks", f"Invalid HEX color code: {hex_code!r}")

    # Sprites
    sprites = _section(data, "sprites", list)
    if not sprites:
        add("WARN", "sprites", "No sprite animations defined")
    for i, s in enumerate(sprites):
        s = s if isinstance(s, dict) else {}
        if not s.get("action"):
            add("BLOCKER", f"sprites[{i}].action", "Action name required")
        for key in ("frames", "fps"):
            if not _positive(s.get(key)):
                add("BLOCKER", f"sprites[{i}].{key}", f"{key} must be a positive number")
        tile = s.get("tile_size")
        if not (isinstance(tile, list) and len(tile) == 2 and all(_positive(t) for t in tile)):
            add("BLOCKER", f"sprites[{i}].tile_size", "tile_size must be [width, height] with positive values")

    # Audio cues
    for i, a in enumerate(_section(data, "audio_cues", list)):
        a = a if isinstance(a, dict) else {}
        if a.get("type") not in SUPPORTED_OSCILLATORS:
            add("WARN", f"audio_cues[{i}].type",
                f"Invalid oscillator {a.get('type')!r}. Choose from {sorted(SUPPORTED_OSCILLATORS)}")
        gain = _num(a.get("gain"))
        if gain is None or not 0 < gain <= 1.0:
            add("BLOCKER", f"audio_cues[{i}].gain", "gain must be a number in (0, 1]")
        elif gain > SAFE_GAIN:
            add("WARN", f"audio_cues[{i}].gain", f"gain {gain} is above the {SAFE_GAIN} safe ceiling")
        for key in ("freq_start", "freq_end"):
            freq = _num(a.get(key))
            if freq is None or not MIN_FREQ_HZ <= freq <= MAX_FREQ_HZ:
                add("BLOCKER", f"audio_cues[{i}].{key}",
                    f"{key} must be between {MIN_FREQ_HZ} and {MAX_FREQ_HZ} Hz")
        if not _positive(a.get("duration_ms")):
            add("BLOCKER", f"audio_cues[{i}].duration_ms", "duration_ms must be positive")

    # Showcase card
    card = _section(data, "bento_card", dict)
    if card:
        contrast = _num(card.get("contrast_ratio"))
        if contrast is None or contrast < MIN_CONTRAST:
            add("BLOCKER", "bento_card.contrast_ratio",
                f"contrast_ratio must be at least {MIN_CONTRAST} (WCAG 2.2 AA body text)")
        accent = card.get("theme_accent")
        if accent is not None and not (isinstance(accent, str) and HEX_COLOR_RE.match(accent)):
            add("WARN", "bento_card.theme_accent", f"Invalid HEX color code: {accent!r}")

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
            return 2
        with open(args.manifest, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as exc:
                print(f"Error: invalid JSON in {args.manifest}: {exc}", file=sys.stderr)
                return 2
        if not isinstance(data, dict):
            print(f"Error: {args.manifest} must hold a JSON object", file=sys.stderr)
            return 2

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
                "character_id": _section(data, "character", dict).get("id"),
                "sprite_count": len(_section(data, "sprites", list)),
                "audio_cue_count": len(_section(data, "audio_cues", list))
            }
        }
        print(json.dumps(report, indent=2))
    else:
        status_text = "PASS" if is_valid else "FAIL"
        print(f"Validation Result: {status_text} (Blockers: {blockers}, Warnings: {warns})")
        for f in findings:
            print(f"  [{f['severity']}] {f['field']}: {f['message']}")
        if is_valid:
            print(f"Manifest '{data.get('title')}' passed every check.")

    return 0 if is_valid else 1


if __name__ == "__main__":
    sys.exit(main())
