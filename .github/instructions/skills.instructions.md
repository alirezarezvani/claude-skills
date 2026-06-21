---
applyTo: "engineering-team/**,engineering/**,product-team/**,marketing-skill/**,c-level-advisor/**,project-management/**,ra-qm-team/**,business-growth/**,business-operations/**,commercial/**,finance/**,research/**,research-ops/**,productivity/**,marketing/**,markdown-html/**,compliance-os/**"
---

These folders are the product surface of the repository: standalone skill packages, their tools, knowledge bases, templates, and plugin manifests.

- Preserve the skill package pattern: `SKILL.md` plus `scripts/`, `references/`, and `assets/` when those directories are present.
- Skills are portable packages. Avoid changes that make one skill depend on another skill at runtime.
- Prefer deterministic Python automation over LLM-dependent scripts. Keep skill scripts stdlib-only unless the skill already documents an allowed dependency.
- Reuse nearby file patterns before adding new structures, helper formats, or duplicate documentation.
- When editing `plugin.json`, keep to the approved schema used in this repo and keep `skills` paths relative to the plugin root with `./`-prefixed entries.
- When updating counts, examples, or install instructions, keep `README.md`, the relevant domain README or `CLAUDE.md`, and the changed skill in sync when the information is directly related.

If a task is only about one skill, make the smallest complete change inside that skill package instead of spreading the change across unrelated domains.
