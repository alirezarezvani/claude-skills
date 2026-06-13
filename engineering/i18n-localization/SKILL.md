---
name: i18n-localization
description: Use when adding or editing user-facing text, translation keys, or locale files; building a language switcher or locale-prefixed routing; formatting numbers, dates, or currency for display; or auditing locale files for drift. Triggers on "i18n", "internationalization", "localization", "translations", "locale files", "react-i18next", "i18next", "language switcher", "Intl.NumberFormat", "RTL", "missing translation key". Ships a stdlib locale-key-drift scanner.
---

# i18n / Localization

Every user-facing string is translatable, present in **all** locales, and rendered through the i18n layer — never hardcoded. The cost of i18n is near-zero when designed in from the first component and enormous when retrofitted. This skill makes that discipline executable and gives you a scanner that fails CI on locale drift.

Library-agnostic; examples use i18next / react-i18next and the platform `Intl` APIs. The principles port to any stack.

## When to use

- Adding or editing any user-facing text (labels, buttons, toasts, validation, `aria-label`s, empty/error states, titles, meta)
- Adding a new translation key or a new locale file
- Building language switching or locale-prefixed routing (`/:lang/...`)
- Formatting numbers, dates, times, or currency for display
- Rendering enum values or dynamic labels from the backend
- Auditing locale files before a release (run the scanner)

**When NOT to use:** internal logs, machine-readable error codes, telemetry, developer-only CLI output. Don't internationalize text no user reads.

## Core principle: route every string through one layer

```
source string -> t('semantic.key') -> per-locale JSON -> rendered UI
                           |
                 Intl.* for numbers/dates/currency (NOT translation keys)
```

A hardcoded label is a bug waiting for the second locale. A key present in one locale file but missing from another is a silent fallback gap only the missing-locale user sees.

## Quick start

```bash
# Audit locale files for drift before shipping (CI-friendly: exit 1 on drift)
python scripts/locale_key_drift.py ./public/locales --base en
python scripts/locale_key_drift.py ./src/locales --json > i18n-drift.json
```

The scanner reports, per locale, the four failure modes that ship broken translations: **missing keys**, **extra keys**, **empty values**, and **placeholder mismatches** (e.g. base `{{count}}` vs translation `{{cnt}}`). Exit `0` = in sync, `1` = drift, `2` = error.

## The seven rules

1. **No hardcoded user-facing strings.** Route every label/message through `t('...')` / `<Trans>`. This includes placeholders, `aria-label`s, toasts, validation messages, and empty/error states.
2. **One source of truth for languages.** Keep the supported-language list and the default/fallback in a single config module and import it. Validate any language code read from storage or the URL before use.
3. **Every key lives in every locale.** Adding a key means adding it to all locale files in the same commit. The scanner enforces this.
4. **Stable, semantic keys.** Dot-path nesting grouped by feature (`cargo.searchPlaceholder`) plus a shared bucket (`common.save`). camelCase keys; reserve `UPPER_SNAKE_CASE` for enum-value keys.
5. **Interpolation, not concatenation.** Use `{{var}}` placeholders so word order can vary per language. Never build sentences with `+`.
6. **Pluralization via the library.** Use i18next plural suffixes (`items_one` / `items_other`), not hand-rolled singular/plural keys.
7. **Format with `Intl`, not keys.** Numbers, dates, and currency go through `Intl.NumberFormat` / `Intl.DateTimeFormat` with a BCP-47 locale — never stored as translation strings.

## Setup (i18next example)

```ts
export const LANGS = ['en', 'ru', 'es'] as const;
export type Lang = (typeof LANGS)[number];
export const DEFAULT_LANG: Lang = 'en';
export const isLang = (v: string): v is Lang => (LANGS as readonly string[]).includes(v);

i18n.use(httpBackend).use(initReactI18next).init({
  supportedLngs: LANGS,
  fallbackLng: DEFAULT_LANG,
  lng: isLang(saved) ? saved : DEFAULT_LANG,      // validated on read
  interpolation: { escapeValue: false },           // the view layer already escapes
  backend: { loadPath: '/locales/{{lng}}.json' },  // lazy-load per language
});
```

## Consuming translations

```tsx
const { t } = useTranslation();
<input placeholder={t('cargo.searchPlaceholder')} />
<span>{t('items.count', { count })}</span>          // interpolation + plural
t('actions.reset', { defaultValue: 'Reset' });       // inline fallback for safety
```

Rich text with embedded markup uses `<Trans i18nKey="...">`.

## Backend enums / dynamic labels

Never render a raw enum string from the API. Normalize it and look up a key with a graceful default:

```ts
export function enumLabel(t: TFunction, group: string, raw: string): string {
  const key = raw.trim().toUpperCase().replace(/[\s-]+/g, '_');
  return key ? t(`${group}.${key}`, { defaultValue: raw.replace(/_/g, ' ') }) : '—';
}
```

When the backend localizes a value itself (`{ name_en, name_ru }`), select by current language with a fallback chain (`current → default → first available`).

## Number / date / currency

```ts
new Intl.NumberFormat(bcp47, { style: 'currency', currency: 'USD' }).format(amount);
new Intl.DateTimeFormat(bcp47, { dateStyle: 'medium' }).format(date);
```

Map app language codes to BCP-47 locales (`en → en-US`).

## Workflows

### Workflow 1: Add a translated string
```
1. Pick a semantic key (feature.thing), not the English text as the key
2. Add it to EVERY locale file (translate or copy English as placeholder)
3. Render via t('feature.thing') — never the literal
4. Run locale_key_drift.py — must be in sync before commit
```

### Workflow 2: Pre-release locale audit
```
1. python scripts/locale_key_drift.py ./public/locales --base en --json > drift.json
2. Fix every missing key (add translation), extra key (remove or re-add to base),
   empty value (translate), placeholder mismatch (align tokens to base)
3. Re-run until exit 0; wire the command into CI as a required check
```

## Anti-patterns

- **Hardcoded string "just this once"** — the first one sets the pattern; wire `t()` from day one.
- **Adding a key to only the English file** — ships a silent fallback gap. Add to all locales in the same commit.
- **English text as the key** (`t('Save changes')`) — breaks when the copy changes; use semantic keys.
- **Concatenating sentences** (`t('You have') + count + t('items')`) — untranslatable word order; use interpolation.
- **Formatting dates/numbers with template strings** — locale rules differ; use `Intl`.
- **Rendering raw API enum values** — map them through a helper with a fallback.
- **Trusting a language code from the URL/storage unvalidated** — validate against the supported list, fall back to default.

## Verifiable success

- `locale_key_drift.py --base <default>` returns exit 0 (zero missing/extra/empty/placeholder issues) and runs in CI
- No user-facing string literal bypasses the translation layer (grep the diff for quoted UI text)
- All locale files share an identical key set; counts/plurals use interpolation
- Numbers, dates, and currency render through `Intl` with a BCP-47 locale

## References

- `references/i18n-patterns.md` — namespaces vs flat files, RTL handling, locale routing, SSR/Next.js notes, pluralization details

## Cross-references

- `engineering-team/a11y-audit` — pair i18n with accessibility (translated `aria-label`s, RTL + screen readers)
- `engineering-team/senior-frontend` — broader frontend architecture this slots into
- `product-team/ui-design-system` — design tokens and components that consume localized strings
