#!/usr/bin/env python3
"""headline_scorer.py — score a LinkedIn headline 0-100 on the five things it must do.

The headline is the single highest-leverage string on LinkedIn: it rides along with
every comment you leave, every search result you appear in, and every connection
request you send. Most of them are a job title, which tells a reader nothing they
could not have guessed.

Five dimensions, 20 points each:
  AUDIENCE       — does it name who this person is for?
  OUTCOME        — does it name what changes for that audience?
  PROOF          — is there a specific, checkable signal (number, company, credential)?
  SEARCHABILITY  — does it contain role/skill terms a recruiter or buyer would type?
  CLARITY        — front-loaded, readable, free of buzzword filler, within limits

Limits enforced (🟡 third-party-documented, LinkedIn does not publish a limits page):
  220 characters hard cap; the first ~60-70 characters are what survive in search
  results and invitation previews, so the load-bearing words go there.

Exit codes:
  0  SHIP     (>= 75)  — good enough to publish
  2  SHARPEN  (50-74)  — usable, but named gaps cost real visibility
  3  REWRITE  (< 50)   — start over; the findings say what is missing

Stdlib only. No network. Deterministic.
"""

import argparse
import json
import re
import sys

HARD_LIMIT = 220
FRONT_LOAD = 60          # characters that survive in search results / invite previews

# Filler that reads as self-description rather than evidence.
BUZZWORDS = [
    "guru", "ninja", "rockstar", "wizard", "evangelist", "thought leader",
    "visionary", "passionate about", "results-driven", "results driven",
    "detail-oriented", "detail oriented", "self-starter", "go-getter",
    "dynamic", "synergy", "disruptor", "innovator", "serial entrepreneur",
    "world-class", "world class", "best-in-class", "growth hacker",
    "seasoned", "proven track record", "hard worker", "team player",
]

# Words that signal an audience is being named.
AUDIENCE_MARKERS = [
    "for ", "helping", "i help", "we help", "to ", "founders", "ctos", "cto",
    "cmos", "engineers", "designers", "marketers", "recruiters", "startups",
    "smbs", "smes", "enterprises", "teams", "b2b", "b2c", "saas", "agencies",
    "nonprofits", "students", "clinicians", "operators", "pms", "product managers",
    "developers", "data teams", "hr", "sales teams", "investors",
]

# Words that signal an outcome / transformation rather than a job description.
OUTCOME_MARKERS = [
    "ship", "grow", "scale", "reduce", "cut", "increase", "double", "win",
    "hire", "raise", "launch", "fix", "unblock", "automate", "migrate",
    "build", "turn", "convert", "retain", "save", "speed", "faster",
    "without", "so they", "so you", "so that", "→", "->", "from ", "into ",
]

# Terms recruiters and buyers actually type into LinkedIn search.
SEARCH_TERMS = [
    "engineer", "developer", "architect", "manager", "director", "head of",
    "vp", "founder", "consultant", "designer", "analyst", "scientist",
    "marketer", "writer", "researcher", "advisor", "coach", "lead",
    "python", "react", "kubernetes", "aws", "gcp", "azure", "sql", "ml",
    "ai", "llm", "security", "devops", "sre", "data", "product", "ux",
    "seo", "content", "finance", "legal", "clinical", "regulatory",
    "recruiter", "sales", "customer success", "operations", "platform",
]

SAMPLE_GOOD = ("Fractional Head of Data for Series A/B SaaS | Cut BigQuery spend 62% at "
               "Zendesk scale | ex-Stripe | I make dashboards people trust")
SAMPLE_WEAK = "Senior Software Engineer | Passionate about technology | Team player"


def _find(text_low: str, needles: list) -> list:
    return [n for n in needles if n in text_low]


