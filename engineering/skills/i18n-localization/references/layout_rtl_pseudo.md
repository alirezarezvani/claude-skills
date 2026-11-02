# Layout, right-to-left and pseudo-localization

Confidence: 🟢 spec or vendor documentation, 🟡 practice.

## 1. Text grows, and short strings grow most

IBM's globalization guidelines, as republished by the W3C, give the size of
translated text relative to the English source [1]: up to 10 characters 200-300%,
11-20 180-200%, 21-30 160-180%, 31-50 140-160%, over 70 about 130%. (The 51-70 row
reads "151-170%" in the W3C copy, which breaks the pattern; treat it as roughly
135%.) German and Finnish run long, CJK runs short but taller. 🟢

`pseudo_localize.py` pads by the lower bound of that growth: +100% up to 10
characters, +80%, +60%, +40%, +35%, +30% above 70. A "Save" button that survives
the pseudo-locale survives German.

Design consequences 🟡: no fixed-width buttons or tabs around text, allow two
lines in table headers, never truncate without a tooltip or `title`, and leave
room in navigation bars.

## 2. Pseudo-localization

A pseudo-locale is generated, not translated, so it costs nothing and can run
before the first translator is hired [2][3].

| Pseudo-locale | Tests | Convention |
|---|---|---|
| `en-XA` accented + expanded + bracketed | untranslated strings stay plain ASCII; clipping; concatenation shows as `[[a]] [[b]]` | Android pseudolocale [2] |
| `ar-XB` mirrored (RLO-wrapped) | RTL layout, mirrored icons, bidi of embedded numbers | Android pseudolocale [2] |

Microsoft's equivalents are `qps-ploc` and `qps-plocm` [3]. Register the pseudo
locale only in development and QA builds.

Reading a pseudo-localized screen: plain English = hardcoded string; `[[...` with
no closing `]]` = truncation; two bracket pairs in one label = concatenation;
`{{name}}` visible = placeholder broken in the source.

## 3. Right-to-left

- Set `dir="rtl"` and `lang` on `<html>` for ar, he, fa, ur [4]. 🟢
- Use CSS logical properties (`margin-inline-start`, `padding-inline-end`,
  `inset-inline-start`, `text-align: start`) instead of left/right [5]. 🟢
- Mirror directional icons (back/forward arrows, progress), not universal ones
  (play button, checkmark, clock, logos). 🟡
- Wrap user-generated or mixed-direction content in `<bdi>` or `dir="auto"` so a
  Hebrew username does not reorder the punctuation around it [4][6]. 🟢
- Numbers stay left-to-right inside RTL text; phone numbers and code too. 🟢

## 4. Release checklist

1. `locale_sync.py` exits 0, or every remaining warning is accepted by name.
2. `hardcoded_strings.py` exits 0 on the changed folders.
3. The app was clicked through in `en-XA` (and `ar-XB` if an RTL locale ships).
4. Dates, numbers and currency show the target locale's separators.
5. The longest language was checked on the narrowest supported screen.
6. Fallback: a deleted key renders the source text, not the key name.

## Sources

1. W3C Internationalization, *Text size in translation* (IBM table). https://www.w3.org/International/articles/article-text-size/
2. Android Developers, *Test your app with pseudolocales*. https://developer.android.com/guide/topics/resources/pseudolocales
3. Microsoft Learn, *Pseudo-localization* (globalization testing). https://learn.microsoft.com/en-us/globalization/methodology/pseudolocalization
4. W3C Internationalization, *Structural markup and right-to-left text in HTML*. https://www.w3.org/International/questions/qa-html-dir
5. MDN Web Docs, *CSS logical properties and values*. https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values
6. W3C Internationalization, *Inline markup and bidirectional text in HTML*. https://www.w3.org/International/articles/inline-bidi-markup/
7. Material Design, *Bidirectionality*. https://m2.material.io/design/usability/bidirectionality.html
