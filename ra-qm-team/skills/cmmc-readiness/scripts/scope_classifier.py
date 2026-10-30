#!/usr/bin/env python3
"""Sort an asset inventory into CMMC Level 2 asset categories and find the scoping gaps an assessor will.

Scope decides cost: every asset in the CMMC Assessment Scope is assessed or at
least documented, so a wrong category either inflates the assessment or fails
it. Categories and treatment follow 32 CFR 170.19(c), Tables 3 and 4.

Categories (decision order)
  SPECIALIZED          IoT, IIoT, OT, GFE, restricted information systems and test equipment that
                       can handle CUI: inventory, SSP, diagram, risk-based policy; SSP reviewed, not assessed
  OUT_OF_SCOPE (VDI)   a VDI client limited to keyboard, video and mouse data
  CUI_ASSET            processes, stores or transmits CUI: assessed against all 110 requirements
  SECURITY_PROTECTION  provides security functions to the scope (including an ESP holding only
                       Security Protection Data): assessed against the requirements it supports
  CRMA                 can, but is not intended to, handle CUI because of policy: SSP reviewed,
                       limited check possible
  OUT_OF_SCOPE         cannot handle CUI and protects nothing in scope: be ready to justify it

Findings
  NOT_IN_SSP / NOT_IN_INVENTORY  in-scope asset missing from the SSP or asset inventory      BLOCKER
  CSP_NOT_FEDRAMP                cloud provider holding CUI without FedRAMP Moderate or an
                                 equivalent body of evidence (DFARS 252.204-7012(b)(2)(ii)(D)) BLOCKER
  NOT_IN_DIAGRAM                 in-scope asset missing from the assessment-scope diagram   HIGH
  NO_POLICY                      CRMA or specialized asset with no policy that governs it   HIGH
  ESP_NO_CRM                     provider handling CUI or SPD with no customer responsibility matrix HIGH
  FEDRAMP_EQUIVALENT             CSP relying on equivalency: you must hold its evidence     MEDIUM
  SPD_PROVIDER_IN_SCOPE          provider holding only Security Protection Data: assessed as an SPA MEDIUM
  OOS_UNJUSTIFIED                out of scope but not separated and no justification given  MEDIUM

Inventory CSV columns
  asset, type, cui (yes|restricted|no), security_function (yes|no), separated (yes|no),
  in_inventory, in_ssp, in_diagram (yes|no), policy_ref, justification,
  provider, provider_is_csp (yes|no), provider_data (cui|spd|none),
  fedramp (moderate|high|equivalent|none|unknown), crm (yes|no), vdi_kvm_only (yes|no)
  type: endpoint, server, network, saas, iaas, iot, iiot, ot, gfe, ris, test_equipment, vdi_client, other
  cui=restricted means the asset can handle CUI but policy keeps CUI off it (the CRMA test).

Deterministic, stdlib only, no network. Not a scoping decision: the C3PAO
agrees the scope at the start of the assessment.

Exit codes:
    0  CLEAN
    2  FINDINGS (no blockers)
    3  invalid input
    4  BLOCKED
"""

import argparse
import csv
import io
import json
import sys

SPECIALIZED_TYPES = {"iot", "iiot", "ot", "gfe", "ris", "test_equipment"}
TYPES = SPECIALIZED_TYPES | {"endpoint", "server", "network", "saas", "iaas", "vdi_client", "other"}
TREATMENT = {
    "CUI_ASSET": "Assessed against all Level 2 requirements; in inventory, SSP and scope diagram.",
    "SECURITY_PROTECTION": "Assessed against the requirements relevant to the security capability it provides.",
    "CRMA": "Documented in inventory, SSP and diagram; SSP reviewed, assessor may run a limited check.",
    "SPECIALIZED": "Documented in inventory, SSP and diagram, managed under risk-based policy; not assessed against other requirements.",
    "OUT_OF_SCOPE": "Not assessed; be ready to show it cannot process, store or transmit CUI.",
}
SEVERITY_ORDER = {"BLOCKER": 0, "HIGH": 1, "MEDIUM": 2}

