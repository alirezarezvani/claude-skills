# Audit and Acceptance Checklist

Use in Mode 1 before rewriting and in Mode 2 as the report skeleton.

## 15-second test

- [ ] One-sentence value proposition on the first screen.
- [ ] Copy-pasteable install command in the first 40 lines.
- [ ] "What is it / why use it / how to install" answered by the hero and the first three sections.

Any unchecked item is a work item.

## Fact audit

For every version number, license, test count, benchmark, link, badge, and screenshot:

- [ ] True — verified in the repository or a live URL.
- [ ] Stale — updated from the repository.
- [ ] Invented — deleted.

Never keep an impressive claim you cannot verify.

## Honesty checks

- [ ] No badge points to a non-existent service.
- [ ] No placeholder image or fake screenshot.
- [ ] No external link added that the project does not actually relate to.
- [ ] The limits section names what the project does **not** do.
- [ ] Claims about tests/coverage match a command the user can run.

## Structure checks

- [ ] Heading hierarchy is one H1, sections in reading order.
- [ ] Navigation links resolve; non-ASCII headings use explicit anchors.
- [ ] Long reference material is inside `<details>`, not in the main flow.
- [ ] Tables have five columns or fewer.
- [ ] Mermaid diagrams have seven nodes or fewer.

## Gate

- [ ] `python3 scripts/check_readme.py README.md` exits 0.
- [ ] `--strict` warnings are either fixed or justified in the report.
- [ ] `--json` output is attached when reporting to another agent.

## Render check (human)

- [ ] Mermaid renders on the target platform.
- [ ] Badges resolve.
- [ ] Callouts render.
- [ ] Anchors navigate.
- [ ] Tables survive a narrow screen.

## Final

- [ ] The README still fits the category tier (a single tool did not acquire a banner).
- [ ] The first command works as written.
- [ ] No sentence claims a feature the code does not have.

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
