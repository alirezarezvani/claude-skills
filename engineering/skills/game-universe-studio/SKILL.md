---
name: "game-universe-studio"
description: "Use when designing web games, interactive WebGL showcases, consistent game characters, 3D cutscenes, or Bento grid game cards. Unifies character consistency, 6-slot camera motion contracts, and web game matrix architecture."
license: MIT
metadata:
  version: 1.0.0
  author: Peng Guo
  category: engineering
  updated: 2026-11-14
---

# Game Universe Studio

## Overview

Use this skill when developing indie web games, interactive WebGL/Three.js game portfolios, or marketing game showcases. Standard generative AI tools produce disconnected one-off assets where characters drift, camera cutscenes jitter, and interactive browser deployment remains an unsolved manual hurdle.

Inspired by the live open-source web game portal at `gaoyaguo.eu.cc`, **Game Universe Studio** compiles loose game concepts into a production-grade 4-tier pipeline:
1. **Character Consistency**: 4-angle turnaround orthographic sheets and action sprite frames without facial morphing.
2. **Cinematic Cutscenes**: 6-slot camera motion contracts for 3D web camera sweeps, trailer sequences, and boss reveals.
3. **High-CTR Bento Cards**: High-contrast, responsive Bento grid game card compositions with retro-futuristic badges.
4. **Instant-Play Web Architecture**: Lightweight, modular browser game matrix supporting Three.js, Babylon.js, Canvas 2D, and procedural Web Audio synthesizers.

## Core Capabilities

- **4-Angle Character Ortho Generator**: Compiles front, 3/4 perspective, profile 90°, and rear views with locked anatomy, palette, and wardrobe.
- **6-Slot Camera Motion Compiler**: Formalizes Starting Anchor, Physical Mechanism, Path & Velocity, Subject Lock, Environment Response, and Ending Anchor for in-engine 3D sweeps and AI video trailers.
- **Bento Grid Showcase Layout**: Generates responsive, accessible HTML/Tailwind CSS components tailored for instant web game embedding.
- **Zero-Dependency Web Audio Synthesizer**: Embeds procedural audio routines for arcade button blips, hover cues, and ambient drones.
- **Narrative Story Route Choreography**: Bridges lore storytelling (`/story`) directly into active gameplay arenas.

## Pipeline Tiers

### Tier 1: Character Consistency Genesis
Lock character facial geometry, wardrobe, and species traits before generating turnarounds or sprites.
- Generate unified 4-view sheets with neutral studio lighting and consistent scale.
- Extract action keyframes: Idle (4 frames), Run/Dash (6 frames), Attack startup/active/recovery.

### Tier 2: Cinematic Cutscene Compilation
Formulate the 6-dimension camera contract:
- `[Anchor]`: Initial position, lens focal length, Dutch tilt.
- `[Mechanism]`: Camera apparatus (FPV drone, motorized orbit, Technocrane boom).
- `[Path & Velocity]`: Trajectory curve and acceleration profile.
- `[Subject Lock]`: Rigid point of focus throughout trajectory.
- `[Environment]`: Lighting flares, volumetric particles, atmospheric fog.
- `[Ending Anchor]`: Final framing landing directly into the playable game state.

### Tier 3: Bento Card & Visual Packaging
- Apply 60/30/10 focal hierarchy (character silhouette / environment / status badge).
- Implement high local contrast and complementary color pairs (Cyan/Amber, Purple/Neon Green).

### Tier 4: Interactive Web Showcase Architecture
- Integrate 2D Canvas and 3D WebGL runtimes inside isolated iframes or direct canvas mounts.
- Wire zero-dependency procedural Web Audio triggers on interactive events.

## Related Skills

- `cinematic-shot-prompting`: Dedicated camera motion contract compiler for video diffusion engines.
- `ad-creative`: High-converting marketing copy and banner creative generation.
