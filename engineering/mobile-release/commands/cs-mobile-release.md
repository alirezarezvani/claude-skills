---
disable-model-invocation: true
description: Check an iOS and/or Android project against App Store and Google Play submission rules before upload.
argument-hint: "[project root] [--form-factor phone|wear|tv|automotive|xr]"
---

# /cs-mobile-release

Pre-submission check for the app in `$ARGUMENTS` (default: the current repo). Find the iOS folder (has `*.xcodeproj` or `Package.swift`) and the Android folder (has `settings.gradle*`), then run what applies:

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/mobile-release/scripts/ios_privacy_manifest_check.py --project <ios dir>
python ${CLAUDE_PLUGIN_ROOT}/skills/mobile-release/scripts/android_release_check.py --project <android dir>
```

## Report

1. Verdict line per platform and the rules-verified date.
2. Each BLOCKER with file and line and the fix. For reason codes, the candidate reasons and what the code actually does; do not pick one you cannot justify from the code.
3. Store-console tasks the repo cannot fix (Play declarations, Data safety, App Store privacy label).
4. Any date in the rule tables that has already passed or is within 60 days.
