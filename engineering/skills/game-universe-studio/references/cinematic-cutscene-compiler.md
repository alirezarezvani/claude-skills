# Cinematic Cutscene & 3D Camera Motion Compiler

This module compiles cinematic camera motion prompts for game trailers, 3D character select screens, boss encounter cutscenes, and immersive web transitions.

---

## 1. The 6-Dimensional Motion Contract

Every video generation prompt (for Kling 1.5, Runway Gen-3, Luma Dream Machine, Sora) must specify all 6 physical camera dimensions:

| Dimension | Role | Examples |
| :--- | :--- | :--- |
| **1. Starting Anchor (起点)** | Initial position, focal length, angle | Low-angle ground level 24mm wide, Dutch angle tilt 15°, extreme close-up eye reflection |
| **2. Physical Mechanism (机制)** | Camera apparatus or flight mode | FPV acrobatic drone, 50-foot Technocrane, circular orbit gimbal, Steadicam run |
| **3. Path & Velocity (路径与加减速)** | Trajectory curve and acceleration curve | Rapid acceleration into logarithmic deceleration, corkscrew helical spiral, supersonic linear dolly |
| **4. Subject Lock (主体锁定)** | Exact focus target during movement | Locked to character's glowing eyes, fixed to racing vehicle exhaust, pinned to boss hammer |
| **5. Environment Response (环境响应)** | Dynamic lighting & particle interactions | Lens flare passing streetlights, volumetric steam displacement, mud splashes hitting lens |
| **6. Ending Anchor (落点)** | Final framing transitioning to next state | Over-the-shoulder third-person gameplay view, wide arena establishing shot |

---

## 2. Standard Cutscene Patterns for Web Games

### Pattern A: 3D Character Select Orbit
```text
[Anchor]: Eye-level medium close-up, 50mm portrait lens, centering on character face.
[Mechanism]: Smooth motorized 360-degree orbital rig.
[Path & Velocity]: Steady constant-speed clockwise sweep around the character.
[Subject Lock]: Locked to protagonist's chest and eyes as character idly adjusts weapon.
[Environment]: Studio rim lighting rimming character edges, floating cybernetic dust motes.
[Ending Anchor]: Settles at three-quarter hero pose, camera gently drifts back to full body.
```

### Pattern B: Boss Battle Encounter Reveal (e.g. Tiger Vanguard / 虎先锋)
```text
[Anchor]: Low ground-level Dutch angle looking up from blood pool, wide 18mm lens.
[Mechanism]: High-speed Technocrane booming up and pushing forward.
[Path & Velocity]: Explosive rapid upward surge, pausing abruptly at eye-level with the boss.
[Subject Lock]: Locked onto the massive fangs and blazing red eyes of the armored tiger boss.
[Environment]: Heavy volumetric blood mist parting, crimson water droplets flying towards camera.
[Ending Anchor]: Extreme wide arena establishing shot, boss roaring as combat HUD elements flick on.
```

### Pattern C: Racing Track Flythrough (e.g. QQ Speed 3D)
```text
[Anchor]: 2 inches above asphalt behind rear spoiler, wide-angle lens with asphalt blur.
[Mechanism]: FPV chase drone skimming track surface.
[Path & Velocity]: Extreme acceleration through hairpin neon turn, bank tilt 45 degrees.
[Subject Lock]: Tightly tracking the twin nitro exhaust plumes emitting cyan flame bursts.
[Environment]: Neon billboards reflecting on wet rain tarmac, lens flare streaks.
[Ending Anchor]: Ascends vertically into bird's-eye isometric track view, countdown timer ready.
```
