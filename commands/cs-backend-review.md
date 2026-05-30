---
description: Backend engineering review — walks the 7 Matt Pocock forcing questions (read/write ratio + QPS, tenancy, sync vs async, data sensitivity, pattern, RPO/RTO, SLO), picks the language + pattern profile, forks into specialists (api-design-reviewer, database-designer, migration-architect, slo-architect). Invokes the cs-backend-engineer agent with context fork.
argument-hint: "<problem or service to review>"
---

# /cs:backend-review — Backend engineering review

Use the `cs-backend-engineer` agent (uses `context: fork`) to handle this inquiry:

**$ARGUMENTS**

## Forcing-question library

Canonical source: `engineering-team/skills/senior-backend/references/forcing_questions.md` (7 questions, one-per-turn, recommendation + canon citation per question).

1. Read/write ratio + one-year p99 QPS
2. Tenancy model (single / shared / isolated multi-tenant)
3. Sync request/response vs async (queue) vs event-driven
4. Data sensitivity tier (public / internal / PII / PHI / PCI)
5. Monolith / modular monolith / microservices (team-size justification)
6. RPO and RTO
7. SLO + named error-budget consumer

## Routing protocol

1. **Walk the 7 forcing questions** in `engineering-team/skills/senior-backend/references/forcing_questions.md`. One per turn. Recommend with cited canon. Track in `/tmp/backend-grill-<date>.md`.
2. **Surface kill criteria** — e.g., "microservices, team size 5" trips (Newman's MonolithFirst). STOP and resolve.
3. **Run the deterministic profile picker:**
   ```bash
   python engineering-team/skills/senior-backend/scripts/backend_decision_engine.py \
     --team-size <N> --qps-p99 <N> --read-write-ratio <ratio> \
     --tenancy <single-tenant|shared-multi-tenant|isolated-multi-tenant> \
     --data-sensitivity <public|pii|phi|pci> \
     --pattern <monolith|modular-monolith|domain-bounded-services|microservices|serverless> \
     --language-preference <typescript|python|go|rust|java|kotlin|dotnet>
   ```
4. **Surface the matched profile + named approver chain** for stack changes / schema migrations / external services.
5. **Fork into specialists in dependency order:**
   - `slo-architect` FIRST — no SLO, no design
   - `api-design-reviewer` — API contract
   - `database-designer` + `database-schema-designer` — schema + ERD
   - `migration-architect` — only if changing existing schema
   - `observability-designer` — golden signals + alerts
   - `ci-cd-pipeline-builder` — pipeline matching cadence target
   - `senior-security` + `adversarial-reviewer` — before public launch
   - `ra-qm-team/*` — if data sensitivity is PHI / PCI / regulated
   - `cs-karpathy-reviewer` — before any commit

## Output expectations (≤ 200-word digest)

- Matched profile + reason
- Three SLO targets (p50, p99 latency + uptime)
- RPO + RTO
- Named approver chain (tech-lead + on-call + DBA + ...)
- List of specialists invoked + artifact paths
- Recommended next sub-skill

## Anti-patterns

- ❌ Recommending Kafka / event-driven before naming the second team that needs it.
- ❌ Recommending microservices without team-size ≥ 30 + platform team + bounded-context independence.
- ❌ Designing the API without forking into `api-design-reviewer`.
- ❌ Recommending a DB without QPS + read/write ratio (Q1 unanswered).
- ❌ Auto-approving a production schema migration. Always name the on-call + DBA.

## Customization

Profiles live at `engineering-team/skills/senior-backend/profiles/`. Four built-in: `node-express`, `fastapi-python`, `django-monolith`, `go-or-rust-microservice`. Copy one to `<your-org>.json` and adjust constraints / SLO floor / approver chain.

## Related commands

- `/cs:fullstack-review` — full-stack lens (parent)
- `/cs:frontend-review` — for API consumer side
- `/cs:engineer-grill` — cross-role 21-question grill
- `/slo-design` — explicit SLO design via slo-architect
- `/karpathy-check` — Karpathy 4-principle review
