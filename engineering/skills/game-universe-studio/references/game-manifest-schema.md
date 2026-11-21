# Game Manifest Schema Specification

## Overview

The Game Asset Manifest formalizes the interface between visual generative assets, character consistency turnarounds, and web browser runtime execution. It standardizes viewport bounds, character orthographic sheets, animation loops, and audio triggers into a verifiable JSON contract.

## Schema Fields

### 1. Root Properties
- `game_id` (string, required): Unique kebab-case identifier for the game prototype.
- `title` (string, required): Human-readable game title.
- `version` (string, semver): Semantic version string (e.g., `1.0.0`).
- `engine` (string, required): One of `canvas2d`, `webgl`, `threejs`, `babylon`, `pixijs`.
- `viewport` (object, required): Viewport geometry:
  - `width` (int): Base render target width.
  - `height` (int): Base render target height.
  - `aspect_ratio` (string): Standard display ratio (`16:9`, `4:3`, `1:1`).
  - `canvas_id` (string, optional): Target DOM canvas element ID.

### 2. Character Specification
- `id` (string, required): Identifier for the primary character/avatar.
- `turnaround_views` (array of string): Must include standard views `["front", "three_quarter", "profile", "back"]`.
- `sheet_dimensions` (object): Width and height of the combined orthographic turnaround sheet.
- `palette_locks` (array of string): 3 to 6 primary HEX color codes defining the locked wardrobe and skin tones to prevent color drift across frames.

### 3. Sprite Matrix
Array of animation definitions:
- `action` (string): State name (`idle`, `run`, `jump`, `attack`, `steer`).
- `frames` (int): Number of consecutive animation keyframes.
- `fps` (int): Target playback frame rate.
- `tile_size` (array of 2 ints): `[width, height]` in pixels per frame.

### 4. Audio Cues
Array of procedural zero-dependency Web Audio synthesizers:
- `name` (string): Trigger name invoked by game events.
- `type` (string): Web Audio oscillator waveform (`sine`, `square`, `sawtooth`, `triangle`).
- `freq_start` (number): Starting frequency in Hz, 20 to 20,000.
- `freq_end` (number): Ending frequency in Hz (for pitch sweeps), 20 to 20,000.
- `duration_ms` (number): Tone duration in milliseconds.
- `gain` (number): Peak amplitude in (0, 1]. Values above 0.4 raise a warning (see `web-audio-synth-primitives.md`).

### 5. Bento Card Presentation
Metadata for catalog showcase rendering:
- `badge` (string): Genre tag or badge label (e.g., `Arcade`, `WebGL 3D`, `Action RPG`).
- `contrast_ratio` (number): WCAG compliant contrast ratio against dark theme background (minimum 4.5).
- `theme_accent` (string): HEX color used for borders, glows, and CTA accents.
