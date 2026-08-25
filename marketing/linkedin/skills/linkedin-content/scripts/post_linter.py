#!/usr/bin/env python3
"""post_linter.py — lint a LinkedIn post before it goes out. Score 0-100.

Checks the things that measurably cost reach or credibility, in four families:

  MECHANICS     length caps, the mobile fold, hashtag count, link placement
  HOOK          does the visible first line survive truncation and earn the click
  INTEGRITY     engagement bait, unverifiable superlatives, machine-written tells
  ACCESSIBILITY Unicode pseudo-bold, emoji load, ALL-CAPS, wall-of-text density

Blocking findings are the ones with named consequences: a post over the 3,000
character cap will not publish; Unicode pseudo-bold is read aloud by screen
readers as "mathematical bold small a"; engagement bait is named in LinkedIn's
Professional Community Policies as demoted content.

Evidence note: the 3,000-character cap and ~140-character mobile fold are
third-party-documented and stable. The reach cost of an in-body external link
(~19% lower median reach in a 1.3M-post third-party study) is a third-party
finding, not a LinkedIn statement — it is flagged as a warning, not a block,
and the reference doc carries the confidence level.

Exit codes:
  0  SHIP    (>= 75 and no blocking findings)
  2  REVISE  (50-74, or any blocking finding)
  3  REWRITE (< 50)

Stdlib only. No network. Deterministic.
"""

import argparse
import json
import re
import sys

HARD_LIMIT = 3000
FOLD_MOBILE = 140        # characters before "…see more" on mobile
FOLD_DESKTOP = 210
BAND_LOW, BAND_HIGH = 1300, 2500   # highest observed median engagement band

BAIT_PATTERNS = [
    (r"\bcomment ['\"][\w ]{1,24}['\"]\s*(below|and i'?ll|to get|for the|if you)\b",
     "comment-for-lead-magnet"),
    (r"\bcomment ['\"]?\w{1,14}['\"]? below\b", "comment-keyword"),
    (r"\band i'?ll (dm|send) (you )?(the|it|a|my)\b", "dm-for-engagement"),
    (r"\b(like|repost|share) (this )?if you\b", "like-if"),
    (r"\btag (someone|a friend|3 people|three people)\b", "tag-someone"),
    (r"\bwho else (agrees|thinks|feels)\b", "agreement-farming"),
    (r"\bagree\?\s*$", "agree-closer"),
    (r"\brepost (this )?(to|so|if)\b", "repost-plea"),
]

# Phrases that read as machine-written to anyone who reads LinkedIn daily.
SLOP_PATTERNS = [
    (r"\bin today'?s (fast[- ]paced|ever[- ]changing|digital|competitive) (world|landscape|era)\b",
     "in-todays-world opener"),
    (r"\bdelve into\b", "delve"),
    (r"\bit'?s not (just )?about \w+[.,] it'?s about\b", "not-x-its-y"),
    (r"\blet that sink in\b", "let-that-sink-in"),
    (r"\bgame[- ]chang(er|ing)\b", "game-changer"),
    (r"\bunlock (the|your) (power|potential|secret)\b", "unlock-the-potential"),
    (r"\bin the ever[- ]evolving\b", "ever-evolving"),
    (r"\bhere'?s the (thing|kicker|secret)\b(?=[\s\S]{0,400}\bhere'?s the)", "repeated here's-the"),
    (r"\bthe results? (speak for themsel|were nothing short of)\w*", "results-speak"),
    (r"\b(revolutioniz|supercharg|turbocharg)\w+", "hype-verb"),
    (r"\bas an? (ai|language model)\b", "assistant-artifact"),
    (r"\bcertainly[!,]", "assistant-artifact"),
]

SUPERLATIVES = [
    "the best", "the only", "guaranteed", "never fails", "always works",
    "100% of", "everyone knows", "no one is talking about", "nobody talks about",
    "the #1", "world-class", "unprecedented", "revolutionary",
]

GENERIC_OPENERS = [
    "i'm excited to announce", "i am excited to announce", "i'm thrilled",
    "i am thrilled", "i'm humbled", "i am humbled", "excited to share",
    "happy to share", "proud to announce", "quick thought", "just a thought",
]

URL_RE = re.compile(r"https?://[^\s)]+|\bwww\.[^\s)]+")
HASHTAG_RE = re.compile(r"(?<!\w)#[A-Za-z][A-Za-z0-9_]{1,49}")
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿️⬀-⯿]")
# Mathematical Alphanumeric Symbols + enclosed alphanumerics: the "bold text
# generators" people paste into LinkedIn. Screen readers do not render these.
PSEUDO_BOLD_RE = re.compile("[\U0001D400-\U0001D7FF\U0001F130-\U0001F189Ａ-ｚ]")

SAMPLE_POST = """Our onboarding took 6 weeks. We got it to 4 days without hiring anyone.

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
"""


def _visible(text: str, n: int) -> str:
    return text[:n]


