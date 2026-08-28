#!/usr/bin/env python3
"""linkedin_policy_gate.py — refuse LinkedIn tactics that break the User Agreement.

Every lane in the `linkedin` plugin passes through this gate before any drafting
work happens. It classifies a described tactic against LinkedIn's User Agreement
(§8.2 "Don'ts"), the Prohibited Software and Extensions policy, and the
Professional Community Policies, then returns ALLOW / CONSTRAIN / REFUSE.

The point is not legal advice. The point is that an account restriction ends the
organic-growth project, so the tactics that risk one are refused up front instead
of drafted and regretted. A REFUSE always names the rule and offers the compliant
substitute — this gate never just says no.

Deterministic: same text in, same verdict out. Stdlib only. No network calls,
no LinkedIn API access, nothing is ever sent anywhere.

Exit codes:
  0  ALLOW      — nothing in the request trips a rule; proceed
  3  CONSTRAIN  — allowed, but only under the named constraints (proceed and honor them)
  4  REFUSE     — breaks a named rule; do not draft it, offer the substitute instead

Usage:
  python3 linkedin_policy_gate.py --text "auto-connect with 500 recruiters a week"
  python3 linkedin_policy_gate.py --input plan.md --output human
  python3 linkedin_policy_gate.py --sample
"""

import argparse
import json
import re
import sys

