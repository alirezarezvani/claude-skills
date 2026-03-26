# security-requirements-review

**Domain:** AppSec / DevSecOps
**Level:** L3 — Practitioner
**Intent:** `analyze`

Proactive security analysis of upstream design documents before any alerts fire. Ingests POA&M, PRDs, architecture docs, project plans, and requirements specs; extracts security-relevant entities; maps to MITRE ATT&CK attack surfaces; and routes findings to downstream skills.

---

## When to use this skill

Use `security-requirements-review` at the **design and requirements phase** of the SDLC — before a line of code is written. It answers the question: *"What security problems are baked into this design?"*

Invoke when:
- A product requirements document is ready for security review
- An architecture document needs trust boundary and data flow analysis
- A POA&M requires remediation gap analysis and regulatory deadline tracking
- A project plan needs security milestone coverage review

Do **not** invoke for live alerts or post-deployment analysis — use `cs-security-analyst` for those.

---

## Quick Start

```bash
# Analyze a PRD
python scripts/security-requirements-review_tool.py --input /path/to/prd.md --output json

# Classify and extract entities from a document
echo '{"document_text": "This product stores PCI cardholder data..."}' \
  | python scripts/pre_analysis.py

# Extract text from any supported format
python ../../../shared/scripts/doc_intake.py --input /path/to/architecture.pdf
```

---

## Supported Input Formats

| Format | Extension | Extraction Method |
|---|---|---|
| Markdown | `.md` | stdlib read |
| Plaintext | `.txt`, `.rst` | stdlib read |
| JSON | `.json` | recursive string extraction |
| YAML | `.yaml`, `.yml` | PyYAML (stdlib fallback) |
| PDF | `.pdf` | pdfminer.six → PyPDF2 → fallback |
| Word | `.docx` | python-docx → fallback |

---

## Output

The skill produces a USAP output contract JSON payload with:

- `agent_slug: "security-requirements-review"`
- `intent_type: "analyze"`
- `severity` — based on worst detected gap (critical/high/medium/low)
- `key_findings` — one entry per critical or high finding
- `evidence_references` — document location for each finding
- `next_agents` — conditional routing based on document type

---

## Files

```
security-requirements-review/
├── SKILL.md                                         # LLM system prompt (this skill's identity)
├── README.md                                        # This file
├── references/workflow.md                           # Document taxonomy + analysis lenses
├── assets/templates/output-template.json            # Output contract template
├── expected_outputs/sample_output.json              # PRD example output
└── scripts/
    ├── security-requirements-review_tool.py         # CLI: --input <file> --output json
    └── pre_analysis.py                              # Document classifier + entity extractor (stdin → JSON)
```

---

## Pre-Analysis Exit Codes

| Code | Meaning |
|---|---|
| 0 | Informational or low findings only |
| 1 | Security design gaps detected (high findings) |
| 2 | Critical architecture issues (no auth, exposed data, hardcoded creds) |

---

## Related Skills

- `risk-threat-modeling` — full STRIDE model for architecture documents
- `compliance-mapping` — regulatory control gap analysis
- `pipeline-security-scan` — pipeline/CI reference scanning
- `appsec-code-review` — code-level security gate configuration