def lint(text: str, has_image: bool = False) -> dict:
    raw = text.rstrip("\n")
    low = raw.lower()
    findings = []
    n = len(raw)

    def add(sev, family, msg, fix):
        findings.append({"severity": sev, "family": family, "finding": msg, "fix": fix})

    # ---------------- MECHANICS ------------------------------------------
    if n > HARD_LIMIT:
        add("blocking", "mechanics",
            f"{n} characters — {n - HARD_LIMIT} over the {HARD_LIMIT} cap. LinkedIn will not publish it.",
            "Cut to one idea. The section you are most attached to is usually the one to lose.")
    elif n < 400:
        add("warning", "mechanics",
            f"{n} characters. Short posts can work, but under ~400 there is rarely room for a claim "
            "and the evidence for it.",
            "Either add the specific example, or accept it as a comment rather than a post.")
    elif not (BAND_LOW <= n <= BAND_HIGH):
        add("info", "mechanics",
            f"{n} characters — outside the {BAND_LOW}-{BAND_HIGH} band where third-party studies "
            "report the highest median engagement.",
            "Not a defect. Worth knowing if reach is the goal for this specific post.")

    urls = URL_RE.findall(raw)
    if urls:
        add("warning", "mechanics",
            f"{len(urls)} external link(s) in the post body. A 1.3M-post third-party study reports "
            "~19% lower median reach for a body link (LinkedIn has never confirmed a penalty).",
            "Put the link in the first comment and say so in the post: 'link in the comments'. "
            "Keep it in the body only when the click IS the goal and you accept the reach cost.")

    tags = HASHTAG_RE.findall(raw)
    if len(tags) > 3:
        add("warning", "mechanics",
            f"{len(tags)} hashtags. Past three they stop being topic signals and start reading as "
            "reach-chasing.",
            "Keep the two or three that describe what the post is actually about.")

    # ---------------- HOOK ------------------------------------------------
    hook = _visible(raw, FOLD_MOBILE).strip()
    first_line = raw.split("\n", 1)[0].strip()
    if len(raw) > FOLD_MOBILE:
        boundary = max(hook.rfind("."), hook.rfind("?"), hook.rfind("!"), hook.rfind("\n"))
        if boundary < FOLD_MOBILE - 90:
            add("major", "hook",
                f"Nothing completes inside the first {FOLD_MOBILE} characters — the mobile fold. "
                "The reader's decision to expand is made on a fragment.",
                f"End a sentence before character {FOLD_MOBILE}. Desktop folds around "
                f"{FOLD_DESKTOP}, so mobile is the binding constraint.")
    gen = [g for g in GENERIC_OPENERS if low.startswith(g) or low[:60].find(g) >= 0]
    if gen:
        add("major", "hook",
            f"Opens with a stock phrase: '{gen[0]}'. It is the most-scrolled-past construction on "
            "the platform.",
            "Open on the specific thing: the number, the mistake, or the sentence someone said to you.")
    if not re.search(r"\d", hook) and "?" not in hook and len(first_line.split()) > 3:
        add("info", "hook",
            "The visible hook has no number and asks nothing. It can still work, but it is doing "
            "it on voice alone.",
            "A concrete number or a real question in the first line is the cheapest specificity available.")

    # ---------------- INTEGRITY -------------------------------------------
    bait = sorted({label for pat, label in BAIT_PATTERNS if re.search(pat, low, re.I)})
    if bait:
        add("blocking", "integrity",
            f"Engagement bait: {', '.join(bait)}. LinkedIn's Professional Community Policies name "
            "bait as content it demotes, and readers recognise it.",
            "Ask the question the post actually earned, or offer the resource with no toll gate.")
    slop = [label for pat, label in SLOP_PATTERNS if re.search(pat, low, re.I)]
    if slop:
        add("major", "integrity",
            f"Machine-written tells: {', '.join(sorted(set(slop)))}.",
            "Rewrite those lines the way you would say them out loud. If a phrase could sit in "
            "anyone's post about anything, it is not carrying meaning.")
    sup = [s for s in SUPERLATIVES if s in low]
    if sup:
        add("warning", "integrity",
            f"Unverifiable superlatives: {', '.join(sup)}.",
            "Replace with the bounded version: what you measured, over what period, in what context.")
    # Rule-of-three cadence: three consecutive short sentence fragments in a row.
    if len(re.findall(r"(?m)^[^\n]{1,45}\.\s*$", raw)) >= 6:
        add("info", "integrity",
            "Many short standalone one-line sentences ('broetry' cadence). It reads as formatted "
            "for the algorithm rather than for a reader.",
            "Keep the line breaks that separate ideas; join the ones that only separate clauses.")

    # ---------------- ACCESSIBILITY ---------------------------------------
    pseudo = PSEUDO_BOLD_RE.findall(raw)
    if pseudo:
        add("blocking", "accessibility",
            f"{len(pseudo)} Unicode pseudo-bold/italic characters. Screen readers announce these "
            "character by character as mathematical symbols, and LinkedIn search does not index "
            "them as words.",
            "Use plain text. Emphasis comes from line breaks and word order, not from a font hack.")
    emoji = EMOJI_RE.findall(raw)
    if len(emoji) > 8:
        add("warning", "accessibility",
            f"{len(emoji)} emoji. Each one is read aloud by name; past a handful the post becomes "
            "tiring to hear.",
            "Keep the ones doing structural work (list markers), cut decorative ones.")
    caps_lines = [ln for ln in raw.split("\n") if len(ln) > 25 and ln.isupper()]
    if caps_lines:
        add("warning", "accessibility",
            f"{len(caps_lines)} ALL-CAPS line(s). Some screen readers spell these out letter by letter.",
            "Sentence case. Put the emphasis in the words.")
    paragraphs = [p for p in re.split(r"\n\s*\n", raw) if p.strip()]
    longest = max((len(p) for p in paragraphs), default=0)
    if longest > 600:
        add("warning", "accessibility",
            f"Longest paragraph is {longest} characters. On a phone that is a wall.",
            "Break at the idea boundaries. Three to four lines per block is readable.")
    if has_image:
        add("info", "accessibility",
            "Image attached: LinkedIn supports alt text on images and does not add it for you.",
            "Write alt text describing what the image shows, not 'chart'. One sentence is enough.")

    # ---------------- CTA --------------------------------------------------
    tail = raw[-300:].lower()
    if "?" not in tail and not re.search(r"\b(tell me|curious|what would you|how do you|"
                                         r"what did|would love to hear|message me|reply)\b", tail):
        add("info", "cta",
            "The post ends without a question or a next step. Comments are the engagement signal "
            "that matters most; nothing here invites one.",
            "One genuine question you would actually want answered. Not 'thoughts?'.")

    # ---------------- score -------------------------------------------------
    weights = {"blocking": 22, "major": 11, "warning": 6, "info": 2}
    score = max(0, 100 - sum(weights[f["severity"]] for f in findings))
    blocking = any(f["severity"] == "blocking" for f in findings)
    if blocking:
        verdict, code = "REVISE", 2
        score = min(score, 60)
    elif score >= 75:
        verdict, code = "SHIP", 0
    elif score >= 50:
        verdict, code = "REVISE", 2
    else:
        verdict, code = "REWRITE", 3

    order = {"blocking": 0, "major": 1, "warning": 2, "info": 3}
    return {
        "score": score,
        "verdict": verdict,
        "exit_code": code,
        "stats": {
            "chars": n, "limit": HARD_LIMIT,
            "optimal_band": [BAND_LOW, BAND_HIGH],
            "hashtags": len(tags), "links_in_body": len(urls),
            "emoji": len(emoji), "paragraphs": len(paragraphs),
            "visible_before_see_more_mobile": hook,
        },
        "findings": sorted(findings, key=lambda f: order[f["severity"]]),
        "counts": {sev: sum(1 for f in findings if f["severity"] == sev)
                   for sev in ("blocking", "major", "warning", "info")},
        "note": ("Character caps and fold positions are third-party-documented and stable. Reach "
                 "effects (link penalty, length band) come from third-party studies of public "
                 "posts, not from LinkedIn — see references/hook_and_fold_mechanics.md for the "
                 "per-claim confidence levels."),
    }


