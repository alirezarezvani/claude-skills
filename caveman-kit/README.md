# caveman-kit

Focused upstream import from:

- <https://github.com/JuliusBrussee/caveman>

This folder keeps the **useful token-saver parts** of the upstream `caveman` repo without pulling in its full benchmark, eval, and installer surface.

## Included

- `skills/caveman/` — core caveman mode
- `skills/caveman-compress/` — compress memory files to save input tokens
- `skills/caveman-stats/` — real session token receipts
- `skills/caveman-review/` — terse code review output
- `skills/caveman-commit/` — terse conventional commit generation
- `skills/caveman-help/` — quick reference
- `skills/cavecrew/` — delegation guide for compressed subagent output
- `agents/` — `cavecrew-builder`, `cavecrew-investigator`, `cavecrew-reviewer`
- `src/hooks/` — hook runtime used by caveman mode and stats
- `src/mcp-servers/caveman-shrink/` — MCP description-compression proxy
- `docs/assets/` — minimal assets referenced by included docs
- `README.upstream.md` and `INSTALL.upstream.md` — copied upstream docs for reference

## Why this folder exists

This repo already has its own native `engineering/caveman/` skill derived from Matt Pocock's original. `caveman-kit/` adds the **JuliusBrussee upstream extras** that are most useful for token reduction and caveman-style workflows.

## License

MIT. See `LICENSE` and `ATTRIBUTION.md`.
