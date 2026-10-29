# access-lifecycle

> Access reviews fail audits in ordinary ways: an incomplete export, someone
> approving their own access, a revoke nobody carried out, a leaver still enabled.

Three deterministic scripts diff the HR roster against account exports, check a
review campaign against the population it was built from, and map every
exception to the SOC 2, ISO 27001, NIST 800-53, PCI DSS, HIPAA or SOX control it
breaks. No IdP or HR connection, no network: export CSV and run.

**Not audit advice.** Inactivity periods and remediation windows are your policy.

## Install

```bash
/plugin marketplace add alirezarezvani/claude-skills
/plugin install access-lifecycle@claude-code-skills
```

## Use

```bash
/cs-access-review hr_roster.csv accounts.csv campaign.csv --framework soc2,iso27001   # full pass
/cs-access-diff hr_roster.csv accounts.csv --inactive-days 90                        # just the diff
```

Or run the scripts directly. Each has `--help`, `--sample` and `--output json`:

```bash
cd skills/access-lifecycle
python scripts/access_diff.py --sample
python scripts/access_review_campaign.py --sample
python scripts/control_evidence_mapper.py --sample --framework soc2,iso27001,pci
```

## The three scripts

| Script | Question | Exit codes |
|---|---|---|
| `access_diff.py` | Who has access they should not? Leavers enabled or **used after exit**, orphans, ownerless service accounts, movers, privileged review age, inactivity | 0 · 2 findings · 3 · **4 blocked** |
| `access_review_campaign.py` | Did the review cover the population, and did the revokes happen? **Population gaps**, undecided, **self-review**, unremoved revokes, late decisions, rubber-stamp signal | 0 · 2 · 3 · **4 incomplete** |
| `control_evidence_mapper.py` | Which controls fail, and what evidence do we keep? FAIL / EXCEPTIONS / NO_EXCEPTIONS / PARTLY_TESTED / NOT_TESTED / NOT_COVERED — never PASS | 0 · 2 · 3 · **4 fail** |

## What it cites

AICPA Trust Services Criteria CC6.1–CC6.3; NIST SP 800-53 Rev 5 AC-2, AC-2(3)
and AC-5 with FedRAMP parameter values; PCI DSS v4.0.1 7.2.4, 7.2.5.1, 8.2.5
and 8.2.6; HIPAA 45 CFR 164.308(a)(3)(ii)(C); PCAOB AS 1105.10 and Staff Audit
Practice Alert 11; ISO/IEC 27001:2022 Annex A titles. Every claim in
`skills/access-lifecycle/references/` carries a confidence marker, and the
finding-to-control mapping is labelled as our judgment.

## Distinct from

- `soc2-compliance` — SOC 2 readiness and control design across all criteria.
- `information-security-manager-iso27001` — ISMS design and Statement of Applicability.
- `isms-audit-expert` — internal audit programme and nonconformity handling.

## License

MIT. See the repository [LICENSE](../../LICENSE).
