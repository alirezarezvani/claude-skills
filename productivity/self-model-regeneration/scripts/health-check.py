#!/usr/bin/env python3
"""SessionStart health check — disk/ram/gpu/config/growth + self-model flag detection.

NEVER blocks, always exits 0. Outputs structured signals to stderr for AI consumption.

Part of the self-model regeneration loop:
  - Detects .self-model-stale flag (written by quality-gate.py at Stop)
  - Outputs REGENERATE_NEEDED or CLEANED_ORPHAN signals
  - Also checks system health: disk, RAM, GPU, temp files, config integrity

Configuration:
  - MEMORY_DIR env var: path to memory directory (default: ~/.claude/memory)
  - CLAUDE_DIR env var: path to .claude directory (default: ~/.claude)
  - WARN_DISK_GB: disk free space warn threshold (default: 50)
  - BLOCK_DISK_GB: disk free space critical threshold (default: 15)
"""

import os
import sys
import shutil
import subprocess
import json
import argparse
import platform
from pathlib import Path
from datetime import date, datetime, timezone

HOME = Path.home()
CLAUDE = Path(os.environ.get("CLAUDE_DIR", str(HOME / ".claude")))
MEMORY = Path(os.environ.get("MEMORY_DIR", str(CLAUDE / "memory")))
STALE_FLAG = MEMORY / ".self-model-stale"
SELF_MODEL = MEMORY / "self-model.md"
GROWTH_LOG_DIR = MEMORY / "growth-log"
SCRIPTS_DIR = CLAUDE / "scripts"

WARN_DISK_GB = int(os.environ.get("WARN_DISK_GB", "50"))
BLOCK_DISK_GB = int(os.environ.get("BLOCK_DISK_GB", "15"))
WARN_TMP_FILES = int(os.environ.get("WARN_TMP_FILES", "500"))
WARN_GPU_TEMP_C = int(os.environ.get("WARN_GPU_TEMP_C", "80"))
WARN_GPU_VRAM_PCT = int(os.environ.get("WARN_GPU_VRAM_PCT", "90"))
STALE_GROWTH_DAYS = int(os.environ.get("STALE_GROWTH_DAYS", "3"))

if platform.system() == "Windows" and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def check_disk():
    usage = shutil.disk_usage(HOME)
    free_gb = usage.free // (1024 ** 3)
    if free_gb < BLOCK_DISK_GB:
        level = "REFUSE"
    elif free_gb < WARN_DISK_GB:
        level = "WARN"
    else:
        level = "OK"
    print(f"DISK:{free_gb}GB:{level}", file=sys.stderr)
    return {"name": "disk", "free_gb": free_gb, "level": level}


def check_tmp():
    p = platform.system()
    if p == "Windows":
        tmp = HOME / "AppData" / "Local" / "Temp"
    else:
        tmp = Path(os.environ.get("TMPDIR", "/tmp"))
    try:
        count = len(os.listdir(tmp))
    except OSError:
        return {"name": "tmp", "count": 0, "level": "OK"}
    level = "WARN" if count > WARN_TMP_FILES else "OK"
    if count > WARN_TMP_FILES:
        print(f"TMP:{count}:WARN", file=sys.stderr)
    return {"name": "tmp", "count": count, "level": level}


