# Beat timing: where the numbers come from

| Number | Used for | Source | Confidence |
|---|---|---|---|
| 160-180 words per minute | upper bound for on-screen text a viewer can read | Ofcom subtitle guidance as cited by BBC R&D, J. Sandford, "How fast should subtitles be?", 11 Sep 2015 | 🟢 |
| ~175 wpm "about right" | BBC R&D viewer study, 24 clips at 90-230 wpm; hearing and hearing-impaired viewers rated alike | same BBC R&D post | 🟢 |
| 3.0 words/s + 0.5 s | reading time per on-screen line in this tool (180 wpm plus a glance-in) | derived from the two rows above | 🟡 design choice |
| 150 wpm (2.5 words/s) | narration pace for voice-over fit | common broadcast narration pace, slower than the reading ceiling so VO and text do not race | 🟡 design choice |
| 1.5 s floor | shortest beat | below about a second a beat registers as a flash cut; also keeps ML9 quiet | 🟡 design choice |

## How the tool fits beats to the brief

1. Each beat needs `max(1.5 s, VO words ÷ 2.5 + 0.3, 0.8 + text words ÷ 3)`,
   plus 1.6 s when it carries a number or chart that animates.
2. If the sum exceeds the brief by more than 0.25 s, it refuses and names the
   words to cut (over-seconds × 2.5). The length belongs to the brief, so the
   script changes, not the brief.
3. Otherwise slack is spread in proportion to each beat's need, snapped to the
   frame grid, and the last beat absorbs rounding so the total is exact.

## Sources

- BBC R&D, J. Sandford, "How fast should subtitles be?" (2015): bbc.co.uk/rd/blog/2015-09-how-fast-should-subtitles-be
- W3C, WCAG 2.2, SC 1.4.3 Contrast (Minimum) and SC 2.3.1 Three Flashes: w3.org/TR/WCAG22/
- Thomas, F. & Johnston, O., *The Illusion of Life: Disney Animation* (1981): timing and staging principles
- Pixar in a Box, "The art of storytelling", Khan Academy: story beats and reels
- AES TD1008 (2021) via productionadvice.co.uk/td1008/: speech loudness for streamed content (used later in conform)
