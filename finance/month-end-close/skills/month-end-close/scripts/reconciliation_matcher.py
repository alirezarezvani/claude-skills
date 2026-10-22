#!/usr/bin/env python3
"""Reconcile a bank statement (or any sub-ledger) to the general ledger, and prove it.

A reconciliation is not "the balances agree". It is a proof: the difference
between the two balances is fully explained by named, dated, aged items, and
someone other than the preparer has reviewed it. This script does the matching,
builds the proof, ages what is left, and refuses to call a reconciliation done
when the proof does not close or the review is missing.

Matching, in order:
  1. same reference and same amount
  2. same amount, dates within --date-window days (closest date wins)
  3. same date window, same sign, amounts that are a digit transposition of
     each other (7,980 vs 7,890): one correcting entry for the difference
Whatever is left is a reconciling item:
  in GL, not in source   timing items (deposits in transit, outstanding payments)
  in source, not in GL   items the books are missing (fees, interest, returned
                         payments): each needs a journal entry

Opening-balance rows ("Opening balance", "Balance forward", "Brought forward",
"Beginning balance") are balances, not transactions, so they are never matched
or booked. When the two sides open at different amounts, that difference was
carried in from the prior period: it is reported as such and blocks sign-off
until it is traced in last period's reconciliation. It is never an entry to
book in this period.

Proof (amounts signed from the company's side: receipts +, payments -):
  adjusted source = source balance + GL-only items
  adjusted GL     = GL balance + source-only items + transposition corrections
  unexplained     = adjusted source - adjusted GL - opening difference
                    (must be 0 within --tolerance)

Aging buckets: 0-30, 31-60, 61-90, >90 days before --as-of. The escalation and
stale thresholds are POLICY choices with defaults of 60 and 90 days; set them
to your own reconciliation policy. No standard prescribes them.

CSV columns (header row required): date (YYYY-MM-DD), amount, ref, description
(or memo).
Amounts may use thousands separators or (parentheses) for negatives.

Deterministic, stdlib only, no network.

Exit codes:
    0  RECONCILED with no open items needing action
    2  RECONCILED_WITH_ITEMS (entries to book, items to escalate, or review pending)
    3  invalid input
    4  UNRECONCILED (unexplained difference), or BLOCKED (stale items, an opening
       difference carried in from the prior period, or preparer = reviewer)
"""

import argparse
import csv
import datetime as dt
import io
import json
import re
import sys

OPENING = re.compile(r"\b(opening|beginning|starting)\s+balance\b|\bbalance\s+(forward|b/?f)\b|\bbrought\s+forward\b", re.I)

SAMPLE_GL = """date,amount,ref,description
2026-10-03,12500.00,INV-1001,Customer receipt Acme
2026-10-07,-4200.00,CHK-5521,Office lease
2026-10-15,-860.40,CHK-5522,Utilities
2026-10-28,-1500.00,CHK-5530,Contractor payment
2026-10-31,7300.00,DEP-1031,Deposit Beta Corp
2026-07-14,-240.00,CHK-5390,Vendor refund never cashed
"""
SAMPLE_BANK = """date,amount,ref,description
2026-10-04,12500.00,INV-1001,ACME CORP WIRE
2026-10-09,-4200.00,5521,CHECK 5521
2026-10-17,-860.40,5522,CHECK 5522
2026-10-31,-35.00,,MONTHLY SERVICE FEE
2026-10-31,4.12,,INTEREST PAID
"""
SAMPLE_ARGS = {"gl_balance": 52708.60, "source_balance": 47144.72, "as_of": "2026-10-31",
               "preparer": "Sam", "reviewer": ""}


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def parse_amount(raw):
    s = str(raw).strip().replace(",", "").replace("$", "").replace("€", "")
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()")
    try:
        v = round(float(s), 2)
    except ValueError:
        _fail(f"not an amount: {raw!r}")
    return -v if neg else v


