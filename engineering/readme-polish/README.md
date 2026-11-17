# readme-polish

Upgrade an existing README to the visual and structural standard of the leading repos in its own
ecosystem: archetype calibration, component selection, restraint boundaries, honesty rules, and a
deterministic lint gate.

## Quickstart

```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills
python3 engineering/readme-polish/scripts/check_readme.py README.md
```

## What it does

- Classifies the repository's category (single tool, framework, collection, commercial) by sampling
  leading repos in the same topic, then picks a presentation tier with reasons.
- Runs a 15-second scannability test on the current README and records each failure as a work item.
- Builds a fact list (true / stale / invented) so the rewrite cannot keep dead badges, old versions,
  or invented metrics.
- Rewrites the hero, quickstart, proof, reference, and limits sections with only components that
  carry information.
- Ships `scripts/check_readme.py`, a stdlib-only gate for dead links, broken or placeholder badges,
  non-ASCII anchors, oversized mermaid diagrams, wide tables, badge overload, and install-command
  placement.

## Usage

```bash
python3 scripts/check_readme.py README.md
python3 scripts/check_readme.py --strict --json README.md
python3 scripts/check_readme.py --help
```

Exit codes: `0` clean, `1` warnings, `2` errors.

## Modes

- **Upgrade** — full audit and rewrite.
- **Audit only** — findings report with line references, no edits.
- **Calibrate** — sample the ecosystem and recommend a tier.

## Limits

Static checks cannot see rendering and cannot judge whether a component is warranted. The human
render check and the fact audit remain manual by design.

## License

MIT.
