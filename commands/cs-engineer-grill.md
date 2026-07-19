---
description: "Cross-role engineering grill — Matt Pocock 7 questions per role × 3 roles (fullstack / frontend / backend) = up to 21 forcing questions, one per turn, with canon citations and kill criteria. Default: ask which lane first; `--all` runs all 21."
argument-hint: "<plan or architecture to grill> [--lane fullstack|frontend|backend|all]"
---

# /cs:engineer-grill — Cross-role engineering forcing-question grill

Walk the user through the Matt Pocock forcing-question discipline before they lock any engineering decision. This is the **grill-with-docs** pattern (canon-anchored, recommended answers, kill criteria) applied across the three engineering role lanes.

**$ARGUMENTS**

## Routing protocol

1. **Detect lane signals** in the user's prompt:
   - **Fullstack signals:** "scaffold", "stack", "Next.js + Postgres", "monorepo", "deploy", "team size", "budget", "cadence"
   - **Frontend signals:** "React", "Next", "Remix", "Vite", "Astro", "bundle", "LCP", "INP", "CLS", "a11y", "WCAG", "Tailwind", "design system"
   - **Backend signals:** "API", "REST", "GraphQL", "database", "Postgres", "MongoDB", "schema", "migration", "QPS", "tenancy", "SLO", "Kafka", "queue", "microservice", "monolith"

2. **If `--lane <name>` is supplied:** walk only that lane's 7 questions.
3. **If lane signals score ≥ 3 hits for one lane:** confirm with the user, then walk that lane's 7 questions.
4. **If lane signals are ambiguous OR `--lane all`:** ask the user: "Fullstack (7 Qs about team / stack / scale), Frontend (7 Qs about device / rendering / bundle / a11y), or Backend (7 Qs about QPS / tenancy / pattern / SLO)? Or `all` for all 21."

## Lane: fullstack

Questions live in `engineering-team/skills/senior-fullstack/references/forcing_questions.md`. Summary:

1. Team size today + 12-month headcount?
2. Deployment cadence — per-PR, daily, weekly, quarterly?
3. Customer-facing, internal tool, or marketing site?
4. One-year p50 / p99 traffic forecast?
5. Hiring against the stack or training the team?
6. Year-one monthly cloud + SaaS ceiling?
7. Three verifiable success criteria with numeric targets?

## Lane: frontend

Questions live in `engineering-team/skills/senior-frontend/references/forcing_questions.md`. Summary:

1. Primary device + network (mobile-4G / desktop-fiber / low-end Android / corporate)?
2. LCP target in ms (and INP, CLS)?
3. RSC / SPA / SSR / SSG — pick and defend?
4. JS bundle budget per route in KB-gzip?
5. SEO-dependent or auth-walled?
6. Design-system source of truth?
7. WCAG target + named a11y owner?

## Lane: backend

Questions live in `engineering-team/skills/senior-backend/references/forcing_questions.md`. Summary:

1. Read/write ratio + p99 QPS forecast?
2. Tenancy model — single / shared / isolated?
3. Sync / async / event-driven — default + exceptions?
4. Data sensitivity tier — PII / PHI / PCI?
5. Monolith / modular monolith / microservices — team-size justification?
6. RPO + RTO?
7. SLO + named error-budget consumer?

## Discipline (Matt Pocock, MIT, preserved verbatim from `engineering/grill-me`)

1. **One question per turn.** Never bundle. Never default to "what do you think?".
2. **Always recommend an answer.** Format: "Recommended: <answer>, because <one-sentence rationale from cited canon>".
3. **Walk depth-first.** Finish a lane before opening another.
4. **Surface the kill criterion.** If the user's answer trips it, STOP and resolve before continuing.
5. **Track answers.** Write to `/tmp/engineer-grill-<lane>-<date>.md` so the conversation survives compaction.

## After the grill

1. **Run the lane's decision engine** with the seven answers:
   - Fullstack → `python engineering-team/skills/senior-fullstack/scripts/fullstack_decision_engine.py ...`
   - Frontend → `python engineering-team/skills/senior-frontend/scripts/frontend_decision_engine.py ...`
   - Backend → `python engineering-team/skills/senior-backend/scripts/backend_decision_engine.py ...`
2. **Surface the matched profile + named approvers.**
3. **Recommend the next sub-skill chain** based on the composition map.

## Output expectations

- One artifact per lane walked, written to `/tmp/engineer-grill-<lane>-<date>.md`.
- One final digest (≤ 250 words) summarizing the matched profile per lane + the three highest-leverage next actions.
- **Never** auto-approve a stack change, schema migration, or architecture choice.

## Related commands

- `/cs:fullstack-review`, `/cs:frontend-review`, `/cs:backend-review` — single-lane deep dives
- `/karpathy-check` — Karpathy review before commit
- `/cs:grill-bizops`, `/cs:grill-commercial` — sibling cross-domain grills (BizOps + Commercial v2.8.0)
