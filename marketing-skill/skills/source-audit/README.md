# source-audit

Pre-publish source audit for drafts that cite links: check that each claim is actually supported by the source it points to.

## What it does

- Extracts every cited link with its paragraph context (`scripts/extract_claims.py`).
- Lists the checkable claims per link: versions, prices, licenses, platform support, feature lists.
- Fetches each source and quotes the passage that supports or contradicts the claim.
- Returns one verdict per claim: `supported`, `partial`, `contradicted`, `not-found`, `unreachable`, `opinion`.
- Writes `<draft>-audit.md` with a summary table, evidence quotes, and a fix list.

## Usage

```bash
python3 scripts/extract_claims.py draft.md --json -o claims.json
python3 scripts/extract_claims.py --sample --json
python3 scripts/extract_claims.py --selftest
python3 scripts/extract_claims.py --help
```

Exit codes: `0` links extracted, `1` no links found, `2` input error.

## Scope

It audits evidence, not prose. Copy-editing, structure, and tone belong to `copywriting`, `md-review`, or `research-summarizer`.

## License

MIT.
