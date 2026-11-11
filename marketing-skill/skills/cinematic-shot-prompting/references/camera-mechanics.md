# Cinematic Camera Mechanics Reference

## Theoretical Foundations

Camera movement in computer graphics and diffusion video generation relies on principles established in physical cinematography:

1. **American Cinematographer Manual (10th Edition)**, edited by Michael Goi, ASC.
   - Spatial translation along Cartesian coordinates (Dolly $Z$-axis, Truck $X$-axis, Boom/Pedestal $Y$-axis).
   - Angular rotation (Pan yaw, Tilt pitch, Roll barrel rotation).

2. **Cinematography: Theory and Practice (3rd Edition)**, Blain Brown.
   - Parallax dynamics: differential apparent velocity of objects based on inverse square distance from the focal center ($v_{\text{apparent}} \propto 1/d$).
   - Lens compression vs. physical translation: optical zoom changes field of view (FOV) without altering perspective convergence, whereas physical dolly alters convergence angles and relative depth relationships.

3. **Mechanical Damping & Acceleration Curves**:
   - Mechanical cranes and dollies operate with physical inertia, governed by ease-in and ease-out acceleration profiles ($\Delta v / \Delta t$).
   - Steadicam and 3-axis gimbal stabilization dampen high-frequency jitter while preserving low-frequency trajectory vectors.

## Diffusion Engine Mechanics Mapping

Generative video models (Runway Gen-3, Kling, Sora, Luma Dream Machine) do not utilize explicit 3D geometry meshes. They approximate 3D space by learning optical flow gradients across latent video tokens.

To prevent generative warping and morphing artifacts:
- **Anchor Point**: Must fix an unambiguous focal origin coordinate.
- **Velocity Thresholds**: Lateral translations exceeding 1.2 m/s trigger background latent shearing. Stable continuous rates range between 0.3 m/s and 0.8 m/s.
- **Parallax Anchoring**: Foreground occluders must have explicit spatial clearance from background horizon planes.
