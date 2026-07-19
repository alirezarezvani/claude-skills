# fable-goal

Turn a ramble about something you want made into **one polished, autonomous /goal prompt** — copy-paste ready for a fresh session. The skill writes the prompt, never the build.

## What this skill does

You describe an outcome in fragments ("I want like 5 landing pages for my prompt pack, crazy good, put them up somewhere"). The skill:

1. **Extracts** the six slots a goal prompt needs: deliverable, quantity, audience/stakes, tools named, quality bar, destination
2. **Fills gaps** from your brand profile (if you keep one) or sensible defaults — asking at most ONE question batch, never interviewing in rounds
3. **Verifies before naming** — every skill, path, or MCP the prompt mentions is checked against the live environment so the fresh session never chases phantoms
4. **Writes** a 150–350 word flowing-prose prompt with the seven-part anatomy: desire + stakes → quality bar → tool inventory + discovery mandate → creative-freedom grant → verification loop matched to the medium → delivery → goal line + autonomy directive
5. **Self-checks** against six binary criteria before delivering, then outputs the prompt in one fenced block plus a short Assumptions list

## The philosophy

Get out of the model's way. A great /goal prompt nails the *what*, grants explicit freedom on the *how*, and demands self-verification before done — with a completion condition the session can observe itself (load the page, run the script, watch the render).

## Usage

```
/cs:fable-goal I keep manually sorting the podcast files my editor sends, write me a prompt so a session builds me something for that
```

Or just ramble and say "turn this into a goal prompt."

## Design notes

Unlike sibling `productivity/*` plugins, this one intentionally ships no `agents/` persona and no `assets/`: the skill is a single reasoning pass with nothing to orchestrate in parallel, invoked via `/cs:fable-goal`, and its output is one prose block with no templates to fill. `scripts/goal_prompt_self_check.py` covers the mechanically checkable subset of the pre-delivery self-check (word count, goal line, autonomy directive, verification/freedom/destination language); deliverable concreteness and live-environment resource verification remain author judgment.

## Attribution

Derived from [duncan-buildroom/freeskills](https://github.com/duncan-buildroom/freeskills) `fable-goal` ("free to use and modify. Made for builders."). This version is a substantial restructure: wrong-tool check, observable-done principle, verification-defaults-by-medium table, six-point pre-delivery self-check, failure-mode catalog, and a second worked example in a non-web medium.
