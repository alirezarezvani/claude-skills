---
name: "game-universe-studio"
description: "Build web game prototypes, character turnaround sheets, procedural Web Audio effects, and Bento showcase card layouts. Validates asset manifests against browser runtime contracts."
---

# Game Universe Studio

## Overview

Use this skill when architecting lightweight web games, interactive WebGL/Canvas prototypes, consistent game character turnaround sheets, or responsive game portfolio showcases.

The skill provides an industrial 3-tier pipeline paired with a deterministic manifest validator to guarantee that assets match modular browser runtime requirements:
1. **Character Consistency**: 4-angle turnaround orthographic sheets (Front, 3/4, Profile, Back) with locked anatomical proportions and HEX palette anchors.
2. **Procedural Web Audio**: Zero-asset synthesis routines (blip, jump, hit, slash) using Web Audio API oscillators to avoid sound loading overhead.
3. **Bento Card Packaging**: High-contrast showcase cards with status tags and responsive canvas viewport mounts.
4. **Manifest Verification**: An integrated stdlib tool (`scripts/game_manifest_validator.py`) to validate game configs, tile dimensions, and audio frequencies before deployment.

## Core Capabilities

- **4-View Orthographic Turnarounds**: Compiles prompts for front, 3/4 angle, 90° profile, and rear views on unified canvas layouts.
- **Zero-Dependency Audio Synthesizers**: Generates procedural Web Audio sound functions without external MP3/WAV file downloads.
- **Bento Grid Showcase Layouts**: Emits semantic HTML/Tailwind CSS components tailored for instant web game embedding.
- **Manifest Contract Validation**: Verifies complete game packages via CLI against standard asset contracts.

## Workflow

### Step 1: Character Turnaround Sheet Generation
Define the character anchor profile before generating animation sprites:
- Specify anatomical scale (e.g. `7.5 heads tall, athletic silhouette`).
- Lock 3-5 key HEX palette colors (e.g. primary armor `#1a1a24`, glow accent `#00e5ff`).
- Arrange into 4 orthogonal views: Front, 3/4 perspective, Side profile, and Rear.
- Reference: `references/character-ortho-spec.md`.

### Step 2: Procedural Audio & Runtime Mount
- Implement browser-native Web Audio oscillators for immediate player feedback (jump, hit, pickup, laser).
- Ensure AudioContext resumes upon first user interaction to comply with browser autoplay constraints.
- Reference: `references/web-audio-synth-primitives.md`.

### Step 3: Compile & Validate Game Manifest
Bundle game metadata, viewport settings, character locks, and audio parameters into a single manifest:
```bash
python3 engineering/skills/game-universe-studio/scripts/game_manifest_validator.py \
  --manifest engineering/skills/game-universe-studio/examples/indie-game-showcase-manifest.json
```
To run the built-in self-check fixture:
```bash
python3 engineering/skills/game-universe-studio/scripts/game_manifest_validator.py --sample --format json
```

## Manifest Schema Reference

See `references/game-manifest-schema.md` for full field specifications and validation rules.