SAMPLE = """asset,type,cui,security_function,separated,in_inventory,in_ssp,in_diagram,policy_ref,justification,provider,provider_is_csp,provider_data,fedramp,crm,vdi_kvm_only
eng-ws-01,endpoint,yes,no,no,yes,yes,yes,,,,,,,,
eng-ws-02,endpoint,yes,no,no,yes,no,yes,,,,,,,,
fileserver-cui,server,yes,no,no,yes,yes,yes,,,,,,,,
m365-gcc-high,saas,yes,no,no,yes,yes,yes,,,Microsoft,yes,cui,high,yes,
cad-vault,saas,yes,no,no,yes,yes,no,,,VaultCo,yes,cui,none,no,
siem,saas,no,yes,no,yes,yes,yes,,,LogCo,yes,spd,equivalent,yes,
edr-console,server,no,yes,no,yes,yes,yes,,,,,,,,
hr-laptop-07,endpoint,restricted,no,no,yes,yes,yes,,,,,,,,
cmm-machine,test_equipment,yes,no,no,yes,yes,yes,POL-OT-02,,,,,,,
lobby-kiosk,endpoint,no,no,no,yes,no,no,,,,,,,,
vdi-thin-client,vdi_client,no,no,no,yes,no,no,,,,,,,,yes
"""


def yes(v):
    return (v or "").strip().lower() in ("yes", "y", "true", "1")


def classify(r):
    t, cui = r["type"], r["cui"]
    if t in SPECIALIZED_TYPES and cui in ("yes", "restricted"):
        return "SPECIALIZED"
    if t == "vdi_client" and yes(r.get("vdi_kvm_only")):
        return "OUT_OF_SCOPE"
    if cui == "yes":
        return "CUI_ASSET"
    if yes(r.get("security_function")) or (r.get("provider_data") or "").strip().lower() == "spd":
        return "SECURITY_PROTECTION"
    if cui == "restricted":
        return "OUT_OF_SCOPE" if yes(r.get("separated")) else "CRMA"
    return "OUT_OF_SCOPE"


