#!/usr/bin/env python3
"""oauth_triage — classify why an MCP connector lost authentication.

Reads a stored token record and (optionally) a connector event log, then reports
which of five failure classes the artifacts support: envelope mismatch, expiry
semantics, rotation clobber, binding fault, or poisoned negative cache.

Standard library only. No network calls. No secrets are printed.

Exit codes:
    0  no defect signals found
    1  suspect findings only
    2  a defect class is confirmed
"""

import argparse
import json
import sys
from datetime import datetime, timezone

SEVERITY_RANK = {"none": 0, "low": 1, "medium": 2, "high": 3}

SECRET_KEYS = {
    "access_token", "refresh_token", "id_token", "client_secret", "token",
    "password", "secret", "authorization", "api_key", "cookie",
}

# Keys a flat OAuth token record is expected to expose at the top level.
EXPECTED_FLAT_KEYS = ("access_token", "token_type", "expires_in", "expires_at",
                      "refresh_token", "scope")

# Log event names commonly emitted by MCP connector implementations.
EXCHANGE_EVENTS = {"exchange", "token_exchange", "refresh", "token_refresh",
                   "oauth_exchange", "oauth_refresh"}
STORE_EVENTS = {"store", "save", "persist", "write", "token_store"}
LOAD_EVENTS = {"load", "read", "get", "token_load"}
CALL_EVENTS = {"call", "tool_call", "invoke", "request", "http_call"}
ERROR_EVENTS = {"error", "fail", "failure", "denied", "unauthorized", "401", "403"}
NEEDS_AUTH_KEYS = {"needs_auth", "needsAuth", "needs_auth_cache", "auth_required",
                   "requires_auth", "reauth_required"}


def redact(value, depth=0):
    """Return a copy of value with secret-looking leaves replaced."""
    if depth > 12:
        return "<max-depth>"
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            if key.lower() in SECRET_KEYS:
                out[key] = "<redacted:{}>".format(type(item).__name__)
            else:
                out[key] = redact(item, depth + 1)
        return out
    if isinstance(value, list):
        return [redact(item, depth + 1) for item in value]
    return value


