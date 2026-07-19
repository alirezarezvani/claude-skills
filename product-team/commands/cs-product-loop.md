---
description: Run the continuous-discovery loop — score the weekly cadence (Torres), act on the named gap, lint the Opportunity Solution Tree as the machine gate, and keep the streak alive with explicit stop states. The product-domain recurring loop; graduates validated assumptions to experiments or PRDs.
argument-hint: "[path to discovery_log.json] [path to ost.json]"
---

# /cs:product-loop — the continuous-discovery loop

Inputs (defaults: `discovery_log.json` and `ost.json` in the workspace; shapes in
`product-team/skills/product-skills/assets/`):

**$ARGUMENTS**

## Sequence (one iteration per invocation)

1. **Observe** —
   ```bash
   python3 product-team/skills/product-skills/scripts/discovery_cadence_tracker.py --input discovery_log.json
   ```
   Exit 5 (< 2 interviews): there is no cadence to measure — help the user book the
   first two weekly touchpoints and write the outcome statement; stop there.
2. **Choose** — the report's `next_loop_action` is the choice. Typical actions: book the
   missing weekly touchpoint · re-anchor the interview guide on the outcome · test the
   top untested assumption (route to `product-discovery`'s assumption_mapper to rank).
3. **Act** — execute with the routed sub-skill's tools (ux-researcher-designer for the
   interview, experiment-designer for the test design). One bounded action per
   iteration.
4. **Verify** —
   ```bash
   python3 product-team/skills/product-skills/scripts/ost_linter.py --input ost.json
   ```
   Exit 2 → fix the listed O1–O5 violations before the tree may drive any roadmap or
   experiment. Then re-run the cadence tracker and confirm the health score did not
   drop.
5. **Record** — update `discovery_log.json` (interview/test entries) and `ost.json`;
   note the health score in the digest so the trend is visible across iterations.
6. **Repeat or stop** — terminal states:
   - **Graduate**: HEALTHY + a validated assumption → hand off to `experiment-designer`
     (A/B gate) or `product-manager-toolkit` (PRD with eval spec if the feature is
     AI-powered).
   - **Escalate**: DORMANT 4+ weeks → name the product lead and say the habit is dead —
     never let discovery die silently.
   - **Clean no-op**: cadence HEALTHY, no gaps — book next week's touchpoint and exit.

## Rules

- Never modify the linter or tracker to make a gate pass.
- Insights require recurrence across independent participants — singletons stay
  anecdotes.
- The loop edits the log and the tree, never the gates (locked-evaluator invariant).
