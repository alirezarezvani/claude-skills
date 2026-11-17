#!/usr/bin/env python3
"""Check which entities DORA (Regulation (EU) 2022/2554) catches and which regime applies to each.

DORA has applied since 17 January 2025 (Art 64) to the twenty financial entity
types of Art 2(1)(a)-(t) and reaches ICT third-party service providers (u)
through contracts and, if designated critical, direct oversight. Art 2(3)
excludes six groups; Art 16 puts five small or exempted types on a simplified
ICT risk-management framework; microenterprises get specific relief in several
articles. This script reads an entity list and returns, per entity, in or out,
the regime, the pillars that apply, and the first actions.

Entity CSV columns
  name, type (key; --list-types), microenterprise (yes|no), exemption (blank or one key of --list-exemptions),
  simplified (blank or one key of --list-simplified), nis2_identified (yes|no), ctpp_designated (yes|no, for ict-tpp)

Regimes
  FULL          Arts 5-15 ICT risk management, Arts 17-23 incidents, Arts 24-27 testing, Arts 28-30 third-party risk
  SIMPLIFIED    Art 16 replaces Arts 5-15; the other pillars still apply (proportionately, Art 4)
  EXCLUDED      Art 2(3)
  TPP           ICT third-party service provider: Art 30 terms flow down by contract; Arts 31-44 oversight only if
                designated critical (CTPP)

Deterministic, stdlib only, no network. Not legal advice: the competent authority decides borderline status.

Exit codes:
    0  every entity placed
    2  placed with findings to act on
    3  invalid input
    4  an entity cannot be placed (unknown type)
"""

import argparse
import csv
import io
import json
import sys

TYPES = {
    "credit-institution": ("credit institution", "(a)"), "payment-institution": ("payment institution, incl. PSD2-exempted", "(b)"),
    "aisp": ("account information service provider", "(c)"), "e-money-institution": ("electronic money institution, incl. exempted", "(d)"),
    "investment-firm": ("investment firm", "(e)"), "casp": ("crypto-asset service provider (MiCA) or issuer of asset-referenced tokens", "(f)"),
    "csd": ("central securities depository", "(g)"), "ccp": ("central counterparty", "(h)"), "trading-venue": ("trading venue", "(i)"),
    "trade-repository": ("trade repository", "(j)"), "aifm": ("manager of alternative investment funds", "(k)"),
    "ucits-manco": ("UCITS management company", "(l)"), "drsp": ("data reporting service provider", "(m)"),
    "insurer": ("insurance or reinsurance undertaking", "(n)"), "insurance-intermediary": ("insurance, reinsurance or ancillary insurance intermediary", "(o)"),
    "iorp": ("institution for occupational retirement provision", "(p)"), "cra-agency": ("credit rating agency", "(q)"),
    "benchmark-administrator": ("administrator of critical benchmarks", "(r)"), "crowdfunding": ("crowdfunding service provider", "(s)"),
    "securitisation-repository": ("securitisation repository", "(t)"), "ict-tpp": ("ICT third-party service provider", "(u)"),
}
EXEMPTIONS = {
    "aifm-art3-2": ("AIFM under the Art 3(2) AIFMD small-manager regime", "Art 2(3)(a)", {"aifm"}),
    "solvency-art4": ("insurance undertaking excluded by Art 4 Solvency II (small)", "Art 2(3)(b)", {"insurer"}),
    "iorp-15-members": ("IORP whose schemes have no more than 15 members in total", "Art 2(3)(c)", {"iorp"}),
    "mifid-exempt": ("person exempted under MiFID II Arts 2 and 3", "Art 2(3)(d)", {"investment-firm"}),
    "intermediary-sme": ("insurance intermediary that is a micro, small or medium-sized enterprise", "Art 2(3)(e)", {"insurance-intermediary"}),
    "post-office-giro": ("post office giro institution (CRD Art 2(5)(3))", "Art 2(3)(f)", {"credit-institution"}),
}
SIMPLIFIED = {
    "small-noninterconnected-if": ("small and non-interconnected investment firm", {"investment-firm"}),
    "psd2-exempt-pi": ("payment institution exempted under PSD2", {"payment-institution"}),
    "crd-exempt-ci": ("credit institution exempted under CRD, where the Member State did not use Art 2(4)", {"credit-institution"}),
    "emd-exempt-emi": ("electronic money institution exempted under EMD2", {"e-money-institution"}),
    "small-iorp": ("small institution for occupational retirement provision", {"iorp"}),
}
YES = {"yes", "y", "true", "1"}
SEVERITY_ORDER = ["BLOCKER", "HIGH", "MEDIUM", "INFO"]

