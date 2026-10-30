# cmmc-readiness

> Level 2 assessments fail in predictable ways: a 5-point gap someone planned to
> defer, an SSP that misses half the assets, a cloud drive holding CUI without
> FedRAMP, and a Conditional status that expires on day 181.

Three deterministic scripts score all 110 NIST SP 800-171 Rev 2 requirements
with the 32 CFR 170.24 weights, check a POA&M against the 180-day closeout
deadline, and sort the asset inventory into the CMMC asset categories. No SPRS
connection, no network: fill CSVs and run.

Built for the request in discussion #358: CMMC 2.0 Level 2, grounded in NIST SP
800-171 Rev 2, with a path to Rev 3. Phase 2 of the CMMC rollout, which adds
Level 2 (C3PAO) certification as a condition of award, starts 10 November 2026.

**Not an assessment and not legal advice.** A C3PAO or DIBCAC assessor decides
MET, and only your Affirming Official affirms in SPRS.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install cmmc-readiness@claude-code-skills
```

## Use

```bash
/cs-cmmc-readiness inventory.csv assessment.csv poam.csv --conditional-date 2026-06-15   # full pass
/cs-sprs-score assessment.csv                                                           # just the score
```

Or run the scripts directly. Each has `--help`, `--sample` and `--output json`:

```bash
cd skills/cmmc-readiness
python scripts/scope_classifier.py --sample
python scripts/sprs_score.py --sample
python scripts/poam_closeout.py --sample
```

## The three scripts

| Script | Question | Exit codes |
|---|---|---|
| `sprs_score.py` | What is the score, and can we reach **Conditional** (88+, only deferrable gaps) or **Final** (110)? Lists what to fix before any assessment | 0 final · 2 conditional · 3 · **4 not eligible** |
| `poam_closeout.py` | Does the POA&M cover exactly the deferred gaps, with owners and dates **inside 180 days**? Prints the expiry and annual affirmation dates | 0 ready · 2 open · 3 · **4 blocked / expired** |
| `scope_classifier.py` | Which assets are CUI, Security Protection, Contractor Risk Managed, Specialized or Out-of-Scope? Blocks on assets **missing from the SSP** and **CSPs holding CUI without FedRAMP** | 0 · 2 · 3 · **4 blocked** |

## What it cites

32 CFR 170.3 (phases), 170.19 (scoping, Tables 3 and 4), 170.21 (POA&M), 170.22
(affirmations) and 170.24 (scoring); DFARS 252.204-7012(b)(2)(ii)(D); DoD CIO's
December 2023 FedRAMP Moderate equivalency memo; DFARS class deviation
2024-O0013; NIST SP 800-171 Rev 2, 800-171A, Rev 3 and 800-172. Every claim in
`skills/cmmc-readiness/references/` carries a confidence marker, and where a
rule is our reading rather than the text, it says so.

## Distinct from

- `compliance-os` — multi-framework orchestration (ISO 27001, SOC 2, ISO 13485 and more), no CMMC.
- `access-lifecycle` — access-review evidence, which also supports AC.L2-3.1.1 and PS.L2-3.9.2.
- `ciso-advisor` — security strategy and roadmap; it mentions CMMC but does not score it.

## License

MIT. See the repository [LICENSE](../../LICENSE).
