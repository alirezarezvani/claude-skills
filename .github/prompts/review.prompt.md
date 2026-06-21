---
description: Review a change in this repository using the existing local quality gates and conventions.
agent: agent
---

Review the current change set for this repository.

1. Read `.github/copilot-instructions.md`.
2. Read the nearest applicable file from `.github/instructions/`.
3. Use existing repository guidance such as `README.md`, `CLAUDE.md`, and `.claude/commands/review.md` when relevant.
4. Run only the checks that match the files being changed.
5. Summarize concrete issues, broken paths, missing documentation updates, and validation gaps before suggesting broad refactors.
6. Keep recommendations aligned with this repo's core rules: self-contained skills, cs-* agents orchestrate skills, and no unnecessary new dependencies.
