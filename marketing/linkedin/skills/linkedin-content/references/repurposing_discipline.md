# Repurposing Discipline — one idea, many surfaces, no duplicates

Repurposing is the highest-leverage move available to anyone who already produces
work: a talk, an article, a README, an internal write-up, a customer call you
took notes on. It is also the fastest route to a feed that feels like a rerun.

The discipline has two halves. One is mechanical — splitting a source into units
that can stand alone. The other is editorial, and it is the half that gets
skipped: **the first-person sentence only you can write.**

---

## What makes a unit standalone

`repurpose_splitter.py` scores four things, each 25 points:

1. **Length in range** (240-2,400 characters). Under 240 there is not room for a
   claim and its evidence; over 2,400 it wants splitting again.
2. **No dangling reference.** A unit that opens with "This meant that…" or "As we
   saw above" refers to something the reader never saw. This is the single most
   common defect in repurposed material and it is invisible to the author, who
   has read the source.
3. **Evidence present.** A number, a duration, a measurable detail. A unit
   carrying no evidence can still work as an opinion post, but it is a different
   kind of post and should be routed as one.
4. **Three or more substantive sentences.** Below that it is a note.

A unit failing 2 or 4 is disqualified regardless of its total score. A dangling
opener fails in the feed no matter how good the evidence beneath it is.

## The reuse ledger

This is the part that matters and the part no other repurposing workflow has.

Repurposing fails in one specific way: the same idea goes out three times over
eight months, and the audience notices before the author does. It happens because
the source is long, the good units are memorable, and eight months is longer than
anyone's memory of what they posted.

`--ledger` stores a normalised content hash of every unit marked as posted, with
the date. Used units are skipped by default and shown with their date on request.
It is a small file and it prevents a specific, embarrassing, recurring failure.

```bash
# Split, see what is available
python3 scripts/repurpose_splitter.py --input talk-transcript.md --ledger .linkedin-ledger.json

# After publishing unit 2, record it
python3 scripts/repurpose_splitter.py --input talk-transcript.md \
  --ledger .linkedin-ledger.json --record 2 --posted-on 2026-08-25
```

Commit the ledger alongside the source if the source lives in a repo. It is
project state, not a cache.

## What you always have to add

Every unit the splitter produces is **source material, not a post**. The tool
will not write the missing part and should not: it is the only genuinely new
thing in a repurposed post.

The missing part is one of three sentences:

- **What it cost.** "We spent five weeks automating the wrong step."
- **What you assumed.** "I thought the delay was engineering capacity."
- **What you would do differently.** "I would instrument the handoffs first now."

A repurposed post without one of these reads as a summary of something else,
because that is what it is.

## Source types and what they yield

| Source | Typical yield | The specific risk |
|---|---|---|
| Conference talk transcript | 4-8 units | Spoken asides do not survive as text; the connective tissue is all dangling references |
| Long article / essay | 3-6 units | Sections written to build on each other rarely stand alone |
| Technical README or docs | 2-4 units | Instructional voice; needs the "why we needed this" frame added |
| Internal post-mortem | 2-5 units | **Consent and confidentiality first.** Anonymise, or get sign-off, or do not |
| Customer conversation notes | 1-3 units | Never quotable without permission. The pattern is publishable; the customer is not |
| Podcast appearance | 3-6 units | You do not own the recording; check before quoting at length |

## Cross-platform, not just within LinkedIn

The same source usually supports a LinkedIn post, a longer piece somewhere you
own, and a talk proposal. Sequence matters:

**LinkedIn first when** you want to test whether anyone cares before investing the
long-form time. The post is cheap and the response is informative.

**Owned platform first when** the artifact is the point and LinkedIn is
distribution. Publish there, then post the strongest unit on LinkedIn with the
link in the first comment.

What does not work is publishing the identical text in both places on the same
day. LinkedIn readers who follow you elsewhere see a duplicate, and the
LinkedIn version carries the link penalty for no gain.

## Frequency

A single strong source can carry a month of posting. It should not carry a
quarter. The signal that you have over-mined a source is that the units start
needing more setup than payload — that is the ledger telling you to go do
something new and write about that instead.

---

## Sources

1. Kleon, A. **Show Your Work!** — process as publishable material, and the case
   for surfacing the same work repeatedly in different forms.
2. Handley, A. **Everybody Writes** — repurposing as an editorial discipline
   rather than a content-volume tactic.
3. Vaynerchuk, G. **Jab, Jab, Jab, Right Hook** — platform-native adaptation;
   the same idea has to be re-formed, not re-pasted.
4. Nielsen Norman Group. **"How People Read Online"** — why a unit that assumes
   prior context fails for a scanning reader who has none.
5. Google Search Central. **Duplicate content guidance** — the mechanics of
   cross-posting identical text, and why canonical placement matters for anything
   you also own.
6. Ebbinghaus, H. **Über das Gedächtnis** (1885), forgetting curve — the
   empirical case for deliberate repetition, and the reason it must be spaced
   and varied rather than repeated verbatim.
7. LinkedIn. **Professional Community Policies** — repetitive posting of the same
   content is named as spam behaviour; the ledger is how you stay clear of it.
