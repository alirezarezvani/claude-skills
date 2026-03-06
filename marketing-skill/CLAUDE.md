# Marketing Skills — Agent Instructions

## For All Agents (Claude Code, Codex CLI, OpenClaw)

This directory contains 42 marketing skills organized into specialist pods.

### How to Use

1. **Start with routing:** Read `marketing-ops/SKILL.md` — it has a routing matrix that maps user requests to the right skill.
2. **Check context:** If `marketing-context.md` exists, read it first. It has brand voice, personas, and competitive landscape.
3. **Load ONE skill:** Read only the specialist SKILL.md you need. Never bulk-load.

### Skill Map

- `marketing-context/` — Run first to capture brand context
- `marketing-ops/` — Router (read this to know where to go)
- `content-production/` — Write content (blog posts, articles, guides)
- `content-strategy/` — Plan what content to create
- `ai-seo/` — Optimize for AI search engines (ChatGPT, Perplexity, Google AI)
- `seo-audit/` — Traditional SEO audit
- `page-cro/` — Conversion rate optimization
- `pricing-strategy/` — Pricing and packaging
- `content-humanizer/` — Fix AI-sounding content

### Python Tools

27 scripts, all stdlib-only. Run directly:
```bash
python3 <skill>/scripts/<tool>.py [args]
```
No pip install needed. Scripts include embedded samples for demo mode (run with no args).

### Anti-Patterns

❌ Don't read all 42 SKILL.md files
❌ Don't skip marketing-context.md if it exists
❌ Don't use content-creator (deprecated → use content-production)
❌ Don't install pip packages for Python tools
