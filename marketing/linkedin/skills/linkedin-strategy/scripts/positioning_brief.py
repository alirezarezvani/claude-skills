#!/usr/bin/env python3
"""positioning_brief.py — validate a LinkedIn positioning brief before any post is written.

Posting without a brief produces a feed of unrelated observations that reads as
noise even when each individual post is good. This tool does not invent the brief
— that is a conversation, and the SKILL.md walks it. It enforces the four things a
brief has to survive:

  1. An objective that is one of the six real ones, not "build my brand".
  2. An audience specific enough that someone could be excluded from it.
  3. Two to four pillars whose shares sum to 100, at least one backed by proof you
     already have, and at least one small enough to be an experiment.
  4. An exclusion list. A positioning that excludes nothing positions nothing.

It then emits observable 90-day criteria for the declared objective, so "is this
working" has an answer that does not depend on how the week felt.

Exit codes:
  0  brief is sound
  2  brief has fixable defects (each one named)
  3  brief is not usable — the objective or audience is too vague to proceed

Stdlib only. No network. Deterministic.
"""

import argparse
import json
import sys

OBJECTIVES = {
    "career-change": {
        "label": "Move into a different role or field",
        "criteria": [
            "≥3 inbound conversations with people who hold the target role (not recruiters)",
            "≥1 referral or intro offered without you asking",
            "Profile headline and About describe the target role, not the current one",
        ],
        "audience_hint": "hiring managers and practitioners in the target field, not your "
                         "current colleagues",
    },
    "consulting": {
        "label": "Generate consulting or freelance work",
        "criteria": [
            "≥5 qualified inbound enquiries (they named a budget, timeline, or scoped problem)",
            "≥1 closed engagement traceable to a post or a comment thread",
            "Featured section contains one artifact a buyer can evaluate in 60 seconds",
        ],
        "audience_hint": "the person who signs the invoice, not the person who does the work",
    },
    "thought-leadership": {
        "label": "Be cited as a credible voice on one specific thing",
        "criteria": [
            "≥3 posts where practitioners in the field argued with you substantively in comments",
            "≥1 invitation (podcast, panel, guest post) that referenced a specific post",
            "You can name the one sentence people now associate with you",
        ],
        "audience_hint": "practitioners who could disagree with you competently",
    },
    "hiring": {
        "label": "Attract candidates to a team you are building",
        "criteria": [
            "≥10 candidate conversations sourced without an agency",
            "≥2 candidates who referenced a specific post in their first message",
            "The team's actual working conditions are described somewhere public",
        ],
        "audience_hint": "the specific engineer/designer/seller you want, not 'talent'",
    },
    "fundraising": {
        "label": "Build investor and operator awareness ahead of a raise",
        "criteria": [
            "≥5 investor or operator conversations initiated by them",
            "A public track record of the thesis dated before the raise, not after",
            "No confidential metric published that the cap table would object to",
        ],
        "audience_hint": "operators and angels in your category, not generalist VC accounts",
    },
    "community": {
        "label": "Build a durable group around a shared problem",
        "criteria": [
            "≥20 named people who reliably show up in your comments",
            "≥1 recurring format the audience anticipates",
            "Conversation continues without you starting it",
        ],
        "audience_hint": "people with the same problem, who would recognise each other",
    },
}

VAGUE_AUDIENCE = [
    "everyone", "professionals", "people", "business leaders", "the industry",
    "anyone interested", "my network", "b2b", "companies", "the market",
    "decision makers", "tech people", "the community",
]

SAMPLE = {
    "objective": "consulting",
    "audience": "heads of data at Series A-B SaaS companies who have three analysts and no "
                "analytics engineer, and whose CEO does not trust the dashboard",
    "pillars": [
        {"name": "Trust debt in analytics", "why_you": "I have rebuilt this at three companies",
         "proof": "the 6-vs-35-days handoff measurement", "share": 40},
        {"name": "dbt and modelling decisions", "why_you": "I maintain two OSS dbt packages",
         "proof": "public repos + a conference talk", "share": 35},
        {"name": "Hiring the first analytics engineer",
         "why_you": "I have written three of these job specs",
         "proof": "two hires who are still in role", "share": 15},
        {"name": "Field notes / experiments", "why_you": "unproven, testing the appetite",
         "proof": "", "share": 10},
    ],
    "exclusions": [
        "generic AI commentary — I have no edge there",
        "hot takes on other companies' layoffs",
        "vendor comparison posts that would compromise client confidentiality",
    ],
}


