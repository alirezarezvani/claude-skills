# Batched, anchored feedback: why the artifact beats the message

The design claim behind this skill: **human feedback should be a structured artifact,
not a chat message.** This document is the argument and the prior art.

---

## 1. The problem with prose feedback

The natural thing a reviewer types is:

> In the third paragraph change X to Y. Cut the third card, it repeats the first. Also
> the CTA needs rewriting, and I think the numbers in the table are stale.

Four instructions, one blob. Everything that goes wrong next is predictable:

| Failure | Why it happens |
|---|---|
| An instruction is missed | Nothing enumerates them, so nothing detects a miss |
| An instruction is misread | "the third paragraph" is positional and drifts as the doc changes |
| The reviewer must re-verify everything | There is no per-item status, so the only check is re-reading the whole artifact |
| Severity is invisible | "Also the CTA needs rewriting" and "this number is wrong" look identical |
| Nothing accumulates | Round 2 cannot tell what round 1 asked for |

Each failure is a *representation* problem, not an attention problem. Structure fixes
what more careful reading does not.

---

## 2. Batching: the review, not the comment

GitHub and GitLab both converged on the same interaction: reviewers **start a review**,
accumulate comments, and **submit them as one batch** — rather than firing each comment
as it is written. This was a deliberate change from the earlier one-comment-at-a-time
model, and the reasons generalise well beyond code:

- **The author gets a coherent picture** rather than a drip of notifications, each of
  which invites a premature partial fix.
- **The reviewer can revise.** A comment written on line 10 often becomes wrong after
  reading line 200. Batching lets it be withdrawn before the author ever sees it.
- **The batch is a unit of work.** "Apply this review" is a well-defined task with a
  clear completion state. "Respond to these seven notifications" is not.

Fagan's inspection process (1976) had already established the same shape half a century
earlier: defects are logged during inspection and handed over as a **single rework list**
with a verification step, not shouted individually.

The `batch.v1` schema is this idea made machine-readable — one round, all items, counts,
and a blocking total.

---

## 3. Anchoring: locating feedback so it survives edits

Positional references ("paragraph 3", "line 40") break the moment the artifact changes.
The web-annotation world solved this properly.

The **W3C Web Annotation Data Model** (Recommendation, 2017) and its companion
*Selectors and States* define `TextQuoteSelector`: locate a target by its **exact quoted
text plus a prefix and suffix of surrounding context**. This is robust in the way
positions are not — if the surrounding text shifts, the quote still matches; if the
quote itself was edited, the mismatch is *detectable* rather than silent.

Hypothesis's open-source anchoring implementation is the reference production system for
this approach, and it is what `petergyang/human-review` also uses (its comment objects
carry `{prefix, quote, suffix}`).

**This skill uses a deliberately simpler two-layer anchor:**

1. A **stable block id** (`b7`) assigned at page-build time — cheap, exact, and enough
   for the common case.
2. An optional **verbatim quote**, which `feedback_parser.py --target` checks against the
   real file and reports when it no longer matches.

The simplification is honest about its limit: block ids are stable *within a round*, not
across a rewrite that reorders blocks. The quote check is what catches drift. If you need
true edit-resilient anchoring across major rewrites, the W3C selector model is the thing
to implement, and the quote field is already the hook for it.

---

## 4. Severity vocabulary: the cheapest quality upgrade

An unlabelled comment forces the author to infer urgency, and authors systematically
infer wrong — usually downward on things that matter and upward on things that do not.

Google's *Code Review Developer Guide* institutionalised the fix with the `Nit:` prefix:
an explicit marker that a comment is a preference the author may decline. Once one rung
exists, the rest follow naturally, and the four-rung ladder is now near-universal:

| Rung | Meaning | Blocks close? |
|---|---|---|
| **BLOCKER** | must be fixed; shipping this is wrong | yes |
| **MAJOR** | strongly recommend; needs a reason to decline | yes |
| **MINOR** | worth fixing | no |
| **NIT** | cosmetic, author's call | no |

**Conventional Comments** (conventionalcomments.org) generalises this into a labelled
grammar — `praise:`, `nitpick:`, `suggestion:`, `issue:`, `question:`, `blocking:` — with
the same underlying insight: *the label is not decoration, it is the routing
information.* A labelled corpus of feedback can be counted, filtered, and gated. An
unlabelled one can only be read.

This skill uses BLOCKER/MAJOR/MINOR/NIT for consistency with
`markdown-html/md-review`, plus three kinds that are not severities:

- **EDIT** — the reviewer already wrote the replacement. Not a request; a fact.
- **NOTE** — unanchored commentary about the whole artifact.
- **APPROVE** — explicit sign-off, distinct from mere absence of blockers.

---

## 5. EDIT items and the verbatim rule

The most valuable thing a reviewer can produce is not a comment — it is **the corrected
text itself**. One sentence they rewrote is worth three paragraphs describing how they
would like it rewritten.

This creates an obligation that is easy to violate: the replacement must be carried
across **verbatim**. Three ways agents break it, all observed:

1. **Paraphrasing** it into the surrounding voice, discarding the reviewer's word choice.
2. **Reverting** it on a later pass, because a general instruction ("tighten the copy")
   overwrote a specific one.
3. **Applying it only to the rendered artifact**, not to the MDX/template/script that
   generates it — so the next build silently deletes the human's edit.

Upstream `human-review`'s SKILL.md is emphatic about exactly these, and it is right to
be. The rule is inherited here unchanged, and stated in the skill's hard rules.

---

## 6. Why the sidecar is plain Markdown

`batch.v1` is JSON, but the thing a *human* writes is Markdown. That is deliberate:

- **No tool required.** A reviewer with `vi` over SSH can produce a valid batch. This is
  what makes the loop survive headless hosts, which is precisely where the
  browser-dependent designs fail.
- **Diffable and reviewable.** The sidecar can live in git next to the artifact.
- **Degrades gracefully.** A malformed sidecar still parses partially, and
  `feedback_parser.py` reports problems rather than refusing everything.

The single-file HTML review page is a **convenience over** this format, never a
prerequisite for it. Any design where the GUI is the only way to produce feedback has
made the browser a hard dependency of the review loop — a bad trade for a capability
whose whole point is to work whenever a human is available.

---

## Sources

1. W3C. *Web Annotation Data Model.* W3C Recommendation, 23 February 2017.
2. W3C. *Selectors and States* (`TextQuoteSelector`). W3C Recommendation, 2017.
3. Hypothesis. *Anchoring* — open-source annotation anchoring implementation.
   https://web.hypothes.is/
4. Google. *Code Review Developer Guide — How to write code review comments.*
   https://google.github.io/eng-practices/review/reviewer/comments.html
5. *Conventional Comments.* https://conventionalcomments.org/
6. Fagan, M. *Design and code inspections to reduce errors in program development.*
   IBM Systems Journal 15(3), 1976.
7. Yang, P. *human-review* — batched browser review for agents (MIT), 2026.
   https://github.com/petergyang/human-review
