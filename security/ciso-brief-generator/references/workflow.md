# CISO Brief Generator Workflow

## Step 1: Brief Type Selection

Determine which brief type is needed:
- Monthly CISO Report — for internal executive distribution
- Board Quarterly Brief — for board/audit committee
- Incident Executive Summary — after a SEV1/2 incident
- Regulatory Update Brief — for new compliance requirements

## Step 2: Data Collection

Collect inputs from other USAP skills:
- Security posture score from `security-posture-score`
- Key metrics (MTTR, MTTD, patch coverage) from `metrics-reporting`
- Recent incident summaries from `incident-commander` outputs
- Compliance status from `compliance-mapping`
- Risk posture from `enterprise-risk-assessment`

## Step 3: Message Hierarchy

1. Identify the #1 message the audience needs to take away
2. Identify 3 supporting points that back the #1 message
3. Identify any asks: decisions needed, approvals required, resources needed

## Step 4: Draft Brief

Apply executive communication framework to each section:
- Headline (one sentence, no jargon)
- So What (business risk/opportunity)
- What We Are Doing (concrete actions)
- Ask (if applicable)

## Step 5: Plain Language Review

- Replace all technical acronyms with plain-language equivalents
- Quantify all risks in business terms (revenue, customer, regulatory penalty)
- Verify active voice throughout

## Step 6: Review and Approve

1. Human review of generated brief
2. Verify all metrics are current and accurate
3. Legal/compliance review if regulatory content is included
4. Approve for distribution
