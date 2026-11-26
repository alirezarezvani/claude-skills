---
disable-model-invocation: true
description: Quote, approve and generate AI plates for the approved animatic's upgrade shots through your own video MCP, then drift-check them. Never spends without a quote and your yes.
argument-hint: "shots.json [--adapter higgsfield] [--model id] [--cap credits]"
---

# /cs-upgrade-shots

Upgrade the shots in `$ARGUMENTS` with the `video-shot-upgrade` skill. Follow its workflow in order
and stop at every exit code that is not 0.

```bash
S=${CLAUDE_PLUGIN_ROOT}/skills/video-shot-upgrade/scripts
python3 $S/provider_adapter.py --shots <shots.json> --adapter <adapter> --model <id> --model-spec <model.json> --out <dir>/requests.json
python3 $S/budget_gate.py quote --requests <dir>/requests.json --quotes <dir>/quotes.json --brief <brief.json> --cap <cap> --balance <balance> --ledger <dir>/spend.json
```

Before any generate call: show the user every shot's price, the total, the cap and the paid-and-trimmed
seconds, then wait for the approval sentence the gate printed. Record it with `budget_gate.py approve`.
Run `budget_gate.py reserve` immediately before each generate call and `record` right after. Never
resubmit a timed-out call; poll the job. Finish with `drift_check.py` and report HOLDS / REVIEW / DRIFTED
per shot.
