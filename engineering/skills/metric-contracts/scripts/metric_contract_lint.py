#!/usr/bin/env python3
"""Lint metric definitions before anyone builds a dashboard on them.

Reads dbt's target/semantic_manifest.json (legacy or 1.12 spec) or a plain
metric contract file (JSON, or YAML with PyYAML). Pass several files to catch
the same metric defined twice in different places.

Rules                                                               Severity
  MC01 NO_OWNER             no owner (meta.owner / config.meta.owner)   ERROR
  MC02 NO_DESCRIPTION       no description                              WARN
  MC03 UNRESOLVED           input metric, measure or model not found    ERROR
  MC04 DUPLICATE            two names, identical computation (synonym)  WARN
  MC05 AVERAGE_OF_RATIO     agg: average over an expression with "/"    ERROR
  MC06 COUNT_NOT_DISTINCT   agg: count over a foreign key or a
                            people/accounts metric (counts rows)        WARN
  MC07 SEMI_ADDITIVE_SUM    balance/MRR/inventory-like sum with no
                            non_additive_dimension (sums over time)     WARN
  MC08 UNDECLARED_INPUT     derived expr names something not declared   ERROR
  MC09 NO_VERSION           no version (ERROR with --require-version)   INFO
  MC10 CONFLICT             same name, different computation, 2 files   ERROR
  MC11 BAD_VALUE            unknown metric type or aggregation          ERROR
  MC12 CYCLE                metric depends on itself                    ERROR
  MC13 NO_TIME_DIMENSION    simple metric with no time dimension        WARN

Exit codes: 0 no errors (and no warnings with --strict), 2 findings, 3 bad input.
Deterministic, stdlib only, no network.
"""
import argparse
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metric_common import AGGS, TYPES, VERIFIED, BadInput, asset, emit, load_many, refs, signature  # noqa: E402

SEMI_ADDITIVE = re.compile(r"(balance|\bmrr\b|\barr\b|inventory|stock_level|on_hand|headcount|outstanding|"
                           r"backlog|snapshot|open_(tickets|orders|positions)|seats_active)", re.I)
PEOPLE = re.compile(r"(^|_)(customer|user|account|visitor|member|subscriber|buyer|seller|patient)s?$", re.I)
QUOTED = re.compile(r"'(?:[^']|'')*'|\"[^\"]*\"|--[^\n]*|/\*.*?\*/", re.S)
SQL_WORDS = {"and", "or", "not", "case", "when", "then", "else", "end", "null", "is", "in", "as",
             "true", "false", "between", "like", "nullif", "coalesce", "cast", "float", "int", "integer",
             "numeric", "decimal", "double", "precision", "over", "partition", "by", "distinct"}


