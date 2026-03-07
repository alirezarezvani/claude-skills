---
name: competitive-matrix
description: Build competitive analysis matrices with scoring and gap analysis. Usage: /competitive-matrix <analyze> [options]
---

# /competitive-matrix

Build competitive matrices with weighted scoring, gap analysis, and market positioning insights.

## Usage

```
/competitive-matrix analyze <competitors.json>                    Full analysis
/competitive-matrix analyze <competitors.json> --weights pricing=2,ux=1.5    Custom weights
```

## Input Format

```json
{
  "your_product": { "name": "MyApp", "scores": {"ux": 8, "pricing": 7, "features": 9} },
  "competitors": [
    { "name": "Competitor A", "scores": {"ux": 7, "pricing": 9, "features": 6} }
  ],
  "dimensions": ["ux", "pricing", "features"]
}
```

## Examples

```
/competitive-matrix analyze competitors.json
/competitive-matrix analyze competitors.json --format json --output matrix.json
```

## Scripts
- `product-team/competitive-teardown/scripts/competitive_matrix_builder.py` — Matrix builder

## Skill Reference
→ `product-team/competitive-teardown/SKILL.md`
