#!/usr/bin/env python3
"""
Motion Contract Compiler
Compiles natural narrative camera movements into a 7-Slot Camera Motion Contract.
Dependency-free (Python standard library only).
"""

import argparse
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Compile narrative camera movement into a 7-Slot Motion Contract."
    )
    parser.add_argument(
        "--intent",
        type=str,
        required=True,
        help="Natural language description of the camera movement.",
    )
    parser.add_argument(
        "--mechanism",
        type=str,
        default="dolly",
        choices=["dolly", "crane", "orbit", "pan", "track"],
        help="Primary camera mechanical translation type.",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="markdown",
        choices=["markdown", "json"],
        help="Output format (markdown or json).",
    )
    return parser.parse_args()


def compile_contract(intent: str, mechanism: str) -> dict:
    mech_map = {
        "dolly": "Mechanical dolly track along central depth Z-axis",
        "crane": "Vertical jib crane elevation arm",
        "orbit": "Radial orbital circular track (counter-clockwise arc)",
        "pan": "Horizontal fluid-head tripod pan",
        "track": "Lateral linear dolly tracking parallel to subject",
    }
    contract = {
        "anchor_axis": "Origin (0, 0, 0) relative to primary subject ground plane",
        "optical_mechanism": mech_map.get(mechanism, "Mechanical steady-cam track"),
        "velocity_profile": "Linear constant rate (0.4m/s) with 0.5s ease-out deceleration",
        "subject_lock": "Rigid center-frame bounding box locked on ocular plane",
        "parallax_mechanics": "Differential foreground motion with rigid background horizon anchor",
        "environmental_response": "Volumetric lighting response and atmospheric depth attenuation",
        "terminal_landing": "Fixed terminal framing with focal plane lock",
        "original_intent": intent,
    }
    return contract


def main():
    args = parse_args()
    contract = compile_contract(args.intent, args.mechanism)

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
