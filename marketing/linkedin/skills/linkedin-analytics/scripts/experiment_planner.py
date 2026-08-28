#!/usr/bin/env python3
"""experiment_planner.py — turn a LinkedIn hypothesis into a test you could actually lose.

A pattern found in past posts is a hypothesis. This sizes the deliberate test:
how many posts per arm, how many weeks that takes at your cadence, what to hold
constant, and — the part that gets skipped — what result would make you abandon
the idea.

Sizing uses the standard two-sample formula with the coefficient of variation of
your own engagement rate:

    n per arm = 2 * (z_alpha/2 + z_beta)^2 * CV^2 / effect^2

Get CV from post_performance_analyzer.py: a robust estimate is
1.4826 * MAD / median. It is typically 0.3-0.6 for an established account and
higher for a new one, which is why honest LinkedIn experiments need more posts
than people expect.

Treat the number as a planning estimate, not inference. Engagement rate is
heavy-tailed and posts are not independent draws — the same week's news moves all
of them. Analyse the result with pattern_miner.py's permutation test rather than
a t-test.

Exit codes:
  0  FEASIBLE     — the test fits the window
  2  TOO_LONG     — does not fit; the minimum detectable effect in the window is returned
  3  REFUSED      — the hypothesis or the effect size is not worth testing

Stdlib only. No network. Deterministic.
"""

import argparse
import json
import math
import sys

# Two-sided z for alpha, one-sided z for power. Small table, no scipy.
Z_ALPHA = {0.20: 1.282, 0.10: 1.645, 0.05: 1.960}
Z_POWER = {0.70: 0.524, 0.80: 0.842, 0.90: 1.282}

MIN_ACTIONABLE_EFFECT = 0.10

CONFOUNDS = [
    "Post at the same time of day in both arms. Time of day and day of week move "
    "engagement more than most of the variables people test.",
    "Alternate arms post by post. Running arm A for a month and arm B for the next month "
    "tests the month, not the variable.",
    "Hold the pillar mix steady. If arm A is all your strongest topic, you measured the topic.",
    "Do not change the profile, headline, or posting cadence mid-test.",
    "Log the arm before you publish, not after. Deciding which arm a post belonged to once "
    "you have seen the numbers is how every informal test goes wrong.",
]

# Chosen to be feasible so the sample shows the full happy path. Note how narrow
# the feasible region is: at CV 0.45 and a 30% target effect this same test needs
# 28 weeks. Most LinkedIn "A/B tests" people describe are not runnable at their
# actual posting volume, and the tool says so rather than pretending otherwise.
SAMPLE = {
    "hypothesis": "Document carousels earn a higher engagement rate than text posts for my audience",
    "variable": "format (document-carousel vs text-post)",
    "baseline_median_er": 0.025,
    "cv": 0.35,
    "effect": 0.40,
    "posts_per_week": 3,
    "max_weeks": 16,
}


def plan(hypothesis: str, variable: str, cv: float, effect: float,
         posts_per_week: float, max_weeks: int, alpha: float, power: float,
         baseline: float) -> dict:
    if not hypothesis.strip() or not variable.strip():
        return {"verdict": "REFUSED", "exit_code": 3,
                "finding": "No hypothesis or no named variable.",
                "fix": "State it as a sentence you could be wrong about: 'X earns a higher "
                       "engagement rate than Y for my audience.' If you cannot say what would "
                       "disprove it, it is a preference, not a hypothesis."}
    if effect < MIN_ACTIONABLE_EFFECT:
        return {"verdict": "REFUSED", "exit_code": 3,
                "finding": f"A {effect:.0%} relative effect is below the "
                           f"{MIN_ACTIONABLE_EFFECT:.0%} floor.",
                "fix": "Test something you would actually change your approach over. Detecting a "
                       "5% difference needs hundreds of posts and would not change a single "
                       "decision when you found it."}
    if cv <= 0:
        return {"verdict": "REFUSED", "exit_code": 3,
                "finding": "Coefficient of variation must be positive.",
                "fix": "Run post_performance_analyzer.py and compute 1.4826 * MAD / median. "
                       "With fewer than 10 posts you do not have a usable CV yet."}

    z_a = Z_ALPHA[alpha]
    z_b = Z_POWER[power]
    n_per_arm = math.ceil(2 * (z_a + z_b) ** 2 * cv ** 2 / effect ** 2)
    total = n_per_arm * 2
    weeks = math.ceil(total / posts_per_week) if posts_per_week > 0 else 10 ** 6

    common = {
        "hypothesis": hypothesis.strip(),
        "variable": variable.strip(),
        "design": {
            "arms": 2, "alpha": alpha, "power": power, "cv": cv,
            "target_relative_effect": effect,
            "baseline_median_engagement_rate": baseline,
            "posts_per_arm": n_per_arm, "total_posts": total,
            "weeks_at_cadence": weeks, "posts_per_week": posts_per_week,
        },
        "hold_constant": CONFOUNDS,
        "analysis_rule": "Analyse with pattern_miner.py (difference of medians, permutation "
                         "test). Do not use a t-test: engagement rate is heavy-tailed and one "
                         "breakout post will carry a mean on its own.",
        "caveat": "Posts are not independent draws — a busy news week moves every arm at once. "
                  "This sizing is a planning aid, not a guarantee of power.",
    }

    if weeks > max_weeks:
        affordable_per_arm = max(1, int(max_weeks * posts_per_week / 2))
        mde = math.sqrt(2 * (z_a + z_b) ** 2 * cv ** 2 / affordable_per_arm)
        return {**common, "verdict": "TOO_LONG", "exit_code": 2,
                "finding": f"{total} posts at {posts_per_week}/week is {weeks} weeks, past the "
                           f"{max_weeks}-week window.",
                "options": [
                    f"Accept a bigger minimum detectable effect: in {max_weeks} weeks you can "
                    f"detect about {mde:.0%} relative, not {effect:.0%}. If a {mde:.0%} "
                    "difference would still change your decision, run it.",
                    "Raise the cadence — but only if the cadence is sustainable for the whole "
                    "window; an abandoned test is worse than none.",
                    "Accept lower power (0.70) and treat the result as directional.",
                    "Do not run it, and pick the option you would rather write anyway. Not every "
                    "question is worth a quarter of your output.",
                ],
                "minimum_detectable_effect_in_window": round(mde, 3),
                "stop_rule": "If you change the plan mid-test, the test is over. Start again or "
                             "accept the result as anecdote."}

    return {**common, "verdict": "FEASIBLE", "exit_code": 0,
            "schedule": f"{n_per_arm} posts per arm, alternating, {posts_per_week}/week — "
                        f"{weeks} weeks.",
            "falsification": f"If the median engagement rate of the {variable.strip()} arm is not "
                             f"at least {effect:.0%} above the other arm at the end of the window, "
                             "the hypothesis failed. Write that down now, before the first post.",
            "stop_rule": [
                "Run the full window. Stopping early because the numbers look good is how a "
                "coin flip becomes a strategy.",
                "One exception: stop if something outside the test changes — a job change, a "
                "viral post, a LinkedIn product change. Then restart rather than salvage.",
            ]}


