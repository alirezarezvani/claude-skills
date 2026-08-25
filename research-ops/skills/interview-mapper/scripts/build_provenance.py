#!/usr/bin/env python3
"""
build_provenance.py — a single audit trail: insight → cluster → nugget → quote → line → interview.

Full traceability of every conclusion — a feature closed products lack.
Joins the output of score_insights.py with (opt.) support verdicts from check_support.py and the
verbatim status from verify_quotes.py, so every piece of evidence carries: verified? support?

Input:
  --insights  output of score_insights.py (clusters with evidence)
  --support   (opt.) output of check_support.py — adds support to quotes
  --verify    (opt.) output of verify_quotes.py — adds verify_status if absent from evidence
Output: provenance.json (machine-readable graph) + brief console.

CLI: python build_provenance.py --insights scored.json [--support sup.json] [--verify q.json]
        [--out provenance.json] [--output {human,json}]
     python build_provenance.py --sample
"""

import argparse
import json
import sys

SAMPLE_SCORED = {
    "summary": {"total_interviews": 3, "insights": 1, "watchlist": 0, "weak": 0},
    "clusters": [
        {
            "cluster": "export-distrust",
            "status": "insight",
            "prevalence": "3/3",
            "roles": ["customer"],
            "severity": 4.0,
            "triangulated": True,
            "tension": False,
            "score_combined": 0.8,
            "evidence": [
                {
                    "interview": "P1",
                    "role": "customer",
                    "line": 4,
                    "verified": True,
                    "quote": "The export didn't match what I saw on screen, so I stopped trusting it",
                },
                {
                    "interview": "P2",
                    "role": "customer",
                    "line": 9,
                    "verified": True,
                    "quote": "I don't trust the export, so I re-check it by hand every time",
                },
            ],
        }
    ],
}


def _read_json(path):
    """Read a JSON file; broken JSON or a missing file → a clear error, exit 1."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except OSError as e:
        sys.exit(f"error: {path}: {e.strerror or e}")
    except UnicodeDecodeError as e:
        sys.exit(f"error: {path}: not UTF-8 ({e.reason})")
    except json.JSONDecodeError as e:
        sys.exit(
            f"error: {path}: invalid JSON — line {e.lineno}, column {e.colno} ({e.msg})"
        )


def index_by_quote(path, field_map):
    """Indexes records from an (optional) JSON output by (cell, quote prefix)."""
    d = {}
    if not path:
        return d
    data = _read_json(path)
    rows = data.get("results", data) if isinstance(data, dict) else data
    for r in rows:
        key = (r.get("cell"), (r.get("quote") or "")[:60])
        d[key] = {k: r.get(v) for k, v in field_map.items()}
    return d


def main():
    """CLI: joins score_insights/check_support/verify_quotes into a single provenance graph."""
    ap = argparse.ArgumentParser(
        description="Join score_insights/check_support/verify_quotes into a provenance graph."
    )
    ap.add_argument(
        "--insights", default=None, help="Required unless --sample is given"
    )
    ap.add_argument("--support", default=None)
    ap.add_argument("--verify", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument(
        "--sample",
        action="store_true",
        help="Run on a built-in sample score_insights.py output",
    )
    ap.add_argument(
        "--output", choices=["human", "json"], default="human", help="Output format"
    )
    a = ap.parse_args()

    if a.sample:
        scored = SAMPLE_SCORED
    else:
        if not a.insights:
            sys.exit("error: --insights is required unless --sample is given")
        scored = _read_json(a.insights)
    sup = index_by_quote(a.support, {"support": "support"})
    ver = index_by_quote(
        a.verify, {"verify_status": "status", "line_found": "line_found"}
    )

    graph = []
    for c in scored.get("clusters", []):
        insight = {
            "cluster": c["cluster"],
            "status": c["status"],
            "prevalence": c["prevalence"],
            "roles": c["roles"],
            "severity": c["severity"],
            "triangulated": c["triangulated"],
            "tension": c["tension"],
            "score": c["score_combined"],
            "evidence": [],
        }
        for e in c["evidence"]:
            key = (None, (e.get("quote") or "")[:60])
            # key by quote without cell (evidence from score doesn't always carry cell)
            skey = next((k for k in sup if k[1] == key[1]), None)
            vkey = next((k for k in ver if k[1] == key[1]), None)
            insight["evidence"].append(
                {
                    "interview": e.get("interview"),
                    "role": e.get("role"),
                    "quote": e.get("quote"),
                    "line": e.get("line"),
                    "verified": e.get("verified"),
                    "verify_status": (ver.get(vkey, {}) or {}).get("verify_status")
                    if vkey
                    else None,
                    "support": (sup.get(skey, {}) or {}).get("support")
                    if skey
                    else None,
                }
            )
        graph.append(insight)

    out = {
        "summary": {
            "insights": scored.get("summary", {}),
            "note": "Every piece of evidence is traceable: interview→quote→line, with verified and support status.",
        },
        "provenance": graph,
    }
    out_path = None
    if a.out or not a.sample:
        out_path = a.out or "provenance.json"
        open(out_path, "w", encoding="utf-8").write(
            json.dumps(out, ensure_ascii=False, indent=2)
        )

    if a.output == "json":
        result = dict(out)
        result["out"] = out_path
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(
            f"Provenance graph: {len(graph)} clusters → {out_path or '(sample, no --out given)'}"
        )
        for g in graph:
            ev = g["evidence"]
            unver = sum(1 for e in ev if not e["verified"])
            print(
                f"  {g['cluster']} [{g['status']}] {g['prevalence']} int | evidence {len(ev)}"
                + (f" | NOT verified: {unver}" if unver else "")
            )


if __name__ == "__main__":
    main()
