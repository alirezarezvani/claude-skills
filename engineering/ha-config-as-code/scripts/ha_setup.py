#!/usr/bin/env python3
"""
ha_setup.py — Configure and connect to Home Assistant.

Interactive wizard to set up .env and validate the HA connection.

Usage:
    python3 ha_setup.py               # interactive wizard
    python3 ha_setup.py --check       # connection test only (CI-safe, no prompts)
    python3 ha_setup.py --json        # JSON output of connection result
"""

import argparse
import collections
import getpass
import json
import os
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from ha_api import HAAPI
except ImportError:
    sys.exit("ha_api.py must be in the same directory.")

try:
    from dotenv import load_dotenv, set_key
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False


# ---------------------------------------------------------------------------
# .env helpers
# ---------------------------------------------------------------------------

def _find_env_file() -> str:
    """Return path to .env file (CWD, then skill root), or CWD/.env if none found."""
    for candidate in [
        os.path.join(os.getcwd(), ".env"),
        os.path.join(_SCRIPT_DIR, "..", ".env"),
    ]:
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    return os.path.join(os.getcwd(), ".env")


def _read_env_file(path: str) -> dict:
    """Parse an .env file into a dict (simple key=value, ignores comments)."""
    result = {}
    if not os.path.exists(path):
        return result
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k, _, v = line.partition("=")
                result[k.strip()] = v.strip()
    return result


def _write_env_file(path: str, values: dict) -> None:
    """Write key=value pairs to .env (preserves existing lines, updates/adds keys)."""
    existing_lines = []
    if os.path.exists(path):
        with open(path) as f:
            existing_lines = f.readlines()

    updated_keys = set()
    new_lines = []
    for line in existing_lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and "=" in stripped:
            k = stripped.split("=", 1)[0].strip()
            if k in values:
                new_lines.append(f"{k}={values[k]}\n")
                updated_keys.add(k)
                continue
        new_lines.append(line if line.endswith("\n") else line + "\n")

    for k, v in values.items():
        if k not in updated_keys:
            new_lines.append(f"{k}={v}\n")

    with open(path, "w") as f:
        f.writelines(new_lines)


# ---------------------------------------------------------------------------
# Interactive wizard
# ---------------------------------------------------------------------------

def _prompt(label: str, default: str = "", secret: bool = False) -> str:
    if default:
        prompt_str = f"  {label} [{default}]: "
    else:
        prompt_str = f"  {label}: "

    if secret:
        value = getpass.getpass(prompt_str)
    else:
        value = input(prompt_str).strip()

    return value or default


def run_wizard(env_path: str) -> dict:
    """Interactive .env configuration wizard. Returns collected values."""
    print("\nHome Assistant — Setup Wizard")
    print("=" * 40)

    existing = _read_env_file(env_path)

    print(f"\n  .env location: {env_path}")
    if existing:
        print("  Existing values found — press Enter to keep them.\n")
    else:
        print()

    ha_url = _prompt(
        "HA internal URL (HA_URL)",
        default=existing.get("HA_URL", "http://192.168.1.100:8123"),
    )
    ha_external = _prompt(
        "HA external URL (HA_EXTERNAL_URL, optional)",
        default=existing.get("HA_EXTERNAL_URL", ""),
    )
    ha_token = _prompt(
        "Long-lived access token (HA_TOKEN)",
        default=existing.get("HA_TOKEN", ""),
        secret=True,
    )

    values = {"HA_URL": ha_url, "HA_TOKEN": ha_token}
    if ha_external:
        values["HA_EXTERNAL_URL"] = ha_external

    # Optional SSH vars
    print("\n  SSH access (only needed for setup_weather_forecast.py — press Enter to skip)")
    ssh_host = _prompt("HA SSH host (HA_SSH_HOST)", default=existing.get("HA_SSH_HOST", ""))
    if ssh_host:
        values["HA_SSH_HOST"] = ssh_host
        values["HA_SSH_USER"] = _prompt(
            "SSH user (HA_SSH_USER)", default=existing.get("HA_SSH_USER", "hassio")
        )
        values["HA_SSH_PASSWORD"] = _prompt(
            "SSH password (HA_SSH_PASSWORD)", default=existing.get("HA_SSH_PASSWORD", ""), secret=True
        )

    return values


# ---------------------------------------------------------------------------
# Connection test
# ---------------------------------------------------------------------------

def test_connection(verbose: bool = True) -> dict:
    """
    Test HA connection using current env vars.
    Returns a result dict with keys: success, url, version, location, entity_counts, error.
    """
    api = HAAPI()
    result = {
        "success": False,
        "url": api.base_url,
        "version": None,
        "location": None,
        "entity_counts": {},
        "error": None,
    }

    if not api.token:
        result["error"] = "HA_TOKEN is not set"
        return result

    if verbose:
        print(f"\n  Connecting to {api.base_url} …", end=" ", flush=True)

    try:
        ok = api.ping()
        if not ok:
            result["error"] = "API ping failed — token may be invalid or HA unreachable"
            if verbose:
                print("FAILED")
            return result

        cfg = api.get_config()
        result["version"] = cfg.get("version", "unknown")
        result["location"] = cfg.get("location_name", "Home")

        states = api.get_states()
        counts: dict = collections.Counter(
            s["entity_id"].split(".")[0] for s in states
        )
        result["entity_counts"] = dict(counts.most_common())
        result["success"] = True

        if verbose:
            print("OK")

    except Exception as e:
        result["error"] = str(e)
        if verbose:
            print("FAILED")

    return result


def print_connection_summary(result: dict) -> None:
    if not result["success"]:
        print(f"\n  [✗] Connection failed: {result['error']}")
        print(f"      URL: {result['url']}")
        print("\n  Troubleshooting:")
        print("    • Check HA_URL points to a running HA instance")
        print("    • Verify HA_TOKEN is a valid Long-Lived Access Token")
        print("    • Ensure the machine can reach the HA host")
        return

    total = sum(result["entity_counts"].values())
    top = sorted(result["entity_counts"].items(), key=lambda x: -x[1])[:8]

    print(f"\n  [✓] Connected to: {result['location']}  (HA {result['version']})")
    print(f"      URL: {result['url']}")
    print(f"\n  Entities: {total} total")
    for domain, count in top:
        bar = "█" * min(count, 30)
        print(f"    {domain:<18} {count:>4}  {bar}")
    if len(result["entity_counts"]) > 8:
        remaining = len(result["entity_counts"]) - 8
        print(f"    … and {remaining} more domains")

    print()
    print("  Next steps:")
    print("    python3 scripts/ha_entity_lister.py --domain light")
    print("    python3 scripts/ha_config_validator.py")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Configure and connect to Home Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Test connection only — no prompts (CI-safe)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output connection result as JSON",
    )
    args = parser.parse_args()

    env_path = _find_env_file()

    if args.check:
        # Non-interactive: load .env if present, then test
        if HAS_DOTENV and os.path.exists(env_path):
            load_dotenv(env_path)
        result = test_connection(verbose=not args.json)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_connection_summary(result)
        sys.exit(0 if result["success"] else 1)

    # Interactive wizard
    values = run_wizard(env_path)

    print(f"\n  Writing {env_path} …", end=" ")
    _write_env_file(env_path, values)
    print("done")

    # Reload env from the file we just wrote
    if HAS_DOTENV:
        load_dotenv(env_path, override=True)
    else:
        for k, v in values.items():
            os.environ[k] = v

    result = test_connection(verbose=True)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_connection_summary(result)

    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
