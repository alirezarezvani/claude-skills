# LinkedIn Platform Canon — what is known, what is inferred, what is folklore

Every quantitative claim below carries a confidence level. This matters more on
LinkedIn than on most platforms: the advice ecosystem is dominated by people
selling LinkedIn advice, almost none of the numbers come from LinkedIn, and the
platform changes the surfaces those numbers describe without announcing it.

**Confidence key**
- 🟢 **High** — stated by LinkedIn in official documentation, engineering
  publications, or peer-reviewed papers authored by LinkedIn engineers.
- 🟡 **Medium** — large-N third-party studies of public posts. Directionally
  useful, methodologically opaque, and the sample is always public posts from
  accounts that opted into being measured.
- 🔴 **Low / folklore** — repeated widely, sourced nowhere. Listed so you can
  recognise it, not so you can use it.

---

## 1. How the feed actually ranks — 🟢

LinkedIn's feed is a multi-stage retrieval-and-ranking system, not a chronological
timeline and not a single "algorithm". The public record is unusually good here
because LinkedIn's engineering organisation publishes:

- **LiRank** (Borisyuk et al., KDD 2024, arXiv:2402.06859) describes the
  production ranking stack for Feed, Ads CTR, and Job recommendations —
  Residual DCN architecture, multi-task objectives, and isotonic calibration.
  The relevant fact for a creator is structural: **the model optimises several
  objectives at once**, and no single engagement action is "the" ranking signal.
- **Dwell time** is an explicit feed-ranking objective. LinkedIn's engineering
  blog documents two measures — dwell "on the feed" (starting when at least half
  of an update is visible during a scroll) and dwell "after the click" — and
  operationalises them as a *Long Dwell* classifier predicting whether a member's
  dwell will exceed a context-dependent threshold.

**What follows for a creator, and what does not.**

Follows: a post that holds attention is being measured on that, so a post worth
reading all the way through is not merely a nice-to-have. Text that rewards the
expand click is doing something the ranker can see.

Does *not* follow: that you should pad posts to increase dwell. Dwell is measured
against a *context-dependent percentile*, not an absolute seconds count, and
padding also depresses the completion and interaction signals that sit alongside
it in a multi-task model. "Add fluff to raise dwell time" is 🔴 folklore built on
a 🟢 fact.

## 2. Comments are the expensive signal — 🟡 (mechanism 🟢)

A reaction costs a reader one tap. A substantive comment costs them thirty
seconds and a small reputational exposure in front of their own network. Third-
party studies consistently find comment-heavy posts travel further, and the
mechanism is consistent with a multi-objective ranker that also predicts
downstream sessions: a comment creates a notification, a return visit, and a
thread other people can enter.

The practical version: **write posts that give a competent reader something to
add.** A post that is complete, correct, and closed invites agreement, and
agreement is the cheapest and least valuable response you can earn.

## 3. Reach is falling and the base has shifted — 🟡

Richard van der Blom's annual *Algorithm Insights* report (Just Connecting) is
the most-cited third-party longitudinal study, drawing on over a million public
posts. Recent editions report substantial year-over-year declines in organic
views, engagement, and follower growth, and an average post reaching roughly
8-12% of a creator's followers.

Treat the *direction* as reliable and the *specific percentages* as indicative.
The sample is public posts, the methodology is not independently auditable, and
"reach" is measured through the same impressions counter whose definition
LinkedIn has revised more than once.

What the trend means practically: **follower count is a worse proxy for
distribution every year.** A focused audience of a few thousand people who
actually work in your field will out-perform a large unfocused one, because
relevance-based retrieval has to decide *who* to show a post to, and an unfocused
follower graph gives it nothing to work with.

## 4. External links in the post body — 🟡, contested

Third-party analysis (van der Blom, 2026 edition, ~1.3M posts) reports a body
link reducing median reach by roughly 19%, and much larger suppression for links
placed in comments in some measurements. **LinkedIn has never confirmed a link
penalty**, and a plausible non-punitive explanation exists: a link that takes a
reader off-platform truncates dwell, and dwell is a ranking objective.

The practical guidance is the same under either explanation, which is why it is
safe to follow: put the link in the first comment, say "link in the comments" in
the post, and keep it in the body only when the click *is* the goal and you
accept the reach cost.

## 5. The first 60-90 minutes — 🟡

Early engagement correlates strongly with eventual reach in every third-party
dataset. The causal story is unproven and probably bidirectional (good posts get
early engagement *and* early engagement helps distribution). Either way the
behavioural implication holds: **be available to reply for an hour after you
post.** Replying is also the cheapest way to add comments to your own post
honestly.

🔴 The "golden hour" as a precise, engineered window with a hard cutoff is
folklore. Nobody outside LinkedIn knows the decay function.

## 6. Hashtags — 🟡, declining relevance

LinkedIn has deprecated hashtag-following surfaces over time and the platform has
moved toward semantic retrieval. Two or three topical hashtags remain a cheap,
harmless topic signal. Ten hashtags signal reach-chasing to human readers, which
is the cost that actually matters now.

## 7. What LinkedIn does *not* publish — worth knowing

- The exact weekly invitation limit (widely observed around 100, adjusted per
  account).
- The exact character position where "…see more" truncates, per surface.
- The full newsletter eligibility criteria (the >150 followers/connections
  threshold is published; "a set of criteria, all of which must be met" is not).
- Any per-signal ranking weight.

Anyone quoting a precise figure for these is quoting an observation, not a
specification. Cite it that way.

---

## Sources

1. Borisyuk, F. et al. **"LiRank: Industrial Large Scale Ranking Models at
   LinkedIn."** KDD 2024. arXiv:2402.06859. — production ranking architecture,
   multi-task objectives.
2. LinkedIn Engineering Blog. **"Understanding feed dwell time to improve
   LinkedIn feed ranking."** linkedin.com/blog/engineering/feed/understanding-feed-dwell-time
   — the two dwell measures and the Long Dwell classifier.
3. LinkedIn. **User Agreement**, §8.2 "Don'ts."
   linkedin.com/legal/user-agreement — the binding rules on automation, scraping,
   and inauthentic engagement.
4. LinkedIn. **Professional Community Policies.**
   linkedin.com/legal/professional-community-policies — authenticity, spam, and
   engagement-bait rules.
5. van der Blom, R. **Algorithm Insights** (annual, Just Connecting) — the
   longest-running third-party longitudinal study of LinkedIn organic
   performance. 🟡 sample is public posts; methodology not independently audited.
6. LinkedIn Help. **"LinkedIn Newsletter access criteria."** — the >150
   followers/connections threshold and the existence of unpublished criteria.
7. Nielsen Norman Group. **"How People Read Online"** and the F-shaped reading
   pattern research — why the visible first lines carry the decision, on any
   platform with a truncated preview.

---

**Rule of thumb for anything not on this page:** if a claim about LinkedIn comes
with a precise percentage and no named study, it is 🔴. Say so out loud rather
than repeating it, and give the user the version of the advice that holds
regardless of whether the number is true.
