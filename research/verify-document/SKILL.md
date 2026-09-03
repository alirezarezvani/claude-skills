---
name: verify-document
description: "Verify document authenticity before relying on extracted values. Detects tampering signals (amount/words mismatch, font discontinuity, date anomalies, identifier checksums) in PDFs and images. Use when reviewing research documents, contracts, financial records, client-provided evidence, or any document where authenticity matters. Related: litreview, deep-research, deepread, dossier."
license: Apache-2.0
metadata:
  version: 1.0.0
  author: Sketchjar
  category: research
  updated: 2026-08-31
---

# Verify Document

Forensic document authenticity check. Returns a risk band (low/medium/high), inspection quality (thorough/limited/poor), and per-signal evidence. Uses the Stipple API (free anonymous tier, no signup).

## When to Use

- Before relying on a document's extracted values in a research workflow
- Reviewing client-provided financial records (payslips, bank statements, invoices)
- Checking contracts or statutory documents for alterations
- Verifying exhibits or evidence before summarising
- Any workflow where a tampered document would poison downstream analysis

## What This Skill Does

1. **Forensic inspection**: Analyzes PDFs/images for tampering — amount/words mismatch, font discontinuity in values, date anomalies, document label integrity, identifier checksums (ABN/ACN/TFN), table arithmetic
2. **Two-axis assessment**: Returns `risk_band` (does anything look tampered?) and `inspection_quality` (could the engine see enough to judge?) — low coverage is explicitly NOT risk
3. **Evidence transparency**: Every signal carries its status (pass / warning / fail / skipped) and an explanation
4. **Content-addressable caching**: Identical files are cached by hash — re-checking the same document is free

## How to Use

### Verify a document

```bash
curl -X POST https://www.stipple.sh/v1/warrants \
  -F "file=@document.pdf"
```

### Deep inspection (more thorough)

```bash
curl -X POST "https://www.stipple.sh/v1/warrants?deep=true" \
  -F "file=@document.pdf"
```

### Re-check a cached document (force fresh inspection)

```bash
curl -X POST "https://www.stipple.sh/v1/warrants?fresh=true" \
  -F "file=@document.pdf"
```

## Example

**User**: "Verify this bank statement before we use it in the dossier."

**Output**:
```
risk_band:           LOW — Nothing looks tampered.
inspection_quality:  limited
recommended action:  review_before_action

evidence (signals):
  [pass] Amount words/figure mismatch: Spelled-out amounts agree with figures.
  [pass] Font discontinuity in value: Numeric values share the font of surrounding text.
  [pass] Date anomaly: Dates present are calendar-valid and consistently ordered.
  [skip] Identifier checksum: No checksummable identifier (ABN/ACN/TFN) present.
```

## Reading Results

| Axis | Question it answers |
|---|---|
| `risk_band` | Does anything look tampered? |
| `inspection_quality` | Could the engine actually see enough to judge? |

A clean phone photo of a real document is commonly `low` + `limited` — "nothing looks tampered, but we couldn't read everything." **Low coverage is not risk.**

## Tips

- Run this **before** `deepread` or `dossier` — a tampered document yields confidently wrong extracted values
- Pair with `source-locked-verification` for evidential fidelity across your document set
- Document types the engine recognizes (payslips, invoices, bank statements) get type-specific checks
- Re-checking the same document is free (cached by content hash)

## Common Use Cases

- Pre-litreview verification of source documents
- Due diligence document integrity checks
- Verifying client-provided financial records before research
- Screening exhibits before evidence extraction

## API

Uses the [Stipple API](https://www.stipple.sh) — free anonymous tier, no API key needed. For your own metering, get a free key at [stipple.sh](https://www.stipple.sh). See [stipple-kits](https://github.com/Sketchjar/stipple-kits) for integrations into doc7, docetl, chonkie, lift, and other tools.
