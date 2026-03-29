# A11y Audit — WCAG 2.2 Accessibility Audit & Fix

Audit and fix WCAG 2.2 accessibility issues in any frontend project. Covers React, Next.js, Vue, Angular, Svelte, and plain HTML.

## Quick Start

```bash
# Scan a project
/a11y-audit ./src

# Or use the scripts directly
python3 scripts/a11y_scanner.py ./src
python3 scripts/contrast_checker.py "#1a1a2e" "#ffffff"
```

## Scripts

| Script | Purpose |
|--------|---------|
| `a11y_scanner.py` | Scan HTML/JSX/TSX/Vue/Svelte/CSS for 20+ a11y violations |
| `contrast_checker.py` | WCAG contrast ratio calculator with AA/AAA checks and `--suggest` mode |

Both are stdlib-only — no pip install needed. CI-friendly exit codes (0 = pass, 1 = blocking issues).

## What It Covers

- **Images**: missing alt, empty alt on informative images
- **Forms**: missing labels, orphan labels, missing fieldset/legend
- **Headings**: skipped levels, missing h1, multiple h1s
- **Landmarks**: missing main/nav/skip link
- **Keyboard**: tabindex > 0, click without keyboard handler
- **ARIA**: invalid attributes, aria-hidden on focusable, missing aria-live
- **Color**: contrast ratios below AA thresholds
- **Links**: empty links, "click here" text
- **Tables**: missing headers, missing caption
- **Media**: missing captions, autoplay without controls

## References

- `references/wcag-quick-ref.md` — WCAG 2.2 Level A/AA criteria table
- `references/aria-patterns.md` — ARIA roles, live regions, keyboard patterns
- `references/framework-a11y-patterns.md` — React, Vue, Angular, Svelte fix patterns

## License

MIT
