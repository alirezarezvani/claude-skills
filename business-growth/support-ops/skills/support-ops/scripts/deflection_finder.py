#!/usr/bin/env python3
"""Find which support contact reasons to deflect, automate or fix at the source.

Input: a tickets CSV with columns id and topic (the helpdesk's tag or
category) or subject, and optionally handle_time_min, macro (the canned reply
or resolution code used), reopened (0/1) and csat (1-5). Rows without a topic
are grouped by a normalised subject (numbers, ids and stop words removed).

Per contact reason it reports volume, share, workload hours, how concentrated
the answers are (share of the most-used macro) and the reopen rate, then
recommends one action:

  FIX_ROOT_CAUSE  reopen rate >= --max-reopen, or the topic names a defect
                  (bug, error, crash, outage, broken, not working): an
                  article will not stop a product problem
  DEFLECT         one macro answers >= --min-concentration of tickets and
                  reopen is low: the answer is known and stable, publish it
                  where customers look (help center, in-product)
  AUTOMATE        a macro answers >= half but < --min-concentration:
                  agents need a faster path (macro, form, workflow), not
                  customers
  REVIEW          answers vary: needs a person to read a sample

Only reasons inside the Pareto head (cumulative share up to --pareto, default
80%) and with at least --min-tickets are ranked. Deflection savings are an
upper bound: the share that self-service actually resolves has to be measured
after launch.

Exit codes: 0 no candidates, 2 candidates found, 3 bad input.
Deterministic, stdlib only, no network.
"""
import argparse
import csv
import io
import json
import re
import statistics
import sys
from collections import Counter, defaultdict

EXIT = {"NONE": 0, "CANDIDATES": 2, "BAD_INPUT": 3}
DEFECT = re.compile(r"\b(bug|error|crash|crashes|outage|broken|not working|fails?|failed|failing|500|down)\b", re.I)
STOP = set("a an the to my i we our is are was can cant can't not how do does for of on in with and or please help "
           "hi hello issue problem question re fw fwd".split())

SAMPLE_ROWS = [
    ("password reset", "Password reset link", "pw-reset-steps", 4, 0, 5, 140),
    ("invoice copy", "Need a copy of invoice INV-2231", "send-invoice-portal", 3, 0, 5, 95),
    ("export csv error", "CSV export fails with error 500", "export-known-issue", 11, 1, 2, 60),
    ("change plan", "How do I upgrade my plan", "plan-change-howto", 6, 0, 4, 55),
    ("sso setup", "SAML SSO configuration help", "", 25, 0, 4, 30),
    ("refund request", "Refund for duplicate charge", "refund-approve", 9, 0, 4, 28),
    ("api rate limit", "Getting 429 from the API", "rate-limit-docs", 8, 0, 4, 22),
    ("other", "Question about the roadmap", "", 12, 0, 4, 15),
]


def build_sample():
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["id", "topic", "subject", "macro", "handle_time_min", "reopened", "csat"])
    n = 0
    for topic, subj, macro, aht, reopen_bias, csat, count in SAMPLE_ROWS:
        for i in range(count):
            n += 1
            m = macro if (macro and i % 10 < (9 if topic in ("password reset", "invoice copy") else 6)) else ("" if not macro else "custom-reply")
            reo = 1 if reopen_bias and i % 3 == 0 else 0
            w.writerow([f"T-{n}", topic, subj, m, aht + (i % 3), reo, csat])
    return out.getvalue()


def norm_subject(s):
    s = re.sub(r"[A-Z]{2,}-?\d+|\d+", " ", s or "")
    words = [w for w in re.findall(r"[a-z]+", s.lower()) if w not in STOP and len(w) > 2]
    return " ".join(words[:4]) or "(empty)"


