# Forgetting Policy — <system name>

> Fill this in **before** the store grows. Every section maps to a check in
> `forgetting_policy_linter.py`. F1 and F4 are blocking: a design that fails
> either is not ready, regardless of how good its retrieval is.
>
> Copy the JSON block at the bottom into your own file and lint it.

**System:** ____________________  **Named owner:** ____________________
**Store location:** ____________________  **Reviewed:** ____________

---

## F1 — Explicit forgetting rule (BLOCKING)

*No evaluated memory system prunes or forgets by default. If it is not written
here, the store only grows.*

Choose at least one:

- [ ] **TTL** — records expire after `______` days
- [ ] **Capacity bound** — max `______` records / `______` bytes
  - Eviction order: ____________________________________
  - *(The eviction order IS the policy. "LRU" is a decision, not a default —
    recency is a poor proxy for value, and the fact retrieved once a year is
    often the one you cannot reconstruct.)*
- [ ] **Relevance decay** — score decays unless retrieved; expire below `______`

**Exempt from forgetting** (records that must never expire), and why:

```
________________________________________________________
```

## F2 — Dedup at write time

- [ ] Every write is fingerprinted and near-matches collapsed
- Method: ____________________  Threshold: ____________

*Duplicates do not merely waste tokens — they let a stale copy outrank a
corrected one.*

## F3 — Consolidation / compaction

- [ ] Enabled   Cadence: ____________
- What merges into what: ______________________________
- [ ] Merges preserve the source list of every merged record

*Warning: consolidation is lossy, and it amplifies. A merge pass propagates a
wrong (or poisoned) record into derived records, past the point where source
attribution helps.*

## F4 — Contradiction handling (BLOCKING)

- [ ] Contradictions are **surfaced to a human** with both versions, both
      sources, and both timestamps
- Who resolves them: ____________________
- Where they surface: ____________________

**Explicitly forbidden:** `auto_merge`, `newest_wins`, `overwrite`,
`last_write_wins`.

*Two memories that disagree may both have been true in different contexts.
"Deploys go through Jenkins" and "deploys go through GitHub Actions" is not a
contradiction to resolve — it is a migration to record.*

## F5 — Scope

| | Who | Notes |
|---|---|---|
| **Read** | ______________ | |
| **Write** | ______________ | |

- [ ] Read scope and write scope are different
- [ ] Shared / org-wide stores are read-only
- [ ] Components ingesting untrusted content do **not** hold write scope

## F6 — Audit trail

- [ ] Every write carries a timestamp
- [ ] Every write carries source attribution
- Where audit events are visible: ____________________

*Without attribution you can detect a bad fact but not find its origin — which
means you cannot stop it recurring.*

## F7 — Rollback and delete

- [ ] Earlier versions can be restored
- [ ] A single record can be hard-deleted without a migration
- [ ] Content can be **redacted from history** (distinct from version rollback,
      and what erasure obligations such as GDPR Art. 17 actually require)
- Delete path: ____________________  Typical time to delete: __________

## F8 — Growth-slope monitoring

- [ ] Footprint over time is tracked, not just current size
- Alert threshold (slope): ____________________
- Current baseline: ____________  Current slope: ____________/month

*Slope, not starting size, is what bankrupts a long-lived agent.*

---

## Lint this

```json
{
  "name": "<system name>",
  "forgetting": {
    "rule": "ttl",
    "ttl_days": 365,
    "max_records": 50000,
    "decay": "none"
  },
  "dedup_on_write": true,
  "consolidation": { "enabled": true, "cadence": "weekly" },
  "contradiction_policy": "surface",
  "scope": {
    "read": ["<who reads>"],
    "write": ["<who writes>"]
  },
  "audit_trail": { "timestamp": true, "source_attribution": true },
  "rollback": { "supported": true, "delete_path": "api" },
  "growth_monitoring": { "tracks_slope": true, "baseline_only": false }
}
```

```bash
python scripts/forgetting_policy_linter.py --policy my_policy.json
# exit 0 = PASS · 2 = CONDITIONAL · 4 = FAIL (F1 or F4 failed)
```

**Ship order reminder** — build the write path first and let it fill; add
contradiction detection by hand a few times; add this policy *before* volume
climbs; tune the hardware layer last.
