#!/usr/bin/env python3
"""Classify every metric change between two versions of the definitions.

Compare the base branch's definitions with the PR's (two semantic_manifest.json
files from `dbt parse`, or two contract files) and say, per metric, whether the
numbers it returns change.

Classes
  BREAKING       a field that decides the number changed (agg, expr, filter,
                 time dimension, table, inputs, window, ...)
  REMOVED        metric gone; every consumer breaks
  RENAMED        gone under one name, identical computation under another
  AFFECTED       definition unchanged (renamed inputs allowed), but an input
                 metric is BREAKING or REMOVED, so its numbers change too
  COSMETIC       only description, label, owner or unit text changed
  ADDED          new metric
  UNCHANGED

Gate: a BREAKING metric is acknowledged when its version went up; a REMOVED or
RENAMED one when it is named in --accept. Anything unacknowledged fails.
AFFECTED metrics never fail on their own; they are listed so their consumers
get told. With --manifest (dbt target/manifest.json) the exposures that read
each changed metric are named.

Exit codes: 0 no unacknowledged breaking change, 2 unacknowledged, 3 bad input.
Deterministic, stdlib only, no network.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from metric_common import (NUMERIC_FIELDS, VERIFIED, BadInput, asset, emit, load_exposures,  # noqa: E402
                           load_many, refs, signature)

COSMETIC_FIELDS = ["description", "label", "owner", "unit"]


def _vnum(v):
    try:
        return tuple(int(x) for x in str(v).lstrip("v").split("."))
    except ValueError:
        return None


def _rename(rec, mapping):
    """Copy of rec with input names mapped through renames, so a pure rename upstream is not a change."""
    if not mapping:
        return rec
    r = dict(rec)
    for k in ("numerator", "denominator"):
        if r.get(k):
            r[k] = dict(r[k], name=mapping.get(r[k]["name"], r[k]["name"]))
    r["inputs"] = [dict(i, name=mapping.get(i["name"], i["name"])) for i in r.get("inputs") or []]
    if r.get("type") == "derived" and r.get("expr"):
        r["expr"] = re.sub(r"\b[A-Za-z_][A-Za-z0-9_]*\b", lambda m: mapping.get(m.group(0), m.group(0)), r["expr"])
    return r


def diff(base, head, accept, consumers):
    b = {m["name"]: m for m in base}
    h = {m["name"]: m for m in head}
    gone = [n for n in b if n not in h]
    new = [n for n in h if n not in b]
    renames = {}
    for n in gone:
        match = [x for x in new if x not in renames.values() and signature(h[x]) == signature(b[n])]
        if len(match) == 1:
            renames[n] = match[0]
    rows = {}
    for n in gone:
        rows[n] = {"metric": n, "class": "RENAMED" if n in renames else "REMOVED", "to": renames.get(n)}
    for n in new:
        if n not in renames.values():
            rows[n] = {"metric": n, "class": "ADDED"}
    for n in b.keys() & h.keys():
        old, cur = _rename(b[n], renames), h[n]
        changed = [f for f in NUMERIC_FIELDS if old.get(f) != cur.get(f)]
        if changed:
            rows[n] = {"metric": n, "class": "BREAKING",
                       "changes": [{"field": f, "before": old.get(f), "after": cur.get(f)} for f in changed],
                       "version": [b[n].get("version"), cur.get("version")]}
        else:
            cos = [f for f in COSMETIC_FIELDS if b[n].get(f) != cur.get(f)]
            rows[n] = {"metric": n, "class": "COSMETIC" if cos else "UNCHANGED", "changes":
                       [{"field": f, "before": b[n].get(f), "after": cur.get(f)} for f in cos]}
    # AFFECTED: unchanged definitions that read a broken metric, transitively (head graph)
    # a pure rename keeps the numbers, so it does not propagate; consumers of the old name are told
    broken = {n for n, r in rows.items() if r["class"] in ("BREAKING", "REMOVED")}
    changed = True
    while changed:
        changed = False
        for n, r in rows.items():
            if r["class"] in ("UNCHANGED", "COSMETIC") and n in h:
                via = sorted(set(refs(h[n])) & broken)
                if via:
                    r["class"], r["via"] = "AFFECTED", via
                    broken.add(n)
                    changed = True
    # acknowledgement
    for n, r in rows.items():
        if r["class"] == "BREAKING":
            vb, vh = (_vnum(v) if v is not None else None for v in r["version"])
            if vb is not None and vh is not None and vh > vb:
                r["ack"] = f"version {r['version'][0]} -> {r['version'][1]}"
            elif r["version"][0] is None and r["version"][1] is None:
                r["problem"] = "unversioned metric changed its numbers; add a version and bump it"
            else:
                r["problem"] = f"numbers change but version stayed {r['version'][1]}; bump it"
        elif r["class"] in ("REMOVED", "RENAMED"):
            if n in accept:
                r["ack"] = "accepted with --accept"
            else:
                r["problem"] = ("removed" if r["class"] == "REMOVED" else f"renamed to {r['to']}") + \
                    "; consumers break. Keep the old name as an alias or pass --accept " + n
        if r["class"] in ("BREAKING", "REMOVED", "RENAMED", "AFFECTED"):
            src = b.get(n) or h.get(n)
            who = list(consumers.get(n, [])) + list(src.get("consumers") or [])
            if r.get("to"):
                who += consumers.get(r["to"], [])
            r["consumers"] = sorted(set(who))
    order = ["REMOVED", "RENAMED", "BREAKING", "AFFECTED", "ADDED", "COSMETIC", "UNCHANGED"]
    return sorted(rows.values(), key=lambda r: (order.index(r["class"]), r["metric"]))


def _fmt(v):
    if isinstance(v, dict):
        return v.get("name", str(v)) + (f" [filter {list(v['filter'])}]" if v.get("filter") else "")
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(_fmt(x) for x in v) + "]"
    return repr(v)


def render(res):
    lines = [f"Metric diff  {res['base']} -> {res['head']}  (verified {VERIFIED})", ""]
    for r in res["rows"]:
        if r["class"] == "UNCHANGED":
            continue
        head = f"  {r['class']:<9} {r['metric']}"
        if r.get("to"):
            head += f" -> {r['to']}"
        if r.get("via"):
            head += f"  (via {', '.join(r['via'])})"
        lines.append(head)
        for c in r.get("changes") or []:
            lines.append(f"              {c['field']}: {_fmt(c['before'])} -> {_fmt(c['after'])}")
        if r.get("problem"):
            lines.append(f"              FAIL: {r['problem']}")
        if r.get("ack"):
            lines.append(f"              ok: {r['ack']}")
        if r.get("consumers"):
            lines.append(f"              tell: {'; '.join(r['consumers'])}")
    c = res["counts"]
    lines += ["", "  " + ", ".join(f"{k.lower()} {v}" for k, v in c.items() if v),
              f"Verdict: {res['verdict']}" + (f" ({res['unacknowledged']} unacknowledged)" if res["unacknowledged"] else "")]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", nargs="+", help="definitions on the base branch")
    ap.add_argument("--head", nargs="+", help="definitions in the change")
    ap.add_argument("--manifest", help="dbt target/manifest.json, to name exposures per metric")
    ap.add_argument("--accept", action="append", default=[], help="removed/renamed metric the owner accepts (repeatable)")
    ap.add_argument("--sample", action="store_true", help="diff the bundled dbt 1.12 base and head examples")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args()
    if a.sample:
        a.base, a.head = [asset("semantic_manifest.base.json")], [asset("semantic_manifest.head.json")]
        a.manifest = a.manifest or asset("manifest_exposures.example.json")
    if not a.base or not a.head:
        ap.error("give --base FILE and --head FILE, or --sample")
    try:
        base, _, _, _ = load_many(a.base)
        head, _, _, _ = load_many(a.head)
        consumers = load_exposures(a.manifest) if a.manifest else {}
    except BadInput as e:
        print(f"bad input: {e}", file=sys.stderr)
        return 3
    rows = diff(base, head, set(a.accept), consumers)
    counts = {}
    for r in rows:
        counts[r["class"]] = counts.get(r["class"], 0) + 1
    unack = sum(1 for r in rows if r.get("problem"))
    res = {"base": ", ".join(os.path.basename(p) for p in a.base), "head": ", ".join(os.path.basename(p) for p in a.head),
           "rows": rows, "counts": counts, "unacknowledged": unack, "verdict": "FAIL" if unack else "PASS"}
    emit(res, a.output, render)
    return 2 if unack else 0


if __name__ == "__main__":
    sys.exit(main())