def render_human(r: dict) -> str:
    if r["verdict"] == "REFUSED":
        return (f"Experiment: REFUSED\n{'=' * 44}\n{r['finding']}\nfix → {r['fix']}")
    d = r["design"]
    lines = [f"Experiment: {r['verdict']}", "=" * 60,
             f"Hypothesis : {r['hypothesis']}",
             f"Variable   : {r['variable']}",
             f"Design     : 2 arms, alpha {d['alpha']}, power {d['power']}, CV {d['cv']}, "
             f"target effect {d['target_relative_effect']:.0%}",
             f"Sample     : {d['posts_per_arm']} posts/arm ({d['total_posts']} total) = "
             f"{d['weeks_at_cadence']} weeks at {d['posts_per_week']}/week", ""]
    if r["verdict"] == "TOO_LONG":
        lines += [r["finding"], "", "Options:"]
        for o in r["options"]:
            lines.append(f"  - {o}")
        lines += ["", f"Stop rule: {r['stop_rule']}"]
    else:
        lines += [f"Schedule   : {r['schedule']}", "",
                  f"Falsification: {r['falsification']}", "", "Stop rule:"]
        for s in r["stop_rule"]:
            lines.append(f"  - {s}")
    lines.append("\nHold constant:")
    for c in r["hold_constant"]:
        lines.append(f"  - {c}")
    lines += ["", r["analysis_rule"], "", r["caveat"]]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Size a LinkedIn posting experiment "
                    "(feasible=0 / too-long=2 / refused=3).")
    ap.add_argument("--hypothesis", default="", help="The claim, stated so it can fail.")
    ap.add_argument("--variable", default="", help="The one thing that differs between arms.")
    ap.add_argument("--cv", type=float, default=0.0,
                    help="Coefficient of variation of your engagement rate "
                         "(1.4826 * MAD / median from post_performance_analyzer.py).")
    ap.add_argument("--effect", type=float, default=0.30,
                    help="Relative effect you would act on (default 0.30 = 30%%).")
    ap.add_argument("--posts-per-week", type=float, default=2.0)
    ap.add_argument("--max-weeks", type=int, default=12)
    ap.add_argument("--alpha", type=float, choices=sorted(Z_ALPHA), default=0.10)
    ap.add_argument("--power", type=float, choices=sorted(Z_POWER), default=0.80)
    ap.add_argument("--baseline-er", type=float, default=0.0,
                    help="Your median engagement rate, for reference in the output.")
    ap.add_argument("--output", choices=["json", "human"], default="json")
    ap.add_argument("--sample", action="store_true", help="Size a built-in example experiment.")
    args = ap.parse_args()

    if args.sample:
        s = SAMPLE
        result = plan(s["hypothesis"], s["variable"], s["cv"], s["effect"],
                      s["posts_per_week"], s["max_weeks"], 0.10, 0.80,
                      s["baseline_median_er"])
    else:
        if not args.hypothesis:
            ap.error("--hypothesis is required (or use --sample)")
        result = plan(args.hypothesis, args.variable, args.cv, args.effect,
                      args.posts_per_week, args.max_weeks, args.alpha, args.power,
                      args.baseline_er)

    print(json.dumps(result, indent=2) if args.output == "json" else render_human(result))
    return result["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
