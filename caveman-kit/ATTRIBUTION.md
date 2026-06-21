# Attribution

This folder vendors a focused subset of:

- Source: <https://github.com/JuliusBrussee/caveman>
- Upstream author: Julius Brussee
- License: MIT (`LICENSE` copied into this folder)

## Included subset

- `skills/caveman/`
- `skills/caveman-compress/`
- `skills/caveman-stats/`
- `skills/caveman-review/`
- `skills/caveman-commit/`
- `skills/caveman-help/`
- `skills/cavecrew/`
- `agents/`
- `src/hooks/`
- `src/mcp-servers/caveman-shrink/`
- `docs/assets/`
- upstream `README.md` as `README.upstream.md`
- upstream `INSTALL.md` as `INSTALL.upstream.md`

## Intentionally omitted

This import does not vendor the entire upstream repository. It omits broader repo plumbing and evaluation surfaces that are not required for the core token-saver functionality bundled here, such as:

- benchmark harnesses
- eval suites
- test suites
- distribution bundles
- installer entrypoints outside the included hook/runtime files
- unrelated repository metadata

The goal is to keep the useful caveman token-saving components available locally while preserving attribution and license terms.
