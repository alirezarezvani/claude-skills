#!/usr/bin/env python3
"""payload_validator.py — pre-launch check of generated payloads.

Validates the four payloads in ./my-agent/payloads/ before you run launch.sh:
required fields present, IDs left as ${ENV_ID}/${AGENT_ID} placeholders (the
script substitutes them), kickoff includes a user.message, an outcome (if any)
has a non-empty rubric and max_iterations in 1..20, and — critically — that NO
payload or the launch script contains an embedded API key. Exit 0 pass, 1 fail.

Stdlib-only; no network calls.

Examples:
  payload_validator.py --dir ./my-agent
  payload_validator.py --sample
"""
import argparse
import json
import re
import sys
from pathlib import Path

KEY_PATTERNS = [re.compile(r"sk-ant-[A-Za-z0-9_\-]{10,}"), re.compile(r"x-api-key:\s*sk-")]
MAX_ITER = 20


def _fail(checks, name, msg):
    checks.append({"level": "FAIL", "check": name, "detail": msg})


def _ok(checks, name, msg):
    checks.append({"level": "PASS", "check": name, "detail": msg})


def _warn(checks, name, msg):
    checks.append({"level": "WARN", "check": name, "detail": msg})


def validate(directory: Path):
    checks = []
    pdir = directory / "payloads"
    files = ["01-environment.json", "02-agent.json", "03-session.json", "04-kickoff.json"]

    payloads = {}
    for f in files:
        p = pdir / f
        if not p.exists():
            _fail(checks, f, "payload missing")
            continue
        try:
            payloads[f] = json.loads(p.read_text())
            _ok(checks, f, "present + valid JSON")
        except json.JSONDecodeError as e:
            _fail(checks, f, f"invalid JSON: {e}")

    # env
    env = payloads.get("01-environment.json", {})
    if env and not env.get("config", {}).get("type"):
        _fail(checks, "env.config.type", "missing config.type")

    # agent
    agent = payloads.get("02-agent.json", {})
    if agent:
        if not agent.get("name"):
            _fail(checks, "agent.name", "missing name")
        if not agent.get("model"):
            _fail(checks, "agent.model", "missing model")
        else:
            _ok(checks, "agent.model", agent["model"])
        # permission discipline: any MCP server should be always_ask
        pols = {p.get("mcp_server"): p.get("policy") for p in agent.get("permission_policies", []) if p.get("mcp_server")}
        for server, pol in pols.items():
            if pol != "always_ask":
                _warn(checks, "permission", f"MCP server {server} not always_ask (got {pol})")

    # session: placeholders should be intact for the script to substitute
    session = payloads.get("03-session.json", {})
    raw_session = json.dumps(session)
    if session:
        if "${ENV_ID}" not in raw_session:
            _warn(checks, "session.env_id", "no ${ENV_ID} placeholder (already substituted? re-generate to be safe)")
        if "${AGENT_ID}" not in raw_session:
            _warn(checks, "session.agent_id", "no ${AGENT_ID} placeholder")

    # kickoff
    kickoff = payloads.get("04-kickoff.json", {})
    events = kickoff.get("events", []) if kickoff else []
    if not any(e.get("type") == "user.message" for e in events):
        _fail(checks, "kickoff.user_message", "kickoff must include a user.message event")
    else:
        _ok(checks, "kickoff.user_message", "present")
    for e in events:
        if e.get("type") == "user.define_outcome":
            if not (e.get("rubric") or "").strip():
                _fail(checks, "outcome.rubric", "define_outcome has empty rubric")
            mi = e.get("max_iterations", 3)
            try:
                mi = int(mi)
                if not (1 <= mi <= MAX_ITER):
                    _fail(checks, "outcome.max_iterations", f"{mi} outside 1..{MAX_ITER}")
                else:
                    _ok(checks, "outcome.max_iterations", str(mi))
            except (TypeError, ValueError):
                _fail(checks, "outcome.max_iterations", "not an integer")

    # KEY LEAK SCAN across payloads + launch.sh
    scan_targets = list(pdir.glob("*.json")) if pdir.exists() else []
    launch = directory / "launch.sh"
    if launch.exists():
        scan_targets.append(launch)
    leaked = []
    for t in scan_targets:
        try:
            text = t.read_text()
        except OSError:
            continue
        for pat in KEY_PATTERNS:
            if pat.search(text):
                # x-api-key: sk- in launch.sh header line with a literal key is a leak;
                # the templated $ANTHROPIC_API_KEY reference is fine.
                if "$ANTHROPIC_API_KEY" in text and pat.pattern.startswith("x-api-key"):
                    continue
                leaked.append(t.name)
    if leaked:
        _fail(checks, "key_leak", f"possible embedded API key in: {', '.join(sorted(set(leaked)))}")
    else:
        _ok(checks, "key_leak", "no embedded key found")

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
    ap = argparse.ArgumentParser(description="Validate generated payloads pre-launch (incl. API-key leak scan).")
    ap.add_argument("--dir", default="./my-agent", help="Folder containing payloads/ and launch.sh.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    if args.sample:
        import tempfile
        d = Path(tempfile.mkdtemp(prefix="al-payload-"))
        (d / "payloads").mkdir()
        (d / "payloads" / "01-environment.json").write_text('{"config":{"type":"cloud"},"networking":{"mode":"unrestricted"}}')
        (d / "payloads" / "02-agent.json").write_text('{"name":"a","model":"claude-opus-5","permission_policies":[]}')
        (d / "payloads" / "03-session.json").write_text('{"environment_id":"${ENV_ID}","agent":{"type":"agent","id":"${AGENT_ID}"}}')
        (d / "payloads" / "04-kickoff.json").write_text('{"events":[{"type":"user.message","content":"go"},{"type":"user.define_outcome","rubric":"- works","max_iterations":5}]}')
        v, c = validate(d)
        _emit(v, c, False)
        return 0

    v, c = validate(Path(args.dir))
    _emit(v, c, args.json)
    return 1 if v == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
