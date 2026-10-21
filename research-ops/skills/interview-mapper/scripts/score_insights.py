#!/usr/bin/env python3
"""
score_insights.py — reliability accounting of nugget clusters for insight synthesis (S6.5).

Clustering (which nugget belongs to which theme) and the wordings are done by the MODEL — that's semantics.
This script does the DETERMINISTIC accounting that cannot be fabricated:
  - how many DIFFERENT interviews are in the cluster (not quotes! one person ≠ a pattern),
  - triangulation: a pattern counts only if ≥K different interviews, each with a verified quote,
  - frequency × severity (two axes, plus a «rare but high-stakes» track = watchlist),
  - tension: the cluster has different roles with conflicting valence (+/−),
  - status: insight / watchlist / weak (a single source is an anecdote, not a pattern).

Input nuggets.json — a list:
  {"id","interview","role","cell","observation","quote","line",
   "verified": true/false, "severity": 1..5 (opt.), "valence": "+"/"-"/"0" (opt.),
   "cluster": "C1"}

CLI: python score_insights.py nuggets.json [--k 3] [--out insights_scored.json]
"""

import argparse
import json
import sys
from collections import defaultdict


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


SAMPLE_NUGGETS = [
    {
        "interview": "P1",
        "role": "customer",
        "cell": "A1",
        "cluster": "export-distrust",
        "quote": "The export didn't match what I saw on screen, so I stopped trusting it",
        "line": 4,
        "verified": True,
        "severity": 4,
        "valence": "-",
    },
    {
        "interview": "P2",
        "role": "customer",
        "cell": "A1",
        "cluster": "export-distrust",
        "quote": "I don't trust the export, so I re-check it by hand every time",
        "line": 9,
        "verified": True,
        "severity": 4,
        "valence": "-",
    },
    {
        "interview": "P3",
        "role": "customer",
        "cell": "A1",
        "cluster": "export-distrust",
        "quote": "The export has been wrong for me too",
        "line": 15,
        "verified": True,
        "severity": 3,
        "valence": "-",
    },
    {
        "interview": "P4",
        "role": "customer",
        "cell": "K2",
        "cluster": "wants-dark-mode",
        "quote": "It would be nice to have a dark mode",
        "line": 20,
        "verified": True,
        "severity": 1,
        "valence": "0",
    },
]


def main():
    """CLI: computes triangulation/severity/tensions across nugget clusters and prints a summary."""
    ap = argparse.ArgumentParser(
        description="Score nugget clusters for triangulation, severity, and cross-role tension (S6.5)."
    )
    ap.add_argument(
        "nuggets", nargs="?", help="Path to nuggets.json (from extract_nuggets.py)"
    )
    ap.add_argument(
        "--k",
        type=int,
        default=3,
        help="Triangulation threshold: min. different interviews with a verified quote",
    )
    ap.add_argument(
        "--severe",
        type=float,
        default=4.0,
        help="Severity threshold for watchlist (1..5)",
    )
    ap.add_argument("--out", default=None)
    ap.add_argument(
        "--sample", action="store_true", help="Run on built-in sample nuggets"
    )
    ap.add_argument(
        "--output",
        choices=["human", "json"],
        default="json",
        help="Output format (default json — this script's stdout is machine-consumed downstream)",
    )
    a = ap.parse_args()

    if a.sample:
        nuggets = SAMPLE_NUGGETS
    else:
        if not a.nuggets:
            sys.exit("error: nuggets is required unless --sample is given")
        nuggets = _read_json(a.nuggets)
    all_interviews = sorted({n.get("interview") for n in nuggets if n.get("interview")})
    N = len(all_interviews)

    clusters = defaultdict(list)
    for n in nuggets:
        clusters[n.get("cluster", "UNCLUSTERED")].append(n)

    out = []
    for cid, items in clusters.items():
        interviews = sorted({i.get("interview") for i in items if i.get("interview")})
        roles = sorted({i.get("role") for i in items if i.get("role")})
        verified_interviews = sorted(
            {
                i.get("interview")
                for i in items
                if i.get("verified") and i.get("interview")
            }
        )
        severities = [
            float(i["severity"]) for i in items if i.get("severity") is not None
        ]
        valences = {i.get("valence") for i in items if i.get("valence")}
        # tension: >=2 roles and both + and − at once
        role_valence = defaultdict(set)
        for i in items:
            if i.get("role") and i.get("valence"):
                role_valence[i["role"]].add(i["valence"])
        cross_role = len(roles) >= 2
        valence_conflict = "+" in valences and "-" in valences
        tension = cross_role and valence_conflict

        distinct_iv = len(interviews)
        distinct_verified = len(verified_interviews)
        prevalence = round(distinct_iv / N, 3) if N else 0.0
        severity = round(max(severities), 1) if severities else None
        triangulated = distinct_verified >= a.k

        # frequency×severity: both normalized 0..1, kept honestly separate + combined for sorting
        prev_norm = distinct_iv / N if N else 0.0
        sev_norm = ((severity - 1) / 4) if severity is not None else 0.0
        combined = round(0.5 * prev_norm + 0.5 * sev_norm, 3)

        # status
        if triangulated:
            status = "insight"
        elif severity is not None and severity >= a.severe:
            status = "watchlist"  # rare but severe — don't bury
        elif tension:
            status = "watchlist"  # a cross-role contradiction is interesting even at medium severity
        else:
            status = "weak"  # single source, low severity — an anecdote

        out.append(
            {
                "cluster": cid,
                "status": status,
                "prevalence": f"{distinct_iv}/{N}",
                "prevalence_ratio": prevalence,
                "distinct_interviews": distinct_iv,
                "verified_interviews": distinct_verified,
                "triangulated": triangulated,
                "roles": roles,
                "severity": severity,
                "score_combined": combined,
                "tension": tension,
                "tension_detail": (
                    {r: sorted(v) for r, v in role_valence.items()} if tension else None
                ),
                "n_nuggets": len(items),
                "evidence": [
                    {
                        "interview": i.get("interview"),
                        "role": i.get("role"),
                        "quote": i.get("quote"),
                        "line": i.get("line"),
                        "verified": bool(i.get("verified")),
                    }
                    for i in items
                ],
            }
        )

    # sorting: insights by combined desc, then watchlist by severity, then weak
    order = {"insight": 0, "watchlist": 1, "weak": 2}
    out.sort(
        key=lambda c: (order[c["status"]], -c["score_combined"], -(c["severity"] or 0))
    )

    summary = {
        "total_interviews": N,
        "interviews": all_interviews,
        "clusters": len(out),
        "insights": sum(1 for c in out if c["status"] == "insight"),
        "watchlist": sum(1 for c in out if c["status"] == "watchlist"),
        "weak": sum(1 for c in out if c["status"] == "weak"),
        "tensions": [c["cluster"] for c in out if c["tension"]],
        "k_triangulation": a.k,
        "note": (
            "insight = ≥k different interviews with a verified quote; "
            "watchlist = rare but severe (severity≥%.1f); "
            "weak = single source, not a pattern. "
            "Small N of interviews → patterns are unreliable." % a.severe
        ),
    }
    result = {"summary": summary, "clusters": out}
    js = json.dumps(result, ensure_ascii=False, indent=2)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(js)

    if a.output == "json":
        print(js)
    else:
        print(
            f"Clusters: {summary['clusters']} | insight {summary['insights']} "
            f"| watchlist {summary['watchlist']} | weak {summary['weak']}"
        )
        if summary["tensions"]:
            print(f"  Tensions: {summary['tensions']}")
        if a.out:
            print(f"  → {a.out}")


if __name__ == "__main__":
    main()