def validate(brief: dict) -> dict:
    findings, blocking = [], []

    def add(sev, field, msg, fix):
        entry = {"severity": sev, "field": field, "finding": msg, "fix": fix}
        (blocking if sev == "blocking" else findings).append(entry)

    obj = (brief.get("objective") or "").strip().lower()
    if obj not in OBJECTIVES:
        add("blocking", "objective",
            f"'{brief.get('objective')}' is not one of the six real objectives "
            f"({', '.join(OBJECTIVES)}).",
            "Pick the one that would make you stop posting if it were achieved. "
            "'Build my brand' is not an objective; it is a side effect of one.")

    aud = (brief.get("audience") or "").strip()
    aud_low = aud.lower()
    if not aud:
        add("blocking", "audience", "No audience declared.",
            "Name them so specifically that a real person could be excluded.")
    elif len(aud.split()) < 6 or any(v == aud_low or aud_low.startswith(v) for v in VAGUE_AUDIENCE):
        add("blocking", "audience",
            f"'{aud}' is too broad to exclude anyone, which means it cannot guide a single "
            "editorial decision.",
            "Add the situation they are in, not just their title: role + company stage + the "
            "problem they have this quarter."
            + (f" For {obj}, aim at {OBJECTIVES[obj]['audience_hint']}." if obj in OBJECTIVES else ""))

    pillars = brief.get("pillars") or []
    if not 2 <= len(pillars) <= 4:
        add("blocking", "pillars",
            f"{len(pillars)} pillar(s). Under two is a monologue; over four is a magazine "
            "nobody subscribed to.",
            "Two to four. If a fifth matters that much, it is displacing one of the others.")
    else:
        total = sum(int(p.get("share") or 0) for p in pillars)
        if abs(total - 100) > 2:
            add("major", "pillars", f"Shares sum to {total}, not 100.",
                "Rebalance. The share is a budget: it decides what gets cut in a busy week.")
        backed = [p for p in pillars if (p.get("proof") or "").strip()]
        if not backed:
            add("blocking", "pillars",
                "No pillar has a proof asset behind it. Every pillar is a claim you would have "
                "to invent evidence for.",
                "At least one pillar must rest on something that already exists: a shipped "
                "project, a measurement, a repo, a hire, a talk.")
        elif len(backed) < len(pillars) - 1:
            add("major", "pillars",
                f"Only {len(backed)}/{len(pillars)} pillars are proof-backed.",
                "One unproven experimental pillar is healthy. Two or more means you are "
                "positioning on ambition rather than track record.")
        experimental = [p for p in pillars if int(p.get("share") or 0) <= 20]
        if not experimental:
            add("major", "pillars",
                "Every pillar is a major commitment; there is no small slot to test something new.",
                "Keep one pillar at 10-20%. It is where next quarter's main pillar comes from.")
        for p in pillars:
            if not (p.get("why_you") or "").strip():
                add("major", "pillars",
                    f"Pillar '{p.get('name', '?')}' has no 'why you'. Anyone could post it.",
                    "State the specific standing you have. If there is none, cut the pillar.")

    exclusions = [e for e in (brief.get("exclusions") or []) if str(e).strip()]
    if len(exclusions) < 2:
        add("blocking", "exclusions",
            f"{len(exclusions)} exclusion(s). A positioning that excludes nothing is not a "
            "positioning — it is availability.",
            "Name at least two topics you will not post about, and why. The trending one you "
            "have no edge on is usually the first.")

    all_findings = blocking + findings
    if blocking:
        verdict, code = ("NOT_USABLE", 3) if any(
            f["field"] in ("objective", "audience") for f in blocking) else ("DEFECTIVE", 2)
    elif findings:
        verdict, code = "DEFECTIVE", 2
    else:
        verdict, code = "SOUND", 0

    out = {
        "verdict": verdict,
        "exit_code": code,
        "objective": obj if obj in OBJECTIVES else None,
        "objective_label": OBJECTIVES[obj]["label"] if obj in OBJECTIVES else None,
        "audience": aud,
        "pillar_mix": [{"name": p.get("name"), "share": p.get("share"),
                        "proof_backed": bool((p.get("proof") or "").strip())}
                       for p in pillars],
        "exclusions": exclusions,
        "findings": all_findings,
        "rule": ("The brief is the editorial constitution. When a post idea does not fit a "
                 "pillar, the answer is not to add a pillar — it is to not post it, or to "
                 "put it in the experimental slot and see."),
    }
    if obj in OBJECTIVES:
        out["ninety_day_criteria"] = OBJECTIVES[obj]["criteria"]
        out["criteria_rule"] = ("Observable by someone other than you. Follower count is not on "
                                "this list on purpose — it moves for reasons unrelated to whether "
                                "the objective is being met.")
    return out


