"""SkillOpt-Sleep — core data types.

These dataclasses are the interfaces between the sleep-cycle stages
(harvest -> mine -> replay -> consolidate -> stage). They are intentionally
plain (no slots, no heavy deps) so the package imports cleanly on any
Python 3.8+ interpreter and the deterministic experiment runs with zero
external dependencies.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

# ── Stage 1: harvest ──────────────────────────────────────────────────────────

@dataclass
class SessionDigest:
    """A normalized summary of one local agent session transcript.

    Produced by source-specific harvesters from Claude Code transcripts or
    Codex Desktop archived sessions.
    """

    session_id: str
    project: str
    git_branch: str = ""
    started_at: str = ""
    ended_at: str = ""
    user_prompts: List[str] = field(default_factory=list)
    assistant_finals: List[str] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)
    files_touched: List[str] = field(default_factory=list)
    feedback_signals: List[str] = field(default_factory=list)  # "still broken", "perfect", ...
    n_user_turns: int = 0
    n_assistant_turns: int = 0
    raw_path: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ── Stage 2: mine ─────────────────────────────────────────────────────────────

@dataclass
class TaskRecord:
    """A self-contained recurring task mined from one or more sessions.

    This is the *training unit* of the sleep cycle — the analogue of a
    SkillOpt benchmark item.
    """

    id: str
    project: str
    intent: str                       # what the user wanted (the "question")
    context_excerpt: str = ""         # minimal context needed to attempt it
    # Optional system framing for the rollout. When set (e.g. real benchmarks
    # carrying the research repo's exact rollout_system), the backend uses THIS
    # verbatim instead of its generic instruction wrapper — this keeps scoring
    # faithful to the source task and avoids re-deriving framing the benchmark
    # already bakes in.
    system: str = ""
    attempted_solution: str = ""      # what the agent produced before
    outcome: str = "unknown"          # success | fail | mixed | unknown
    reference_kind: str = "none"      # exact | rubric | rule | none
    reference: str = ""               # exact answer, or rubric text
    judge: Dict[str, Any] = field(default_factory=dict)  # gbrain-style rule judge
    tags: List[str] = field(default_factory=list)
    source_sessions: List[str] = field(default_factory=list)
    # split ∈ {train, val, test}.  val + test come ONLY from real mined tasks and
    # never overlap (val gates updates, test is the final held-out measure). train
    # may be dream-augmented (see origin).  Legacy values replay->train,
    # holdout->val are normalized on load.
    split: str = "train"
    # origin ∈ {real, dream}.  'real' = mined from the user's actual sessions;
    # 'dream' = synthetic/augmented for the training pool. Dream tasks are NEVER
    # allowed into val/test, which is the anti-overfitting guarantee.
    origin: str = "real"
    derived_from: str = ""            # for dream tasks: the real task id it varies

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TaskRecord":
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in d.items() if k in known})


# ── Stage 3: replay ───────────────────────────────────────────────────────────

@dataclass
class ReplayResult:
    """Outcome of re-running one TaskRecord offline under a given skill+memory."""

    id: str
    hard: float = 0.0                 # 0/1 exact, or continuous reward
    soft: float = 0.0                 # partial credit / judge score 0..1
    response: str = ""
    fail_reason: str = ""
    task_type: str = "task"
    judge_rationale: str = ""
    tools_called: List[str] = field(default_factory=list)
    tokens: int = 0                   # approx tokens this rollout cost (for token objective)
    latency_ms: float = 0.0           # wall-clock for this rollout (for latency objective)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ── Stage 4/5: consolidation report ───────────────────────────────────────────

@dataclass
class EditRecord:
    """One bounded edit proposed/applied to skill or memory."""

    target: str                       # "skill" | "memory"
    op: str                           # add | delete | replace
    content: str = ""
    anchor: str = ""                  # for replace/delete: text being changed
    rationale: str = ""


@dataclass
class SleepReport:
    """Everything one night produced — written to staging for review."""

    night: int
    project: str
    started_at: str = ""
    ended_at: str = ""
    n_sessions: int = 0
    n_tasks: int = 0
    n_replayed: int = 0
    baseline_score: float = 0.0
    candidate_score: float = 0.0
    accepted: bool = False
    gate_action: str = ""
    no_edits_reason: str = ""
    edits: List[EditRecord] = field(default_factory=list)
    rejected_edits: List[EditRecord] = field(default_factory=list)
    tokens_used: int = 0
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d
