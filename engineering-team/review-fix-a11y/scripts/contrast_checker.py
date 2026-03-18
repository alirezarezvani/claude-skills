#!/usr/bin/env python3
"""
contrast_checker.py — WCAG contrast ratio calculator.

Computes relative luminance and contrast ratio between two colors.
Stdlib-only, zero pip installs required.

Usage:
    python scripts/contrast_checker.py "#1a1a2e" "#ffffff"
    python scripts/contrast_checker.py "rgb(26,26,46)" "white"
    python scripts/contrast_checker.py "#1a1a2e" "#ffffff" --json
    python scripts/contrast_checker.py "#1a1a2e" --suggest  # suggest accessible pairs
"""

import argparse
import json
import sys

# ---------------------------------------------------------------------------
# Color parsing
# ---------------------------------------------------------------------------

NAMED_COLORS = {
    "white": "#ffffff",
    "black": "#000000",
    "red": "#ff0000",
    "green": "#008000",
    "blue": "#0000ff",
    "gray": "#808080",
    "grey": "#808080",
    "silver": "#c0c0c0",
    "navy": "#000080",
    "yellow": "#ffff00",
    "orange": "#ffa500",
    "purple": "#800080",
    "pink": "#ffc0cb",
    "teal": "#008080",
}


def parse_color(color: str) -> tuple[int, int, int]:
    """Parse a color string to (r, g, b) tuple (0-255 each)."""
    color = color.strip().lower()

    # Named color
    if color in NAMED_COLORS:
        color = NAMED_COLORS[color]

    # Hex #rrggbb or #rgb
    if color.startswith("#"):
        hex_str = color[1:]
        if len(hex_str) == 3:
            hex_str = "".join(c * 2 for c in hex_str)
        if len(hex_str) != 6:
            raise ValueError(f"Invalid hex color: {color}")
        r = int(hex_str[0:2], 16)
        g = int(hex_str[2:4], 16)
        b = int(hex_str[4:6], 16)
        return r, g, b

    # rgb(r, g, b)
    if color.startswith("rgb("):
        inner = color[4:].rstrip(")")
        parts = [p.strip() for p in inner.split(",")]
        if len(parts) != 3:
            raise ValueError(f"Invalid rgb() color: {color}")
        return int(parts[0]), int(parts[1]), int(parts[2])

    raise ValueError(f"Unsupported color format: {color!r}. Use #hex, rgb(), or a named color.")


# ---------------------------------------------------------------------------
# WCAG contrast calculation
# ---------------------------------------------------------------------------

def _linearize(channel: int) -> float:
    """Convert 8-bit channel value to linear light."""
    s = channel / 255.0
    if s <= 0.04045:
        return s / 12.92
    return ((s + 0.055) / 1.055) ** 2.4


def relative_luminance(r: int, g: int, b: int) -> float:
    """Compute WCAG relative luminance (0=black, 1=white)."""
    return 0.2126 * _linearize(r) + 0.7152 * _linearize(g) + 0.0722 * _linearize(b)


