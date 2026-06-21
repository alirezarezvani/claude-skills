---
applyTo: "agents/**/*.md"
---

Treat `agents/**/*.md` as first-class agent definitions for this repository.

- Standard task agents use the `cs-` prefix and keep YAML frontmatter with `name`, `description`, `skills`, `domain`, `model`, and `tools`.
- Agents orchestrate existing skills. Reference skill files and Python tools with repository-relative `../../` paths from the agent file instead of copying large parts of the skill into the agent.
- Keep the documented section structure from `agents/CLAUDE.md`: purpose, skill integration, workflows, integration examples, success metrics, related agents, and references.
- Document at least 3 workflows for task agents: primary, advanced, and integration use cases.
- Prefer concrete commands and real relative paths in examples.
- When you change paths to scripts, references, or assets, update the examples in the agent so they still resolve.

Persona files under `agents/personas/` are the exception:

- Preserve persona-style frontmatter such as `name`, `description`, `color`, `emoji`, `vibe`, and `tools`.
- Preserve the persona section flow: identity, mission, rules, capabilities, workflows, communication style, metrics, advanced capabilities, and learning.
- Keep personas role-shaped and cross-domain; do not rewrite them into ordinary task agents.
