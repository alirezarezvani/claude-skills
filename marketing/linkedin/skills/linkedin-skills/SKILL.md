---
name: linkedin-skills
description: Use when someone wants to grow an organic LinkedIn presence — a content strategy for a career change or consulting or thought leadership, a rewritten profile or headline, post drafts and hooks, a posting cadence or newsletter plan, connection notes and outreach, a commenting strategy, repurposing an article or talk into posts, or a read on why their reach dropped. Triggers on "grow my LinkedIn", "fix my headline", "write a LinkedIn post", "what should I post about", "LinkedIn strategy", "connection request", "my reach dropped". Forks context to route to one of five sub-skills, and refuses automation, scraping, pods, and bulk DMs before any drafting starts.
context: fork
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-08-25
  build_pattern: "Domain orchestrator — deterministic lane router + policy gate, five managed sub-skills"
  distinct_from: "marketing-skill/x-twitter-growth (X/Twitter-specific); marketing-skill/social-content (multi-platform calendars); marketing-skill/social-media-analyzer (cross-platform reporting); productivity/andreessen (venture judgement, not audience building)"
---

# LinkedIn — Organic Presence Orchestrator

> **Portability + safety:** 17 stdlib-only Python scripts. **No LinkedIn credentials, no API
> calls, no scraping, nothing auto-sent.** Every output is text the account holder posts
> themselves — automated posting, connecting, and commenting are prohibited by LinkedIn's
> User Agreement §8.2, and a restricted account ends the whole project.

Building an authentic presence over months, not generating a post. The five lanes cover what
actually moves: who you are (profile), what you stand for (strategy), what you publish
(content), who you talk to (engagement), and what any of it did (analytics).

## Step 1 — Gate, before anything is drafted

```bash
python3 scripts/linkedin_policy_gate.py --text "<the user's own words>" --output human
```

- **exit 4 REFUSE** — a named rule is broken (automation, scraping, pods, bulk DMs, fake
  identity, fabricated proof, a prohibited automation platform). Do not draft it: name the
  rule, offer the substitute the gate prints, and route there instead. A REFUSE outranks any
  route below.
- **exit 3 CONSTRAIN** — proceed, and state the constraint out loud in your reply.
- **exit 0 ALLOW** — proceed.

## Step 2 — Route

```bash
python3 scripts/linkedin_goal_router.py --text "<the goal>" --output human
```

Exit 0 routes — invoke that lane, surfacing any `prerequisite` as a question first.
Exit 2 is ambiguous — ask **one** question naming both candidates, with a recommendation.
Exit 3 has no signal — ask what they want to walk away with, rather than guessing.

| Lane | Typical ask |
|---|---|
| `linkedin-profile` | "fix my headline", "my profile gets views but nothing happens" |
| `linkedin-strategy` | "what should I post about", "how often", "should I start a newsletter" |
| `linkedin-content` | "write this post", "turn my talk into posts", "is this hook any good" |
| `linkedin-engagement` | "who should I comment on", "write a connection note" |
| `linkedin-analytics` | "why did reach drop", "what's working", "should I test this" |

## Step 3 — Forcing questions

One at a time, each with a recommended answer. Stop as soon as the lane can run honestly.
`/cs:grill-linkedin` walks all five with the recommendation and the canon behind each.

1. What has to be true in 90 days for this to have been worth it? *(Not a follower count.)*
2. Who is this for, specifically enough that someone is excluded?
3. How many minutes a week will you protect — measured from a bad week?
4. What proof already exists? *(If none, the first pillar is process, not results.)*
5. What will you not post about?

## Hard rules

- **Nothing is automated and nothing is sent.** No credentials, no API, no scraping.
- **Refuse, then substitute.** Every REFUSE names the compliant alternative.
- **The account holder is the author of record.** They read every line before it ships.
- **No claim they cannot substantiate.** A real number, a bounded range, or nothing.
- **Never silently chain lanes.** Offer the next one as a question.
- **Cite the confidence level.** LinkedIn-official is 🟢, third-party studies are 🟡,
  folklore is 🔴 and gets named as folklore.

## Scripts

| Script | Role |
|---|---|
| [`scripts/linkedin_policy_gate.py`](scripts/linkedin_policy_gate.py) | ALLOW / CONSTRAIN / REFUSE against User Agreement §8.2 + Community Policies. 7 refusal rules, each with a substitute. |
| [`scripts/linkedin_goal_router.py`](scripts/linkedin_goal_router.py) | Deterministic five-lane classifier: route (0) / ask (2) / no-signal (3), with cross-lane prerequisites. |

## References and assets

- [`references/linkedin_platform_canon.md`](references/linkedin_platform_canon.md) — how the feed ranks, evidence-graded (7 sources)
- [`references/policy_and_account_safety.md`](references/policy_and_account_safety.md) — §8.2, prohibited software, restriction triggers (7 sources)
- [`assets/linkedin_operating_agreement.md`](assets/linkedin_operating_agreement.md) — the standing rules in one page, agreed before work starts

## Distinct from

- **`marketing-skill/x-twitter-growth`** — X/Twitter mechanics. Different platform and rules.
- **`marketing-skill/social-content` / `social-media-manager`** — multi-platform brand
  calendars. This is one person's presence on one platform, in depth.
- **`marketing-skill/social-media-analyzer`** — cross-platform campaign reporting.

---

**Version:** 1.0.0 · 5 lanes · 17 stdlib scripts · nothing auto-sent
