# linkedin — organic LinkedIn presence, with the rules enforced in code

A strategic assistant for building an authentic LinkedIn presence over months, not a post
generator. Built in response to
[discussion #934](https://github.com/alirezarezvani/claude-skills/discussions/934).

**The design constraint that shapes everything else:** this plugin holds no LinkedIn
credentials, makes no API calls, scrapes nothing, and sends nothing. Every output is text the
account holder posts themselves. Automated posting, connecting, commenting, and liking are
prohibited by LinkedIn's User Agreement §8.2, and a restricted account ends a compounding
asset that took months to build. So the refusals are in code, at the front of every lane,
and each one names a compliant substitute.

```
/cs:linkedin                # gate + route
/cs:grill-linkedin          # five forcing questions before the work starts
/cs:linkedin-profile        # headline, About, whole-profile audit
/cs:linkedin-plan           # brief, pillars, cadence, newsletter
/cs:linkedin-post           # format, draft, lint
/cs:linkedin-repurpose      # article/talk -> posts, with a reuse ledger
/cs:linkedin-outreach       # comment roster + one message at a time
/cs:linkedin-analyze        # your own export, analysed honestly
```

---

## What is here

| Skill | Tools | Does |
|---|---|---|
| **linkedin-skills** (orchestrator, `context: fork`) | 2 | Policy gate (ALLOW / CONSTRAIN / REFUSE) then a deterministic five-lane router with cross-lane prerequisites |
| **linkedin-profile** | 3 | Headline scored on five dimensions vs the 220-char cap; whole profile 0-100 with fixes ranked by points per hour; About section assembled to survive the fold |
| **linkedin-strategy** | 3 | Positioning brief validator; cadence priced in minutes with a 90-minute floor; newsletter eligibility + six-month sustainability gate |
| **linkedin-content** | 3 | Post linter (mechanics / hook / integrity / accessibility); format picker; repurpose splitter with a reuse ledger |
| **linkedin-engagement** | 3 | Capped commenting roster; message builder that refuses templates; volume guard that refuses automation-shaped plans |
| **linkedin-analytics** | 3 | Median/MAD describer; four-gate permutation pattern miner; experiment planner |

Plus 2 agents, 8 commands, 15 references (7 sources each), 11 assets.

## The parts that are different

**The policy gate runs before anything is drafted.** Seven refusal rules covering automation,
scraping, engagement pods, bulk messaging, fake identity, fabricated proof, and named
third-party automation tools — each with the User Agreement clause and a substitute that
achieves the same goal legitimately. A REFUSE outranks any route.

**Evidence is graded, and two popular claims are corrected.** Every quantitative claim carries
🟢 (LinkedIn-official), 🟡 (third-party study), or 🔴 (folklore, named as folklore).

- The "a personalised note triples acceptance" claim is not supported by the largest samples,
  which show acceptance close to identical either way (~26.4%). What a note actually moves is
  the **post-accept reply rate** (~5.4% → ~9.4%). That changes what the note should say: it
  earns the conversation, not the meeting — which is why `outreach_message_builder.py`
  refuses an ask in a first-touch connection note.
- The ~19% in-body link reach reduction has **never been confirmed by LinkedIn as a penalty**
  and has a plausible non-punitive explanation via dwell time. It is a warning, not a block.

**The analytics refuse to over-conclude.** `pattern_miner.py` puts every candidate through four
gates: a group-size floor, a 15% minimum relative effect, a seeded permutation test, and a
multiple-comparisons accounting that reports how many candidates would pass on noise alone.
Below 10 posts it refuses to test anything. `NOTHING_SURVIVED` is the most common honest
answer and is reported as a finding, not a failure.

**Accessibility is a blocking finding, not a footnote.** Unicode pseudo-bold — the output of
"bold text generators" — is a blocking lint failure, because screen readers announce those
characters as mathematical symbols and LinkedIn search does not index them as words.

**Refusals are refusals.** A cadence under 90 minutes a week returns a comment-only plan
rather than a schedule that will be abandoned in week five. A newsletter whose six-month cost
exceeds the budget is refused before the promise is made. An experiment that needs more posts
than a quarter allows is reported as infeasible rather than quietly re-sized.

## Quick start

```bash
# See every tool run with zero configuration
python3 skills/linkedin-skills/scripts/linkedin_policy_gate.py --sample --output human
python3 skills/linkedin-profile/scripts/headline_scorer.py --sample-weak --output human
python3 skills/linkedin-strategy/scripts/cadence_planner.py --sample --output human
python3 skills/linkedin-content/scripts/post_linter.py --sample --output human
python3 skills/linkedin-engagement/scripts/outreach_volume_guard.py --sample --output human
python3 skills/linkedin-analytics/scripts/pattern_miner.py --sample --output human
```

Every tool supports `--help`, `--sample`, and `--output json`, uses the standard library
only, and returns typed exit codes so an agent can branch on the verdict rather than parse
prose.

## Distinct from

- **`marketing-skill/x-twitter-growth`** — X/Twitter mechanics. Different platform, different
  format economics, different rules.
- **`marketing-skill/social-content`, `social-media-manager`** — multi-platform brand
  calendars. This is one person's own presence on one platform, in depth.
- **`marketing-skill/social-media-analyzer`** — cross-platform campaign reporting. This reads
  your own LinkedIn export and refuses to conclude below 10 posts.
- **`marketing-skill/cold-email`** — different channel, different law, different caps.

## Provenance

Requested in [discussion #934](https://github.com/alirezarezvani/claude-skills/discussions/934).
Refusal rules derive from LinkedIn's published User Agreement §8.2, the Prohibited Software
and Extensions help article, and the Professional Community Policies. No LinkedIn code, data,
or proprietary material is included. See `.claude-plugin/authoring-notes.json`.

---

**Version:** 1.0.0 · MIT · 6 skills · 17 stdlib tools · 15 references · nothing auto-sent
