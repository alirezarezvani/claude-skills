#!/usr/bin/env python3
"""deployment_builder.py — build a POST /v1/deployments payload (the recurring loop).

A scheduled deployment fires a fresh session on a POSIX-cron cadence ("run without
you"). initial_events MUST include a user.message; it MAY also carry a
user.define_outcome so each firing self-grades (the nested loop). Emits the
deployment payload + a BYOK curl snippet to create it and to test it once via the
manual `run` endpoint. Stdlib-only; no network calls and no key handling.

Examples:
  deployment_builder.py --sheet ./my-agent/build-sheet.json --nest-outcome --out ./my-agent/payloads/deployment.json
  deployment_builder.py --name nightly --agent-id agent_123 --env-id env_456 \
     --message "Run the audit" --cron "0 2 * * *" --timezone UTC
  deployment_builder.py --sample
"""
import argparse
import json
import sys
from pathlib import Path

# reuse cron validation from the sibling tool
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import cron_validator  # type: ignore
except ImportError:
    cron_validator = None


def build(name, agent_ref, env_id, message, cron, timezone, outcome):
    initial_events = [{"type": "user.message", "content": message}]
    if outcome:
        initial_events.append(outcome if outcome.get("type") == "user.define_outcome"
                              else {"type": "user.define_outcome", **outcome})
    payload = {
        "name": name,
        "agent": agent_ref,
        "environment_id": env_id,
        "initial_events": initial_events,
        "schedule": {"type": "cron", "expression": cron, "timezone": timezone or "UTC"},
    }
    return payload


def curl_snippet(name):
    return (
        "# Create the deployment (reads $ANTHROPIC_API_KEY from your env; never paste the key):\n"
        "curl -sS -X POST \"$ANTHROPIC_BASE_URL/v1/deployments\" \\\n"
        "  -H \"x-api-key: $ANTHROPIC_API_KEY\" -H \"anthropic-version: 2023-06-01\" \\\n"
        "  -H \"anthropic-beta: managed-agents-2026-04-01\" -H \"content-type: application/json\" \\\n"
        f"  -d @./my-agent/payloads/deployment.json\n"
        "# Test it ONCE before trusting the schedule (manual run):\n"
        "curl -sS -X POST \"$ANTHROPIC_BASE_URL/v1/deployments/$DEPL_ID/run\" \\\n"
        "  -H \"x-api-key: $ANTHROPIC_API_KEY\" -H \"anthropic-version: 2023-06-01\" \\\n"
        "  -H \"anthropic-beta: managed-agents-2026-04-01\"\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a POST /v1/deployments payload (recurring cron loop).")
    ap.add_argument("--sheet", help="build-sheet.json (reads agent_name, goal, outcome, deployment.schedule).")
    ap.add_argument("--name")
    ap.add_argument("--agent-id", help="agent_... id (or use --agent-version to pin).")
    ap.add_argument("--agent-version", type=int, default=None)
    ap.add_argument("--env-id")
    ap.add_argument("--message")
    ap.add_argument("--cron")
    ap.add_argument("--timezone", default="UTC")
    ap.add_argument("--nest-outcome", action="store_true", help="Include the outcome so each firing self-grades.")
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        sheet = json.loads((Path(__file__).resolve().parents[3] / "assets" / "example-build-sheet.json").read_text())
        oc = sheet["primitives"].get("outcome")
        sched = sheet["primitives"].get("deployment", {}).get("schedule", {})
        payload = build(sheet["agent_name"] + "-nightly",
                        {"type": "agent", "id": "agent_EXAMPLE"}, "env_EXAMPLE",
                        sheet["goal"], sched.get("expression", "0 9 * * *"),
                        sched.get("timezone", "UTC"),
                        {"type": "user.define_outcome", **oc} if oc else None)
        print(json.dumps(payload, indent=2))
        print("\n" + curl_snippet(payload["name"]), file=sys.stderr)
        return 0

    name = args.name
    message = args.message
    cron = args.cron
    timezone = args.timezone
    outcome = None
    agent_ref = None

    if args.sheet:
        sheet = json.loads(Path(args.sheet).read_text())
        name = name or (sheet.get("agent_name", "agent") + "-scheduled")
        message = message or sheet.get("goal", "Run the task.")
        sched = sheet.get("primitives", {}).get("deployment", {}).get("schedule", {})
        cron = cron or sched.get("expression")
        timezone = timezone if args.timezone != "UTC" else sched.get("timezone", "UTC")
        if args.nest_outcome and sheet.get("primitives", {}).get("outcome"):
            oc = sheet["primitives"]["outcome"]
            outcome = {"type": "user.define_outcome", **oc}

    if args.agent_id:
        agent_ref = {"type": "agent", "id": args.agent_id}
        if args.agent_version is not None:
            agent_ref["version"] = args.agent_version
    elif agent_ref is None:
        agent_ref = {"type": "agent", "id": "${AGENT_ID}"}

    if not (name and message and cron):
        print("Need at least --name/--message/--cron (or a --sheet supplying them).", file=sys.stderr)
        return 2

    # validate cron before emitting
    if cron_validator:
        ok, errs = cron_validator.validate_cron(cron)
        tzok, _ = cron_validator.validate_tz(timezone)
        if not ok:
            print(f"ERROR: invalid cron {cron!r}: {errs}", file=sys.stderr)
            return 1
        if not tzok:
            print(f"WARN: timezone {timezone!r} may be invalid.", file=sys.stderr)

    payload = build(name, agent_ref, args.env_id or "${ENV_ID}", message, cron, timezone, outcome)
    text = json.dumps(payload, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n")
        print(f"Wrote {args.out}")
        print("\n" + curl_snippet(name), file=sys.stderr)
    if args.json or not args.out:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