def lint(metrics, models, measures, kinds, require_version):
    findings = []

    def add(code, sev, metric, msg):
        findings.append({"code": code, "severity": sev, "metric": metric, "message": msg})

    by_name = defaultdict(list)
    for m in metrics:
        by_name[m["name"]].append(m)
    # MC10: same name defined twice with different numbers
    for name, recs in by_name.items():
        if len({signature(r) for r in recs}) > 1:
            add("MC10", "ERROR", name, "defined differently in " + ", ".join(sorted({os.path.basename(r["source"]) for r in recs}))
                + "; one business term needs one definition")
    uniq = {n: recs[0] for n, recs in by_name.items()}

    sigs = defaultdict(list)
    for name, m in uniq.items():
        t = m.get("type")
        if t not in TYPES:
            add("MC11", "ERROR", name, f"unknown metric type {t!r}; expected one of {sorted(TYPES)}")
        if t == "simple":
            if m.get("agg") is None and m.get("measure"):
                add("MC03", "ERROR", name, f"measure {m['measure']!r} not found on any semantic model")
            elif m.get("agg") not in AGGS:
                add("MC11", "ERROR", name, f"unknown aggregation {m.get('agg')!r}")
            if m.get("semantic_model") and models and m["semantic_model"] not in models:
                add("MC03", "ERROR", name, f"semantic model {m['semantic_model']!r} not found")
            if not m.get("time_dimension"):
                add("MC13", "WARN", name, "no time dimension: trends and period totals are undefined")
            sigs[signature(m)].append(name)
        if not m.get("owner"):
            add("MC01", "ERROR", name, "no owner; nobody can approve a change or answer for the number")
        if not (m.get("description") or "").strip():
            add("MC02", "WARN", name, "no description; say what is counted, what is excluded and the unit")
        if m.get("version") is None:
            add("MC09", "ERROR" if require_version else "INFO", name,
                "no version; a breaking change cannot be told apart from a fix")
        for r in refs(m):
            if r not in uniq:
                add("MC03", "ERROR", name, f"references metric {r!r}, which is not defined")
        agg, expr = m.get("agg"), str(m.get("expr") or "")
        bare = QUOTED.sub(" ", expr)  # string literals and comments are not code
        if agg == "average" and "/" in bare:
            add("MC05", "ERROR", name, f"averages a ratio ({expr}); small rows weigh as much as big ones. "
                "Define a ratio metric of two sums instead")
        if agg == "count":
            ent = models.get(m.get("semantic_model"), {}).get("entities", {})
            if ent.get(expr) == "foreign":
                add("MC06", "WARN", name, f"count of foreign key {expr} counts rows, not distinct entities; "
                    "use count_distinct if you mean unique ones")
            elif PEOPLE.search(name) and "_per_" not in name and ent.get(expr) != "primary":
                add("MC06", "WARN", name, f"'{name}' sounds like unique entities but agg is count over {expr}; "
                    "use count_distinct or rename it")
        if agg == "sum" and not m.get("non_additive") and (SEMI_ADDITIVE.search(name) or SEMI_ADDITIVE.search(expr)):
            add("MC07", "WARN", name, "looks like a snapshot quantity (balance, MRR, inventory); summing it over "
                "days multiplies it. Add non_additive_dimension on the snapshot date")
        if m.get("type") == "derived" and expr:
            declared = {i["name"] for i in m["inputs"]} | {i["alias"] for i in m["inputs"] if i.get("alias")}
            used = {t for t in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\b(?!\s*\()", bare)
                    if t.lower() not in SQL_WORDS}  # tokens taken from bare, below
            for u in sorted(used - declared):
                add("MC08", "ERROR", name, f"expr uses {u!r}, which is not a declared input or alias")
    # MC04: same computation, two names
    for names in sigs.values():
        if len(names) > 1:
            add("MC04", "WARN", ", ".join(sorted(names)), "identical computation under different names; "
                "keep one and make the others aliases, or the two will drift apart")
    # MC12: cycles
    graph = {n: [r for r in refs(m) if r in uniq] for n, m in uniq.items()}
    state = {}

    def visit(n, path):
        state[n] = 1
        for nxt in graph[n]:
            if state.get(nxt) == 1:
                add("MC12", "ERROR", n, "cycle: " + " -> ".join(path[path.index(nxt):] + [nxt]))
            elif not state.get(nxt):
                visit(nxt, path + [nxt])
        state[n] = 2

    for n in graph:
        if not state.get(n):
            visit(n, [n])
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda f: (order[f["severity"]], f["code"], f["metric"]))
    return findings


def render(res):
    lines = [f"Metric contract lint  ({res['metrics']} metrics from {', '.join(res['inputs'])}; "
             f"rules verified {VERIFIED})", ""]
    if not res["findings"]:
        lines.append("No findings.")
    for f in res["findings"]:
        lines.append(f"  {f['severity']:<5} {f['code']}  {f['metric']}: {f['message']}")
    c = res["counts"]
    lines += ["", f"{c['ERROR']} error(s), {c['WARN']} warning(s), {c['INFO']} info.  Verdict: {res['verdict']}"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", nargs="+", help="semantic_manifest.json and/or contract files")
    ap.add_argument("--require-version", action="store_true", help="MC09 becomes an error")
    ap.add_argument("--strict", action="store_true", help="warnings also fail (exit 2)")
    ap.add_argument("--sample", action="store_true", help="lint the bundled dbt 1.12 example")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args()
    paths = [asset("semantic_manifest.base.json")] if a.sample else a.input
    if not paths:
        ap.error("give --input FILE [FILE ...] or --sample")
    try:
        metrics, models, measures, kinds = load_many(paths)
        if not metrics:
            raise BadInput("no metrics found in the input")
    except BadInput as e:
        print(f"bad input: {e}", file=sys.stderr)
        return 3
    findings = lint(metrics, models, measures, kinds, a.require_version)
    counts = {s: sum(f["severity"] == s for f in findings) for s in ("ERROR", "WARN", "INFO")}
    failed = counts["ERROR"] or (a.strict and counts["WARN"])
    res = {"inputs": [os.path.basename(p) for p in paths], "kinds": sorted(kinds),
           "metrics": len({m["name"] for m in metrics}), "findings": findings, "counts": counts,
           "verdict": "FAIL" if failed else "PASS"}
    emit(res, a.output, render)
    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
