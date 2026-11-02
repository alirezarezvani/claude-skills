# String routing and locale-aware formatting

The rules `hardcoded_strings.py` enforces, plus the ones it cannot see. Confidence:
🟢 spec or vendor documentation, 🟡 established practice.

## 1. Every user-facing string goes through the translation function

Text nodes, `placeholder`, `title`, `alt`, `aria-label` and toast/error messages
are all user-facing. `aria-label` and `alt` matter twice: screen-reader users hear
them, so an untranslated label fails WCAG 3.1.2 *Language of Parts* for that user
unless it is marked with its own `lang` [6]. 🟢

Not user-facing, never translate: CSS classes, test ids, event names, analytics
keys, log messages read by engineers, enum values compared in code, URLs.

**Adoption order 🟡:** run the scanner with `--warn-only` on a legacy codebase,
fix one feature folder at a time, then switch to blocking mode in CI so the count
can only go down.

## 2. Never build a sentence by concatenation

`t('deleted') + ' ' + count + ' ' + t('files')` assumes English word order and
English plural rules. German puts the verb last, Japanese has no plural, Russian
needs three forms. Use one message with named placeholders and a plural branch:
`t('files_deleted', { count })`. 🟢 [1][2]

Also flagged by the scanner: `${t('a')} ${name}` template literals mixing
translated and raw parts. A label plus a keyboard shortcut ("Bold — Ctrl+B") is a
common legitimate case; keep it, but put the separator inside the message.

## 3. Format with the user's locale, explicitly

| Value | Do | Don't |
|---|---|---|
| Date/time | `new Intl.DateTimeFormat(locale, { dateStyle: 'medium' })` | `date.toLocaleDateString()` (runtime default locale), `'MM/dd/yyyy'` |
| Number | `new Intl.NumberFormat(locale).format(n)` | `n.toFixed(2)` (always `.` decimal) |
| Currency | `new Intl.NumberFormat(locale, { style: 'currency', currency })` | `'$' + amount` (symbol position, spacing and decimals vary: `1.234,56 €`) |
| Relative time | `Intl.RelativeTimeFormat` | hand-built "3 days ago" |
| Lists | `Intl.ListFormat` | `items.join(', ')` + "and" |
| Sorting | `Intl.Collator(locale).compare` | `a < b` (code-point order) |

`toLocaleString()` with no argument uses the browser's or server's locale, not
the language the user picked in your app, and gives different output in SSR and
the client (hydration mismatch). Pass the app locale every time. 🟢 [1][2]

The currency **code** belongs to the data (what the customer pays), never derived
from the UI locale: a German user looking at a USD invoice must see `1.234,56 $`,
not euros. 🟢 [1]

## 4. Locale identifiers and fallback

- Use BCP 47 tags (`pt-BR`, `zh-Hant-TW`, `sr-Latn`) [3]. Android directories use
  `values-pt-rBR` / `values-b+sr+Latn`; Apple uses `pt-BR.lproj`.
- Negotiate with a fallback chain (`de-AT` → `de` → source), RFC 4647 *lookup* [4].
  A missing key must fall back to the source language, never render the key name.
- `zh` alone is ambiguous between Simplified and Traditional: ship script subtags.
- Set `<html lang>` from the active locale (hyphenation, font selection, screen
  reader voice) [5][6].

## 5. What the scanner cannot see

- Strings built on the server (emails, PDFs, push notifications) and stored in the
  database (category names, plan names): they need their own translation path.
- Images containing text, and icons whose meaning is cultural.
- Case mapping: Turkish dotted/dotless i (`"i".toUpperCase()` is `İ` in `tr`).
  Use `toLocaleUpperCase(locale)` [2].
- Text truncated with fixed widths: use the pseudo-locale (see `layout_rtl_pseudo.md`).

## Sources

1. MDN Web Docs, `Intl` (DateTimeFormat, NumberFormat, RelativeTimeFormat, ListFormat, Collator). https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl
2. ECMA-402, *ECMAScript Internationalization API Specification*. https://tc39.es/ecma402/
3. IETF RFC 5646 (BCP 47), *Tags for Identifying Languages*. https://www.rfc-editor.org/rfc/rfc5646
4. IETF RFC 4647, *Matching of Language Tags* (lookup and filtering). https://www.rfc-editor.org/rfc/rfc4647
5. W3C Internationalization, *Language tags in HTML and XML*. https://www.w3.org/International/articles/language-tags/
6. W3C, WCAG 2.2 Success Criteria 3.1.1 *Language of Page* and 3.1.2 *Language of Parts*. https://www.w3.org/TR/WCAG22/#language-of-page
7. Unicode CLDR project (locale data behind Intl and ICU). https://cldr.unicode.org/
