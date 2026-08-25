#!/usr/bin/env python3
"""interview_planner.py — map Phase-1 interview answers to a CMA primitives skeleton.

Deterministic mapping of the six intake slots (job, trigger, inputs, actions,
definition-of-done, recurrence) to an agent/environment/session/outcome/deployment
skeleton plus suggested v1/v2 deferrals. Implements references/interview-to-config.md.
Stdlib-only; no network calls.

Examples:
  interview_planner.py --job "Triage support email" --trigger schedule \
     --inputs "gmail,memory" --actions "label,draft" --dod "one label + grounded reason" \
     --recurrence daily --model claude-opus-5
  interview_planner.py --answers answers.json --json
  interview_planner.py --sample
"""
import argparse
import json
import sys
from pathlib import Path

TRIGGERS = {"ask", "on-demand", "event", "schedule"}
RECURRENCE = {"once", "on-request", "daily", "weekly", "hourly", "custom"}

# input token -> resource / server suggestion
INPUT_MAP = {
    "files": ("resource", {"type": "file"}),
    "file": ("resource", {"type": "file"}),
    "repo": ("resource", {"type": "repository"}),
    "repository": ("resource", {"type": "repository"}),
    "memory": ("memory", {"access": "read_write"}),
    "gmail": ("mcp", {"server": "gmail", "permission": "always_ask"}),
    "slack": ("mcp", {"server": "slack", "permission": "always_ask"}),
    "github": ("mcp", {"server": "github", "permission": "always_ask"}),
    "web": ("tool", {"type": "web_fetch"}),
}


def plan(job, trigger, inputs, actions, dod, recurrence, model, name):
    inputs = [i.strip().lower() for i in inputs if i.strip()]
    actions = [a.strip() for a in actions if a.strip()]

    agent = {
        "model": model,
        "system": job.strip(),
        "tools": [{"type": "agent_toolset_20260401"}],
        "mcp_servers": [],
        "skills": [],
    }
    session = {"resources": [], "vault_ids": [], "memory_stores": []}
    deferrals = []
    networking = "unrestricted"
    allowed_hosts = []

    for tok in inputs:
        kind, payload = INPUT_MAP.get(tok, (None, None))
        if kind == "resource":
            session["resources"].append(payload)
        elif kind == "memory":
            session["memory_stores"].append({**payload, "instructions": "Cross-session context."})
        elif kind == "mcp":
            # v0: mock as custom tool; v1: wire real MCP.
            agent["tools"].append({
                "type": "custom",
                "name": f"{payload['server']}_action",
                "description": f"MOCK {payload['server']} action for v0 (schema-true).",
                "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}},
            })
            deferrals.append({
                "version": "v1",
                "item": f"Real {payload['server']} via MCP",
                "reason": "OAuth/credential not registered yet",
                "mechanism": f"Register a vault cred for the {payload['server']} MCP server; replace the mock "
                             f"{payload['server']}_action custom tool with the real MCP toolset (always_ask).",
            })
        elif kind == "tool":
            if payload not in agent["tools"]:
                agent["tools"].append(payload)
            networking = "limited"  # web usually wants a host allowlist as a v1 hardening

    # actions that clearly defer (send/publish) stay human-in-loop in v0
    for a in actions:
        al = a.lower()
        if any(k in al for k in ("send", "publish", "post", "email out", "reply")):
            deferrals.append({
                "version": "v2",
                "item": f"Automate '{a}'",
                "reason": "Irreversible/outward action — keep human review in v0",
                "mechanism": f"Add a custom tool for '{a}' behind always_ask; promote to always_allow only after grading.",
            })

    outcome = None
    if dod:
        outcome = {
            "description": job.strip(),
            "rubric": _rubric_from_dod(dod),
            "max_iterations": 5,
        }

    deployment = None
    rec = (recurrence or "once").lower()
    if rec in ("daily", "weekly", "hourly", "custom") or trigger == "schedule":
        deployment = {"schedule": {"expression": _cron_for(rec), "timezone": "UTC"}}

    return {
        "agent_name": name or _slug(job),
        "goal": job.strip(),
        "primitives": {
            "agent": agent,
            "environment": {"type": "cloud", "networking": networking, "allowed_hosts": allowed_hosts, "packages": {}},
            "session": session,
            **({"outcome": outcome} if outcome else {}),
            **({"deployment": deployment} if deployment else {}),
        },
        "deferrals": deferrals,
        "eval_plan": {"success_criteria": _criteria_from_dod(dod), "held_back_cases": []},
        "_notes": {
            "trigger": trigger, "recurrence": rec,
            "loop_hint": "cron-loop" if deployment else ("grade-iterate" if outcome else "single-pass"),
        },
    }


def _rubric_from_dod(dod: str) -> str:
    parts = [p.strip() for p in dod.replace(";", ",").split(",") if p.strip()]
    if not parts:
        parts = [dod.strip()]
    return "\n".join(f"- {p}" for p in parts)


def _criteria_from_dod(dod):
    if not dod:
        return []
    return [p.strip() for p in dod.replace(";", ",").split(",") if p.strip()]


def _cron_for(rec: str) -> str:
    return {"daily": "0 9 * * *", "weekly": "0 8 * * 1", "hourly": "0 * * * *"}.get(rec, "0 9 * * *")


def _slug(text: str) -> str:
    s = "".join(c.lower() if c.isalnum() else "-" for c in text).strip("-")
    while "--" in s:
        s = s.replace("--", "-")
    return (s[:40] or "agent").strip("-")


def main() -> int:
    ap = argparse.ArgumentParser(description="Map interview answers to a CMA primitives skeleton + deferrals.")
    ap.add_argument("--job", help="One-sentence job the agent does.")
    ap.add_argument("--trigger", choices=sorted(TRIGGERS), default="ask")
    ap.add_argument("--inputs", default="", help="Comma list: files,repo,memory,gmail,slack,github,web")
    ap.add_argument("--actions", default="", help="Comma list of actions the agent takes.")
    ap.add_argument("--dod", default="", help="Definition of done (becomes the rubric).")
    ap.add_argument("--recurrence", choices=sorted(RECURRENCE), default="once")
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--name", default=None)
    ap.add_argument("--answers", help="JSON file with the same keys instead of flags.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", help="Write the plan JSON to this path.")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        p = plan("Triage overnight support email", "schedule", ["gmail", "memory"],
                 ["label", "reply"], "one label per email, grounded reason, no invented facts",
                 "daily", "claude-opus-5", "support-triage")
        print(json.dumps(p, indent=2))
        return 0

    if args.answers:
        data = json.loads(Path(args.answers).read_text())
        job = data.get("job", "")
        trigger = data.get("trigger", "ask")
        inputs = data.get("inputs", []) if isinstance(data.get("inputs"), list) else str(data.get("inputs", "")).split(",")
        actions = data.get("actions", []) if isinstance(data.get("actions"), list) else str(data.get("actions", "")).split(",")
        dod = data.get("dod", "")
        recurrence = data.get("recurrence", "once")
        model = data.get("model", "claude-opus-5")
        name = data.get("name")
    else:
        if not args.job:
            print("Provide --job (or --answers file).", file=sys.stderr)
            return 2
        job, trigger = args.job, args.trigger
        inputs = args.inputs.split(",")
        actions = args.actions.split(",")
        dod, recurrence, model, name = args.dod, args.recurrence, args.model, args.name

    p = plan(job, trigger, inputs, actions, dod, recurrence, model, name)
    out = json.dumps(p, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(out + "\n")
        print(f"Wrote plan to {args.out}")
    if args.json or not args.out:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
