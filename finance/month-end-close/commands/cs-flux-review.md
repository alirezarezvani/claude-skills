---
description: Just the flux gate - mark material fluctuations by your threshold rule and return every explanation that is missing, boilerplate, unquantified or unevidenced.
argument-hint: "tb_compare.csv [--pct N --abs N --rule and|or --compare prior|budget --reviewer NAME]"
---

# /cs-flux-review

Answer one question about `$ARGUMENTS`: **is every material fluctuation explained well enough to sign?**

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/month-end-close/scripts/flux_analyzer.py --input <tb_compare.csv> --pct <policy> --abs <policy> [--rule and|or] --reviewer <name>
```

If no thresholds were given, ask for the entity's policy. Do not present the defaults as a standard.

## What blocks (exit 4)

- A material account whose explanation is missing, boilerplate ("timing", "in line with expectations"), or has no number.
- A material account owned by the reviewer: nobody reviews their own explanation.

## What warns (exit 2)

- An explanation with a driver but no supporting document.

## Report

Verdict first, then a table of material accounts with change, rule that fired, explanation status, and what a
passing explanation would add. Do not write the explanation for them; the owner of the account does.