def load_json(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path):
    events = []
    with open(path, "r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except ValueError:
                events.append({"parse_error": True, "line": lineno, "raw_len": len(line)})
    return events


def parse_ts(value):
    """Best-effort timestamp parse returning POSIX seconds or None."""
    if isinstance(value, (int, float)):
        # Treat very large values as milliseconds.
        return float(value) / 1000.0 if value > 1e11 else float(value)
    if not isinstance(value, str):
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def event_name(event):
    for key in ("event", "type", "action", "name", "kind"):
        value = event.get(key)
        if isinstance(value, str):
            return value.strip().lower()
    return ""


def find_token_envelope(record):
    """Return (envelope_key, inner_dict) when the token lives one level down."""
    if not isinstance(record, dict):
        return None, None
    if "access_token" in record:
        return None, None
    for key, value in record.items():
        if isinstance(value, dict) and "access_token" in value:
            return key, value
    return None, None


def check_envelope(record, expect_flat):
    findings = []
    key, inner = find_token_envelope(record)
    if key is not None:
        findings.append({
            "class": "envelope_mismatch",
            "severity": "high",
            "evidence": "token sits under nested key '{}'; a flat reader sees no access_token".format(key),
        })
    if isinstance(record, dict):
        present = set(record.keys())
        missing = [k for k in EXPECTED_FLAT_KEYS if k not in present]
        if key is not None and inner:
            inner_missing = [k for k in EXPECTED_FLAT_KEYS if k not in set(inner.keys())]
            missing = inner_missing
        if expect_flat and missing and "access_token" not in present and key is None:
            findings.append({
                "class": "envelope_mismatch",
                "severity": "high",
                "evidence": "record has no access_token and is missing: {}".format(", ".join(missing)),
            })
    return findings


def check_expiry(record, expect_absolute):
    findings = []
    target = record
    key, inner = find_token_envelope(record)
    if inner is not None:
        target = inner
    if not isinstance(target, dict):
        return findings

    expires_in = target.get("expires_in")
    expires_at = target.get("expires_at")

    if isinstance(expires_in, float) and not expires_in.is_integer():
        findings.append({
            "class": "expiry_semantics",
            "severity": "medium",
            "evidence": "expires_in is fractional ({!r}); integer-only readers truncate it".format(expires_in),
        })
    if isinstance(expires_in, str):
        findings.append({
            "class": "expiry_semantics",
            "severity": "medium",
            "evidence": "expires_in is a string ({!r}); arithmetic on it depends on coercion".format(expires_in),
        })
    if expires_at is not None and not isinstance(expires_at, (int, float)):
        findings.append({
            "class": "expiry_semantics",
            "severity": "medium",
            "evidence": "expires_at is not numeric ({})".format(type(expires_at).__name__),
        })
    if isinstance(expires_at, (int, float)) and expires_at == 0:
        findings.append({
            "class": "expiry_semantics",
            "severity": "high",
            "evidence": "expires_at is 0; falsy-expiry readers treat this as 'never expires'",
        })
    if expires_at is None and expires_in is not None and expect_absolute:
        findings.append({
            "class": "expiry_semantics",
            "severity": "low",
            "evidence": "record stores only a relative TTL; caller asked for an absolute expiry",
        })
    if isinstance(expires_at, (int, float)) and expires_at > 1e11:
        findings.append({
            "class": "expiry_semantics",
            "severity": "low",
            "evidence": "expires_at looks like milliseconds ({}); readers assuming seconds will see a far-future token".format(expires_at),
        })
    return findings


def check_rotation(record, events):
    findings = []
    timed = []
    for event in events:
        name = event_name(event)
        if name in EXCHANGE_EVENTS:
            stamp = None
            for key in ("ts", "time", "timestamp", "at", "date"):
                stamp = parse_ts(event.get(key))
                if stamp is not None:
                    break
            timed.append((stamp, event))

    timed.sort(key=lambda pair: (pair[0] is None, pair[0] or 0.0))

    rapid = 0
    for index in range(1, len(timed)):
        previous = timed[index - 1][0]
        current = timed[index][0]
        if previous is not None and current is not None and (current - previous) <= 60:
            rapid += 1
    if rapid:
        findings.append({
            "class": "rotation_clobber",
            "severity": "high",
            "evidence": "{} exchange(s) within 60s of the previous one; concurrent refreshers rotate each other's token".format(rapid),
        })

    last_returned = None
    for event in events:
        result = event.get("result") or event.get("response") or {}
        if isinstance(result, dict) and isinstance(result.get("refresh_token"), str):
            last_returned = result["refresh_token"]

    stored = None
    target = record
    key, inner = find_token_envelope(record)
    if inner is not None:
        target = inner
    if isinstance(target, dict) and isinstance(target.get("refresh_token"), str):
        stored = target["refresh_token"]

    if last_returned is not None and stored is not None:
        same = last_returned == stored
        if not same:
            findings.append({
                "class": "rotation_clobber",
                "severity": "high",
                "evidence": "stored refresh_token does not match the most recent exchange result ({} vs {} chars)".format(len(stored), len(last_returned)),
            })
        if same:
            findings.append({
                "class": "rotation_clobber",
                "severity": "none",
                "evidence": "stored refresh_token matches the most recent exchange result",
            })

    unpaired_stores = 0
    for event in events:
        name = event_name(event)
        if name in STORE_EVENTS and not isinstance(event.get("refresh_token"), str):
            unpaired_stores += 1
    if unpaired_stores and (rapid or (last_returned is not None and stored != last_returned)):
        findings.append({
            "class": "rotation_clobber",
            "severity": "medium",
            "evidence": "{} store event(s) carry no refresh_token payload, so a clobbering writer cannot be distinguished from a correct one".format(unpaired_stores),
        })
    return findings


def first_claim(record, names):
    target = record
    key, inner = find_token_envelope(record)
    if inner is not None:
        target = inner
    if not isinstance(target, dict):
        return None
    claims = target.get("claims")
    for container in (target, claims if isinstance(claims, dict) else {}):
        for name in names:
            value = container.get(name)
            if isinstance(value, str) and value:
                return value
    return None


def check_binding(record, expect_aud, expect_iss):
    findings = []
    if expect_aud:
        actual = first_claim(record, ("aud", "audience", "resource"))
        if actual is None:
            findings.append({
                "class": "binding_fault",
                "severity": "medium",
                "evidence": "record exposes no audience claim; cannot prove the token was minted for {}".format(expect_aud),
            })
        elif expect_aud not in actual:
            findings.append({
                "class": "binding_fault",
                "severity": "high",
                "evidence": "token audience {!r} does not cover the requested surface {!r}".format(actual, expect_aud),
            })
    if expect_iss:
        actual = first_claim(record, ("iss", "issuer"))
        if actual is not None and expect_iss not in actual:
            findings.append({
                "class": "binding_fault",
                "severity": "high",
                "evidence": "token issuer {!r} does not match expected issuer {!r}".format(actual, expect_iss),
            })

    target = record
    key, inner = find_token_envelope(record)
    if inner is not None:
        target = inner
    if isinstance(target, dict):
        identity_keys = ("email", "account_email", "user_email", "username", "login")
        used = [k for k in identity_keys if isinstance(target.get(k), str)]
        has_stable = isinstance(target.get("account_id"), str) or isinstance(target.get("sub"), str)
        if used and not has_stable:
            findings.append({
                "class": "binding_fault",
                "severity": "medium",
                "evidence": "credentials keyed on {} with no stable account identifier; multi-account installs collide".format("/".join(used)),
            })
    return findings


def collect_needs_auth_keys(value, prefix="", depth=0):
    found = []
    if depth > 8:
        return found
    if isinstance(value, dict):
        for key, item in value.items():
            path = "{}.{}".format(prefix, key) if prefix else key
            if key in NEEDS_AUTH_KEYS or key.lower() in {k.lower() for k in NEEDS_AUTH_KEYS}:
                found.append((path, item))
            found.extend(collect_needs_auth_keys(item, path, depth + 1))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(collect_needs_auth_keys(item, "{}[{}]".format(prefix, index), depth + 1))
    return found


def check_negative_cache(record, events):
    findings = []
    for path, value in collect_needs_auth_keys(record):
        if value:
            findings.append({
                "class": "negative_cache",
                "severity": "medium",
                "evidence": "record carries a live auth marker at '{}'; confirm it is scoped to this credential".format(path),
            })

    marker_seen = False
    success_after_marker = False
    cleared = False
    for event in events:
        name = event_name(event)
        if name in ("needs_auth", "auth_required", "reauth", "mark_needs_auth"):
            marker_seen = True
        if name in ("success", "ok", "connected", "authenticated"):
            if marker_seen:
                success_after_marker = True
        if name in ("clear_needs_auth", "unmark", "invalidate_cache"):
            cleared = True

    if marker_seen and success_after_marker and not cleared:
        findings.append({
            "class": "negative_cache",
            "severity": "high",
            "evidence": "a needs-auth marker was set and a later success followed it, but no clear event exists; the marker outlives the failure",
        })
    return findings


def build_verdict(findings):
    """Collapse raw findings into (primary_class, confidence, actionable_findings)."""
    real = [f for f in findings if SEVERITY_RANK.get(str(f.get("severity")), 0) >= 1]
    if not real:
        return "none", "none", []

    per_class = {}
    for finding in real:
        name = finding["class"]
        rank = SEVERITY_RANK.get(str(finding.get("severity")), 1)
        if name not in per_class or rank > per_class[name]:
            per_class[name] = rank

    primary = max(per_class.items(), key=lambda pair: pair[1])[0]
    confidence = "high" if per_class[primary] >= 3 else "medium"
    return primary, confidence, real


# Embedded rotation-clobber case for --sample: three concurrent exchanges, one
# store, and a stored refresh token that matches none of the issued ones.
SAMPLE_RECORD = {
    "access_token": "redacted-access",
    "expires_at": 4102444800,
    "refresh_token": "stale-refresh-token",
}
SAMPLE_EVENTS = [
    {"event": "exchange", "result": {"refresh_token": "new-token-one"}, "ts": 1793113193},
    {"event": "exchange", "result": {"refresh_token": "new-token-two"}, "ts": 1793113203},
    {"event": "exchange", "result": {"refresh_token": "newest-token-value"}, "ts": 1793113213},
    {"event": "store", "ts": 1793113223},
]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Classify why an MCP connector lost OAuth authentication.",
        epilog=(
            "Artifacts only: no network calls, no secrets printed.\n\n"
            "Examples:\n"
            "  oauth_triage.py --token-file token.json --log connector.jsonl\n"
            "  oauth_triage.py --token-file token.json --expect-flat --expect-absolute-expiry\n"
            "  oauth_triage.py --token-file token.json --redact\n"
            "  oauth_triage.py --sample --json"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--token-file", help="Path to the stored token record (JSON)")
    parser.add_argument("--log", help="Path to a connector event log (JSONL)")
    parser.add_argument("--redact", action="store_true",
                        help="Print the token record with secret values removed, then exit")
    parser.add_argument("--expect-absolute-expiry", action="store_true",
                        help="Flag records that store only a relative TTL")
    parser.add_argument("--expect-flat", action="store_true",
                        help="Require a flat top-level token record")
    parser.add_argument("--expect-aud", help="Audience or resource the failing surface advertises")
    parser.add_argument("--expect-iss", help="Issuer the failing surface advertises")
    parser.add_argument("--json", action="store_true", help="Emit a JSON verdict")
    parser.add_argument("--verbose", action="store_true", help="Print each finding as it is produced")
    parser.add_argument("--sample", action="store_true",
                        help="Classify an embedded rotation-clobber record and log; no files needed")
    args = parser.parse_args(argv)

    if args.sample:
        args.token_file, args.log = "<sample>", "<sample>"

    if not args.token_file and not args.log:
        parser.print_help()
        return 1

    record = {}
    events = []

    if args.sample:
        record, events = dict(SAMPLE_RECORD), list(SAMPLE_EVENTS)
    elif args.token_file:
        try:
            record = load_json(args.token_file)
        except (OSError, ValueError) as exc:
            print("cannot read token file: {}".format(exc), file=sys.stderr)
            return 2

    if args.redact:
        print(json.dumps(redact(record), indent=2, sort_keys=True))
        return 0

    if args.log and not args.sample:
        try:
            events = load_jsonl(args.log)
        except OSError as exc:
            print("cannot read log file: {}".format(exc), file=sys.stderr)
            return 2

    findings = []
    findings.extend(check_envelope(record, args.expect_flat))
    findings.extend(check_expiry(record, args.expect_absolute_expiry))
    findings.extend(check_rotation(record, events))
    findings.extend(check_binding(record, args.expect_aud, args.expect_iss))
    findings.extend(check_negative_cache(record, events))

    primary, confidence, real = build_verdict(findings)

    if primary == "none":
        exit_code = 0
    elif confidence == "high":
        exit_code = 2
    else:
        exit_code = 1

    if args.json:
        payload = {
            "primary_class": primary,
            "confidence": confidence,
            "findings": real,
            "next_probe": None if primary == "none" else next_probe_for(primary),
            "exit_code": exit_code,
            "artifacts": {
                "token_file": args.token_file,
                "log": args.log,
                "events": len(events),
            },
        }
        print(json.dumps(payload, indent=2))
    else:
        print("primary_class: {}".format(primary))
        print("confidence:    {}".format(confidence))
        for finding in real:
            print("  - [{}] {}: {}".format(finding.get("severity"), finding["class"], finding["evidence"]))
        if primary != "none":
            print("next_probe:    {}".format(next_probe_for(primary)))
        print("exit_code:     {}".format(exit_code))

    if args.verbose:
        for finding in findings:
            print("finding: {} ({})".format(finding["class"], finding.get("severity")), file=sys.stderr)

    return exit_code


def next_probe_for(primary):
    probes = {
        "envelope_mismatch": "Print the keys the reader requests next to the keys the record has; normalise on write and delete any second reader.",
        "expiry_semantics": "Compare elapsed time at first failure with the provider's token lifetime; store one absolute integer expiry and treat zero as expired.",
        "rotation_clobber": "Count concurrent refreshers; add a single-flight lock around exchange plus store, then re-check the stored refresh token.",
        "binding_fault": "Compare the token's aud/iss claims with the failing surface's protected-resource metadata; key credentials on a stable account id.",
        "negative_cache": "Clear only the needs-auth marker, retry with the same credentials, then scope the marker to the credential it describes.",
    }
    return probes.get(primary, "Collect a token record plus a connector event log.")


if __name__ == "__main__":
    sys.exit(main())
