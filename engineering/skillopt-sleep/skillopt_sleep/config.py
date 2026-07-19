"""SkillOpt-Sleep — configuration.

Config is JSON-first (yaml optional) so the engine and the deterministic
experiment run with zero external dependencies. Defaults are safe:
review-gated adoption, single-project scope, bounded token/task budgets.

Resolution order (later wins):
  1. built-in DEFAULTS
  2. ~/.skillopt-sleep/config.json  (or .yaml if PyYAML available)
  3. explicit overrides passed to load_config(**overrides)
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

HOME_STATE_DIR = os.path.expanduser("~/.skillopt-sleep")
CLAUDE_HOME = os.path.expanduser("~/.claude")
CODEX_HOME = os.path.expanduser("~/.codex")


DEFAULTS: Dict[str, Any] = {
    # ── scope ──────────────────────────────────────────────────────────────
    "claude_home": CLAUDE_HOME,
    "codex_home": CODEX_HOME,
    "transcript_source": "claude",  # "claude" | "codex" | "auto"
    "projects": "invoked",        # "invoked" | "all" | [list of abs paths]
    "invoked_project": "",        # filled at runtime (cwd) when projects == "invoked"
    "lookback_hours": 72,         # harvest window when no prior sleep recorded
    # ── budgets ────────────────────────────────────────────────────────────
    "max_tasks_per_night": 40,
    "max_tokens_per_night": 400_000,
    "holdout_fraction": 0.34,     # legacy alias for val_fraction
    "val_fraction": 0.34,         # real tasks reserved to gate updates
    "test_fraction": 0.0,         # real tasks reserved as the final held-out measure
    # ── optimizer ──────────────────────────────────────────────────────────
    "backend": "mock",            # "mock" | "claude" | "codex" | "copilot"
    "model": "",                  # backend-specific; "" => backend default
    "gate_mode": "on",            # "on" (validation-gated) | "off" (greedy, no hard filter)
    "codex_path": "",             # "" => auto-detect the real @openai/codex binary
    "edit_budget": 4,             # textual learning rate (max edits/night)
    "gate_metric": "mixed",       # hard | soft | mixed (mixed best for tiny holdouts)
    "gate_mixed_weight": 0.5,
    "replay_mode": "mock",        # "mock" (sandboxed prompt) | "fresh" (worktree)
    # ── dream + recall (opt-in; defaults reproduce the prior single-shot loop) ─
    "dream_rollouts": 1,          # >1 => multi-rollout contrastive reflection per task
    "dream_factor": 0,            # >0 => add N synthetic variants of each task to the dream
    "recall_k": 0,                # >0 => recall the K most-similar past tasks into the dream
    "evolve_memory": True,        # consolidate CLAUDE.md
    "evolve_skill": True,         # consolidate the managed SKILL.md
    "llm_mine": True,             # use the backend to mine checkable tasks (real backends)
    "target_skill_path": "",      # explicit SKILL.md target for repo-scoped agents
    "target_task_filter": True,   # prefer mined tasks matching target_skill_path/text
    "progress": False,            # print phase progress to stderr
    # ── adoption / safety ──────────────────────────────────────────────────
    "auto_adopt": False,          # default: stage + require explicit `adopt`
    "managed_skill_name": "skillopt-sleep-learned",
    "redact_secrets": True,
    "seed": 42,
}


@dataclass
class SleepConfig:
    data: Dict[str, Any] = field(default_factory=lambda: dict(DEFAULTS))

    # convenient attribute access -------------------------------------------
    def __getattr__(self, name: str) -> Any:
        # only called when normal attribute lookup fails
        data = object.__getattribute__(self, "data")
        if name in data:
            return data[name]
        raise AttributeError(name)

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.data)

    # paths ------------------------------------------------------------------
    @property
    def state_dir(self) -> str:
        # Allow full isolation: if the caller overrides state_dir explicitly,
        # honor it; else derive from claude_home's parent so a single
        # --claude-home flag isolates transcripts AND state together; else the
        # default ~/.skillopt-sleep.
        explicit = self.data.get("state_dir")
        if explicit:
            return explicit
        ch = self.data.get("claude_home", CLAUDE_HOME)
        if os.path.abspath(ch) != os.path.abspath(CLAUDE_HOME):
            return os.path.join(os.path.dirname(os.path.abspath(ch)), ".skillopt-sleep")
        return HOME_STATE_DIR

    @property
    def state_path(self) -> str:
        return os.path.join(self.state_dir, "state.json")

    @property
    def transcripts_dir(self) -> str:
        return os.path.join(self.data["claude_home"], "projects")

    @property
    def codex_archived_sessions_dir(self) -> str:
        return os.path.join(self.data["codex_home"], "archived_sessions")

    @property
    def history_path(self) -> str:
        return os.path.join(self.data["claude_home"], "history.jsonl")

    @property
    def skills_dir(self) -> str:
        return os.path.join(self.data["claude_home"], "skills")

    def managed_skill_path(self) -> str:
        target = self.data.get("target_skill_path") or ""
        if target:
            target = os.path.expanduser(str(target))
            if not os.path.isabs(target):
                base = self.data.get("invoked_project") or os.getcwd()
                target = os.path.join(base, target)
            return os.path.abspath(target)
        return os.path.join(
            self.skills_dir, self.data["managed_skill_name"], "SKILL.md"
        )


def _user_config_path() -> Optional[str]:
    for name in ("config.json", "config.yaml", "config.yml"):
        p = os.path.join(HOME_STATE_DIR, name)
        if os.path.exists(p):
            return p
    return None


def _load_file(path: str) -> Dict[str, Any]:
    if path.endswith((".yaml", ".yml")):
        try:
            import yaml  # optional
            with open(path) as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}
    with open(path) as f:
        return json.load(f)


def load_config(**overrides: Any) -> SleepConfig:
    data = dict(DEFAULTS)
    path = _user_config_path()
    if path:
        try:
            data.update(_load_file(path) or {})
        except Exception:
            pass
    data.update({k: v for k, v in overrides.items() if v is not None})
    if data.get("projects") == "invoked" and not data.get("invoked_project"):
        data["invoked_project"] = os.getcwd()
    return SleepConfig(data=data)
