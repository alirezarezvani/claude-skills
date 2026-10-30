# Rendered checks and the WCAG 2.2 criteria behind them

Every blocking check in `rendered_audit.py` maps to one WCAG 2.2 success
criterion. This file states the rule as the standard writes it, what the
script measures, and where measurement and conformance can disagree.

Confidence markers: 🟢 normative text of the standard · 🟡 W3C informative
guidance or a browser spec · 🔴 practitioner convention, not a requirement.

## The checks

| Code | Criterion | Level | Threshold the script uses |
|---|---|---|---|
| `TEXT_CONTRAST` | 1.4.3 Contrast (Minimum) | AA | 4.5:1, or 3:1 for large-scale text 🟢 |
| `NO_FOCUS_INDICATOR` | 2.4.7 Focus Visible | AA | any visible change on focus 🟢 |
| `FOCUS_OBSCURED` | 2.4.11 Focus Not Obscured (Minimum) | AA, new in 2.2 | focused control not *entirely* hidden by author content 🟢 |
| `REFLOW_SCROLL` | 1.4.10 Reflow | AA | no horizontal scroll at 320 CSS px wide 🟢 |
| `NO_ACCESSIBLE_NAME` | 4.1.2 Name, Role, Value | A | computed name not empty 🟢 |
| `TARGET_TOO_SMALL` | 2.5.8 Target Size (Minimum) | AA, new in 2.2 | 24×24 CSS px, or the spacing exception 🟢 |
| `NOT_KEYBOARD_REACHED` | 2.1.1 Keyboard | A | reached by a full Tab pass 🟢 (the Tab pass is a proxy 🟡) |

### Contrast (1.4.3)

- Large-scale text is at least 18 point, or 14 point bold. In CSS pixels that is
  24 px, or 18.66 px at weight 700 and above. The script uses those numbers. 🟢
- The ratio is `(L1 + 0.05) / (L2 + 0.05)` on relative luminance, with the
  sRGB linearisation in the WCAG definition. The script implements it exactly
  and reproduces the reference values: black on white is 21:1, and #767676 on
  white is 4.54:1. 🟢
- Disabled controls and pure decoration are exempt (the "incidental" exception). The
  script skips disabled controls. It cannot tell decoration from content, so
  waive decorative text with a reason. 🟢
- **Where measurement and conformance disagree.** Text on an image or gradient has
  no single background. The collector reports it as unknown, and the script
  warns (`CONTRAST_UNVERIFIED`) and does not guess. Check the lightest point
  under the text by hand. 🟡

### Focus visible and not obscured (2.4.7, 2.4.11)

- 2.4.7 asks for a visible indicator. It does not set a size or a contrast for
  it; those are in 2.4.13 Focus Appearance, which is AAA. The script blocks
  on *no* visible change. A faint ring passes the script but may fail a
  usability review. 🟢
- 2.4.11 fails only when the focused component is *entirely* hidden by
  author-created content, such as sticky headers, cookie banners or chat
  launchers. The collector samples the centre and corners of the focused box
  and reports obscured only when none of those points shows the element. 🟢
- Script focus (`el.focus()`) does not always match `:focus-visible`. The HTML
  focus-visible heuristics depend on how focus last moved. That is why
  `capture_snapshot.mjs` presses real Tab keys, and why console captures report
  `FOCUS_UNVERIFIED` rather than pass when they cannot tell. 🟡

### Reflow (1.4.10)

- Content must work at a width equal to 320 CSS px (1280 px at 400% zoom)
  without two-dimensional scrolling. Data tables, maps and diagrams are
  allowed to scroll. Waive those with a reason; do not widen the viewport to
  make the finding go away. 🟢
- At wider viewports, horizontal scroll is not a WCAG failure, so the script
  reports it as `PAGE_SCROLLS_X` (HIGH, a finish defect). 🔴

### Target size (2.5.8)

The normative exceptions, all of which the script models or lets you waive: 🟢

1. **Spacing**: undersized targets pass if a 24 px diameter circle centred on each
   target's bounding box intersects no other target and no other undersized target's
   circle. The script computes this from the rendered boxes.
2. **Equivalent**: another control on the same page does the same thing. Waive with the id of that control.
3. **Inline**: the target sits in a sentence or is constrained by line height. The
   collector flags links inside running text, and the script skips them.
4. **User agent control**: the size is the browser's default and the author did not change it.
5. **Essential**: the presentation is essential or legally required.

The 44×44 figure often quoted is 2.5.5 Target Size (Enhanced), AAA, and also
Apple's HIG minimum for touch. 2.5.8 at AA is 24×24. Do not block on 44. 🟢

## What the rendered pass cannot see

- Meaning: whether alt text is *right*, whether a label describes the field. Use
  `a11y-audit` and a human.
- Screen-reader announcements, live regions and the reading order inside complex widgets. Test those with a screen reader.
- States the page was not in when you captured it. Capture each state from
  `state_matrix_checker.py` that matters (empty, error, long content) as its
  own snapshot.

## Sources

1. W3C, *Web Content Accessibility Guidelines (WCAG) 2.2*, W3C Recommendation (5 Oct 2023, updated 12 Dec 2024). Normative text of 1.4.3, 1.4.10, 2.1.1, 2.4.7, 2.4.11, 2.5.8 and 4.1.2, and the definitions of *large scale*, *relative luminance* and *contrast ratio*. https://www.w3.org/TR/WCAG22/
2. W3C WAI, *Understanding SC 2.5.8 Target Size (Minimum)*: the spacing-circle method and its worked examples. https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
3. W3C WAI, *Understanding SC 2.4.11 Focus Not Obscured (Minimum)*: sticky content and the "entirely hidden" test. https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
4. W3C WAI, *Understanding SC 1.4.10 Reflow*: the 320 CSS px width and its exceptions for two-dimensional content. https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
5. WHATWG, *HTML Living Standard*, §6.6 Focus, and CSS Selectors Level 4 `:focus-visible`: when script focus should and should not show the indicator. https://html.spec.whatwg.org/multipage/interaction.html#focus and https://www.w3.org/TR/selectors-4/#the-focus-visible-pseudo
6. W3C, *Accessible Name and Description Computation 1.2*: the order the collector approximates (aria-labelledby, aria-label, label, content, title). https://www.w3.org/TR/accname-1.2/
7. Apple, *Human Interface Guidelines: Accessibility*: 44×44 pt touch minimum. This is the source of the AAA-sized number, which is not the AA rule. https://developer.apple.com/design/human-interface-guidelines/accessibility
