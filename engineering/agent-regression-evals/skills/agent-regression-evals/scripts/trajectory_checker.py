#!/usr/bin/env python3
"""Check an agent's tool-call trajectory against what the case expected.

A final answer can be right for the wrong reason: the agent guessed, skipped
the lookup it was supposed to do, or called a destructive tool on the way. An
outcome-only grader passes all three. This checker grades the path.

Per case, the spec states:

  expected        ordered list of {"tool": name, "args": {...}} steps
  match           strict | unordered | subset | superset
                    strict     same tools, same order, nothing extra
                    unordered  same multiset of tools, any order
                    subset     every actual call appears in expected (no extras)
                    superset   every expected call appears in actual (extras ok)
  args_match      exact | subset | ignore   (default subset: listed keys must
                  match, extra keys in the actual call are allowed)
  forbidden       tool names that must never appear (checked in every mode)
  max_calls       optional ceiling on total calls (catches loops)

`superset` is the honest default for most agents: it requires the steps that
matter and tolerates harmless exploration. Use `strict` only where order is the
requirement (e.g. "read before write").

Results file: JSONL, one trial per line:
  {"case_id": "...", "trial": 1, "trajectory": [{"tool": "...", "args": {...}}]}

Deterministic, stdlib only, no network, no LLM calls.

Exit codes:
    0  every trial matches its expected trajectory
    2  at least one trial deviates (findings listed)
    3  invalid input
    4  a forbidden tool was called (blocking, regardless of match mode)
"""

import argparse
import json
import sys
from collections import Counter

MATCH_MODES = {"strict", "unordered", "subset", "superset"}
ARGS_MODES = {"exact", "subset", "ignore"}

SAMPLE_SPEC = {
    "refund-lookup": {
        "expected": [
            {"tool": "get_order", "args": {"order_id": "A-1001"}},
            {"tool": "get_refund_policy", "args": {}},
            {"tool": "issue_refund", "args": {"order_id": "A-1001"}},
        ],
        "match": "strict",
        "args_match": "subset",
        "forbidden": ["delete_order"],
        "max_calls": 6,
    },
    "faq-shipping": {
        "expected": [{"tool": "search_kb", "args": {}}],
        "match": "superset",
        "args_match": "ignore",
        "forbidden": ["issue_refund"],
    },
}

