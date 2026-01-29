#!/usr/bin/env python3
"""
Feature Engineering Pipeline - Data Transformation Tool

Analyze CSV data and generate feature engineering recommendations
based on column types, distributions, and data quality.

Usage:
    python feature_engineering_pipeline.py data.csv
    python feature_engineering_pipeline.py data.csv --json
    python feature_engineering_pipeline.py data.csv --target conversion
"""

import argparse
import csv
import json
import math
import sys
from collections import Counter
from typing import Dict, List, Optional, Tuple


def detect_column_type(values: List[str]) -> str:
    """
    Detect the semantic type of a column based on its values.

    Returns: 'numeric', 'categorical', 'datetime', 'boolean', 'text', 'id'
    """
    # Filter empty values
    non_empty = [v for v in values if v.strip()]

    if not non_empty:
        return "empty"

    # Sample for analysis
    sample = non_empty[:1000]

    # Check for boolean
    bool_values = {"true", "false", "yes", "no", "1", "0", "t", "f", "y", "n"}
    if all(v.lower() in bool_values for v in sample):
        return "boolean"

    # Check for numeric
    numeric_count = 0
    for v in sample:
        try:
            float(v.replace(",", ""))
            numeric_count += 1
        except ValueError:
            pass

    if numeric_count / len(sample) > 0.9:
        return "numeric"

    # Check for datetime patterns
    datetime_patterns = ["-", "/", ":", "T", "AM", "PM"]
    datetime_score = sum(1 for v in sample if any(p in v for p in datetime_patterns))
    if datetime_score / len(sample) > 0.8:
        # Check if looks like date
        if any(c.isdigit() for c in sample[0]):
            return "datetime"

    # Check for ID-like columns (high cardinality, sequential or UUID-like)
    unique_ratio = len(set(sample)) / len(sample)
    if unique_ratio > 0.95:
        return "id"

    # Check for text (long strings)
    avg_length = sum(len(v) for v in sample) / len(sample)
    if avg_length > 50:
        return "text"

    # Default to categorical
    return "categorical"


def analyze_numeric_column(values: List[float]) -> Dict:
    """Analyze a numeric column and provide statistics."""
    if not values:
        return {"error": "No values"}

    n = len(values)
    sorted_vals = sorted(values)

    # Basic stats
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    std = math.sqrt(variance) if variance > 0 else 0

    # Percentiles
    def percentile(p):
        idx = int(p * (n - 1))
        return sorted_vals[idx]

    q1 = percentile(0.25)
    median = percentile(0.50)
    q3 = percentile(0.75)
    iqr = q3 - q1

    # Outliers using IQR
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = [v for v in values if v < lower_bound or v > upper_bound]

    # Skewness approximation
    if std > 0:
        skewness = sum((x - mean) ** 3 for x in values) / (n * std ** 3)
    else:
        skewness = 0

    # Distribution characteristics
    distribution = "normal"
    if abs(skewness) > 1:
        distribution = "right-skewed" if skewness > 0 else "left-skewed"
    elif iqr == 0:
        distribution = "constant"

    return {
        "count": n,
        "mean": round(mean, 4),
        "std": round(std, 4),
        "min": round(min(values), 4),
        "q1": round(q1, 4),
        "median": round(median, 4),
        "q3": round(q3, 4),
        "max": round(max(values), 4),
        "outlier_count": len(outliers),
        "outlier_pct": round(len(outliers) / n * 100, 2),
        "skewness": round(skewness, 4),
        "distribution": distribution
    }


def analyze_categorical_column(values: List[str]) -> Dict:
    """Analyze a categorical column."""
    if not values:
        return {"error": "No values"}

    n = len(values)
    counter = Counter(values)
    unique_count = len(counter)

    # Top categories
    top_5 = counter.most_common(5)

    # Cardinality
    cardinality = "low" if unique_count <= 10 else "medium" if unique_count <= 100 else "high"

    # Check for rare categories
    rare_threshold = n * 0.01  # Less than 1%
    rare_categories = sum(1 for _, count in counter.items() if count < rare_threshold)

    return {
        "count": n,
        "unique_count": unique_count,
        "cardinality": cardinality,
        "top_categories": [{"value": v, "count": c, "pct": round(c / n * 100, 2)} for v, c in top_5],
        "rare_category_count": rare_categories,
        "mode": top_5[0][0] if top_5 else None,
        "mode_frequency": round(top_5[0][1] / n * 100, 2) if top_5 else 0
    }