def render_human(r: dict) -> str:
    lines = [f"Positioning brief: {r['verdict']}", "=" * 52]
    if r["objective_label"]:
        lines.append(f"Objective : {r['objective']} — {r['objective_label']}")
    lines.append(f"Audience  : {r['audience'] or '(none)'}")
    if r["pillar_mix"]:
        lines.append("Pillars   :")
        for p in r["pillar_mix"]:
            mark = "proof-backed" if p["proof_backed"] else "UNPROVEN"
            lines.append(f"   {str(p['share']):>3}%  {p['name']}  [{mark}]")
    if r["exclusions"]:
        lines.append("Will not post about:")
        for e in r["exclusions"]:
            lines.append(f"   - {e}")
    if r["findings"]:
        lines.append("\nFindings:")
        for f in r["findings"]:
            lines.append(f"  [{f['severity'].upper():<8}] {f['field']}: {f['finding']}")
            lines.append(f"             fix → {f['fix']}")
    else:
        lines.append("\nNo findings.")
    if r.get("ninety_day_criteria"):
        lines.append("\n90-day success criteria:")
        for c in r["ninety_day_criteria"]:
            lines.append(f"   [ ] {c}")
        lines.append(f"   ({r['criteria_rule']})")
    lines.append(f"\n{r['rule']}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Validate a LinkedIn positioning brief "
                    "(sound=0 / defective=2 / not-usable=3).")
    ap.add_argument("--objective", choices=sorted(OBJECTIVES))
    ap.add_argument("--audience", help="Who this is for, specifically.")
    ap.add_argument("--pillar", action="append", default=[],
                    help="name:why_you:proof:share — repeatable. Empty proof = experimental.")
    ap.add_argument("--exclude", action="append", default=[],
                    help="A topic you will not post about. Repeatable.")
    ap.add_argument("--input", help="Read the whole brief from a JSON file ('-' for stdin).")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Validate a built-in sample brief.")
    ap.add_argument("--print-schema", action="store_true", help="Print the JSON shape and exit.")
    args = ap.parse_args()

    if args.print_schema:
        print(json.dumps(SAMPLE, indent=2))
        return 0
    if args.sample:
        brief = SAMPLE
    elif args.input:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        try:
            brief = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"ERROR: input is not valid JSON: {exc}", file=sys.stderr)
            return 4
    else:
        pillars = []
        for spec in args.pillar:
            parts = spec.split(":")
            while len(parts) < 4:
                parts.append("")
            name, why, proof, share = parts[0], parts[1], parts[2], parts[3]
            try:
                share_val = int(share) if share.strip() else 0
            except ValueError:
                print(f"ERROR: pillar share must be an integer: '{spec}'", file=sys.stderr)
                return 4
            pillars.append({"name": name.strip(), "why_you": why.strip(),
                            "proof": proof.strip(), "share": share_val})
        brief = {"objective": args.objective, "audience": args.audience,
                 "pillars": pillars, "exclusions": args.exclude}
        if not brief["objective"] and not brief["audience"]:
            ap.error("provide --objective and --audience (or --input / --sample)")

    result = validate(brief)
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