def _has_proof(text: str) -> list:
    """Specific checkable signals: numbers, %/$, ex-Company, named credentials."""
    signals = []
    if re.search(r"\d+\s*(%|x\b|×)", text):
        signals.append("percentage or multiple")
    if re.search(r"[$€£]\s?\d", text) or re.search(r"\d+\s?(k|m|bn|b)\b", text, re.I):
        signals.append("money or magnitude")
    if re.search(r"\bex-[A-Z][\w&.-]+", text):
        signals.append("prior company (ex-)")
    if re.search(r"\b(phd|md|mba|cpa|pmp|cissp|cfa|rn|jd)\b", text, re.I):
        signals.append("credential")
    if re.search(r"\b(author|speaker|patent|award|forbes|ycombinator|y combinator|"
                 r"techstars|open[- ]source maintainer)\b", text, re.I):
        signals.append("third-party proof")
    if re.search(r"\b\d{1,3}(,\d{3})+\b|\b\d+\s*(users|customers|clients|teams|"
                 r"engineers|downloads|subscribers)\b", text, re.I):
        signals.append("scale number")
    return signals


def score_headline(text: str) -> dict:
    raw = text.strip()
    low = raw.lower()
    findings, dims = [], {}

    # --- AUDIENCE -----------------------------------------------------------
    aud = _find(low, AUDIENCE_MARKERS)
    dims["audience"] = 20 if len(aud) >= 2 else (12 if aud else 0)
    if not aud:
        findings.append({
            "severity": "blocking", "dimension": "audience",
            "finding": "No audience named. A reader cannot tell whether this person is for them.",
            "fix": "Name the group in plain words: 'for Series A SaaS founders', 'for clinical data teams'.",
        })

    # --- OUTCOME ------------------------------------------------------------
    out = _find(low, OUTCOME_MARKERS)
    dims["outcome"] = 20 if len(out) >= 2 else (12 if out else 0)
    if not out:
        findings.append({
            "severity": "blocking", "dimension": "outcome",
            "finding": "States a role, not a result. Titles are interchangeable; outcomes are not.",
            "fix": "Add what changes because of you: 'cut onboarding from 6 weeks to 4 days'.",
        })

    # --- PROOF --------------------------------------------------------------
    proof = _has_proof(raw)
    dims["proof"] = 20 if len(proof) >= 2 else (12 if proof else 0)
    if not proof:
        findings.append({
            "severity": "major", "dimension": "proof",
            "finding": "No checkable signal. Every claim here is self-assessed.",
            "fix": "One number, one prior company, or one credential. Real, or leave it out.",
        })

    # --- SEARCHABILITY ------------------------------------------------------
    terms = _find(low, SEARCH_TERMS)
    dims["searchability"] = 20 if len(terms) >= 3 else (13 if len(terms) == 2 else
                                                        (7 if terms else 0))
    if len(terms) < 2:
        findings.append({
            "severity": "major", "dimension": "searchability",
            "finding": f"Only {len(terms)} recognizable search term(s). "
                       "LinkedIn search matches headline text; invented job titles do not rank.",
            "fix": "Keep at least one conventional role or skill term alongside the creative framing.",
        })

    # --- CLARITY ------------------------------------------------------------
    clarity = 20
    hits = _find(low, BUZZWORDS)
    if hits:
        clarity -= min(10, 4 * len(hits))
        findings.append({
            "severity": "major", "dimension": "clarity",
            "finding": f"Buzzword filler: {', '.join(hits)}. These describe an attitude, not a capability.",
            "fix": "Delete them. The space buys you a real number or a real audience.",
        })
    pipes = raw.count("|") + raw.count("•") + raw.count("·")
    if pipes > 3:
        clarity -= 5
        findings.append({
            "severity": "minor", "dimension": "clarity",
            "finding": f"{pipes} separators. Past three, it reads as a list of keywords rather than a claim.",
            "fix": "Keep three segments: who you help / what changes / one proof.",
        })
    emoji = len(re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", raw))
    if emoji > 2:
        clarity -= 4
        findings.append({
            "severity": "minor", "dimension": "clarity",
            "finding": f"{emoji} emoji. They survive truncation and crowd out words that carry meaning.",
            "fix": "At most one, and only if it separates segments.",
        })
    caps_words = [w for w in raw.split() if len(w) > 3 and w.isupper()]
    if len(caps_words) > 1:
        clarity -= 3
        findings.append({
            "severity": "minor", "dimension": "clarity",
            "finding": "Multiple ALL-CAPS words read as shouting and hurt scannability.",
            "fix": "Sentence case. Emphasis comes from specificity, not capitals.",
        })
    dims["clarity"] = max(0, clarity)

    # --- Length + front-loading (structural, reported alongside the score) ---
    length = len(raw)
    front = raw[:FRONT_LOAD]
    over = max(0, length - HARD_LIMIT)
    if over:
        findings.append({
            "severity": "blocking", "dimension": "length",
            "finding": f"{length} characters — {over} over the 220-character cap. LinkedIn will refuse it.",
            "fix": f"Cut {over} characters. Start with the segment carrying the least proof.",
        })
    front_has_proof = bool(_has_proof(front)) or bool(_find(front.lower(), AUDIENCE_MARKERS))
    if not front_has_proof:
        findings.append({
            "severity": "major", "dimension": "front-load",
            "finding": f"The first {FRONT_LOAD} characters — the part that survives in search "
                       f"results and invitation previews — carry no audience and no proof: "
                       f"\"{front}\"",
            "fix": "Move the strongest segment first. Everything after it is a bonus, not a plan.",
        })

    total = sum(dims.values())
    if over:                       # a headline LinkedIn will not accept cannot ship
        total = min(total, 49)
    verdict, code = (("SHIP", 0) if total >= 75 else
                     ("SHARPEN", 2) if total >= 50 else ("REWRITE", 3))

    return {
        "headline": raw,
        "score": total,
        "verdict": verdict,
        "exit_code": code,
        "dimensions": dims,
        "length": {"chars": length, "limit": HARD_LIMIT, "over_by": over,
                   "front_loaded_preview": front},
        "signals": {"audience": aud, "outcome": out, "proof": proof, "search_terms": terms},
        "findings": sorted(findings,
                           key=lambda f: {"blocking": 0, "major": 1, "minor": 2}[f["severity"]]),
        "note": ("Character limits are documented by third parties, not by an official LinkedIn "
                 "limits page — treat 220 as reliable and the ~60-70 front-load window as an "
                 "estimate that shifts with UI changes."),
    }


def render_human(r: dict) -> str:
    lines = [
        f"Headline score: {r['score']}/100 — {r['verdict']}",
        "=" * 52,
        f"\"{r['headline']}\"",
        f"{r['length']['chars']}/{r['length']['limit']} chars"
        + (f"  (OVER BY {r['length']['over_by']})" if r["length"]["over_by"] else ""),
        f"Search/invite preview: \"{r['length']['front_loaded_preview']}\"",
        "",
        "Dimensions (20 each):",
    ]
    for k, v in r["dimensions"].items():
        bar = "#" * (v // 2) + "." * (10 - v // 2)
        lines.append(f"  {k:<14} {v:>2}/20  [{bar}]")
    if r["findings"]:
        lines.append("\nFindings:")
        for f in r["findings"]:
            lines.append(f"  [{f['severity'].upper():<8}] {f['dimension']}: {f['finding']}")
            lines.append(f"             fix → {f['fix']}")
    else:
        lines.append("\nNo findings. Ship it.")
    lines.append(f"\n{r['note']}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Score a LinkedIn headline 0-100 (SHIP=0 / SHARPEN=2 / REWRITE=3).")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--headline", help="The headline text to score.")
    src.add_argument("--input", help="Read the headline from a file ('-' for stdin).")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true",
                    help="Score a built-in strong sample headline.")
    ap.add_argument("--sample-weak", action="store_true",
                    help="Score a built-in weak sample headline (shows the failure modes).")
    args = ap.parse_args()

    if args.sample:
        text = SAMPLE_GOOD
    elif args.sample_weak:
        text = SAMPLE_WEAK
    elif args.headline:
        text = args.headline
    elif args.input:
        text = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    else:
        ap.error("one of --headline, --input, --sample, or --sample-weak is required")

    result = score_headline(text)
    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