def read_rows(text, label):
    reader = csv.DictReader(io.StringIO(text))
    need = {"date", "amount"}
    if not reader.fieldnames or not need <= {f.strip().lower() for f in reader.fieldnames}:
        _fail(f"{label}: CSV needs at least date and amount columns")
    rows = []
    for n, r in enumerate(reader, 2):
        r = {k.strip().lower(): (v or "").strip() for k, v in r.items() if k}
        try:
            d = dt.date.fromisoformat(r["date"])
        except ValueError:
            _fail(f"{label} line {n}: date must be YYYY-MM-DD (got {r['date']!r})")
        desc = r.get("description") or r.get("memo", "")
        rows.append({"date": d, "amount": parse_amount(r["amount"]), "ref": r.get("ref", ""),
                     "description": desc, "line": n, "opening": bool(OPENING.search(desc))})
    return rows


def split_opening(rows):
    """Separate opening-balance rows (balances, not transactions) from transactions."""
    return [r for r in rows if r["opening"]], [r for r in rows if not r["opening"]]


def is_transposition(a, b):
    """True when two amounts are the same digits in a different order (7,980 vs 7,890)."""
    da, db = f"{abs(a):.2f}".replace(".", ""), f"{abs(b):.2f}".replace(".", "")
    return a != b and (a > 0) == (b > 0) and sorted(da) == sorted(db) and round(abs(a - b) * 100) % 9 == 0


def norm_ref(ref):
    return "".join(ch for ch in ref.upper() if ch.isdigit()) or ref.upper()


def match(gl, src, window):
    gl_open, src_open, pairs = list(gl), list(src), []
    for g in list(gl_open):
        if not g["ref"]:
            continue
        hit = next((s for s in src_open if s["ref"] and norm_ref(s["ref"]) == norm_ref(g["ref"]) and s["amount"] == g["amount"]), None)
        if hit:
            pairs.append((g, hit, "ref+amount"))
            gl_open.remove(g)
            src_open.remove(hit)
    for g in sorted(list(gl_open), key=lambda r: r["date"]):
        cands = [s for s in src_open if s["amount"] == g["amount"] and abs((s["date"] - g["date"]).days) <= window]
        if cands:
            hit = min(cands, key=lambda s: abs((s["date"] - g["date"]).days))
            pairs.append((g, hit, "amount+date"))
            gl_open.remove(g)
            src_open.remove(hit)
    transposed = []
    for g in sorted(list(gl_open), key=lambda r: r["date"]):
        cands = [s for s in src_open if is_transposition(g["amount"], s["amount"])
                 and abs((s["date"] - g["date"]).days) <= window]
        if cands:
            hit = min(cands, key=lambda s: abs((s["date"] - g["date"]).days))
            transposed.append((g, hit))
            gl_open.remove(g)
            src_open.remove(hit)
    return pairs, gl_open, src_open, transposed


def bucket(days):
    return "0-30" if days <= 30 else "31-60" if days <= 60 else "61-90" if days <= 90 else ">90"


