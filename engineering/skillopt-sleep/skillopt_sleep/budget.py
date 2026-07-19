"""SkillOpt-Sleep — budget controller.

Lets the user say how much they're willing to spend on a night's "dreaming",
in tokens or wall-clock minutes, and the engine schedules depth (how many
rollouts × how many nights) within that budget. Stops cleanly when exhausted
and reports what it skipped (no silent truncation).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Budget:
    max_tokens: Optional[int] = None      # None = unlimited
    max_minutes: Optional[float] = None   # None = unlimited
    _start_time: Optional[float] = None
    _tokens_at_start: int = 0

    def start(self, clock_fn, tokens_now: int) -> None:
        self._start_time = clock_fn()
        self._tokens_at_start = tokens_now

    def tokens_spent(self, tokens_now: int) -> int:
        return max(0, tokens_now - self._tokens_at_start)

    def minutes_elapsed(self, clock_fn) -> float:
        if self._start_time is None:
            return 0.0
        return (clock_fn() - self._start_time) / 60.0

    def remaining_fraction(self, *, tokens_now: int, clock_fn) -> float:
        """Smallest remaining fraction across all active limits (1.0 = fresh)."""
        fracs = [1.0]
        if self.max_tokens:
            fracs.append(max(0.0, 1.0 - self.tokens_spent(tokens_now) / self.max_tokens))
        if self.max_minutes:
            fracs.append(max(0.0, 1.0 - self.minutes_elapsed(clock_fn) / self.max_minutes))
        return min(fracs)

    def exhausted(self, *, tokens_now: int, clock_fn) -> bool:
        if self.max_tokens and self.tokens_spent(tokens_now) >= self.max_tokens:
            return True
        if self.max_minutes and self.minutes_elapsed(clock_fn) >= self.max_minutes:
            return True
        return False

    def status(self, *, tokens_now: int, clock_fn) -> str:
        parts = []
        if self.max_tokens:
            parts.append(f"tokens {self.tokens_spent(tokens_now)}/{self.max_tokens}")
        if self.max_minutes:
            parts.append(f"minutes {self.minutes_elapsed(clock_fn):.1f}/{self.max_minutes}")
        return ", ".join(parts) or "unbounded"


def plan_depth(budget: Budget, *, n_tasks: int,
               default_nights: int = 2, default_k: int = 1) -> tuple:
    """Heuristically choose (nights, rollouts_per_task) from a token budget.

    Rough cost model: one rollout ≈ 1 unit; a night does ~n_tasks*k rollouts
    plus reflect/gate (~2*n_tasks). We scale k and nights up with more budget.
    Returns (nights, k). With no budget set, returns the defaults.
    """
    if not budget.max_tokens:
        return default_nights, default_k
    # assume ~1.5k tokens per rollout as a planning constant
    rollouts_affordable = budget.max_tokens / 1500.0
    per_night = max(1, n_tasks) * 3  # rollouts + reflect + gate, k=1
    nights = max(1, min(4, int(rollouts_affordable // per_night)))
    # spend surplus on more rollouts-per-task (contrastive signal)
    surplus = rollouts_affordable - nights * per_night
    k = max(1, min(5, 1 + int(surplus // max(1, n_tasks))))
    return nights, k
