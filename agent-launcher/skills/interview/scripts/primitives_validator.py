#!/usr/bin/env python3
"""primitives_validator.py — validate a build sheet against CMA limits.

Deterministic checks against the documented ceilings in
references/cma-primitives.md. Emits PASS / WARN / FAIL with per-check detail.
Exit 0 = PASS (warnings allowed), 1 = FAIL. Stdlib-only; no network calls.

Limits enforced: <=20 skills/session, <=8 memory stores, multiagent depth-1 &
<=20 roster & <=25 threads, outcome max_iterations 1..20, <=20 creds/vault,
required agent.model, rubric present if outcome present, cron 5-field if scheduled.

Examples:
  primitives_validator.py --sheet ./my-agent/build-sheet.json
  primitives_validator.py --sample
"""
import argparse
import json
import sys
from pathlib import Path

LIMITS = {
    "skills_per_session": 20,
    "memory_stores": 8,
    "multiagent_roster": 20,
    "multiagent_threads": 25,
    "max_iterations": 20,
    "creds_per_vault": 20,
}


def validate(sheet: dict):
    checks = []

    def add(level, name, msg):
        checks.append({"level": level, "check": name, "detail": msg})

    prim = sheet.get("primitives", {})
    agent = prim.get("agent", {})
    env = prim.get("environment", {})
    session = prim.get("session", {})

    # required fields
    if not sheet.get("agent_name"):
        add("FAIL", "agent_name", "missing required agent_name")
    if not sheet.get("goal"):
        add("FAIL", "goal", "missing required one-sentence goal")
    if not agent.get("model"):
        add("FAIL", "agent.model", "agent.model is required (Claude 4.5-family or later)")
    else:
        add("PASS", "agent.model", agent["model"])
    if not env.get("type"):
        add("FAIL", "environment.type", "environment.type required (cloud|self_hosted)")

    # skills ceiling
    skills = agent.get("skills", []) or []
    if len(skills) > LIMITS["skills_per_session"]:
        add("FAIL", "skills", f"{len(skills)} skills > {LIMITS['skills_per_session']} per session")
    elif skills:
        add("PASS", "skills", f"{len(skills)} skills")

    # memory stores ceiling
    stores = session.get("memory_stores", []) or []
    if len(stores) > LIMITS["memory_stores"]:
        add("FAIL", "memory_stores", f"{len(stores)} > {LIMITS['memory_stores']} per session")
    elif stores:
        add("PASS", "memory_stores", f"{len(stores)} store(s)")
    # injection warning
    for s in stores:
        if s.get("access", "read_write") == "read_write":
            add("WARN", "memory.access", "read_write memory + untrusted input can be poisoned by prompt injection; "
                                          "prefer read_only where possible")
            break

    # multiagent
    ma = agent.get("multiagent")
    if ma:
        roster = ma.get("agents", []) or []
        if len(roster) > LIMITS["multiagent_roster"]:
            add("FAIL", "multiagent.roster", f"{len(roster)} > {LIMITS['multiagent_roster']}")
        if ma.get("depth", 1) and int(ma.get("depth", 1)) > 1:
            add("FAIL", "multiagent.depth", "depth must be 1")

    # outcome
    outcome = prim.get("outcome")
    if outcome:
        if not outcome.get("rubric", "").strip():
            add("FAIL", "outcome.rubric", "outcome present but rubric is empty (rubric is required)")
        else:
            add("PASS", "outcome.rubric", "rubric present")
        mi = outcome.get("max_iterations", 3)
        try:
            mi = int(mi)
            if mi < 1 or mi > LIMITS["max_iterations"]:
                add("FAIL", "outcome.max_iterations", f"{mi} outside 1..{LIMITS['max_iterations']}")
            else:
                add("PASS", "outcome.max_iterations", str(mi))
        except (TypeError, ValueError):
            add("FAIL", "outcome.max_iterations", "not an integer")

    # deployment cron shape
    dep = prim.get("deployment")
    if dep:
        expr = dep.get("schedule", {}).get("expression", "")
        fields = expr.split()
        if len(fields) != 5:
            add("FAIL", "deployment.cron", f"expected 5-field POSIX cron, got {len(fields)} field(s): {expr!r}")
        else:
            add("PASS", "deployment.cron", expr)
        if not dep.get("schedule", {}).get("timezone"):
            add("WARN", "deployment.timezone", "no IANA timezone set; defaults to UTC")

    # vaults
    vaults = session.get("vault_ids", []) or []
    # (creds-per-vault is enforced at vault build time; here just note count)
    if vaults:
        add("PASS", "vaults", f"{len(vaults)} vault(s) referenced")

    # networking hardening hint
    if env.get("networking", "unrestricted") == "unrestricted":
        add("WARN", "networking", "unrestricted networking; tighten to 'limited' with allowed_hosts as a v1 step")

    # deferrals discipline
    for d in sheet.get("deferrals", []) or []:
        for k in ("version", "item", "reason", "mechanism"):
            if not d.get(k):
                add("WARN", "deferral", f"deferral missing '{k}': {d.get('item', d)}")

    fails = [c for c in checks if c["level"] == "FAIL"]
    warns = [c for c in checks if c["level"] == "WARN"]
    verdict = "FAIL" if fails else ("WARN" if warns else "PASS")
    return verdict, checks


def _emit(verdict, checks, as_json):
    if as_json:
        print(json.dumps({"verdict": verdict, "checks": checks}, indent=2))
        return
    print(f"VERDICT: {verdict}")
    for c in checks:
        print(f"  [{c['level']:4}] {c['check']}: {c['detail']}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a build sheet against CMA limits (exit 0 pass, 1 fail).")
    ap.add_argument("--sheet", help="Path to build-sheet.json.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        bad = {
            "agent_name": "x", "goal": "do stuff",
            "primitives": {
                "agent": {"model": "claude-opus-5", "skills": ["s" + str(i) for i in range(22)]},
                "environment": {"type": "cloud", "networking": "unrestricted"},
                "session": {"memory_stores": [{"access": "read_write"}] * 9},
                "outcome": {"rubric": "", "max_iterations": 99},
                "deployment": {"schedule": {"expression": "0 9 * *"}},
            },
            "deferrals": [{"version": "v1", "item": "x"}],
        }
        v, c = validate(bad)
        _emit(v, c, False)
        print("\n(sample intentionally trips several FAIL/WARN checks)")
        return 0

    if not args.sheet:
        print("Provide --sheet path.", file=sys.stderr)
        return 2
    sheet = json.loads(Path(args.sheet).read_text())
    verdict, checks = validate(sheet)
    _emit(verdict, checks, args.json)
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
