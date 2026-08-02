# Expected Changelog Output

## [2.3.0] - 2024-01-15

### Breaking Changes
- ui: redesign dashboard with new component library - The dashboard API endpoints have changed structure. Frontend clients must update to use the new /v2/dashboard endpoints. The legacy /v1/dashboard endpoints will be removed in version 3.0.0. (#345, #367, #389) [m1n2o3p]

### Added
- auth: add OAuth2 integration with Google and GitHub (#123, #145) [a1b2c3d]
- payment: add Stripe payment processor integration (#567) [g7h8i9j]
- search: implement fuzzy search with Elasticsearch (#789) [s7t8u9v]

### Fixed
- api: resolve race condition in user creation endpoint (#234) [e4f5g6h]
- db: optimize slow query in user search functionality (#456) [q4r5s6t]
- ui: resolve mobile navigation menu overflow issue (#678) [k1l2m3n]
- security: patch SQL injection vulnerability in reports [w1x2y3z] ⚠️ BREAKING

### Changed
- image: implement WebP compression reducing size by 40% [c4d5e6f]
- api: extract validation logic into reusable middleware [o4p5q6r]
- readme: update installation and deployment instructions [i7j8k9l]

# Release Summary
- **Version:** 2.3.0
- **Total Commits:** 13
- **Notable Changes:** 9
- **Breaking Changes:** 2
- **Issue References:** 8
- **By Type:**
  - feat: 4
  - fix: 4
  - perf: 1
  - refactor: 1
  - docs: 1
  - test: 1
  - chore: 1