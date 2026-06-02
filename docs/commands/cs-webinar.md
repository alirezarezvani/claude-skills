---
title: "/cs-webinar — Slash Command for AI Coding Agents"
description: "/cs:webinar — Webinar & virtual-event marketing workflow. Plan a webinar from scratch (sized backward from the business goal), rescue one whose. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-webinar

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/commands/cs-webinar.md">Source</a></span>
</div>


**Command:** `/cs:webinar [mode] [args]`

The `cs-webinar` command is the **entry point for webinar workflows**: plan → promote → run → follow up, or diagnose → fix → re-run.

## When To Run

- Planning a webinar, virtual event, live demo, workshop, masterclass, fireside chat, or virtual summit from scratch
- Rescuing a webinar whose numbers disappointed — low registrations, low show-up, or attendees who don't convert
- Turning a one-time webinar into an always-on evergreen / on-demand engine
- Scoring an existing funnel to find the stage that's actually broken

## When NOT To Run

- Full product launch (not just a webinar) → use `/cs:launch` / launch-strategy
- Generic lifecycle nurture email unrelated to an event → use the `emails` skill
- In-person field-event logistics (venue, catering, booth) → out of scope

## Modes

### `plan` — Design the whole motion from scratch

```bash
/cs:webinar plan
```

Walks the intake, locks the promise + format, sizes the funnel backward from the business goal,
builds the promotion runway, and designs show-up + live-to-close + follow-up. Delivers a full plan
using `templates/webinar-plan-template.md`.

### `rescue` — Diagnose and fix an underperforming webinar

```bash
/cs:webinar rescue --input funnel.json
```

Scores the funnel, names the weakest stage, and returns ranked fixes targeting the actual bottleneck
— not a reflexive landing-page rewrite.

### `evergreen` — Convert a past webinar to on-demand

```bash
/cs:webinar evergreen
```

Maps the on-demand registration → watch → follow-up automation, with honest live-vs-simulated framing.

### `score` — Run the funnel scorer directly

```bash
/cs:webinar score --input funnel.json
/cs:webinar score                 # embedded sample data
```

## Minimal Intake (3 Questions)

| Q | Asks | When |
|---|---|---|
| Q1 | Which mode — plan / rescue / evergreen? | Always |
| Q2 | Business goal + conversion action (leads, pipeline, adoption, retention, brand)? | Always (drives the backward funnel math) |
| Q3 | Audience temperature (customers / warm / owned_cold / paid_cold)? | Always (selects benchmarks) |

Read `marketing-context.md` first if it exists — it covers brand voice, personas, and customer language,
so you only ask for what's specific to this event.

## Workflow

```bash
# Mode: rescue / score — find the broken stage first
python3 marketing-skill/skills/webinar-marketing/scripts/webinar_funnel_scorer.py funnel.json
# → overall 0-100 score + per-stage rate vs. benchmark + named bottleneck

# Pipe JSON via stdin
cat funnel.json | python3 marketing-skill/skills/webinar-marketing/scripts/webinar_funnel_scorer.py -

# Demo on embedded sample data (no --help flag — run with no args)
python3 marketing-skill/skills/webinar-marketing/scripts/webinar_funnel_scorer.py
```

Input JSON (`registrations` + `attended_live` required; rest optional):

```json
{
  "invited": 5000, "page_visits": 1800, "registrations": 620,
  "attended_live": 180, "cta_clicks": 40, "conversions": 14,
  "audience": "owned_cold", "runtime_min": 45, "avg_watch_min": 26
}
```

## The Funnel Math (Plan Backward)

Always size from the business goal backward — this stops anyone celebrating 800 registrations while 6 people buy:

```
Business goal:        20 sales-qualified opportunities
÷ attendee→SQO rate   (~10%)      → need 200 engaged attendees
÷ register→attend     (~35% live) → need ~570 registrations
÷ landing-page CVR     (~40%)     → need ~1,425 landing-page visits
→ promotion must drive ~1,425 qualified visits
```

If the required visits exceed the reachable audience, fix the goal, format, or promotion budget *now*.

## Audience Benchmarks

The scorer calibrates per audience temperature (warmer audiences convert better at every stage):

| Audience | Page→Reg | Reg→Attend | Attend→CTA | Attend→Convert |
|---|---|---|---|---|
| `customers` | 40% | 50% | 25% | 12% |
| `warm` | 35% | 42% | 22% | 10% |
| `owned_cold` | 25% | 35% | 18% | 7% |
| `paid_cold` | 18% | 28% | 15% | 5% |

## Anti-Patterns Rejected

- Celebrating registrations while show-up or conversion quietly fails
- Rewriting the landing page when the broken stage is show-up or live-to-close
- Promoting before sizing the funnel backward from the business goal
- Obvious fake-live framing that erodes audience trust
- Treating a webinar as an event instead of a funnel

## Trigger Phrases

- "plan a webinar" / "webinar strategy"
- "my webinar isn't converting" / "low show-up rate"
- "webinar promotion" / "webinar follow-up"
- "virtual event" / "live demo" / "masterclass" / "fireside chat" / "virtual summit"
- "evergreen webinar" / "on-demand webinar"
- "registration funnel" / "attendance rate"

## Related

- Agent: [`cs-webinar-marketer`](https://github.com/alirezarezvani/claude-skills/tree/main/agents/marketing/cs-webinar-marketer.md)
- Skill: [`webinar-marketing`](https://github.com/alirezarezvani/claude-skills/tree/main/marketing-skill/skills/webinar-marketing/SKILL.md)
- Companion: `/cs:aeo` (get supporting content cited by AI search), launch-strategy (full launches)

---

**Version:** 2.9.0
**License:** MIT
