---
name: "cs-linkedin"
description: "/cs:linkedin — Route any organic LinkedIn goal to the right lane (profile / strategy / content / engagement / analytics) after gating it against LinkedIn's User Agreement. Refuses automation, scraping, engagement pods, bulk DMs, fake identity, and fabricated proof before a word is drafted. Nothing is ever sent."
argument-hint: "[what you want from LinkedIn — a goal, a profile problem, a post, an outreach plan, or a question about your numbers]"
---

# /cs:linkedin — Gate, then route

**Command:** `/cs:linkedin [your goal]`

This plugin holds no LinkedIn credentials, makes no API calls, and sends nothing. Every
output is text you paste and post yourself.

## When to run

- "Help me grow on LinkedIn" / "I want to build an audience"
- You do not know which part of the problem to work on first
- Any LinkedIn request where you want the platform rules checked before the work starts

## When NOT to run

- You already know the lane → go straight to `/cs:linkedin-profile`, `/cs:linkedin-plan`,
  `/cs:linkedin-post`, `/cs:linkedin-outreach`, or `/cs:linkedin-analyze`
- X/Twitter → `marketing-skill/x-twitter-growth`
- Multi-platform brand social calendars → `marketing-skill/social-content`
- Cold email → `marketing-skill/cold-email`

## What you get

1. **A policy verdict** — ALLOW, CONSTRAIN (with the constraint stated), or REFUSE (with the
   rule named and a compliant substitute offered).
2. **A route** — one of five lanes, with the matched signals, or one clarifying question when
   two lanes are genuinely close.
3. **Forcing questions**, one at a time with a recommended answer, until the lane can run
   honestly.
4. **The lane's artifact** — audit, brief, draft, roster, or analysis.

## Workflow

```bash
# 1. Gate first, always
python3 ../skills/linkedin-skills/scripts/linkedin_policy_gate.py \
  --text "<the user's own words>" --output human
#    exit 4 REFUSE  -> name the rule, offer the substitute, route there instead
#    exit 3 CONSTRAIN -> proceed and state the constraint out loud
#    exit 0 ALLOW   -> proceed

# 2. Route
python3 ../skills/linkedin-skills/scripts/linkedin_goal_router.py \
  --text "<the goal>" --output human
#    exit 0 route · exit 2 ask ONE question · exit 3 ask what they want to walk away with
```

## Trigger phrases (auto-invoke without /cs:)

"grow my LinkedIn" · "LinkedIn strategy" · "build an audience on LinkedIn" ·
"my LinkedIn isn't working" · "what should I post on LinkedIn"

## Discipline

- **Gate before route, route before draft.** A REFUSE outranks any route.
- **Never silently chain lanes.** Offer the next one as a question with a recommendation.
- **Evidence-graded claims.** 🟢 LinkedIn-official / 🟡 third-party study / 🔴 folklore, and
  folklore gets named rather than repeated.
- **Nothing is fetched or sent.**

## Stop conditions

- Lane delivered its artifact and the user knows the one thing only they can do next → done.
- REFUSE delivered with a substitute offered, and the user declines the substitute → done.
  Do not build a partial version of the refused thing.
- Router returns NO_SIGNAL twice on the same input → hand the question back plainly.

## Related

- Agent: [`cs-linkedin-orchestrator`](../agents/cs-linkedin-orchestrator.md)
- Skill: [`linkedin-skills`](../skills/linkedin-skills/SKILL.md)
- Siblings: [`/cs:grill-linkedin`](cs-grill-linkedin.md) and the six lane commands
