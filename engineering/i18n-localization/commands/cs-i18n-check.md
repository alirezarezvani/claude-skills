---
disable-model-invocation: true
description: Check translation files and code before a release - missing keys, broken placeholders, CLDR plural forms, hardcoded UI strings.
argument-hint: "[locales dir] [source dir] [--source-locale en]"
---

# /cs-i18n-check

Check translation files and UI code before a release: `$ARGUMENTS` (default: the project's locales folder and `src/`).

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/i18n-localization/scripts/locale_sync.py <locales dir> --source-locale <source>
python ${CLAUDE_PLUGIN_ROOT}/skills/i18n-localization/scripts/hardcoded_strings.py <source dir>
```

## Report

1. The verdict line of each script.
2. Blockers grouped by locale, with file and key, and the fix for each (add the plural keys, restore the placeholder, use `=0`).
3. Hardcoded strings you checked and confirm are user-facing, with file:line. Name any you judged false positives.
4. Warnings, briefly. Do not fill missing translations with English or machine output; list them for a translator.
