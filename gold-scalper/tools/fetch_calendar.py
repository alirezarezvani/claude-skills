#!/usr/bin/env python3
"""Fetch the ForexFactory economic calendar and write config/calendar.json.

The engine's news blackout (core/engine.py:in_news_blackout) consumes a list of
{"time": "<ISO-8601 with offset>", "impact": "high"} and parses "time" with
datetime.fromisoformat, comparing against tz-aware UTC now — so every "time"
written here carries an explicit +00:00 offset.

Usage:
    python tools/fetch_calendar.py [--out config/calendar.json]
                                   [--currencies USD,EUR,GBP]
                                   [--min-impact high] [--dry-run]
                                   [--from-file path.json]

Exit codes: 0 ok, 2 all sources failed (existing calendar.json left untouched).
"""

import argparse
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

FEED_URLS = [
    ("this week", "https://nfs.faireconomy.media/ff_calendar_thisweek.json"),
    ("next week", "https://nfs.faireconomy.media/ff_calendar_nextweek.json"),
]
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")
TIMEOUT = 15
IMPACT_RANK = {"high": 3, "medium": 2, "low": 1}
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def warn(msg: str) -> None:
    print(f"warning: {msg}", file=sys.stderr)


def fetch_feed(label: str, url: str) -> list | None:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.load(resp)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            OSError, json.JSONDecodeError, ValueError) as e:
        warn(f"fetch failed for {label} ({url}): {e}")
        return None
    if not isinstance(data, list):
        warn(f"{label}: unexpected payload type {type(data).__name__}, expected list")
        return None
    return data


def normalize_event(raw: dict) -> dict | None:
    """FF feed item -> engine event, or None (with warning) on schema drift."""
    if not isinstance(raw, dict):
        warn(f"skipping non-object event: {raw!r:.80}")
        return None
    title = raw.get("title")
    country = raw.get("country")
    date_str = raw.get("date")
    impact = raw.get("impact")
    if not all(isinstance(v, str) and v for v in (title, country, date_str, impact)):
        warn(f"skipping event with missing/invalid fields: "
             f"title={title!r} country={country!r} date={date_str!r} impact={impact!r}")
        return None
    try:
        t = datetime.fromisoformat(date_str)
    except ValueError:
        warn(f"skipping {title!r}: unparseable date {date_str!r}")
        return None
    if t.tzinfo is None:
        warn(f"skipping {title!r}: date {date_str!r} has no timezone offset")
        return None
    return {
        "time": t.astimezone(timezone.utc).isoformat(),
        "impact": impact.strip().lower(),
        "title": title,
        "currency": country.strip().upper(),
    }


def collect(feeds: list[list], currencies: set[str], min_impact: str) -> list[dict]:
    min_rank = IMPACT_RANK[min_impact]
    seen = set()
    events = []
    for feed in feeds:
        for raw in feed:
            ev = normalize_event(raw)
            if ev is None:
                continue
            if ev["currency"] not in currencies:
                continue
            if IMPACT_RANK.get(ev["impact"], 0) < min_rank:
                continue
            key = (ev["time"], ev["currency"], ev["title"])
            if key in seen:
                continue
            seen.add(key)
            events.append(ev)
    events.sort(key=lambda e: e["time"])
    return events


def atomic_write(path: Path, events: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def describe_delta(now: datetime, then: datetime) -> str:
    secs = (then - now).total_seconds()
    sign = "in " if secs >= 0 else ""
    suffix = "" if secs >= 0 else " ago"
    secs = abs(secs)
    days, rem = divmod(int(secs), 86400)
    hours, rem = divmod(rem, 3600)
    minutes = rem // 60
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return f"{sign}{' '.join(parts)}{suffix}"


def summarize(events: list[dict], now: datetime) -> None:
    upcoming_high = [e for e in events
                     if e["impact"] == "high" and datetime.fromisoformat(e["time"]) > now]
    if upcoming_high:
        nxt = upcoming_high[0]
        when = datetime.fromisoformat(nxt["time"])
        print(f"next high-impact: {nxt['title']} ({nxt['currency']}) at "
              f"{nxt['time']} ({describe_delta(now, when)})")
    else:
        print("no upcoming high-impact events in the fetched window")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Fetch ForexFactory calendar into the engine's calendar.json format.")
    ap.add_argument("--out", default=str(PROJECT_ROOT / "config" / "calendar.json"),
                    help="output path (default: <project>/config/calendar.json)")
    ap.add_argument("--currencies", default="USD",
                    help="comma-separated calendar currencies (default: USD — "
                         "gold's dominant driver; XAU is not a calendar currency)")
    ap.add_argument("--min-impact", default="high", choices=sorted(IMPACT_RANK),
                    help="minimum impact to keep (default: high — the engine only "
                         "blacks out 'high')")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the event table instead of writing")
    ap.add_argument("--from-file", metavar="PATH",
                    help="debug: parse a local FF-format JSON file instead of fetching")
    args = ap.parse_args()

    currencies = {c.strip().upper() for c in args.currencies.split(",") if c.strip()}
    if not currencies:
        print("error: --currencies is empty", file=sys.stderr)
        return 1
    out_path = Path(args.out)
    now = datetime.now(timezone.utc)

    feeds = []
    if args.from_file:
        try:
            feeds.append(json.loads(Path(args.from_file).read_text(encoding="utf-8")))
        except (OSError, json.JSONDecodeError) as e:
            print(f"error: cannot read {args.from_file}: {e}", file=sys.stderr)
            return 1
    else:
        for label, url in FEED_URLS:
            feed = fetch_feed(label, url)
            if feed is not None:
                feeds.append(feed)
        if not feeds:
            print("error: all calendar sources failed", file=sys.stderr)
            if out_path.exists():
                age_h = (now.timestamp() - out_path.stat().st_mtime) / 3600
                warn(f"keeping existing {out_path} untouched "
                     f"(stale data beats no data — file is {age_h:.1f}h old)")
            else:
                warn(f"no existing {out_path} to fall back on — engine will have "
                     f"no news blackout until a fetch succeeds")
            return 2

    events = collect(feeds, currencies, args.min_impact)

    if args.dry_run:
        print(f"{'time (UTC)':<26} {'impact':<7} {'cur':<4} title")
        for ev in events:
            print(f"{ev['time']:<26} {ev['impact']:<7} {ev['currency']:<4} {ev['title']}")
        print(f"\n{len(events)} events matched "
              f"(currencies={','.join(sorted(currencies))}, min-impact={args.min_impact}) "
              f"— dry run, nothing written")
        summarize(events, now)
        return 0

    atomic_write(out_path, events)
    print(f"{len(events)} events written to {out_path}")
    summarize(events, now)
    return 0


if __name__ == "__main__":
    sys.exit(main())
