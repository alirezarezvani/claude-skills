#!/usr/bin/env python3
"""Ratchet a design-qa report against a baseline: fail on what is new, not on what was there.

On an existing product the first finish_lint / state_matrix_checker / rendered_audit run
is usually red. Blocking every PR on that history teaches people to switch the gate off;
waving it through teaches nothing. A baseline turns the report into a ratchet: a PR may
not add a finding, findings that disappear are counted as fixed, and the baseline only
shrinks: --update writes it when nothing is new, and refuses to grow it unless
--allow-growth is given, which is a recorded waiver (the verdict still names the new
findings), not a way to make CI pass. Identical findings are counted, so a second copy
of an existing finding is new.

Input: the --output json report of any of the three design-qa scripts. The kind is
detected from its fields. Findings are matched by a key that survives unrelated edits:
  finish_lint           code + file + snippet   (line numbers shift, so they are ignored)
  state_matrix_checker  code + surface + state
  rendered_audit        code + example selector  (one key per example in each group)

Verdicts
  NEW_BLOCKING  a BLOCKER or HIGH finding not in the baseline           exit 4
  NEW_WARN      only WARN findings are new                              exit 2
  CLEAN         nothing new (fixed findings are reported)               exit 0
  BAD_INPUT     unreadable report, different kinds, unknown kind        exit 3

Deterministic, stdlib only, no network.
"""
import argparse
import json
import sys

EXIT = {"CLEAN": 0, "NEW_WARN": 2, "BAD_INPUT": 3, "NEW_BLOCKING": 4}
BLOCKING = {"BLOCKER", "HIGH"}

SAMPLE_BASE = {"verdict": "BLOCKED", "files_scanned": 2, "findings": [
    {"file": "src/Pricing.tsx", "line": 10, "code": "PLACEHOLDER_COPY", "severity": "BLOCKER",
     "message": "Unfinished copy on screen: 'Lorem ipsum'.", "snippet": "<p>Lorem ipsum dolor sit amet</p>"},
    {"file": "src/Nav.tsx", "line": 4, "code": "DEAD_LINK", "severity": "HIGH",
     "message": "Link goes nowhere (href=\"#\").", "snippet": "<a href=\"#\">Docs</a>"},
    {"file": "src/theme.css", "line": 1, "code": "TOKEN_DRIFT", "severity": "WARN",
     "message": "19 distinct raw colors.", "snippet": ""}]}
SAMPLE_HEAD = {"verdict": "BLOCKED", "files_scanned": 3, "findings": [
    {"file": "src/Pricing.tsx", "line": 14, "code": "PLACEHOLDER_COPY", "severity": "BLOCKER",
     "message": "Unfinished copy on screen: 'Lorem ipsum'.", "snippet": "<p>Lorem ipsum dolor sit amet</p>"},
    {"file": "src/theme.css", "line": 1, "code": "TOKEN_DRIFT", "severity": "WARN",
     "message": "19 distinct raw colors.", "snippet": ""},
    {"file": "src/Checkout.tsx", "line": 22, "code": "INERT_HANDLER", "severity": "BLOCKER",
     "message": "Control does nothing (empty arrow function).",
     "snippet": "<button onClick={() => {}}>Pay now</button>"}]}


def kind_of(report):
    if not isinstance(report, dict):
        return None
    if "groups" in report and "viewport" in report:
        return "rendered_audit"
    if "files_scanned" in report:
        return "finish_lint"
    if "surfaces" in report and "coverage" in report:
        return "state_matrix_checker"
    return None


def keyed(report, kind):
    """Map stable key -> [severity, human label, count] for every finding in the report.

    Keys repeat when one file holds two identical findings, so occurrences are counted:
    a second identical dead link is a new finding, not a duplicate of the first."""
    out = {}

    def put(key, sev, label):
        if key in out:
            out[key][2] += 1
        else:
            out[key] = [sev, label, 1]
    if kind == "rendered_audit":
        for g in report.get("groups", []):
            for ex in g.get("examples") or [g.get("pattern", "")]:
                key = f"{g['code']}|{ex}"
                put(key, g.get("severity", "WARN"), f"{g['code']} on {ex}: {g.get('message', '')}")
    elif kind == "finish_lint":
        for f in report.get("findings", []):
            key = f"{f['code']}|{f.get('file', '')}|{(f.get('snippet') or '').strip()}"
            put(key, f.get("severity", "WARN"),
                f"{f['code']} in {f.get('file', '')}:{f.get('line', '?')}: {f.get('message', '')}")
    else:
        for f in report.get("findings", []):
            key = f"{f['code']}|{f.get('surface', '')}|{f.get('state', '')}"
            put(key, f.get("severity", "WARN"),
                f"{f['code']} for {f.get('surface', '')} / {f.get('state', '')}: {f.get('message', '')}")
    return out


