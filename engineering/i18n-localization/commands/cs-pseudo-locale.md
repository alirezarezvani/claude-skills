---
disable-model-invocation: true
description: Generate an en-XA (or ar-XB right-to-left) pseudo-locale from the source strings to find hardcoded text, truncation and concatenation in the running UI.
argument-hint: "<source locale file> [--bidi]"
---

# /cs-pseudo-locale

Generate a pseudo-locale from the source locale file in `$ARGUMENTS` and register it for development builds.

```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/i18n-localization/scripts/pseudo_localize.py <source file> -o <locales>/en-XA/<name>
python ${CLAUDE_PLUGIN_ROOT}/skills/i18n-localization/scripts/pseudo_localize.py <source file> --bidi -o <locales>/ar-XB/<name>   # RTL
```

Register the pseudo-locale in the i18n config for development builds only, then tell the user what to look for:

- plain, unaccented English: a hardcoded string
- `[[...` with no closing `]]`: truncated text
- two `[[ ]]` pairs in one label: runtime concatenation
- broken layout in `ar-XB`: left/right CSS instead of logical properties
