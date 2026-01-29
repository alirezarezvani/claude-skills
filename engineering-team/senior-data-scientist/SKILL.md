---
name: senior-data-scientist
description: Data science skill for statistical modeling, experimentation, and causal inference. Includes A/B test design, sample size calculation, feature engineering analysis, and statistical hypothesis testing. CLI tools for experiment planning, data transformation recommendations, and result analysis.
---

# Senior Data Scientist

Statistical analysis, experiment design, and feature engineering toolkit for data-driven decision making.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Core Workflows](#core-workflows)
- [Tools Reference](#tools-reference)
- [Reference Documentation](#reference-documentation)
- [Validation Checklist](#validation-checklist)

---

## Quick Start

### Design an A/B Test

```bash
# Calculate sample size for 10% baseline, detecting 1% absolute lift
python scripts/experiment_designer.py --baseline 0.10 --mde 0.01

# Include duration estimate with daily traffic
python scripts/experiment_designer.py --baseline 0.10 --mde 0.01 --traffic 5000

# JSON output for programmatic use
python scripts/experiment_designer.py --baseline 0.05 --mde 0.005 --json
```

### Analyze CSV Features

```bash
# Get feature engineering recommendations for a dataset
python scripts/feature_engineering_pipeline.py data.csv

# JSON output for integration
python scripts/feature_engineering_pipeline.py data.csv --json
```

### Run Statistical Tests

```bash
# A/B test result analysis (proportions)
python scripts/model_evaluation_suite.py --ab \
  --control-success 450 --control-total 5000 \
  --treatment-success 520 --treatment-total 5000

# T-test from CSV data
python scripts/model_evaluation_suite.py data.csv --test ttest --group variant --metric revenue

# Correlation analysis
python scripts/model_evaluation_suite.py data.csv --test correlation --columns "age,income"
```

---

## Core Workflows

### Workflow 1: A/B Test Planning

Design a statistically valid experiment before launch.

**Step 1: Define parameters**
- Baseline conversion rate (from historical data)
- Minimum detectable effect (smallest meaningful change)
- Significance level (typically 0.05)
- Power (typically 0.80)

**Step 2: Calculate sample size**
```bash
python scripts/experiment_designer.py --baseline 0.10 --mde 0.01 --power 0.80
```

Example output:
```
============================================================
EXPERIMENT DESIGN
============================================================

Baseline conversion rate: 10.00%
Minimum detectable effect: 1.00% (absolute)
Expected treatment rate: 11.00%
Relative lift: 10.0%
Significance level (α): 0.05
Statistical power (1-β): 80%

────────────────────────────────────────
SAMPLE SIZE REQUIREMENTS
────────────────────────────────────────
Per group: 14,752 users
Total: 29,504 users
Actual power: 80.1%
```

**Step 3: Estimate duration**
```bash
python scripts/experiment_designer.py --baseline 0.10 --mde 0.01 --traffic 2000
```

**Step 4: Validate design**
- [ ] Sample size achievable within timeline?
- [ ] MDE aligned with business impact threshold?
- [ ] Weekly patterns accounted for (run 2+ weeks)?

### Workflow 2: Feature Engineering Analysis

Get transformation recommendations for a new dataset.

**Step 1: Analyze data**
```bash
python scripts/feature_engineering_pipeline.py customer_data.csv
```

**Step 2: Review column types**
```
COLUMN TYPE SUMMARY
──────────────────────────────────────────────────
Numeric columns: 5
Categorical columns: 3
Datetime columns: 1
ID columns (to drop): 1
```

**Step 3: Apply recommendations**
For each column, the tool suggests:
- Scaling method (StandardScaler vs RobustScaler)
- Encoding approach (One-Hot vs Target vs Frequency)
- Transformation (log, binning)
- Missing value imputation

**Step 4: Validate**
- [ ] High-cardinality categoricals handled?
- [ ] Outliers addressed?
- [ ] Missing values imputed appropriately?
- [ ] ID columns excluded?

### Workflow 3: A/B Test Result Analysis

Analyze experiment results and make ship decisions.

**Step 1: Gather results**
- Control: 450 conversions out of 5,000 users (9.0%)
- Treatment: 520 conversions out of 5,000 users (10.4%)

**Step 2: Run statistical test**
```bash
python scripts/model_evaluation_suite.py --ab \
  --control-success 450 --control-total 5000 \
  --treatment-success 520 --treatment-total 5000
```

**Step 3: Interpret results**
```
Control: 9.0% (450/5000)
Treatment: 10.4% (520/5000)

────────────────────────────────────────
DIFFERENCE
────────────────────────────────────────
Absolute difference: 1.4%
Relative lift: 15.56%
95% CI: [0.36%, 2.44%]

────────────────────────────────────────
STATISTICS
────────────────────────────────────────
z_statistic: 2.3077
p_value: 0.021011
significant_at_05: Yes

────────────────────────────────────────
RECOMMENDATION: Ship treatment
```

**Step 4: Decision checklist**
- [ ] p-value < 0.05?
- [ ] Confidence interval excludes zero?
- [ ] Effect size practically meaningful?
- [ ] Guardrail metrics OK (latency, errors)?
- [ ] Sample ratio mismatch checked?

---

## Tools Reference

### experiment_designer.py

Calculate sample sizes and experiment duration for A/B tests.

| Parameter | Flag | Default | Description |
|-----------|------|---------|-------------|
| Baseline | `--baseline`, `-b` | Required | Current conversion rate (0-1) |
| MDE | `--mde`, `-m` | Required | Minimum detectable effect (absolute) |
| Alpha | `--alpha`, `-a` | 0.05 | Significance level |
| Power | `--power`, `-p` | 0.80 | Statistical power |
| Traffic | `--traffic`, `-t` | None | Daily traffic for duration estimate |
| Traffic % | `--traffic-percent` | 100 | Percentage of traffic in experiment |
| JSON | `--json`, `-j` | False | Output as JSON |

**Example: High-power test**
```bash
python scripts/experiment_designer.py --baseline 0.05 --mde 0.005 --power 0.90 --alpha 0.01
```

### feature_engineering_pipeline.py

Analyze CSV data and generate feature transformation recommendations.

| Parameter | Flag | Description |
|-----------|------|-------------|
| Input | positional | CSV file path |
| Target | `--target`, `-t` | Target column (optional context) |
| JSON | `--json`, `-j` | Output as JSON |

**Output includes:**
- Column type detection (numeric, categorical, datetime, text, ID)
- Missing value analysis
- Distribution statistics (mean, std, skewness, outliers)
- Transformation recommendations with code snippets

### model_evaluation_suite.py

Statistical hypothesis testing for experiment analysis.

**A/B Test Mode (proportions):**
```bash
python scripts/model_evaluation_suite.py --ab \
  --control-success N --control-total M \
  --treatment-success N --treatment-total M
```

**T-Test Mode (continuous metrics):**
```bash
python scripts/model_evaluation_suite.py data.csv --test ttest \
  --group variant_column --metric metric_column
```

**Correlation Mode:**
```bash
python scripts/model_evaluation_suite.py data.csv --test correlation \
  --columns "column1,column2"
```

**Chi-Square Mode:**
```bash
python scripts/model_evaluation_suite.py data.csv --test chisquare \
  --row row_variable --column column_variable
```

---

## Reference Documentation

### Statistical Methods (`references/statistical_methods_advanced.md`)

- Hypothesis testing framework (Type I/II errors, one vs two-tailed)
- P-value interpretation and common misconceptions
- Effect size measures (Cohen's d, relative lift)
- Confidence intervals
- Causal inference methods (RCT, DiD, propensity scoring, IV)
- Bayesian A/B testing
- Time series analysis (stationarity, seasonality)
- Statistical test selection guide
- Multiple comparisons correction

### Experiment Design (`references/experiment_design_frameworks.md`)

- A/B test anatomy and metrics taxonomy
- Power analysis and sample size calculation
- Randomization schemes (simple, stratified, cluster, switchback)
- Experiment lifecycle (design → pre-checks → analysis → decision)
- Multi-armed bandits (Thompson sampling, epsilon-greedy)
- Common pitfalls (peeking, SRM, Simpson's paradox, novelty effects)

### Feature Engineering (`references/feature_engineering_patterns.md`)

- Numeric transformations (scaling, power transforms, binning)
- Categorical encoding (one-hot, target, frequency)
- Feature selection (filter, wrapper, embedded methods)
- Collinearity detection (correlation matrix, VIF)
- Time-based features (extraction, lags, rolling windows)
- Text features (TF-IDF, basic statistics)
- Production patterns (sklearn pipelines, feature stores)

---

## Validation Checklist

### Before Running Experiment

- [ ] Hypothesis clearly stated
- [ ] Primary metric defined
- [ ] Sample size calculated with adequate power (≥80%)
- [ ] Guardrail metrics identified
- [ ] Duration accounts for weekly patterns (≥2 weeks)
- [ ] Randomization unit appropriate (user, session, etc.)
- [ ] Logging verified in test environment

### Before Analyzing Results

- [ ] Sample ratio mismatch check passed (p > 0.001)
- [ ] Reached planned sample size
- [ ] No incidents during experiment period
- [ ] Data quality validated

### Before Shipping

- [ ] Primary metric significant (p < 0.05)
- [ ] Confidence interval direction matches hypothesis
- [ ] Effect size practically meaningful
- [ ] Guardrail metrics not regressed
- [ ] Segment analysis completed (no Simpson's paradox)
- [ ] Results documented

---

## Common Scenarios

### Low baseline conversion
With very low baselines (<2%), detecting small effects requires large samples:

```bash
# 1% baseline, detect 0.1% absolute change (10% relative)
python scripts/experiment_designer.py --baseline 0.01 --mde 0.001
# Result: ~785,000 per group
```

Consider larger MDE or longer duration.

### High-variance metrics (revenue)
Revenue metrics have high variance. Use larger samples or variance reduction:

```bash
# Revenue example in statistical_methods_advanced.md
# Mean=$50, Std=$100 → Coefficient of variation = 2.0
# Detecting 5% lift requires ~6,400 per group
```

### Underpowered test
If an experiment didn't reach significance:

1. Check if sample size was adequate
2. Calculate observed power
3. If underpowered, don't conclude "no effect" — extend or repeat

```bash
# Re-run with observed effect size to calculate required n
python scripts/experiment_designer.py --baseline 0.10 --mde 0.005
```
