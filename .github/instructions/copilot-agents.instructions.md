---
applyTo: ".github/agents/**/*.agent.md"
---

Treat these files as GitHub Copilot custom agents for this repository.

- Keep them lightweight wrappers around the real repository structure; do not duplicate entire skills or agent catalogs into these files.
- Point Copilot at the existing sources of truth: `README.md`, `CLAUDE.md`, `agents/CLAUDE.md`, domain `CLAUDE.md` files, and the nearest skill or command docs.
- Prefer body instructions that explain when to use the agent, where to look first, what files to change, and how to validate the touched surface.
- Match the repository's real operating model: skills are self-contained packages, `cs-*` agents orchestrate skills, and `.claude/` remains the Claude-specific workspace layer.
- If a Copilot agent references MCP-backed capabilities, keep them aligned with `.vscode/mcp.json` and `.mcp.json`.