def contrast_ratio(color1: tuple, color2: tuple) -> float:
    """Compute WCAG contrast ratio between two (r,g,b) tuples."""
    l1 = relative_luminance(*color1)
    l2 = relative_luminance(*color2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# ---------------------------------------------------------------------------
# WCAG pass/fail assessment
# ---------------------------------------------------------------------------

def assess(ratio: float) -> dict:
    return {
        "ratio": round(ratio, 2),
        "normal_text": {
            "AA": ratio >= 4.5,
            "AAA": ratio >= 7.0,
        },
        "large_text": {
            "AA": ratio >= 3.0,
            "AAA": ratio >= 4.5,
        },
        "ui_components": {
            "AA": ratio >= 3.0,
        },
    }


def _pass_fail(val: bool) -> str:
    return "PASS ✅" if val else "FAIL ❌"


# ---------------------------------------------------------------------------
# Suggest accessible dark/light pairs for a given foreground
# ---------------------------------------------------------------------------

SUGGEST_BACKGROUNDS = [
    ("#ffffff", "white"),
    ("#f8f9fa", "near-white"),
    ("#e9ecef", "light gray"),
    ("#dee2e6", "mid-light gray"),
    ("#1a1a2e", "near-black"),
    ("#212529", "dark gray"),
    ("#343a40", "charcoal"),
    ("#000000", "black"),
]


def suggest_pairs(foreground_str: str) -> list[dict]:
    fg = parse_color(foreground_str)
    results = []
    for bg_hex, bg_name in SUGGEST_BACKGROUNDS:
        bg = parse_color(bg_hex)
        r = contrast_ratio(fg, bg)
        a = assess(r)
        results.append({
            "background": bg_hex,
            "background_name": bg_name,
            "ratio": a["ratio"],
            "normal_AA": a["normal_text"]["AA"],
            "large_AA": a["large_text"]["AA"],
        })
    # Sort by ratio descending
    results.sort(key=lambda x: x["ratio"], reverse=True)
    return results


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def print_assessment(fg_str: str, bg_str: str, ratio: float, a: dict) -> None:
    print(f"\n{'='*50}")
    print(f"  Foreground : {fg_str}")
    print(f"  Background : {bg_str}")
    print(f"  Ratio      : {a['ratio']}:1")
    print(f"{'='*50}")
    print(f"  Normal text   AA  (4.5:1): {_pass_fail(a['normal_text']['AA'])}")
    print(f"  Normal text   AAA (7.0:1): {_pass_fail(a['normal_text']['AAA'])}")
    print(f"  Large text    AA  (3.0:1): {_pass_fail(a['large_text']['AA'])}")
    print(f"  Large text    AAA (4.5:1): {_pass_fail(a['large_text']['AAA'])}")
    print(f"  UI components AA  (3.0:1): {_pass_fail(a['ui_components']['AA'])}")
    print(f"{'='*50}\n")

    if not a["normal_text"]["AA"]:
        # Calculate how much darker/lighter needed
        needed = 4.5
        print(f"  ⚠️  Normal text fails AA. Need ratio ≥ {needed}:1")
        print("  Run with --suggest to see accessible background options.\n")


def print_suggestions(fg_str: str, suggestions: list[dict]) -> None:
    print(f"\n  Accessible backgrounds for foreground {fg_str}:\n")
    print(f"  {'Background':<20} {'Name':<16} {'Ratio':>7}  Normal AA  Large AA")
    print(f"  {'-'*20} {'-'*16} {'-'*7}  {'-'*9}  {'-'*8}")
    for s in suggestions:
        n_aa = "PASS" if s["normal_AA"] else "fail"
        l_aa = "PASS" if s["large_AA"] else "fail"
        print(
            f"  {s['background']:<20} {s['background_name']:<16} "
            f"{s['ratio']:>6.2f}:1  {n_aa:<9}  {l_aa}"
        )
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="WCAG contrast ratio calculator.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("foreground", help="Foreground color (#hex, rgb(), or name)")
    parser.add_argument("background", nargs="?", help="Background color")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument(
        "--suggest",
        action="store_true",
        help="Suggest accessible background options for the given foreground",
    )
    args = parser.parse_args()

    try:
        fg = parse_color(args.foreground)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.suggest:
        suggestions = suggest_pairs(args.foreground)
        if args.json:
            print(json.dumps({"foreground": args.foreground, "suggestions": suggestions}, indent=2))
        else:
            print_suggestions(args.foreground, suggestions)
        return

    if not args.background:
        parser.error("background color is required unless --suggest is used")

    try:
        bg = parse_color(args.background)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    ratio = contrast_ratio(fg, bg)
    a = assess(ratio)

    if args.json:
        print(json.dumps({
            "foreground": args.foreground,
            "background": args.background,
            **a,
        }, indent=2))
    else:
        print_assessment(args.foreground, args.background, ratio, a)

    # Exit 1 if fails normal text AA
    sys.exit(0 if a["normal_text"]["AA"] else 1)


if __name__ == "__main__":
    main()
