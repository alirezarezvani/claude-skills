# Experiment Design Frameworks for Data Science

Comprehensive guide for A/B testing, power analysis, sample size calculation, and randomization schemes in production systems.

---

## Table of Contents

- [A/B Testing Fundamentals](#ab-testing-fundamentals)
- [Power Analysis](#power-analysis)
- [Sample Size Calculation](#sample-size-calculation)
- [Randomization Schemes](#randomization-schemes)
- [Experiment Lifecycle](#experiment-lifecycle)
- [Multi-Armed Bandits](#multi-armed-bandits)
- [Common Pitfalls](#common-pitfalls)

---

## A/B Testing Fundamentals

### Anatomy of an A/B Test

```
┌─────────────────────────────────────────────────────────────┐
│                    EXPERIMENT DESIGN                        │
├─────────────────────────────────────────────────────────────┤
│  Population: All eligible users                             │
│  ↓                                                          │
│  Randomization Unit: User ID / Session / Device             │
│  ↓                                                          │
│  ┌─────────────┐    ┌─────────────┐                        │
│  │  Control    │    │  Treatment  │                        │
│  │  (50%)      │    │  (50%)      │                        │
│  │  Old flow   │    │  New flow   │                        │
│  └──────┬──────┘    └──────┬──────┘                        │
│         │                   │                               │
│         ▼                   ▼                               │
│  Measure primary metric (e.g., conversion rate)             │
│         │                   │                               │
│         └───────┬───────────┘                               │
│                 ▼                                           │
│  Statistical Test → Decision                                │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Description | Example |
|-----------|-------------|---------|
| **Hypothesis** | What you're testing | "New CTA increases signups" |
| **Primary Metric** | Main success measure | Signup conversion rate |
| **Secondary Metrics** | Guardrail/supporting | Revenue, engagement, latency |
| **Randomization Unit** | How users are assigned | User ID (most common) |
| **Duration** | How long to run | 2+ weeks for weekly cycles |

### Metrics Taxonomy

```python
class MetricType:
    """Types of metrics in A/B testing"""

    # Primary: The main metric you're optimizing
    PRIMARY = "primary"  # e.g., conversion rate

    # Guardrail: Must not regress significantly
    GUARDRAIL = "guardrail"  # e.g., page load time, error rate

    # Secondary: Nice to improve, not required
    SECONDARY = "secondary"  # e.g., engagement metrics

    # Debug: Help explain results
    DEBUG = "debug"  # e.g., funnel step metrics


def define_experiment_metrics():
    """Example metric definition for a checkout experiment"""
    return {
        "primary": {
            "name": "checkout_completion_rate",
            "type": "proportion",
            "direction": "increase",
            "mde": 0.02  # 2% minimum detectable effect
        },
        "guardrails": [
            {"name": "error_rate", "type": "proportion", "threshold": 0.01},
            {"name": "page_load_p95", "type": "continuous", "threshold": 3.0}
        ],
        "secondary": [
            {"name": "revenue_per_user", "type": "continuous"},
            {"name": "items_per_order", "type": "continuous"}
        ]
    }
```

---

## Power Analysis

### Understanding Statistical Power

```
Power = P(reject H₀ | H₁ is true)
      = P(detect effect | effect exists)
      = 1 - β (Type II error rate)

Standard target: 80% power (β = 0.20)
```

### Power Calculation

```python
from scipy import stats
import numpy as np

def calculate_power(n_per_group, effect_size, alpha=0.05):
    """
    Calculate statistical power for two-sample t-test

    Parameters:
    - n_per_group: Sample size per group
    - effect_size: Cohen's d (standardized effect)
    - alpha: Significance level

    Returns:
    - Statistical power (0 to 1)
    """
    # Critical value for two-tailed test
    z_alpha = stats.norm.ppf(1 - alpha / 2)

    # Standard error of the difference
    se = np.sqrt(2 / n_per_group)

    # Non-centrality parameter
    ncp = effect_size / se

    # Power calculation
    power = 1 - stats.norm.cdf(z_alpha - ncp) + stats.norm.cdf(-z_alpha - ncp)

    return power


def power_curve(effect_size, alpha=0.05, max_n=10000):
    """Generate power curve for different sample sizes"""
    sample_sizes = np.arange(100, max_n, 100)
    powers = [calculate_power(n, effect_size, alpha) for n in sample_sizes]

    # Find minimum n for 80% power
    min_n = next((n for n, p in zip(sample_sizes, powers) if p >= 0.80), None)

    return {
        "sample_sizes": sample_sizes.tolist(),
        "powers": powers,
        "min_n_for_80_power": min_n
    }
```

### Factors Affecting Power

| Factor | Effect on Power | Action |
|--------|-----------------|--------|
| **↑ Sample size** | ↑ Power | Run longer or increase traffic |
| **↑ Effect size** | ↑ Power | Target larger changes |
| **↓ Variance** | ↑ Power | Use variance reduction techniques |
| **↑ Alpha** | ↑ Power | Accept more false positives |

---

## Sample Size Calculation

### For Proportions (Conversion Rates)

```python
from scipy import stats
import numpy as np

def sample_size_proportions(p_control, mde, alpha=0.05, power=0.80):
    """
    Calculate sample size for comparing two proportions

    Parameters:
    - p_control: Expected control conversion rate
    - mde: Minimum detectable effect (absolute, e.g., 0.02 for 2%)
    - alpha: Significance level (default 0.05)
    - power: Statistical power (default 0.80)

    Returns:
    - Sample size per group
    """
    p_treatment = p_control + mde

    # Average proportion
    p_pooled = (p_control + p_treatment) / 2

    # Z-scores
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    # Sample size formula
    numerator = (z_alpha * np.sqrt(2 * p_pooled * (1 - p_pooled)) +
                 z_beta * np.sqrt(p_control * (1 - p_control) +
                                  p_treatment * (1 - p_treatment))) ** 2
    denominator = (p_treatment - p_control) ** 2

    n = numerator / denominator

    return int(np.ceil(n))


# Example usage
baseline_conversion = 0.10  # 10% conversion rate
minimum_detectable_effect = 0.01  # Want to detect 1% absolute change

n_per_group = sample_size_proportions(baseline_conversion, minimum_detectable_effect)
print(f"Need {n_per_group:,} users per group")
print(f"Total users needed: {2 * n_per_group:,}")
```

### For Continuous Metrics (Revenue, Time)

```python
def sample_size_continuous(mean_control, std_control, mde_relative,
                           alpha=0.05, power=0.80):
    """
    Calculate sample size for comparing two means

    Parameters:
    - mean_control: Expected control mean
    - std_control: Expected standard deviation
    - mde_relative: Minimum detectable effect (relative, e.g., 0.05 for 5%)
    - alpha: Significance level
    - power: Statistical power

    Returns:
    - Sample size per group
    """
    # Convert relative MDE to absolute
    mde_absolute = mean_control * mde_relative

    # Effect size (Cohen's d)
    effect_size = mde_absolute / std_control

    # Z-scores
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    # Sample size formula
    n = 2 * ((z_alpha + z_beta) / effect_size) ** 2

    return int(np.ceil(n))


# Example: Revenue per user
mean_revenue = 50.0
std_revenue = 100.0  # High variance typical for revenue
mde = 0.05  # 5% lift

n = sample_size_continuous(mean_revenue, std_revenue, mde)
print(f"Need {n:,} users per group to detect 5% revenue lift")
```

### Sample Size Reference Table

| Baseline Rate | MDE (Relative) | N per Group | Total N |
|---------------|----------------|-------------|---------|
| 1% | 20% (0.2%) | 196,000 | 392,000 |
| 1% | 10% (0.1%) | 785,000 | 1,570,000 |
| 5% | 10% (0.5%) | 30,400 | 60,800 |
| 5% | 5% (0.25%) | 122,000 | 244,000 |
| 10% | 10% (1.0%) | 14,400 | 28,800 |
| 10% | 5% (0.5%) | 57,600 | 115,200 |
| 20% | 10% (2.0%) | 6,400 | 12,800 |
| 20% | 5% (1.0%) | 25,600 | 51,200 |

*Calculated at α=0.05, power=0.80*

---

## Randomization Schemes

### 1. Simple Random Assignment

```python
import hashlib

def simple_random_assignment(user_id, experiment_id, salt=""):
    """
    Deterministic random assignment using hashing

    Benefits: Consistent, repeatable, no storage needed
    """
    hash_input = f"{experiment_id}:{user_id}:{salt}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)

    # Convert to 0-1 range
    bucket = (hash_value % 10000) / 10000

    return "treatment" if bucket < 0.5 else "control"
```

### 2. Stratified Randomization

Use when you need balanced groups across important segments.

```python
def stratified_assignment(user_id, experiment_id, stratum):
    """
    Randomize within strata (e.g., country, device type)

    Ensures equal proportions of each stratum in treatment/control
    """
    hash_input = f"{experiment_id}:{stratum}:{user_id}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
    bucket = (hash_value % 10000) / 10000

    return "treatment" if bucket < 0.5 else "control"


# Example: Balance by country
user_assignment = stratified_assignment(
    user_id="user123",
    experiment_id="checkout_v2",
    stratum="US"  # Stratify by country
)
```

### 3. Cluster Randomization

Use when individual randomization causes spillover effects.

```python
def cluster_assignment(cluster_id, experiment_id):
    """
    Assign entire clusters (e.g., cities, companies) to treatment

    Use when:
    - Network effects between users
    - Operational constraints (can't show different UIs in same store)
    - Marketplace experiments (sellers/buyers interact)
    """
    hash_input = f"{experiment_id}:{cluster_id}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
    bucket = (hash_value % 10000) / 10000

    return "treatment" if bucket < 0.5 else "control"


def get_user_assignment_via_cluster(user_id, user_cluster, experiment_id):
    """User inherits assignment from their cluster"""
    return cluster_assignment(user_cluster, experiment_id)
```

### 4. Switchback (Time-Based)

```python
from datetime import datetime

def switchback_assignment(timestamp, period_minutes=60):
    """
    Alternate treatment/control over time periods

    Use for:
    - Marketplace experiments (can't split buyers/sellers)
    - Capacity-constrained systems
    - Delivery/logistics experiments
    """
    period = int(timestamp.timestamp() // (period_minutes * 60))
    return "treatment" if period % 2 == 0 else "control"
```

### Randomization Selection Guide

| Scenario | Recommended Approach |
|----------|---------------------|
| Standard A/B test | Simple random (user-level) |
| Must balance demographics | Stratified randomization |
| Social network experiment | Cluster by network graph |
| Marketplace (buyers/sellers) | Switchback or cluster by market |
| B2B (company accounts) | Cluster by company |
| Physical stores | Cluster by store |

---

## Experiment Lifecycle

### Phase 1: Design

```python
def create_experiment_design(
    name,
    hypothesis,
    primary_metric,
    baseline_rate,
    mde,
    traffic_percent=100,
    alpha=0.05,
    power=0.80
):
    """Create experiment design document"""

    n_per_group = sample_size_proportions(baseline_rate, mde, alpha, power)

    return {
        "name": name,
        "hypothesis": hypothesis,
        "design": {
            "type": "A/B",
            "variants": ["control", "treatment"],
            "traffic_allocation": {"control": 0.5, "treatment": 0.5},
            "traffic_percent": traffic_percent,
            "randomization_unit": "user_id"
        },
        "metrics": {
            "primary": primary_metric,
            "guardrails": [],
            "secondary": []
        },
        "statistical_plan": {
            "alpha": alpha,
            "power": power,
            "mde": mde,
            "baseline_rate": baseline_rate,
            "sample_size_per_group": n_per_group,
            "total_sample_size": 2 * n_per_group
        },
        "status": "design"
    }
```

### Phase 2: Pre-Experiment Checks

```python
def run_pre_experiment_checks(experiment_data):
    """Validate experiment before launch"""
    checks = {}

    # 1. Sample Ratio Mismatch (SRM) check
    n_control = experiment_data["control"]["n"]
    n_treatment = experiment_data["treatment"]["n"]
    expected_ratio = 0.5

    from scipy.stats import chisquare
    observed = [n_control, n_treatment]
    expected = [sum(observed) * expected_ratio] * 2
    _, srm_pvalue = chisquare(observed, expected)

    checks["srm"] = {
        "passed": srm_pvalue > 0.001,
        "p_value": srm_pvalue,
        "actual_ratio": n_control / (n_control + n_treatment)
    }

    # 2. AA check - pre-treatment metrics should be balanced
    # (Run this before treatment is applied)

    # 3. Novelty effect check - exclude first day's data

    return checks
```

### Phase 3: Analysis

```python
from scipy import stats
import numpy as np

def analyze_experiment(control_data, treatment_data, metric_type="proportion"):
    """
    Analyze A/B test results

    Parameters:
    - control_data: List of outcomes for control group
    - treatment_data: List of outcomes for treatment group
    - metric_type: "proportion" or "continuous"
    """
    control = np.array(control_data)
    treatment = np.array(treatment_data)

    if metric_type == "proportion":
        # Proportions test
        successes = [control.sum(), treatment.sum()]
        trials = [len(control), len(treatment)]

        from statsmodels.stats.proportion import proportions_ztest
        z_stat, p_value = proportions_ztest(successes, trials)

        control_rate = control.mean()
        treatment_rate = treatment.mean()
        lift = (treatment_rate - control_rate) / control_rate

    else:
        # Two-sample t-test
        t_stat, p_value = stats.ttest_ind(control, treatment)

        control_rate = control.mean()
        treatment_rate = treatment.mean()
        lift = (treatment_rate - control_rate) / control_rate

    # Confidence interval for lift
    se = np.sqrt(control.var()/len(control) + treatment.var()/len(treatment))
    ci_lower = (treatment_rate - control_rate - 1.96*se) / control_rate
    ci_upper = (treatment_rate - control_rate + 1.96*se) / control_rate

    return {
        "control": {
            "n": len(control),
            "mean": control_rate,
            "std": control.std()
        },
        "treatment": {
            "n": len(treatment),
            "mean": treatment_rate,
            "std": treatment.std()
        },
        "lift": {
            "relative": lift,
            "absolute": treatment_rate - control_rate,
            "ci_95": (ci_lower, ci_upper)
        },
        "statistical_test": {
            "p_value": p_value,
            "significant_at_05": p_value < 0.05
        }
    }
```

### Phase 4: Decision Framework

```
┌──────────────────────────────────────────────────────────┐
│                   DECISION MATRIX                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  p < 0.05 AND lift CI > 0?                              │
│     │                                                    │
│     ├── YES → Check guardrails                          │
│     │         │                                          │
│     │         ├── Guardrails OK → SHIP IT               │
│     │         └── Guardrails fail → INVESTIGATE         │
│     │                                                    │
│     └── NO → Not significant                            │
│              │                                           │
│              ├── Reached sample size?                    │
│              │   ├── YES → NO EFFECT DETECTED           │
│              │   └── NO → Continue running              │
│              │                                           │
│              └── Is p close (0.05 < p < 0.10)?          │
│                  └── Consider extending test             │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Multi-Armed Bandits

### When to Use Bandits vs A/B Tests

| Criteria | A/B Test | Bandit |
|----------|----------|--------|
| **Goal** | Learn truth | Maximize reward |
| **Duration** | Fixed | Continuous |
| **Traffic** | Equal split | Dynamic allocation |
| **Use case** | Ship/no-ship decisions | Content optimization |

### Thompson Sampling

```python
import numpy as np
from scipy import stats

class ThompsonSamplingBandit:
    """Multi-armed bandit using Thompson Sampling"""

    def __init__(self, n_arms, prior_alpha=1, prior_beta=1):
        self.n_arms = n_arms
        self.alpha = np.ones(n_arms) * prior_alpha  # Successes + prior
        self.beta = np.ones(n_arms) * prior_beta    # Failures + prior

    def select_arm(self):
        """Sample from posterior and select highest"""
        samples = [stats.beta(a, b).rvs() for a, b in zip(self.alpha, self.beta)]
        return np.argmax(samples)

    def update(self, arm, reward):
        """Update posterior with observed reward"""
        if reward == 1:
            self.alpha[arm] += 1
        else:
            self.beta[arm] += 1

    def get_statistics(self):
        """Return current estimates"""
        return {
            "arm_means": self.alpha / (self.alpha + self.beta),
            "arm_samples": (self.alpha + self.beta - 2).astype(int),
            "best_arm": np.argmax(self.alpha / (self.alpha + self.beta))
        }


# Usage example
bandit = ThompsonSamplingBandit(n_arms=3)

# Simulate 1000 trials
for _ in range(1000):
    arm = bandit.select_arm()
    # Simulate reward (arm 1 is best with 15% conversion)
    true_rates = [0.10, 0.15, 0.08]
    reward = 1 if np.random.random() < true_rates[arm] else 0
    bandit.update(arm, reward)

print(bandit.get_statistics())
```

### Epsilon-Greedy

```python
class EpsilonGreedyBandit:
    """Simple epsilon-greedy bandit"""

    def __init__(self, n_arms, epsilon=0.1):
        self.n_arms = n_arms
        self.epsilon = epsilon
        self.counts = np.zeros(n_arms)
        self.values = np.zeros(n_arms)

    def select_arm(self):
        """Explore with probability epsilon, exploit otherwise"""
        if np.random.random() < self.epsilon:
            return np.random.randint(self.n_arms)
        return np.argmax(self.values)

    def update(self, arm, reward):
        """Update running average for arm"""
        self.counts[arm] += 1
        n = self.counts[arm]
        value = self.values[arm]
        self.values[arm] = value + (reward - value) / n
```

---

## Common Pitfalls

### 1. Peeking Problem

**Problem:** Checking results early inflates false positive rate.

```python
def adjusted_alpha_for_peeking(n_peeks, base_alpha=0.05):
    """
    Adjust significance level for multiple looks

    Uses Pocock boundary (conservative)
    """
    # Pocock boundary adjustments
    pocock_adjustments = {
        1: 0.05,
        2: 0.0294,
        3: 0.0221,
        4: 0.0182,
        5: 0.0158
    }
    return pocock_adjustments.get(n_peeks, base_alpha / n_peeks)
```

**Solution:** Use sequential testing or pre-commit to fixed duration.

### 2. Sample Ratio Mismatch (SRM)

**Problem:** Unequal assignment indicates bugs.

```python
def check_srm(n_control, n_treatment, expected_ratio=0.5, threshold=0.001):
    """
    Detect sample ratio mismatch

    SRM indicates:
    - Assignment bug
    - Bot traffic
    - Data pipeline issues
    """
    from scipy.stats import chisquare

    total = n_control + n_treatment
    expected = [total * expected_ratio, total * (1 - expected_ratio)]
    observed = [n_control, n_treatment]

    _, p_value = chisquare(observed, expected)

    return {
        "has_srm": p_value < threshold,
        "p_value": p_value,
        "actual_ratio": n_control / total,
        "expected_ratio": expected_ratio
    }
```

### 3. Simpson's Paradox

**Problem:** Aggregate results differ from segment results.

```
Example:
- Desktop: Treatment 10% vs Control 8% → Treatment wins
- Mobile: Treatment 5% vs Control 4% → Treatment wins
- Overall: Treatment 6% vs Control 7% → Control wins!

Cause: Treatment had more mobile users (lower baseline)
```

**Solution:** Always segment analysis. Check for assignment imbalance.

### 4. Novelty/Primacy Effects

**Problem:** Users react differently to change than steady state.

```python
def analyze_by_cohort(data, experiment_start_date):
    """
    Analyze by when users first saw experiment

    Helps detect novelty effects
    """
    data['days_since_start'] = (data['first_exposure'] - experiment_start_date).dt.days

    cohorts = {
        'week_1': data[data['days_since_start'] < 7],
        'week_2': data[(data['days_since_start'] >= 7) & (data['days_since_start'] < 14)],
        'week_3_plus': data[data['days_since_start'] >= 14]
    }

    results = {}
    for cohort_name, cohort_data in cohorts.items():
        results[cohort_name] = {
            'control': cohort_data[cohort_data['variant'] == 'control']['metric'].mean(),
            'treatment': cohort_data[cohort_data['variant'] == 'treatment']['metric'].mean()
        }

    return results
```

### 5. Multiple Comparisons

**Problem:** Testing many metrics inflates false positives.

```python
from statsmodels.stats.multitest import multipletests

def correct_for_multiple_tests(p_values, method='fdr_bh'):
    """
    Correct p-values for multiple comparisons

    Methods:
    - bonferroni: Most conservative
    - fdr_bh: Benjamini-Hochberg (recommended)
    """
    reject, corrected_pvals, _, _ = multipletests(p_values, method=method)
    return corrected_pvals
```

---

## Quick Reference

### Experiment Checklist

**Before Launch:**
- [ ] Hypothesis documented
- [ ] Primary metric defined
- [ ] Sample size calculated
- [ ] Guardrail metrics identified
- [ ] Randomization unit chosen
- [ ] Duration planned (include weekly cycles)
- [ ] Logging verified

**During Experiment:**
- [ ] SRM check daily
- [ ] Monitor guardrails
- [ ] No peeking at primary metric
- [ ] Document any incidents

**After Experiment:**
- [ ] SRM final check
- [ ] Analyze primary metric
- [ ] Check guardrails
- [ ] Segment analysis
- [ ] Document learnings

### Duration Guidelines

| Traffic per Day | 10% MDE | 5% MDE | 2% MDE |
|-----------------|---------|--------|--------|
| 1,000 | 3 days | 14 days | 80 days |
| 10,000 | 1 day | 2 days | 8 days |
| 100,000 | 1 day | 1 day | 1 day |

*Based on 10% baseline conversion, 80% power, α=0.05*

---

*See also: `statistical_methods_advanced.md` for hypothesis testing details*
