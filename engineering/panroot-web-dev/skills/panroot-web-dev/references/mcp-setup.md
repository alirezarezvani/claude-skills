# MCP Setup Guide — Web Dev Tools

## Figma MCP
Install the Figma MCP to design on a live canvas from Claude:
```bash
# Via Claude Code plugin
/plugin install figma@claude-plugins-official

# Or via npx
npx figma-mcp
# Set: FIGMA_ACCESS_TOKEN in env
```
Capabilities: read/write Figma files, inspect components, export design tokens, pixel-level refinement.

## 21st.dev Magic MCP
Grab production-ready components (navbars, heroes, cards, forms) and adapt them:
```bash
npx @21st-dev/magic@latest init
# Set: TWENTY_FIRST_API_KEY=<your-key>
```
Add to `~/.claude/settings.json` under `mcpServers`:
```json
"21st-dev": {
  "command": "npx",
  "args": ["-y", "@21st-dev/magic@latest", "run"],
  "env": { "TWENTY_FIRST_API_KEY": "<your-key>" }
}
```

## paper.design MCP
Live design canvas — Claude designs visually, you see and manipulate in real time.
Configure via paper.design account settings → MCP integration → copy server URL + token.

## stitch MCP
Stitch design tool integration for component stitching and layout assembly.
Configure via stitch account → developer settings → MCP server config.

## Browser-Based Sourcing (No MCP Needed)
- **21st.dev** — `WebFetch` to browse component library
- **CodePen** — search for technique, rewrite clean in TypeScript
- **igloo.inc** — reference for glassmorphism dark premium aesthetic
- **Dribbble / Awwwards** — visual inspiration, never copy code
