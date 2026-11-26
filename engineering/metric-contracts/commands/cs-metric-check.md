---
disable-model-invocation: true
description: Check metric definitions (dbt semantic_manifest.json or a contract JSON) - lint all 13 rules and, with --base, classify what a change does to the numbers and who to warn.
argument-hint: "<semantic_manifest.json|contract.json> [--base base.json] [--manifest manifest.json]"
---

# /cs-metric-check

Lint the definitions in `$ARGUMENTS`:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/metric-contracts/scripts/metric_contract_lint.py --input <file>
```

If a base version was given, also diff it:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/metric-contracts/scripts/metric_diff.py --base <base> --head <file> [--manifest <manifest.json>]
```

dbt users without an artifact: run `dbt parse` (no warehouse query) and use `target/semantic_manifest.json`; for the base, parse the main branch in a worktree.

## Report

Verdict first. Then each ERROR and each BREAKING, REMOVED or RENAMED metric with its owner, the field that changed and the consumers to tell. For each breaking change, offer to fill `${CLAUDE_PLUGIN_ROOT}/skills/metric-contracts/assets/metric_change_notice.md`.
