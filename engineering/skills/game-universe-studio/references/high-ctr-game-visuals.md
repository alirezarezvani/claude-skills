# High-CTR Game Cards & Visual Identity Packaging

This module translates game mechanics and thematic lore into high-converting Bento grid thumbnails, store covers, and social media key art.

---

## 1. Visual Composition Rules for Game Cards

To achieve high click-through rates (CTR) on game aggregation platforms, app stores, and Bento grids:

1. **The 3-Second Focal Hierarchy**:
   - **Dominant Element (60%)**: Hero character silhouette or dynamic vehicle action breaking the frame.
   - **Environment Context (30%)**: Vibrant background world (neon city, ancient temple, cosmic arena).
   - **Badge & Title Clarity (10%)**: High-contrast typography and platform tags (`3D`, `PVP`, `NEW`).

2. **Lighting & Palette Chemistry**:
   - High local contrast (deep shadows vs. intense neon highlights).
   - Complementary color clashes (Cyan / Amber, Purple / Acid Green, Crimson / Ice Blue).
   - Micro-rim highlights on character edges to pop out against dark backgrounds.

---

## 2. Bento Card Prompt Template

```text
Game cover art thumbnail, Bento card asset for web game showcase. Dynamic low-angle perspective of [Hero/Vehicle/Boss action]. Vivid neon cyberpunk and fantasy game aesthetics, volumetric lighting, particle embers, dynamic motion blur on edges, cinematic composition. Unreal Engine 5 render, raytraced reflections, highly detailed 8k texture, clean focal hierarchy, dark atmospheric vignette border --ar 16:9
```

---

## 3. Web UI Component Integration

- **Badge Pill**: `bg-cyan-500/10 text-cyan-400 border border-cyan-500/30 text-xs font-mono uppercase px-2 py-0.5 rounded-full`
- **Glow Hover Effect**: `hover:shadow-[0_0_25px_rgba(6,182,212,0.25)] hover:border-cyan-400/60 transition-all duration-300`
- **Card Media Container**: `aspect-[16/10] overflow-hidden rounded-xl bg-zinc-950 relative`
