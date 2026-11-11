#!/usr/bin/env python3
"""Classify medical device software under IEC 62304, the FDA documentation level and FDA section 524B.

Reads one row per software system or software item and answers three questions
that teams routinely answer with the wrong input:

  1. IEC 62304:2006+A1:2015 software safety class (A, B, C), clause 4.3.
     A1 rule (Figure 3): software that cannot contribute to a hazardous
     situation is class A; so is software whose contribution leaves an
     acceptable risk once risk control measures EXTERNAL to the software system
     are applied. Otherwise the severity of the possible injury decides:
     non-serious -> B, serious injury or death -> C. Unclassified -> C.
     Items inherit the class of the system they belong to unless a documented
     segregation rationale justifies a lower class, and a system is never lower
     than its highest item.
  2. FDA documentation level (Content of Premarket Submissions for Device
     Software Functions, June 2023): Enhanced when a failure or flaw could
     present a hazardous situation with a probable risk of death or serious
     injury, assessed BEFORE risk control measures. Class III devices and
     device constituents of combination products are generally Enhanced.
     A product can therefore be IEC 62304 class B and FDA Enhanced.
  3. FDA "cyber device" (FD&C Act section 524B(c), 21 U.S.C. 360n-2):
     software validated/installed/authorised by the sponsor + ability to
     connect to the internet + technological characteristics that could be
     vulnerable to cybersecurity threats. If yes, 524B(b)(1)-(3) items are due
     in the premarket submission.

CSV columns (header required; one row per software system or item):
  id                      unique id
  parent                  id of the containing system/item ('' for a software system)
  contributes_to_hazard   yes | no | unknown      can it contribute to a hazardous situation?
  external_control        description of risk control external to this software system ('' if none)
  external_control_verified  yes | no           verified, e.g. by test or usability evaluation
  acceptable_after_external  yes | no | ''      residual risk acceptable once the external control works
  severity                none | non-serious | serious | death | unknown   worst-case possible injury
                          AFTER external risk controls (A1); before them only if there are none
  segregation_rationale   architecture argument for an item class lower than its parent ('' if none)
  claimed_class           A | B | C | ''        class the team has documented today
  -- FDA columns (only read on software system rows; leave blank outside the US) --
  probable_serious_harm_before_controls  yes | no | ''
  device_class_us         I | II | III | ''
  combination_product     yes | no | ''
  internet_capable        yes | no | ''         any ability to connect to the internet, even indirectly
  software_by_sponsor     yes | no | ''

Findings
  CLAIM_TOO_LOW           claimed class lower than the class the inputs support      BLOCKER
  UNVERIFIED_EXTERNAL     an external control is used to lower the class but not verified  BLOCKER
  ITEM_BELOW_PARENT       item classed below its parent without a segregation rationale    BLOCKER
  SYSTEM_BELOW_ITEM       system classed below one of its items                            BLOCKER
  UNKNOWN_INPUT           contribution or severity unknown: treated as class C             HIGH
  ENHANCED_GAP            62304 class A/B but FDA Enhanced documentation applies           HIGH
  CYBER_DEVICE            524B applies: plan, processes, SBOM due in the submission        HIGH
  CLAIM_HIGHER            claimed class above the computed one (allowed; costs effort)     INFO

Deterministic, stdlib only, no network. It applies the rules to the inputs it is
given; the hazard analysis behind those inputs comes from the ISO 14971 risk
management file, and a notified body or FDA reviewer can read borderline
severity calls differently. Clause references are to IEC 62304:2006+A1:2015;
check wording against your licensed copy.

Exit codes:
    0  CLASSIFIED (no findings above INFO)
    2  FINDINGS (HIGH)
    3  invalid input
    4  BLOCKED
"""

import argparse
import csv
import io
import json
import sys

RANK = {"A": 1, "B": 2, "C": 3}
YES = {"yes", "y", "true", "1"}
NO = {"no", "n", "false", "0"}
SEVERITIES = {"none", "non-serious", "serious", "death", "unknown"}
COLUMNS = ["id", "parent", "contributes_to_hazard", "external_control", "external_control_verified",
           "acceptable_after_external", "severity", "segregation_rationale", "claimed_class"]
SEV = {"BLOCKER": 4, "HIGH": 2, "INFO": 0}

SAMPLE = """id,parent,contributes_to_hazard,external_control,external_control_verified,acceptable_after_external,severity,segregation_rationale,claimed_class,probable_serious_harm_before_controls,device_class_us,combination_product,internet_capable,software_by_sponsor
INF-SYS,,yes,hardware pressure-limit valve,yes,no,serious,,B,yes,II,no,yes,yes
INF-UI,INF-SYS,yes,,,,serious,,B,,,,,
INF-DOSE,INF-SYS,yes,,,,serious,,C,,,,,
INF-LOG,INF-SYS,no,,,,none,runs as separate process on a separate core; read-only queue from INF-DOSE,A,,,,,
VIEW-SYS,,yes,clinician confirms every value against the source image,no,yes,non-serious,,A,no,II,no,yes,yes
"""


def norm(v):
    return (v or "").strip()