def reconcile(gl, src, gl_balance, src_balance, as_of, window, tolerance, escalate, stale, preparer, reviewer, label):
    gl_opening, gl = split_opening(gl)
    src_opening, src = split_opening(src)
    pairs, gl_only, src_only, transposed = match(gl, src, window)
    items = []
    for side, rows in (("in GL, not in " + label, gl_only), ("in " + label + ", not in GL", src_only)):
        for r in rows:
            age = (as_of - r["date"]).days
            action = "timing - confirm it clears next period" if side.startswith("in GL") else "book a journal entry"
            items.append({"side": side, "date": r["date"].isoformat(), "amount": r["amount"], "ref": r["ref"],
                          "description": r["description"], "age_days": age, "bucket": bucket(age), "action": action})
    for g, sr in transposed:
        age = (as_of - g["date"]).days
        diff = round(sr["amount"] - g["amount"], 2)
        items.append({"side": "transposition", "date": g["date"].isoformat(), "amount": diff,
                      "ref": g["ref"] or sr["ref"], "description": g["description"] or sr["description"],
                      "age_days": age, "bucket": bucket(age),
                      "action": f"correct the GL posting: {label} shows {sr['amount']:,.2f}, GL has {g['amount']:,.2f}"})
    findings = []
    proof = None

    # Opening balances: explicit rows win; a side without one is implied from
    # its ending balance only when the other side states its opening explicitly.
    opening_diff = 0.0
    if gl_opening or src_opening:
        gl_open_bal = (sum(r["amount"] for r in gl_opening) if gl_opening
                       else (gl_balance - sum(r["amount"] for r in gl) if gl_balance is not None else None))
        src_open_bal = (sum(r["amount"] for r in src_opening) if src_opening
                        else (src_balance - sum(r["amount"] for r in src) if src_balance is not None else None))
        if gl_open_bal is not None and src_open_bal is not None:
            opening_diff = round(src_open_bal - gl_open_bal, 2)
            if abs(opening_diff) > tolerance:
                findings.append(("R5", "BLOCKER",
                                 f"opening balances differ by {opening_diff:,.2f} ({label} {src_open_bal:,.2f}, GL {gl_open_bal:,.2f}): "
                                 "carried in from the prior period, not an error in this one; trace it in last period's "
                                 "reconciliation before sign-off and do not book it as a current-period entry"))

    if gl_balance is not None and src_balance is not None:
        adj_src = round(src_balance + sum(r["amount"] for r in gl_only), 2)
        adj_gl = round(gl_balance + sum(r["amount"] for r in src_only)
                       + sum(it["amount"] for it in items if it["side"] == "transposition"), 2)
        unexplained = round(adj_src - adj_gl - opening_diff, 2)
        proof = {"source_balance": src_balance, "gl_balance": gl_balance, "adjusted_source": adj_src,
                 "adjusted_gl": adj_gl, "opening_difference": opening_diff, "unexplained_difference": unexplained}
        if abs(unexplained) > tolerance:
            hint = ""
            cents = round(abs(unexplained) * 100)
            gl_open = gl_balance - sum(r["amount"] for r in gl)
            src_open = src_balance - sum(r["amount"] for r in src)
            if not (gl_opening or src_opening) and abs(round(src_open - gl_open, 2) - unexplained) <= tolerance:
                hint = (f" (opening balances already differ: {label} implies {src_open:,.2f}, GL {gl_open:,.2f};"
                        " start from last period's reconciliation)")
            elif cents % 9 == 0:
                hint = " (divisible by 9: check for a transposed figure)"
            elif any(abs(abs(unexplained) - abs(it["amount"]) * k) <= tolerance for it in items for k in (1, 2)):
                hint = " (equals an open item or twice one: check for a missing or doubled posting)"
            findings.append(("R1", "BLOCKER", f"unexplained difference of {unexplained:,.2f}{hint}; the reconciliation does not prove"))
    else:
        findings.append(("R1", "WARN", "balances not supplied; matching only, no proof"))
    for it in items:
        if it["age_days"] > stale:
            findings.append(("R2", "BLOCKER", f"{it['ref'] or it['description']} ({it['amount']:,.2f}) is {it['age_days']} days old; write it off, correct it, or document why it stays"))
        elif it["age_days"] > escalate:
            findings.append(("R2", "WARN", f"{it['ref'] or it['description']} ({it['amount']:,.2f}) is {it['age_days']} days old; escalate to the controller"))
    entries = [it for it in items if it["action"] == "book a journal entry"]
    if entries:
        findings.append(("R3", "WARN", f"{len(entries)} {label} item(s) missing from the GL need journal entries ({sum(e['amount'] for e in entries):,.2f})"))
    for it in items:
        if it["side"] == "transposition":
            findings.append(("R3", "WARN", f"probable transposition on {it['date']} ({it['description'] or it['ref'] or 'item'}): "
                                           f"{it['action']}; correcting entry {it['amount']:,.2f}"))
    if not preparer:
        findings.append(("R4", "WARN", "no preparer recorded"))
    if not reviewer:
        findings.append(("R4", "WARN", "not yet reviewed; a reconciliation without an independent reviewer is not complete"))
    elif preparer and reviewer.strip().lower() == preparer.strip().lower():
        findings.append(("R4", "BLOCKER", f"preparer and reviewer are the same person ({reviewer}); segregation of duties fails"))

    sev = [f[1] for f in findings]
    if "BLOCKER" in sev:
        verdict, code = "UNRECONCILED" if any(f[0] == "R1" and f[1] == "BLOCKER" for f in findings) else "BLOCKED", 4
    elif sev:
        verdict, code = "RECONCILED_WITH_ITEMS", 2
    else:
        verdict, code = "RECONCILED", 0
    aging = {b: round(sum(i["amount"] for i in items if i["bucket"] == b), 2) for b in ("0-30", "31-60", "61-90", ">90")}
    return {"verdict": verdict, "as_of": as_of.isoformat(), "matched": len(pairs),
            "match_methods": {m: sum(p[2] == m for p in pairs) for m in ("ref+amount", "amount+date")},
            "proof": proof, "aging": aging, "reconciling_items": items,
            "preparer": preparer or None, "reviewer": reviewer or None,
            "findings": [{"id": i, "severity": s, "message": m} for i, s, m in sorted(findings, key=lambda f: (f[1] != "BLOCKER", f[0]))]}, code


