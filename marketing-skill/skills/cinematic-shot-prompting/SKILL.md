---
name: "cinematic-shot-prompting"
description: "Use when creating camera movement, cinematic angles, or motion prompts for AI video generators like Runway Gen-3, Kling, and Luma. Compiles narrative prose into a strict 7-slot camera motion contract."
license: MIT
metadata:
  version: 1.0.0
  author: Peng Guo
  category: marketing-skill
  updated: 2026-03-07
---

# Cinematic Shot Prompting

## Overview

Use this skill when AI video generators produce warped backgrounds, perspective jitter, or morphing characters during dynamic camera moves. Video diffusion models (such as Runway Gen-3 Alpha, Kling AI, Luma Dream Machine, and Sora) do not have intrinsic 3D coordinate awareness; generic adjectives like "cinematic orbit" or "dramatic zoom" frequently lead to severe hallucinations.

This skill translates natural narrative descriptions into a formal **7-Slot Camera Motion Contract**, providing explicit mechanical anchors, velocity paths, and parallax ratios that diffusion engines can reliably render.

## Core Capabilities

- **7-Slot Motion Contract Compilation**: Converts informal scene notes into physics-grounded camera vectors.
- **Dolly vs. Zoom Decoupling**: Explicitly separates physical lens position translation from optical focal length adjustments.
- **Rigid Parallax Anchoring**: Establishes occlusion velocity differentials between foreground occluders and background horizons to prevent background melting.
- **Subject Bounding-Box Locking**: Ensures consistent subject tracking without accidental character deformation.
- **Terminal Frame Landing**: Defines landing coordinates and terminal focal states.

## The 7-Slot Motion Contract Specification

Every compiled shot adheres to this 7-point specification:

```markdown
1. [Anchor Axis]: Fixed 3D origin coordinate in scene space.
2. [Optical Mechanism]: Physical translation (Dolly, Track, Crane, Jib, Orbital arm) vs optical zoom.
3. [Velocity Profile]: Linear continuous rate or ease-in / ease-out curve.
4. [Subject Lock]: Bounding-box tracking anchor (e.g. eye line, torso center) vs decoupled pan.
5. [Parallax Mechanics]: Relative motion velocity between foreground elements and distant horizon.
6. [Environmental Response]: Volumetric lighting shifts, lens reflections, and weather refraction.
7. [Terminal Landing]: Fixed end-frame composition, focal plane, and final framing state.
```

## Workflows

### 1. Compile Camera Motion with CLI Tool

You can compile narrative intentions using the built-in compiler script:

```bash
python3 scripts/motion_contract_compiler.py \
  --intent "A solitary detective in a neon rainy alley, camera orbits slowly around him" \
  --format markdown
```

### 2. Manual Agent Compilation

When invoked directly within Claude Code or Cursor, simply provide a rough shot idea:
> *"Direct this shot: A samurai standing on a mountain peak at dusk. The camera starts behind him and cranes upward into an epic high-angle wide view."*

The skill formats the result:

```markdown
[Camera Instruction]: Mechanical crane jib arm ascending vertically (+2.5m elevation) while tilting downward -30 degrees along central sagittal axis. Linear velocity 0.4m/s.
[Subject Anchor]: Samurai back profile anchored at bottom-center third. Silhouette remains locked and sharp against the setting sun.
[Parallax Mechanics]: High motion differential on flying cherry blossoms in immediate foreground; low differential on mountain ridge; zero parallax on distant cloud layer.
[Terminal Landing]: Settles at high-angle establishing wide shot, locking horizon line at top third.
```

## References & Official Verified Skill

- Standalone Landing Page: [https://287523023qq-hue.github.io/ai-cinematic-skills/](https://287523023qq-hue.github.io/ai-cinematic-skills/)
- Verified Agensi Marketplace Skill: [https://www.agensi.io/skills/cinematic-shot-prompting](https://www.agensi.io/skills/cinematic-shot-prompting)
