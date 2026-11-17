#!/usr/bin/env python3
"""Say which EU cyber laws apply to an organisation and which reporting clocks one event starts.

One ransomware night can start four clocks with four recipients: NIS2 (24 h to
the CSIRT), DORA (4 h after classification to the financial supervisor), the
CRA (24 h to ENISA's Single Reporting Platform if your own product was the
way in) and GDPR (72 h to the data protection authority). Teams usually run
the one they know and miss the others. This router takes an organisation
profile and, optionally, an event, and returns every regime that applies, the
lex specialis rules between them, and every deadline with its recipient.

Regimes and rules
  NIS2   Directive (EU) 2022/2555: Annex I/II sector + medium or larger, or size-independent ground (Art 2)
  DORA   Regulation (EU) 2022/2554: financial entity types of Art 2(1)(a)-(t), ICT third-party providers (u)
         DORA is lex specialis to NIS2 Arts 21 and 23 for financial entities (NIS2 Art 4, recital 28)
  CRA    Regulation (EU) 2024/2847: manufacturer of a product with digital elements on the EU market;
         Article 14 reporting applies since 11 September 2026
  GDPR   Regulation (EU) 2016/679: personal data breach, Art 33 (authority) and Art 34 (data subjects)

Deadlines produced for an event (from awareness unless stated)
  NIS2 significant incident     early warning 24 h; notification 72 h; final report 1 month after notification
  DORA major ICT incident       initial 4 h after classification as major and no later than 24 h after
                                awareness; intermediate 72 h after the initial; final 1 month after the
                                last intermediate (Delegated Regulation (EU) 2025/301 Art 5)
  CRA exploited vulnerability   early warning 24 h; notification 72 h; final 14 days after a fix is available
  CRA severe incident           early warning 24 h; notification 72 h; final 1 month after notification
  GDPR personal data breach     authority 72 h unless unlikely to result in a risk; data subjects without
                                undue delay if high risk

Deterministic, stdlib only, no network. A routing aid, not legal advice: national transpositions and
the competent authority decide borderline cases.

Exit codes:
    0  routed, no event or every clock computed
    2  routed with open questions (a classification the router cannot make)
    3  invalid input
"""

import argparse
import datetime as dt
import json
import sys

NIS2_SECTORS = {
    "I": {"energy-electricity", "energy-district-heating", "energy-oil", "energy-gas", "energy-hydrogen",
          "transport-air", "transport-rail", "transport-water", "transport-road", "banking",
          "financial-market-infrastructure", "health", "drinking-water", "waste-water", "digital-infrastructure",
          "ict-service-management", "public-administration", "space"},
    "II": {"postal-courier", "waste-management", "chemicals", "food", "manufacturing-medical-devices",
           "manufacturing-electronics", "manufacturing-electrical", "manufacturing-machinery",
           "manufacturing-motor-vehicles", "manufacturing-other-transport", "digital-providers", "research"},
}
SIZE_INDEPENDENT = {"public-ecomms", "qtsp", "tsp", "tld-registry", "dns", "critical-entity", "public-admin-central",
                    "sole-provider", "disruption-impact", "critical-importance", "designated-essential"}
DORA_TYPES = {
    "credit-institution": "(a)", "payment-institution": "(b)", "aisp": "(c)", "e-money-institution": "(d)",
    "investment-firm": "(e)", "casp": "(f)", "csd": "(g)", "ccp": "(h)", "trading-venue": "(i)",
    "trade-repository": "(j)", "aifm": "(k)", "ucits-manco": "(l)", "drsp": "(m)", "insurer": "(n)",
    "insurance-intermediary": "(o)", "iorp": "(p)", "cra-agency": "(q)", "benchmark-administrator": "(r)",
    "crowdfunding": "(s)", "securitisation-repository": "(t)", "ict-tpp": "(u)",
}
H = dt.timedelta(hours=1)


def size_large_or_medium(staff, turnover, balance):
    if staff is None and (turnover is None or balance is None):
        return None
    if (staff is not None and staff >= 50) or (turnover and balance and turnover > 10 and balance > 10):
        return True
    return False


