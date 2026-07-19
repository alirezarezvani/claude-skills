"""SkillOpt-Sleep — persona task fixtures for the validation experiment.

Each persona is a list of TaskRecords with EXACT checkable references and a
`rule:<key>` tag naming the single skill rule that makes the task solvable
(consumed by MockBackend). This lets the experiment prove — deterministically,
with no API — that nightly consolidation lifts a held-out score and that the
gate blocks regressions.

Personas mirror the user's framing: programmer / researcher / analyst.
"""
from __future__ import annotations

from typing import List

from skillopt_sleep.types import TaskRecord


def _t(i, intent, ref, rule, project="/personas/demo", outcome="fail") -> TaskRecord:
    return TaskRecord(
        id=f"persona_{rule}_{i}",
        project=project,
        intent=intent,
        context_excerpt="",
        attempted_solution="",
        outcome=outcome,
        reference_kind="exact",
        reference=ref,
        tags=[f"rule:{rule}"],
        source_sessions=[f"sess_{i}"],
    )


def researcher_persona() -> List[TaskRecord]:
    """Researcher who always wants arXiv ids wrapped in <answer> tags."""
    items = [
        ("Give me the arXiv id for the SkillOpt paper", "arXiv:2605.23904"),
        ("What's the arXiv id of the Attention paper?", "arXiv:1706.03762"),
        ("arXiv id for the GAN paper?", "arXiv:1406.2661"),
        ("arXiv id for BERT?", "arXiv:1810.04805"),
        ("arXiv id for the ResNet paper?", "arXiv:1512.03385"),
        ("arXiv id for the Adam optimizer paper?", "arXiv:1412.6980"),
        ("arXiv id for Dropout?", "arXiv:1207.0580"),
        ("arXiv id for the Transformer-XL paper?", "arXiv:1901.02860"),
        ("arXiv id for word2vec?", "arXiv:1301.3781"),
        ("arXiv id for the VAE paper?", "arXiv:1312.6114"),
        ("arXiv id for batch norm?", "arXiv:1502.03167"),
        ("arXiv id for GPT-3?", "arXiv:2005.14165"),
    ]
    # Both rules required: format the id (arxiv-id) AND wrap in answer tags.
    out: List[TaskRecord] = []
    for i, (q, a) in enumerate(items):
        t = _t(i, q, a, "wrap-answer")
        t.tags = ["rule:wrap-answer", "rule:arxiv-id"]
        out.append(t)
    return out


def programmer_persona() -> List[TaskRecord]:
    """Programmer who wants imperative-mood commit subjects."""
    items = [
        ("commit message for adding a login form", "Add login form"),
        ("commit message for fixing the null pointer bug", "Fix null pointer in parser"),
        ("commit message for updating the README", "Update README"),
        ("commit message for removing dead code", "Remove dead code"),
        ("commit message for bumping the version", "Bump version to 1.2.0"),
        ("commit message for refactoring the auth module", "Refactor auth module"),
        ("commit message for adding tests", "Add unit tests for scheduler"),
        ("commit message for fixing the CI pipeline", "Fix CI pipeline"),
    ]
    return [_t(i, q, a, "commit-imperative") for i, (q, a) in enumerate(items)]


def harmful_edit_task() -> TaskRecord:
    """A task whose 'fix' is a known-bad rule; used to prove the gate rejects
    regressions. The MockBackend proposes the harmful rule on this failure,
    but applying it does NOT raise the held-out score, so the gate must reject.
    """
    t = _t(99, "answer this freely", "THIS_WILL_NOT_MATCH", "__harmful__")
    t.reference = "an-answer-that-the-harmful-rule-cannot-produce"
    return t


PERSONAS = {
    "researcher": researcher_persona,
    "programmer": programmer_persona,
}
