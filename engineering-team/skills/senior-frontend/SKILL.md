---
name: "senior-frontend"
description: "Build and review React, Next.js, TypeScript or Tailwind frontends: components, scaffolding, performance and bundle size. Use whenever the user wants a new component or app, a page feels slow, the bundle is too big, or asks for a frontend code review."
---

# Senior Frontend

Frontend development patterns, performance optimization, and automation tools for React/Next.js applications.

## Table of Contents

- [Project Scaffolding](#project-scaffolding)
- [Component Generation](#component-generation)
- [Bundle Analysis](#bundle-analysis)
- [React Patterns](#react-patterns)
- [Next.js Optimization](#nextjs-optimization)
- [Accessibility and Testing](#accessibility-and-testing)

---

## Project Scaffolding

Generate a new Next.js or React project with TypeScript, Tailwind CSS, and best practice configurations.

### Workflow: Create New Frontend Project

1. Run the scaffolder with your project name and template:
   ```bash
   python scripts/frontend_scaffolder.py my-app --template nextjs
   ```

2. Add optional features (auth, api, forms, testing, storybook):
   ```bash
   python scripts/frontend_scaffolder.py dashboard --template nextjs --features auth,api
   ```

3. Navigate to the project and install dependencies:
   ```bash
   cd my-app && npm install
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

### Scaffolder Options

| Option | Description |
|--------|-------------|
| `--template nextjs` | Next.js 14+ with App Router and Server Components |
| `--template react` | React + Vite with TypeScript |
| `--features auth` | Add NextAuth.js authentication |
| `--features api` | Add React Query + API client |
| `--features forms` | Add React Hook Form + Zod validation |
| `--features testing` | Add Vitest + Testing Library |
| `--dry-run` | Preview files without creating them |

### Generated outputs

The generated project structure and an example component are in `references/frontend_best_practices.md` (section Generated outputs).

---

## Component Generation

Generate React components with TypeScript, tests, and Storybook stories.

### Workflow: Create a New Component

1. Generate a client component:
   ```bash
   python scripts/component_generator.py Button --dir src/components/ui
   ```

2. Generate a server component:
   ```bash
   python scripts/component_generator.py ProductCard --type server
   ```

3. Generate with test and story files:
   ```bash
   python scripts/component_generator.py UserProfile --with-test --with-story
   ```

4. Generate a custom hook:
   ```bash
   python scripts/component_generator.py FormValidation --type hook
   ```

### Generator Options

| Option | Description |
|--------|-------------|
| `--type client` | Client component with 'use client' (default) |
| `--type server` | Async server component |
| `--type hook` | Custom React hook |
| `--with-test` | Include test file |
| `--with-story` | Include Storybook story |
| `--flat` | Create in output dir without subdirectory |
| `--dry-run` | Preview without creating files |

---

## Bundle Analysis

Analyze package.json and project structure for bundle optimization opportunities.

### Workflow: Optimize Bundle Size

1. Run the analyzer on your project:
   ```bash
   python scripts/bundle_analyzer.py /path/to/project
   ```

2. Review the health score and issues:
   ```
   Bundle Health Score: 75/100 (C)

   HEAVY DEPENDENCIES:
     moment (290KB)
       Alternative: date-fns (12KB) or dayjs (2KB)

     lodash (71KB)
       Alternative: lodash-es with tree-shaking
   ```

3. Apply the recommended fixes by replacing heavy dependencies.

4. Re-run with verbose mode to check import patterns:
   ```bash
   python scripts/bundle_analyzer.py . --verbose
   ```

### Bundle Score Interpretation

| Score | Grade | Action |
|-------|-------|--------|
| 90-100 | A | Bundle is well-optimized |
| 80-89 | B | Minor optimizations available |
| 70-79 | C | Replace heavy dependencies |
| 60-69 | D | Multiple issues need attention |
| 0-59 | F | Critical bundle size problems |

### Heavy Dependencies Detected

The analyzer identifies these common heavy packages:

| Package | Size | Alternative |
|---------|------|-------------|
| moment | 290KB | date-fns (12KB) or dayjs (2KB) |
| lodash | 71KB | lodash-es with tree-shaking |
| axios | 14KB | Native fetch or ky (3KB) |
| jquery | 87KB | Native DOM APIs |
| @mui/material | Large | shadcn/ui or Radix UI |

---

---

## React Patterns

Compound components, custom hooks and render props are in `references/react_patterns.md` (section Examples).

---

## Next.js Optimization

Server vs Client Components, image optimization and data fetching examples are in `references/nextjs_optimization_guide.md` (section Examples).

---

## Accessibility and Testing

Code examples for accessibility and testing are in `references/frontend_best_practices.md`.

### Accessibility Checklist

1. **Semantic HTML**: Use proper elements (`<button>`, `<nav>`, `<main>`)
2. **Keyboard Navigation**: All interactive elements focusable
3. **ARIA Labels**: Provide labels for icons and complex widgets
4. **Color Contrast**: Minimum 4.5:1 for normal text
5. **Focus Indicators**: Visible focus states

---

## Quick Reference

Config, Tailwind and TypeScript snippets are in `references/frontend_best_practices.md` (section Quick reference).

---

## Resources

- React Patterns: `references/react_patterns.md`
- Next.js Optimization: `references/nextjs_optimization_guide.md`
- Best Practices: `references/frontend_best_practices.md`
- Forcing-question library (Matt Pocock grill): `references/forcing_questions.md`
- Composition map (which specialist to fork into): `references/composition_map.md`

---


## Assumptions and Verifiable Success Criteria (Karpathy discipline)

Before this skill scaffolds a component, recommends a framework, or audits a bundle, the following four assumptions MUST be surfaced.

1. **Primary user device + network** — mobile-4G, desktop-fiber, low-end-Android, or corporate-network. Drives every perf decision.
2. **LCP target in milliseconds** — a single number, not "fast." Drives bundle budget and rendering choice.
3. **SEO-dependent vs. auth-walled** — drives rendering (SSR/SSG/RSC vs. SPA).
4. **WCAG target + named a11y owner** — AA, AAA, or best-effort. Drives a11y investment and CI gates.

**Verifiable success criteria** (Karpathy #4) — every recommendation must include:

- Core Web Vitals targets (LCP, INP, CLS) at p75 on the primary device
- A per-route JS bundle budget in KB-gzip
- A Lighthouse a11y floor + perf floor

If any of those three is not stated, the recommendation is incomplete — return to Q2 of the forcing-question library.

The `scripts/frontend_decision_engine.py` tool encodes these checks: it refuses to recommend a profile without the four assumption inputs and prints the verifiable thresholds for the matched profile.

---


## Customization profiles

Four built-in profiles in `profiles/` calibrate every recommendation:

| Profile | When to pick | LCP target (mobile-4G p75) | Bundle budget |
|---|---|---|---|
| `next-app-router` | SaaS customer-facing, SEO + dynamic, RSC-first | 2000ms | 150 KB-gzip / route |
| `remix-or-sveltekit` | Mobile-4G primary, low-JS-first, progressive enhancement | 1500ms | 80 KB-gzip / route |
| `vite-spa` | Auth-walled app, desktop/corporate primary | 2500ms | 200 KB init + 80 KB / route |
| `astro-or-static` | Marketing / docs / blog, near-zero write, SEO-critical | 1200ms | 30 KB JS / page |

Pick a profile via:

```bash
python scripts/frontend_decision_engine.py \
  --primary-device mobile-4g --lcp-target-ms 2000 \
  --seo-dependent true --auth-walled false --team-size 5
```

The tool returns the best-fit profile, the runner-up tradeoff (if within 15%), the stack picks, the anti-patterns to avoid on that profile, and the required CI gates.

To add a custom profile (e.g., your org's internal-tool defaults): copy `profiles/vite-spa.json` to `profiles/<your-org>.json` and adjust `constraints` + `success_thresholds`.

---


## Composition map

This skill does NOT reimplement scope owned by the POWERFUL-tier specialists. It forks into them. See `references/composition_map.md` for the full routing table. Key forks:

| Concern | Fork into |
|---|---|
| WCAG audit, contrast, screen-reader | `engineering-team/skills/a11y-audit/` |
| Bundle profiling + runtime perf | `engineering/skills/performance-profiler/` |
| Cinematic / scroll-storytelling landing | `engineering-team/skills/epic-design/` |
| Apple HIG (iOS / macOS / visionOS) | `product-team/skills/apple-hig-expert/` |
| Pre-commit Karpathy review | `engineering/karpathy-coder/` |
| Pre-flight architecture grill | `engineering/grill-me/` |

The `cs-frontend-engineer` agent orchestrates these forks via `context: fork`. Invoke it from another agent with `Agent({subagent_type: "cs-frontend-engineer", prompt: "..."})` or via `/cs-frontend-review <your problem>`.

---


## Forcing-question library (Matt Pocock grill)

Before locking a framework or rendering decision, walk the seven forcing questions in `references/forcing_questions.md`: one question per turn, cite the canon for each recommended answer, and stop when a kill criterion trips. After Q7, run `frontend_decision_engine.py` with the answers.

1. Primary device + network?
2. LCP target in ms (and INP, CLS)?
3. RSC / SPA / SSR / SSG — pick and defend?
4. JS bundle budget per route?
5. SEO-dependent or auth-walled?
6. Design-system source of truth?
7. WCAG target + named a11y owner?

---


## Invocation from other agents and skills

Three surfaces:

1. **Slash command:** `/cs-frontend-review <prompt>` — full grill + decision engine + composition routing.
2. **Agent subagent:** `Agent({subagent_type: "cs-frontend-engineer", prompt: "..."})` — forks context, returns ≤ 200-word digest.
3. **Direct tool call:** `python scripts/frontend_decision_engine.py ...` — deterministic profile match when inputs are known.

See `agents/engineering/cs-frontend-engineer.md` for the full invocation contract.
