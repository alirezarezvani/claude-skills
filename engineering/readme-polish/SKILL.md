---
name: readme-polish
description: "Use when an existing README must be upgraded, audited, or made scannable: polish/美化/升级/优化/打磨 README, add badges, mermaid, callouts, or collapsible sections, compare against top repos in the same ecosystem, or fix a plain/ugly first screen. Calibrates to the repo's own category, rewrites the hero and information hierarchy, and enforces a deterministic lint gate. Not for brand-new READMEs from scratch or hero-image design."
license: MIT
metadata:
  version: 1.0.0
  author: zhengqiuyang
  category: engineering
  updated: 2026-11-16
---

# README Polish

Upgrade an **existing** README to the standard of the leading repos in its own ecosystem. Polish is
information hierarchy that survives a 15-second skim; every component must earn its place. This is
not a generator: no banner for a single-tool repo, no badge for a service that does not exist, no
screenshot placeholder.

Do not use it for a README with no content yet, for hero or banner image design, or for API
reference docs. If the README is already accurate and scannable, say so and propose a smaller change.

## Before starting

Ask only what the repo cannot tell you: the category (single tool, library or framework, collection,
commercial product), the audience (evaluating developers or installing users), and which claims are
true today (version, license, test status).

## Modes

- **Upgrade** (default): run the full workflow and rewrite the file.
- **Audit only**: run steps 1-3 and 5, report findings with line references, do not rewrite.
- **Calibrate**: run step 1 only and recommend a presentation tier with reasons.

## Workflow

1. **Calibrate.** Sample 2-3 leading repos in the same category and classify them as minimal or
   full-component. Single tools get the middle tier (badges, mermaid, callouts); collections and
   commercial products may use full components. If the network or `gh` is unavailable, take the
   conservative default and write "calibration skipped". Never claim calibration you did not do.
   Mapping and `gh` commands: [references/archetypes.md](references/archetypes.md).
2. **Run the 15-second test.** The first screen states the value in one sentence, a copy-pasteable
   install command sits in the first 40 lines, and the hero plus three sections answer what, why
   and how to install. Each failure is a work item.
3. **Build the fact list.** Mark every version, license, test claim, benchmark, link, badge and
   screenshot as true, stale or invented. Keep true ones, update stale ones from the repo, delete
   invented ones. A dead badge is worse than no badge.
4. **Rewrite in this order:** hero (title, one-sentence value, badge row, nav links), quickstart,
   why it exists (a comparison table beats adjectives), how it works (mermaid of seven nodes or
   fewer), proof with real numbers from this repo, reference material in `<details>`, and limits.
   Put explicit anchors (`<a id="install"></a>`) before non-ASCII or emoji headings. Component
   choice, anti-patterns and syntax: [references/components.md](references/components.md).
5. **Run the gate.** Fix every error and justify each remaining warning.
6. **Ask for a render check.** Static checks cannot see rendering: the user confirms on the target
   platform that mermaid, badges, callouts, anchors and tables render, then rerun step 2.

## Example

```bash
python3 scripts/check_readme.py README.md
python3 scripts/check_readme.py --strict --json README.md
python3 scripts/check_readme.py --sample
```

The stdlib-only gate (no network) flags dead local links, broken or placeholder badges, non-ASCII
and broken anchors, mermaid diagrams over the node limit, tables wider than five columns, more than
six badges, and a first screen with no install command. Exit codes: `0` clean, `1` warnings, `2`
errors.

## Output

A rewritten `README.md` (or a findings report in audit mode), the calibration note, the fact list,
the gate output, and the items still awaiting a human render check. Acceptance checklist and
proactive triggers: [references/checklist.md](references/checklist.md).

## Related skills

- `write-a-skill`: authoring a new skill, not polishing docs.
- `code-tour`: a guided walkthrough of code, not install docs.
- `commit-craft`: turning the change into a clean commit or PR.
