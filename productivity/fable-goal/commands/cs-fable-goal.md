---
name: "cs-fable-goal"
argument-hint: "[ramble about the thing you want made]"
description: "/cs:fable-goal — Turn a ramble about something you want made into one polished, autonomous /goal prompt (copy-paste ready). Extracts deliverable/quantity/stakes/tools/destination, asks at most one question batch, verifies every named resource exists, writes a 150–350 word prose prompt with the seven-part anatomy, and self-checks before delivering."
---

# /cs:fable-goal — Goal Prompt Writer

**Command:** `/cs:fable-goal <ramble>`

Converts a rambling description of a desired outcome into a single polished /goal prompt for a fresh autonomous session. The output is the prompt, never the build.

## When to Run

- You know what you want made but not how to ask for it well
- Voice-to-text rambles ("I want like 5 landing pages, crazy good, put them up somewhere")
- You're about to kick off a fresh autonomous session and want the prompt engineered first

## When NOT to Run

- You want the thing built right now in this session — just ask for it directly
- You already have a well-formed prompt and want it executed

## What You Get

1. One fenced code block containing the finished /goal prompt (150–350 words, flowing first-person prose) with all seven anatomy parts: desire + stakes, quality bar, verified tool inventory + discovery mandate, creative-freedom grant, medium-matched verification loop, delivery destination, and the closing goal line + autonomy directive
2. A 2–4 bullet **Assumptions** list so you can correct any gap-fill with one line instead of re-rambling

## Process (enforced by the skill)

Extract the six slots from the ramble → fill gaps from your brand profile or defaults, asking at most ONE question batch → verify every resource the prompt will name actually exists → write the prompt → run the six-point self-check → deliver.

See `skills/fable-goal/SKILL.md` for the full anatomy, verification-by-medium table, and anti-pattern list.