def compare(base, head):
    kb, kh = kind_of(base), kind_of(head)
    if kb is None or kh is None:
        raise ValueError("not a design-qa JSON report (run the script with --output json)")
    if kb != kh:
        raise ValueError(f"baseline is a {kb} report but the current one is {kh}")
    b, h = keyed(base, kb), keyed(head, kh)
    new, fixed = [], []
    for k in sorted(set(b) | set(h)):
        nb, nh = (b[k][2] if k in b else 0), (h[k][2] if k in h else 0)
        if nh > nb:
            new.append({"key": k, "severity": h[k][0], "finding": h[k][1], "added": nh - nb})
        elif nb > nh:
            fixed.append({"key": k, "severity": b[k][0], "finding": b[k][1], "removed": nb - nh})
    if any(n["severity"] in BLOCKING for n in new):
        verdict = "NEW_BLOCKING"
    elif new:
        verdict = "NEW_WARN"
    else:
        verdict = "CLEAN"
    return {"verdict": verdict, "kind": kb, "baseline_findings": sum(v[2] for v in b.values()), "current_findings": sum(v[2] for v in h.values()),
            "unchanged": sum(min(b[k][2], h[k][2]) for k in set(b) & set(h)), "new": new, "fixed": fixed}


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def render(res):
    lines = [f"design-qa baseline ({res['kind']}): {res['verdict']}",
             f"  baseline {res['baseline_findings']} · current {res['current_findings']} · "
             f"unchanged {res['unchanged']} · new {len(res['new'])} · fixed {len(res['fixed'])}"]
    for n in res["new"]:
        lines.append(f"  NEW   [{n['severity']}] {n['finding']}" + (f" (x{n['added']})" if n["added"] > 1 else ""))
    for f in res["fixed"]:
        lines.append(f"  FIXED [{f['severity']}] {f['finding']}")
    if res["verdict"] == "NEW_BLOCKING":
        lines.append("  This change adds blocking findings. Fix them, or waive them with an owner and a reason; "
                     "do not refresh the baseline to make the gate pass.")
    elif res["fixed"] and not res["new"]:
        lines.append("  Findings were fixed: shrink the baseline with --update so they cannot come back.")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog="Exit codes: 0 nothing new, 2 new warnings only, 3 bad input, 4 new blocking findings.")
    ap.add_argument("--baseline", help="baseline report JSON (a missing file is treated as an empty baseline with --update)")
    ap.add_argument("--current", help="current report JSON from finish_lint, state_matrix_checker or rendered_audit")
    ap.add_argument("--update", action="store_true", help="write the current report as the new baseline when it adds nothing")
    ap.add_argument("--allow-growth", action="store_true",
                    help="with --update, write a baseline that grows: a deliberate waiver for the first run or accepted "
                         "debt, never a CI default. The verdict still reports the new findings.")
    ap.add_argument("--sample", action="store_true", help="run on a built-in example")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        if a.sample:
            base, head = SAMPLE_BASE, SAMPLE_HEAD
        else:
            if not a.current:
                raise ValueError("--current is required (or use --sample)")
            head = load(a.current)
            if not a.baseline:
                raise ValueError("--baseline is required")
            try:
                base = load(a.baseline)
            except FileNotFoundError:
                if not a.update:
                    raise ValueError(f"baseline {a.baseline} not found; create it with --update --allow-growth")
                base = dict(head, findings=[], groups=[])
        res = compare(base, head)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        msg = {"verdict": "BAD_INPUT", "error": str(exc)}
        print(json.dumps(msg) if a.output == "json" else f"BAD_INPUT: {exc}")
        return EXIT["BAD_INPUT"]
    if a.update and not a.sample:
        if res["new"] and not a.allow_growth:
            res["update"] = "refused: the current report adds findings; fix them or pass --allow-growth"
        else:
            with open(a.baseline, "w", encoding="utf-8") as fh:
                json.dump(head, fh, indent=2)
            res["update"] = f"baseline written to {a.baseline}" + (
                f" (grew by {sum(n['added'] for n in res['new'])} finding(s), waived)" if res["new"] else "")
    print(json.dumps(res, indent=2) if a.output == "json" else render(res) + (f"\n  {res['update']}" if "update" in res else ""))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
