# Marketing Skills & Plugins — Gap Audit

**Audit date:** 2026-05-28
**Branch:** `claude/marketing-audit-gaps-GCCiT`
**Scope:** `marketing-skill/` (45 skills, 1 plugin) + `marketing/landing/` (1 standalone plugin)
**Method:** structural survey + content sampling + script smoke tests + governance cross-check

---

## Executive Summary

The marketing portfolio is the largest single domain in the repo and broadly **production-ready at the script and content layer** — 60 Python tools all pass `--help`, stdlib-only, zero LLM calls — but it has **serious governance drift, count inconsistencies, and notable coverage holes** in modern channels (video, newsletter, community, PR, ABM, SMS).

| Dimension | Verdict | Why |
|---|---|---|
| Scripts / automation | **PASS** | 60/60 stdlib-only, no API calls, all `--help` clean |
| SKILL.md content | **PASS with 1 thin skill** | Only `brand-guidelines` is clearly under-built (94 lines) |
| Governance / counts | **FAIL** | README says "6 skills"; marketplace says "44"; CLAUDE.md says "46"; reality is 45 |
| Discoverability (commands/agents) | **FAIL** | Only 2/45 skills have slash commands; only 3 cs-* agents for 8 pods |
| Coverage of modern channels | **PARTIAL** | Missing YouTube, TikTok, newsletter, community, PR, ABM, SMS, influencer |
| Internal redundancy | **PARTIAL** | Social-media quadrant is over-segmented; `prompt-engineer-toolkit` is mis-located |
| Path-B contract compliance | **MIXED** | Only `aeo` is fully Path-B; rest predate the convention |

---

## 1. Critical Governance Issues (fix first)

### 1.1 Skill-count drift across 4 sources — VERDICT: FIX IMMEDIATELY
**Why:** every downstream consumer (marketplace search, README, plugin loader) sees a different number.

| Source | Claims | Actual |
|---|---|---|
| Disk inventory | 45 | 45 |
| `marketing-skill/.claude-plugin/plugin.json:3` | "45 production-ready marketing skills" | ✅ |
| `.claude-plugin/marketplace.json:18` | "44 marketing skills across 7 pods" | ❌ (-1) |
| `.claude-plugin/marketplace.json:7` (top description) | "marketing (46 …)" | ❌ (+1) |
| `marketing-skill/README.md:3` | "Complete suite of **6** expert marketing skills" | ❌ (-39) |
| `marketing-skill/CLAUDE.md:3` | "45 marketing skills" | ✅ |
| Root `CLAUDE.md` | "46 marketing skills (8 pods)" | ❌ (+1) |