def yn(v):
    v = norm(v).lower()
    if v in YES:
        return "yes"
    if v in NO:
        return "no"
    return "" if v == "" else "bad"


def parse(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("no rows")
    missing = [c for c in COLUMNS if c not in rows[0]]
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")
    seen = {}
    for i, r in enumerate(rows, 2):
        rid = norm(r["id"])
        if not rid:
            raise ValueError(f"line {i}: empty id")
        if rid in seen:
            raise ValueError(f"line {i}: duplicate id {rid}")
        sev = norm(r["severity"]).lower() or "unknown"
        if sev not in SEVERITIES:
            raise ValueError(f"line {i}: severity must be one of {sorted(SEVERITIES)}")
        cc = norm(r["claimed_class"]).upper()
        if cc and cc not in RANK:
            raise ValueError(f"line {i}: claimed_class must be A, B, C or blank")
        for col in ("contributes_to_hazard", "external_control_verified", "acceptable_after_external"):
            if yn(r[col]) == "bad" and norm(r[col]).lower() != "unknown":
                raise ValueError(f"line {i}: {col} must be yes, no or blank")
        r = {k: norm(v) for k, v in r.items() if k}
        r["severity"] = sev
        r["claimed_class"] = cc
        seen[rid] = r
    for rid, r in seen.items():
        if r["parent"] and r["parent"] not in seen:
            raise ValueError(f"{rid}: parent {r['parent']} not found")
    # cycle check
    for rid in seen:
        walk, cur = set(), rid
        while seen[cur]["parent"]:
            if cur in walk:
                raise ValueError(f"{rid}: parent chain loops")
            walk.add(cur)
            cur = seen[cur]["parent"]
    return seen


def own_class(r, findings):
    """Class from this row's own inputs, per IEC 62304 A1 4.3 / Figure 3."""
    rid = r["id"]
    contrib = norm(r["contributes_to_hazard"]).lower()
    if contrib in NO:
        return "A", "cannot contribute to a hazardous situation (4.3)"
    if contrib not in YES:
        findings.append(("HIGH", "UNKNOWN_INPUT", rid,
                         "contribution to a hazardous situation not established: treated as class C until the risk analysis says otherwise (4.3)"))
        return "C", "unclassified defaults to C"
    if r["external_control"]:
        acc = yn(r["acceptable_after_external"])
        ver = yn(r["external_control_verified"])
        if acc == "yes" and ver == "yes":
            return "A", f"risk acceptable after external control '{r['external_control']}' (4.3, Figure 3)"
        if acc == "yes" and ver != "yes":
            findings.append(("BLOCKER", "UNVERIFIED_EXTERNAL", rid,
                             f"external control '{r['external_control']}' is relied on for class A but is not verified; "
                             "verify it (test, or usability evaluation for a human check) or classify without it"))
    sev = r["severity"]
    if sev == "unknown":
        findings.append(("HIGH", "UNKNOWN_INPUT", rid, "worst-case severity unknown: treated as class C"))
        return "C", "severity unknown"
    if sev == "none":
        findings.append(("HIGH", "UNKNOWN_INPUT", rid,
                         "contributes to a hazardous situation but severity 'none' is contradictory: treated as class C; fix the risk analysis"))
        return "C", "contradictory inputs"
    if sev == "non-serious":
        return "B", "possible injury is non-serious (4.3)"
    return "C", "possible injury is serious or death (4.3)"


def classify(rows):
    findings = []
    own = {}
    why = {}
    for rid, r in rows.items():
        own[rid], why[rid] = own_class(r, findings)
    children = {}
    for rid, r in rows.items():
        if r["parent"]:
            children.setdefault(r["parent"], []).append(rid)

    def subtree_max(rid):
        best = own[rid]
        for c in children.get(rid, []):
            m = subtree_max(c)
            if RANK[m] > RANK[best]:
                best = m
        return best

    computed = {}

    def resolve(rid, parent_cls):
        r = rows[rid]
        cls = subtree_max(rid)
        reason = why[rid]
        if parent_cls and RANK[cls] < RANK[parent_cls]:
            if r["segregation_rationale"]:
                reason += f"; lower than parent via segregation: {r['segregation_rationale']}"
            else:
                cls = parent_cls
                reason = f"inherits class {parent_cls} from {r['parent']} (no segregation rationale)"
        computed[rid] = (cls, reason)
        for c in children.get(rid, []):
            resolve(c, cls)

    for rid, r in rows.items():
        if not r["parent"]:
            resolve(rid, None)

    for rid, r in rows.items():
        cls = computed[rid][0]
        cc = r["claimed_class"]
        if not cc:
            continue
        if RANK[cc] < RANK[cls]:
            findings.append(("BLOCKER", "CLAIM_TOO_LOW", rid,
                             f"documented as class {cc}, inputs support class {cls}: {computed[rid][1]}"))
        elif RANK[cc] > RANK[cls]:
            findings.append(("INFO", "CLAIM_HIGHER", rid,
                             f"documented as class {cc}, inputs support {cls}; allowed, but every {cc}-only activity is now owed"))
        if r["parent"]:
            pc = rows[r["parent"]]["claimed_class"]
            if pc and RANK[cc] < RANK[pc] and not r["segregation_rationale"]:
                findings.append(("BLOCKER", "ITEM_BELOW_PARENT", rid,
                                 f"claimed {cc} under parent claimed {pc} with no segregation rationale (4.3; 5.3.5 for class C)"))
            if pc and RANK[cc] > RANK[pc]:
                findings.append(("BLOCKER", "SYSTEM_BELOW_ITEM", r["parent"],
                                 f"claimed {pc} but contains {rid} claimed {cc}; a system takes its highest item's class"))
    return computed, findings


def fda(rows, computed, findings):
    out = {}
    for rid, r in rows.items():
        if r["parent"]:
            continue
        cols = [r.get(k, "") for k in ("probable_serious_harm_before_controls", "device_class_us",
                                       "combination_product", "internet_capable", "software_by_sponsor")]
        if not any(cols):
            continue
        reasons = []
        if yn(r.get("probable_serious_harm_before_controls")) == "yes":
            reasons.append("failure could present a probable risk of death or serious injury before risk controls")
        if norm(r.get("device_class_us")).upper() == "III":
            reasons.append("Class III device (generally Enhanced)")
        if yn(r.get("combination_product")) == "yes":
            reasons.append("device constituent of a combination product (generally Enhanced)")
        level = "Enhanced" if reasons else "Basic"
        if level == "Enhanced" and computed[rid][0] in ("A", "B"):
            findings.append(("HIGH", "ENHANCED_GAP", rid,
                             f"IEC 62304 class {computed[rid][0]} but FDA Enhanced documentation: submit SDS, unit and integration "
                             "test protocols/reports and a full configuration management and maintenance plan"))
        cyber = yn(r.get("internet_capable")) == "yes" and yn(r.get("software_by_sponsor")) != "no"
        if cyber:
            findings.append(("HIGH", "CYBER_DEVICE", rid,
                             "FD&C Act 524B applies: submit a postmarket vulnerability plan incl. coordinated disclosure (b)(1), "
                             "processes for cybersecurity assurance and patch cadence (b)(2), SBOM (b)(3)"))
        out[rid] = {"documentation_level": level, "reasons": reasons or ["no Enhanced criterion met"],
                    "cyber_device_524B": cyber}
    return out


def run(text):
    rows = parse(text)
    computed, findings = classify(rows)
    fda_out = fda(rows, computed, findings)
    worst = max([SEV[f[0]] for f in findings] or [0])
    verdict = {4: "BLOCKED", 2: "FINDINGS", 0: "CLASSIFIED"}[worst]
    order = {"BLOCKER": 0, "HIGH": 1, "INFO": 2}
    findings.sort(key=lambda f: (order[f[0]], f[2]))
    return {
        "verdict": verdict,
        "standard": "IEC 62304:2006+A1:2015 clause 4.3; FDA device software functions guidance (2023); FD&C Act 524B",
        "classes": [{"id": rid, "parent": rows[rid]["parent"], "class": c, "reason": why,
                     "claimed": rows[rid]["claimed_class"] or None} for rid, (c, why) in computed.items()],
        "fda": fda_out,
        "findings": [{"severity": s, "code": c, "id": i, "detail": d} for s, c, i, d in findings],
        "note": "Inputs come from the ISO 14971 risk management file. Borderline severity calls go to the notified body or FDA reviewer.",
    }


def render(out):
    lines = [f"IEC 62304 / FDA software classification: {out['verdict']}", ""]
    lines.append(f"{'id':<12} {'parent':<10} {'class':<6} {'claimed':<8} reason")
    for c in out["classes"]:
        lines.append(f"{c['id']:<12} {c['parent'] or '-':<10} {c['class']:<6} {c['claimed'] or '-':<8} {c['reason']}")
    if out["fda"]:
        lines.append("")
        for rid, f in out["fda"].items():
            lines.append(f"FDA {rid}: {f['documentation_level']} documentation ({'; '.join(f['reasons'])}); "
                         f"cyber device under 524B: {'yes' if f['cyber_device_524B'] else 'no'}")
    if out["findings"]:
        lines.append("")
        for f in out["findings"]:
            lines.append(f"[{f['severity']}] {f['code']} {f['id']}: {f['detail']}")
    lines += ["", out["note"]]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog="Exit codes: 0 classified, 2 findings, 3 invalid input, 4 blocked.")
    p.add_argument("--inventory", help="software systems/items CSV (see module docstring for columns)")
    p.add_argument("--template", action="store_true", help="print a blank CSV header and exit")
    p.add_argument("--sample", action="store_true", help="run on a built-in infusion-pump example")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if a.template:
        print(SAMPLE.splitlines()[0])
        return 0
    try:
        if a.sample:
            text = SAMPLE
        else:
            if not a.inventory:
                p.print_usage(sys.stderr)
                print("error: give --inventory, --template or --sample", file=sys.stderr)
                return 3
            with open(a.inventory, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
        out = run(text)
    except (OSError, ValueError, csv.Error) as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return {"BLOCKED": 4, "FINDINGS": 2, "CLASSIFIED": 0}[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
