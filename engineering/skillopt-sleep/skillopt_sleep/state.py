"""SkillOpt-Sleep — persistent cross-night state.

state.json lives in ~/.skillopt-sleep and is the "long-term" store that
turns nightly episodes into durable competence (the Agent-Sleep paper's
short-term -> long-term transfer). It records:

  - night counter
  - last harvest timestamp per project (so each night only sees new data)
  - cross-night "slow/meta" memory (lessons that persisted across nights)
  - per-night history (scores, accept/reject) for trend reporting
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional


def _now_iso(clock: Optional[float] = None) -> str:
    # caller passes a timestamp; we avoid importing time at module import
    import time as _t
    return _t.strftime("%Y-%m-%dT%H:%M:%S", _t.localtime(clock if clock is not None else _t.time()))


DEFAULT_STATE: Dict[str, Any] = {
    "version": 1,
    "night": 0,
    "last_harvest": {},     # project -> iso timestamp of last harvested record
    "slow_memory": "",      # cross-night consolidated lessons (meta-skill analogue)
    "history": [],          # list of per-night summaries
    "task_archive": [],     # capped list of past mined tasks (for associative recall)
}


class SleepState:
    def __init__(self, path: str, data: Optional[Dict[str, Any]] = None) -> None:
        self.path = path
        self.data = data if data is not None else dict(DEFAULT_STATE)

    # io ---------------------------------------------------------------------
    @classmethod
    def load(cls, path: str) -> "SleepState":
        if os.path.exists(path):
            try:
                with open(path) as f:
                    data = json.load(f)
                merged = dict(DEFAULT_STATE)
                merged.update(data if isinstance(data, dict) else {})
                return cls(path, merged)
            except Exception:
                pass
        return cls(path, dict(DEFAULT_STATE))

    def save(self) -> None:
        # state.json carries real harvested session content (task intents,
        # code excerpts, project context) in plaintext, kept indefinitely —
        # tighten permissions rather than leave them at the process umask
        # default, which is world-readable on a typical multi-user box.
        state_dir = os.path.dirname(self.path)
        # mode= only governs the leaf dir mkdir() creates (intermediate
        # parents still fall back to the umask default) and is itself
        # subject to umask, so the chmod below still matters -- but passing
        # it here closes the window between creation and chmod for the
        # common case where state_dir doesn't already exist.
        os.makedirs(state_dir, mode=0o700, exist_ok=True)
        try:
            os.chmod(state_dir, 0o700)
        except OSError:
            pass
        tmp = self.path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        try:
            os.chmod(tmp, 0o600)
        except OSError:
            pass
        os.replace(tmp, self.path)

    # accessors --------------------------------------------------------------
    @property
    def night(self) -> int:
        return int(self.data.get("night", 0))

    def last_harvest_for(self, project: str) -> Optional[str]:
        return self.data.get("last_harvest", {}).get(project)

    def set_last_harvest(self, project: str, iso_ts: str) -> None:
        self.data.setdefault("last_harvest", {})[project] = iso_ts

    @property
    def slow_memory(self) -> str:
        return str(self.data.get("slow_memory", ""))

    def set_slow_memory(self, content: str) -> None:
        self.data["slow_memory"] = content

    def begin_night(self, clock: Optional[float] = None) -> int:
        self.data["night"] = self.night + 1
        return self.night

    def record_night(self, summary: Dict[str, Any]) -> None:
        self.data.setdefault("history", []).append(summary)

    # ── task archive (associative-recall memory) ──────────────────────────
    def task_archive(self) -> list:
        """Past mined tasks as plain dicts (newest last)."""
        return list(self.data.get("task_archive", []))

    def add_to_archive(self, task_dicts: list, cap: int = 300) -> None:
        """Append tonight's tasks; keep only the most recent ``cap``."""
        arc = self.data.setdefault("task_archive", [])
        arc.extend(task_dicts)
        if len(arc) > cap:
            self.data["task_archive"] = arc[-cap:]
