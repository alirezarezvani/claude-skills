# Plurals and message syntax

What `locale_sync.py` checks, and why each check exists. Confidence: 🟢 normative
spec or vendor documentation, 🟡 widely observed practice.

## 1. Plural categories come from CLDR, not from English

Every locale picks from at most six categories: `zero`, `one`, `two`, `few`,
`many`, `other`. Which ones a locale uses, and which numbers select them, is
defined by Unicode CLDR [1][2] and exposed at runtime by `Intl.PluralRules` [7],
ICU [3] and i18next v21+ [4]. 🟢

| Locale | Categories (whole numbers) | Example |
|---|---|---|
| en, de, nl, sv | one (1), other | 1 file, 2 files |
| fr, pt (Brazil) | one (0 and 1), many (1,000,000+), other | 0 fichier, 1 fichier |
| es, it, ca, pt-PT | one (1), many (1,000,000+), other | 1 millón de |
| ru, uk, be | one (1, 21, 31), few (2-4, 22-24), many (0, 5-20, 25-30) | 1 файл, 2 файла, 5 файлов |
| pl | one (1 only), few (2-4, 22-24), many (0, 5-21) | 1 plik, 2 pliki, 5 plików |
| cs, sk | one (1), few (2-4), other; `many` is decimals only | 1 soubor, 2 soubory, 5 souborů |
| ar | zero, one, two, few (3-10), many (11-99), other (100+) | six forms |
| he | one, two, other | |
| ja, zh, ko, th, id, ms | other only | no plural inflection |

The script embeds the CLDR 49 table for all 225 locales and reports a missing
category only when a whole-number count can select it. Categories that only
apply to decimals (`many` in cs, `other` in ru) are not demanded. Categories that
only start at 1,000,000 (`many` in fr/es/it/pt) are a warning, not a blocker.

**Most common release defect 🟡:** a Russian, Polish, Ukrainian or Arabic file
created by copying the English `_one`/`_other` pair. It passes every key-count
check and prints "5 файла" (wrong case) for every count above 4.

## 2. ICU MessageFormat rules [3]

- `plural` and `select` must have an `other` branch. ICU treats a missing
  `other` as a syntax error; some runtimes fail only at format time. 🟢
- `zero {...}` is a **category**, not "the number 0". In English, `zero` is never
  selected, so `{n, plural, zero {No files} other {# files}}` prints "0 files".
  Write `=0 {No files}`. `=N` exact matches are checked before categories. 🟢
- `#` inside a plural branch is the formatted number (after `offset`). 🟢
- Apostrophes: ICU uses `DOUBLE_OPTIONAL` mode. A lone `'` is literal unless it
  precedes `{`, `}`, `#` (in plurals) or `|`; `''` is one apostrophe. 🟢
- `selectordinal` uses ordinal rules ("1st, 2nd, 3rd"), which differ from cardinal
  rules. The script parses it but does not check ordinal coverage.

**Java exception [6] 🟢:** `java.text.MessageFormat` (Java `.properties` with
`{0}` arguments) treats every single `'` as a quote. `Don't delete {0}` renders as
`Dont delete {0}`. Write `Don''t`. The script warns (`JAVA_APOSTROPHE`) only in
`.properties` files that contain `{n}` arguments.

## 3. Library-specific plural keys

| Stack | Shape | Notes |
|---|---|---|
| i18next v21+ (JSON v4) [4] | `items_one`, `items_few`, `items_other` | `_zero` is optional and used for count 0 in any language; `_ordinal_*` for ordinals |
| Android [5] | `<plurals><item quantity="few">` | `quantity` values are the CLDR categories; `zero` is ignored in English even if present |
| gettext [8] | `msgid_plural` + `msgstr[0..n-1]`, `Plural-Forms: nplurals=N; plural=...` | Form count and order come from the header formula, not from CLDR names |
| ICU / FormatJS / ARB | inline `{n, plural, ...}` | as in section 2 |

For gettext the script checks that every plural entry has `nplurals` non-empty
forms and warns when the header's `nplurals` differs from the number of CLDR
whole-number categories (ru 3, pl 3, ar 6, ja 1). Fuzzy entries are warned: GNU
`msgfmt` excludes them from the compiled catalogue unless `--use-fuzzy` is set [8].

## 4. Placeholder integrity

A translation must keep every placeholder of its source, by name: `{{name}}`
(i18next), `{name}` (ICU), `%(name)s` (Python), `%{name}` (Ruby/Rails),
`%1$s` (positional printf, Android/Java). Unnumbered printf (`%s ... %d`) must keep
the same order, because translators cannot reorder them; the fix is positional
`%1$s ... %2$d`, which Android and Apple both support [5]. 🟢

A plural variant may drop the number when the language writes it as a word
(Russian `one` → "один файл"), so a missing `{{count}}` in a non-`other` variant is
not reported; an unknown placeholder still is.

## Sources

1. Unicode CLDR, *Language Plural Rules* chart. https://www.unicode.org/cldr/charts/latest/supplemental/language_plural_rules.html
2. Unicode Technical Standard #35, Part 3 Numbers, *Language Plural Rules*. https://www.unicode.org/reports/tr35/tr35-numbers.html#Language_Plural_Rules
3. ICU User Guide, *Formatting Messages* (MessageFormat, apostrophe mode). https://unicode-org.github.io/icu/userguide/format_parse/messages/
4. i18next documentation, *Plurals*. https://www.i18next.com/translation-function/plurals
5. Android Developers, *String resources: Quantity strings (plurals)* and *Formatting strings*. https://developer.android.com/guide/topics/resources/string-resource
6. Oracle Java SE API, `java.text.MessageFormat` (quoting rules). https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/text/MessageFormat.html
7. MDN Web Docs, `Intl.PluralRules`. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules
8. GNU gettext manual, *Plural forms* and *Fuzzy Entries*. https://www.gnu.org/software/gettext/manual/html_node/Plural-forms.html
