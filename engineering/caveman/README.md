# caveman

Ultra-compressed communication mode. Cuts token usage ~75% by dropping filler, articles, and pleasantries while keeping full technical accuracy.

## Attribution

**Derived from [Matt Pocock's caveman](https://github.com/mattpocock/skills/tree/main/skills/productivity/caveman)** (MIT). Matt's SKILL.md voice + activation triggers + persistence rules preserved verbatim per his MIT license.

## What this adds on top of Matt's original

| Addition | Where | Why |
|---|---|---|
| **3 stdlib Python tools** | `skills/caveman/scripts/` | Compressor (apply Matt's rules deterministically), token-savings estimator (measure %), lint (verify response follows rules) |
| **3 in-depth references** (5+ sources each) | `skills/caveman/references/` | Compression principles · Technical communication patterns · When caveman backfires (the auto-clarity exceptions, deepened) |
| **cs-caveman-mode persona agent** | `agents/cs-caveman-mode.md` | Persistent caveman-mode operator with hard rules for technical-content exceptions |
| **`/cs:caveman` slash command** | `commands/cs-caveman.md` | One-line trigger + persistence enforcer |

## Quick start

```bash
# Compress text per Matt's rules
python skills/caveman/scripts/caveman_compressor.py "Sure! I'd be happy to help you with that. The issue is..."

# Estimate token savings on a piece of text
python skills/caveman/scripts/token_savings_estimator.py "input text"

# Lint a response to check caveman compliance
python skills/caveman/scripts/caveman_lint.py "response text"
```

All three tools run with embedded samples if no input provided.

## License

MIT (matching Matt's upstream).
