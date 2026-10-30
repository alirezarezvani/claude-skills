#!/usr/bin/env python3
"""Check that every UI surface has its required interaction states designed, built and evidenced.

Screens are reviewed in their happy state; users meet the other ones. A list
with no empty state, a form with no server-error state, or a button with no
busy state is unfinished, however good the screenshot looks. This script
derives the required states from what each surface is (its kind) and checks
the state matrix you keep for it. An unlisted state counts as missing.

Kinds and the states they require (BLOCKING states marked *)
  data_view   loading*, empty*, error*, populated, long_content
  form        default, focus_visible*, validation_error*, submitting*, success, server_error*
  action      default, hover, focus_visible*, disabled, busy*, failure*     (control that starts async work)
  control     default, hover, focus_visible*, active, disabled               (link, tab, toggle, menu item)
  media       loading, error*, populated                                     (image, video, embed)
  page        narrow_320*, wide_1440, long_content                           (whole screen layout)

Status values: DONE (needs evidence: screenshot path, story id or test name),
PARTIAL, MISSING, NA (needs a reason).

Findings
  MISSING_BLOCKING     required blocking state missing, partial or unlisted     BLOCKER
  MISSING_STATE        other required state missing, partial or unlisted        HIGH
  DONE_NO_EVIDENCE     DONE with no evidence                                     HIGH
  EVIDENCE_NOT_FOUND   evidence looks like a file path but does not exist        HIGH
  NA_NO_REASON         NA with no reason                                         HIGH
  UNKNOWN_STATE        state not in the kind's list (kept, reported)             WARN

Matrix CSV columns: surface, kind, state, status, evidence, note
Extra states per kind: --require kind:state[,kind:state]

Deterministic, stdlib only, no network.
"""
import argparse
import csv
import io
import json
import os
import sys

REQUIRED = {
    "data_view": ["loading", "empty", "error", "populated", "long_content"],
    "form": ["default", "focus_visible", "validation_error", "submitting", "success", "server_error"],
    "action": ["default", "hover", "focus_visible", "disabled", "busy", "failure"],
    "control": ["default", "hover", "focus_visible", "active", "disabled"],
    "media": ["loading", "error", "populated"],
    "page": ["narrow_320", "wide_1440", "long_content"],
}
BLOCKING = {
    "data_view": {"loading", "empty", "error"},
    "form": {"focus_visible", "validation_error", "submitting", "server_error"},
    "action": {"focus_visible", "busy", "failure"},
    "control": {"focus_visible"},
    "media": {"error"},
    "page": {"narrow_320"},
}
WHY = {
    "loading": "users see a blank or frozen screen while data arrives (Nielsen heuristic 1, visibility of system status)",
    "empty": "first-run and zero-result screens are where users decide what to do next",
    "error": "the request will fail sometimes; without this state the screen lies or breaks",
    "validation_error": "users need to know which field is wrong and how to fix it (heuristic 9)",
    "server_error": "a failed submit must keep the input and say what to do next",
    "submitting": "without it users double-submit",
    "busy": "without it users click again or think nothing happened",
    "failure": "the action will fail sometimes; say so and offer a retry",
    "focus_visible": "keyboard users cannot see where they are (WCAG 2.4.7)",
    "narrow_320": "content must reflow at 320 CSS px without horizontal scrolling (WCAG 1.4.10)",
}
STATUSES = {"DONE", "PARTIAL", "MISSING", "NA"}
SEV_ORDER = {"BLOCKER": 0, "HIGH": 1, "WARN": 2}
EXIT = {"BLOCKED": 4, "FINDINGS": 2, "COMPLETE": 0}