# ---------------------------------------------------------------------------
# Refusal rules. Each carries the policy anchor and the compliant substitute,
# because a gate that only blocks teaches the user nothing.
# ---------------------------------------------------------------------------
REFUSE_RULES = [
    {
        "id": "P1-AUTOMATION",
        "title": "Automated activity on LinkedIn",
        "anchor": "LinkedIn User Agreement §8.2 (bots/automated methods to access the "
                  "Services, add contacts, send messages, create/comment/like/share posts)",
        "patterns": [
            r"\bauto[- ]?(connect|invite|dm|message|like|comment|follow|endorse|post|apply)\w*",
            r"\bautomat(e|ed|ing|ion)\b(?!.{0,40}\bis (prohibited|banned|against)\b)",
            r"\bbot\b", r"\bbots\b", r"\bheadless browser\b", r"\bselenium\b", r"\bpuppeteer\b",
            r"\bbrowser (extension|plugin|add-?on)\b.{0,40}\b(linkedin|connect|message)\b",
            r"\bscript that (logs? in|clicks?|sends?|connects?)\b",
        ],
        "substitute": "Do the same volume by hand on a capped schedule. "
                      "`linkedin-engagement/scripts/outreach_volume_guard.py` sizes a manual "
                      "cadence you can actually sustain; the plugin drafts the text, you press send.",
    },
    {
        "id": "P2-SCRAPING",
        "title": "Scraping or bulk-copying member data",
        "anchor": "LinkedIn User Agreement §8.2 (crawlers/scrapers to copy profiles or other "
                  "data) + Prohibited Software and Extensions policy",
        "patterns": [
            r"\bscrap(e|ed|er|ing)\b", r"\bcrawl(er|ing)?\b",
            r"\b(harvest|extract|mine)\b.{0,30}\b(email|profile|contact|lead|member)s?\b",
            r"\bexport\b.{0,25}\b(connections?|leads?|profiles?|members?)\b.{0,25}\b(list|database|csv)\b",
            r"\bemail finder\b", r"\bfind (their|his|her) email\b",
            r"\bbuild(ing)? a (lead )?(list|database)\b.{0,30}\bfrom linkedin\b",
        ],
        "substitute": "Use LinkedIn's own export of YOUR data (Settings → Data privacy → "
                      "Get a copy of your data) and LinkedIn-native search. Analytics work in "
                      "this plugin runs on your own exported post/profile stats, never on "
                      "other members' data.",
    },
    {
        "id": "P3-INAUTHENTIC",
        "title": "Inauthentic engagement (pods, bought signals)",
        "anchor": "LinkedIn User Agreement §8.2 (drive inauthentic engagement) + Professional "
                  "Community Policies (be authentic / no fake engagement)",
        "patterns": [
            r"\b(engagement|comment|like|linkedin) ?pod\b", r"\bpods?\b(?=.{0,30}\b(join|run|group)\b)",
            r"\bbuy(ing)? (followers?|likes?|comments?|connections?|views?|impressions?)\b",
            r"\b(fake|paid|bought|purchased) (followers?|engagement|likes?|comments?)\b",
            r"\bengagement (group|ring|circle|exchange|swap)\b",
            r"\blike[- ]?for[- ]?like\b", r"\bcomment[- ]?for[- ]?comment\b",
        ],
        "substitute": "Build a real reciprocity list instead: "
                      "`linkedin-engagement/scripts/comment_target_planner.py` picks accounts "
                      "whose audience overlaps yours and budgets genuine daily comments. Slower, "
                      "and it survives an audit.",
    },
    {
        "id": "P4-IDENTITY",
        "title": "Fake identity, duplicate accounts, impersonation",
        "anchor": "LinkedIn User Agreement §8.2 (create a false identity, misrepresent your "
                  "identity, use another's account) + Professional Community Policies",
        "patterns": [
            r"\bfake (profile|account|persona|identity)\b",
            r"\b(second|burner|dummy|alt|multiple) (linkedin )?accounts?\b",
            r"\bimpersonat(e|ing|ion)\b",
            r"\bpretend(ing)? to be\b", r"\bpose as\b",
            r"\bghost(write|writing)\b.{0,30}\bwithout\b.{0,20}\b(disclos|know)\w*",
            r"\bpost as (?:my|the) (ceo|founder|boss|client)\b.{0,40}\bwithout\b",
        ],
        "substitute": "One real profile, your real name. Ghostwriting for an executive is fine "
                      "when that executive knows and approves every post — the account holder is "
                      "the author of record.",
    },
    {
        "id": "P5-BULK-MESSAGING",
        "title": "Bulk or unsolicited mass messaging",
        "anchor": "LinkedIn User Agreement §8.2 (send or redirect messages by automated means; "
                  "spam) + Professional Community Policies (no spam/unsolicited commercial content)",
        "patterns": [
            r"\b(mass|bulk|blast|spray)\b.{0,20}\b(dm|message|inmail|invite|connection)s?\b",
            r"\b(dm|message|inmail)\b.{0,20}\b(everyone|all my connections|the whole list|1000|500)\b",
            r"\bsend the same (message|dm|note) to\b",
            r"\bcopy[- ]?paste\b.{0,25}\b(dm|message|outreach)\b.{0,25}\b(everyone|all|hundreds)\b",
            r"\bdrip (campaign|sequence)\b.{0,30}\blinkedin\b",
        ],
        "substitute": "Per-person messages with a specific reason, sent by hand, under a weekly "
                      "cap. `outreach_message_builder.py` refuses a template with no "
                      "person-specific line for exactly this reason.",
    },
    {
        "id": "P6-FABRICATION",
        "title": "Fabricated credentials, metrics, or social proof",
        "anchor": "LinkedIn User Agreement §8.2 (post inaccurate information) + Professional "
                  "Community Policies (no false or misleading content); FTC endorsement rules "
                  "apply to testimonials",
        "patterns": [
            r"\b(make up|invent|fabricate|fake)\b.{0,30}\b(metric|number|result|case study|"
            r"testimonial|client|revenue|stat|credential|degree|certification)s?\b",
            r"\b(inflate|exaggerate)\b.{0,25}\b(number|revenue|result|headcount|arr|mrr)s?\b",
            r"\bpretend (i|we) (have|had|built|grew|raised)\b",
            r"\bsay (i|we) (have|had) \d+.{0,20}\b(clients?|customers?|users?)\b.{0,25}\bwe don'?t\b",
        ],
        "substitute": "Use a real number, a bounded range, or a qualitative claim. "
                      "If the proof does not exist yet, the post is about the process, not the "
                      "result — that is a legitimate post and it ages well.",
    },
    {
        "id": "P7-PROHIBITED-TOOLS",
        "title": "Named third-party automation tools",
        "anchor": "LinkedIn Help — Prohibited Software and Extensions (third-party software that "
                  "scrapes, modifies, or automates activity on LinkedIn is not permitted)",
        "patterns": [
            r"\b(dux[- ]?soup|phantom ?buster|expandi|linked ?helper|meet ?alfred|waalaxy|"
            r"octopus ?crm|lempod|zopto|we[- ]?connect|prospectin|salesflow|closely|"
            r"linkedin ?helper|texau|captain ?data)\b",
        ],
        "substitute": "Native LinkedIn scheduling and LinkedIn's own Marketing Developer "
                      "Platform partners are the supported path. This plugin never logs into "
                      "your account at all — it hands you text.",
    },
]

# ---------------------------------------------------------------------------
# Constraint rules. Legitimate tactics that go wrong at volume or without a
# disclosure. These proceed, but the constraint is printed and must be honored.
# ---------------------------------------------------------------------------
CONSTRAIN_RULES = [
    {
        "id": "C1-OUTREACH-VOLUME",
        "title": "Manual outreach at campaign scale",
        "patterns": [
            r"\b(outreach|connection request|invite|cold dm|cold message|inmail)\b",
            r"\bnetworking (campaign|push|sprint)\b",
        ],
        "constraint": "Manual send only, one person at a time, every message carrying a line "
                      "that could only have been written for that person. Run "
                      "`outreach_volume_guard.py` before sending — LinkedIn enforces an "
                      "invitation limit (roughly 100/week for most accounts) and withdrawn "
                      "invites still count against it.",
    },
    {
        "id": "C2-ENGAGEMENT-BAIT",
        "title": "Engagement bait",
        "patterns": [
            r"\bcomment ['\"][\w ]{1,24}['\"]\s*(below|and i'?ll|to get|for the|if you)\b",
            r"\bcomment ['\"]?\w{1,14}['\"]? below\b",
            r"\band i'?ll (dm|send) (you )?(the|it|a|my)\b",
            r"\b(like|repost|share) (this )?if you\b",
            r"\bagree\?\s*$", r"\btag (someone|3|three|a friend)\b",
            r"\bdm me ['\"]\w+['\"]\b",
        ],
        "constraint": "LinkedIn's Professional Community Policies name engagement bait as "
                      "content it demotes. Ask a real question the post has earned instead — "
                      "`post_linter.py` flags bait patterns as blocking findings.",
    },
    {
        "id": "C4-EMPLOYER-CONTEXT",
        "title": "Posting about an employer, client, or regulated topic",
        "patterns": [
            r"\b(my employer|my company|our client|my client|internal|confidential|"
            r"under nda|customer data|patient|clinical|financial advice|investment advice)\b",
            r"\b(layoff|acquisition|funding round|earnings)\b",
        ],
        "constraint": "Check the employment agreement, the client NDA, and any sector rules "
                      "(financial promotion, medical claims, securities disclosure) before "
                      "posting. Named third parties should consent. When unsure, describe the "
                      "pattern without the identifying detail.",
    },
]

