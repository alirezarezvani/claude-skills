#!/usr/bin/env python3
"""profile_completeness_auditor.py — score a LinkedIn profile 0-100 and rank the fixes.

Takes a JSON description of the profile YOU control (never scraped, never fetched —
you fill it in or dictate it) and returns a weighted completeness score plus a fix
list ordered by points-per-hour, so the first hour of work is the one that moves
the most.

Weights are set by what the section actually does for discovery and conversion,
not by how prominent it looks. The headline and the About opening are worth more
than education because they are what a stranger reads before deciding to care.

Input JSON (every key optional; missing = absent):
  {
    "photo": true, "banner_custom": false, "custom_url": true,
    "headline": "...", "about": "...",
    "current_role": {"title": "...", "bullets": ["cut X 40%", "..."]},
    "featured_items": 2, "featured_updated_days_ago": 400,
    "skills": ["python", "sql"], "recommendations_received": 1,
    "open_to_or_services": false, "education": true, "certifications": 0,
    "contact_info": true, "days_since_last_post": 90
  }

Exit codes:
  0  STRONG      (>= 80)
  2  INCOMPLETE  (50-79) — fix list returned
  3  WEAK        (< 50)  — the profile is costing you every visit it receives

Stdlib only. No network. Deterministic.
"""

import argparse
import json
import sys

# (key, weight, effort_hours, label)
CHECKS = [
    ("photo", 8, 0.5, "Profile photo"),
    ("banner", 5, 0.5, "Custom banner"),
    ("headline", 14, 1.0, "Headline that is not just a job title"),
    ("about", 14, 1.5, "About section with a self-contained opening"),
    ("experience", 12, 2.0, "Current role written as outcomes, not duties"),
    ("featured", 8, 0.5, "Featured section with something recent"),
    ("skills", 6, 0.3, "Skills listed and relevant"),
    ("recommendations", 8, 1.0, "Recommendations received"),
    ("custom_url", 3, 0.1, "Custom profile URL"),
    ("open_to", 4, 0.2, "Open To / Services block set"),
    ("education", 3, 0.2, "Education filled in"),
    ("certifications", 2, 0.5, "Certifications listed"),
    ("contact_info", 3, 0.2, "A reachable contact method"),
    ("activity", 10, 1.0, "Posted in the last 30 days"),
]

WHY = {
    "photo": "Profiles without a photo read as abandoned or fake; a stranger's first "
             "judgement happens before they read a word.",
    "banner": "The default blue banner is 1,584x396 pixels of unused positioning. It is the "
              "cheapest place to state what you do.",
    "headline": "It travels with every comment, search result, and invitation you send. A bare "
                "job title spends that space saying nothing a reader could not guess.",
    "about": "LinkedIn truncates it after roughly the first 265-300 characters. If those do not "
             "stand alone, the rest is never read.",
    "experience": "Duty lists are interchangeable across everyone with the same title. Outcomes "
                  "are the only part a reader cannot get elsewhere.",
    "featured": "The one place you choose what a visitor sees first. Empty, and they see whatever "
                "you last reposted.",
    "skills": "Skills are a matching surface for search and for recruiter filters.",
    "recommendations": "The only text on the profile written by someone other than you. Two "
                       "specific ones beat ten generic.",
    "custom_url": "Shareable, memorable, and it is a two-minute fix.",
    "open_to": "Tells LinkedIn's matching systems and human visitors what you want. Absent, they "
               "guess — usually wrong.",
    "education": "A weak signal on its own, but it is a common filter and a common icebreaker.",
    "certifications": "Only worth points where the certification is a gate in your field.",
    "contact_info": "A profile that converts interest into a conversation needs a way to start one.",
    "activity": "A profile with no recent activity converts a visit into nothing. Consistency, not "
                "volume, is the signal.",
}

SAMPLE = {
    "photo": True,
    "banner_custom": False,
    "custom_url": True,
    "headline": "Senior Software Engineer at Acme",
    "about": "Experienced engineer passionate about building great software.",
    "current_role": {"title": "Senior Software Engineer",
                     "bullets": ["Responsible for backend services",
                                 "Worked with cross-functional teams"]},
    "featured_items": 0,
    "featured_updated_days_ago": None,
    "skills": ["python", "sql", "aws"],
    "recommendations_received": 0,
    "open_to_or_services": False,
    "education": True,
    "certifications": 0,
    "contact_info": True,
    "days_since_last_post": 210,
}

OUTCOME_WORDS = ("cut", "grew", "reduced", "increased", "shipped", "launched", "saved",
                 "doubled", "migrated", "led", "%", "x", "from", "to")