def analyse(text, pareto, min_tickets, min_conc, max_reopen):
    rdr = csv.DictReader(io.StringIO(text))
    cols = set(rdr.fieldnames or [])
    if "id" not in cols or not ({"topic", "subject"} & cols):
        raise ValueError("tickets CSV needs id and topic (or subject)")
    groups = defaultdict(list)
    for r in rdr:
        key = (r.get("topic") or "").strip().lower() or "~" + norm_subject(r.get("subject"))
        groups[key].append(r)
    total = sum(len(v) for v in groups.values())
    if total == 0:
        raise ValueError("no tickets")
    rows = []
    cum = 0.0
    for key, items in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        n = len(items)
        share = n / total
        ht = [float(x["handle_time_min"]) for x in items if (x.get("handle_time_min") or "").strip()]
        macros = Counter((x.get("macro") or "").strip() for x in items if (x.get("macro") or "").strip())
        top_macro, top_n = (macros.most_common(1)[0] if macros else ("", 0))
        conc = top_n / n
        reopen = sum((x.get("reopened") or "0").strip() in ("1", "true", "yes") for x in items) / n
        csat = [float(x["csat"]) for x in items if (x.get("csat") or "").strip()]
        label = key[1:] + " (by subject)" if key.startswith("~") else key
        in_head = cum < pareto
        cum += share
        if max_reopen <= reopen or DEFECT.search(label) or any(DEFECT.search(x.get("subject") or "") for x in items[:20]) and reopen > 0:
            action, why = "FIX_ROOT_CAUSE", f"reopen {reopen:.0%}" + (" and defect wording" if DEFECT.search(label) else "")
        elif conc >= min_conc:
            action, why = "DEFLECT", f"'{top_macro}' answers {conc:.0%}"
        elif conc >= 0.5:
            action, why = "AUTOMATE", f"'{top_macro}' answers {conc:.0%}, below {min_conc:.0%}"
        else:
            action, why = "REVIEW", "answers vary" if macros else "no macro data"
        rows.append({"reason": label, "tickets": n, "share": round(share, 3), "cumulative": round(cum, 3),
                     "workload_h": round(sum(ht) / 60, 1) if ht else None,
                     "median_handle_min": statistics.median(ht) if ht else None,
                     "top_macro": top_macro or None, "macro_concentration": round(conc, 3),
                     "reopen_rate": round(reopen, 3), "csat_avg": round(statistics.mean(csat), 2) if csat else None,
                     "action": action, "why": why, "ranked": in_head and n >= min_tickets})
    ranked = [r for r in rows if r["ranked"]]
    deflect_h = sum(r["workload_h"] or 0 for r in ranked if r["action"] == "DEFLECT")
    total_h = sum(r["workload_h"] or 0 for r in rows)
    return {"verdict": "CANDIDATES" if any(r["action"] != "REVIEW" for r in ranked) else "NONE",
            "tickets": total, "reasons": len(rows), "workload_h": round(total_h, 1),
            "deflect_upper_bound_h": round(deflect_h, 1),
            "thresholds": {"pareto": pareto, "min_tickets": min_tickets, "min_concentration": min_conc, "max_reopen": max_reopen},
            "ranked": ranked, "tail": [r for r in rows if not r["ranked"]]}


def render(res):
    out = [f"Deflection finder: {res['verdict']}  ({res['tickets']} tickets, {res['reasons']} reasons, {res['workload_h']}h handle time)", ""]
    for r in res["ranked"]:
        wl = f"{r['workload_h']}h" if r["workload_h"] is not None else "n/a"
        out.append(f"  {r['action']:15s} {r['reason'][:32]:32s} {r['tickets']:>5d} ({r['share']:.0%}, cum {r['cumulative']:.0%})  {wl:>7s}  {r['why']}")
    out.append("")
    out.append(f"Upper bound on hours DEFLECT topics take today: {res['deflect_upper_bound_h']}h. "
               "Measure what self-service actually resolves after launch before claiming savings.")
    if res["tail"]:
        out.append(f"Not ranked (outside the Pareto head or too few tickets): {len(res['tail'])} reasons")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], epilog="Exit codes: 0 no candidates, 2 candidates, 3 bad input.")
    ap.add_argument("--tickets", help="tickets CSV (id, topic or subject [, macro, handle_time_min, reopened, csat])")
    ap.add_argument("--pareto", type=float, default=0.8, help="rank reasons inside this cumulative share (default 0.8)")
    ap.add_argument("--min-tickets", type=int, default=20, help="minimum tickets for a reason to be ranked (default 20)")
    ap.add_argument("--min-concentration", type=float, default=0.7, help="top-macro share for DEFLECT (default 0.7)")
    ap.add_argument("--max-reopen", type=float, default=0.15, help="reopen rate at or above which a reason is FIX_ROOT_CAUSE (default 0.15)")
    ap.add_argument("--sample", action="store_true", help="run on a built-in ticket set")
    ap.add_argument("--output", "--format", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        if a.sample:
            text = build_sample()
        elif a.tickets:
            with open(a.tickets, encoding="utf-8-sig") as fh:
                text = fh.read()
        else:
            raise ValueError("give --tickets FILE or --sample")
        for v in (a.pareto, a.min_concentration, a.max_reopen):
            if not 0 < v <= 1:
                raise ValueError("--pareto, --min-concentration and --max-reopen must be in (0, 1]")
        res = analyse(text, a.pareto, a.min_tickets, a.min_concentration, a.max_reopen)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT["BAD_INPUT"]
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
