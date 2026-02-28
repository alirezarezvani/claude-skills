---
name: defi-vault-analyst
description: Performs DeFi vault risk analysis, yield comparison, portfolio assessment, and oracle monitoring across institutional vaults using the Philidor CLI. Use when analyzing DeFi vault safety, comparing yields, checking risk scores, or monitoring protocol health.
---

# DeFi Vault Analyst

Institutional-grade DeFi risk intelligence for analyzing vault safety, comparing yields, assessing portfolio risk, and monitoring oracle health across 1000+ vaults on Morpho, Yearn, Aave, Beefy, and Spark protocols.

## Overview

This skill provides comprehensive DeFi vault analysis using the Philidor CLI. It covers risk scoring, yield screening, portfolio assessment, protocol comparison, and oracle monitoring. All data comes from Philidor's continuously-indexed risk infrastructure covering Ethereum, Base, Arbitrum, and Polygon chains.

Key capabilities:
- **Risk-first analysis** — every vault has a 0-10 risk score decomposed into three vectors
- **Yield screening** — filter and sort vaults by APR, TVL, chain, asset, and risk tier
- **Portfolio assessment** — analyze positions across chains with weighted risk metrics
- **Protocol intelligence** — audit histories, incident records, TVL distribution
- **Oracle monitoring** — real-time Chainlink feed freshness and deviation tracking

## When to Use

- Finding the safest vaults for a given asset or chain
- Comparing yields across protocols with risk-adjusted context
- Screening vaults by strategy type (conservative, balanced, aggressive)
- Analyzing portfolio risk across multiple positions
- Checking protocol security history and audit status
- Monitoring oracle feed health and staleness
- Evaluating curator track records and vault performance
- Getting a market overview of DeFi vault TVL and risk distribution

## Prerequisites

Install the Philidor CLI globally:

```bash
npm install -g @philidorlabs/cli
```

No API key is required. The CLI connects to the public Philidor API.

Verify installation:

```bash
philidor --version
philidor stats
```

## Core Concepts

### Risk Tiers

Every vault receives a risk score from 0 to 10:

| Tier | Score Range | Meaning |
|------|------------|---------|
| **Prime** | 8.0 - 10.0 | Highest safety — blue-chip assets, battle-tested protocols, strong governance |
| **Core** | 5.0 - 7.9 | Moderate risk — established protocols with some complexity or newer assets |
| **Edge** | 0.0 - 4.9 | Higher risk — newer protocols, exotic assets, or limited audit coverage |

### Three Risk Vectors

Risk scores are composed from three independent vectors:

| Vector | Weight | What It Measures |
|--------|--------|-----------------|
| **Asset Composition** | 40% | Underlying asset quality, liquidity depth, oracle reliability |
| **Platform & Strategy** | 40% | Protocol maturity, audit coverage, code complexity, strategy risk |
| **Control** | 20% | Governance structure, upgrade mechanisms, admin key exposure |

### APR Convention

APR values are stored as decimals: `0.05` means 5%. The CLI formats these for display automatically.

- `apr_net` — total APR including base yield + incentive rewards
- `base_apr` — native protocol yield only (lending rate, share price accrual)
- Rewards are broken down by type: `token_incentive`, `points`, `trading_fee`, `strategy`

## Commands

### Finding Safe Vaults

```bash
# Top 10 safest vaults overall
philidor safest

# Safest USDC vaults
philidor safest --asset USDC

# Safest vaults on Ethereum with minimum $10M TVL
philidor safest --chain Ethereum --min-tvl 10000000

# Output as JSON for programmatic use
philidor safest --asset WETH --json
```

### Screening Vaults

```bash
# Conservative preset: Prime tier, >$50M TVL, blue-chip assets
philidor screen conservative

# Balanced preset: Core+ tier, >$5M TVL
philidor screen balanced

# Aggressive preset: all tiers, sorted by APR
philidor screen aggressive

# Custom screen with filters
philidor screen --asset USDC --chain Base --min-tvl 1000000 --sort apr_net --order desc
```

### Searching Vaults

```bash
# Search by name, symbol, or keyword
philidor search "morpho blue"

# Filter by protocol
philidor vaults --protocol morpho --limit 20

# Filter by chain and asset
philidor vaults --chain Ethereum --asset WETH --sort tvl_usd --order desc

# Filter by risk tier
philidor vaults --risk-tier Prime --sort apr_net --order desc
```

