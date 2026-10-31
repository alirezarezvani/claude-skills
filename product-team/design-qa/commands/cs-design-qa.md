---
disable-model-invocation: true
description: Run the full UI finish gate on a screen - source lint, interaction states and a rendered audit at 320 px and desktop - and say whether it is done.
argument-hint: "<source path> [running URL] [state matrix CSV]"
---

# /cs-design-qa

Gate `$ARGUMENTS` before it is called done.

If there is no running URL, run steps 1 and 2 and say that the rendered audit is still owed. Do not call the screen done without it.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/design-qa/scripts/finish_lint.py <source path>
python ${CLAUDE_PLUGIN_ROOT}/skills/design-qa/scripts/state_matrix_checker.py --matrix <states.csv>
node ${CLAUDE_PLUGIN_ROOT}/skills/design-qa/assets/capture_snapshot.mjs <url> --width 320 --out s320.json
node ${CLAUDE_PLUGIN_ROOT}/skills/design-qa/assets/capture_snapshot.mjs <url> --width 1440 --out s1440.json
python ${CLAUDE_PLUGIN_ROOT}/skills/design-qa/scripts/rendered_audit.py --snapshot s320.json
python ${CLAUDE_PLUGIN_ROOT}/skills/design-qa/scripts/rendered_audit.py --snapshot s1440.json
```

No state matrix yet? Draft one from the source (which surfaces fetch data, which are forms, which start async work) using `${CLAUDE_PLUGIN_ROOT}/skills/design-qa/assets/states.example.csv`, and mark only what you can see as DONE.

## Report

1. Verdict per step (the script's first line), then **DONE** or **NOT DONE**.
2. Blockers, grouped by fix, each with file:line or element id and the one-line fix.
3. Missing states, blocking ones first.
4. Template traits and generic risk. Say whether the brief asks for the look; never block on it.
5. What the scripts could not check: unverified contrast, the screen-reader pass, and `a11y-audit` for source accessibility.