def generate_recommendations(column_name: str, col_type: str, analysis: Dict) -> List[Dict]:
    """Generate feature engineering recommendations based on analysis."""
    recommendations = []

    if col_type == "numeric":
        # Scaling recommendation
        if analysis.get("std", 0) > 0:
            if analysis.get("outlier_pct", 0) > 5:
                recommendations.append({
                    "action": "scale",
                    "method": "RobustScaler",
                    "reason": f"High outlier percentage ({analysis['outlier_pct']}%)",
                    "code": f"from sklearn.preprocessing import RobustScaler\nscaler = RobustScaler()\ndf['{column_name}_scaled'] = scaler.fit_transform(df[['{column_name}']])"
                })
            else:
                recommendations.append({
                    "action": "scale",
                    "method": "StandardScaler",
                    "reason": "Normal distribution suitable for standard scaling",
                    "code": f"from sklearn.preprocessing import StandardScaler\nscaler = StandardScaler()\ndf['{column_name}_scaled'] = scaler.fit_transform(df[['{column_name}']])"
                })

        # Transformation for skewed data
        if abs(analysis.get("skewness", 0)) > 1:
            direction = "right" if analysis["skewness"] > 0 else "left"
            recommendations.append({
                "action": "transform",
                "method": "log1p" if direction == "right" else "square",
                "reason": f"Skewed distribution ({direction}-skewed, skewness={analysis['skewness']})",
                "code": f"import numpy as np\ndf['{column_name}_log'] = np.log1p(df['{column_name}'])" if direction == "right" else f"df['{column_name}_sq'] = df['{column_name}'] ** 2"
            })

        # Binning for continuous
        recommendations.append({
            "action": "bin",
            "method": "quantile",
            "reason": "Create categorical version for tree-based models",
            "code": f"df['{column_name}_binned'] = pd.qcut(df['{column_name}'], q=5, labels=['very_low', 'low', 'medium', 'high', 'very_high'], duplicates='drop')"
        })

    elif col_type == "categorical":
        cardinality = analysis.get("cardinality", "low")

        if cardinality == "low":
            recommendations.append({
                "action": "encode",
                "method": "OneHotEncoder",
                "reason": f"Low cardinality ({analysis['unique_count']} unique values)",
                "code": f"df = pd.get_dummies(df, columns=['{column_name}'], drop_first=True)"
            })
        elif cardinality == "medium":
            recommendations.append({
                "action": "encode",
                "method": "TargetEncoder",
                "reason": f"Medium cardinality ({analysis['unique_count']} unique values)",
                "code": f"# Use cross-validation to prevent leakage\nfrom category_encoders import TargetEncoder\nencoder = TargetEncoder(cols=['{column_name}'])\ndf['{column_name}_encoded'] = encoder.fit_transform(df['{column_name}'], df['target'])"
            })
        else:
            recommendations.append({
                "action": "encode",
                "method": "FrequencyEncoder",
                "reason": f"High cardinality ({analysis['unique_count']} unique values)",
                "code": f"freq = df['{column_name}'].value_counts(normalize=True)\ndf['{column_name}_freq'] = df['{column_name}'].map(freq)"
            })

        # Handle rare categories
        if analysis.get("rare_category_count", 0) > 0:
            recommendations.append({
                "action": "group",
                "method": "rare_category_grouping",
                "reason": f"{analysis['rare_category_count']} rare categories (< 1%)",
                "code": f"freq = df['{column_name}'].value_counts(normalize=True)\nrare = freq[freq < 0.01].index\ndf['{column_name}'] = df['{column_name}'].replace(rare, 'OTHER')"
            })

    elif col_type == "datetime":
        recommendations.append({
            "action": "extract",
            "method": "datetime_components",
            "reason": "Extract temporal features",
            "code": f"df['{column_name}'] = pd.to_datetime(df['{column_name}'])\ndf['{column_name}_year'] = df['{column_name}'].dt.year\ndf['{column_name}_month'] = df['{column_name}'].dt.month\ndf['{column_name}_dayofweek'] = df['{column_name}'].dt.dayofweek\ndf['{column_name}_is_weekend'] = df['{column_name}'].dt.dayofweek.isin([5, 6]).astype(int)"
        })
        recommendations.append({
            "action": "extract",
            "method": "cyclical_encoding",
            "reason": "Preserve cyclical nature of time",
            "code": f"import numpy as np\ndf['{column_name}_month_sin'] = np.sin(2 * np.pi * df['{column_name}'].dt.month / 12)\ndf['{column_name}_month_cos'] = np.cos(2 * np.pi * df['{column_name}'].dt.month / 12)"
        })

    elif col_type == "boolean":
        recommendations.append({
            "action": "encode",
            "method": "binary",
            "reason": "Convert to 0/1",
            "code": f"df['{column_name}'] = df['{column_name}'].map({{'true': 1, 'false': 0, 'yes': 1, 'no': 0, 'True': 1, 'False': 0}}).fillna(df['{column_name}'])"
        })

    elif col_type == "text":
        recommendations.append({
            "action": "extract",
            "method": "text_features",
            "reason": "Extract statistical text features",
            "code": f"df['{column_name}_char_count'] = df['{column_name}'].str.len()\ndf['{column_name}_word_count'] = df['{column_name}'].str.split().str.len()"
        })
        recommendations.append({
            "action": "encode",
            "method": "TF-IDF",
            "reason": "Create bag-of-words features",
            "code": f"from sklearn.feature_extraction.text import TfidfVectorizer\nvectorizer = TfidfVectorizer(max_features=100)\ntfidf = vectorizer.fit_transform(df['{column_name}'].fillna(''))"
        })

    elif col_type == "id":
        recommendations.append({
            "action": "drop",
            "method": "exclude",
            "reason": "ID columns should not be used as features",
            "code": f"df = df.drop(columns=['{column_name}'])"
        })

    return recommendations


