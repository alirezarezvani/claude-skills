---
title: "/cs-frontend-review — Slash Command for AI Coding Agents"
description: "Frontend engineering review — walks the 7 Matt Pocock forcing questions (device, LCP target, rendering, bundle budget, SEO vs auth, design system. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-frontend-review

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/cs-frontend-review.md">Source</a></span>
</div>


Use the `cs-frontend-engineer` agent (uses `context: fork`) to handle this inquiry:

**$ARGUMENTS**

## Forcing-question library

Canonical source: `engineering-team/skills/senior-frontend/references/forcing_questions.md` (7 questions, one-per-turn, recommendation + canon citation per question).

1. Primary device + network (desktop-fiber / mobile-4G / low-end Android / corporate)
2. LCP target on primary device (milliseconds)
3. Server Components vs SPA vs SSR vs SSG
4. JS bundle budget per route (KB gzipped)
5. SEO-dependent or auth-walled
6. Design-system location (Figma + tokens / ad-hoc Tailwind / headless UI)
7. WCAG target (AA / AAA / best-effort) + accessibility owner

## Routing protocol

1. **Walk the 7 forcing questions** in `engineering-team/skills/senior-frontend/references/forcing_questions.md`. One per turn. Recommend with cited canon. Track in `/tmp/frontend-grill-<date>.md`.
2. **Surface kill criteria** — e.g., "SEO-dependent + SPA-only" trips. STOP and resolve.
3. **Run the deterministic profile picker:**
   ```bash
   python engineering-team/skills/senior-frontend/scripts/frontend_decision_engine.py \
     --primary-device <mobile-4g|desktop-fiber|low-end-android|corporate-network> \
     --lcp-target-ms <N> --seo-dependent <true|false> \
     --auth-walled <true|false> --team-size <N>
   ```
4. **Surface the matched profile + runner-up tradeoff** (if within 15%).
5. **Fork into specialists** (one at a time, depth-first):
   - `a11y-audit` for WCAG baseline (always)
   - `performance-profiler` for CWV baseline + bundle audit
   - `epic-design` only for `astro-or-static` marketing surfaces
   - `apple-hig-expert` only for Apple-platform-native surfaces
   - `dependency-auditor` before any major release
   - `cs-karpathy-reviewer` before any commit

## Output expectations (≤ 200-word digest)

- Matched profile + reason
- Three CWV targets (LCP, INP, CLS) at p75 on the primary device
- Per-route JS bundle budget in KB-gzip
- Named a11y owner
- List of specialists invoked + artifact paths
- Recommended next sub-skill

## Anti-patterns

- ❌ Recommending Next App Router as a universal default. Device + SEO + auth decide rendering.
- ❌ Setting "fast" as a target. Pick a number in ms.
- ❌ Skipping `a11y-audit` on customer-facing surface.
- ❌ Reimplementing perf-profiling logic. Fork into `performance-profiler`.

## Customization

Profiles live at `engineering-team/skills/senior-frontend/profiles/`. Four built-in: `next-app-router`, `remix-or-sveltekit`, `vite-spa`, `astro-or-static`. Copy one to `<your-org>.json` and adjust to add your org's defaults.

## Related commands

- `/cs:fullstack-review` — full-stack lens (parent)
- `/cs:backend-review` — for API contract on the consumer side
- `/cs:engineer-grill` — cross-role 21-question grill
- `/karpathy-check` — Karpathy 4-principle review
