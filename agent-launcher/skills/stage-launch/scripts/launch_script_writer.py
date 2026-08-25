#!/usr/bin/env python3
"""launch_script_writer.py — emit a resumable BYOK curl launch script.

Writes ./my-agent/launch.sh that creates environment -> agent -> session ->
kickoff in order, chaining IDs between steps. The script reads the key from
$ANTHROPIC_API_KEY at runtime; this generator NEVER accepts, prints, logs, or
writes an API key. Idempotent-ish: each step guards on whether its ID file
already exists so a re-run resumes rather than duplicates.

Stdlib-only; no network calls.

Examples:
  launch_script_writer.py --out-dir ./my-agent
  launch_script_writer.py --sample
"""
import argparse
import stat
import sys
from pathlib import Path

BASE_URL_DEFAULT = "https://api.anthropic.com"

TEMPLATE = r'''#!/usr/bin/env bash
# agent-launcher — resumable CMA launch (BYOK).
# Reads the key from the environment; NEVER hardcode it here.
#   export ANTHROPIC_API_KEY=sk-ant-...    # do NOT paste the key into chat
# Re-running resumes: each step skips if its *.id file already exists.
set -euo pipefail

BASE_URL="${{ANTHROPIC_BASE_URL:-{base_url}}}"
API_VERSION="${{ANTHROPIC_VERSION:-2023-06-01}}"
BETA="${{ANTHROPIC_BETA:-managed-agents-2026-04-01}}"
DIR="$(cd "$(dirname "$0")" && pwd)"
P="$DIR/payloads"

if [[ -z "${{ANTHROPIC_API_KEY:-}}" ]]; then
  echo "ERROR: export ANTHROPIC_API_KEY first (never paste it into chat)." >&2
  exit 1
fi

hdr=(-H "x-api-key: $ANTHROPIC_API_KEY"
     -H "anthropic-version: $API_VERSION"
     -H "anthropic-beta: $BETA"
     -H "content-type: application/json")

extract_id() {{ python3 -c 'import sys,json;print(json.load(sys.stdin).get("id",""))'; }}

# 1) Environment
if [[ -f "$DIR/env.id" ]]; then
  ENV_ID="$(cat "$DIR/env.id")"; echo "resume: env $ENV_ID"
else
  ENV_ID="$(curl -sS "${{hdr[@]}}" -X POST "$BASE_URL/v1/environments" -d @"$P/01-environment.json" | extract_id)"
  [[ -n "$ENV_ID" ]] || {{ echo "env create failed" >&2; exit 1; }}
  echo "$ENV_ID" > "$DIR/env.id"; echo "created env $ENV_ID"
fi

# 2) Agent
if [[ -f "$DIR/agent.id" ]]; then
  AGENT_ID="$(cat "$DIR/agent.id")"; echo "resume: agent $AGENT_ID"
else
  AGENT_ID="$(curl -sS "${{hdr[@]}}" -X POST "$BASE_URL/v1/agents" -d @"$P/02-agent.json" | extract_id)"
  [[ -n "$AGENT_ID" ]] || {{ echo "agent create failed" >&2; exit 1; }}
  echo "$AGENT_ID" > "$DIR/agent.id"; echo "created agent $AGENT_ID"
fi

# 3) Session (substitute env/agent ids into the payload)
if [[ -f "$DIR/session.id" ]]; then
  SESSION_ID="$(cat "$DIR/session.id")"; echo "resume: session $SESSION_ID"
else
  SESS_PAYLOAD="$(sed -e "s/\${{ENV_ID}}/$ENV_ID/g" -e "s/\${{AGENT_ID}}/$AGENT_ID/g" "$P/03-session.json")"
  SESSION_ID="$(printf '%s' "$SESS_PAYLOAD" | curl -sS "${{hdr[@]}}" -X POST "$BASE_URL/v1/sessions" -d @- | extract_id)"
  [[ -n "$SESSION_ID" ]] || {{ echo "session create failed" >&2; exit 1; }}
  echo "$SESSION_ID" > "$DIR/session.id"; echo "created session $SESSION_ID"
fi

# 4) Kickoff (send the first event(s))
echo "kickoff -> session $SESSION_ID"
curl -sS "${{hdr[@]}}" -X POST "$BASE_URL/v1/sessions/$SESSION_ID/events" -d @"$P/04-kickoff.json" >/dev/null
echo "launched. watch: $BASE_URL/v1/sessions/$SESSION_ID/stream"
echo "Console: https://platform.claude.com/  (agent $AGENT_ID / session $SESSION_ID)"
'''


def render(base_url: str) -> str:
    return TEMPLATE.format(base_url=base_url)


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit a resumable BYOK curl launch script (never handles the key).")
    ap.add_argument("--out-dir", default="./my-agent")
    ap.add_argument("--base-url", default=BASE_URL_DEFAULT)
    ap.add_argument("--stdout", action="store_true")
    ap.add_argument("--sample", action="store_true")
    args = ap.parse_args()

    script = render(args.base_url)

    if args.sample or args.stdout:
        print(script)
        if args.sample:
            print("\n# NOTE: reads $ANTHROPIC_API_KEY at runtime; no key is embedded.", file=sys.stderr)
        return 0

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "launch.sh"
    dest.write_text(script)
    dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP)
    print(f"Wrote {dest} (chmod +x). Run: export ANTHROPIC_API_KEY=... && {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