def analyze_csv(filepath: str, target_column: Optional[str] = None) -> Dict:
    """
    Analyze a CSV file and generate feature engineering recommendations.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        return {"error": f"Failed to read CSV: {str(e)}"}

    if not rows:
        return {"error": "Empty CSV file"}

    columns = list(rows[0].keys())
    n_rows = len(rows)

    result = {
        "file": filepath,
        "rows": n_rows,
        "columns": len(columns),
        "analysis": {},
        "recommendations": {},
        "summary": {
            "numeric_columns": [],
            "categorical_columns": [],
            "datetime_columns": [],
            "text_columns": [],
            "id_columns": [],
            "boolean_columns": []
        }
    }

    for col in columns:
        values = [row[col] for row in rows]
        non_empty = [v for v in values if v.strip()]

        # Missing value analysis
        missing_count = len(values) - len(non_empty)
        missing_pct = round(missing_count / len(values) * 100, 2)

        # Detect type
        col_type = detect_column_type(values)

        # Build column analysis
        col_analysis = {
            "type": col_type,
            "missing_count": missing_count,
            "missing_pct": missing_pct
        }

        # Type-specific analysis
        if col_type == "numeric":
            numeric_values = []
            for v in non_empty:
                try:
                    numeric_values.append(float(v.replace(",", "")))
                except ValueError:
                    pass
            if numeric_values:
                col_analysis["stats"] = analyze_numeric_column(numeric_values)
            result["summary"]["numeric_columns"].append(col)

        elif col_type == "categorical":
            col_analysis["stats"] = analyze_categorical_column(non_empty)
            result["summary"]["categorical_columns"].append(col)

        elif col_type == "datetime":
            result["summary"]["datetime_columns"].append(col)

        elif col_type == "text":
            result["summary"]["text_columns"].append(col)

        elif col_type == "id":
            result["summary"]["id_columns"].append(col)

        elif col_type == "boolean":
            result["summary"]["boolean_columns"].append(col)

        # Generate recommendations
        recommendations = generate_recommendations(col, col_type, col_analysis.get("stats", {}))

        # Add missing value handling if needed
        if missing_pct > 0:
            if col_type == "numeric":
                recommendations.insert(0, {
                    "action": "impute",
                    "method": "median",
                    "reason": f"Handle {missing_pct}% missing values",
                    "code": f"df['{col}'].fillna(df['{col}'].median(), inplace=True)"
                })
            elif col_type in ["categorical", "text"]:
                recommendations.insert(0, {
                    "action": "impute",
                    "method": "mode_or_constant",
                    "reason": f"Handle {missing_pct}% missing values",
                    "code": f"df['{col}'].fillna('MISSING', inplace=True)"
                })

        result["analysis"][col] = col_analysis
        result["recommendations"][col] = recommendations

    return result


def print_human_readable(result: Dict) -> None:
    """Print analysis in human-readable format."""
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print("\n" + "=" * 70)
    print("FEATURE ENGINEERING ANALYSIS")
    print("=" * 70)
    print(f"\nFile: {result['file']}")
    print(f"Rows: {result['rows']:,}")
    print(f"Columns: {result['columns']}")

    # Summary
    summary = result["summary"]
    print(f"\n{'─' * 50}")
    print("COLUMN TYPE SUMMARY")
    print(f"{'─' * 50}")
    print(f"Numeric columns: {len(summary['numeric_columns'])}")
    print(f"Categorical columns: {len(summary['categorical_columns'])}")
    print(f"Datetime columns: {len(summary['datetime_columns'])}")
    print(f"Text columns: {len(summary['text_columns'])}")
    print(f"Boolean columns: {len(summary['boolean_columns'])}")
    print(f"ID columns (to drop): {len(summary['id_columns'])}")

    # Per-column analysis and recommendations
    print(f"\n{'=' * 70}")
    print("COLUMN ANALYSIS & RECOMMENDATIONS")
    print("=" * 70)

    for col, analysis in result["analysis"].items():
        print(f"\n{'─' * 50}")
        print(f"Column: {col}")
        print(f"{'─' * 50}")
        print(f"Type: {analysis['type']}")
        print(f"Missing: {analysis['missing_count']} ({analysis['missing_pct']}%)")

        if "stats" in analysis:
            stats = analysis["stats"]
            if analysis["type"] == "numeric":
                print(f"Mean: {stats['mean']}, Std: {stats['std']}")
                print(f"Range: [{stats['min']}, {stats['max']}]")
                print(f"Distribution: {stats['distribution']}")
                if stats['outlier_count'] > 0:
                    print(f"Outliers: {stats['outlier_count']} ({stats['outlier_pct']}%)")
            elif analysis["type"] == "categorical":
                print(f"Unique values: {stats['unique_count']} ({stats['cardinality']} cardinality)")
                print(f"Mode: {stats['mode']} ({stats['mode_frequency']}%)")

        # Recommendations
        recs = result["recommendations"].get(col, [])
        if recs:
            print("\nRecommendations:")
            for i, rec in enumerate(recs, 1):
                print(f"  {i}. [{rec['action'].upper()}] {rec['method']}")
                print(f"     Reason: {rec['reason']}")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Feature Engineering Pipeline - Analyze CSV and generate recommendations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.csv
      Analyze data.csv and show recommendations

  %(prog)s data.csv --json
      Output analysis as JSON

  %(prog)s data.csv --target conversion
      Specify target column for context
        """
    )

    parser.add_argument(
        "input",
        help="Input CSV file path"
    )
    parser.add_argument(
        "--target", "-t",
        help="Target column name (for context)"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )

    args = parser.parse_args()

    # Analyze
    result = analyze_csv(args.input, args.target)

    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_human_readable(result)

    # Exit code
    sys.exit(0 if "error" not in result else 1)


if __name__ == "__main__":
    main()
