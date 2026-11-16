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

Upgrade an **existing** README to the standard of the leading repos in its own ecosystem.

Core belief: polish is information hierarchy that survives a 15-second skim. Restraint is part of
the design — every component must earn its place.

## Overview

A README is not a brochure. It has three jobs, in order: state what the project is, prove why it
matters, and make the first command copy-pasteable. This skill audits the current README against
the conventions of its category, then rewrites it with only the components that carry real
information.

It is deliberately **not** a generator: no banner for a single-tool repo, no badge for a service
that does not exist, no screenshot placeholder.

## When to Use This Skill

- The user says the README is plain, ugly, outdated, or "needs a polish" (美化 / 升级 / 打磨).
- A README still describes an older version, or lists features that no longer match the code.
- The repo is about to be published and needs a credible front page.
- The user wants a comparison against top repos in the same ecosystem.
- The user wants a deterministic check for broken links, broken badges, or anchors.

Do **not** use it for a new README with no content (write content first), for hero/banner image
design, or for API reference documentation.

## Before Starting

Ask only what you cannot infer from the repo:

1. **Category**: single tool, library/framework, list/collection, or commercial product?
2. **Audience**: developers evaluating it, or users installing it?
3. **Evidence**: which claims are real today (version, license, test status, stars)?

If the user asks for a total rewrite but the README is already accurate and scannable, say so and
propose a smaller change. Polish is not a reason to churn good content.

## How This Skill Works

### Mode 1: Upgrade (default)

Use when the README needs a new structure or visual hierarchy. Run the full workflow below and
rewrite the file.

### Mode 2: Audit Only

Use when the user wants a review, not edits. Run the calibration, the 15-second test, the fact
audit, and the deterministic gate; report findings with file and line references. Do not rewrite.

### Mode 3: Calibrate

Use when the user is unsure what level of presentation fits. Sample 2-3 leading repos in the same
category, classify them (minimal vs full-component), and recommend a tier with reasons. Stop there
unless the user asks for the rewrite.

## Core Workflow

### Step 1: Calibrate against the ecosystem

Find 2-3 leading repos in the same category (same topic or toolchain), then classify them:

- **Minimal**: zero badges, typography and prose carry the confidence.
- **Full-component**: banner, badge wall, centered hero, sponsor tables.

Map the category to a tier:

| Repo type | Tier | Why |
|---|---|---|
| Single tool / skill | Middle: badges + mermaid + callouts | A banner reads as oversell |
| Collection / list | Full-component allowed | The front page is the product |
| Framework / methodology | Minimal or full | Minimal signals confidence |
| Commercial product | Full-component | Brand assets are real |

If the network or `gh` is unavailable, skip sampling, take the conservative default for the
category, and say "calibration skipped" in the report. Never claim calibration you did not do.

`gh` commands and the full mapping table: [references/archetypes.md](references/archetypes.md).

### Step 2: Run the 15-second test

All three must pass before rewriting:

1. The first screen states the value proposition in one sentence.
2. A copy-pasteable install command appears in the first 40 lines.
3. "What is it / why use it / how do I install it" are answered in the hero and the first three
   sections.

Record each failure as a work item.

### Step 3: Build the fact list

List every verifiable assertion in the current README: version numbers, license, test/coverage
claims, benchmark numbers, links, badges, screenshots. Mark each **true**, **stale**, or
**invented**.

Rules: keep true claims, update stale ones from the repository, delete invented ones. A dead badge
or a fake download count is worse than no badge.

### Step 4: Rewrite the hero and hierarchy

Write the new README in this order:

1. Centered hero: title, one-sentence value proposition, badge row, navigation links.
2. Quickstart: install + first command within the first screen.
3. Why it exists: a comparison table beats a list of adjectives.
4. How it works: a small mermaid diagram (seven nodes or fewer) or a short numbered flow.
5. Proof: a real example with real numbers from this repository.
6. Reference: commands, artifact layout, and long tables inside collapsible sections.
7. Limits: what the project does not do; this builds more trust than another feature list.

Use explicit anchors (`<a id="install"></a>`) before headings when the heading is non-ASCII or
contains emoji. Component syntax: [references/components.md](references/components.md).

### Step 5: Run the deterministic gate

```bash
python3 scripts/check_readme.py README.md
python3 scripts/check_readme.py --strict --json README.md
```

The gate checks dead local links, broken/placeholder badges, non-ASCII anchors, broken anchors,
oversized mermaid diagrams, wide tables, badge overload, and whether an install command appears in
the first screen. Exit codes: `0` clean, `1` warnings, `2` errors. Fix every error and justify each
remaining warning.

### Step 6: Human render check

Static checks cannot see rendering. Ask the user to open the README on the target platform and
confirm: mermaid renders, badges resolve, callouts render, anchors navigate, and tables survive a
narrow screen. Then rerun the 15-second test.

## Component Selection

| Component | Use when | Skip when |
|---|---|---|
| Badge row (six or fewer) | License, language/runtime, version, real status | The entity does not exist |
| Mermaid | Flow, funnel, decision path (seven nodes or fewer) | Full architecture panorama |
| Native callouts (`> [!NOTE]`) | Install note, real evidence, risk | Decoration |
| Collapsible `<details>` | Long command reference, artifact layout, FAQ | The core value |
| Comparison table | "Before vs after", "it is / it is not" | Prose would be shorter |
| Explicit anchors | Non-ASCII or emoji headings | Short English headings |
| Banner image | Collection or commercial repo with real assets | Single tool without design assets |
| Table of contents | README longer than about 300 lines | Short documents |

## Anti-Patterns

- **Banner on a single-tool repo.** It reads as compensating.
- **More than six badges**, or badges for things that do not exist.
- **Placeholder images or fake screenshots.** Remove them or ship a real one.
- **Mermaid with more than seven nodes.** The diagram stops being scannable.
- **Tables wider than five columns.** They break on a phone.
- **Anchors that rely on auto-generated slugs** for non-ASCII headings; they will be wrong.
- **Hiding the value proposition inside `<details>`.**
- **Rewriting a README that is already accurate and scannable.**
- **Keeping stale claims** (old version, removed feature) because they look impressive.

## Proactive Triggers

- The README's first screen has no install command.
- The version in the title or badges differs from `VERSION`, `package.json`, or the latest tag.
- The badge row contains a shields.io image not backed by a real entity.
- A mermaid block defines more nodes than the configured maximum.
- A relative link or image points to a file that no longer exists.
- The README contains a table with more than five columns.

## Output Artifacts

- A rewritten `README.md` (Mode 1), or a findings report with line references (Mode 2).
- A calibration note: sampled repos, archetype, chosen tier, and why.
- A fact list marking every claim true / stale / invented.
- The gate output: errors, warnings, and the exit code.
- A short list of items that still need human rendering checks.

## Related Skills

- `write-a-skill`: use when the user is authoring a new skill, not polishing docs; do not use for
  README structure.
- `code-tour`: use when the user wants a guided walkthrough of code; do not use for install docs.
- `commit-craft`: use when the change should become a clean commit or PR; do not use to decide
  content.

## Scripts

`scripts/check_readme.py` is a deterministic, stdlib-only gate (no network, no LLM):

```bash
python3 scripts/check_readme.py --help
python3 scripts/check_readme.py README.md
python3 scripts/check_readme.py --strict --json README.md
```

## Cross-References

- Ecosystem archetypes and calibration commands: [references/archetypes.md](references/archetypes.md)
- Component syntax and limits: [references/components.md](references/components.md)
- Audit and acceptance checklist: [references/checklist.md](references/checklist.md)
