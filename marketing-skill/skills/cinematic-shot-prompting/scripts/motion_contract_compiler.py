#!/usr/bin/env python3
"""
Motion Contract Compiler
Compiles natural narrative camera movements into a deterministic 7-Slot Camera Motion Contract.
Dependency-free (Python standard library only).
"""

import argparse
import json
import re
import sys

SAMPLE_INTENT = "A lone astronaut walking on Martian red sand at dusk, camera slowly orbits around him while rising"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compile narrative camera movement into a 7-Slot Motion Contract."
    )
    parser.add_argument(
        "--intent",
        type=str,
        default=None,
        help="Natural language description of the camera movement.",
    )
    parser.add_argument(
        "--mechanism",
        type=str,
        default=None,
        choices=["dolly", "crane", "orbit", "pan", "track"],
        help="Optional override for primary camera mechanical translation type.",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Run on an embedded sample intent for verification and smoke testing.",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="markdown",
        choices=["markdown", "json"],
        help="Output format (markdown or json).",
    )
    return parser.parse_args()


def detect_mechanism(intent_lower: str, explicit_mechanism: str = None) -> str:
    if explicit_mechanism:
        return explicit_mechanism
    if any(k in intent_lower for k in ["crane", "jib", "rise", "rising", "ascend", "overhead", "high-angle"]):
        return "crane"
    if any(k in intent_lower for k in ["orbit", "circular", "circle", "arc", "revolve", "around"]):
        return "orbit"
    if any(k in intent_lower for k in ["pan", "tilt", "sweep", "rotate", "whip"]):
        return "pan"
    if any(k in intent_lower for k in ["track", "truck", "follow", "lateral", "alongside"]):
        return "track"
    return "dolly"


def detect_velocity(intent_lower: str) -> str:
    if any(k in intent_lower for k in ["slow", "slowly", "gentle", "crawl", "gradual", "subtle"]):
        return "Slow continuous rate (0.25m/s) with 0.8s ease-in and ease-out stabilization"
    if any(k in intent_lower for k in ["fast", "rapid", "rush", "sprint", "whip", "quick", "dynamic"]):
        return "Accelerated dynamic profile (1.2m/s) with 0.3s snap deceleration"
    return "Linear continuous velocity (0.5m/s) with steady-state mechanical damping"


def detect_subject_lock(intent_lower: str) -> str:
    subjects = []
    if any(k in intent_lower for k in ["astronaut", "pilot", "cosmonaut"]):
        subjects.append("Astronaut helmet visor and upper torso")
    elif any(k in intent_lower for k in ["detective", "man", "warrior", "samurai", "character", "woman", "person"]):
        subjects.append("Primary subject eye-line plane and sagittal centerline")
    elif any(k in intent_lower for k in ["car", "vehicle", "ship", "craft"]):
        subjects.append("Vehicle center-chassis bounding box")
    else:
        subjects.append("Primary focal subject center of mass")

    if any(k in intent_lower for k in ["face", "eyes", "eye", "close"]):
        return f"Tight framing lock on {subjects[0]} (ocular axis tracking)"
    return f"Medium bounding-box lock on {subjects[0]} (continuous headroom retention)"


def detect_environmental_response(intent_lower: str) -> str:
    factors = []
    if any(k in intent_lower for k in ["rain", "rainy", "wet", "droplet"]):
        factors.append("dynamic lens droplet refraction and wet surface specular bounce")
    if any(k in intent_lower for k in ["neon", "glow", "cyber", "night"]):
        factors.append("volumetric neon glare streaking and edge rim highlight displacement")
    if any(k in intent_lower for k in ["dust", "sand", "smoke", "fog", "mist"]):
        factors.append("atmospheric depth falloff with particulate light scattering")
    if any(k in intent_lower for k in ["dusk", "sunset", "dawn", "sun"]):
        factors.append("golden-hour oblique shadow elongation and low-angle lens flare")

    if factors:
        return "Active environmental response: " + "; ".join(factors)
    return "Neutral studio-calibrated lighting response with minimal chromatic distortion"


def detect_parallax(mechanism: str, intent_lower: str) -> str:
    if mechanism == "orbit":
        return "Radial 360-degree parallax shift: rapid foreground angular displacement against fixed celestial/horizon anchor"
    if mechanism == "crane":
        return "Vertical planar parallax: progressive ground terrain compression with horizon elevation shift"
    if mechanism == "track":
        return "Lateral multi-plane shearing: foreground elements translate at 3x speed relative to background plate"
    if mechanism == "pan":
        return "Angular rotation parallax: static focal depth plane with zero translation baseline"
    return "Z-axis depth expansion: foreground occluder clearance with exponential scale expansion approaching lens"


def compile_contract(intent: str, mechanism: str = None) -> dict:
    intent_clean = intent.strip() if intent else SAMPLE_INTENT
    intent_lower = intent_clean.lower()

    mech = detect_mechanism(intent_lower, mechanism)
    mech_descriptions = {
        "dolly": "Mechanical dolly track along depth Z-axis (optical axis aligned)",
        "crane": "Vertical mechanical jib crane elevation with synchronized pitch damping",
        "orbit": "Radial orbital arm maintaining fixed radius trajectory around target pivot",
        "pan": "Tripod-mounted fluid head horizontal pan with zero translational baseline",
        "track": "Parallel lateral tracking rail alongside subject locomotion path",
    }

    contract = {
        "anchor_axis": "Origin (0, 0, 0) pinned to subject ground plane contact coordinate",
        "optical_mechanism": mech_descriptions[mech],
        "velocity_profile": detect_velocity(intent_lower),
        "subject_lock": detect_subject_lock(intent_lower),
        "parallax_mechanics": detect_parallax(mech, intent_lower),
        "environmental_response": detect_environmental_response(intent_lower),
        "terminal_landing": f"Stable terminal frame settle locked on {mech} terminal quadrant with depth-of-field freeze",
        "original_intent": intent_clean,
    }
    return contract


def main():
    args = parse_args()

    if args.sample:
        intent = SAMPLE_INTENT
    elif args.intent:
        intent = args.intent
    else:
        # If neither intent nor sample provided, print help or default to sample
        sys.stderr.write("Error: either --intent or --sample is required.\n")
        sys.exit(2)

    contract = compile_contract(intent, args.mechanism)

    if args.format == "json":
        print(json.dumps(contract, indent=2))
    else:
        print("### Compiled 7-Slot Camera Motion Contract\n")
        print(f"**Original Intent**: {contract['original_intent']}\n")
        print(f"- **[Anchor Axis]**: {contract['anchor_axis']}")
        print(f"- **[Optical Mechanism]**: {contract['optical_mechanism']}")
        print(f"- **[Velocity Profile]**: {contract['velocity_profile']}")
        print(f"- **[Subject Lock]**: {contract['subject_lock']}")
        print(f"- **[Parallax Mechanics]**: {contract['parallax_mechanics']}")
        print(f"- **[Environmental Response]**: {contract['environmental_response']}")
        print(f"- **[Terminal Landing]**: {contract['terminal_landing']}")


if __name__ == "__main__":
    main()
