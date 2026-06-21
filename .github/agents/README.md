# GitHub Copilot workspace agents

This folder is the GitHub Copilot counterpart to the repository's existing `.claude/` workspace customizations.

These files are **lightweight Copilot agents** for working on this repository as a workspace. They do not replace the real shipped agents under `agents/`; instead, they guide Copilot toward the existing source-of-truth files and patterns already used in the repo.

## Included agents

- `repo-maintainer.agent.md` — general repository changes across skills, commands, docs, and workspace config
- `skill-editor.agent.md` — focused changes inside skill packages
- `agent-builder.agent.md` — changes to `agents/**` and related orchestration docs

## Related workspace config

- `.github/copilot-instructions.md` — repo-wide Copilot instructions
- `.github/instructions/` — path-specific instructions
- `.github/prompts/` — reusable prompts
- `.vscode/mcp.json` — VS Code / GitHub Copilot MCP config
- `.claude/` — Claude Code workspace customizations
