"""SkillOpt-Sleep — vendored validation gate.

This is a self-contained copy of the SkillOpt validation gate so the sleep
engine has ZERO dependency on the research package (skillopt/*). The research
repo's ``skillopt.evaluation.gate`` is the reference implementation and the two
are kept behaviourally identical; vendoring keeps this open-source tool
decoupled from the paper's experiment code.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateResult:
    action: str            # "accept_new_best" | "accept" | "reject"
    current_skill: str
    current_score: float
    best_skill: str
    best_score: float
    best_step: int


def select_gate_score(hard: float, soft: float, metric: str = "hard",
                      mixed_weight: float = 0.5) -> float:
    """Project (hard, soft) onto a single comparison metric."""
    if metric == "hard":
        return float(hard)
    if metric == "soft":
        return float(soft)
    if metric == "mixed":
        w = max(0.0, min(1.0, float(mixed_weight)))
        return (1.0 - w) * float(hard) + w * float(soft)
    raise ValueError(f"unknown gate metric {metric!r}; expected hard/soft/mixed")


def evaluate_gate(candidate_skill: str, cand_hard: float, current_skill: str,
                  current_score: float, best_skill: str, best_score: float,
                  best_step: int, global_step: int, *, cand_soft: float = 0.0,
                  metric: str = "hard", mixed_weight: float = 0.5) -> GateResult:
    """Pure gate decision: compare candidate score to current/best."""
    cand_score = select_gate_score(cand_hard, cand_soft, metric, mixed_weight)
    if cand_score > current_score:
        if cand_score > best_score:
            return GateResult("accept_new_best", candidate_skill, cand_score,
                              candidate_skill, cand_score, global_step)
        return GateResult("accept", candidate_skill, cand_score,
                          best_skill, best_score, best_step)
    return GateResult("reject", current_skill, current_score,
                      best_skill, best_score, best_step)
