# Ecosystem Archetypes

Two archetypes cover almost every healthy README. Classify before writing; the category decides
the tier, not personal taste.

## Minimal

Characteristics: no badges, no images, typography and short prose carry the confidence. Common in
methodologies, frameworks, and tools whose audience already trusts the author.

Signal: the README answers "what is it" in one line and "why this one" in one paragraph.

## Full-component

Characteristics: banner or hero image, centered title, badge wall, sponsor or community section,
screenshots, long feature catalogue. Common in collections, commercial products, and
list-style repositories where the front page is the product.

Signal: the page is browsed, not read; the visuals carry real information.

## Mapping

| Repo type | Tier | Notes |
|---|---|---|
| Single tool / skill | Middle | Badges + one mermaid + callouts; no banner |
| Collection / list | Full-component | Banner earns its place |
| Framework / methodology | Minimal or full | Minimal signals confidence |
| Commercial product | Full-component | Brand assets are real |

## Calibration commands

```bash
# Leading repos in the same topic, by stars
gh api "search/repositories?q=topic:<topic>&sort=stars&per_page=10" \
  --jq '.items[] | "\(.full_name) | \(.stargazers_count) | \(.pushed_at[:10])"'

# Read two or three of them
gh api repos/<owner>/<repo>/readme -H "Accept: application/vnd.github.raw"
```

If `gh` is unavailable, offline, or the category is too small, skip sampling and take the
conservative default: a single tool gets the middle tier. Say "calibration skipped" in the report.

## Tier boundaries

Middle tier may include: badge row (six or fewer), one mermaid diagram, native callouts, a
comparison table, collapsible reference sections, explicit anchors.

Middle tier does **not** include: banner images, sponsor tables, badge walls, animated demos,
centered marketing headlines.
