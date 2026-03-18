# WCAG Criteria Reference

## WCAG 2.2 Level A & AA Summary

WCAG 2.2 (W3C Recommendation, Dec 2024) builds on 2.1. Conformance to 2.2 satisfies 2.0 and 2.1.

### Perceivable
| SC | Level | Criterion |
|----|-------|-----------|
| 1.1.1 | A | Non-text content has a text alternative |
| 1.2.1 | A | Audio-only / video-only: provide transcript or audio description |
| 1.2.2 | A | Captions for prerecorded audio in video |
| 1.2.3 | A | Audio description or media alternative for prerecorded video |
| 1.2.4 | AA | Captions for live audio in video |
| 1.2.5 | AA | Audio description for prerecorded video |
| 1.3.1 | A | Info and relationships conveyed through structure (headings, lists, tables) |
| 1.3.2 | A | Meaningful sequence preserved when CSS removed |
| 1.3.3 | A | Sensory characteristics not sole means of conveying info |
| 1.3.4 | AA | Orientation: content not restricted to one display orientation |
| 1.3.5 | AA | Identify input purpose (autocomplete attributes) |
| 1.4.1 | A | Color not the only visual means of conveying info |
| 1.4.2 | A | Audio control: ability to pause/stop/mute auto-playing audio |
| 1.4.3 | AA | Contrast: 4.5:1 for normal text, 3:1 for large text |
| 1.4.4 | AA | Resize text: up to 200% without loss of content or function |
| 1.4.5 | AA | Images of text avoided where possible |
| 1.4.10 | AA | Reflow: content at 320px width without horizontal scroll |
| 1.4.11 | AA | Non-text contrast: UI components and graphics 3:1 |
| 1.4.12 | AA | Text spacing: no loss of content when line/letter/word spacing increased |
| 1.4.13 | AA | Content on hover/focus: dismissible, hoverable, persistent |

### Operable
| SC | Level | Criterion |
|----|-------|-----------|
| 2.1.1 | A | Keyboard: all functionality available via keyboard |
| 2.1.2 | A | No keyboard trap |
| 2.1.4 | A | Character key shortcuts: can be turned off or remapped |
| 2.2.1 | A | Timing adjustable: extend, turn off, or adjust time limits |
| 2.2.2 | A | Pause, stop, hide: moving/blinking/scrolling content controllable |
| 2.3.1 | A | Three flashes or below threshold: no content flashes >3/sec |
| 2.4.1 | A | Bypass blocks: skip navigation link |
| 2.4.2 | A | Page titled: descriptive `<title>` |
| 2.4.3 | A | Focus order: logical sequence |
| 2.4.4 | A | Link purpose: understandable from link text or context |
| 2.4.5 | AA | Multiple ways to find a page |
| 2.4.6 | AA | Headings and labels: descriptive |
| 2.4.7 | AA | Focus visible: keyboard focus indicator visible |
| 2.4.11 | AA | Focus not obscured (min): focused component not entirely hidden |
| 2.5.1 | A | Pointer gestures: all multi-point/path gestures have single-point alternative |
| 2.5.2 | A | Pointer cancellation: up-event for activation where possible |
| 2.5.3 | A | Label in name: accessible name contains visible label text |
| 2.5.4 | A | Motion actuation: no device-motion-only functions |
| 2.5.7 | AA | Dragging movements: alternative for all drag operations |
| 2.5.8 | AA | Target size (min): at least 24×24 CSS pixels |

### Understandable
| SC | Level | Criterion |
|----|-------|-----------|
| 3.1.1 | A | Language of page: `lang` attribute on `<html>` |
| 3.1.2 | AA | Language of parts: `lang` on elements in different language |
| 3.2.1 | A | On focus: no unexpected context change |
| 3.2.2 | A | On input: no unexpected context change |
| 3.2.3 | AA | Consistent navigation across pages |
| 3.2.4 | AA | Consistent identification of components |
| 3.3.1 | A | Error identification: text description of error |
| 3.3.2 | A | Labels or instructions for user input |
| 3.3.3 | AA | Error suggestion: suggest correction where possible |
| 3.3.4 | AA | Error prevention: reversible, checked, or confirmed for legal/financial |

### Robust
| SC | Level | Criterion |
|----|-------|-----------|
| 4.1.1 | A | Parsing: valid HTML (no duplicate IDs, properly nested) |
| 4.1.2 | A | Name, role, value: all UI components have accessible name/role/state |
| 4.1.3 | AA | Status messages: announced without receiving focus |

## Contrast Quick Reference

| Text Type | AA Minimum | AAA |
|-----------|-----------|-----|
| Normal text (<18pt, <14pt bold) | 4.5:1 | 7:1 |
| Large text (≥18pt or ≥14pt bold) | 3:1 | 4.5:1 |
| UI components, graphics | 3:1 | — |

**Calculate**: `(L1 + 0.05) / (L2 + 0.05)` where L1 is the lighter relative luminance.

Use the bundled `scripts/contrast_checker.py` to calculate from hex values.
