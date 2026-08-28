#!/usr/bin/env python3
"""outreach_message_builder.py — assemble one LinkedIn message, and refuse the template.

Cold outreach on LinkedIn fails for one structural reason: the message could have
been sent to anyone. This tool will not assemble a message without a
person-specific line — something you could only have written after actually
looking at what this person did — and it refuses an ask on a first-touch
connection note, because the note is for getting into the room, not for selling
in the doorway.

Caps enforced (🟡 third-party-documented; LinkedIn does not publish a limits page):
  connection note   200 characters (free) / 300 (Premium) — use --premium
  DM / InMail       no practical cap, but this tool warns past 600 characters
                    because reply rate falls off a cliff on a phone screen

Nothing is sent. The output is text you paste, one person at a time. That is not
a limitation of the tool; automated sending is prohibited by LinkedIn's User
Agreement §8.2 and is the fastest route to a restricted account.

Exit codes:
  0  PASS  — assembled and clean
  2  WARN  — assembled, with findings worth fixing
  3  FAIL  — refused: missing the person-specific line, over the cap, or pitching too early

Stdlib only. No network. Nothing is transmitted anywhere.
"""

import argparse
import json
import re
import sys

CAPS = {"connection": {"free": 200, "premium": 300},
        "dm": {"free": 1800, "premium": 1800},
        "inmail": {"free": 1900, "premium": 1900},
        "followup": {"free": 1200, "premium": 1200}}
DM_COMFORT = 600

DEAD_PHRASES = [
    ("i came across your profile", "It tells them nothing. Say what you were reading when you found them."),
    ("i'd love to pick your brain", "It asks for unpaid time with no bounded question."),
    ("i would love to pick your brain", "It asks for unpaid time with no bounded question."),
    ("hope this finds you well", "Filler. Delete it and start with the specific line."),
    ("hope you're doing well", "Filler. Delete it and start with the specific line."),
    ("quick question", "It is never quick, and everyone knows it."),
    ("just following up", "Say what changed since last time, or do not follow up."),
    ("touch base", "Says nothing about what you want."),
    ("synergy", "Nobody has ever replied to this word."),
    ("i'll keep it short", "Then keep it short instead of announcing it."),
    ("as a fellow", "Category membership is not a reason to connect."),
    ("i see we're both in", "So are two million other people."),
    ("let's connect", "A request with no reason attached."),
    ("15 minutes of your time", "Fine as a second-touch ask; never in a first-touch note."),
]

PITCH_RE = re.compile(
    r"\b(our (product|platform|solution|service|tool)|we help companies|book a (call|demo)|"
    r"schedule a (call|demo)|are you the right person|decision[- ]maker|"
    r"i'?d like to show you|free trial|pricing|proposal)\b", re.I)

ASK_RE = re.compile(r"\b(call|chat|meeting|demo|coffee|zoom|15 min|30 min|hop on|jump on)\b", re.I)

SAMPLE = {
    "type": "connection",
    "recipient": "Priya",
    "specific_line": "Your teardown of the dbt exposures rollout matched what broke for us at "
                     "step three.",
    "reason": "I am working the same problem from the platform side and would like to follow "
              "what you publish.",
    "ask": "",
    "premium": False,
}


def assemble(parts: dict) -> str:
    name = (parts.get("recipient") or "").strip()
    specific = (parts.get("specific_line") or "").strip()
    reason = (parts.get("reason") or "").strip()
    ask = (parts.get("ask") or "").strip()
    chunks = []
    if name:
        chunks.append(f"{name} —")
    if specific:
        chunks.append(specific)
    if reason:
        chunks.append(reason)
    if ask:
        chunks.append(ask)
    return " ".join(chunks).strip()


