#!/usr/bin/env python3
"""
route.py — deterministic pipeline router: intake answers → lens + output + steps.

Closes the pipeline: from goal/respondent/output/number of interviews it produces a plan (which lens to read,
which output to build, which stages apply). The model doesn't guess the route — it's fixed.

CLI (flags or interactive):
  python route.py --goal org --respondent employee --output insights --n 6 [--baseline yes]
Values:
  goal:       discovery|org|experience|brand|prioritization|usability|expert|personas|exit|winloss|retro|
              intercept|conflict|ethnography|changereadiness
  respondent: employee|customer|expert|visitor|stakeholder|candidate|group|conflictparty
  output:     mapping|insights|jobmap|persona|journey|memo|opportunity
  n:          number of interviews (int)

Sample: python route.py --sample
"""

import argparse
import json
import sys

LENS = {  # (by respondent, considering the goal) → lens file
    "employee": "templates/org-mapping-vmdi.md",
    "visitor": "templates/visitor-experience.md",
    "expert": "templates/expert.md",
    "customer": "templates/jtbd.md",  # refined by goal below
    "stakeholder": "templates/expert.md",
    "candidate": "templates/candidate.md",
    "group": "templates/focus-group.md",  # refined by goal below (retro → team-retro)
    "conflictparty": "templates/conflict-mediation.md",
}
LENS_BY_GOAL = {  # goal overrides the lens when the goal matters more than «who»
    "discovery": "templates/custdev.md",
    "brand": "templates/brand-positioning.md",
    "experience": "templates/visitor-experience.md",
    "expert": "templates/expert.md",
    "usability": "templates/usability.md",
    "exit": "templates/exit.md",
    "winloss": "templates/winloss.md",
    "retro": "templates/team-retro.md",
    "intercept": "templates/intercept.md",
    "conflict": "templates/conflict-mediation.md",
    "ethnography": "templates/ethnographic.md",
    "changereadiness": "templates/change-readiness.md",
}
OUTPUT = {
    "insights": "outputs/insight-cards.md",
    "persona": "outputs/personas.md",
    "personas": "outputs/personas.md",
    "journey": "outputs/journey-map.md",
    "memo": "outputs/decision-memo.md",
    "opportunity": "outputs/opportunity-prioritization.md",
    "prioritization": "outputs/opportunity-prioritization.md",
    "mapping": None,  # output = the mapping itself, no synthesis needed
    "jobmap": "templates/jtbd.md",
}
K = 3  # default triangulation threshold


def choose_lens(goal, respondent):
    """Chooses the lens file by goal and respondent type (goal usually beats «who»)."""
    # respondent beats goal where the respondent type alone unambiguously sets the lens
    # (a candidate interview is not "expert validation"; a conflict party must not be confused with expert/stakeholder)
    if respondent in ("candidate", "conflictparty"):
        return LENS[respondent]
    # goal-override is stronger, except for org/employee
    if goal in LENS_BY_GOAL and not (goal == "org"):
        return LENS_BY_GOAL[goal]
    if goal == "brand":
        return "templates/brand-positioning.md"
    return LENS.get(respondent, "templates/org-mapping-vmdi.md")


def main():
    """CLI: builds a deterministic pipeline plan from the intake (goal/respondent/output/N)."""
    ap = argparse.ArgumentParser(
        description="Route intake answers (goal/respondent) to a lens + output + pipeline plan."
    )
    ap.add_argument("--goal", default=None, help="Required unless --sample is given")
    ap.add_argument(
        "--respondent", default=None, help="Required unless --sample is given"
    )
    ap.add_argument(
        "--output",
        default=None,
        help="Pipeline output kind (insights/persona/journey/...); if not set, inferred from --goal. "
        "NOT the display format — this script's stdout is always JSON.",
    )
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--baseline", default="no")
    ap.add_argument(
        "--sample",
        action="store_true",
        help="Run with built-in sample intake answers (--goal discovery --respondent customer --n 3)",
    )
    a = ap.parse_args()

    if a.sample:
        a.goal = a.goal or "discovery"
        a.respondent = a.respondent or "customer"
        a.n = a.n if a.n != 1 else 3
    elif not a.goal or not a.respondent:
        sys.exit("error: --goal and --respondent are required unless --sample is given")

    lens = choose_lens(a.goal, a.respondent)
    # output by goal, if not explicitly set
    default_out = {
        "org": "insights",
        "discovery": "insights",
        "experience": "journey",
        "brand": "memo",
        "prioritization": "opportunity",
        "personas": "persona",
        "expert": "memo",
        "usability": "insights",
        "exit": "insights",
        "winloss": "memo",
        "retro": "insights",
        "intercept": "insights",
        "conflict": "memo",
        "ethnography": "insights",
        "changereadiness": "memo",
    }.get(a.goal, "insights")
    out_key = a.output or default_out
    out_file = OUTPUT.get(out_key)

    can_synthesize = a.n >= K
    steps = [
        "S1 Transcript QA (number_lines → proofreading → log)",
        f"S2 Mapping by lens ({lens}) + verify_quotes + check_support + omission",
        "S3 Reliability council on unstable cells (consensus) → flag to human",
    ]
    if a.n >= 2 and out_key not in ("mapping",):
        if can_synthesize:
            steps += [
                "S5 extract_nuggets across all mappings",
                "S6 Clustering (different interviews, not quotes)",
                f"S6.5 score_insights --k {K} (triangulation, frequency×severity, tensions)",
                f"S7 Output: {out_file}",
                "S7 build_provenance + render_board (audit + board)",
            ]
        else:
            steps += [
                f"⚠ n={a.n} < k={K}: synthesis yields only watchlist, NOT insights. Add interviews or mark as pilot."
            ]
    if a.baseline.lower() in ("yes", "y", "да"):
        steps += [
            "Human↔AI comparison on rubric.md (Δ 1–5, per-block), scored by a human blind"
        ]

    caveats = [
        "Latent cells (eNPS, recognition, forecast) are always candidates for a human.",
        "Thresholds are calibrated on synthetic data only — validate on your data (references/validation.md).",
    ]
    if a.respondent == "group":
        caveats.append(
            "Group format: the coding unit is utterance+speaker, not an isolated statement. The transcript MUST be diarized (speakers labeled) — otherwise it's an S1 blocker; do not re-code by eye."
        )
    if a.respondent == "conflictparty" or a.goal == "conflict":
        caveats.append(
            "Conflict/mediation: each party gets a SEPARATE mapping file, do not mix. The «interest compatibility» cell (A2) is high-stakes — mandatory human-mediator review before use in negotiations."
        )
    if a.goal == "changereadiness":
        caveats.append(
            "Change readiness: hypotheses about hidden personal interest (A1) MUST NOT be shared with respondents without anonymization and must not be the sole basis for HR decisions without human review."
        )

    plan = {
        "goal": a.goal,
        "respondent": a.respondent,
        "n_interviews": a.n,
        "lens": lens,
        "output": out_file,
        "output_kind": out_key,
        "can_synthesize_patterns": can_synthesize,
        "k_triangulation": K,
        "pipeline": steps,
        "caveats": caveats,
    }
    print(json.dumps(plan, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
