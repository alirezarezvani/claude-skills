#!/usr/bin/env python3
"""
Statistical Analysis Suite - Hypothesis Testing & Analysis Tool

Perform statistical tests on CSV data including t-tests, chi-square tests,
correlation analysis, and A/B test result analysis.

Usage:
    python model_evaluation_suite.py data.csv --test ttest --group treatment --metric conversion
    python model_evaluation_suite.py data.csv --test correlation --columns "age,income,score"
    python model_evaluation_suite.py --ab --control-success 450 --control-total 5000 --treatment-success 520 --treatment-total 5000
"""

import argparse
import csv
import json
import math
import sys
from collections import Counter
from typing import Dict, List, Optional, Tuple


def calculate_z_score(probability: float) -> float:
    """Approximate inverse normal CDF using Abramowitz & Stegun formula."""
    if probability <= 0 or probability >= 1:
        raise ValueError("Probability must be between 0 and 1")

    if probability > 0.5:
        return -calculate_z_score(1 - probability)

    t = math.sqrt(-2.0 * math.log(probability))
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d1, d2, d3 = 1.432788, 0.189269, 0.001308

    z = t - (c0 + c1 * t + c2 * t * t) / (1 + d1 * t + d2 * t * t + d3 * t * t * t)
    return -z


def normal_cdf(z: float) -> float:
    """Approximate normal CDF using error function."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def t_distribution_cdf(t: float, df: int) -> float:
    """
    Approximate t-distribution CDF.
    For large df, approaches normal distribution.
    """
    if df > 100:
        return normal_cdf(t)

    # Approximation for t-distribution
    x = df / (df + t * t)
    # Use incomplete beta function approximation
    if t >= 0:
        return 1 - 0.5 * incomplete_beta(df / 2, 0.5, x)
    else:
        return 0.5 * incomplete_beta(df / 2, 0.5, x)


def incomplete_beta(a: float, b: float, x: float) -> float:
    """Approximation of incomplete beta function using continued fraction."""
    if x == 0 or x == 1:
        return x

    # Simple approximation
    bt = math.exp(
        math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) +
        a * math.log(x) + b * math.log(1 - x)
    )

    if x < (a + 1) / (a + b + 2):
        return bt * beta_cf(a, b, x) / a
    else:
        return 1 - bt * beta_cf(b, a, 1 - x) / b


def beta_cf(a: float, b: float, x: float) -> float:
    """Continued fraction for incomplete beta."""
    max_iter = 100
    eps = 1e-10

    qab = a + b
    qap = a + 1
    qam = a - 1
    c = 1
    d = 1 - qab * x / qap

    if abs(d) < eps:
        d = eps
    d = 1 / d
    h = d

    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        if abs(d) < eps:
            d = eps
        c = 1 + aa / c
        if abs(c) < eps:
            c = eps
        d = 1 / d
        h *= d * c

        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        if abs(d) < eps:
            d = eps
        c = 1 + aa / c
        if abs(c) < eps:
            c = eps
        d = 1 / d
        delta = d * c
        h *= delta

        if abs(delta - 1) < eps:
            break

    return h


def two_sample_ttest(group1: List[float], group2: List[float], equal_var: bool = False) -> Dict:
    """
    Perform two-sample t-test (Welch's t-test by default).

    Parameters:
        group1: First group of values
        group2: Second group of values
        equal_var: If True, use pooled variance (Student's t-test)

    Returns:
        Test results including t-statistic, p-value, and effect size
    """
    n1, n2 = len(group1), len(group2)

    if n1 < 2 or n2 < 2:
        return {"error": "Each group needs at least 2 observations"}

    # Means
    mean1 = sum(group1) / n1
    mean2 = sum(group2) / n2

    # Variances
    var1 = sum((x - mean1) ** 2 for x in group1) / (n1 - 1)
    var2 = sum((x - mean2) ** 2 for x in group2) / (n2 - 1)

    # Standard deviations
    std1 = math.sqrt(var1)
    std2 = math.sqrt(var2)

    if equal_var:
        # Pooled variance (Student's t-test)
        pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
        se = math.sqrt(pooled_var * (1 / n1 + 1 / n2))
        df = n1 + n2 - 2
    else:
        # Welch's t-test (unequal variances)
        se = math.sqrt(var1 / n1 + var2 / n2)
        # Welch-Satterthwaite degrees of freedom
        numerator = (var1 / n1 + var2 / n2) ** 2
        denominator = (var1 / n1) ** 2 / (n1 - 1) + (var2 / n2) ** 2 / (n2 - 1)
        df = numerator / denominator if denominator > 0 else n1 + n2 - 2

    if se == 0:
        return {"error": "No variance in data"}

    # T-statistic
    t_stat = (mean1 - mean2) / se

    # P-value (two-tailed)
    p_value = 2 * (1 - t_distribution_cdf(abs(t_stat), int(df)))

    # Effect size (Cohen's d)
    pooled_std = math.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    cohens_d = (mean1 - mean2) / pooled_std if pooled_std > 0 else 0

    # Effect size interpretation
    d_abs = abs(cohens_d)
    if d_abs < 0.2:
        effect_interpretation = "negligible"
    elif d_abs < 0.5:
        effect_interpretation = "small"
    elif d_abs < 0.8:
        effect_interpretation = "medium"
    else:
        effect_interpretation = "large"

    return {
        "test": "Two-sample t-test" + (" (Welch)" if not equal_var else " (Student)"),
        "group1": {
            "n": n1,
            "mean": round(mean1, 4),
            "std": round(std1, 4)
        },
        "group2": {
            "n": n2,
            "mean": round(mean2, 4),
            "std": round(std2, 4)
        },
        "difference": {
            "mean_diff": round(mean1 - mean2, 4),
            "relative_diff": round((mean1 - mean2) / mean2 * 100, 2) if mean2 != 0 else None
        },
        "statistics": {
            "t_statistic": round(t_stat, 4),
            "degrees_of_freedom": round(df, 2),
            "p_value": round(p_value, 6),
            "significant_at_05": p_value < 0.05,
            "significant_at_01": p_value < 0.01
        },
        "effect_size": {
            "cohens_d": round(cohens_d, 4),
            "interpretation": effect_interpretation
        }
    }


def chi_square_test(observed: List[List[int]]) -> Dict:
    """
    Perform chi-square test of independence.

    Parameters:
        observed: 2D list of observed counts (contingency table)

    Returns:
        Test results including chi-square statistic and p-value
    """
    rows = len(observed)
    cols = len(observed[0])

    # Calculate row and column totals
    row_totals = [sum(row) for row in observed]
    col_totals = [sum(observed[r][c] for r in range(rows)) for c in range(cols)]
    total = sum(row_totals)

    if total == 0:
        return {"error": "No observations"}

    # Calculate expected frequencies
    expected = []
    for r in range(rows):
        exp_row = []
        for c in range(cols):
            exp_val = (row_totals[r] * col_totals[c]) / total
            exp_row.append(exp_val)
        expected.append(exp_row)

    # Calculate chi-square statistic
    chi2 = 0
    for r in range(rows):
        for c in range(cols):
            if expected[r][c] > 0:
                chi2 += (observed[r][c] - expected[r][c]) ** 2 / expected[r][c]

    # Degrees of freedom
    df = (rows - 1) * (cols - 1)

    # P-value approximation using chi-square distribution
    # Using Wilson-Hilferty approximation
    if df > 0:
        z = ((chi2 / df) ** (1/3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df))
        p_value = 1 - normal_cdf(z)
    else:
        p_value = 1.0

    # Cramér's V (effect size)
    min_dim = min(rows - 1, cols - 1)
    cramers_v = math.sqrt(chi2 / (total * min_dim)) if min_dim > 0 and total > 0 else 0

    return {
        "test": "Chi-square test of independence",
        "contingency_table": {
            "observed": observed,
            "expected": [[round(e, 2) for e in row] for row in expected]
        },
        "statistics": {
            "chi_square": round(chi2, 4),
            "degrees_of_freedom": df,
            "p_value": round(p_value, 6),
            "significant_at_05": p_value < 0.05
        },
        "effect_size": {
            "cramers_v": round(cramers_v, 4),
            "interpretation": "small" if cramers_v < 0.3 else "medium" if cramers_v < 0.5 else "large"
        }
    }


def pearson_correlation(x: List[float], y: List[float]) -> Dict:
    """
    Calculate Pearson correlation coefficient.
    """
    n = len(x)
    if n != len(y):
        return {"error": "Lists must have same length"}
    if n < 3:
        return {"error": "Need at least 3 observations"}

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    # Covariance and variances
    cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    var_x = sum((xi - mean_x) ** 2 for xi in x)
    var_y = sum((yi - mean_y) ** 2 for yi in y)

    if var_x == 0 or var_y == 0:
        return {"error": "No variance in one or both variables"}

    # Correlation
    r = cov / math.sqrt(var_x * var_y)

    # T-statistic for significance test
    if abs(r) < 1:
        t_stat = r * math.sqrt((n - 2) / (1 - r ** 2))
        df = n - 2
        p_value = 2 * (1 - t_distribution_cdf(abs(t_stat), df))
    else:
        t_stat = float('inf') if r > 0 else float('-inf')
        p_value = 0

    # Interpretation
    r_abs = abs(r)
    if r_abs < 0.1:
        strength = "negligible"
    elif r_abs < 0.3:
        strength = "weak"
    elif r_abs < 0.5:
        strength = "moderate"
    elif r_abs < 0.7:
        strength = "strong"
    else:
        strength = "very strong"

    direction = "positive" if r > 0 else "negative"

    return {
        "test": "Pearson correlation",
        "statistics": {
            "r": round(r, 4),
            "r_squared": round(r ** 2, 4),
            "t_statistic": round(t_stat, 4),
            "p_value": round(p_value, 6),
            "significant_at_05": p_value < 0.05
        },
        "interpretation": {
            "strength": strength,
            "direction": direction,
            "description": f"{strength.capitalize()} {direction} correlation"
        }
    }


def proportions_test(successes1: int, total1: int, successes2: int, total2: int) -> Dict:
    """
    Two-proportion z-test for A/B testing.

    Parameters:
        successes1: Successes in control group
        total1: Total in control group
        successes2: Successes in treatment group
        total2: Total in treatment group
    """
    if total1 == 0 or total2 == 0:
        return {"error": "Cannot have zero total"}

    p1 = successes1 / total1
    p2 = successes2 / total2

    # Pooled proportion
    p_pooled = (successes1 + successes2) / (total1 + total2)

    # Standard error
    se = math.sqrt(p_pooled * (1 - p_pooled) * (1 / total1 + 1 / total2))

    if se == 0:
        return {"error": "No variance - proportions are 0 or 1"}

    # Z-statistic
    z = (p2 - p1) / se

    # P-value (two-tailed)
    p_value = 2 * (1 - normal_cdf(abs(z)))

    # Confidence interval for difference
    se_diff = math.sqrt(p1 * (1 - p1) / total1 + p2 * (1 - p2) / total2)
    ci_lower = (p2 - p1) - 1.96 * se_diff
    ci_upper = (p2 - p1) + 1.96 * se_diff

    # Relative lift
    lift = (p2 - p1) / p1 if p1 > 0 else None
    lift_ci_lower = ci_lower / p1 if p1 > 0 else None
    lift_ci_upper = ci_upper / p1 if p1 > 0 else None

    return {
        "test": "Two-proportion z-test",
        "control": {
            "successes": successes1,
            "total": total1,
            "rate": round(p1, 4),
            "rate_pct": round(p1 * 100, 2)
        },
        "treatment": {
            "successes": successes2,
            "total": total2,
            "rate": round(p2, 4),
            "rate_pct": round(p2 * 100, 2)
        },
        "difference": {
            "absolute": round(p2 - p1, 4),
            "absolute_pct": round((p2 - p1) * 100, 2),
            "relative_lift": round(lift * 100, 2) if lift else None,
            "ci_95_lower": round(ci_lower * 100, 2),
            "ci_95_upper": round(ci_upper * 100, 2)
        },
        "statistics": {
            "z_statistic": round(z, 4),
            "p_value": round(p_value, 6),
            "significant_at_05": p_value < 0.05,
            "significant_at_01": p_value < 0.01
        },
        "recommendation": "Ship treatment" if p_value < 0.05 and p2 > p1 else
                         "Ship control (treatment worse)" if p_value < 0.05 and p2 < p1 else
                         "No significant difference detected"
    }


def load_csv_data(filepath: str) -> Tuple[List[str], List[Dict]]:
    """Load CSV file and return headers and rows."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames or []
    return headers, rows


def extract_numeric_column(rows: List[Dict], column: str) -> List[float]:
    """Extract numeric values from a column."""
    values = []
    for row in rows:
        try:
            val = float(row.get(column, '').replace(',', ''))
            values.append(val)
        except (ValueError, TypeError):
            pass
    return values


def print_result(result: Dict, output_json: bool = False) -> None:
    """Print analysis result."""
    if output_json:
        print(json.dumps(result, indent=2))
        return

    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print("\n" + "=" * 60)
    print(f"STATISTICAL TEST: {result.get('test', 'Unknown')}")
    print("=" * 60)

    # Print sections based on test type
    if "group1" in result and "group2" in result:
        print(f"\nGroup 1: n={result['group1']['n']}, mean={result['group1']['mean']}, std={result['group1']['std']}")
        print(f"Group 2: n={result['group2']['n']}, mean={result['group2']['mean']}, std={result['group2']['std']}")

    if "control" in result and "treatment" in result:
        print(f"\nControl: {result['control']['rate_pct']}% ({result['control']['successes']}/{result['control']['total']})")
        print(f"Treatment: {result['treatment']['rate_pct']}% ({result['treatment']['successes']}/{result['treatment']['total']})")

    if "difference" in result:
        diff = result["difference"]
        print(f"\n{'─' * 40}")
        print("DIFFERENCE")
        print(f"{'─' * 40}")
        if "absolute_pct" in diff:
            print(f"Absolute difference: {diff['absolute_pct']}%")
        if "relative_lift" in diff and diff["relative_lift"] is not None:
            print(f"Relative lift: {diff['relative_lift']}%")
        if "ci_95_lower" in diff:
            print(f"95% CI: [{diff['ci_95_lower']}%, {diff['ci_95_upper']}%]")
        if "mean_diff" in diff:
            print(f"Mean difference: {diff['mean_diff']}")

    if "statistics" in result:
        stats = result["statistics"]
        print(f"\n{'─' * 40}")
        print("STATISTICS")
        print(f"{'─' * 40}")
        for key, val in stats.items():
            if key.startswith("significant"):
                print(f"{key}: {'Yes' if val else 'No'}")
            else:
                print(f"{key}: {val}")

    if "effect_size" in result:
        effect = result["effect_size"]
        print(f"\n{'─' * 40}")
        print("EFFECT SIZE")
        print(f"{'─' * 40}")
        for key, val in effect.items():
            print(f"{key}: {val}")

    if "interpretation" in result:
        print(f"\n{'─' * 40}")
        print("INTERPRETATION")
        print(f"{'─' * 40}")
        if isinstance(result["interpretation"], dict):
            for key, val in result["interpretation"].items():
                print(f"{key}: {val}")
        else:
            print(result["interpretation"])

    if "recommendation" in result:
        print(f"\n{'─' * 40}")
        print(f"RECOMMENDATION: {result['recommendation']}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Statistical Analysis Suite - Hypothesis testing and analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # T-test from CSV
  %(prog)s data.csv --test ttest --group variant --metric revenue

  # Correlation analysis
  %(prog)s data.csv --test correlation --columns "age,income"

  # A/B test proportions (direct input)
  %(prog)s --ab --control-success 450 --control-total 5000 \\
           --treatment-success 520 --treatment-total 5000

  # Chi-square test
  %(prog)s data.csv --test chisquare --row category --column outcome
        """
    )

    # Input source
    parser.add_argument("input", nargs="?", help="Input CSV file")

    # Test type
    parser.add_argument("--test", "-t", choices=["ttest", "correlation", "chisquare"],
                        help="Statistical test to perform")

    # For t-test
    parser.add_argument("--group", "-g", help="Column containing group labels")
    parser.add_argument("--metric", "-m", help="Column containing metric values")

    # For correlation
    parser.add_argument("--columns", "-c", help="Comma-separated column names for correlation")

    # For chi-square
    parser.add_argument("--row", help="Row variable for chi-square")
    parser.add_argument("--column", help="Column variable for chi-square")

    # For direct A/B test input
    parser.add_argument("--ab", action="store_true", help="Run A/B test with direct inputs")
    parser.add_argument("--control-success", type=int, help="Control group successes")
    parser.add_argument("--control-total", type=int, help="Control group total")
    parser.add_argument("--treatment-success", type=int, help="Treatment group successes")
    parser.add_argument("--treatment-total", type=int, help="Treatment group total")

    # Output
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    result = {}

    # Direct A/B test
    if args.ab:
        if not all([args.control_success is not None, args.control_total,
                    args.treatment_success is not None, args.treatment_total]):
            print("Error: --ab requires --control-success, --control-total, "
                  "--treatment-success, --treatment-total")
            sys.exit(1)

        result = proportions_test(
            args.control_success, args.control_total,
            args.treatment_success, args.treatment_total
        )

    # CSV-based tests
    elif args.input and args.test:
        try:
            headers, rows = load_csv_data(args.input)
        except Exception as e:
            print(f"Error loading CSV: {e}")
            sys.exit(1)

        if args.test == "ttest":
            if not args.group or not args.metric:
                print("Error: t-test requires --group and --metric")
                sys.exit(1)

            # Split data by group
            groups = {}
            for row in rows:
                grp = row.get(args.group, '')
                if grp not in groups:
                    groups[grp] = []
                try:
                    val = float(row.get(args.metric, '').replace(',', ''))
                    groups[grp].append(val)
                except (ValueError, TypeError):
                    pass

            group_names = list(groups.keys())
            if len(group_names) != 2:
                print(f"Error: t-test requires exactly 2 groups, found {len(group_names)}: {group_names}")
                sys.exit(1)

            result = two_sample_ttest(groups[group_names[0]], groups[group_names[1]])
            result["groups"] = {"group1": group_names[0], "group2": group_names[1]}

        elif args.test == "correlation":
            if not args.columns:
                print("Error: correlation requires --columns")
                sys.exit(1)

            cols = [c.strip() for c in args.columns.split(',')]
            if len(cols) != 2:
                print("Error: correlation requires exactly 2 columns")
                sys.exit(1)

            x = extract_numeric_column(rows, cols[0])
            y = extract_numeric_column(rows, cols[1])

            # Align lengths
            min_len = min(len(x), len(y))
            result = pearson_correlation(x[:min_len], y[:min_len])
            result["variables"] = {"x": cols[0], "y": cols[1]}

        elif args.test == "chisquare":
            if not args.row or not args.column:
                print("Error: chi-square requires --row and --column")
                sys.exit(1)

            # Build contingency table
            counts = {}
            for row in rows:
                r_val = row.get(args.row, '')
                c_val = row.get(args.column, '')
                if r_val and c_val:
                    if r_val not in counts:
                        counts[r_val] = {}
                    counts[r_val][c_val] = counts[r_val].get(c_val, 0) + 1

            row_labels = list(counts.keys())
            col_labels = list(set(c for r in counts.values() for c in r.keys()))

            observed = []
            for r in row_labels:
                row_vals = [counts[r].get(c, 0) for c in col_labels]
                observed.append(row_vals)

            result = chi_square_test(observed)
            result["labels"] = {"rows": row_labels, "columns": col_labels}

    else:
        parser.print_help()
        sys.exit(0)

    print_result(result, args.json)
    sys.exit(0 if "error" not in result else 1)


if __name__ == "__main__":
    main()
