# Character Consistency Orthographic Specification

## Purpose

Generative image pipelines frequently drift in facial anatomy, clothing textures, and scale when prompting different views. This specification provides deterministic prompting anchors to ensure 100% visual continuity across game turnarounds and sprite extractions.

## 4-View Orthographic Plane

A complete game character sheet requires 4 locked perspectives arranged on a single high-resolution canvas (minimum 2048x2048):

1. **Front View (0° Yaw, 0° Pitch)**:
   - Symmetrical T-pose or relaxed A-pose.
   - Arms positioned away from torso to expose costume contour lines.
   - Neutral diffuse studio lighting without directional shadow bias.

2. **Three-Quarter View (45° Yaw, 0° Pitch)**:
   - Reveals facial depth, nose bridge, ear placement, and shoulder volume.
   - Confirms weapon holster or accessory placement on hips/back.

3. **Side Profile View (90° Yaw, 0° Pitch)**:
   - Locks cranial shape, silhouette thickness, footwear contours, and hair volume.
   - Essential for side-scroller sprite mapping and 3D modeling baseline reference.

4. **Rear View (180° Yaw, 0° Pitch)**:
   - Critical for third-person camera perspective.
   - Details backpack, cape, hair tie, spinal armor plates, and footwear heels.

## Anchor Rules for Prompt Generation

- **Geometric Lock**: Define anatomical proportions in fixed head units (e.g., "7.5 heads tall, broad athletic build").
- **Palette Lock**: Specify exactly 3 to 5 HEX color values directly in the prompt (e.g., primary tunic `#1a1a24`, cybernetic glow `#00e5ff`, metallic trim `#e0e0e0`).
- **Feature Consistency**: Name invariant signature markers (e.g., "scar across left eyebrow", "mechanical right arm with exposed piston").
- **Exclusion Clause**: Explicitly forbid camera focal length changes, fisheye distortion, and dynamic dramatic perspective tilt across the sheet.
