# Feature Engineering Patterns for Data Science

Practical guide for data transformations, categorical encoding, feature selection, and production-ready feature pipelines.

---

## Table of Contents

- [Numeric Transformations](#numeric-transformations)
- [Categorical Encoding](#categorical-encoding)
- [Feature Selection](#feature-selection)
- [Time-Based Features](#time-based-features)
- [Text Features](#text-features)
- [Feature Pipelines](#feature-pipelines)
- [Production Patterns](#production-patterns)

---

## Numeric Transformations

### Scaling Methods

| Method | Formula | Use When |
|--------|---------|----------|
| **StandardScaler** | (x - μ) / σ | Gaussian distribution, SVM/LR |
| **MinMaxScaler** | (x - min) / (max - min) | Bounded range needed, neural nets |
| **RobustScaler** | (x - median) / IQR | Outliers present |
| **MaxAbsScaler** | x / |max| | Sparse data |

```python
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

def choose_scaler(data, method='auto'):
    """
    Select appropriate scaler based on data characteristics

    Parameters:
    - data: numpy array or pandas Series
    - method: 'auto', 'standard', 'minmax', 'robust'
    """
    if method == 'auto':
        # Check for outliers using IQR
        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        outlier_count = np.sum((data < q1 - 1.5*iqr) | (data > q3 + 1.5*iqr))
        outlier_ratio = outlier_count / len(data)

        if outlier_ratio > 0.05:
            return RobustScaler()
        elif np.min(data) >= 0 and np.max(data) <= 1:
            return MinMaxScaler()  # Already bounded
        else:
            return StandardScaler()

    scalers = {
        'standard': StandardScaler(),
        'minmax': MinMaxScaler(),
        'robust': RobustScaler()
    }
    return scalers.get(method, StandardScaler())
```

### Power Transforms

Use for non-Gaussian distributions to achieve normality.

```python
from sklearn.preprocessing import PowerTransformer
import numpy as np

def apply_power_transform(data, method='yeo-johnson'):
    """
    Apply power transformation for normalization

    Methods:
    - yeo-johnson: Works with positive and negative values
    - box-cox: Only positive values (adds constant if needed)
    """
    transformer = PowerTransformer(method=method, standardize=True)

    # Handle negative values for box-cox
    if method == 'box-cox' and np.any(data <= 0):
        shift = abs(np.min(data)) + 1
        data = data + shift

    return transformer.fit_transform(data.reshape(-1, 1)).flatten()


def log_transform(data, offset=1):
    """
    Log transformation with offset for zeros

    Use for: Right-skewed data (income, prices, counts)
    """
    return np.log1p(data + offset - 1)  # log1p(x) = log(1+x)


def sqrt_transform(data):
    """
    Square root transformation

    Use for: Count data, moderate right skew
    """
    return np.sqrt(np.clip(data, 0, None))
```

### Binning Strategies

```python
import pandas as pd
import numpy as np

def create_bins(data, method='quantile', n_bins=5, labels=None):
    """
    Discretize continuous variables

    Methods:
    - quantile: Equal frequency bins
    - uniform: Equal width bins
    - kmeans: Cluster-based bins
    """
    if labels is None:
        labels = [f'bin_{i}' for i in range(n_bins)]

    if method == 'quantile':
        return pd.qcut(data, q=n_bins, labels=labels, duplicates='drop')

    elif method == 'uniform':
        return pd.cut(data, bins=n_bins, labels=labels)

    elif method == 'kmeans':
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=n_bins, random_state=42, n_init=10)
        bins = kmeans.fit_predict(data.values.reshape(-1, 1))
        return pd.Series(bins).map(lambda x: labels[x])


def age_bins(age):
    """Domain-specific binning example"""
    bins = [0, 18, 25, 35, 45, 55, 65, 100]
    labels = ['minor', 'young_adult', 'adult_25_35', 'adult_35_45',
              'middle_aged', 'senior', 'elderly']
    return pd.cut(age, bins=bins, labels=labels)
```

---

## Categorical Encoding

### Encoding Selection Guide

| Method | Cardinality | Use Case | Pros | Cons |
|--------|-------------|----------|------|------|
| **One-Hot** | Low (<10) | Nominal categories | Simple, interpretable | Sparse for high cardinality |
| **Label** | Any | Ordinal or tree-based | Memory efficient | Implies ordering |
| **Target** | High | Predictive encoding | Captures relationship | Risk of leakage |
| **Frequency** | High | Count-based signal | Simple, no leakage | Loses category identity |
| **Binary** | High | Many categories | Fewer columns than one-hot | Less interpretable |

### One-Hot Encoding

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def one_hot_encode(df, columns, drop_first=True, handle_unknown='ignore'):
    """
    One-hot encoding with production safeguards

    Parameters:
    - df: DataFrame
    - columns: List of columns to encode
    - drop_first: Avoid multicollinearity
    - handle_unknown: How to handle unseen categories in production
    """
    encoder = OneHotEncoder(
        drop='first' if drop_first else None,
        sparse_output=False,
        handle_unknown=handle_unknown
    )

    encoded = encoder.fit_transform(df[columns])
    feature_names = encoder.get_feature_names_out(columns)

    encoded_df = pd.DataFrame(encoded, columns=feature_names, index=df.index)

    # Drop original and concat
    result = df.drop(columns=columns).join(encoded_df)

    return result, encoder
```

### Target Encoding

```python
import numpy as np
import pandas as pd

class TargetEncoder:
    """
    Target encoding with smoothing and cross-validation

    Prevents overfitting by blending category mean with global mean
    """

    def __init__(self, smoothing=10, min_samples=1):
        self.smoothing = smoothing
        self.min_samples = min_samples
        self.encodings = {}
        self.global_mean = None

    def fit(self, X, y, columns):
        """Fit encoder on training data"""
        self.global_mean = y.mean()

        for col in columns:
            # Calculate category statistics
            stats = pd.DataFrame({
                'target': y,
                'category': X[col]
            }).groupby('category').agg(['mean', 'count'])['target']

            # Smoothed mean: blend category mean with global mean
            # Higher count → more weight to category mean
            smooth_mean = (
                (stats['mean'] * stats['count'] + self.global_mean * self.smoothing) /
                (stats['count'] + self.smoothing)
            )

            self.encodings[col] = smooth_mean.to_dict()

        return self

    def transform(self, X, columns):
        """Transform using fitted encodings"""
        result = X.copy()

        for col in columns:
            result[f'{col}_encoded'] = X[col].map(self.encodings[col])
            # Handle unseen categories with global mean
            result[f'{col}_encoded'].fillna(self.global_mean, inplace=True)

        return result

    def fit_transform_cv(self, X, y, columns, n_folds=5):
        """
        Cross-validated target encoding to prevent leakage

        Each fold's encoding is computed from other folds
        """
        from sklearn.model_selection import KFold

        result = X.copy()
        kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)

        for col in columns:
            result[f'{col}_encoded'] = np.nan

            for train_idx, val_idx in kf.split(X):
                # Fit on train fold
                self.fit(X.iloc[train_idx], y.iloc[train_idx], [col])
                # Transform validation fold
                result.loc[result.index[val_idx], f'{col}_encoded'] = \
                    X.iloc[val_idx][col].map(self.encodings[col])

            # Fill any remaining NaN with global mean
            result[f'{col}_encoded'].fillna(y.mean(), inplace=True)

        return result
```

### Frequency Encoding

```python
def frequency_encode(df, columns):
    """
    Encode categories by their frequency

    Use for: High cardinality features where count matters
    Example: zip_code frequency might indicate population density
    """
    result = df.copy()
    encodings = {}

    for col in columns:
        freq = df[col].value_counts(normalize=True)
        result[f'{col}_freq'] = df[col].map(freq)
        encodings[col] = freq.to_dict()

    return result, encodings
```

### Handling High Cardinality

```python
def reduce_cardinality(df, column, threshold=0.01, other_label='OTHER'):
    """
    Group rare categories into 'OTHER'

    Parameters:
    - threshold: Minimum frequency to keep category
    """
    freq = df[column].value_counts(normalize=True)
    rare_categories = freq[freq < threshold].index

    result = df[column].copy()
    result[result.isin(rare_categories)] = other_label

    return result
```

---

## Feature Selection

### Filter Methods

```python
import pandas as pd
import numpy as np
from scipy import stats

def correlation_filter(X, y, threshold=0.05):
    """
    Select features with significant correlation to target

    For continuous target: Pearson correlation
    For binary target: Point-biserial correlation
    """
    selected = []

    for col in X.columns:
        if X[col].dtype in ['int64', 'float64']:
            corr, p_value = stats.pearsonr(X[col].fillna(0), y)
            if p_value < threshold:
                selected.append({
                    'feature': col,
                    'correlation': corr,
                    'p_value': p_value
                })

    return pd.DataFrame(selected).sort_values('p_value')


def variance_filter(X, threshold=0.01):
    """
    Remove low-variance features

    Features with variance below threshold are likely uninformative
    """
    from sklearn.feature_selection import VarianceThreshold

    selector = VarianceThreshold(threshold=threshold)
    selector.fit(X)

    selected_features = X.columns[selector.get_support()].tolist()
    removed_features = X.columns[~selector.get_support()].tolist()

    return selected_features, removed_features


def mutual_information_filter(X, y, n_features=20, discrete_features='auto'):
    """
    Select features using mutual information

    Works for both classification and regression
    """
    from sklearn.feature_selection import mutual_info_classif, mutual_info_regression

    # Determine task type
    if len(np.unique(y)) <= 10:
        mi_func = mutual_info_classif
    else:
        mi_func = mutual_info_regression

    mi_scores = mi_func(X.fillna(0), y, discrete_features=discrete_features)

    mi_df = pd.DataFrame({
        'feature': X.columns,
        'mi_score': mi_scores
    }).sort_values('mi_score', ascending=False)

    return mi_df.head(n_features)['feature'].tolist()
```

### Wrapper Methods

```python
from sklearn.feature_selection import RFE, RFECV
from sklearn.ensemble import RandomForestClassifier

def recursive_feature_elimination(X, y, n_features=10, cv=5):
    """
    Select features using RFE with cross-validation

    Iteratively removes least important features
    """
    estimator = RandomForestClassifier(n_estimators=100, random_state=42)

    # With cross-validation to find optimal number
    selector = RFECV(
        estimator=estimator,
        step=1,
        cv=cv,
        scoring='roc_auc',
        min_features_to_select=5
    )
    selector.fit(X, y)

    return {
        'selected_features': X.columns[selector.support_].tolist(),
        'feature_ranking': dict(zip(X.columns, selector.ranking_)),
        'optimal_n_features': selector.n_features_,
        'cv_scores': selector.cv_results_['mean_test_score']
    }
```

### Embedded Methods

```python
import numpy as np
from sklearn.linear_model import LassoCV
from sklearn.ensemble import RandomForestClassifier

def lasso_feature_selection(X, y, cv=5):
    """
    L1 regularization for automatic feature selection

    Coefficients shrunk to zero are excluded
    """
    lasso = LassoCV(cv=cv, random_state=42)
    lasso.fit(X, y)

    importance = pd.DataFrame({
        'feature': X.columns,
        'coefficient': np.abs(lasso.coef_)
    }).sort_values('coefficient', ascending=False)

    selected = importance[importance['coefficient'] > 0]['feature'].tolist()

    return {
        'selected_features': selected,
        'importance': importance,
        'optimal_alpha': lasso.alpha_
    }


def tree_based_importance(X, y, n_features=20):
    """
    Feature importance from tree-based models

    Uses permutation importance for unbiased estimates
    """
    from sklearn.inspection import permutation_importance

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Permutation importance (more reliable than built-in)
    perm_importance = permutation_importance(
        model, X, y,
        n_repeats=10,
        random_state=42,
        n_jobs=-1
    )

    importance_df = pd.DataFrame({
        'feature': X.columns,
        'importance_mean': perm_importance.importances_mean,
        'importance_std': perm_importance.importances_std
    }).sort_values('importance_mean', ascending=False)

    return importance_df.head(n_features)['feature'].tolist()
```

### Collinearity Detection

```python
import pandas as pd
import numpy as np

def detect_multicollinearity(X, threshold=0.8):
    """
    Find highly correlated feature pairs

    Correlated features provide redundant information
    """
    corr_matrix = X.corr().abs()

    # Get upper triangle
    upper = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )

    # Find pairs above threshold
    high_corr_pairs = []
    for col in upper.columns:
        for idx in upper.index:
            if upper.loc[idx, col] > threshold:
                high_corr_pairs.append({
                    'feature_1': idx,
                    'feature_2': col,
                    'correlation': upper.loc[idx, col]
                })

    return pd.DataFrame(high_corr_pairs)


def variance_inflation_factor(X):
    """
    Calculate VIF for each feature

    VIF > 5-10 indicates problematic multicollinearity
    """
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    vif_data = pd.DataFrame()
    vif_data['feature'] = X.columns
    vif_data['vif'] = [
        variance_inflation_factor(X.values, i)
        for i in range(X.shape[1])
    ]

    return vif_data.sort_values('vif', ascending=False)
```

---

## Time-Based Features

### Date/Time Extraction

```python
import pandas as pd
import numpy as np

def extract_datetime_features(df, date_column):
    """
    Extract comprehensive features from datetime column
    """
    dt = pd.to_datetime(df[date_column])
    prefix = date_column

    features = pd.DataFrame({
        # Basic components
        f'{prefix}_year': dt.dt.year,
        f'{prefix}_month': dt.dt.month,
        f'{prefix}_day': dt.dt.day,
        f'{prefix}_hour': dt.dt.hour,
        f'{prefix}_minute': dt.dt.minute,
        f'{prefix}_dayofweek': dt.dt.dayofweek,
        f'{prefix}_dayofyear': dt.dt.dayofyear,
        f'{prefix}_weekofyear': dt.dt.isocalendar().week,
        f'{prefix}_quarter': dt.dt.quarter,

        # Binary flags
        f'{prefix}_is_weekend': dt.dt.dayofweek.isin([5, 6]).astype(int),
        f'{prefix}_is_month_start': dt.dt.is_month_start.astype(int),
        f'{prefix}_is_month_end': dt.dt.is_month_end.astype(int),

        # Cyclical encoding (for periodic patterns)
        f'{prefix}_hour_sin': np.sin(2 * np.pi * dt.dt.hour / 24),
        f'{prefix}_hour_cos': np.cos(2 * np.pi * dt.dt.hour / 24),
        f'{prefix}_day_sin': np.sin(2 * np.pi * dt.dt.dayofweek / 7),
        f'{prefix}_day_cos': np.cos(2 * np.pi * dt.dt.dayofweek / 7),
        f'{prefix}_month_sin': np.sin(2 * np.pi * dt.dt.month / 12),
        f'{prefix}_month_cos': np.cos(2 * np.pi * dt.dt.month / 12),
    })

    return features
```

### Lag Features

```python
def create_lag_features(df, column, lags, group_by=None):
    """
    Create lagged features for time series

    Parameters:
    - lags: List of lag periods [1, 7, 30]
    - group_by: Column to group by (e.g., user_id for user-level series)
    """
    result = df.copy()

    for lag in lags:
        if group_by:
            result[f'{column}_lag_{lag}'] = df.groupby(group_by)[column].shift(lag)
        else:
            result[f'{column}_lag_{lag}'] = df[column].shift(lag)

    return result


def create_rolling_features(df, column, windows, group_by=None):
    """
    Create rolling window statistics

    Parameters:
    - windows: List of window sizes [7, 30, 90]
    """
    result = df.copy()

    for window in windows:
        if group_by:
            grouped = df.groupby(group_by)[column]
        else:
            grouped = df[column]

        result[f'{column}_rolling_mean_{window}'] = grouped.transform(
            lambda x: x.rolling(window, min_periods=1).mean()
        )
        result[f'{column}_rolling_std_{window}'] = grouped.transform(
            lambda x: x.rolling(window, min_periods=1).std()
        )
        result[f'{column}_rolling_min_{window}'] = grouped.transform(
            lambda x: x.rolling(window, min_periods=1).min()
        )
        result[f'{column}_rolling_max_{window}'] = grouped.transform(
            lambda x: x.rolling(window, min_periods=1).max()
        )

    return result
```

### Time Since Events

```python
def time_since_event(df, date_column, event_column, unit='days'):
    """
    Calculate time since last event occurrence

    Example: Days since last purchase, hours since last login
    """
    df = df.sort_values(date_column)

    # Find last event date for each row
    event_dates = df[df[event_column] == 1][date_column]

    def calc_time_since(row_date):
        past_events = event_dates[event_dates < row_date]
        if len(past_events) == 0:
            return np.nan
        time_diff = row_date - past_events.max()
        if unit == 'days':
            return time_diff.days
        elif unit == 'hours':
            return time_diff.total_seconds() / 3600
        return time_diff

    return df[date_column].apply(calc_time_since)
```

---

## Text Features

### Basic Text Features

```python
import re
import numpy as np

def extract_text_features(df, text_column):
    """
    Extract basic statistical features from text
    """
    text = df[text_column].fillna('')

    features = pd.DataFrame({
        # Length features
        f'{text_column}_char_count': text.str.len(),
        f'{text_column}_word_count': text.str.split().str.len(),
        f'{text_column}_sentence_count': text.str.count(r'[.!?]+'),

        # Average lengths
        f'{text_column}_avg_word_length': text.apply(
            lambda x: np.mean([len(w) for w in x.split()]) if x else 0
        ),

        # Special character counts
        f'{text_column}_digit_count': text.str.count(r'\d'),
        f'{text_column}_uppercase_count': text.str.count(r'[A-Z]'),
        f'{text_column}_special_char_count': text.str.count(r'[!@#$%^&*()]'),

        # Ratios
        f'{text_column}_uppercase_ratio': text.apply(
            lambda x: sum(1 for c in x if c.isupper()) / len(x) if x else 0
        ),
    })

    return features
```

### TF-IDF Features

```python
from sklearn.feature_extraction.text import TfidfVectorizer

def create_tfidf_features(texts, max_features=100, ngram_range=(1, 2)):
    """
    Create TF-IDF features from text

    Parameters:
    - max_features: Limit vocabulary size
    - ngram_range: Include unigrams and bigrams
    """
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        stop_words='english',
        min_df=5,  # Appear in at least 5 documents
        max_df=0.95  # Appear in at most 95% of documents
    )

    tfidf_matrix = vectorizer.fit_transform(texts.fillna(''))

    feature_names = [f'tfidf_{name}' for name in vectorizer.get_feature_names_out()]

    return pd.DataFrame(
        tfidf_matrix.toarray(),
        columns=feature_names
    ), vectorizer
```

---

## Feature Pipelines

### Sklearn Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def create_feature_pipeline(numeric_cols, categorical_cols):
    """
    Create a reusable preprocessing pipeline
    """
    # Numeric pipeline
    numeric_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Categorical pipeline
    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Combine
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_cols),
            ('cat', categorical_transformer, categorical_cols)
        ],
        remainder='drop'  # Drop other columns
    )

    return preprocessor


# Usage
# preprocessor = create_feature_pipeline(['age', 'income'], ['gender', 'city'])
# X_transformed = preprocessor.fit_transform(X_train)
# X_test_transformed = preprocessor.transform(X_test)
```

### Custom Transformer

```python
from sklearn.base import BaseEstimator, TransformerMixin

class DatetimeFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Custom transformer for datetime feature extraction

    Compatible with sklearn Pipeline
    """

    def __init__(self, date_columns, include_cyclical=True):
        self.date_columns = date_columns
        self.include_cyclical = include_cyclical

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        feature_dfs = []

        for col in self.date_columns:
            dt = pd.to_datetime(X[col])
            features = {
                f'{col}_year': dt.dt.year,
                f'{col}_month': dt.dt.month,
                f'{col}_dayofweek': dt.dt.dayofweek,
                f'{col}_is_weekend': dt.dt.dayofweek.isin([5, 6]).astype(int)
            }

            if self.include_cyclical:
                features[f'{col}_month_sin'] = np.sin(2 * np.pi * dt.dt.month / 12)
                features[f'{col}_month_cos'] = np.cos(2 * np.pi * dt.dt.month / 12)

            feature_dfs.append(pd.DataFrame(features))

        return pd.concat([X.drop(columns=self.date_columns)] + feature_dfs, axis=1)
```

---

## Production Patterns

### Feature Store Pattern

```python
class FeatureStore:
    """
    Simple feature store for training/serving consistency
    """

    def __init__(self):
        self.feature_definitions = {}
        self.computed_features = {}

    def register_feature(self, name, compute_fn, dependencies=None):
        """Register a feature computation function"""
        self.feature_definitions[name] = {
            'compute_fn': compute_fn,
            'dependencies': dependencies or []
        }

    def compute_feature(self, name, data):
        """Compute a feature, resolving dependencies"""
        if name in self.computed_features:
            return self.computed_features[name]

        definition = self.feature_definitions[name]

        # Compute dependencies first
        for dep in definition['dependencies']:
            if dep not in self.computed_features:
                self.compute_feature(dep, data)

        # Compute this feature
        result = definition['compute_fn'](data, self.computed_features)
        self.computed_features[name] = result
        return result

    def get_feature_set(self, feature_names, data):
        """Get multiple features as DataFrame"""
        self.computed_features = {}  # Reset cache
        features = {}
        for name in feature_names:
            features[name] = self.compute_feature(name, data)
        return pd.DataFrame(features)


# Usage example
# store = FeatureStore()
# store.register_feature('age_bucket', lambda d, _: age_bins(d['age']))
# store.register_feature('income_scaled', lambda d, _: StandardScaler().fit_transform(d[['income']]))
# features = store.get_feature_set(['age_bucket', 'income_scaled'], df)
```

### Feature Validation

```python
def validate_features(train_features, test_features, report=True):
    """
    Check for training/serving skew

    Common issues:
    - Missing columns
    - Different dtypes
    - Distribution shift
    """
    issues = []

    # Check columns match
    train_cols = set(train_features.columns)
    test_cols = set(test_features.columns)

    missing_in_test = train_cols - test_cols
    extra_in_test = test_cols - train_cols

    if missing_in_test:
        issues.append(f"Missing in test: {missing_in_test}")
    if extra_in_test:
        issues.append(f"Extra in test: {extra_in_test}")

    # Check dtypes
    common_cols = train_cols & test_cols
    for col in common_cols:
        if train_features[col].dtype != test_features[col].dtype:
            issues.append(f"Dtype mismatch for {col}: "
                         f"{train_features[col].dtype} vs {test_features[col].dtype}")

    # Check for distribution shift (numeric only)
    for col in common_cols:
        if train_features[col].dtype in ['int64', 'float64']:
            train_mean = train_features[col].mean()
            test_mean = test_features[col].mean()

            if abs(train_mean - test_mean) / (train_mean + 1e-10) > 0.5:
                issues.append(f"Large mean shift for {col}: "
                             f"{train_mean:.2f} -> {test_mean:.2f}")

    if report:
        if issues:
            print("Feature validation issues:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("Feature validation passed!")

    return len(issues) == 0, issues
```

---

## Quick Reference

### Feature Engineering Checklist

**Before modeling:**
- [ ] Handle missing values appropriately
- [ ] Scale/normalize numeric features
- [ ] Encode categorical variables
- [ ] Remove or combine collinear features
- [ ] Create domain-specific features
- [ ] Extract datetime features

**Selection criteria:**
- [ ] Filter features with low variance
- [ ] Check correlation with target
- [ ] Use embedded methods (Lasso/Tree importance)
- [ ] Validate with cross-validation

**Production readiness:**
- [ ] Pipeline can transform new data
- [ ] Handles unseen categories
- [ ] No data leakage from target
- [ ] Feature validation between train/serve

### Common Transformations by Data Type

| Data Type | Common Transformations |
|-----------|----------------------|
| **Numeric** | Scaling, log/power, binning |
| **Categorical** | One-hot, target, frequency encoding |
| **Datetime** | Extract components, cyclical, lags |
| **Text** | Length stats, TF-IDF, embeddings |
| **Boolean** | Interaction terms, aggregations |

---

*See also: `statistical_methods_advanced.md` for feature selection statistics*