SAMPLE_RESULTS = [
    {"case_id": "refund-lookup", "trial": 1, "trajectory": [
        {"tool": "get_order", "args": {"order_id": "A-1001"}},
        {"tool": "get_refund_policy", "args": {}},
        {"tool": "issue_refund", "args": {"order_id": "A-1001", "reason": "late"}}]},
    {"case_id": "refund-lookup", "trial": 2, "trajectory": [
        {"tool": "get_order", "args": {"order_id": "A-1001"}},
        {"tool": "issue_refund", "args": {"order_id": "A-1001"}}]},
    {"case_id": "faq-shipping", "trial": 1, "trajectory": [
        {"tool": "search_kb", "args": {"q": "shipping times"}},
        {"tool": "search_kb", "args": {"q": "express shipping"}}]},
    {"case_id": "faq-shipping", "trial": 2, "trajectory": [
        {"tool": "search_kb", "args": {"q": "shipping"}},
        {"tool": "issue_refund", "args": {"order_id": "A-2002"}}]},
]


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def load_jsonl(path):
    rows = []
    try:
        with open(path, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    _fail(f"{path}:{n}: not valid JSON ({exc.msg})")
    except OSError as exc:
        _fail(f"cannot read {path}: {exc.strerror}")
    return rows


def load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except OSError as exc:
        _fail(f"cannot read {path}: {exc.strerror}")
    except json.JSONDecodeError as exc:
        _fail(f"{path}: not valid JSON ({exc.msg})")


def args_ok(expected_args, actual_args, mode):
    if mode == "ignore":
        return True
    expected_args = expected_args or {}
    actual_args = actual_args or {}
    if mode == "exact":
        return expected_args == actual_args
    return all(k in actual_args and actual_args[k] == v for k, v in expected_args.items())


def _consume(expected, actual, args_mode):
    """Greedy multiset match. Returns (unmatched_expected, unmatched_actual)."""
    remaining = list(actual)
    missing = []
    for step in expected:
        hit = next((i for i, a in enumerate(remaining)
                    if a.get("tool") == step.get("tool")
                    and args_ok(step.get("args"), a.get("args"), args_mode)), None)
        if hit is None:
            missing.append(step)
        else:
            remaining.pop(hit)
    return missing, remaining


def check_trial(case, trajectory):
    mode = case.get("match", "superset")
    args_mode = case.get("args_match", "subset")
    expected = case.get("expected", [])
    findings = []

    called = [c.get("tool") for c in trajectory]
    forbidden_hits = sorted(set(called) & set(case.get("forbidden", [])))
    if forbidden_hits:
        findings.append({"kind": "FORBIDDEN_TOOL", "detail": f"called {', '.join(forbidden_hits)}"})

    max_calls = case.get("max_calls")
    if max_calls is not None and len(trajectory) > max_calls:
        findings.append({"kind": "TOO_MANY_CALLS", "detail": f"{len(trajectory)} calls > max {max_calls}"})

    if mode == "strict":
        if len(trajectory) != len(expected):
            findings.append({"kind": "LENGTH", "detail": f"{len(trajectory)} calls, expected {len(expected)}"})
        for i, (exp, act) in enumerate(zip(expected, trajectory)):
            if exp.get("tool") != act.get("tool"):
                findings.append({"kind": "ORDER", "detail": f"step {i + 1}: got {act.get('tool')}, expected {exp.get('tool')}"})
                break
            if not args_ok(exp.get("args"), act.get("args"), args_mode):
                findings.append({"kind": "ARGS", "detail": f"step {i + 1} {exp.get('tool')}: args {act.get('args')} do not match {exp.get('args')}"})
    else:
        missing, extra = _consume(expected, trajectory, args_mode)
        if mode in ("unordered", "superset") and missing:
            findings.append({"kind": "MISSING", "detail": "missing " + ", ".join(s.get("tool", "?") for s in missing)})
        if mode in ("unordered", "subset") and extra:
            findings.append({"kind": "EXTRA", "detail": "unexpected " + ", ".join(a.get("tool", "?") for a in extra)})
    return findings


def validate_spec(spec):
    if not isinstance(spec, dict) or not spec:
        _fail("spec must be a non-empty object keyed by case_id")
    for cid, case in spec.items():
        if case.get("match", "superset") not in MATCH_MODES:
            _fail(f"case {cid}: match must be one of {sorted(MATCH_MODES)}")
        if case.get("args_match", "subset") not in ARGS_MODES:
            _fail(f"case {cid}: args_match must be one of {sorted(ARGS_MODES)}")
        if not isinstance(case.get("expected", []), list):
            _fail(f"case {cid}: expected must be a list")


def run(spec, results):
    validate_spec(spec)
    trials, unknown = [], set()
    for row in results:
        cid = row.get("case_id")
        if cid not in spec:
            unknown.add(str(cid))
            continue
        traj = row.get("trajectory")
        if not isinstance(traj, list):
            _fail(f"case {cid} trial {row.get('trial')}: trajectory must be a list")
        findings = check_trial(spec[cid], traj)
        trials.append({"case_id": cid, "trial": row.get("trial"), "ok": not findings, "findings": findings})

    not_run = sorted(set(spec) - {t["case_id"] for t in trials})
    forbidden = any(f["kind"] == "FORBIDDEN_TOOL" for t in trials for f in t["findings"])
    deviations = sum(1 for t in trials if not t["ok"])
    if forbidden:
        verdict, code = "FORBIDDEN_TOOL_CALLED", 4
    elif deviations or not_run:
        verdict, code = "DEVIATIONS", 2
    else:
        verdict, code = "ALL_MATCH", 0
    kinds = Counter(f["kind"] for t in trials for f in t["findings"])
    return {
        "verdict": verdict,
        "trials_checked": len(trials),
        "trials_deviating": deviations,
        "finding_counts": dict(kinds),
        "cases_not_run": not_run,
        "unknown_case_ids": sorted(unknown),
        "trials": trials,
    }, code


def render(report):
    lines = [f"Trajectory check: {report['verdict']}",
             f"  trials checked: {report['trials_checked']}, deviating: {report['trials_deviating']}"]
    if report["finding_counts"]:
        lines.append("  findings: " + ", ".join(f"{k}={v}" for k, v in sorted(report["finding_counts"].items())))
    for t in report["trials"]:
        if t["ok"]:
            continue
        lines.append(f"  - {t['case_id']} trial {t['trial']}:")
        for f in t["findings"]:
            lines.append(f"      {f['kind']}: {f['detail']}")
    if report["cases_not_run"]:
        lines.append("  cases in spec with no trials: " + ", ".join(report["cases_not_run"]))
    if report["unknown_case_ids"]:
        lines.append("  results for cases not in spec (ignored): " + ", ".join(report["unknown_case_ids"]))
    if report["verdict"] == "FORBIDDEN_TOOL_CALLED":
        lines.append("  BLOCKING: a forbidden tool was called. A correct final answer does not excuse it.")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Grade agent tool-call trajectories against expected paths (strict/unordered/subset/superset).")
    p.add_argument("--spec", help="JSON object keyed by case_id with expected/match/args_match/forbidden/max_calls")
    p.add_argument("--results", help="JSONL of trials: {case_id, trial, trajectory:[{tool,args}]}")
    p.add_argument("--sample", action="store_true", help="run on the embedded sample spec and results")
    p.add_argument("--print-sample-spec", action="store_true", help="print the sample spec JSON and exit")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()

    if a.print_sample_spec:
        print(json.dumps(SAMPLE_SPEC, indent=2))
        return 0
    if a.sample:
        spec, results = SAMPLE_SPEC, SAMPLE_RESULTS
    elif a.spec and a.results:
        spec, results = load_json(a.spec), load_jsonl(a.results)
    else:
        p.error("give --spec and --results, or --sample")
    report, code = run(spec, results)
    print(json.dumps(report, indent=2) if a.output == "json" else render(report))
    return code


if __name__ == "__main__":
    sys.exit(main())
