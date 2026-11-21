# Motion craft: timing, easing, accessibility, rendering

## Principles the engine encodes

| Principle | In the engine | Source | Confidence |
|---|---|---|---|
| Slow in and slow out | default `expo-out` for entrances, `ease-in-out` for camera | Thomas & Johnston, *The Illusion of Life* (1981), the 12 principles | 🟢 |
| Staging: one idea per shot | linter pacing warnings, one hero layer per beat in beat_board output | same | 🟢 |
| Short UI-scale motion | entrances 0.6-0.7 s, exits 0.3 s | Material Design 3, motion: easing and duration (m3.material.io/styles/motion) | 🟡 scaled up for video |
| No more than 3 flashes per second | ML4 blocks | WCAG 2.2 SC 2.3.1 (w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold) | 🟢 |
| Text contrast at least 4.5:1 | ML5 blocks on flat backgrounds | WCAG 2.2 SC 1.4.3 | 🟢 |
| Respect reduced motion in previews | the preview hides autoplay under `prefers-reduced-motion` | WCAG 2.2 SC 2.3.3 (AAA), MDN `prefers-reduced-motion` | 🟢 |

ML4 approximates WCAG 2.3.1 from shot background luminance (changes of 10% or
more of relative luminance where the darker side is under 0.80). It cannot see
flashes inside images or plates; check those on the rendered file.

## Why a seekable page instead of CSS animations

CSS and JS animations run on the browser's clock, so a screenshot taken "at
2 s" lands wherever the clock happens to be. `window.__seek(t)` computes every
property from `t` alone, so the renderer can ask for t = N / fps and get the
same frame every time. The same approach underlies HyperFrames and Remotion,
which both render by stepping a deterministic timeline in headless Chrome.

## Safe areas

ML8 keeps text 5% inside each edge. For 9:16 it also keeps clear of the top
12% and bottom 20%, where platform UI (captions, buttons, account names) sits.
These margins are working defaults, not a published standard; platforms move
their UI, so check a real upload.

## Sources

- Thomas, F. & Johnston, O., *The Illusion of Life: Disney Animation*, Abbeville Press, 1981
- Material Design 3, Motion: m3.material.io/styles/motion/overview
- W3C, WCAG 2.2: w3.org/TR/WCAG22/ (SC 1.4.3, 2.3.1, 2.3.3)
- MDN Web Docs, `prefers-reduced-motion`: developer.mozilla.org/docs/Web/CSS/@media/prefers-reduced-motion
- Playwright, `page.screenshot` and `page.evaluate`: playwright.dev/docs/screenshots
- HyperFrames, github.com/heygen-com/hyperframes (deterministic HTML-to-video rendering)
- Remotion, remotion.dev/docs (frame-based React video rendering)