def _looks_like_path(s):
    return ("/" in s or "\\" in s) and os.path.splitext(s)[1].lower() in {
        ".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".webm", ".pdf", ".json", ".html"}


def analyse(text, extra=None, evidence_root=None):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("matrix is empty")
    need = {"surface", "kind", "state", "status"}
    missing_cols = need - set(k.strip().lower() for k in rows[0].keys() if k)
    if missing_cols:
        raise ValueError(f"missing columns: {', '.join(sorted(missing_cols))}")
    required = {k: list(v) for k, v in REQUIRED.items()}
    for item in extra or []:
        kind, _, state = item.partition(":")
        if kind not in required or not state:
            raise ValueError(f"bad --require entry '{item}' (use kind:state, kind in {', '.join(REQUIRED)})")
        required[kind].append(state)

    surfaces, errors = {}, []
    for i, r in enumerate(rows, 2):
        r = {(k or "").strip().lower(): (v or "").strip() for k, v in r.items()}
        kind, status = r["kind"].lower(), r["status"].upper()
        if kind not in required:
            errors.append(f"row {i}: unknown kind '{r['kind']}' (use {', '.join(REQUIRED)})")
            continue
        if status not in STATUSES:
            errors.append(f"row {i}: unknown status '{r['status']}' (use DONE, PARTIAL, MISSING, NA)")
            continue
        s = surfaces.setdefault(r["surface"], {"kind": kind, "states": {}})
        if s["kind"] != kind:
            errors.append(f"row {i}: surface '{r['surface']}' listed as both {s['kind']} and {kind}")
            continue
        s["states"][r["state"].lower()] = {"status": status, "evidence": r.get("evidence", ""), "note": r.get("note", "")}
    if errors:
        raise ValueError("; ".join(errors[:10]))

    findings, coverage = [], []
    for name, s in surfaces.items():
        kind, states = s["kind"], s["states"]
        done = 0
        for st in required[kind]:
            row = states.get(st)
            status = row["status"] if row else "UNLISTED"
            if status == "DONE":
                done += 1
                ev = row["evidence"]
                if not ev:
                    findings.append(_f(name, st, "DONE_NO_EVIDENCE", "HIGH", "marked DONE with no evidence",
                                       "Link a screenshot, story id or test that shows this state."))
                elif evidence_root and _looks_like_path(ev) and not os.path.exists(os.path.join(evidence_root, ev)):
                    findings.append(_f(name, st, "EVIDENCE_NOT_FOUND", "HIGH", f"evidence '{ev}' not found under {evidence_root}",
                                       "Fix the path or capture the screenshot."))
            elif status == "NA":
                done += 1
                if not (row["note"] or row["evidence"]):
                    findings.append(_f(name, st, "NA_NO_REASON", "HIGH", "marked NA with no reason",
                                       "Say why this state cannot occur (e.g. data is static and bundled)."))
            else:
                blocking = st in BLOCKING.get(kind, set())
                why = WHY.get(st, "required for this kind of surface")
                findings.append(_f(name, st, "MISSING_BLOCKING" if blocking else "MISSING_STATE",
                                   "BLOCKER" if blocking else "HIGH", f"{status.lower()}: {why}",
                                   "Design and build the state, then add evidence to the matrix."))
        for st in states:
            if st not in required[kind]:
                findings.append(_f(name, st, "UNKNOWN_STATE", "WARN", f"'{st}' is not a required {kind} state",
                                   "Fine if intentional; check for a typo of a required state."))
        coverage.append({"surface": name, "kind": kind, "done": done, "required": len(required[kind]),
                         "pct": round(100 * done / len(required[kind]))})
    findings.sort(key=lambda f: (SEV_ORDER[f["severity"]], f["surface"], f["state"]))
    counts = {k: sum(1 for f in findings if f["severity"] == k) for k in SEV_ORDER}
    total_req = sum(c["required"] for c in coverage)
    total_done = sum(c["done"] for c in coverage)
    verdict = "BLOCKED" if counts["BLOCKER"] else ("FINDINGS" if counts["HIGH"] or counts["WARN"] else "COMPLETE")
    return {"verdict": verdict, "surfaces": len(surfaces), "coverage_pct": round(100 * total_done / total_req),
            "counts": counts, "coverage": coverage, "findings": findings}


def _f(surface, state, code, sev, msg, fix):
    return {"surface": surface, "state": state, "code": code, "severity": sev, "message": msg, "fix": fix}


def render(out):
    lines = [f"design-qa state matrix: {out['verdict']}  ({out['surfaces']} surfaces, {out['coverage_pct']}% of required states covered; "
             f"{out['counts']['BLOCKER']} blocker, {out['counts']['HIGH']} high, {out['counts']['WARN']} warn)", ""]
    for c in out["coverage"]:
        lines.append(f"  {c['surface']:<28} {c['kind']:<10} {c['done']}/{c['required']}  {c['pct']}%")
    lines.append("")
    for f in out["findings"]:
        lines.append(f"[{f['severity']}] {f['code']}  {f['surface']} :: {f['state']}")
        lines.append(f"    {f['message']}")
        lines.append(f"    fix: {f['fix']}")
    return "\n".join(lines)


SAMPLE = """surface,kind,state,status,evidence,note
Invoices list,data_view,loading,DONE,shots/invoices-loading.png,
Invoices list,data_view,empty,MISSING,,
Invoices list,data_view,error,PARTIAL,,toast only; table stays blank
Invoices list,data_view,populated,DONE,shots/invoices.png,
New invoice,form,default,DONE,story:InvoiceForm/Default,
New invoice,form,focus_visible,DONE,,
New invoice,form,validation_error,DONE,story:InvoiceForm/Invalid,
New invoice,form,submitting,DONE,story:InvoiceForm/Submitting,
New invoice,form,success,DONE,story:InvoiceForm/Saved,
Send invoice,action,default,DONE,story:SendButton/Default,
Send invoice,action,hover,DONE,story:SendButton/Hover,
Send invoice,action,focus_visible,DONE,story:SendButton/Focus,
Send invoice,action,disabled,NA,,
Send invoice,action,busy,DONE,story:SendButton/Sending,
Send invoice,action,failure,MISSING,,
Customer avatar,media,loading,NA,,initials render synchronously
Customer avatar,media,error,DONE,story:Avatar/BrokenImage,
Customer avatar,media,populated,DONE,story:Avatar/Photo,
Invoices page,page,narrow_320,DONE,shots/invoices-320.png,
Invoices page,page,wide_1440,DONE,shots/invoices-1440.png,
Invoices page,page,long_content,DONE,shots/invoices-500-rows.png,
"""


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 complete, 2 findings, 3 invalid input, 4 blocked.")
    p.add_argument("--matrix", help="state matrix CSV (surface,kind,state,status,evidence,note)")
    p.add_argument("--require", action="append", default=[], help="extra required state, kind:state (repeatable)")
    p.add_argument("--evidence-root", help="check that file-path evidence exists under this directory")
    p.add_argument("--sample", action="store_true", help="run on a built-in example")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    try:
        extra = [x for item in a.require for x in item.split(",") if x]
        if a.sample:
            text = SAMPLE
        elif a.matrix:
            with open(a.matrix, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
        else:
            p.print_usage(sys.stderr)
            print("error: give --matrix FILE or --sample", file=sys.stderr)
            return 3
        out = analyse(text, extra, a.evidence_root)
    except (OSError, ValueError) as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return EXIT[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
