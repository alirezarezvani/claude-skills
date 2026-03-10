---
name: okr
description: Generate OKR cascades from company strategy to team objectives. Usage: /okr generate <strategy>
---

# /okr

Generate cascaded OKR frameworks from company-level strategy down to team-level key results.

## Usage

```
/okr generate <strategy>                                     Generate OKR cascade
```

Supported strategies: `growth`, `retention`, `revenue`, `innovation`

## Input Format

Pass a strategy keyword directly. The generator produces company, department, and team-level OKRs aligned to the chosen strategy.

## Examples

```
/okr generate growth
/okr generate retention
/okr generate revenue
/okr generate innovation
/okr generate growth --format json --output okrs.json
```

## Scripts
- `product-team/product-strategist/scripts/okr_cascade_generator.py` — OKR cascade generator

## Skill Reference
> `product-team/product-strategist/SKILL.md`
