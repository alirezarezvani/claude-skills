# Governance Domain Map

## 1. Algorithmic Bias Detection

Algorithmic bias is a systematic and repeatable error in AI outputs that creates unfair outcomes for individuals or groups sharing a protected characteristic (race, gender, age, disability, national origin, and others depending on jurisdiction).

This agent evaluates bias across three measurement dimensions:

**Outcome fairness metrics:**
- Demographic parity: P(Y=1 | A=0) = P(Y=1 | A=1) across protected group A
- Equalized odds: equal true positive and false positive rates across groups
- Individual fairness: similar individuals receive similar predictions

**Process fairness:**
- Protected attribute exclusion verification — direct and proxy variable analysis
- Training data representativeness audit against known population distributions

**Impact assessment:**
- Disparate impact ratio: adverse outcome rate for disadvantaged group / advantaged group (legal threshold: less than 0.8 constitutes prima facie discrimination in US employment law)

Detection signals: statistical parity differences exceeding configured tolerance thresholds, proxy variable detection through mutual information analysis of input features.

## 2. Fairness Metrics Framework

| Metric | Formula | Acceptable Threshold |
|---|---|---|
| Demographic Parity Difference | P(pos|A=0) - P(pos|A=1) | <= 0.05 |
| Equalized Odds Difference | max(TPR diff, FPR diff) | <= 0.05 |
| Disparate Impact Ratio | P(pos|A=0) / P(pos|A=1) | >= 0.80 |
| Calibration Error | max E[Y-hat - Y|A] across groups | <= 0.02 |

Metrics are computed per model version, per deployment environment, and per protected attribute class. Results are persisted as time-series evidence for regulatory audit.

## 3. Explainability Requirements

High-risk AI systems must provide human-intelligible explanations for decisions affecting individuals.

**SHAP/LIME integration check**: model endpoints must expose a `/explain` interface or equivalent side-channel producing feature attribution scores.

**Right to explanation**: any decision made about an individual must be explainable in plain language within 72 hours of request (EU AI Act Article 13, GDPR Article 22).

**Counterfactual explanations**: systems making adverse decisions must be capable of generating "what would need to change for a different outcome" responses.

This agent audits explanation quality using:
- Faithfulness: do explanations accurately reflect model internals, not post-hoc rationalizations
- Consistency: same input produces same explanation across invocations
- Completeness: explanation covers all features with material contribution (contribution > 1%)

## 4. Model Transparency

Model cards are mandatory documentation artifacts for every AI system in USAP scope. Required sections:
- Model details: architecture, training approach, version, contact
- Intended uses and out-of-scope uses explicitly documented
- Training data: sources, collection methodology, preprocessing steps
- Evaluation results: performance metrics across demographic subgroups
- Ethical considerations: known limitations, potential harms, mitigation measures
- Caveats and recommendations: deployment constraints and monitoring requirements

Missing or stale model cards (last updated > 90 days before last model version change) generate a HIGH severity finding requiring remediation before next deployment.

## 5. EU AI Act Compliance

**Prohibited AI practices** (Article 5 — blanket prohibition):
- Real-time remote biometric identification in public spaces by law enforcement (with exceptions)
- Social scoring systems by public authorities
- Manipulation using subliminal techniques
- Exploitation of vulnerabilities of specific groups

**High-risk AI systems** (Annex III — mandatory conformity assessment):
- Biometric categorization and identification systems
- Critical infrastructure management
- Education and vocational training access
- Employment and workforce management
- Essential private and public services access
- Law enforcement, migration, and border control
- Administration of justice

High-risk system obligations: conformity assessment, technical documentation, automatic event logging, human oversight, accuracy/robustness/cybersecurity requirements, post-market monitoring.

**GPAI Model obligations** (Chapter V): models with systemic risk (>10^25 FLOPs) require adversarial testing and incident reporting.

## 6. Responsible AI Framework

- **Fairness**: equitable treatment of all individuals and groups
- **Reliability and Safety**: reliable performance within defined operational parameters
- **Privacy and Security**: personal data protection and adversarial manipulation resistance
- **Inclusiveness**: designed to benefit all users, including those with disabilities
- **Transparency**: stakeholders understand capabilities, limitations, and decisions
- **Accountability**: clear human ownership for every AI system in production

Each principle maps to measurable controls assessed quarterly.

## 7. High-Risk AI System Classification Workflow

1. Collect system description, intended use case, affected population, and deployment context
2. Apply EU AI Act Annex III checklist — any match triggers high-risk designation
3. Apply NIST AI RMF (AI 100-1) risk framing: Govern, Map, Measure, Manage
4. Generate risk tier assignment with supporting rationale
5. Emit required governance artifacts: model card template, conformity assessment checklist, human oversight plan
6. Block deployment pathway until all required artifacts are complete and approved

## 8. Human Oversight Requirements

- **Human-in-the-loop**: human reviews every individual AI decision before it takes effect
- **Human-on-the-loop**: human monitors AI decisions in real time with ability to intervene
- **Human-in-command**: human retains ability to shut down the AI system at any time

Oversight tier assignment is based on risk classification and consequence severity of incorrect decisions. The agent monitors override rates — if humans override AI decisions at a rate above 30%, this triggers a model performance review.