def render_human(r: dict) -> str:
    s = r["stats"]
    lines = [f"Post lint: {r['score']}/100 — {r['verdict']}", "=" * 56,
             f"{s['chars']}/{s['limit']} chars  ·  {s['hashtags']} hashtags  ·  "
             f"{s['links_in_body']} body links  ·  {s['emoji']} emoji  ·  {s['paragraphs']} blocks",
             "", "VISIBLE BEFORE \"…see more\" (mobile):",
             f"  {s['visible_before_see_more_mobile']}", ""]
    if r["findings"]:
        lines.append("Findings:")
        for f in r["findings"]:
            lines.append(f"  [{f['severity'].upper():<8}] {f['family']}: {f['finding']}")
            lines.append(f"             fix → {f['fix']}")
    else:
        lines.append("No findings. Ship it.")
    lines += ["", r["note"]]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Lint a LinkedIn post 0-100 (SHIP=0 / REVISE=2 / REWRITE=3).")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--text", help="The post body.")
    src.add_argument("--input", help="Read the post from a file ('-' for stdin).")
    ap.add_argument("--has-image", action="store_true",
                    help="The post carries an image or document (adds the alt-text check).")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Lint a built-in sample post.")
    args = ap.parse_args()

    if args.sample:
        text = SAMPLE_POST
    elif args.text:
        text = args.text
    elif args.input:
        text = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    else:
        ap.error("one of --text, --input, or --sample is required")

    result = lint(text, has_image=args.has_image)
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
