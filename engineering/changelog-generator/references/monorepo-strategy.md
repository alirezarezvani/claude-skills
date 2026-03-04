# Monorepo Strategy

## Approaches

- Single root changelog for product-wide releases
- Per-package changelogs for independent versioning
- Hybrid model: root summary + package-specific details

## Practical Pattern

- Enforce scoped commits: `feat(payments): ...`
- Filter commits by scope when generating package notes
- Keep shared infrastructure changes in root changelog
