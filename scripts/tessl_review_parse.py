#!/usr/bin/env python3
"""Parse `tessl review run --json` output into one pipe-separated line for CI.

Used by .github/workflows/skill-quality-review.yml. Prints:

    STATUS|SCORE|DESCRIPTION|CONTENT|SUGGESTIONS_JSON

STATUS is OK when an overall score was found, ERROR otherwise. Scores are
0-100 integers, or "-" when that component is absent. SUGGESTIONS_JSON is a
JSON list of strings.

Tessl does not document the JSON schema of `tessl review run --json`, and the
CLI auto-updates, so the parser looks up scores by key name instead of fixed
paths. It accepts the old `tessl skill review` shape (review.reviewScore,
descriptionJudge.normalizedScore, contentJudge.normalizedScore) as well. When
no overall score is found it reports ERROR and lists the keys it did see on
stderr, so the next CI log shows what changed. It never invents a 0 score.

Usage:
    tessl review run <dir> --workspace <ws> --json | python3 scripts/tessl_review_parse.py
    python3 scripts/tessl_review_parse.py --file output.txt
"""

import argparse
import json
import sys

OVERALL_KEYS = ("reviewscore", "overallscore", "totalscore", "finalscore", "score")
SECTION_SCORE_KEYS = ("normalizedscore", "score", "percentage", "value")


def extract_json(text):
    """Return the first JSON object in text, skipping warnings printed before it."""
    decoder = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch == "{":
            try:
                obj, _ = decoder.raw_decode(text[i:])
            except ValueError:
                continue
            if isinstance(obj, dict):
                return obj
    return None


def as_percent(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if 0 <= value <= 1 and isinstance(value, float):
        value = value * 100
    if 0 <= value <= 100:
        return int(round(value))
    return None


def walk(node, path=()):
    """Yield (path, key, value) for every key in nested dicts and lists."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield path, key, value
            yield from walk(value, path + (str(key).lower(),))
    elif isinstance(node, list):
        for item in node:
            yield from walk(item, path)


def find_overall(data):
    # Shallowest match wins, in the priority order of OVERALL_KEYS.
    best = None
    for path, key, value in walk(data):
        k = str(key).lower()
        if k not in OVERALL_KEYS:
            continue
        # A bare "score" inside a description/content section is not overall.
        if k == "score" and any(p for p in path if "description" in p or "content" in p or "validation" in p):
            continue
        pct = as_percent(value)
        if pct is None:
            continue
        rank = (len(path), OVERALL_KEYS.index(k))
        if best is None or rank < best[0]:
            best = (rank, pct)
    return None if best is None else best[1]


def find_section(data, word):
    for path, key, value in walk(data):
        k = str(key).lower()
        in_section = any(word in p for p in path)
        if word in k and isinstance(value, dict):
            for sub in SECTION_SCORE_KEYS:
                for sk, sv in value.items():
                    if str(sk).lower() == sub and as_percent(sv) is not None:
                        return as_percent(sv)
        if word in k and k.endswith("score") and as_percent(value) is not None:
            return as_percent(value)
        if in_section and k in SECTION_SCORE_KEYS and as_percent(value) is not None:
            return as_percent(value)
    return None


def find_suggestions(data):
    out = []
    for path, key, value in walk(data):
        if str(key).lower() not in ("suggestions", "recommendations"):
            continue
        if not isinstance(value, list):
            continue
        label = "content" if any("content" in p for p in path) else (
            "description" if any("description" in p for p in path) else "")
        for item in value:
            if isinstance(item, dict):
                item = item.get("text") or item.get("message") or item.get("suggestion") or json.dumps(item)
            text = " ".join(str(item).split())
            out.append(f"[{label}] {text}" if label else text)
    return out


def parse(text):
    data = extract_json(text)
    if data is None:
        print("tessl_review_parse: no JSON object in CLI output", file=sys.stderr)
        return "ERROR|-|-|-|[]"
    overall = find_overall(data)
    if overall is None:
        keys = sorted({str(k) for _, k, _ in walk(data)})[:60]
        print(f"tessl_review_parse: no overall score; keys seen: {', '.join(keys)}", file=sys.stderr)
        return "ERROR|-|-|-|[]"
    desc = find_section(data, "description")
    content = find_section(data, "content")
    fmt = lambda v: "-" if v is None else str(v)
    suggestions = json.dumps(find_suggestions(data)).replace("|", "/")
    return f"OK|{overall}|{fmt(desc)}|{fmt(content)}|{suggestions}"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--file", help="read CLI output from this file instead of stdin")
    args = ap.parse_args()
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    else:
        text = sys.stdin.read()
    print(parse(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
