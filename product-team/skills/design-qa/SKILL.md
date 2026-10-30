---
name: design-qa
description: Use when a UI screen, page or component is about to be called done, handed off or shipped, or when generated UI looks generic or half-finished. Gates the rendered result, not the design file - finds controls that do nothing, placeholder copy, removed focus rings, missing loading/empty/error states, low contrast, small targets, hidden focus and broken reflow measured in the real browser, and flags template defaults without blocking on taste.
argument-hint: "[UI source path | state matrix CSV | rendered snapshot JSON | URL to capture]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three deterministic stdlib scripts (source finish lint, interaction-state matrix, rendered snapshot audit) with blocking exit codes, plus a read-only browser collector and an optional Playwright keyboard pass; WCAG 2.2 AA thresholds for contrast, focus, reflow, names and target size; template traits from Anthropic's frontend-design skill as warnings only"
  distinct_from: "a11y-audit (source-level WCAG scan: alt text, labels, ARIA, headings); ui-design-system (generates tokens and components); ux-researcher-designer (research); epic-design and frontend-design (make the design, this checks the build)"
---

# Design QA

> **Portability:** 3 stdlib Python scripts, no network. The browser collector is
> plain JavaScript; the keyboard pass needs Playwright in your own project.
> **This checks the build, not the taste.** Objective defects block; template
> defaults only warn, because the brief may ask for them.

Screens get reviewed in a static, populated, happy-path frame and ship with a
button wired to `() => {}`, an empty state that says "Lorem ipsum", and a focus
ring someone removed. Each script catches one class of these before a user does.

## Workflow

```bash
# 1 - Source: is anything unfinished in the code?
python scripts/finish_lint.py src/ --output json > lint.json
# 2 - States: does every surface have loading, empty, error, busy, focus...?
python scripts/state_matrix_checker.py --matrix states.csv --evidence-root .
# 3 - Rendered: what did the browser actually show? (capture 320 px and desktop)
node assets/capture_snapshot.mjs http://localhost:3000/invoices --width 320 --out s320.json
python scripts/rendered_audit.py --snapshot s320.json --waivers waivers.csv
```

**Step 1** blocks on inert handlers, dead links, placeholder copy and focus
outlines removed without a replacement. It warns on sample data, token drift and
each template trait it finds, and rates generic risk LOW, MEDIUM or HIGH.

**Step 2** derives required states from each surface's kind (`data_view`,
`form`, `action`, `control`, `media`, `page`). An unlisted state counts as
missing, and DONE without evidence is reported. Start from `assets/states.example.csv`.

**Step 3** reads a snapshot of the rendered page and blocks on WCAG 2.2 AA
failures: text contrast, no focus indicator, focus obscured, reflow at 320 px,
empty accessible names and targets under 24×24 px without the spacing exception.
Contrast is composited through translucent layers and `opacity`, so a token that
passes on white but fails inside a tinted card is caught. Repeated rows are grouped.
No Playwright? Paste `assets/collect_snapshot.js` into the DevTools console and
run `copy(JSON.stringify(designQaSnapshot()))`. Focus results are then
unverified rather than passed.

Capture one snapshot per key state (empty, error, long content), not just the
populated page. Fill `assets/finish_signoff.md` from the three runs.

## Hard rules

- **Unlisted is missing.** A state nobody wrote down was not built.
- **Measure the render, not the CSS.** Contrast on a real background beats a declared colour pair.
- **Never block on taste.** Template traits warn. Record in the sign-off whether the brief asks for the look.
- **A waiver names the WCAG exception or a ticket.** The scripts reject a waiver or NA with no reason.
- **Unverified is not pass.** Text on a gradient or focus from script focus is checked by hand or with the keyboard pass.
- **Not an accessibility conformance claim.** The checks cover what can be measured. A screen-reader pass and `a11y-audit` cover the rest.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/finish_lint.py` | Inert controls, dead links, placeholder copy, removed focus, template traits, token drift | 0 clean · 2 findings · 3 bad input · 4 blocked |
| `scripts/state_matrix_checker.py` | Required states per surface kind, evidence and NA reasons | 0 complete · 2 · 3 · 4 blocked |
| `scripts/rendered_audit.py` | Contrast, focus, target size, names, clipping, reflow from a snapshot | 0 clean · 2 · 3 · 4 blocked |

All support `--help`, `--sample` and `--output json`.

## References and assets

- [`references/rendered_checks_wcag22.md`](references/rendered_checks_wcag22.md): each rendered check, its WCAG 2.2 criterion and exceptions (7 sources)
- [`references/interaction_states.md`](references/interaction_states.md): required states per kind and what done looks like (7 sources)
- [`references/generic_ui_defaults.md`](references/generic_ui_defaults.md): unfinished-work patterns and the template traits (6 sources)
- [`assets/collect_snapshot.js`](assets/collect_snapshot.js), [`assets/capture_snapshot.mjs`](assets/capture_snapshot.mjs): snapshot capture
- [`assets/states.example.csv`](assets/states.example.csv), [`assets/snapshot.example.json`](assets/snapshot.example.json), [`assets/waivers.example.csv`](assets/waivers.example.csv): input formats
- [`assets/finish_signoff.md`](assets/finish_signoff.md): sign-off before a screen is called done