def evaluate_check(key: str, p: dict) -> tuple:
    """Return (earned_fraction 0..1, detail string)."""
    if key == "photo":
        return (1.0, "present") if p.get("photo") else (0.0, "missing")
    if key == "banner":
        return (1.0, "custom") if p.get("banner_custom") else (0.0, "default LinkedIn banner")
    if key == "headline":
        h = (p.get("headline") or "").strip()
        if not h:
            return 0.0, "empty"
        title_only = len(h) < 60 and "|" not in h and "for " not in h.lower()
        return (0.4, f"job-title-shaped ({len(h)} chars) — run headline_scorer.py") if title_only \
            else (1.0, f"{len(h)} chars, structured")
    if key == "about":
        a = (p.get("about") or "").strip()
        if not a:
            return 0.0, "empty"
        if len(a) < 300:
            return 0.4, f"{len(a)} chars — too short to say anything specific"
        if len(a) < 600:
            return 0.7, f"{len(a)} chars — thin but usable"
        return 1.0, f"{len(a)} chars"
    if key == "experience":
        role = p.get("current_role") or {}
        bullets = role.get("bullets") or []
        if not role.get("title"):
            return 0.0, "no current role listed"
        if not bullets:
            return 0.3, "role listed with no description"
        with_outcome = [b for b in bullets
                        if any(w in b.lower() for w in OUTCOME_WORDS)]
        frac = 0.4 + 0.6 * (len(with_outcome) / max(1, len(bullets)))
        return min(1.0, frac), f"{len(with_outcome)}/{len(bullets)} bullets carry an outcome"
    if key == "featured":
        n = p.get("featured_items") or 0
        if not n:
            return 0.0, "empty"
        age = p.get("featured_updated_days_ago")
        if age is not None and age > 365:
            return 0.5, f"{n} item(s), last updated {age} days ago — stale"
        return 1.0, f"{n} item(s)"
    if key == "skills":
        n = len(p.get("skills") or [])
        return (1.0, f"{n} listed") if n >= 5 else (n / 5.0, f"only {n} listed")
    if key == "recommendations":
        n = p.get("recommendations_received") or 0
        return (1.0, f"{n} received") if n >= 2 else (n / 2.0, f"{n} received")
    if key == "custom_url":
        return (1.0, "set") if p.get("custom_url") else (0.0, "still the default /in/name-8a3f2b")
    if key == "open_to":
        return (1.0, "set") if p.get("open_to_or_services") else (0.0, "not set")
    if key == "education":
        return (1.0, "present") if p.get("education") else (0.0, "missing")
    if key == "certifications":
        n = p.get("certifications") or 0
        return (1.0, f"{n} listed") if n else (0.0, "none listed")
    if key == "contact_info":
        return (1.0, "present") if p.get("contact_info") else (0.0, "missing")
    if key == "activity":
        d = p.get("days_since_last_post")
        if d is None:
            return 0.0, "no posting activity reported"
        if d <= 30:
            return 1.0, f"last post {d} days ago"
        if d <= 90:
            return 0.4, f"last post {d} days ago — the profile reads as dormant"
        return 0.0, f"last post {d} days ago — effectively inactive"
    return 0.0, "unknown check"


def audit(profile: dict) -> dict:
    rows, fixes, total = [], [], 0.0
    for key, weight, effort, label in CHECKS:
        frac, detail = evaluate_check(key, profile)
        earned = round(weight * frac, 2)
        total += earned
        rows.append({"check": key, "label": label, "weight": weight,
                     "earned": earned, "detail": detail})
        lost = round(weight - earned, 2)
        if lost >= 0.5:
            fixes.append({
                "check": key, "label": label, "points_available": lost,
                "effort_hours": effort,
                "points_per_hour": round(lost / effort, 1),
                "current": detail,
                "why": WHY[key],
            })
    fixes.sort(key=lambda f: (-f["points_per_hour"], -f["points_available"]))
    score = round(total)
    verdict, code = (("STRONG", 0) if score >= 80 else
                     ("INCOMPLETE", 2) if score >= 50 else ("WEAK", 3))
    first_hour = []
    budget = 1.0
    for f in fixes:
        if f["effort_hours"] <= budget:
            first_hour.append(f["label"])
            budget -= f["effort_hours"]
    return {
        "score": score,
        "verdict": verdict,
        "exit_code": code,
        "checks": rows,
        "fixes_by_leverage": fixes,
        "first_hour_plan": first_hour,
        "points_recoverable_in_first_hour": round(
            sum(f["points_available"] for f in fixes if f["label"] in first_hour), 1),
        "note": ("Scores your own profile from your own description. Nothing is fetched, "
                 "scraped, or sent. Weights reflect discovery and conversion impact, not "
                 "LinkedIn's internal 'profile strength' meter, which is a different and "
                 "undocumented measure."),
    }


def render_human(r: dict) -> str:
    lines = [f"Profile completeness: {r['score']}/100 — {r['verdict']}", "=" * 56]
    for row in r["checks"]:
        mark = "OK " if row["earned"] >= row["weight"] - 0.01 else "-- "
        lines.append(f"  {mark}{row['label']:<48} {row['earned']:>5}/{row['weight']:<3} {row['detail']}")
    lines.append("\nFixes ranked by points per hour:")
    for f in r["fixes_by_leverage"]:
        lines.append(f"  +{f['points_available']:<5} pts  ~{f['effort_hours']}h  "
                     f"({f['points_per_hour']} pts/h)  {f['label']}")
        lines.append(f"        now : {f['current']}")
        lines.append(f"        why : {f['why']}")
    if r["first_hour_plan"]:
        lines.append(f"\nFirst hour: {', '.join(r['first_hour_plan'])} "
                     f"(+{r['points_recoverable_in_first_hour']} points)")
    lines.append(f"\n{r['note']}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Audit a LinkedIn profile 0-100 and rank fixes by points per hour "
                    "(STRONG=0 / INCOMPLETE=2 / WEAK=3).")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--input", help="Profile JSON file ('-' for stdin).")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true",
                    help="Audit a built-in sample profile (a typical unoptimized one).")
    ap.add_argument("--print-schema", action="store_true",
                    help="Print the input JSON schema/sample and exit.")
    args = ap.parse_args()

    if args.print_schema:
        print(json.dumps(SAMPLE, indent=2))
        return 0
    if args.sample:
        profile = SAMPLE
    elif args.input:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        try:
            profile = json.loads(raw)
        except json.JSONDecodeError as exc:
            print(f"ERROR: input is not valid JSON: {exc}", file=sys.stderr)
            return 4
    else:
        ap.error("--input or --sample is required (see --print-schema)")

    result = audit(profile)
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
