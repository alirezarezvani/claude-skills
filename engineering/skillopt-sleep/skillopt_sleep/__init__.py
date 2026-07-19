"""SkillOpt-Sleep — nightly offline self-evolution for a local Claude agent.

A Claude Code plugin engine that gives a user's agent a "sleep cycle":
harvest the day's real session transcripts, mine recurring tasks, replay
them offline, and consolidate short-term experience into long-term memory
(CLAUDE.md) and skills (SKILL.md) behind a SkillOpt validation gate.

Synthesizes three ideas:
  * SkillOpt  — validation-gated bounded text optimization (this repo)
  * Dreams    — offline memory consolidation, input never mutated
  * Sleep     — short-term experience -> long-term competence, offline

Public entry points:
  * skillopt_sleep.cli      — `python -m skillopt_sleep ...`
  * skillopt_sleep.cycle.run_sleep_cycle(...)
"""
from __future__ import annotations

__all__ = ["__version__"]
__version__ = "0.2.0"