def render(r):
    out = [f"Reconciliation as of {r['as_of']}: {r['verdict']}",
           f"  matched {r['matched']} ({r['match_methods']['ref+amount']} by reference, {r['match_methods']['amount+date']} by amount and date)"]
    if r["proof"]:
        p = r["proof"]
        opening = f"; opening difference {p['opening_difference']:,.2f}" if p.get("opening_difference") else ""
        out.append(f"  adjusted source {p['adjusted_source']:,.2f} vs adjusted GL {p['adjusted_gl']:,.2f}{opening}; unexplained {p['unexplained_difference']:,.2f}")
    out.append("  aging: " + ", ".join(f"{b} {v:,.2f}" for b, v in r["aging"].items()))
    for it in r["reconciling_items"]:
        out.append(f"    {it['date']} {it['amount']:>12,.2f}  {it['ref'] or '-':<9} {it['description'][:28]:<28} {it['side']}; {it['action']} ({it['age_days']}d)")
    out += [f"  [{f['severity']}] {f['id']}: {f['message']}" for f in r["findings"]]
    out.append(f"  preparer: {r['preparer'] or '-'}   reviewer: {r['reviewer'] or '-'}")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Match a bank statement or sub-ledger to the GL, prove the reconciliation, age open items, check review.")
    p.add_argument("--gl", help="GL detail CSV (date, amount, ref, description)")
    p.add_argument("--source", help="bank statement or sub-ledger CSV, same columns")
    p.add_argument("--source-label", default="bank", help="name for the source side (default bank)")
    p.add_argument("--gl-balance", type=float, help="GL ending balance")
    p.add_argument("--source-balance", type=float, help="statement or sub-ledger ending balance")
    p.add_argument("--as-of", help="period-end date YYYY-MM-DD (default today)")
    p.add_argument("--date-window", type=int, default=5, help="days allowed between matched dates (default 5)")
    p.add_argument("--tolerance", type=float, default=0.005, help="unexplained difference tolerated (default 0.005)")
    p.add_argument("--escalate-days", type=int, default=60, help="policy: age that triggers escalation (default 60)")
    p.add_argument("--stale-days", type=int, default=90, help="policy: age that blocks sign-off (default 90)")
    p.add_argument("--preparer", default="", help="who prepared the reconciliation")
    p.add_argument("--reviewer", default="", help="who reviewed it (must differ from preparer)")
    p.add_argument("--sample", action="store_true", help="run on an embedded sample bank reconciliation")
    p.add_argument("--output", choices=["text", "json"], default="text")
    a = p.parse_args()

    if a.sample:
        gl, src = read_rows(SAMPLE_GL, "gl"), read_rows(SAMPLE_BANK, "bank")
        s = SAMPLE_ARGS
        gl_bal, src_bal, as_of, prep, rev = s["gl_balance"], s["source_balance"], dt.date.fromisoformat(s["as_of"]), s["preparer"], s["reviewer"]
    elif a.gl and a.source:
        try:
            gl = read_rows(open(a.gl, encoding="utf-8-sig").read(), a.gl)
            src = read_rows(open(a.source, encoding="utf-8-sig").read(), a.source)
        except OSError as exc:
            _fail(f"cannot read input: {exc.strerror}")
        gl_bal, src_bal, prep, rev = a.gl_balance, a.source_balance, a.preparer, a.reviewer
        try:
            as_of = dt.date.fromisoformat(a.as_of) if a.as_of else dt.date.today()
        except ValueError:
            p.error("--as-of must be YYYY-MM-DD")
    else:
        p.error("give --gl and --source, or --sample")
    report, code = reconcile(gl, src, gl_bal, src_bal, as_of, a.date_window, a.tolerance, a.escalate_days,
                             a.stale_days, prep, rev, a.source_label)
    print(json.dumps(report, indent=2) if a.output == "json" else render(report))
    return code


if __name__ == "__main__":
    sys.exit(main())
