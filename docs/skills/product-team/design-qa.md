---
title: "Design QA — Agent Skill for Product Teams"
description: "Use when a UI screen, page or component is about to be called done, handed off or shipped, or when generated UI looks generic or half-finished. Gates. Agent skill for Claude Code, Codex CLI, Gemini CLI, OpenClaw."
---

# Design QA

<div class="page-meta" markdown>
<span class="meta-badge">:material-lightbulb-outline: Product</span>
<span class="meta-badge">:material-identifier: `design-qa`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/product-team/skills/design-qa/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install product-skills</code>
</div>


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

- [`references/rendered_checks_wcag22.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/skills/design-qa/references/rendered_checks_wcag22.md): each rendered check, its WCAG 2.2 criterion and exceptions (7 sources)
- [`references/interaction_states.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/skills/design-qa/references/interaction_states.md): required states per kind and what done looks like (7 sources)
- [`references/generic_ui_defaults.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/skills/design-qa/references/generic_ui_defaults.md): unfinished-work patterns and the template traits (6 sources)
- [`assets/collect_snapshot.js`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/skills/design-qa/assets/collect_snapshot.js), [`assets/capture_snapshot.mjs`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/skills/design-qa/assets/capture_snapshot.mjs): snapshot capture
- [`assets/states.example.csv`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/skills/design-qa/assets/states.example.csv), [`assets/snapshot.example.json`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/skills/design-qa/assets/snapshot.example.json), [`assets/waivers.example.csv`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/skills/design-qa/assets/waivers.example.csv): input formats
- [`assets/finish_signoff.md`](https://github.com/alirezarezvani/claude-skills/tree/main/product-team/skills/design-qa/assets/finish_signoff.md): sign-off before a screen is called done
