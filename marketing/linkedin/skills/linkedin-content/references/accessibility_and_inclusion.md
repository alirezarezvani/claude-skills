# Accessibility and Inclusion — the part of LinkedIn craft nobody audits

LinkedIn is a professional network, which means a meaningful fraction of your
audience uses assistive technology at work — screen readers, captions,
magnification, high-contrast modes. It also means the accessibility failures in
LinkedIn posts are unusually visible, because they are almost all self-inflicted
by formatting tricks people adopt for reach.

`post_linter.py` treats two of these as blocking findings. This document is why.

---

## 1. Unicode pseudo-bold is the big one — blocking

LinkedIn does not support rich text in posts, so people paste text through "bold
text generators". Those tools do not bold anything. They substitute the Latin
letters for characters from the **Mathematical Alphanumeric Symbols** block
(U+1D400-U+1D7FF), which are visually similar and semantically unrelated.

What actually happens:

- **Screen readers** announce them individually as mathematical symbols —
  "mathematical sans-serif bold small a, mathematical sans-serif bold small b" —
  or skip them entirely, depending on the reader and its verbosity settings.
  A "bolded" heading becomes noise or silence.
- **Search** does not index them as the words they resemble. Your post about
  𝗸𝘂𝗯𝗲𝗿𝗻𝗲𝘁𝗲𝘀 does not match a search for kubernetes.
- **Copy-paste** into any system with real text handling produces mojibake.
- **Translation** fails.

There is no version of this that is worth it. Emphasis on LinkedIn comes from
line breaks, word order, and putting the important thing first — the same tools
every writer had before bold existed.

The same applies to fullwidth characters (Ａ-ｚ) and enclosed alphanumerics.

## 2. Alt text on images — LinkedIn supports it and will not write it

LinkedIn offers an alt-text field on image uploads. It is not filled in for you
and it is easy to skip.

Writing it well takes one sentence and one rule: **describe what the image
communicates, not what it is.** "Chart" is useless. "Line chart: median
onboarding time falling from 41 days in March to 4 days in July" is the whole
content of the image, delivered to someone who cannot see it — and, incidentally,
to anyone whose image failed to load.

For a document carousel, upload a real PDF with selectable text rather than
exported images. The text layer is what makes the slides readable to assistive
technology at all.

## 3. Video captions — the floor, and also just correct

Most feed video is watched sound-off, so captions serve everyone. LinkedIn
provides auto-captions with an editing step. **The editing step is not optional**:
auto-captioning mangles exactly the domain vocabulary your post is about, and an
uncorrected caption track is worse than none because it looks like a caption
track.

WCAG 2.2 SC 1.2.2 (Captions, Prerecorded) is the standard, and for a professional
audience it is also the polite minimum.

## 4. Emoji load — warning, not blocking

Emoji are read aloud by name. A bullet list built from 🔥 emoji becomes "fire,
fire, fire". A handful is fine and can even help structure. Fifteen makes a post
tiring to hear.

Where emoji do useful work: as list markers (one per line, consistently), or as a
segment separator in a headline. Where they do not: decoration, emphasis, or
replacing words.

## 5. ALL-CAPS lines — warning

Some screen readers spell out all-caps words letter by letter, treating them as
initialisms. A full line of capitals becomes an alphabet recital. Sentence case,
with the emphasis carried by the words.

## 6. Colour and contrast in carousels and images

If you make slides:

- Do not encode meaning in colour alone (WCAG 1.4.1). If the red bar is the bad
  one, label it.
- Body text on a slide needs 4.5:1 contrast against its background (WCAG 1.4.3);
  large text needs 3:1.
- Slide text should be large enough to read on a phone at feed size. If you have
  to zoom to read your own slide on your own phone, it is too small.

## 7. Plain language is an accessibility feature

Not only for non-native readers, though that is a large part of a global
professional audience. Dense sentences with three subordinate clauses are harder
for everyone, and much harder for anyone reading through a screen reader with no
ability to skim back.

Practical version: short sentences, one idea per paragraph, expand an acronym the
first time. This is the same advice as good writing, which is convenient.

## 8. What this costs

About four minutes per post: write the alt text, check the captions, do not paste
through a bold generator. It is the cheapest quality signal available and almost
nobody does it, which means it is also differentiating.

---

## Sources

1. W3C. **Web Content Accessibility Guidelines (WCAG) 2.2** — SC 1.1.1 (Non-text
   Content), 1.2.2 (Captions, Prerecorded), 1.4.1 (Use of Color), 1.4.3
   (Contrast Minimum).
2. Unicode Consortium. **Unicode Standard, Chapter 22 / Mathematical Alphanumeric
   Symbols (U+1D400-U+1D7FF)** — what these characters are actually for, and the
   explicit note that they are not styled Latin letters.
3. WebAIM. **Screen Reader User Survey** (recurring) — how screen-reader users
   actually navigate, and the cost of non-semantic text substitutes.
4. LinkedIn Help. **"Add alternative text to images"** and LinkedIn's video
   captioning documentation — what the platform supports.
5. LinkedIn. **Accessibility statement / LinkedIn Accessibility** — the
   platform's own commitments and the assistive-technology surfaces it supports.
6. Nielsen Norman Group. **"Plain Language Is for Everyone, Even Experts"** —
   comprehension gains from plain language across expertise levels.
7. Deque / axe accessibility documentation on **text alternatives and meaningful
   sequence** — practical guidance for writing alt text that carries the content
   rather than naming the object.
