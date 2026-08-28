# Comment Strategy — the cheapest distribution on LinkedIn

From a standing start, your posts reach almost nobody. That is not a failure of
the writing; it is what an empty follower graph and a relevance-based retrieval
system produce together. Publishing harder does not fix it.

Commenting does. A substantive comment on a post that already has an audience
puts your name, your headline, and one paragraph of your thinking in front of
people who are already reading about your subject. It costs six minutes.

Most people do it badly, in an identifiable way.

---

## What a comment is competing on

A reader scanning a comment thread is making the same decision they make in the
feed, with less patience. Your comment competes against forty others, most of
which say some version of "great post". The bar for standing out is therefore
much lower than it looks, and it is entirely about **adding something the post
did not say.**

Five things that qualify:

1. **A counter-example.** "This holds until the team crosses about fifteen
   people, and then the handoff cost dominates."
2. **A number.** "We measured this: 6 days of work, 35 days of queue."
3. **The case where it breaks.** The most valuable comment type, and the rarest.
4. **A specific mechanism.** Why the thing the author observed happens.
5. **A question only someone who read it properly could ask.**

Two that do not: agreement, and a summary of the post the author just wrote.

## Tiering, and why the biggest accounts are the wrong target

`comment_target_planner.py` scores accounts on audience overlap, posting
frequency, and tier.

| Tier | Relative size | Factor | Reality |
|---|---|---|---|
| **huge** | 10x+ | 1.0 | Crowded. 400 comments, most never read. Worth it only if you are early *and* excellent |
| **larger** | 2-10x | 1.5 | The best ratio of reachable audience to competition |
| **peer** | ~1x | 1.3 | Reciprocity compounds. These relationships still exist in a year |
| **smaller** | <0.5x | 0.9 | Low reach today, high goodwill, and some will not be smaller for long |

The instinct is to comment on the biggest accounts in the field. It is the worst
use of the time: your comment is one of hundreds, the author will not read it,
and their audience is scanning past the whole thread.

**The under-rated tier is peer.** Reciprocity is real and it is mutual — the
people at your size who show up in your comments now are the ones whose audience
overlaps yours most, and the relationship runs both directions.

## The rules the planner enforces

- **No account more than twice a week.** Commenting daily on one person reads as
  following them around, and it exhausts the goodwill it earns.
- **At least one peer slot per day**, for the reason above.
- **No more than half a day's slots in the huge tier.**

## What the planner will not do

It does not write comments. This is the whole point of the design: a comment
written by a tool is exactly the thing LinkedIn's User Agreement §8.2 names when
it prohibits automated methods to "create, comment on, like, share, or re-share
posts, or otherwise drive inauthentic engagement."

More practically: a generated comment is recognisable, and being recognised as
someone who generates comments is worse than not commenting.

## Engagement pods

A pod is a group that agrees to reciprocally comment on each other's posts,
usually within the first hour. The pitch is that it is just humans helping
humans.

It is prohibited. The User Agreement language is "otherwise drive inauthentic
engagement", and coordinated reciprocal commenting on schedule is the central
example. `linkedin_policy_gate.py` refuses pod requests at exit 4.

The legitimate version of the same instinct is the reciprocity list: a set of
people whose work you genuinely read, whom you comment on because you have
something to say. It is slower, it produces the same relationships, and it
survives an audit.

## Replying to your own comments

Half of the value of a post is in the thread underneath it. Replies to your own
post are not a bonus round:

- Reply to every substantive comment within 24 hours, and to the early ones
  within the hour if you can.
- Reply with something, not "thanks!". The reply is visible to everyone who opens
  the thread, and it is a second chance to say the thing.
- **Reply to replies on your comments elsewhere.** That sub-thread is where
  people actually meet you.

`cadence_planner.py` budgets 20 minutes per published post for this, and treats
it as part of the post rather than an extra.

## Groups and communities

LinkedIn Groups are mostly dormant. The exceptions are narrow, actively moderated
professional groups, where the signal is high because the population is small.
The test is whether posts in the group get real replies from named humans; if the
last three posts have no comments, it is a graveyard and posting there is a
donation to nobody.

The higher-yield version of the same instinct is off-LinkedIn communities where
your audience already talks — a Slack, a Discord, a mailing list, a conference —
and bringing what you learn there back to LinkedIn as posts.

## Measuring it

Commenting does not produce a metric LinkedIn will show you cleanly. The
observable signals, in order of reliability:

1. Profile views trending up in weeks you commented consistently.
2. Connection requests *from* people whose posts you commented on.
3. Named references: someone says "I saw your comment on X's post".

None of these are clean attribution, and there is no honest way to make them so.
Treat commenting as a fixed practice rather than a tracked channel.

---

## Sources

1. LinkedIn. **User Agreement §8.2** — the explicit prohibition on automated or
   inauthentic commenting, liking, and sharing.
2. Granovetter, M. **"The Strength of Weak Ties."** *American Journal of
   Sociology*, 1973 — why the peer and larger tiers, not the huge tier, are where
   opportunity actually flows.
3. Burt, R. **Structural Holes: The Social Structure of Competition** (1992) —
   brokerage between clusters; commenting across adjacent fields is exactly this.
4. Cialdini, R. **Influence: The Psychology of Persuasion** — reciprocity and
   liking, and why they are destroyed by being made transactional.
5. Grant, A. **Give and Take** — givers who succeed do so through specific,
   bounded generosity, not indiscriminate availability.
6. Nielsen, J. **"The 90-9-1 Rule for Participation Inequality"** (NN/g) — the
   small population of people who comment at all, and why being one of them is
   cheap differentiation.
7. LinkedIn Engineering. **"Understanding feed dwell time to improve LinkedIn
   feed ranking."** — the mechanism by which threads that hold attention are
   measured.
