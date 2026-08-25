# Worked Example — a post that passes the linter

The post below scores 98/100 in `post_linter.py` with one INFO finding (it sits below the
1,300-2,500 character band, which is not a defect). Annotations follow.

---

Our onboarding took 6 weeks. We got it to 4 days without hiring anyone.

The bottleneck was not the product. It was that three different teams each owned
one step and none of them owned the handoff.

What we changed:

1. One named owner for the whole path, not per step. Every stall now has someone
   whose week it ruins.
2. We deleted the "kickoff call" and replaced it with a 4-question form. 80% of
   accounts never needed the call.
3. We stopped treating the CRM stage as the source of truth and started measuring
   the customer's first real use.

The part I got wrong: I assumed the delay was engineering capacity. It was
handoffs. We spent five weeks building automation for the wrong step before
anyone measured where the time actually went.

If you are staring at a slow onboarding number, measure the wait between steps
before you optimise any single step. That is where ours was hiding.

What did the handoff cost you the last time you measured it?

---

## Why it passes

**Hook (first 140 characters).** Two complete sentences land inside the mobile fold, both
carrying numbers, and the second names a constraint people assume is binding — "without
hiring anyone". A reader decides on those two sentences alone.

**Specificity throughout.** 6 weeks, 4 days, 80%, five wasted weeks. Every number is one the
author could be challenged on, which is exactly why they carry weight.

**The admission.** "The part I got wrong" is the load-bearing paragraph. It is expensive to
write, which is why it reads as true, and it is the paragraph practitioners reply to.

**Structure.** Seven blocks, none longer than four lines. Numbered list where the content is
a sequence. No Unicode pseudo-bold, no emoji, no hashtags — none of which are required.

**The close.** A real question with a specific answer available only to someone who has
measured the same thing. Not "thoughts?".

**No link in the body.** If there were a write-up, it goes in the first comment with "link
in the comments" in the post.

## Run it yourself

```bash
python3 ../scripts/post_linter.py --sample --output human
```