# Always returned, on every verdict. These are not triggered by wording — they
# hold for every piece of LinkedIn work this plugin produces.
STANDING_CONSTRAINTS = [
    "Author of record: the account holder publishes it, so the account holder reads "
    "every line. Cut anything you would not say out loud in a room of peers.",
    "Nothing is auto-sent. This plugin has no LinkedIn credentials and makes no API "
    "calls; every output is text you paste and post yourself.",
    "No claim you cannot substantiate. A real number, a bounded range, or a "
    "qualitative statement — never a placeholder metric that ships.",
]

SAMPLE_TEXT = ("I want to grow to 20k followers in six months. Plan: use Dux-Soup to "
               "auto-connect with 500 recruiters a week, join a comment pod for the first "
               "90 minutes, and blast the same DM to everyone who accepts.")


def _scan(text: str, rules: list, key: str) -> list:
    low = text.lower()
    hits = []
    for rule in rules:
        matched = []
        for pat in rule["patterns"]:
            for m in re.finditer(pat, low, re.IGNORECASE):
                snippet = m.group(0).strip()
                if snippet and snippet not in matched:
                    matched.append(snippet)
        if matched:
            hits.append({
                "id": rule["id"],
                "title": rule["title"],
                "matched": matched[:5],
                "anchor": rule.get("anchor", ""),
                key: rule[key],
            })
    return hits


def evaluate(text: str) -> dict:
    refusals = _scan(text, REFUSE_RULES, "substitute")
    constraints = _scan(text, CONSTRAIN_RULES, "constraint")
    if refusals:
        verdict, code = "REFUSE", 4
    elif constraints:
        verdict, code = "CONSTRAIN", 3
    else:
        verdict, code = "ALLOW", 0
    return {
        "verdict": verdict,
        "exit_code": code,
        "refusals": refusals,
        "constraints": constraints,
        "input_preview": text.strip()[:280],
        "standing_constraints": STANDING_CONSTRAINTS,
        "disclaimer": ("Deterministic pattern check against LinkedIn's published policies, not "
                       "legal advice and not exhaustive. A clean ALLOW does not certify a plan; "
                       "it means nothing in the text tripped a known rule."),
    }


def render_human(result: dict) -> str:
    out = [f"LinkedIn policy gate: {result['verdict']}", "=" * 46]
    if result["refusals"]:
        out.append("\nREFUSED — these break a named LinkedIn rule:\n")
        for r in result["refusals"]:
            out.append(f"  [{r['id']}] {r['title']}")
            out.append(f"      matched : {', '.join(r['matched'])}")
            out.append(f"      rule    : {r['anchor']}")
            out.append(f"      instead : {r['substitute']}\n")
    if result["constraints"]:
        out.append("\nALLOWED UNDER CONSTRAINT — proceed, but honor these:\n")
        for c in result["constraints"]:
            out.append(f"  [{c['id']}] {c['title']}")
            out.append(f"      matched : {', '.join(c['matched'])}")
            out.append(f"      honor   : {c['constraint']}\n")
    if result["verdict"] == "ALLOW":
        out.append("\nNothing in this request trips a known rule. Proceed.\n")
    out.append("\nStanding constraints (always apply):")
    for sc in result["standing_constraints"]:
        out.append(f"  - {sc}")
    out.append("")
    out.append(result["disclaimer"])
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Classify a LinkedIn tactic against the User Agreement: "
                    "ALLOW (0) / CONSTRAIN (3) / REFUSE (4).")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--text", help="The tactic, plan, or request to check.")
    src.add_argument("--input", help="Read the text from a file ('-' for stdin).")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true",
                    help="Run the built-in sample (a plan that trips four rules).")
    args = ap.parse_args()

    if args.sample:
        text = SAMPLE_TEXT
    elif args.text:
        text = args.text
    elif args.input:
        text = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    else:
        ap.error("one of --text, --input, or --sample is required")

    result = evaluate(text)
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
