# Post Formats Canon — what each native format is good at

Format is usually chosen by fashion. "Carousels are working right now" is the
single most common reason a person makes a carousel, and it is why most carousels
are a text post cut into slides.

The useful question is not which format performs best in general. It is which
format the material you actually have can support, in the time you actually have.

---

## The nine native formats

### Plain text post
**Good at:** stories, opinions, single ideas, anything where the words are the
point. The default, and it should be.
**Cost:** ~25 minutes including revision.
**Constraint:** one idea. If it needs two, it is two posts.

### Document post (PDF carousel)
**Good at:** step sequences, comparisons, data with structure, anything
inherently visual.
**Cost:** ~90 minutes.
**Constraints:** every slide must survive alone — most readers swipe two and
leave, so the payload cannot live on slide nine. Upload a real PDF with
selectable text rather than exported images: text is accessible, indexed, and
readable when a slide is zoomed. Slide one is the hook, and it is subject to the
same test as a text hook.

### Native video
**Good at:** demonstration, personality, anything where seeing it beats reading it.
**Cost:** ~120 minutes for anything watchable.
**Constraints:** captions are mandatory — most feed viewing is sound-off, and
captions are also the accessibility floor. Say the point in the first five
seconds; the fold applies to video too, it is just measured in seconds.

### Single image + text
**Good at:** one chart, one photo, one artifact. Announcements.
**Cost:** ~30 minutes.
**Constraint:** write alt text. LinkedIn supports it and does not generate it for
you. A chart with no alt text excludes readers and says nothing to anyone whose
image fails to load.

### Poll
**Good at:** settling a real question you will report back on.
**Cost:** ~10 minutes.
**Constraint:** `format_picker.py` refuses a poll without a declared decision.
A poll you do not follow up on is a reach trick with a two-week half-life, and
readers have learned to recognise it. The follow-up post — "here is what 400 of
you said, and here is what we changed" — is the actual content.

### Long-form article
**Good at:** the durable artifact. A link you will still send someone in two
years.
**Cost:** ~180 minutes.
**Constraint:** articles reach far fewer people than posts. Write one when the
artifact matters more than this week's impressions, and then mine it for posts.

### Newsletter issue
**Good at:** a returning readership.
**Cost:** ~150 minutes, plus a standing promise. See `newsletter_playbook.md`.

### Substantive comment on someone else's post
**Good at:** visibility from a standing start. The most under-rated format on the
platform and the cheapest by an order of magnitude.
**Cost:** ~6 minutes.
**Constraint:** it has to add something the original missed. Agreement is not a
comment.

### Repost with your own take
**Good at:** entering a conversation someone else started, with a position.
**Cost:** ~15 minutes.
**Constraint:** your take must be longer than "this". A bare repost spends your
credibility on someone else's idea and returns nothing.

---

## Choosing

`format_picker.py` scores goal fit against material fit and refuses what the time
budget cannot pay for. Two refusals are hard:

- **Video with no camera and no footage.** Not a judgement about your face; a
  refusal to plan work that will not happen.
- **A poll with no real decision behind it.**

When two formats score within a point, the tool asks rather than picking. The
tie-breaker is which one you would actually enjoy making, because the one you
repeat beats the one that scores higher once.

## The carousel trap

Carousels reliably out-perform on engagement rate in third-party data, which
produces a predictable failure: people convert text posts into carousels for the
reach and end up with ten slides carrying two slides of content.

The test: **could a reader get the value from slide one plus the caption?** If
yes, it is a text post and the extra nine slides are cost. If no — if the
sequence itself is the content — it is a carousel.

## Video captions are not optional

Beyond accessibility: the majority of feed video is watched sound-off. An
uncaptioned video is a silent film with no intertitles. LinkedIn offers
auto-captions with an edit step; the edit step is not optional either, because
auto-captions mangle exactly the domain terms your post is about.

## Cross-format sequencing

A single body of work supports a sequence, and the sequence out-performs any one
piece:

1. **Text post** with the specific finding (cheap, tests appetite)
2. **Carousel** with the full method, two weeks later, if the post landed
3. **Article or newsletter issue** as the durable artifact
4. **Comments** on other people's related posts throughout, linking nothing

Run the source through `repurpose_splitter.py` with a ledger so the same unit
does not go out twice under two different formats.

---

## Sources

1. Tufte, E. **The Visual Display of Quantitative Information** — data-ink ratio,
   the direct argument against a carousel slide that carries one sentence.
2. Tufte, E. **The Cognitive Style of PowerPoint** — the specific failure of
   slide sequences that fragment an argument into bullet residue.
3. Nielsen Norman Group. **"How People Read Online"** and mobile reading
   research — scanning and the cost of sequential reveal.
4. W3C. **Web Content Accessibility Guidelines (WCAG) 2.2**, SC 1.1.1 (Non-text
   Content) and 1.2.2 (Captions, Prerecorded) — the floor for images and video.
5. LinkedIn Help. **"Add alternative text to images"** and LinkedIn's video
   caption documentation — what the platform supports and what it does not do
   for you.
6. van der Blom, R. **Algorithm Insights** (annual) — 🟡 comparative format
   performance in public-post samples; directionally useful, not a specification.
7. Kleon, A. **Show Your Work!** — process content as the material most formats
   are actually best at carrying.
