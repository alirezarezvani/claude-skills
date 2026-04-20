# Code → PRD

Reverse-engineer any codebase into a complete Product Requirements Document (PRD).

## Quick Start

```bash
# One command
/code-to-prd /path/to/project

# Or step by step
python3 scripts/codebase_analyzer.py /path/to/project -o analysis.json
python3 scripts/prd_scaffolder.py analysis.json -o prd/ -n "My App"
```

## Supported Frameworks

| Stack | Frameworks |
|-------|-----------|
| Frontend | React, Vue, Angular, Svelte, Next.js, Nuxt, SvelteKit, Remix |
| Backend | NestJS, Express, Django, DRF, FastAPI, Flask |
| Fullstack | Next.js (pages + API), Nuxt (pages + server), Django (views + templates) |

## What It Generates

```
prd/
├── README.md                  # System overview
├── pages/
│   ├── 01-user-mgmt-list.md   # Per-page/endpoint docs
│   └── ...
└── appendix/
    ├── enum-dictionary.md      # All enums and status codes
    ├── api-inventory.md        # Complete API reference
    └── page-relationships.md   # Navigation and data coupling
```

## Scripts

| Script | Purpose |
|--------|---------|
| `codebase_analyzer.py` | Scan codebase → extract routes, APIs, models, enums |
| `prd_scaffolder.py` | Generate PRD directory skeleton from analysis JSON |

Both are stdlib-only — no pip install needed. Run `--help` for full usage.

## References

- `references/framework-patterns.md` — Route, state, API, form, and model patterns per framework
- `references/prd-quality-checklist.md` — Validation checklist for completeness and accuracy

## Attribution

Inspired by [code-to-prd](https://github.com/lihanglogan/code-to-prd) by [@lihanglogan](https://github.com/lihanglogan).

## License

MIT