### Vault Detail

```bash
# Full vault details by address
philidor vault --network ethereum --address 0x1234...

# Risk breakdown for a specific vault
philidor risk --network ethereum --address 0x1234...

# Compare 2-3 vaults side by side
philidor compare \
  --vault ethereum:0x1234... \
  --vault base:0x5678...
```

### Portfolio Analysis

```bash
# Analyze a portfolio of positions
philidor portfolio \
  --position ethereum:0xVault1:1000000 \
  --position base:0xVault2:500000 \
  --position arbitrum:0xVault3:250000

# JSON output for integration
philidor portfolio \
  --position ethereum:0xVault1:1000000 \
  --position base:0xVault2:500000 \
  --json
```

### Protocol Intelligence

```bash
# Protocol details including audits and incidents
philidor protocol morpho
philidor protocol aave-v3
philidor protocol yearn-v3

# List all curators with their managed vaults
philidor curator steakhouse

# Market overview — total TVL, vault count, risk distribution
philidor stats
```

### Oracle Monitoring

```bash
# Check oracle feed freshness
philidor oracles

# Filter by chain
philidor oracles --chain Ethereum

# JSON output for monitoring pipelines
philidor oracles --json
```

## Agent Workflows

### Workflow 1: Find the Best Vault for an Asset

1. Run `philidor safest --asset USDC --json` to get top safe vaults
2. Pick the top 2-3 candidates by risk score
3. Run `philidor risk --network <net> --address <addr>` on each to get the full risk breakdown
4. Compare APR, TVL, and risk vectors
5. Recommend the vault with the best risk-adjusted yield

### Workflow 2: Compare Protocols

1. Run `philidor protocol morpho` and `philidor protocol aave-v3` for protocol-level data
2. Run `philidor vaults --protocol morpho --asset USDC --json` and same for aave-v3
3. Compare vault counts, TVL, average risk scores, and APR ranges
4. Check audit coverage and incident history
5. Present a side-by-side comparison with recommendation

### Workflow 3: Portfolio Risk Assessment

1. Gather the user's vault positions (network, address, amount)
2. Run `philidor portfolio --position <net>:<addr>:<amount> ...` for aggregate metrics
3. Run `philidor risk --network <net> --address <addr>` for each position
4. Identify concentration risks (single chain, single protocol, single asset)
5. Suggest rebalancing if weighted risk score is below target

### Workflow 4: Monitor Safety

1. Run `philidor oracles --json` to check all oracle feeds
2. Flag any feeds with staleness above threshold
3. Run `philidor stats` for market-wide health
4. Check if any held vaults have had recent incidents
5. Alert on any degradation in risk scores or oracle freshness

## Output Formats

The CLI supports multiple output formats:

| Flag | Format | Use Case |
|------|--------|----------|
| `--json` | JSON | Programmatic processing, piping to jq |
| `--table` | ASCII table | Human-readable terminal output (default) |
| `--csv` | CSV | Spreadsheet export, data analysis |
| `--select <fields>` | Filtered columns | Show only specific fields |
| `--results-only` | Raw data | Skip headers and metadata |

Example with jq:

```bash
# Get just the vault names and APRs
philidor vaults --protocol morpho --json | jq '.[] | {name, apr_net, risk_score}'

# Count vaults by risk tier
philidor vaults --json | jq 'group_by(.risk_tier) | map({tier: .[0].risk_tier, count: length})'
```

## Best Practices

1. **Always use `--json` for analysis** — structured output is more reliable than parsing tables
2. **Check risk before recommending** — never recommend a vault based on APR alone; always verify the risk score and tier
3. **Note data timestamps** — vault data is point-in-time; APR and TVL change continuously
4. **Use TVL as a quality signal** — vaults with higher TVL generally have deeper liquidity and more battle-tested strategies
5. **Cross-reference risk vectors** — a vault may score well overall but have a weak Control score indicating governance risk
6. **Monitor oracle freshness** — stale oracle feeds can indicate upstream issues that affect vault safety
7. **Consider chain risk** — L2 vaults may have additional bridge and sequencer risks not captured in vault-level scoring
8. **Verify protocol audit status** — use `philidor protocol <id>` to check audit coverage before recommending vaults on newer protocols
