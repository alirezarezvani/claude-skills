"""Process supervisor for the gold-scalper engine (stdlib-only, Windows-first).

Keeps `python main.py` alive: restarts on crash, detects a hung engine via the
heartbeat file the engine writes each iteration (logs/heartbeat.json:
{"ts": iso-utc, "equity": float, "open_positions": int}), and -- mirroring the
repo's agent-harness loop discipline -- never crash-loops forever: after
--max-restarts restarts inside --window-hours it writes logs/ESCALATE with the
reason + restart history and exits 3 so a human intervenes.

Usage:
  python tools/watchdog.py [--cmd "python main.py"]
                           [--heartbeat logs/heartbeat.json]
                           [--stale-seconds 120] [--max-restarts 3]
                           [--window-hours 1] [--once]

--once runs a single freshness check (exit 0 fresh / 1 stale) for
Windows Task Scheduler integration.

Windows notes:
  * The child is started with CREATE_NEW_PROCESS_GROUP so console CTRL events
    do not propagate between watchdog and engine uncontrolled.
  * Graceful stop sends CTRL_BREAK_EVENT to the child's group first (the only
    console signal deliverable to another process group on Windows), waits
    15s, then TerminateProcess via terminate(), then kill() after 10s more.
  * On POSIX the same sequence degrades to SIGTERM -> wait -> SIGKILL.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import shlex
import signal
import subprocess
import sys
import time

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent   # gold-scalper root
LOG_PATH = BASE_DIR / "logs" / "watchdog.log"
ESCALATE_PATH = BASE_DIR / "logs" / "ESCALATE"
BACKOFF_SECONDS = (10, 30, 90)          # 1st, 2nd, 3rd+ restart
GRACEFUL_WAIT = 15                      # s after CTRL_BREAK/SIGTERM before terminate()
KILL_WAIT = 10                          # s after terminate() before kill()
MISSING_GRACE = 180                     # s post-start before a missing heartbeat = hung
POLL_SECONDS = 1.0

IS_WINDOWS = os.name == "nt"
_STOP = False                           # set by our own signal handlers


def log(msg: str) -> None:
    line = f"{dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass                            # never let logging kill the supervisor


# ---------- heartbeat ----------

def heartbeat_age(path: pathlib.Path) -> float | None:
    """Seconds since the engine last proved it was alive, or None if no
    usable heartbeat exists. Prefers the JSON `ts` field; falls back to file
    mtime if the file is mid-write or malformed."""
    try:
        raw = path.read_text(encoding="utf-8")
        ts = dt.datetime.fromisoformat(json.loads(raw)["ts"])
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=dt.timezone.utc)
        return (dt.datetime.now(dt.timezone.utc) - ts).total_seconds()
    except FileNotFoundError:
        return None
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        try:
            return time.time() - path.stat().st_mtime
        except OSError:
            return None


def check_hung(path: pathlib.Path, child_started: float,
               stale_seconds: int) -> str | None:
    """Return a reason string if the engine looks hung, else None.
    A heartbeat that pre-dates this child (leftover from the previous run)
    counts as missing, so a fresh restart gets the full grace period."""
    age = heartbeat_age(path)
    since_start = time.time() - child_started
    if age is None or age > since_start:            # missing / stale leftover
        if since_start > MISSING_GRACE:
            return (f"no heartbeat from this run after {since_start:.0f}s "
                    f"(grace {MISSING_GRACE}s)")
        return None
    if age > stale_seconds:
        return f"heartbeat stale: {age:.0f}s old (limit {stale_seconds}s)"
    return None


# ---------- child lifecycle ----------

def start_child(cmd: str) -> subprocess.Popen:
    if IS_WINDOWS:
        return subprocess.Popen(
            cmd, cwd=str(BASE_DIR),
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    return subprocess.Popen(shlex.split(cmd), cwd=str(BASE_DIR),
                            start_new_session=True)


def stop_child(proc: subprocess.Popen) -> None:
    """Graceful-then-forceful: CTRL_BREAK (SIGTERM on POSIX) -> 15s ->
    terminate() -> 10s -> kill(). The engine flattens/journals on the
    graceful signal, so give it real time before TerminateProcess."""
    if proc.poll() is not None:
        return
    try:
        if IS_WINDOWS:
            proc.send_signal(signal.CTRL_BREAK_EVENT)
            log(f"sent CTRL_BREAK_EVENT to pid {proc.pid}")
        else:
            proc.terminate()
            log(f"sent SIGTERM to pid {proc.pid}")
        proc.wait(timeout=GRACEFUL_WAIT)
        log(f"child pid {proc.pid} exited gracefully (rc={proc.returncode})")
        return
    except subprocess.TimeoutExpired:
        pass
    except (OSError, ValueError):
        pass                            # already dead or signal undeliverable
    try:
        proc.terminate()
        log(f"terminate() sent to pid {proc.pid}")
        proc.wait(timeout=KILL_WAIT)
    except subprocess.TimeoutExpired:
        proc.kill()
        log(f"kill() sent to pid {proc.pid}")
        try:
            proc.wait(timeout=KILL_WAIT)
        except subprocess.TimeoutExpired:
            log(f"WARNING: pid {proc.pid} did not die even after kill()")
    except OSError:
        pass
    if proc.poll() is not None:
        log(f"child pid {proc.pid} stopped (rc={proc.returncode})")


def interruptible_sleep(seconds: float) -> None:
    end = time.time() + seconds
    while not _STOP and time.time() < end:
        time.sleep(min(0.5, max(0.0, end - time.time())))


# ---------- escalation ----------

def escalate(reason: str, history: list[float]) -> None:
    body = {
        "ts": dt.datetime.now(dt.timezone.utc).isoformat(),
        "reason": reason,
        "restart_history_utc": [
            dt.datetime.fromtimestamp(t, dt.timezone.utc).isoformat(timespec="seconds")
            for t in history],
        "action_required": "Engine restarted too often; watchdog stopped. "
                           "Investigate logs/watchdog.log + logs/harness.log, "
                           "then delete this file and restart the watchdog.",
    }
    ESCALATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ESCALATE_PATH.write_text(json.dumps(body, indent=2), encoding="utf-8")
    log(f"ESCALATE: {reason} -- restart budget exhausted, wrote {ESCALATE_PATH}, exiting 3")


# ---------- modes ----------

def run_once(hb_path: pathlib.Path, stale_seconds: int) -> int:
    age = heartbeat_age(hb_path)
    if age is None:
        log(f"once: STALE -- heartbeat missing/unreadable at {hb_path}")
        return 1
    if age > stale_seconds:
        log(f"once: STALE -- heartbeat {age:.0f}s old (limit {stale_seconds}s)")
        return 1
    log(f"once: FRESH -- heartbeat {age:.0f}s old (limit {stale_seconds}s)")
    return 0


def supervise(args: argparse.Namespace, hb_path: pathlib.Path) -> int:
    window = args.window_hours * 3600.0
    restarts: list[float] = []          # epoch times of restarts performed
    log(f"watchdog start: cmd={args.cmd!r} heartbeat={hb_path} "
        f"stale={args.stale_seconds}s max_restarts={args.max_restarts}/"
        f"{args.window_hours}h")

    while not _STOP:
        proc = start_child(args.cmd)
        started = time.time()
        log(f"started child pid {proc.pid}")

        reason = None
        while not _STOP:
            rc = proc.poll()
            if rc is not None:
                reason = f"child pid {proc.pid} exited rc={rc}"
                break
            hung = check_hung(hb_path, started, args.stale_seconds)
            if hung:
                reason = f"child pid {proc.pid} hung: {hung}"
                log(reason + " -- stopping it")
                stop_child(proc)
                break
            time.sleep(POLL_SECONDS)

        if _STOP:
            log("shutdown requested -- stopping child and exiting 0")
            stop_child(proc)
            return 0

        log(reason)
        now = time.time()
        restarts = [t for t in restarts if now - t <= window]
        if len(restarts) >= args.max_restarts:
            escalate(reason, restarts + [now])
            return 3
        restarts.append(now)
        backoff = BACKOFF_SECONDS[min(len(restarts) - 1, len(BACKOFF_SECONDS) - 1)]
        log(f"restart {len(restarts)}/{args.max_restarts} in window -- "
            f"backing off {backoff}s")
        interruptible_sleep(backoff)

    return 0


def _on_signal(signum, _frame):
    global _STOP
    _STOP = True
    log(f"received signal {signum} -- shutting down")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Supervise the gold-scalper engine: restart on crash/hang "
                    "with bounded retries, then escalate to a human.")
    ap.add_argument("--cmd", default="python main.py",
                    help="command to launch the engine (default: 'python main.py')")
    ap.add_argument("--heartbeat", default="logs/heartbeat.json",
                    help="heartbeat file the engine writes each iteration")
    ap.add_argument("--stale-seconds", type=int, default=120,
                    help="heartbeat older than this = engine hung")
    ap.add_argument("--max-restarts", type=int, default=3,
                    help="restarts allowed inside --window-hours before escalating")
    ap.add_argument("--window-hours", type=float, default=1.0,
                    help="sliding window for the restart budget")
    ap.add_argument("--once", action="store_true",
                    help="single freshness check: exit 0 fresh / 1 stale "
                         "(for Windows Task Scheduler)")
    args = ap.parse_args()

    hb_path = pathlib.Path(args.heartbeat)
    if not hb_path.is_absolute():
        hb_path = BASE_DIR / hb_path

    if args.once:
        return run_once(hb_path, args.stale_seconds)

    signal.signal(signal.SIGINT, _on_signal)
    signal.signal(signal.SIGTERM, _on_signal)
    if IS_WINDOWS and hasattr(signal, "SIGBREAK"):
        signal.signal(signal.SIGBREAK, _on_signal)

    try:
        return supervise(args, hb_path)
    except KeyboardInterrupt:
        log("KeyboardInterrupt -- exiting 0")
        return 0


if __name__ == "__main__":
    sys.exit(main())
