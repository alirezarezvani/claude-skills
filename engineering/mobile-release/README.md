# mobile-release

Get an iOS or Android release through store review and roll it out without
widening a crash spike. Three stdlib Python scripts; no network, no store API.

| Script | What it stops |
|---|---|
| `ios_privacy_manifest_check.py` | Uploads refused for an undeclared required-reason API (ITMS-91053), invalid or SDK-only reason codes, a missing `NS...UsageDescription`, SDKs without their own manifest |
| `android_release_check.py` | targetSdk below Play's level for the date and form factor, intent-filter components without `android:exported`, debuggable builds, permissions needing a Play declaration, prebuilt `.so` files not 16 KB aligned |
| `rollout_gate.py` | Widening a staged or phased rollout while crash or ANR rates are above Play's thresholds or significantly worse than the last release |

```bash
/plugin install mobile-release@claude-code-skills
/cs-mobile-release ./app          # pre-submission check
/cs-rollout-gate rollout.csv      # PROCEED / HOLD / HALT
```

Rules were verified on 2026-11-17 against Apple and Android developer
documentation; each script prints that date. Store rules change yearly, so
re-check the official pages listed in `skills/mobile-release/references/`
after any date in the rule tables.

Agent: `cs-mobile-release`. License: MIT.
