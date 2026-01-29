#!/usr/bin/env python3
"""
Experiment Designer - A/B Test Planning Tool

Calculate sample sizes, statistical power, and experiment duration
for A/B tests and controlled experiments.

Usage:
    python experiment_designer.py --baseline 0.10 --mde 0.01
    python experiment_designer.py --baseline 0.10 --mde 0.01 --traffic 5000 --json
    python experiment_designer.py --baseline 0.10 --mde 0.01 --power 0.90 --alpha 0.01
"""

import argparse
import json
import math
import sys
from typing import Dict, Optional


def calculate_z_score(probability: float) -> float:
    """
    Approximate inverse normal CDF (z-score) using Abramowitz & Stegun formula.
    Standard library only - no scipy required.
    """
    if probability <= 0 or probability >= 1:
        raise ValueError("Probability must be between 0 and 1")

    # Handle symmetry
    if probability > 0.5:
        return -calculate_z_score(1 - probability)

    # Rational approximation for lower tail
    t = math.sqrt(-2.0 * math.log(probability))

    # Coefficients for approximation
    c0 = 2.515517
    c1 = 0.802853
    c2 = 0.010328
    d1 = 1.432788
    d2 = 0.189269
    d3 = 0.001308

    z = t - (c0 + c1 * t + c2 * t * t) / (1 + d1 * t + d2 * t * t + d3 * t * t * t)
    return -z


def sample_size_proportions(
    p_control: float,
    mde: float,
    alpha: float = 0.05,
    power: float = 0.80,
    two_tailed: bool = True
) -> int:
    """
    Calculate sample size for comparing two proportions.

    Parameters:
        p_control: Baseline conversion rate (e.g., 0.10 for 10%)
        mde: Minimum detectable effect, absolute (e.g., 0.01 for 1%)
        alpha: Significance level (default 0.05)
        power: Statistical power (default 0.80)
        two_tailed: Use two-tailed test (default True)

    Returns:
        Sample size per group
    """
    p_treatment = p_control + mde

    # Pooled proportion
    p_pooled = (p_control + p_treatment) / 2

    # Z-scores
    if two_tailed:
        z_alpha = calculate_z_score(1 - alpha / 2)
    else:
        z_alpha = calculate_z_score(1 - alpha)

    z_beta = calculate_z_score(power)

    # Sample size formula for two proportions
    numerator = (
        z_alpha * math.sqrt(2 * p_pooled * (1 - p_pooled)) +
        z_beta * math.sqrt(
            p_control * (1 - p_control) +
            p_treatment * (1 - p_treatment)
        )
    ) ** 2

    denominator = mde ** 2

    return int(math.ceil(numerator / denominator))


def sample_size_continuous(
    mean_control: float,
    std_control: float,
    mde_relative: float,
    alpha: float = 0.05,
    power: float = 0.80
) -> int:
    """
    Calculate sample size for comparing two means.

    Parameters:
        mean_control: Expected control mean
        std_control: Expected standard deviation
        mde_relative: Minimum detectable effect, relative (e.g., 0.05 for 5%)
        alpha: Significance level
        power: Statistical power

    Returns:
        Sample size per group
    """
    # Convert relative MDE to absolute
    mde_absolute = mean_control * mde_relative

    # Effect size (Cohen's d)
    effect_size = mde_absolute / std_control

    # Z-scores
    z_alpha = calculate_z_score(1 - alpha / 2)
    z_beta = calculate_z_score(power)

    # Sample size formula
    n = 2 * ((z_alpha + z_beta) / effect_size) ** 2

    return int(math.ceil(n))


def calculate_power(
    n_per_group: int,
    p_control: float,
    mde: float,
    alpha: float = 0.05
) -> float:
    """
    Calculate statistical power given sample size.

    Uses normal approximation.
    """
    p_treatment = p_control + mde
    p_pooled = (p_control + p_treatment) / 2

    z_alpha = calculate_z_score(1 - alpha / 2)

    # Standard error under null
    se_null = math.sqrt(2 * p_pooled * (1 - p_pooled) / n_per_group)

    # Standard error under alternative
    se_alt = math.sqrt(
        (p_control * (1 - p_control) + p_treatment * (1 - p_treatment)) / n_per_group
    )

    # Non-centrality parameter
    ncp = mde / se_alt

    # Critical value in terms of effect
    critical = z_alpha * se_null

    # Power = P(Z > critical - ncp)
    z_power = (critical - mde) / se_alt

    # Approximate CDF using error function
    power = 1 - 0.5 * (1 + math.erf(z_power / math.sqrt(2)))

    return min(max(power, 0), 1)


def estimate_duration(
    n_total: int,
    daily_traffic: int,
    traffic_percent: float = 100.0
) -> Dict:
    """
    Estimate experiment duration.

    Parameters:
        n_total: Total sample size needed
        daily_traffic: Daily eligible traffic
        traffic_percent: Percentage of traffic in experiment

    Returns:
        Duration estimates
    """
    effective_traffic = daily_traffic * (traffic_percent / 100)

    if effective_traffic <= 0:
        return {"error": "No traffic available"}

    days_needed = math.ceil(n_total / effective_traffic)

    return {
        "days_needed": days_needed,
        "weeks_needed": round(days_needed / 7, 1),
        "effective_daily_traffic": int(effective_traffic),
        "total_sample_size": n_total
    }


