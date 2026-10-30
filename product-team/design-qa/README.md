# design-qa

Gate a UI before it is called done. design-qa checks the build, not the design file.

Screens get reviewed as a populated, happy-path screenshot and ship with a
button wired to `() => {}`, "Lorem ipsum" in the empty state, no error state,
and a focus ring someone removed. design-qa finds those with three
deterministic scripts and separates what is **broken** (blocks) from what is
merely a **template default** (warns, because the brief may ask for it).

Built for the request in [issue #962](https://github.com/alirezarezvani/claude-skills/issues/962).
It is an independent implementation with no third-party code or service.

## What it checks

| Script | Input | Blocks on | Warns on |
|---|---|---|---|
| `finish_lint.py` | UI source (`.tsx .jsx .vue .svelte .html .css` …) | inert handlers, dead links, placeholder copy, focus outline removed with no replacement | buttons with no visible action, sample data, token drift, template traits (generic-risk rating) |
| `state_matrix_checker.py` | state matrix CSV | missing loading / empty / error / busy / failure / focus-visible / 320 px states | other missing states, DONE without evidence, NA without reason |
| `rendered_audit.py` | browser snapshot JSON | WCAG 2.2 AA: text contrast, no focus indicator, focus obscured, reflow at 320 px, empty accessible name, target under 24×24 | clipped text, controls not reached by Tab, contrast on gradients, unverified focus |

Snapshots come from `assets/collect_snapshot.js`, which is read-only and runs in
the DevTools console, or from `assets/capture_snapshot.mjs`, which uses your
project's Playwright and presses real Tab keys so focus results are proven.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install design-qa@claude-code-skills
```

It also ships inside the `product-skills` bundle.

## Quick start

```bash
cd skills/design-qa
python scripts/finish_lint.py --sample
python scripts/state_matrix_checker.py --sample
python scripts/rendered_audit.py --sample
```

On your app:

```bash
python scripts/finish_lint.py ../../my-app/src
python scripts/state_matrix_checker.py --matrix states.csv --evidence-root ../../my-app
node assets/capture_snapshot.mjs http://localhost:3000/invoices --width 320 --out s320.json
python scripts/rendered_audit.py --snapshot s320.json --waivers waivers.csv
```

Exit codes: `0` clean, `2` findings, `3` invalid input, `4` blocked. CI can fail on `4`.

## Commands and agent

- `/cs-design-qa <src> [url] [states.csv]` runs the full gate and answers DONE or NOT DONE.
- `/cs-ui-finish-lint <path>` runs the quick source lint.
- `cs-design-qa` is the QA lead persona. It asks for the empty state, the error state and the 320 px view first.

## Not covered

- Source accessibility (alt text, labels, ARIA, headings): use `a11y-audit`.
- Whether the design is *good*: template traits are flagged, not judged.
- Screen-reader behaviour: still a manual pass, listed in the sign-off.

## Requirements

Python 3.8+ (stdlib only). For the keyboard pass: Node 18+ and Playwright in the
project under test. Nothing is sent anywhere. The collector reads computed
styles and moves focus; it never clicks or types.

## License

MIT, part of [claude-skills](https://github.com/alirezarezvani/claude-skills).
