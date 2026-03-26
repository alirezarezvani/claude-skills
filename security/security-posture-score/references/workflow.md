# Security Posture Scoring Workflow

## Step 1: Data Collection

Gather inputs from each domain skill:
- Detection: MTTD, hunt frequency, telemetry coverage %
- Response: MTTR by severity, forensic completion rate
- Cloud: CSPM score, patch SLA compliance, drift incidents
- AppSec: Critical PR findings, SBOM coverage, gate pass rate
- Identity: MFA coverage, privileged access review completion
- Compliance: Framework coverage %, open audit findings
- Governance: Policy coverage, finding closure rate, training %

## Step 2: Domain Scoring

For each domain:
1. Calculate control passing rate
2. Apply maturity multiplier
3. Produce 0–100 domain score

## Step 3: Composite Calculation

Apply domain weights to produce composite 0–100 score.

## Step 4: Trend Analysis

Compare current score to prior period (monthly or quarterly).
Calculate: trend = current_score - prior_score

## Step 5: Scorecard Generation

Produce board-ready scorecard with:
- Composite score + rating
- Domain breakdown table
- Trend indicators (up/down/stable)
- Top 3 improvement priorities
- Peer benchmark guidance
