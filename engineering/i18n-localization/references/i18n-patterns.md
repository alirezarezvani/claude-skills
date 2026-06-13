# i18n Patterns — detailed reference

Detailed material that backs the workflows in `SKILL.md`. Library-agnostic; examples use i18next / react-i18next and the platform `Intl` APIs.

## Namespaces vs a single flat file

Decide up front and stay consistent:

| Approach | Use when | Trade-off |
|---|---|---|
| **Single flat file** per language (dot-path nesting) | Small/medium apps, < ~500 keys | Simplest; one HTTP request per language |
| **Namespaces** (multiple files per language, e.g. `common`, `dashboard`, `billing`) | Large apps, code-split routes | Lazy-load per route; more files to keep in sync |

With namespaces, load the namespace a route needs rather than the whole catalog. Keep file *shapes* identical across languages within each namespace.

## Key naming

- Group by screen/feature: `cargo.list.searchPlaceholder`, `billing.invoice.downloadCta`.
- Shared/reusable strings go in `common.*` (`common.save`, `common.cancel`, `common.loading`).
- camelCase segments. Reserve `UPPER_SNAKE_CASE` for enum-value keys so they line up with backend enums.
- Never use the English copy as the key — semantic keys survive copy edits.

## Pluralization

i18next selects the plural form from the `count` option using CLDR plural categories:

```jsonc
// en.json
{ "items_one": "{{count}} item", "items_other": "{{count}} items" }
// ru.json — Russian has one/few/many
{ "items_one": "{{count}} элемент", "items_few": "{{count}} элемента", "items_many": "{{count}} элементов" }
```

```ts
t('items', { count }); // picks _one / _few / _many / _other automatically
```

Never hand-roll `if (count === 1)` in the component — let the library apply the locale's CLDR rules.

## Number / date / currency with Intl

```ts
const bcp47 = { en: 'en-US', ru: 'ru-RU', es: 'es-ES' }[lang];

new Intl.NumberFormat(bcp47).format(1234567.89);                       // 1,234,567.89 / 1 234 567,89
new Intl.NumberFormat(bcp47, { style: 'currency', currency: 'EUR' }).format(9.9);
new Intl.DateTimeFormat(bcp47, { dateStyle: 'medium', timeStyle: 'short' }).format(new Date());
new Intl.RelativeTimeFormat(bcp47, { numeric: 'auto' }).format(-1, 'day'); // "yesterday"
```

Currency code is data, not locale — pass it explicitly. Map app language codes to BCP-47 once, in your language config.

## Locale-prefixed routing

When the language lives in the URL (`/:lang/...`):

1. A provider reads the `:lang` segment.
2. Validates it against the supported list (`isLang`).
3. Calls `changeLanguage(lang)` and persists it.
4. Redirects bare or invalid paths to a valid prefix (`/` → `/en/`).

Build internal links through typed path helpers that inject the active prefix — never hardcode `/en/...`.

Send the active language to the backend via a request header (`Accept-Language` or a custom `X-Language`) so server-rendered messages match the client. If a language isn't supported server-side yet, map it to a supported one for the header while still localizing fully on the client.

## Right-to-left (RTL)

- Set `dir="rtl"` on `<html>` for RTL languages (ar, he, fa, ur); drive it from the language config, not per-component.
- Use CSS logical properties (`margin-inline-start`, `padding-inline-end`, `inset-inline`) instead of physical `left`/`right` so layouts mirror automatically.
- RTL detection belongs in the same single language config as the supported-language list.
- Legitimate RTL text uses the inherent directionality of the script — do **not** insert explicit Unicode bidi override characters to "fix" rendering.

## SSR / Next.js notes

- Initialize i18n per request on the server; never share a mutable language instance across requests (it leaks one user's language to another).
- Pass the resolved language and the needed namespace(s) to the client to avoid a flash of the default language.
- Prefer Server Components for static localized content; keep the `t` usage that needs interactivity in client components.

## Missing-key strategy

- In development, configure the library to surface missing keys loudly (a `missingKeyHandler` that logs).
- In production, fall back to the default language and log to telemetry — never render the raw key to the user.
- Gate merges on `scripts/locale_key_drift.py` so missing keys are caught before they ship, not in production logs.