**Verdict:** README is **~3 years stale** — still describes the 6-skill v1 era. Marketplace.json description undercounts pods (7 vs 8 — AEO pod was added in v2.7.3 and the marketplace blurb wasn't updated). Single source of truth needed.

### 1.2 README.md is unusable — VERDICT: REWRITE
- 1,003 lines that document only `content-creator` (deprecated), `marketing-demand-acquisition`, and `marketing-strategy-pmm`. A user landing here discovers <7% of the available tooling.
- Currently functions as anti-documentation: it actively misleads.

### 1.3 Loose .zip artifacts in repo root — VERDICT: DELETE
Five `.zip` files (May 23 dates) in `marketing-skill/` root: `app-store-optimization.zip`, `content-creator.zip`, `marketing-demand-acquisition.zip`, `marketing-strategy-pmm.zip`, `social-media-analyzer.zip`. These are v1-era distribution bundles superseded by the `skills/` tree. **No purpose**, ~118 KB of dead weight, confusing to cloners. Drop them; if they need to persist for archival, move to `documentation/legacy-bundles/` and gitignore.

### 1.4 Deprecated `content-creator/` still loadable — VERDICT: REMOVE or HARD-DEPRECATE
- `marketing-skill/skills/content-creator/SKILL.md` still resolvable via plugin
- `agents/marketing/cs-content-creator.md` still references it
- CLAUDE.md says it's deprecated ("→ use content-production") but nothing enforces it
- Either delete the folder entirely or make SKILL.md a 5-line redirect stub.

---

## 2. Discoverability — Severe Under-Investment

### 2.1 Slash commands: 2 of 45 skills — VERDICT: BUILD 6 PRIORITY COMMANDS
`commands/` contains only `cs-aeo.md` and `seo-auditor.md`. Compare to:
- `c-level-advisor/`: ~17 `/cs:*` commands for 28 skills
- `engineering/`: many `/slo-design`, `/chaos-experiment`, `/flag-cleanup`, etc.

Marketing is the largest domain (45 skills) and has the fewest commands per skill (0.04). Recommended Phase-1 commands:
- `/cs:marketing` — pod router (wraps `marketing-ops`)
- `/cs:seo-audit` — wraps `seo-audit` skill
- `/cs:cro` — wraps `page-cro` + funnel chain
- `/cs:content-brief` — wraps `content-strategy`
- `/cs:launch-plan` — wraps `launch-strategy`
- `/cs:competitor-analysis` — wraps `competitor-alternatives`

### 2.2 Agents: 3 cs-* marketing agents for 8 pods — VERDICT: BUILD 5 MORE
Current: `cs-aeo`, `cs-content-creator` (deprecated), `cs-demand-gen-specialist`. Missing personas for: Content, SEO, CRO, Social, Growth. Following the pattern in `c-level-advisor/c-level-agents/`, each pod deserves a forcing-question persona agent.

### 2.3 No `.gemini/` sync despite plugin.json claim — VERDICT: SYNC OR REMOVE CLAIM
`marketing-skill/plugin.json:3` claims compatibility with "Claude Code, Codex, Gemini CLI, Cursor, OpenClaw" but only `.codex/instructions.md` exists. Either run `sync-gemini-skills.py` parallel to the codex pattern, or trim the claim.

---

## 3. Coverage Gaps — What's Missing

Verdicts below are "ADD" if the channel is mainstream B2B/SaaS marketing in 2026 and currently has zero coverage in the 45 skills.

| Missing capability | Verdict | Why |
|---|---|---|
| **YouTube strategy** (script-to-publish, thumbnails, retention) | **ADD — priority 1** | YouTube is now the #1 long-form discovery engine; no skill covers it. `video-content-strategist/` exists as a sibling folder but isn't wired into the marketing-skill plugin |
| **Short-form video** (TikTok, Reels, Shorts) | **ADD — priority 1** | Dominant 2024-2026 discovery surface; only x-twitter-growth touches video |
| **Newsletter strategy** (Substack/Beehiiv era — list growth, monetization, sponsorship) | **ADD — priority 1** | `email-sequence` covers lifecycle and `cold-email` covers outreach; nothing covers owned newsletter audience-building, which is now table-stakes B2B distribution |
| **Community marketing** (Discord, Slack, Circle, owned communities) | **ADD — priority 2** | Highest retention & word-of-mouth lever in 2026; zero coverage |
| **PR / earned media** (press release, journalist outreach, HARO-style replies) | **ADD — priority 2** | Compounds with AEO (citations drive E-E-A-T); currently no skill |
| **ABM (account-based marketing)** | **ADD — priority 2** | B2B SaaS staple; the cold-email skill is too narrow |
| **Multi-touch attribution** | **ADD — priority 2** | `analytics-tracking` only generates tracking plans; no attribution model selection (MTA vs MMM vs incrementality) |
| **Influencer / creator partnerships** | **ADD — priority 3** | Mainstream channel; zero coverage |
| **Affiliate program operations** | **ADD — priority 3** | `referral-program` covers customer referrals, not third-party affiliates |
| **LinkedIn organic growth** | **ADD — priority 3** | X has its own skill; LinkedIn (the dominant B2B social) does not |
| **SMS marketing** | **ADD — priority 4** | High ROI for ecom/D2C; absent |
| **Push notifications** | **ADD — priority 4** | Mobile retention lever; absent |
| **i18n / localization marketing** | **SKIP — fold into marketing-strategy-pmm** | `marketing-strategy-pmm/references/international-gtm.md` exists; can be promoted into a sub-skill later |
| **Podcast marketing** | **SKIP** | Niche; lower ROI than the above |

---

## 4. Internal Redundancy & Mis-located Skills

### 4.1 Social-media quadrant — VERDICT: CONSOLIDATE OR DOCUMENT BOUNDARIES
Four overlapping skills, no clear router:
- `social-content/` (write posts)
- `social-media-manager/` (strategy, calendar)
- `social-media-analyzer/` (metrics, ROI)
- `x-twitter-growth/` (X-specific tactics)

A user who says "grow my Twitter following" plausibly matches 3 of 4. Either:
- **(a)** Add an explicit Social pod orchestrator skill (`social-ops`) with a routing matrix, OR
- **(b)** Consolidate `social-content` + `social-media-manager` → one `social-media` skill; keep analyzer + x-twitter-growth distinct.

Recommendation: **(a)** — preserves depth, fixes routing.

### 4.2 `prompt-engineer-toolkit/` — VERDICT: MOVE TO ENGINEERING
2 scripts, 3 refs, all about prompt-engineering infrastructure (versioning, A/B eval, regression testing). This is engineering tooling, not marketing. A marketer doesn't write prompt eval harnesses. Either:
- Move to `engineering/prompt-engineer-toolkit/`, OR
- Refocus the skill to *marketing-prompt-craft* (headline prompts, content-brief prompts, copy-rewrite prompts) and rename to `marketing-prompts/`.

### 4.3 `marketing-skills/` vs `marketing-ops/` — VERDICT: KEEP BOTH (with note)
The Explore agent confirmed these are complementary, not duplicates: `marketing-skills/` is the ecosystem-architecture doc, `marketing-ops/` is the question-router. **Document the distinction in both SKILL.md frontmatters** so users don't bounce between them.

### 4.4 `marketing/landing/` standalone vs `marketing-skill/skills/page-cro/` — VERDICT: KEEP DISTINCT (verified)
- `marketing/landing/` produces single-file HTML with GSAP animation (premium one-pager output)
- `product-team/skills/landing-page-generator/` outputs Next.js TSX (conversion-optimized)
- `page-cro/` audits live pages for conversion friction

The `source.distinct_from` field in `marketing/landing/plugin.json` already documents this — good pattern, replicate elsewhere.

---

## 5. Per-Skill Quality Issues (the 12 thinnest)

From the structural survey + content sampling:

| Skill | Issue | Verdict |
|---|---|---|
| `brand-guidelines` | 94 lines, mostly Q&A, no scripts, 1 ref | **EXPAND** — add brand audit script, brand-voice scorer, +2 refs |
| `paywall-upgrade-cro` | 0 scripts, 0 refs (body is self-contained 259 lines) | **ADD** 1 paywall-friction scorer script + 1 ref on paywall canon (Steinman, Lincoln Murphy) |
| `popup-cro` | 0 scripts | **ADD** popup-frequency-cap calculator + popup A/B sizer |
| `social-content` | 0 scripts despite 324-line SKILL.md | **ADD** hook-quality scorer + post-format classifier |
| `marketing-psychology` | 0 scripts | **ADD** mental-model picker (Cialdini/JTBD/loss-aversion routing) |
| `marketing-ideas` | 0 scripts | **ADD** idea-prioritizer (RICE-for-marketing) |
| `marketing-strategy-pmm` | 0 scripts despite 399-line SKILL.md + 4 refs | **ADD** ICP scorer + positioning-statement validator |
| `ai-seo` | 0 scripts | **ADD** AI-search audit script (LLM-citation surface check) |
| `programmatic-seo` | 0 refs | **ADD** ref on programmatic-SEO canon (Zapier/G2/Tripadvisor patterns) |
| `onboarding-cro` | 0 refs | **ADD** ref on activation patterns (Reforge/Eppo) |
| `page-cro` | 0 refs | **ADD** ref on CRO canon (Bryan Eisenberg, Linnworks, CXL) |
| `social-media-manager` | 0 refs | **ADD** platform-specific refs |

**Why this matters:** the Path-B contract (3 scripts + 3 refs each) became the standard from v2.7.0 onward; legacy marketing skills predate it. Bringing them up to 1+ script and 1+ ref each is a low-cost lift that doubles the deterministic tooling surface.

---

## 6. Path-B Contract Compliance

Only `aeo/` was built under the Path-B 11-file contract (SKILL.md + 3 scripts + 3 refs + cs-* agent + /cs:* command + plugin.json + `source` field). The other 44 skills predate it. **Verdict: DO NOT retroactively force Path-B on all 44** — it's expensive and the legacy skills work. Instead:

- Apply Path-B to all *new* marketing skills going forward (newsletter, YouTube, community, etc. from §3).
- Promote 5 highest-traffic legacy skills to Path-B opportunistically: `seo-audit`, `page-cro`, `content-production`, `copywriting`, `paid-ads`.

---

## 7. Recommended Action Plan (Prioritized)

| # | Action | Effort | Impact |
|---|---|---|---|
| 1 | Fix the count drift (README, marketplace.json:7, marketplace.json:18, root CLAUDE.md) → single source = 45 skills, 8 pods | XS | HIGH — fixes discoverability immediately |
| 2 | Delete the 5 legacy `.zip` files | XS | LOW noise reduction |
| 3 | Replace README.md with an auto-generated index of the 45 skills (1 line per skill, grouped by pod) | S | HIGH — current README is anti-documentation |
| 4 | Hard-deprecate or delete `content-creator/` skill + `cs-content-creator.md` agent | XS | MEDIUM — removes a known landmine |
| 5 | Build 6 priority slash commands (§2.1) | M | HIGH — discoverability |
| 6 | Build 5 pod cs-* agents (§2.2) | M | MEDIUM |
| 7 | Add 4 high-priority missing skills: `newsletter`, `youtube`, `short-form-video`, `community-marketing` (Path-B each) | L | HIGH — covers the largest channel gaps |
| 8 | Decide on `prompt-engineer-toolkit/`: move to engineering OR refocus on marketing prompt craft | S | MEDIUM |
| 9 | Add the 12 missing scripts/refs from §5 | M | MEDIUM |
| 10 | Add Gemini CLI sync OR remove the claim from plugin.json | S | LOW |
| 11 | Phase-2 missing skills: ABM, attribution-modeling, PR-outreach, influencer-marketing, linkedin-growth | L | MEDIUM |
| 12 | Phase-3: SMS, push, affiliate, podcast (lower ROI per effort) | L | LOW |

**Quick wins (do this week):** #1, #2, #3, #4 — entirely governance, low effort, removes most of the documentation rot.

**Strategic investments (next quarter):** #5, #6, #7 — bring discoverability and modern-channel coverage to par with c-level-advisor and engineering domains.

---

## Appendix A — Verified Data Points

- 45 skill subdirectories on disk in `marketing-skill/skills/`
- 60 Python scripts in marketing skills (all stdlib, all `--help` clean, zero API calls)
- ~75 reference docs across skills
- 2 marketing-related slash commands (`cs-aeo`, `seo-auditor`)
- 3 cs-* marketing agents (1 deprecated)
- 1 `.codex/` sync folder; no `.gemini/`, `.hermes/`, or `.vibe/` for marketing
- 5 legacy `.zip` artifacts in domain root (~118 KB)
- 1 standalone plugin (`marketing/landing/`) — legitimately distinct from `page-cro` and `landing-page-generator`

## Appendix B — Skills With Strong Content But Zero Tooling

These are the skills most worth investing 1 script + 1 ref in (highest content-to-tooling ratio):

| Skill | SKILL.md lines | Scripts | Refs |
|---|---|---|---|
| `marketing-strategy-pmm` | 399 | 0 | 4 |
| `social-content` | 324 | 0 | 3 |
| `paywall-upgrade-cro` | 259 | 0 | 0 |
| `popup-cro` | 230 | 0 | 1 |
| `marketing-ideas` | 212 | 0 | 1 |
| `social-media-manager` | 198 | 1 | 0 |
| `marketing-psychology` | 124 | 0 | 1 |
| `brand-guidelines` | 94 | 0 | 1 |

---

**End of audit.**