SAMPLE = """name,type,microenterprise,exemption,simplified,nis2_identified,ctpp_designated
Nordbank AG,credit-institution,no,,,yes,
PayFlow GmbH,payment-institution,no,,,no,
MiniPay UG,payment-institution,yes,,psd2-exempt-pi,no,
Assekuranz Makler KG,insurance-intermediary,no,intermediary-sme,,no,
Alpine Capital Partners,aifm,no,,,no,
CoreHost Cloud SE,ict-tpp,no,,,yes,no
Velo Pension Fund,iorp,no,iorp-15-members,,no,
Mystery Fintech,neo-bank,no,,,no,
"""


def norm(v):
    return (v or "").strip()


def place(row, line):
    name = norm(row.get("name")) or f"row {line}"
    t = norm(row.get("type")).lower()
    ex = norm(row.get("exemption")).lower()
    simp = norm(row.get("simplified")).lower()
    micro = norm(row.get("microenterprise")).lower() in YES
    findings = []

    def add(sev, code, msg, ref):
        findings.append({"severity": sev, "code": code, "message": msg, "ref": ref})

    e = {"name": name, "type": t, "regime": None, "basis": None, "pillars": [], "findings": findings}
    if t not in TYPES:
        add("BLOCKER", "UNKNOWN_TYPE", f"type '{t}' is not an Art 2(1) entity key (--list-types). If you hold an authorisation, map it to the type it grants; a licence you do not have does not bring you in", "Art 2(1)")
        e["regime"] = "UNPLACED"
        return e
    label, letter = TYPES[t]
    e["basis"] = f"Art 2(1){letter}: {label}"
    if ex:
        if ex not in EXEMPTIONS:
            raise ValueError(f"row {line}: unknown exemption '{ex}' (--list-exemptions)")
        d, ref, types = EXEMPTIONS[ex]
        if t not in types:
            raise ValueError(f"row {line}: exemption '{ex}' does not fit type '{t}'")
        e["regime"], e["basis"] = "EXCLUDED", f"{ref}: {d}"
        add("INFO", "EXCLUDED", "outside DORA; keep the evidence for the exclusion (size, member count, authorisation) and re-check yearly", ref)
        return e
    if t == "ict-tpp":
        ctpp = norm(row.get("ctpp_designated")).lower() in YES
        e["regime"] = "TPP"
        e["pillars"] = ["Art 30 contract terms required by financial-entity customers", "support for customers' incident reporting and testing (TLPT pooled or joint where agreed)"]
        if ctpp:
            e["pillars"].append("direct oversight by the Lead Overseer, Arts 31-44; if established in a third country, financial entities may only use you once you have an EU subsidiary, set up within 12 months of designation (Art 31(12))")
            add("HIGH", "CTPP", "designated critical: oversight plan, information requests, inspections, periodic penalty payments up to 1% of average daily worldwide turnover for up to six months", "Arts 33-35, Art 35(7)-(8)")
        else:
            add("MEDIUM", "CONTRACT_FLOWDOWN", "not directly supervised, but customers must put Art 30(2) terms in every contract and Art 30(3) terms where you support a critical or important function; run register_of_information_check.py on your customer contracts", "Art 28, Art 30")
        return e
    if simp:
        if simp not in SIMPLIFIED:
            raise ValueError(f"row {line}: unknown simplified key '{simp}' (--list-simplified)")
        d, types = SIMPLIFIED[simp]
        if t not in types:
            raise ValueError(f"row {line}: simplified key '{simp}' does not fit type '{t}'")
        e["regime"] = "SIMPLIFIED"
        e["basis"] += f"; Art 16(1): {d}"
        e["pillars"] = ["simplified ICT risk-management framework (Art 16; RTS Delegated Regulation (EU) 2024/1774 Title III)",
                        "major ICT incident classification and reporting (Arts 17-19)", "digital operational resilience testing, proportionate (Arts 4, 24-25)",
                        "ICT third-party risk and register of information (Arts 28-30)"]
    else:
        e["regime"] = "FULL"
        e["pillars"] = ["ICT risk-management framework, management body accountability (Arts 5-15; RTS 2024/1774)",
                        "major ICT incident classification and reporting (Arts 17-19; RTS 2024/1772, 2025/301)",
                        "digital operational resilience testing (Arts 24-25); TLPT every 3 years if identified by the authority (Art 26)",
                        "ICT third-party risk, register of information, Art 30 contract terms, exit strategies (Arts 28-30)"]
    add("HIGH", "REGISTER_OF_INFORMATION", "maintain the register of all ICT third-party contractual arrangements and report it to the competent authority on request and as it asks (annual collection)", "Art 28(3); ITS (EU) 2024/2956")
    add("INFO", "MANAGEMENT_ACCOUNTABLE", "management body defines, approves, oversees and is responsible for the ICT risk-management framework and must keep its ICT knowledge current", "Art 5(2), 5(4)")
    if micro:
        add("INFO", "MICROENTERPRISE", "microenterprise: proportionality applies (Art 4) and several provisions are lighter; e.g. no monthly recurring-incident check (RTS 2024/1772 Art 8(2)). Check each article that names microenterprises", "Art 4; RTS 2024/1772 Art 8(2)")
    if norm(row.get("nis2_identified")).lower() in YES:
        add("MEDIUM", "NIS2_OVERLAP", "also a NIS2 entity: DORA replaces NIS2 Arts 21 and 23 for you; no weekend/holiday extension for initial and intermediate reports; the Member State may require copies to the NIS2 CSIRT", "NIS2 Art 4; DORA Art 19(1); RTS 2025/301 Art 5(5)")
    if t in {"credit-institution", "ccp", "trading-venue"}:
        add("INFO", "NO_WEEKEND_RELIEF", "initial and intermediate reports cannot slip to the next working day", "RTS 2025/301 Art 5(5)")
    return e


