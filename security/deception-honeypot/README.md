# Deception & Honeypot Strategy

Design deception technology deployments — honeypots, canary tokens, and lateral movement traps — to detect adversaries with near-zero false positives.

## When to use

- You want to detect lateral movement before it reaches crown jewels
- You need a high-fidelity alert source with minimal false positives
- You want to seed fake credentials to catch credential theft
- You are hardening detection coverage gaps in your SOC

## Quick Start

```bash
python scripts/deception-honeypot_tool.py --help
python scripts/deception-honeypot_tool.py --output json
```

## Skill Level: L4

Production honeypot deployment requires operator approval. Canary token strategies can be planned at L3 and deployed at L4.
