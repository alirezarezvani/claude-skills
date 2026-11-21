# Zero-Dependency Web Audio Synth Primitives

## Architecture

Modern web games often fail to ship with responsive audio due to large asset download sizes, CORS loading issues, or missing sound files. The Web Audio API allows instant, zero-asset sound synthesis directly through procedural code.

## Core Oscillator Recipes

### 1. Arcade Jump / Blip (Frequency Sweep)
```javascript
function playArcadeBlip(ctx = new (window.AudioContext || window.webkitAudioContext)()) {
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = 'square';
  osc.frequency.setValueAtTime(440, ctx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.08);
  gain.gain.setValueAtTime(0.15, ctx.currentTime);
  gain.gain.linearRampToValueAtTime(0.01, ctx.currentTime + 0.08);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start();
  osc.stop(ctx.currentTime + 0.08);
}
```

### 2. Hit / Explosion (Noise & Low Sawtooth)
```javascript
function playHitSound(ctx) {
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = 'sawtooth';
  osc.frequency.setValueAtTime(150, ctx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(30, ctx.currentTime + 0.15);
  gain.gain.setValueAtTime(0.3, ctx.currentTime);
  gain.gain.linearRampToValueAtTime(0.01, ctx.currentTime + 0.15);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start();
  osc.stop(ctx.currentTime + 0.15);
}
```

### 3. Laser Slash / Whoosh
```javascript
function playLaserSlash(ctx) {
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.type = 'sawtooth';
  osc.frequency.setValueAtTime(900, ctx.currentTime);
  osc.frequency.exponentialRampToValueAtTime(180, ctx.currentTime + 0.12);
  gain.gain.setValueAtTime(0.2, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
  osc.connect(gain);
  gain.connect(ctx.destination);
  osc.start();
  osc.stop(ctx.currentTime + 0.12);
}
```

## Production Guidelines

- Always resume the `AudioContext` on the first user interaction (`click`, `keydown`, or `touchstart`) to satisfy browser autoplay policies.
- Clamp master gain below `0.4` to prevent clipping and protect user hearing across different headphones and laptop speakers.
