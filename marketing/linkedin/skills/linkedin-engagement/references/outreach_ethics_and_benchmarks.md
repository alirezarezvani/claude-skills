# Outreach Ethics and Benchmarks — what the numbers say, and what they cost

Cold outreach on LinkedIn works and is widely hated, and both facts have the same
cause: it is cheap to send and expensive to receive. The volume that makes it
economically attractive is the volume that makes it spam, and the platform
enforces against the pattern rather than the intent.

This document holds the numbers, with their provenance, and the rules that keep
the practice on the right side of the line.

---

## The benchmarks, with a correction

Third-party outreach studies are large but self-selected: the data comes from
users of outreach tooling, measured by the vendors of that tooling. Treat all of
it 🟡.

| Metric | Reported | Source class |
|---|---|---|
| Connection acceptance, platform-wide average | ~26-29% | 🟡 multi-million-touch vendor datasets |
| Acceptance with a personalised note | ~26.4% | 🟡 same |
| Acceptance with **no** note | ~26.4% | 🟡 same |
| Post-accept reply rate, **without** a note | ~5.4% | 🟡 |
| Post-accept reply rate, **with** a note | ~9.4% | 🟡 |
| Cold InMail response | 10-25% typical | 🟡 |
| Individually sent vs bulk InMail | ~15% higher response individually | 🟢 LinkedIn-reported |

**The correction that matters.** The widely repeated claim is that a personalised
note roughly triples acceptance (≈45% vs ≈15%). The largest available datasets do
not support it: acceptance is close to identical either way (26.42% vs 26.37% in
one ~13M-touch sample). What the note does move — and moves a lot — is the
**reply rate after acceptance**, roughly 5.4% → 9.4%.

The practical conclusion is the same as the folklore's, but the reasoning is
different and it changes what you write. **The note is not there to get the
connection. It is there to earn the conversation.** Which means it should be
about them and about why this conversation, not about you and what you sell.

`outreach_message_builder.py` encodes exactly this: it refuses an ask in a
first-touch connection note, because the note's job is the conversation, not the
meeting.

## The character caps

| Message type | Free | Premium | Confidence |
|---|---|---|---|
| Connection request note | 200 | 300 | 🟡 |
| Direct message | ~1,800 | ~1,800 | 🟡 |
| InMail body | ~1,900 | ~1,900 | 🟡 |

Two hundred characters is roughly two sentences. That is the entire budget, and
it is why the builder puts the person-specific line first and treats everything
else as optional.

## The person-specific line

The builder refuses to assemble a message without one. It is the single
discriminator between outreach and spam, and it is checkable: **could this
sentence have been sent to anyone else on your list?** If yes, it is not
specific.

What qualifies:
- Something they published, named, with the part that mattered to you.
- A decision they made that you are facing.
- A disagreement. "Your point about X is the opposite of what we found" is a
  better opener than any compliment.

What does not:
- "I came across your profile."
- Their job title, company, or industry.
- "As a fellow [category]."
- Praise with no specifics, which reads as a mail merge because it usually is.

## Phrases to delete

The builder flags these because they mark a message as bulk before anyone reads
the content: *I came across your profile · I'd love to pick your brain · hope
this finds you well · quick question · just following up · touch base · synergy ·
I'll keep it short · as a fellow · I see we're both in · let's connect.*

"Pick your brain" deserves a specific note: it asks for unbounded unpaid time
with no bounded question attached. The version that works is the opposite —
one specific question, answerable in two sentences, with an explicit "no reply
needed if you're busy".

## Volume, and what actually triggers restrictions

Covered in full in `linkedin-skills/references/policy_and_account_safety.md`. The
short version:

- Weekly invitation limit observed around **100**, adjusted per account, with
  **pending invitations counting against it**. 🟡
- Withdrawn invitations cannot be re-sent to the same person for about three
  weeks. 🟡
- **Low acceptance rate at volume is the discriminating signal**, not volume
  alone. Below ~20%, stop and fix the targeting rather than pushing through.
- Machine-regular pacing looks automated whether or not it is.

`outreach_volume_guard.py` refuses above 40 invitations per day outright: nobody
reads that many profiles and writes that many specific lines, so the plan is an
automation plan whatever the intent.

## Follow-up

One follow-up, at least a week later, **only if you have something new to say**.
A second follow-up with no new information is the point at which you become the
thing you were avoiding.

"Just bumping this up" is not new information. A relevant thing that happened
since, or a genuinely useful link with nothing attached, is.

## The order that actually works

1. **Comment on their work for two weeks.** Substantively, in public.
2. **Then send the invitation**, referencing something specific from that
   reading — which by now you have actually done.
3. **After acceptance, do nothing for a while.** Then ask, once, small.

This converts far better than any note optimisation, and it is not a growth hack
— it is what happens when you talk to people whose work you read.

## When outreach is the wrong channel

If the target number is the point rather than the people, LinkedIn outreach is
the wrong instrument. Advertising exists, it is designed for volume, it is
honest about what it is, and it does not risk the account you spent a year
building.

---

## Sources

1. LinkedIn. **User Agreement §8.2** — automated messaging, bulk sending, and
   inauthentic engagement.
2. LinkedIn Help. **"Account restrictions"** and **"Automated activity on
   LinkedIn"** — what LinkedIn says it acts on.
3. Expandi. **LinkedIn Outreach Benchmarks** (2026 edition, ~13.2M data points) —
   🟡 acceptance with and without a note, and the post-accept reply-rate gap.
4. Cleverly. **LinkedIn Benchmarks** (~20M outreach touches) — 🟡 connection and
   reply rates by industry.
5. LinkedIn Sales Solutions. **InMail best-practice guidance** — 🟢 the
   individually-sent vs bulk response-rate difference.
6. Cialdini, R. **Influence** — reciprocity and commitment, and why an ask
   arriving before any relationship inverts both.
7. Granovetter, M. **"The Strength of Weak Ties"** (1973) — the structural reason
   cold outreach works at all, and why it works better after public visibility.