def design_experiment(
    baseline: float,
    mde: float,
    alpha: float = 0.05,
    power: float = 0.80,
    daily_traffic: Optional[int] = None,
    traffic_percent: float = 100.0,
    metric_type: str = "proportion"
) -> Dict:
    """
    Design a complete A/B test experiment.

    Returns comprehensive experiment design with sample size,
    power analysis, and duration estimates.
    """
    # Validate inputs
    if baseline <= 0 or baseline >= 1:
        return {"error": "Baseline must be between 0 and 1"}

    if mde <= 0:
        return {"error": "MDE must be positive"}

    if baseline + mde >= 1:
        return {"error": "Baseline + MDE must be less than 1"}

    # Calculate sample size
    n_per_group = sample_size_proportions(baseline, mde, alpha, power)
    n_total = 2 * n_per_group

    # Calculate actual power
    actual_power = calculate_power(n_per_group, baseline, mde, alpha)

    # Build result
    result = {
        "experiment_design": {
            "type": "A/B Test",
            "variants": 2,
            "metric_type": metric_type,
            "test_type": "two-tailed"
        },
        "parameters": {
            "baseline_rate": baseline,
            "minimum_detectable_effect": mde,
            "expected_treatment_rate": round(baseline + mde, 4),
            "relative_lift": round(mde / baseline * 100, 2),
            "significance_level": alpha,
            "target_power": power
        },
        "sample_size": {
            "per_group": n_per_group,
            "total": n_total,
            "actual_power": round(actual_power, 4)
        },
        "interpretation": {
            "if_significant": f"Treatment effect of {mde:.2%} detected with {power:.0%} confidence",
            "if_not_significant": f"Cannot detect effects smaller than {mde:.2%}"
        }
    }

    # Add duration estimates if traffic provided
    if daily_traffic:
        duration = estimate_duration(n_total, daily_traffic, traffic_percent)
        result["duration"] = duration

        # Add recommendations
        if duration.get("days_needed", 0) < 7:
            result["warning"] = "Experiment shorter than 1 week may miss weekly patterns"
        elif duration.get("days_needed", 0) > 90:
            result["warning"] = "Long experiment duration. Consider larger MDE or more traffic"

    return result


def print_human_readable(result: Dict) -> None:
    """Print experiment design in human-readable format."""
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print("\n" + "=" * 60)
    print("EXPERIMENT DESIGN")
    print("=" * 60)

    # Parameters
    params = result["parameters"]
    print(f"\nBaseline conversion rate: {params['baseline_rate']:.2%}")
    print(f"Minimum detectable effect: {params['minimum_detectable_effect']:.2%} (absolute)")
    print(f"Expected treatment rate: {params['expected_treatment_rate']:.2%}")
    print(f"Relative lift: {params['relative_lift']}%")
    print(f"Significance level (α): {params['significance_level']}")
    print(f"Statistical power (1-β): {params['target_power']:.0%}")

    # Sample size
    sample = result["sample_size"]
    print(f"\n{'─' * 40}")
    print("SAMPLE SIZE REQUIREMENTS")
    print(f"{'─' * 40}")
    print(f"Per group: {sample['per_group']:,} users")
    print(f"Total: {sample['total']:,} users")
    print(f"Actual power: {sample['actual_power']:.1%}")

    # Duration
    if "duration" in result:
        dur = result["duration"]
        print(f"\n{'─' * 40}")
        print("DURATION ESTIMATE")
        print(f"{'─' * 40}")
        print(f"Days needed: {dur['days_needed']} days")
        print(f"Weeks needed: {dur['weeks_needed']} weeks")
        print(f"Daily traffic in experiment: {dur['effective_daily_traffic']:,}")

    # Warnings
    if "warning" in result:
        print(f"\n⚠️  Warning: {result['warning']}")

    # Interpretation
    interp = result["interpretation"]
    print(f"\n{'─' * 40}")
    print("INTERPRETATION")
    print(f"{'─' * 40}")
    print(f"If significant: {interp['if_significant']}")
    print(f"If not significant: {interp['if_not_significant']}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="A/B Test Experiment Designer - Calculate sample sizes and duration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --baseline 0.10 --mde 0.01
      Design test for 10%% baseline, detecting 1%% absolute change

  %(prog)s --baseline 0.05 --mde 0.005 --traffic 10000
      Include duration estimate with 10k daily traffic

  %(prog)s --baseline 0.10 --mde 0.01 --power 0.90 --alpha 0.01
      Use 90%% power and 1%% significance level

  %(prog)s --baseline 0.10 --mde 0.01 --json
      Output as JSON for programmatic use
        """
    )

    parser.add_argument(
        "--baseline", "-b",
        type=float,
        required=True,
        help="Baseline conversion rate (e.g., 0.10 for 10%%)"
    )
    parser.add_argument(
        "--mde", "-m",
        type=float,
        required=True,
        help="Minimum detectable effect, absolute (e.g., 0.01 for 1%%)"
    )
    parser.add_argument(
        "--alpha", "-a",
        type=float,
        default=0.05,
        help="Significance level (default: 0.05)"
    )
    parser.add_argument(
        "--power", "-p",
        type=float,
        default=0.80,
        help="Statistical power (default: 0.80)"
    )
    parser.add_argument(
        "--traffic", "-t",
        type=int,
        default=None,
        help="Daily eligible traffic for duration estimate"
    )
    parser.add_argument(
        "--traffic-percent",
        type=float,
        default=100.0,
        help="Percentage of traffic in experiment (default: 100)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    # Design experiment
    result = design_experiment(
        baseline=args.baseline,
        mde=args.mde,
        alpha=args.alpha,
        power=args.power,
        daily_traffic=args.traffic,
        traffic_percent=args.traffic_percent
    )

    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_human_readable(result)

    # Exit code
    sys.exit(0 if "error" not in result else 1)


if __name__ == "__main__":
    main()
