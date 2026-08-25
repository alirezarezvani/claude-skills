# LinkedIn Metrics Canon — what each number is, and what it is not

LinkedIn gives creators a small set of numbers and almost no definitions. The
result is a advice ecosystem built on metrics whose meaning has changed at least
twice, compared across periods where they meant different things.

This is what each one actually is, and which ones are worth tracking.

---

## The numbers LinkedIn shows you

### Impressions
The count of times a post was rendered in a feed. **Not unique people.** One
person scrolling past your post twice can produce two impressions. LinkedIn has
revised the counting rules (notably around what counts as "viewed") more than
once, without a changelog a creator can read.

Consequence: **compare posts from the same period, not across a year.** A 2024
impression and a 2026 impression are not obviously the same object.

### Members reached
Where available, this is closer to unique people and is the better denominator.
It is not exposed everywhere, which is why engagement rate is usually computed on
impressions.

### Reactions, comments, reposts
Counts of the three interaction types. Reposts split into "repost" and "repost
with your thoughts", which behave differently and are usually reported together.

### Engagement rate
LinkedIn does not publish a single definition, and neither does anyone else
consistently. This plugin uses:

```
engagement_rate = (reactions + comments + reposts) / impressions
```

Stated explicitly because the alternative definitions (including clicks,
including follows, dividing by followers) produce numbers that differ by 3-5x.
**Any benchmark you read elsewhere is on an unknown denominator.** Compare
against your own history, not against a published benchmark.

### Profile views
Weakly attributable and heavily lagged. Useful as a trend across weeks, useless
per post.

### Followers gained
The metric people optimise and should not. It moves for reasons unrelated to
whether the work is working: one post reaching an adjacent audience adds
followers who will never engage again. A quarter of excellent, well-targeted work
can add very few.

---

## What to actually track

Three tiers, in descending reliability.

**Tier 1 — outcome metrics.** Inbound conversations, specific references
("I saw your post on X"), invitations, referrals, qualified enquiries. Counted by
hand, in a note. These are the only numbers tied to the objective, and they are
the ones nobody tracks because they require writing things down.

**Tier 2 — behavioural proxies.** Comment count and comment *share*
(comments / total interactions). A comment costs a reader thirty seconds and a
small reputational exposure; a reaction costs a tap. Comment share is the
cleanest available proxy for whether the work is landing with people who care.

**Tier 3 — reach metrics.** Impressions, engagement rate, followers. Noisy,
redefined without notice, and easy to move in ways that do not serve the
objective. Track them to notice large changes, not to make weekly decisions.

## Why median, not mean

`post_performance_analyzer.py` reports median and MAD (median absolute
deviation), not mean and standard deviation. LinkedIn post performance is
heavy-tailed: a small number of posts reach far outside the normal range, and one
of them drags a mean to a value that describes none of your posts.

The bands the analyzer reports are Tukey's: Q1, Q3, and a 1.5×IQR fence above Q3
for "breakout". This is the standard robust definition of an outlier and it means
"breakout" has a threshold rather than a feeling.

## The floor

The analyzer refuses to characterise a body of work under **10 posts**, and the
pattern miner refuses to test anything under 10.

This is not conservatism. The between-post variance on LinkedIn is routinely
larger than any group difference eight posts could show — which means with eight
posts you can "discover" almost any pattern you go looking for. See
`evidence_thresholds.md`.

## Exporting your own data

LinkedIn provides two routes, both to *your own* data:

- **Analytics → Post impressions → Export** for per-post performance.
- **Settings → Data privacy → Get a copy of your data** for a fuller archive.

Both tools in this skill read these exports. **Nothing is fetched from LinkedIn
and no other member's data is involved** — scraping profiles or post data is
prohibited by User Agreement §8.2, and there is no version of this analysis that
needs it.

## Benchmarks against other people

Don't. Three reasons, any one of which is sufficient:

1. The denominators differ and are usually unstated.
2. Audience composition dominates. A 12% engagement rate on 400 followers who
   all know you personally is not comparable to 2% on 20,000.
3. The published benchmarks come from samples of accounts that opted into being
   measured, usually by a vendor selling to them.

Your own history is the only honest baseline, which is another argument for
posting consistently enough to have one.

---

## Sources

1. LinkedIn Help. **Analytics and post performance** documentation — the
   definitions LinkedIn does publish, and the export path.
2. LinkedIn Help. **"Get a copy of your data"** — the supported self-export.
3. LinkedIn. **User Agreement §8.2** — why analysis here is limited to your own
   exports.
4. Tukey, J. **Exploratory Data Analysis** (1977) — median, IQR, and the 1.5×IQR
   outlier fence used for the band thresholds.
5. Huber, P. & Ronchetti, E. **Robust Statistics** (2nd ed.) — MAD as a robust
   scale estimate, and the 1.4826 consistency constant used to derive CV.
6. Taleb, N.N. **The Black Swan** / **Statistical Consequences of Fat Tails** —
   why sample means are unreliable descriptors for heavy-tailed processes.
7. Nielsen, J. **"The 90-9-1 Rule for Participation Inequality"** (NN/g) — the
   structural reason interaction counts are small and skewed relative to reach.
