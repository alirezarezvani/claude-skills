#!/usr/bin/env python3
"""payload_generator.py — build-sheet.json -> exact CMA API payloads.

Emits the four JSON payloads a launch needs, in order, under
./my-agent/payloads/: 01-environment.json, 02-agent.json, 03-session.json,
04-kickoff.json (a user.message event, optionally with user.define_outcome).
Deterministic; stdlib-only; NO network calls and NO API key handling.

Examples:
  payload_generator.py --sheet ./my-agent/build-sheet.json --out-dir ./my-agent
  payload_generator.py --sample
"""
import argparse
import json
import sys
from pathlib import Path


def gen(sheet: dict, kickoff_message: str):
    prim = sheet.get("primitives", {})
    agent = prim.get("agent", {})
    env = prim.get("environment", {})
    session = prim.get("session", {})
    outcome = prim.get("outcome")

    env_payload = {
        "config": {"type": env.get("type", "cloud")},
        "networking": {"mode": env.get("networking", "unrestricted")},
    }
    if env.get("networking") == "limited" and env.get("allowed_hosts"):
        env_payload["networking"]["allowed_hosts"] = env["allowed_hosts"]
    if env.get("packages"):
        env_payload["packages"] = env["packages"]

    agent_payload = {"name": sheet.get("agent_name", "agent"), "model": agent.get("model", "claude-opus-5")}
    if agent.get("system"):
        agent_payload["system"] = agent["system"]
    for k in ("tools", "mcp_servers", "skills", "multiagent", "description", "metadata"):
        if agent.get(k):
            agent_payload[k] = agent[k]
    # permission-policy hint: agent toolset always_allow, mcp always_ask
    agent_payload["permission_policies"] = _permissions(agent)

    session_payload = {
        "environment_id": "${ENV_ID}",
        "agent": {"type": "agent", "id": "${AGENT_ID}"},
    }
    if session.get("resources"):
        session_payload["resources"] = session["resources"]
    if session.get("vault_ids"):
        session_payload["vault_ids"] = session["vault_ids"]
    if session.get("memory_stores"):
        session_payload["memory_stores"] = [
            {"type": "memory_store", **m} for m in session["memory_stores"]
        ]

    msg = kickoff_message or sheet.get("goal", "Begin the task.")
    kickoff = {"events": [{"type": "user.message", "content": msg}]}
    if outcome:
        kickoff["events"].append({
            "type": "user.define_outcome",
            "description": outcome.get("description", sheet.get("goal", "")),
            "rubric": outcome.get("rubric", ""),
            "max_iterations": int(outcome.get("max_iterations", 3)),
        })

    return {
        "01-environment.json": env_payload,
        "02-agent.json": agent_payload,
        "03-session.json": session_payload,
        "04-kickoff.json": kickoff,
    }


def _permissions(agent: dict):
    pols = []
    for t in agent.get("tools", []):
        ttype = t.get("type", "")
        if ttype.startswith("agent_toolset"):
            pols.append({"toolset": ttype, "policy": "always_allow"})
        elif ttype == "custom":
            pols.append({"tool": t.get("name", "custom"), "policy": "always_ask"})
    for s in agent.get("mcp_servers", []):
        pols.append({"mcp_server": s.get("name", s.get("url", "mcp")), "policy": "always_ask"})
    return pols


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate CMA API payloads from a build sheet.")
    ap.add_argument("--sheet", help="Path to build-sheet.json.")
    ap.add_argument("--out-dir", default="./my-agent")
    ap.add_argument("--message", default=None, help="Override the kickoff user.message.")
    ap.add_argument("--json", action="store_true", help="Print all payloads instead of writing files.")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        sheet = json.loads((Path(__file__).resolve().parents[3] / "assets" / "example-build-sheet.json").read_text())
        payloads = gen(sheet, None)
        print(json.dumps(payloads, indent=2))
        return 0

    if not args.sheet:
        print("Provide --sheet path.", file=sys.stderr)
        return 2
    sheet = json.loads(Path(args.sheet).read_text())
    payloads = gen(sheet, args.message)
    if args.json:
        print(json.dumps(payloads, indent=2))
        return 0
    pdir = Path(args.out_dir) / "payloads"
    pdir.mkdir(parents=True, exist_ok=True)
    for name, body in payloads.items():
        (pdir / name).write_text(json.dumps(body, indent=2) + "\n")
    print(f"Wrote {len(payloads)} payloads to {pdir}/")
    for name in payloads:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
