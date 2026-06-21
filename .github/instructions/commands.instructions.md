---
applyTo: "commands/**/*.md,.claude/commands/**/*.md"
---

Treat these files as reusable command definitions, not general prose documentation.

- Preserve YAML frontmatter at the top of each command file.
- `commands/` holds repository-shipped slash commands; `.claude/commands/` holds Claude workspace commands used when this repo itself is the workspace.
- Keep the body action-oriented: purpose, usage, examples, referenced scripts, and workflow steps.
- Prefer pointing to existing scripts, skills, checks, or files instead of embedding large duplicate procedures.
- If a workflow exists in both `commands/` and `.claude/commands/`, keep the intent aligned unless the difference is explicitly tool-specific.
- When a command references file paths or scripts, update those references in the same change if you move or rename the targets.
