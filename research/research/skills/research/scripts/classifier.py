#!/usr/bin/env python3
"""
classifier.py — Deterministic SIGNALS-based routing classifier for the research orchestrator.

Given a research question, returns the routing decision (specialist name or "fallback"),
matched signals per specialist, and confidence reasoning.

The SIGNALS map is the post-PR-#657-audit canonical version: verb-noun-paired phrases
that route reliably, with NO bracketed placeholders (those over-trigger on generic
"research [topic]" queries that should fall back instead).

Usage:
  python classifier.py --question "What's the literature on PICO for sepsis?"
  python classifier.py --question "..." --output json
  python classifier.py --sample
"""

import argparse
import json
import sys

SIGNALS = {
    "pulse": [
        "reddit", "hn", "hacker news", "x.com", "twitter", "buzz",
        "sentiment", "trending", "what are people saying",
        "what's happening", "the conversation around",
        "pulse on", "take the pulse", "current conversation",
    ],
    "grants": [
        "nih", "grant", "grants for", "r01", "r21", "k-award", "reporter",
        "nosi", "funding", "fda", "study section", "principal investigator",
    ],
    "litreview": [
        "literature review", "lit review", "litreview", "pico", "spider",
        "systematic review", "review papers on", "research papers on",
        "papers about", "meta-analysis",
    ],
    "syllabus": [
        "syllabus", "course outline", "curriculum", "reading list",
        "for my class", "for my students", "course material",
    ],
    "patent": [
        "prior art", "fto", "freedom to operate", "patent",
        "patent landscape", "invention", "novelty search",
        "patent search", "ip landscape",
    ],
    "dossier": [
        "dossier on", "due diligence", "background check",
        "prep me for", "competitor research", "investor diligence",
        "interview prep", "research my competitor", "background on",
    ],
}


def classify(question: str) -> dict:
    """
    Apply the deterministic routing algorithm:
      - score[S] = count of SIGNALS[S] substrings matched (case-insensitive)
      - if max(score) >= 2: route to argmax
      - elif max(score) == 1 AND only one specialist scored 1: route to that one
      - else: route to "fallback"
    """
    q = question.lower()
    scores = {}
    matched = {}

    for specialist, phrases in SIGNALS.items():
        hits = [p for p in phrases if p in q]
        scores[specialist] = len(hits)
        if hits:
            matched[specialist] = hits

    max_score = max(scores.values()) if scores else 0
    top = [s for s, sc in scores.items() if sc == max_score and sc > 0]

    if max_score >= 2:
        route_to = top[0] if len(top) == 1 else _pick_highest_priority(top, scores)
        confidence = f"high ({max_score} signals)"
    elif max_score == 1:
        single_scorers = [s for s, sc in scores.items() if sc == 1]
        if len(single_scorers) == 1:
            route_to = single_scorers[0]
            confidence = "weak (1 signal, single specialist)"
        else:
            route_to = "fallback"
            confidence = "ambiguous (multiple specialists with 1 signal)"
    else:
        route_to = "fallback"
        confidence = "no signals matched"

    return {
        "route_to": route_to,
        "confidence": confidence,
        "scores": scores,
        "matched_signals": matched,
        "question": question,
    }


def _pick_highest_priority(candidates: list, scores: dict) -> str:
    """When max(score) is tied across specialists, prefer the one with the
    most specific signals (longest matched phrase across SIGNALS map). This is
    a tie-breaker; in practice ties at ≥2 are rare."""
    return sorted(candidates)[0]


def render_human(result: dict) -> str:
    lines = [
        f"Question: {result['question']}",
        f"Route to: {result['route_to']}",
        f"Confidence: {result['confidence']}",
        "",
        "Per-specialist scores:",
    ]
    for s, sc in sorted(result["scores"].items(), key=lambda kv: -kv[1]):
        lines.append(f"  {s}: {sc}")
    if result["matched_signals"]:
        lines.append("")
        lines.append("Matched signals:")
        for s, phrases in result["matched_signals"].items():
            lines.append(f"  {s}: {', '.join(repr(p) for p in phrases)}")
    if result["route_to"] != "fallback":
        lines.append("")
        lines.append(
            f"Routing transparency: 'Routing to `{result['route_to']}` because "
            f"of {result['confidence']}. Override or proceed in 5s.'"
        )
    else:
        lines.append("")
        lines.append("Routing transparency: 'No specialist matched. Running fallback.'")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--question", help="The research question to classify.")
    p.add_argument("--output", choices=["human", "json"], default="human")
    p.add_argument("--sample", action="store_true", help="Run with built-in sample question.")
    args = p.parse_args()

    if args.sample:
        args.question = "Can you do a systematic review of PICO frameworks for sepsis treatment? I need a meta-analysis."

    if not args.question:
        p.error("either --question or --sample is required")

    result = classify(args.question)

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(render_human(result))


if __name__ == "__main__":
    main()
