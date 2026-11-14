# Character Consistency & Sprite Pipeline for Game Worlds

This module defines the process of locking game protagonists, bosses, and NPC characters into repeatable visual assets across 2D/3D styles.

---

## 1. Character Genesis & Identity Lock Contract

When prompting any generative model (Midjourney v6, Flux.1, DALL-E 3) for game characters, define an immutable Identity Anchor:

```text
[Subject Core]: [Species/Role], [Age/Gender], [Signature Facial Trait], [Signature Hair & Color]
[Wardrobe Lock]: [Primary Garment], [Signature Accessory/Weapon], [Accent Material], [Color Palette]
[Art Direction]: [Game Art Style, e.g., Unreal Engine 5 stylized PBR / Pixel art / Cel-shaded anime], [Even Studio Lighting, Neutral White Background]
```

### Example Identity Anchor:
```text
Cyberpunk bounty hunter, female late 20s, sharp angular jawline, heterochromia eyes (left cyan, right amber), undercut asymmetrical silver-violet hair, neon-trimmed carbon fiber jacket, holographic katana on hip, deep matte black and electric cyan palette, 3D stylized game asset render, Unreal Engine 5 character lighting, neutral grey backdrop.
```

---

## 2. Orthographic 4-Angle Turnaround Sheet

To hand off assets to 3D modellers or 2D sprite animators, generate a unified multi-angle turnaround:

```text
Prompt Template:
full body character turnaround sheet, multiple views of the same character on one canvas: front view, three-quarter view, 90-degree profile side view, and rear back view. [Insert Character Identity Anchor]. Character in neutral A-pose, consistent height and proportions, clean lines, no shadows on floor, studio character design sheet, game asset turnaround --ar 16:9
```

---

## 3. Sprite Sheet & Action Keyframe Synthesis

For 2D canvas games (like retro fighting games, platformers, or top-down shooters):
1. **Idle Stance**: 4-frame breathing/weight-shift cycle.
2. **Run/Dash**: 6-frame dynamic run cycle with trailing visual effects.
3. **Attack / Ability**: 4-frame startup, active hitbox frame, recovery frames.
4. **Hit React & Defeat**: Stagger, fall, and dissolution particles.
