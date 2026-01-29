# Advanced Statistical Methods for Data Science

Comprehensive reference for hypothesis testing, causal inference, and statistical analysis in production systems.

---

## Table of Contents

- [Hypothesis Testing](#hypothesis-testing)
- [Statistical Significance](#statistical-significance)
- [Causal Inference](#causal-inference)
- [Bayesian Methods](#bayesian-methods)
- [Time Series Analysis](#time-series-analysis)
- [Common Statistical Tests](#common-statistical-tests)

---

## Hypothesis Testing

### Framework

```
1. State null hypothesis (H₀) and alternative (H₁)
2. Choose significance level (α, typically 0.05)
3. Calculate test statistic
4. Compute p-value
5. Compare p-value to α
6. Make decision and interpret
```

### Types of Errors

| Error Type | Description | Consequence |
|------------|-------------|-------------|
| **Type I (α)** | Reject H₀ when true | False positive - ship bad feature |
| **Type II (β)** | Fail to reject H₀ when false | False negative - miss good feature |

**Trade-off:** Lowering α increases β and vice versa.

### One-Tailed vs Two-Tailed Tests

| Test Type | Use When | Example |
|-----------|----------|---------|
| **One-tailed** | Direction is known | "New version increases conversion" |
| **Two-tailed** | Direction unknown | "New version affects conversion" |

```python
# Two-tailed test
from scipy import stats

t_stat, p_value = stats.ttest_ind(group_a, group_b)
is_significant = p_value < alpha

# One-tailed test (upper)
p_value_one_tail = p_value / 2
is_significant = (t_stat > 0) and (p_value_one_tail < alpha)
```

---

## Statistical Significance

### P-Value Interpretation

| P-Value | Interpretation |
|---------|----------------|
| < 0.01 | Strong evidence against H₀ |
| 0.01 - 0.05 | Moderate evidence against H₀ |
| 0.05 - 0.10 | Weak evidence against H₀ |
| > 0.10 | Insufficient evidence |

**Warning:** P-values do NOT tell you:
- The probability H₀ is true
- The probability you made an error
- The size of the effect

### Effect Size Measures

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **Cohen's d** | (μ₁ - μ₂) / σ_pooled | 0.2 small, 0.5 medium, 0.8 large |
| **Relative Lift** | (μ_treatment - μ_control) / μ_control | Percentage improvement |
| **Correlation (r)** | Pearson coefficient | 0.1 small, 0.3 medium, 0.5 large |

```python
def cohens_d(group1, group2):
    """Calculate Cohen's d effect size"""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)

    # Pooled standard deviation
    pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))

    return (np.mean(group1) - np.mean(group2)) / pooled_std
```

### Confidence Intervals

```python
def confidence_interval(data, confidence=0.95):
    """Calculate confidence interval for mean"""
    n = len(data)
    mean = np.mean(data)
    se = stats.sem(data)
    margin = se * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean - margin, mean + margin
```

**Interpretation:** "We are 95% confident the true population mean lies between [lower, upper]"

---

## Causal Inference

### Causal vs Correlation

| Question | Correlation | Causal |
|----------|-------------|--------|
| **Asks** | Are X and Y related? | Does X cause Y? |
| **Requires** | Observational data | Experimental or quasi-experimental |
| **Confounders** | May be present | Controlled or adjusted |

### Methods for Causal Inference

#### 1. Randomized Controlled Trials (RCTs)

**Gold standard** - random assignment eliminates confounding.

```
Treatment Assignment:
- Random: Users randomly assigned to treatment/control
- Balanced: Equal distribution of confounders
- Independent: One user's assignment doesn't affect another
```

#### 2. Difference-in-Differences (DiD)

Use when randomization is impossible but you have before/after data.

```
Effect = (Treatment_After - Treatment_Before) - (Control_After - Control_Before)
```

```python
def difference_in_differences(df, treatment_col, time_col, outcome_col):
    """Calculate DiD estimate"""
    # Group means
    treat_before = df[(df[treatment_col]==1) & (df[time_col]==0)][outcome_col].mean()
    treat_after = df[(df[treatment_col]==1) & (df[time_col]==1)][outcome_col].mean()
    control_before = df[(df[treatment_col]==0) & (df[time_col]==0)][outcome_col].mean()
    control_after = df[(df[treatment_col]==0) & (df[time_col]==1)][outcome_col].mean()

    did_estimate = (treat_after - treat_before) - (control_after - control_before)
    return did_estimate
```

#### 3. Propensity Score Matching

Match treated and control units on probability of treatment.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

def propensity_score_matching(df, treatment_col, confounders, outcome_col):
    """Propensity score matching for causal effect estimation"""
    # Estimate propensity scores
    model = LogisticRegression()
    model.fit(df[confounders], df[treatment_col])
    df['propensity'] = model.predict_proba(df[confounders])[:, 1]

    # Match treatment to control
    treated = df[df[treatment_col] == 1]
    control = df[df[treatment_col] == 0]

    nn = NearestNeighbors(n_neighbors=1)
    nn.fit(control[['propensity']])
    distances, indices = nn.kneighbors(treated[['propensity']])

    matched_control = control.iloc[indices.flatten()]

    # Calculate ATE
    ate = treated[outcome_col].mean() - matched_control[outcome_col].mean()
    return ate
```

#### 4. Instrumental Variables

Use when you have unmeasured confounding but an instrument.

**Requirements for valid instrument (Z):**
1. Relevance: Z affects treatment (X)
2. Exclusion: Z affects outcome (Y) only through X
3. Independence: Z is not confounded with Y

```python
from linearmodels.iv import IV2SLS

# Two-stage least squares
model = IV2SLS.from_formula('outcome ~ 1 + [treatment ~ instrument]', data=df)
result = model.fit()
```

---

## Bayesian Methods

### Bayesian vs Frequentist

| Aspect | Frequentist | Bayesian |
|--------|-------------|----------|
| **Probability** | Long-run frequency | Degree of belief |
| **Parameters** | Fixed, unknown | Random variables |
| **Data** | Random | Fixed (observed) |
| **Output** | P-values, CIs | Posterior distribution |

### Bayesian A/B Testing

```python
import numpy as np
from scipy import stats

def bayesian_ab_test(successes_a, trials_a, successes_b, trials_b,
                      prior_alpha=1, prior_beta=1, n_samples=100000):
    """
    Bayesian A/B test with Beta-Binomial model

    Returns probability that B > A
    """
    # Posterior distributions (Beta-Binomial conjugate)
    posterior_a = stats.beta(
        prior_alpha + successes_a,
        prior_beta + trials_a - successes_a
    )
    posterior_b = stats.beta(
        prior_alpha + successes_b,
        prior_beta + trials_b - successes_b
    )

    # Sample from posteriors
    samples_a = posterior_a.rvs(n_samples)
    samples_b = posterior_b.rvs(n_samples)

    # Probability B > A
    prob_b_better = np.mean(samples_b > samples_a)

    # Expected lift
    expected_lift = np.mean((samples_b - samples_a) / samples_a)

    # Credible interval for lift
    lift_samples = (samples_b - samples_a) / samples_a
    ci_lower, ci_upper = np.percentile(lift_samples, [2.5, 97.5])

    return {
        'prob_b_better': prob_b_better,
        'expected_lift': expected_lift,
        'ci_95': (ci_lower, ci_upper)
    }
```

### When to Use Bayesian Methods

- Small sample sizes (incorporate prior information)
- Sequential testing (can peek at results)
- Need probability statements ("90% chance B is better")
- Multiple comparisons (automatic shrinkage)

---

## Time Series Analysis

### Stationarity Testing

```python
from statsmodels.tsa.stattools import adfuller, kpss

def check_stationarity(series):
    """Test for stationarity using ADF and KPSS"""
    # ADF test (null: non-stationary)
    adf_result = adfuller(series)
    adf_stationary = adf_result[1] < 0.05

    # KPSS test (null: stationary)
    kpss_result = kpss(series, regression='c')
    kpss_stationary = kpss_result[1] > 0.05

    return {
        'adf_statistic': adf_result[0],
        'adf_pvalue': adf_result[1],
        'adf_stationary': adf_stationary,
        'kpss_statistic': kpss_result[0],
        'kpss_pvalue': kpss_result[1],
        'kpss_stationary': kpss_stationary,
        'is_stationary': adf_stationary and kpss_stationary
    }
```

### Seasonality Detection

```python
from statsmodels.tsa.seasonal import seasonal_decompose

def decompose_series(series, period=7):
    """Decompose time series into trend, seasonal, residual"""
    decomposition = seasonal_decompose(series, model='additive', period=period)

    return {
        'trend': decomposition.trend,
        'seasonal': decomposition.seasonal,
        'residual': decomposition.resid,
        'seasonal_strength': 1 - (decomposition.resid.var() /
                                   (decomposition.seasonal + decomposition.resid).var())
    }
```

### Forecasting Methods

| Method | Best For | Complexity |
|--------|----------|------------|
| **Moving Average** | Smoothing, simple trends | Low |
| **Exponential Smoothing** | Short-term, no seasonality | Low |
| **ARIMA** | Stationary, no seasonality | Medium |
| **SARIMA** | Seasonal patterns | Medium |
| **Prophet** | Multiple seasonalities, holidays | Low |
| **LSTM** | Complex patterns, large data | High |

---

## Common Statistical Tests

### Test Selection Guide

| Data Type | Groups | Test |
|-----------|--------|------|
| Continuous | 2 independent | t-test (or Mann-Whitney) |
| Continuous | 2 paired | Paired t-test (or Wilcoxon) |
| Continuous | 3+ independent | ANOVA (or Kruskal-Wallis) |
| Categorical | 2x2 | Chi-square (or Fisher's exact) |
| Categorical | RxC | Chi-square |
| Correlation | 2 continuous | Pearson (or Spearman) |

### Assumptions Checklist

**T-test:**
- [ ] Independence of observations
- [ ] Normality (or large n > 30)
- [ ] Equal variances (use Welch's if violated)

**ANOVA:**
- [ ] Independence
- [ ] Normality per group
- [ ] Homogeneity of variances (Levene's test)

**Chi-square:**
- [ ] Independence
- [ ] Expected counts > 5 in each cell

### Multiple Comparisons Correction

```python
from statsmodels.stats.multitest import multipletests

def correct_pvalues(pvalues, method='fdr_bh'):
    """
    Correct for multiple comparisons

    Methods:
    - bonferroni: Most conservative
    - holm: Less conservative than Bonferroni
    - fdr_bh: Benjamini-Hochberg (controls FDR)
    - fdr_by: Benjamini-Yekutieli (conservative FDR)
    """
    reject, corrected_pvalues, _, _ = multipletests(pvalues, method=method)
    return corrected_pvalues, reject
```

---

## Quick Reference

### Sample Size Formulas

**Comparing two means:**
```
n = 2 * ((z_α + z_β) * σ / δ)²

Where:
- z_α = z-score for significance level (1.96 for α=0.05)
- z_β = z-score for power (0.84 for 80% power)
- σ = standard deviation
- δ = minimum detectable effect
```

**Comparing two proportions:**
```
n = 2 * p̄(1-p̄) * ((z_α + z_β) / δ)²

Where:
- p̄ = average of p1 and p2
- δ = |p1 - p2| minimum detectable difference
```

### Common Distributions

| Distribution | Use Case | Parameters |
|--------------|----------|------------|
| Normal | Continuous, symmetric | μ, σ |
| Binomial | Count of successes | n, p |
| Poisson | Count events per interval | λ |
| Exponential | Time between events | λ |
| Beta | Proportions, Bayesian | α, β |
| Gamma | Waiting times | α, β |

---

*See also: `experiment_design_frameworks.md` for A/B testing*