def validate(text: str, parts: dict, mtype: str, premium: bool) -> list:
    findings = []
    low = text.lower()

    def add(sev, check, finding, fix):
        findings.append({"severity": sev, "check": check, "finding": finding, "fix": fix})

    specific = (parts.get("specific_line") or "").strip()
    if not specific:
        add("blocking", "person-specific-line",
            "No person-specific line. Without it this is a template, and a template is the "
            "thing being ignored.",
            "Read one thing they published and quote the part you disagreed with or used. "
            "If you will not spend three minutes reading, do not spend theirs.")
    elif len(specific.split()) < 6:
        add("major", "person-specific-line",
            f"The specific line is {len(specific.split())} words — too short to prove you read "
            "anything.",
            "Name the artifact and the part of it that mattered.")
    elif not re.search(r"\b(your|you)\b", specific, re.I):
        add("warning", "person-specific-line",
            "The specific line does not refer to them at all.",
            "Anchor it: 'your post on…', 'the talk you gave at…'.")

    cap = CAPS[mtype]["premium" if premium else "free"]
    n = len(text)
    if n > cap:
        add("blocking", "length",
            f"{n} characters — {n - cap} over the {cap}-character cap for a "
            f"{mtype} ({'Premium' if premium else 'free'} account).",
            "Cut the reason, keep the specific line. The reason can wait for the reply.")
    elif mtype in ("dm", "inmail", "followup") and n > DM_COMFORT:
        add("warning", "length",
            f"{n} characters. Past ~{DM_COMFORT} the message is a wall on a phone and reply "
            "rate drops.",
            "One specific line, one reason, one bounded ask. Everything else is for the reply.")

    if mtype == "connection":
        ask = (parts.get("ask") or "").strip()
        if ask:
            add("blocking", "premature-ask",
                "A connection note carries an ask. The note is for getting into the room; the "
                "ask belongs in the conversation after they accept.",
                "Move it. A third-party study of ~13M outreach touches found notes barely move "
                "acceptance (about 26.4% either way) but roughly double the post-accept reply "
                "rate — the note earns the conversation, not the meeting.")
        if PITCH_RE.search(low):
            add("blocking", "pitch-on-first-touch",
                "Pitch language in a first-touch connection note.",
                "Delete it. Nobody has ever bought from a connection request, and the request "
                "is the only impression you get.")
    else:
        if PITCH_RE.search(low) and not ASK_RE.search(low):
            add("warning", "pitch-without-ask",
                "Product language with no clear, bounded ask.",
                "Either make the ask explicit and small, or cut the product language.")

    dead = [(p, why) for p, why in DEAD_PHRASES if p in low]
    if dead:
        add("major", "dead-phrases",
            "Phrases that mark this as bulk: " + "; ".join(f"'{p}' — {why}" for p, why in dead),
            "Cut each one. What remains is either specific or it is nothing, and nothing is "
            "better than bulk.")

    if not (parts.get("reason") or "").strip() and mtype == "connection":
        add("warning", "reason",
            "No reason to connect stated.",
            "One clause: what you want to follow, learn, or compare notes on.")

    if parts.get("recipient") and parts["recipient"].strip().lower() in (
            "there", "team", "sir", "madam", "friend", "connection"):
        add("major", "salutation",
            f"'{parts['recipient']}' is a placeholder greeting.",
            "Use their name, spelled the way they spell it.")

    return findings


def build(parts: dict, mtype: str, premium: bool) -> dict:
    text = assemble(parts)
    findings = validate(text, parts, mtype, premium)
    blocking = [f for f in findings if f["severity"] == "blocking"]
    verdict, code = (("FAIL", 3) if blocking
                     else ("WARN", 2) if findings else ("PASS", 0))
    cap = CAPS[mtype]["premium" if premium else "free"]
    return {
        "verdict": verdict,
        "exit_code": code,
        "type": mtype,
        "premium": premium,
        "message": text,
        "chars": len(text),
        "cap": cap,
        "findings": findings,
        "send_rule": ("Paste and send this yourself, to this one person. Nothing here is "
                      "transmitted by the tool, and automating the send would violate "
                      "LinkedIn's User Agreement §8.2."),
        "followup_rule": ("One follow-up, at least a week later, only if you have something new "
                          "to say. A second follow-up with no new information is the point at "
                          "which you become the thing you were avoiding."),
    }


def render_human(r: dict) -> str:
    lines = [f"Outreach ({r['type']}): {r['verdict']}  "
             f"[{r['chars']}/{r['cap']} chars"
             f"{', Premium' if r['premium'] else ''}]",
             "=" * 56, "", r["message"] or "(nothing assembled)", ""]
    if r["findings"]:
        lines.append("Findings:")
        for f in r["findings"]:
            lines.append(f"  [{f['severity'].upper():<8}] {f['check']}: {f['finding']}")
            lines.append(f"             fix → {f['fix']}")
    else:
        lines.append("No findings.")
    lines += ["", r["send_rule"], "", r["followup_rule"]]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Assemble one LinkedIn outreach message (PASS=0 / WARN=2 / FAIL=3). "
                    "Nothing is sent.")
    ap.add_argument("--type", choices=sorted(CAPS), default="connection")
    ap.add_argument("--recipient", help="Their first name.")
    ap.add_argument("--specific-line", help="The line only this person could receive. Required.")
    ap.add_argument("--reason", help="Why you want the connection.")
    ap.add_argument("--ask", default="", help="The ask (never on a first-touch connection note).")
    ap.add_argument("--premium", action="store_true",
                    help="Premium account (300-char connection notes).")
    ap.add_argument("--input", help="Read all parts from a JSON file ('-' for stdin).")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Build the built-in sample message.")
    ap.add_argument("--print-schema", action="store_true", help="Print the JSON shape and exit.")
    args = ap.parse_args()

    if args.print_schema:
        print(json.dumps(SAMPLE, indent=2))
        return 0
    if args.sample:
        parts, mtype, premium = SAMPLE, SAMPLE["type"], SAMPLE["premium"]
    elif args.input:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        try:
            parts = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"ERROR: input is not valid JSON: {exc}", file=sys.stderr)
            return 4
        mtype = parts.get("type", args.type)
        premium = bool(parts.get("premium", args.premium))
        if mtype not in CAPS:
            print(f"ERROR: unknown message type '{mtype}'", file=sys.stderr)
            return 4
    else:
        parts = {"recipient": args.recipient, "specific_line": args.specific_line,
                 "reason": args.reason, "ask": args.ask}
        mtype, premium = args.type, args.premium
        if not any(parts.values()):
            ap.error("provide --specific-line (or --input / --sample / --print-schema)")

    result = build(parts, mtype, premium)
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