def check_ram():
    p = platform.system()
    try:
        if p == "Windows":
            out = subprocess.run(
                ["wmic", "OS", "get", "TotalVisibleMemorySize,FreePhysicalMemory", "/format:list"],
                capture_output=True, text=True, timeout=10
            )
            total_kb = free_kb = None
            for line in out.stdout.strip().split("\n"):
                line = line.strip()
                if "TotalVisibleMemorySize" in line:
                    total_kb = int(line.split("=")[-1].strip())
                elif "FreePhysicalMemory" in line:
                    free_kb = int(line.split("=")[-1].strip())
            if total_kb and free_kb:
                pct = 100 - (free_kb * 100 // total_kb)
                print(f"RAM:{pct}%:{free_kb // 1024}MB:{total_kb // 1024}MB", file=sys.stderr)
                return {"name": "ram", "pct": pct, "free_mb": free_kb // 1024, "total_mb": total_kb // 1024}
        elif p == "Linux":
            mem = {}
            with open("/proc/meminfo") as f:
                for line in f:
                    if "MemTotal" in line or "MemAvailable" in line:
                        parts = line.split(":")
                        key = parts[0].strip()
                        mem[key] = int(parts[1].strip().split()[0])
            if "MemTotal" in mem and "MemAvailable" in mem:
                used = mem["MemTotal"] - mem["MemAvailable"]
                pct = used * 100 // mem["MemTotal"]
                print(f"RAM:{pct}%:{mem['MemAvailable'] // 1024}MB:{mem['MemTotal'] // 1024}MB", file=sys.stderr)
                return {"name": "ram", "pct": pct, "free_mb": mem["MemAvailable"] // 1024, "total_mb": mem["MemTotal"] // 1024}
        elif p == "Darwin":
            out = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True, timeout=5)
            total_bytes = int(out.stdout.strip())
            total_mb = total_bytes // (1024 * 1024)
            out = subprocess.run(["vm_stat"], capture_output=True, text=True, timeout=5)
            page_size = 4096
            free_pages = 0
            for line in out.stdout.strip().split("\n"):
                if any(k in line for k in ("Pages free", "Pages speculative", "Pages inactive")):
                    free_pages += int(line.strip().split(":")[-1].strip().rstrip("."))
            free_mb = (free_pages * page_size) // (1024 * 1024)
            pct = 100 - (free_mb * 100 // total_mb) if total_mb else 0
            print(f"RAM:{pct}%:{free_mb}MB:{total_mb}MB", file=sys.stderr)
            return {"name": "ram", "pct": pct, "free_mb": free_mb, "total_mb": total_mb}
    except Exception:
        pass
    return None


def check_gpu():
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=temperature.gpu,utilization.gpu,memory.used,memory.total",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10
        )
        parts = out.stdout.strip().split(",")
        if len(parts) >= 4:
            temp = int(parts[0].strip())
            gpu_pct = int(parts[1].strip())
            vram_used = int(parts[2].strip())
            vram_total = int(parts[3].strip())
            vram_pct = vram_used * 100 // vram_total
            state = "WARN" if temp > WARN_GPU_TEMP_C or vram_pct > WARN_GPU_VRAM_PCT else "OK"
            print(f"GPU:{temp}C:{gpu_pct}%:{vram_used}/{vram_total}MB:{state}", file=sys.stderr)
            return {"name": "gpu", "temp_c": temp, "util_pct": gpu_pct,
                    "vram_used_mb": vram_used, "vram_total_mb": vram_total, "level": state}
    except Exception:
        pass
    return None


def check_config():
    files = ["quality-gate.py", "health-check.py", "log-regeneration.py"]
    missing = []
    for f in files:
        if not (SCRIPTS_DIR / f).exists():
            missing.append(f)
    if missing:
        print(f"CONFIG:MISSING:{','.join(missing)}", file=sys.stderr)
    else:
        print("CONFIG:ALL:OK", file=sys.stderr)
    return {"name": "config", "missing": missing, "level": "WARN" if missing else "OK"}


def check_growth():
    import re
    if not GROWTH_LOG_DIR.is_dir():
        print("GROWTH:NO_DIR", file=sys.stderr)
        return {"name": "growth-log", "status": "no_dir", "level": "WARN"}
    today = date.today()
    latest = None
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}")
    for f in GROWTH_LOG_DIR.iterdir():
        if f.suffix == ".md":
            m = date_pattern.match(f.name)
            if not m:
                continue
            try:
                d = date.fromisoformat(m.group())
                if latest is None or d > latest:
                    latest = d
            except ValueError:
                continue
    if latest:
        days = (today - latest).days
        state = "WARN" if days > STALE_GROWTH_DAYS else "OK"
        print(f"GROWTH:{latest}:{days}d:{state}", file=sys.stderr)
        return {"name": "growth-log", "latest": str(latest), "days": days, "level": state}
    else:
        print("GROWTH:EMPTY:WARN", file=sys.stderr)
        return {"name": "growth-log", "latest": None, "days": None, "level": "WARN"}


def check_skills():
    skills_dir = CLAUDE / "skills"
    count = 0
    if skills_dir.is_dir():
        for name in skills_dir.iterdir():
            if name.is_dir() and (name / "SKILL.md").exists():
                count += 1
    print(f"SKILLS:{count}:OK", file=sys.stderr)
    return {"name": "skills", "count": count, "level": "OK"}


def check_self_model_flag():
    if not STALE_FLAG.exists():
        return None
    flag_mtime = datetime.fromtimestamp(STALE_FLAG.stat().st_mtime, tz=timezone.utc)
    if not SELF_MODEL.exists():
        print("SELF_MODEL:REGENERATE_NEEDED:model_missing", file=sys.stderr)
        payload = json.dumps({"action": "regenerate", "reason": "self-model.md missing", "trigger": "flag"})
        print(f"SELF_MODEL:JSON:{payload}", file=sys.stderr)
        return {"signal": "REGENERATE_NEEDED", "reason": "model_missing", "action": "regenerate", "payload": json.loads(payload)}
    try:
        size = SELF_MODEL.stat().st_size
        if size == 0:
            print("SELF_MODEL:REGENERATE_NEEDED:empty_file", file=sys.stderr)
            return {"signal": "REGENERATE_NEEDED", "reason": "empty_file", "action": "regenerate"}
        if size < 50:
            print(f"SELF_MODEL:WARN:truncated_file:{size}bytes", file=sys.stderr)
    except OSError:
        pass
    model_mtime = datetime.fromtimestamp(SELF_MODEL.stat().st_mtime, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    if model_mtime > now:
        future_sec = (model_mtime - now).total_seconds()
        print(f"SELF_MODEL:WARN:future_mtime:{future_sec:.0f}s_ahead", file=sys.stderr)
    newer_logs = []
    if GROWTH_LOG_DIR.is_dir():
        for f in GROWTH_LOG_DIR.iterdir():
            if f.suffix == ".md":
                if datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc) >= model_mtime:
                    newer_logs.append(f.stem)
    if newer_logs:
        newer_logs.sort()
        print(f"SELF_MODEL:REGENERATE_NEEDED:growth_logs_newer({len(newer_logs)}):{','.join(newer_logs[:5])}",
              file=sys.stderr)
        payload = json.dumps({"action": "regenerate",
                              "reason": f"growth-log entries newer than self-model: {', '.join(newer_logs)}",
                              "trigger": "flag", "sources": newer_logs})
        print(f"SELF_MODEL:JSON:{payload}", file=sys.stderr)
        return {"signal": "REGENERATE_NEEDED", "reason": f"growth_logs_newer({len(newer_logs)})",
                "action": "regenerate", "payload": json.loads(payload)}
    else:
        try:
            STALE_FLAG.unlink()
        except OSError:
            pass
        print(f"SELF_MODEL:CLEANED_ORPHAN:model_fresh:flag_was_{flag_mtime.strftime('%Y-%m-%dT%H:%M:%S')}",
              file=sys.stderr)
        return {"signal": "CLEANED_ORPHAN", "reason": "model_fresh", "action": "cleaned",
                "flag_mtime": flag_mtime.isoformat()}


def main():
    parser = argparse.ArgumentParser(description="SessionStart health check")
    parser.add_argument("--json", action="store_true", help="Output results as JSON to stdout")
    args = parser.parse_args()

    print("--- health ---", file=sys.stderr)
    checks = {}
    checks["disk"] = check_disk()
    ram_result = check_ram()
    if ram_result:
        checks["ram"] = ram_result
    gpu_result = check_gpu()
    if gpu_result:
        checks["gpu"] = gpu_result
    checks["tmp"] = check_tmp()
    checks["config"] = check_config()
    checks["growth"] = check_growth()
    checks["skills"] = check_skills()
    flag_result = check_self_model_flag()
    checks["self_model_flag"] = flag_result if flag_result else {"signal": "none", "action": "none"}
    checks["exit_code"] = 0

    if args.json:
        print(json.dumps(checks, ensure_ascii=False, indent=2))

    sys.exit(0)


if __name__ == "__main__":
    main()