def add_month(t):
    import calendar
    y, m = (t.year + 1, 1) if t.month == 12 else (t.year, t.month + 1)
    return t.replace(year=y, month=m, day=min(t.day, calendar.monthrange(y, m)[1]))


def fmt(t):
    return t.astimezone(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC") if isinstance(t, dt.datetime) else t


def route(p):
    regimes, questions, clocks = [], [], []
    sector = p.get("sector") or "none"
    specials = set(p.get("special") or [])
    unknown = specials - SIZE_INDEPENDENT - {"domain-registrar", "public-admin-regional", "education", "ose-nis1"}
    if unknown:
        raise ValueError(f"unknown special flag(s): {', '.join(sorted(unknown))}")
    annex = "I" if sector in NIS2_SECTORS["I"] else "II" if sector in NIS2_SECTORS["II"] else None
    if sector != "none" and not annex:
        raise ValueError(f"unknown sector '{sector}'; use a key from nis2_scope_classifier.py --list-sectors or 'none'")
    dora_type = p.get("dora_type")
    if dora_type and dora_type not in DORA_TYPES:
        raise ValueError(f"unknown DORA entity type '{dora_type}'; one of {', '.join(DORA_TYPES)}")
    is_fin = bool(dora_type) and dora_type != "ict-tpp"

    big = size_large_or_medium(p.get("employees"), p.get("turnover_eur_m"), p.get("balance_eur_m"))
    nis2 = None
    if specials & SIZE_INDEPENDENT:
        nis2 = True
    elif annex and big:
        nis2 = True
    elif annex and big is None:
        questions.append("NIS2: give headcount or turnover and balance sheet (group-adjusted); the size cap decides scope (Art 2(1))")
    elif annex:
        nis2 = False
    if nis2:
        note = "risk management Art 21 and reporting Art 23 replaced by DORA (NIS2 Art 4, recital 28); national list and registration may still apply" if is_fin else "Art 20 governance, Art 21 measures, Art 23 reporting; run nis2_scope_classifier.py for the category"
        regimes.append({"regime": "NIS2", "law": "Directive (EU) 2022/2555", "applies": True, "note": note})
    if dora_type:
        if is_fin:
            regimes.append({"regime": "DORA", "law": "Regulation (EU) 2022/2554", "applies": True,
                            "note": f"financial entity Art 2(1){DORA_TYPES[dora_type]}; check Art 2(3) exclusions and Art 16 simplified framework with dora-readiness"})
        else:
            regimes.append({"regime": "DORA", "law": "Regulation (EU) 2022/2554", "applies": True,
                            "note": "ICT third-party service provider Art 2(1)(u): bound through Art 30 contract terms with financial-entity customers, and directly overseen only if designated critical (Art 31)"})
    if p.get("product_manufacturer"):
        regimes.append({"regime": "CRA", "law": "Regulation (EU) 2024/2847", "applies": True,
                        "note": "Article 14 reporting since 11 Sep 2026; Annex I and CE marking from 11 Dec 2027; medical devices, IVDs, vehicles and marine equipment are excluded (Art 2(2)-(4))"})
    if p.get("personal_data"):
        regimes.append({"regime": "GDPR", "law": "Regulation (EU) 2016/679", "applies": True,
                        "note": "personal data breach notification Arts 33-34"})

    ev = p.get("event")
    if ev:
        aware = ev.get("aware_at")
        t0 = dt.datetime.fromisoformat(aware.replace("Z", "+00:00")) if aware else None
        if t0 is not None and t0.tzinfo is None:
            raise ValueError("event aware_at needs a UTC offset")

        def at(delta):
            return fmt(t0 + delta) if t0 else f"awareness + {int(delta.total_seconds() // 3600)} h"

        services = ev.get("service_impact")
        if nis2 and not is_fin and services:
            clocks += [
                {"regime": "NIS2", "report": "early warning", "due": at(24 * H), "to": "national CSIRT or competent authority", "ref": "NIS2 Art 23(4)(a)", "condition": "if significant (Art 23(3); 2024/2690 Art 3 for digital providers)"},
                {"regime": "NIS2", "report": "incident notification", "due": at(24 * H if "tsp" in specials or "qtsp" in specials else 72 * H), "to": "national CSIRT or competent authority", "ref": "NIS2 Art 23(4)(b)", "condition": "if significant"},
                {"regime": "NIS2", "report": "final report", "due": "1 month after the notification", "to": "national CSIRT or competent authority", "ref": "NIS2 Art 23(4)(d)", "condition": "if significant"},
            ]
        if is_fin and services:
            clocks += [
                {"regime": "DORA", "report": "initial notification", "due": f"4 h after classification as major, at the latest {at(24 * H)}", "to": "financial competent authority", "ref": "DORA Art 19(4); 2025/301 Art 5(1)", "condition": "if major under 2024/1772 Art 8"},
                {"regime": "DORA", "report": "intermediate report", "due": "72 h after the initial notification", "to": "financial competent authority", "ref": "2025/301 Art 5(1)(b)", "condition": "if major"},
                {"regime": "DORA", "report": "final report", "due": "1 month after the last intermediate report", "to": "financial competent authority", "ref": "2025/301 Art 5(1)(c)", "condition": "if major"},
            ]
            if nis2:
                questions.append("DORA + NIS2: the Member State may require copies of DORA reports to the NIS2 CSIRT (DORA Art 19(1)); the weekend extension of 2025/301 Art 5(4) does not apply to NIS2 entities' initial and intermediate reports (Art 5(5))")
            if services and ev.get("clients_financial_interest"):
                clocks.append({"regime": "DORA", "report": "inform clients", "due": "without undue delay", "to": "affected clients", "ref": "DORA Art 19(3)", "condition": "major incident affecting clients' financial interests"})
        if p.get("product_manufacturer") and ev.get("own_product_exploited"):
            clocks += [
                {"regime": "CRA", "report": "early warning", "due": at(24 * H), "to": "CSIRT coordinator + ENISA via the Single Reporting Platform", "ref": "CRA Art 14(2)(a)/(4)(a)", "condition": "actively exploited vulnerability or severe incident in your product"},
                {"regime": "CRA", "report": "notification", "due": at(72 * H), "to": "CSIRT coordinator + ENISA via the Single Reporting Platform", "ref": "CRA Art 14(2)(b)/(4)(b)", "condition": ""},
                {"regime": "CRA", "report": "final report", "due": "14 days after a fix is available (vulnerability) or 1 month after the notification (incident)", "to": "CSIRT coordinator + ENISA", "ref": "CRA Art 14(2)(c)/(4)(c)", "condition": ""},
            ]
        if p.get("personal_data") and ev.get("personal_data_affected"):
            clocks += [
                {"regime": "GDPR", "report": "breach notification", "due": at(72 * H), "to": "lead supervisory authority", "ref": "GDPR Art 33(1)", "condition": "unless unlikely to result in a risk; a processor tells the controller without undue delay (Art 33(2))"},
                {"regime": "GDPR", "report": "inform data subjects", "due": "without undue delay", "to": "data subjects", "ref": "GDPR Art 34", "condition": "if likely to result in a high risk"},
            ]
        if ev.get("personal_data_affected") is None and p.get("personal_data"):
            questions.append("GDPR: was personal data affected? If yes, the 72-hour Art 33 clock runs in parallel")
        if not clocks:
            questions.append("event given, but no clock started: say whether services were impacted (service_impact), your own product was the vector (own_product_exploited) or personal data was affected")
    return {"verdict": "OPEN_QUESTIONS" if questions else "ROUTED", "regimes": regimes, "clocks": clocks, "questions": questions,
            "skills": [s for s, r in (("nis2-readiness", "NIS2"), ("dora-readiness", "DORA"), ("cra-readiness", "CRA"), ("gdpr-dsgvo-expert", "GDPR"))
                       if any(x["regime"] == r for x in regimes)]}


SAMPLE = {
    "name": "Nordbank AG (credit institution that also makes its own POS terminal)",
    "sector": "banking", "employees": 320, "turnover_eur_m": 95, "balance_eur_m": 140,
    "special": [], "dora_type": "credit-institution", "product_manufacturer": True, "personal_data": True,
    "event": {"aware_at": "2026-11-16T23:40:00+01:00", "service_impact": True, "own_product_exploited": True,
              "personal_data_affected": True, "clients_financial_interest": True},
}


def render(out, name):
    lines = [f"EU cyber regime routing: {out['verdict']}" + (f"  ({name})" if name else ""), ""]
    if not out["regimes"]:
        lines.append("  no NIS2, DORA, CRA or GDPR ground found from the profile")
    for r in out["regimes"]:
        lines.append(f"  {r['regime']:<5} {r['law']}: {r['note']}")
    if out["clocks"]:
        lines += ["", "Clocks started by the event (run them in parallel):"]
        for c in out["clocks"]:
            cond = f"  [{c['condition']}]" if c["condition"] else ""
            lines.append(f"  {c['regime']:<5} {c['report']:<22} due {c['due']}  -> {c['to']}  ({c['ref']}){cond}")
    for q in out["questions"]:
        lines.append(f"  OPEN  {q}")
    if out["skills"]:
        lines += ["", "Next: " + ", ".join(out["skills"])]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 routed, 2 open questions, 3 invalid input.")
    p.add_argument("--profile", dest="input_path", help="JSON profile (see --sample --json for the shape)")
    p.add_argument("--sector", help="NIS2 sector key or 'none'")
    p.add_argument("--employees", type=float)
    p.add_argument("--turnover-eur-m", type=float)
    p.add_argument("--balance-eur-m", type=float)
    p.add_argument("--special", default="", help="semicolon list of NIS2 special flags (qtsp;dns;critical-entity...)")
    p.add_argument("--dora-type", help=f"DORA entity type: {', '.join(DORA_TYPES)}")
    p.add_argument("--product-manufacturer", action="store_true", help="places products with digital elements on the EU market")
    p.add_argument("--personal-data", action="store_true", help="processes personal data")
    p.add_argument("--event-aware-at", help="awareness time of a live event, ISO 8601 with offset")
    p.add_argument("--service-impact", action="store_true", help="event disrupted or threatened your services")
    p.add_argument("--own-product-exploited", action="store_true", help="a vulnerability in your own product was exploited or the product's security was hit")
    p.add_argument("--personal-data-affected", choices=["yes", "no"], help="event affected personal data")
    p.add_argument("--sample", action="store_true", help="route a built-in example")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    try:
        if a.sample:
            prof = SAMPLE
        elif a.input_path:
            with open(a.input_path, encoding="utf-8") as fh:
                prof = json.load(fh)
        elif a.sector or a.dora_type or a.product_manufacturer or a.personal_data:
            prof = {"sector": a.sector or "none", "employees": a.employees, "turnover_eur_m": a.turnover_eur_m,
                    "balance_eur_m": a.balance_eur_m, "special": [s.strip() for s in a.special.split(";") if s.strip()],
                    "dora_type": a.dora_type, "product_manufacturer": a.product_manufacturer, "personal_data": a.personal_data}
            if a.event_aware_at or a.service_impact or a.own_product_exploited or a.personal_data_affected:
                prof["event"] = {"aware_at": a.event_aware_at, "service_impact": a.service_impact,
                                 "own_product_exploited": a.own_product_exploited,
                                 "personal_data_affected": None if a.personal_data_affected is None else a.personal_data_affected == "yes"}
        else:
            p.print_usage(sys.stderr)
            print("error: give --profile, profile flags or --sample", file=sys.stderr)
            return 3
        out = route(prof)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps({"profile": prof, **out}, indent=2) if a.output == "json" else render(out, prof.get("name")))
    return 2 if out["questions"] else 0


if __name__ == "__main__":
    sys.exit(main())
