---
name: i18n-localization
description: Use when adding UI text, adding or shipping a language, reviewing translation files, or building i18n into an app. Checks missing keys, placeholders and CLDR plural forms with locale_sync.py, finds hardcoded strings with hardcoded_strings.py, and builds a pseudo-locale with pseudo_localize.py.
argument-hint: "[locales dir | source dir | release check]"
license: MIT
metadata:
  version: 1.0.0
  build_pattern: "Three deterministic stdlib scripts (translation-file checker with the CLDR 49 plural table embedded, hardcoded-string scanner for React/Vue/Svelte/HTML, pseudo-locale generator) with blocking exit codes; rules cited to Unicode CLDR and UTS #35, ICU MessageFormat, ECMA-402/MDN Intl, i18next, Android and gettext docs, W3C Internationalization and WCAG 3.1"
  distinct_from: "a11y-audit (WCAG in source; this checks the translation layer and lang/dir only as they affect i18n); email-template-builder (localizes one email template); marketing localization and transcreation skills (copy, not code)"
---

# i18n Localization

> **Portability:** 3 stdlib Python scripts. No network, no translation service.
> They check and generate files; they never translate text or call an API.

A release with a new language usually breaks in the same places: keys added in
English and never synced, a placeholder renamed by a translator, Russian or
Arabic files that copied English's two plural forms, UI text that never went
through `t()`, and dates formatted in the server's locale. This skill makes each
of those a check that fails before the release, not a bug report after it.

## Workflow

```bash
# 1 - Translation files: keys, placeholders, ICU syntax, CLDR plural forms
python scripts/locale_sync.py locales/ --source-locale en
# 2 - Code: user-facing text that bypasses t(), concatenation, locale-less formatting
python scripts/hardcoded_strings.py src/
# 3 - Layout: generate a pseudo-locale and click through the app in it
python scripts/pseudo_localize.py locales/en/common.json -o locales/en-XA/common.json
python scripts/pseudo_localize.py locales/en/common.json --bidi -o locales/ar-XB/common.json
```

**Step 1** reads JSON/ARB (i18next or ICU), `.properties`, Apple `.strings`,
Android `strings.xml` and gettext `.po`, pairs each target with the source file of
the same namespace, and blocks on missing or empty keys, changed placeholders,
ICU syntax errors, plural/select without `other`, a `zero` branch that can never
match, and plural categories the target locale needs (ru `few`/`many`, ar six
forms), using the embedded CLDR 49 table. Untranslated values, orphan keys,
fuzzy entries and markup drift are warnings.

**Step 2** blocks on literal text between tags and literal user-facing
attributes (`placeholder`, `alt`, `aria-label`, `title`...), and warns on
literals rendered from `{cond ? 'Saving...' : ...}`, `t('a') + x` concatenation,
`toLocaleString()` with no locale, `'$' + amount` and hardcoded date patterns.
It is a text heuristic: read each finding. Use `--warn-only` to adopt it on a
legacy codebase, `i18n-ignore` on a line, and `.i18n-allow` for brand names.

**Step 3** accents, pads (by translation-growth rates) and brackets every string
while keeping placeholders and ICU syntax intact. Plain English on screen is a
hardcoded string; a cut-off `[[...` is truncation; `[[a]] [[b]]` is concatenation.

## Hard rules

- **Never concatenate translated fragments.** One message per sentence, with named placeholders and a plural branch.
- **Plural forms follow CLDR for the target locale**, not English. Never copy `_one`/`_other` into ru, pl, uk, cs, ar, he files and call them done.
- **`=0`, not `zero`,** for an empty-count message in ICU.
- **Pass the locale to every formatter.** Currency comes from the data, not the UI locale.
- **Placeholders are code.** A translator may move them, never rename or drop them; use positional `%1$s` where order can change.
- **Do not machine-translate to make the checker pass.** A missing translation falls back to the source language; a wrong one ships silently. Mark gaps for a translator instead.

## Scripts

| Script | Role | Exit codes |
|---|---|---|
| `scripts/locale_sync.py` | Translation files vs source locale: keys, placeholders, ICU, CLDR plurals, gettext | 0 · 2 warnings · 3 bad input · 4 blocked |
| `scripts/hardcoded_strings.py` | React/Vue/Svelte/HTML: untranslated text, concatenation, locale-less formatting | 0 · 2 · 3 · 4 |
| `scripts/pseudo_localize.py` | `en-XA` (or `--bidi` `ar-XB`) pseudo-locale from JSON/ARB/.properties | 0 · 3 |

All support `--help`, `--sample` and `--output json`.

## References and assets

- [`references/plurals_and_messages.md`](references/plurals_and_messages.md): CLDR categories per locale, ICU rules, library key shapes, placeholders (8 sources)
- [`references/string_routing_and_formatting.md`](references/string_routing_and_formatting.md): what to route through `t()`, Intl formatting, BCP 47 and fallback (7)
- [`references/layout_rtl_pseudo.md`](references/layout_rtl_pseudo.md): text expansion, pseudo-locales, RTL, release checklist (7)
- [`assets/i18n-gate.yml`](assets/i18n-gate.yml): CI job example
- [`assets/i18n-allow.example`](assets/i18n-allow.example): allowlist format
