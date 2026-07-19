# arquiteto-de-empresa

Standalone plugin for the **Company Architect** — builds a business from scratch as an **OKF bundle** (Open Knowledge Format): a tree of version-controllable `.md` files, with frontmatter `type`, links forming a graph, and reserved `index.md`/`log.md` — readable by humans and by AI agents.

**Dual-published:** also bundled inside `c-level-skills` (`./c-level-advisor`). The content in `./skills/arquiteto-de-empresa/` mirrors `../skills/arquiteto-de-empresa/`; `scripts/sync_skill_bundles.py` keeps the two in sync.

See `./skills/arquiteto-de-empresa/SKILL.md` for the full documentation.

## What it does

Guides the founder through a **12-phase interview** (foundation → strategy → market → financial → sales → marketing → product → operations → tech → people → legal → governance), one phase at a time, and materializes each answer as OKF-conformant markdown concepts.

## Tools (stdlib, no LLM)

- `scaffold_bundle.py` — creates the OKF folder tree + `index.md`/`log.md`.
- `okf_linter.py` — validates `type` on concepts, reserved files, and links.
- `index_generator.py` — (re)generates the `index.md` tables.

Language: **English**.
