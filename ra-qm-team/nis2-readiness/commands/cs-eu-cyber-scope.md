---
disable-model-invocation: true
description: Route one company and one event across NIS2, DORA, CRA and GDPR - which laws apply, which reporting clocks run in parallel, and who receives what.
argument-hint: "profile.json (or describe: sector, size, entity type, products, the event and when you knew)"
---

# /cs-eu-cyber-scope

For `$ARGUMENTS`, answer: **which EU cyber laws apply, and if something happened, which reports are due to whom and when?**

If the user describes the company instead of giving a file, pass the facts as flags (see `--help`).

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/nis2-readiness/scripts/eu_cyber_regime_router.py --profile <profile.json>
```

## Report

1. Each regime that applies and why, with lex specialis notes (DORA over NIS2).
2. The parallel clocks, earliest first, with recipients.
3. Open questions the user must answer (e.g. a CSIRT copy of DORA reports, weekend relief).
4. Which skill to run next: `nis2-readiness`, `dora-readiness`, `cra-readiness`, `gdpr-dsgvo-expert`.

Not legal advice; national transpositions differ.