def analyse(text):
    reader = csv.DictReader(io.StringIO(text))
    need = {"asset", "type", "cui"}
    if not reader.fieldnames or not need <= set(reader.fieldnames):
        raise ValueError("inventory CSV needs at least columns asset, type, cui")
    assets, findings, seen = [], [], set()

    def add(sev, code, asset, detail):
        findings.append({"severity": sev, "code": code, "asset": asset, "detail": detail})

    for line, raw in enumerate(reader, start=2):
        r = {k: (v or "").strip() for k, v in raw.items() if k}
        name = r.get("asset", "")
        r["type"] = r.get("type", "").lower()
        r["cui"] = r.get("cui", "").lower()
        if not name:
            raise ValueError(f"line {line}: asset name is empty")
        if name in seen:
            raise ValueError(f"line {line}: asset '{name}' listed twice")
        seen.add(name)
        if r["type"] not in TYPES:
            raise ValueError(f"line {line}: type '{r['type']}' must be one of {', '.join(sorted(TYPES))}")
        if r["cui"] not in ("yes", "restricted", "no"):
            raise ValueError(f"line {line}: cui '{r['cui']}' must be yes, restricted or no")
        cat = classify(r)
        assets.append({"asset": name, "type": r["type"], "category": cat})
        in_scope = cat != "OUT_OF_SCOPE"
        if in_scope:
            if not yes(r.get("in_inventory")):
                add("BLOCKER", "NOT_IN_INVENTORY", name, "in-scope assets must be in the asset inventory (170.19(c), Table 3)")
            if not yes(r.get("in_ssp")):
                add("BLOCKER", "NOT_IN_SSP", name, "document how this asset is treated in the SSP (170.19(c), Table 3; CA.L2-3.12.4)")
            if not yes(r.get("in_diagram")):
                add("HIGH", "NOT_IN_DIAGRAM", name, "show it on the CMMC Assessment Scope network diagram")
        if cat in ("CRMA", "SPECIALIZED") and not r.get("policy_ref"):
            add("HIGH", "NO_POLICY", name,
                "name the policy or procedure that keeps CUI off it (CRMA) or manages its risk (specialized); "
                "without it the assessor may assess it as a CUI asset")
        if cat == "OUT_OF_SCOPE" and r["type"] != "vdi_client" and not yes(r.get("separated")) and not r.get("justification"):
            add("MEDIUM", "OOS_UNJUSTIFIED", name,
                "write down why it cannot process, store or transmit CUI, or separate it physically or logically")
        pdata = (r.get("provider_data") or "").lower()
        if r.get("provider") and pdata in ("cui", "spd"):
            if not yes(r.get("crm")):
                add("HIGH", "ESP_NO_CRM", name,
                    f"{r['provider']}: the SSP, service description and customer responsibility matrix must show "
                    "who does what (170.19(c)(2))")
            fed = (r.get("fedramp") or "unknown").lower()
            if pdata == "cui" and yes(r.get("provider_is_csp")):
                if fed in ("none", "unknown", ""):
                    add("BLOCKER", "CSP_NOT_FEDRAMP", name,
                        f"{r['provider']} holds CUI without FedRAMP Moderate (or higher) authorization or an equivalent "
                        "body of evidence (DFARS 252.204-7012(b)(2)(ii)(D)); move the CUI or get the evidence")
                elif fed == "equivalent":
                    add("MEDIUM", "FEDRAMP_EQUIVALENT", name,
                        f"{r['provider']}: keep the 3PAO-assessed body of evidence with all controls met; "
                        "the contractor answers for it (DoD CIO memo, Dec 2023)")
            elif pdata == "spd":
                add("MEDIUM", "SPD_PROVIDER_IN_SCOPE", name,
                    f"{r['provider']} holds only Security Protection Data; it is assessed as a Security Protection Asset, "
                    "cloud or not, and whatever its FedRAMP status (170.19(c)(2), Table 4)")
    findings.sort(key=lambda f: SEVERITY_ORDER[f["severity"]])
    counts = {c: sum(1 for a in assets if a["category"] == c) for c in TREATMENT}
    if any(f["severity"] == "BLOCKER" for f in findings):
        verdict = "BLOCKED"
    elif findings:
        verdict = "FINDINGS"
    else:
        verdict = "CLEAN"
    return {"verdict": verdict, "assets_total": len(assets), "counts": counts,
            "in_scope": len(assets) - counts["OUT_OF_SCOPE"], "treatment": TREATMENT,
            "assets": assets, "findings": findings}


def render(out):
    lines = [f"CMMC Level 2 scope: {out['verdict']}   {out['in_scope']} of {out['assets_total']} asset(s) in scope"]
    for cat, n in out["counts"].items():
        if n:
            names = ", ".join(a["asset"] for a in out["assets"] if a["category"] == cat)
            lines.append(f"  {cat:<20} {n:>3}  {names}")
    if out["findings"]:
        lines.append("")
    for f in out["findings"]:
        lines.append(f"[{f['severity']}] {f['code']} {f['asset']}: {f['detail']}")
    lines.append("\nThe C3PAO agrees the final scope at the start of the assessment.")
    return "\n".join(lines)


EXIT = {"CLEAN": 0, "FINDINGS": 2, "BLOCKED": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 clean, 2 findings, 3 invalid input, 4 blocked.")
    p.add_argument("--inventory", help="asset inventory CSV")
    p.add_argument("--sample", action="store_true", help="run on a built-in example")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    try:
        if a.sample:
            text = SAMPLE
        elif a.inventory:
            with open(a.inventory, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
        else:
            p.print_usage(sys.stderr)
            print("error: give --inventory FILE or --sample", file=sys.stderr)
            return 3
        out = analyse(text)
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
