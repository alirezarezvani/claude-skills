# i18n-localization

Ship a new language without the usual breakage: keys that never got synced,
placeholders a translator renamed, Russian and Arabic files with English's two
plural forms, UI text that never went through `t()`, and buttons that clip in German.

## What it does

| Script | Job | Blocks on |
|---|---|---|
| `locale_sync.py` | Compares each locale file with the source locale: JSON/ARB (i18next, ICU), `.properties`, `.strings`, Android `strings.xml`, gettext `.po` | Missing/empty keys, renamed placeholders, ICU syntax, no `other`, `zero` that never matches, plural categories the locale needs (CLDR 49 embedded) |
| `hardcoded_strings.py` | Scans React, Vue, Svelte and HTML for text that skips the translation layer | Literal text between tags, literal `placeholder`/`alt`/`aria-label`/`title` |
| `pseudo_localize.py` | Builds an `en-XA` (accented, expanded, bracketed) or `ar-XB` (right-to-left) pseudo-locale | nothing; it writes a file |

All three are stdlib Python with no network access, and none of them translates
text. Each supports `--help`, `--sample` and `--output json`.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install i18n-localization@claude-code-skills
```

Commands: `/cs-i18n-check` (release check) and `/cs-pseudo-locale`. Agent:
`cs-i18n-engineer`. A CI example is in `skills/i18n-localization/assets/i18n-gate.yml`.

## Limits

- `hardcoded_strings.py` reads source text, not an AST. On two held-out codebases
  it was measured before tuning at 20/20 true positives for text between tags,
  17/20 for attributes and 15/20 for expression literals (which are warnings).
  Read each finding.
- Ordinal plurals (`selectordinal`, `_ordinal_*`) are parsed but not checked for coverage.
- YAML locale files (Rails) are not read; convert to JSON for the check.
- No check can tell whether a translation is correct, only whether it is complete and well-formed.

## Origin

Requested in issue #849. Built independently from public sources (Unicode CLDR,
ICU, ECMA-402, i18next, Android, GNU gettext, W3C Internationalization); no code
or text from the requester's fork was used.

MIT © Alireza Rezvani