def run(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("entity list has no rows")
    if not {"name", "type"} <= set(rows[0].keys()):
        raise ValueError("entity list needs columns name,type")
    ents = [place(r, i + 2) for i, r in enumerate(rows)]
    counts = {s: 0 for s in SEVERITY_ORDER}
    regimes = {}
    for e in ents:
        regimes[e["regime"]] = regimes.get(e["regime"], 0) + 1
        for f in e["findings"]:
            counts[f["severity"]] += 1
    verdict = "BLOCKED" if counts["BLOCKER"] else "FINDINGS" if counts["HIGH"] or counts["MEDIUM"] else "CLEAR"
    return {"verdict": verdict, "summary": {"entities": len(ents), "regimes": regimes, "findings": counts}, "entities": ents}


def render(out):
    lines = [f"DORA scope: {out['verdict']}", ""]
    for e in out["entities"]:
        lines.append(f"- {e['name']}: {e['regime']}" + (f"  [{e['basis']}]" if e["basis"] else ""))
        for p in e["pillars"]:
            lines.append(f"    * {p}")
        for f in sorted(e["findings"], key=lambda f: SEVERITY_ORDER.index(f["severity"])):
            lines.append(f"    {f['severity']:<7} {f['code']}: {f['message']} [{f['ref']}]")
    s = out["summary"]
    lines += ["", f"{s['entities']} entities: " + ", ".join(f"{k} {v}" for k, v in s["regimes"].items()),
              "Findings: " + ", ".join(f"{k} {v}" for k, v in s["findings"].items()),
              "Next: dora_incident_classifier.py for live incidents; register_of_information_check.py for ICT contracts."]
    return "\n".join(lines)


EXIT = {"CLEAR": 0, "FINDINGS": 2, "BLOCKED": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 clear, 2 findings, 3 invalid input, 4 unplaced entity.")
    p.add_argument("--entities", help="entity CSV (columns in the module docstring)")
    p.add_argument("--list-types", action="store_true")
    p.add_argument("--list-exemptions", action="store_true")
    p.add_argument("--list-simplified", action="store_true")
    p.add_argument("--sample", action="store_true", help="run on a built-in example list")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if a.list_types:
        for k, (d, l) in TYPES.items():
            print(f"  {k:<26} Art 2(1){l} {d}")
        return 0
    if a.list_exemptions:
        for k, (d, ref, _) in EXEMPTIONS.items():
            print(f"  {k:<20} {d} [{ref}]")
        return 0
    if a.list_simplified:
        for k, (d, _) in SIMPLIFIED.items():
            print(f"  {k:<28} {d} [Art 16(1)]")
        return 0
    try:
        if a.sample:
            text = SAMPLE
        else:
            if not a.entities:
                p.print_usage(sys.stderr)
                print("error: give --entities or --sample", file=sys.stderr)
                return 3
            with open(a.entities, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
        out = run(text)
    except (OSError, ValueError, csv.Error) as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return EXIT[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
