# Domain audit: ra-qm-team/ + compliance-os/ — new-gen model optimization
Audited: 2026-06-10 · Skills: 26 distinct (17 ra-qm-team incl. meta + 9 compliance-os; +2 verbatim sub-plugin duplicates) · Agents: 9 (8 compliance-os + cs-quality-regulatory) · Commands: 0 standalone (8 compliance-os skills are /cs:* command-shaped) · Plugins: 4 manifests (1 in marketplace)

## Scorecard

| Skill | Verdict | Top issue |
|---|---|---|
| ra-qm-team/capa-officer | OPTIMIZE | Cites 21 CFR 820.100 as current; removed by QMSR (eff. 2026-02-02) |
| ra-qm-team/eu-ai-act-specialist | OPTIMIZE | Embedded sample mis-teaches Art. 5(1)(f): tags RETAIL emotion recognition as prohibited (workplace/education only) |
| ra-qm-team/fda-consultant-specialist | REWRITE | Entire QSR section presents pre-QMSR 21 CFR 820 as current law; FY2024 user fees |
| ra-qm-team/gdpr-dsgvo-expert | OPTIMIZE | "30 days" deadlines (Art. 12(3) says one month + 2-month extension); WP29 framing; score-without-owner output |
| ra-qm-team/information-security-manager-iso27001 | OPTIMIZE | "Overall Compliance: 87%" auto-verdict example; thin clause citation; generic IR section |
| ra-qm-team/isms-audit-expert | KEEP | — |
| ra-qm-team/iso42001-specialist | KEEP | — (exemplary; template for the rest of the domain) |
| ra-qm-team/mdr-745-specialist | OPTIMIZE | PSUR table contradicts MDR Art. 86(1); IIb conformity-route table garbled; no Reg. 2023/607 transition note |
| ra-qm-team/qms-audit-expert | KEEP | — |
| ra-qm-team/quality-documentation-manager | OPTIMIZE | FDA table cites removed 820.40/.180/.181/.184/.186 as current |
| ra-qm-team/quality-manager-qmr | OPTIMIZE | Compliance matrix: "21 CFR 820 / QSR compliance" stale; "MPG/MPDG" half-stale |
| ra-qm-team/quality-manager-qms-iso13485 | OPTIMIZE | Record-retention table cites removed 820.30/.181/.184/.198 sections |
| ra-qm-team/ra-qm-skills (meta) | CUT-OR-MERGE | 66-line catalog with wrong paths and wrong skill count; adds no behavior |
| ra-qm-team/regulatory-affairs-head | OPTIMIZE | "~$22K (2024)" fee labeled current; QSR framing in pathway step 2 |
| ra-qm-team/risk-management-specialist | OPTIMIZE | ALARP w/ cost-benefit ("Proportionality") contradicts EU MDR "as far as possible" (EN ISO 14971:2019/A11:2021) |
| ra-qm-team/soc2-compliance | KEEP | — |
| ra-qm-team/compliance-team-eu-ai-act/* (dup) | CUT-OR-MERGE | Byte-identical copy of skills/eu-ai-act-specialist; drift risk |
| ra-qm-team/compliance-team-iso42001/* (dup) | CUT-OR-MERGE | Byte-identical copy of skills/iso42001-specialist; drift risk |
| compliance-os/compliance-os | KEEP | — (plugin.json description drift noted under Plugins) |
| compliance-os/compliance-readiness | KEEP | — |
| compliance-os/aims-audit | KEEP | — |
| compliance-os/ai-act-readiness | KEEP | — (phasing dates 2025-02-02/2025-08-02/2026-08-02/2027-08-02 correct) |
| compliance-os/gdpr-audit-prep | KEEP | — |
| compliance-os/iso27001-audit-prep | KEEP | — (typo: "Article 9.3" should be "Clause 9.3") |
| compliance-os/iso13485-audit-prep | KEEP | — |
| compliance-os/soc2-audit-prep | KEEP | — |
| compliance-os/fda-qsr-audit-prep | OPTIMIZE | Acknowledges QMSR yet cites removed 820.75/.100/.180/.198/.250 as live citations |

**Counts:** KEEP 13 · OPTIMIZE 11 · REWRITE 1 · CUT-OR-MERGE 1 (+2 duplicate copies)

## Domain-level findings

**1. The domain is two generations in one tree.** The 2026-05 wave (eu-ai-act-specialist, iso42001-specialist, all of compliance-os) is the best compliance work in the repo: Article/Clause-cited verdicts, explicit NOT-boundaries, deterministic tools with embedded samples, "Your Decision: [the call only the compliance officer can make]" output blocks, outside-counsel routing. The legacy 2025-era wave (the other 14 ra-qm-team skills) is competent practitioner content but pre-dates the citation-discipline pattern and has not been re-baselined against 2026 regulatory state.

**2. FDA QMSR is the single largest freshness failure (REWRITE/OPTIMIZE driver for 6 skills).** The FDA Quality Management System Regulation (final rule 89 FR 7496) replaced the QSR effective 2026-02-02 — four months before this audit. It incorporates ISO 13485:2016 by reference and REMOVES the subsection structure the legacy skills cite as current: 820.20/.30/.40/.50/.70/.75/.100/.180/.181/.184/.186/.198 no longer exist (retained/renumbered: 820.10 requirements, 820.35 records, 820.45 labeling+packaging; 21 CFR 801/803/806/830 unchanged). `fda-consultant-specialist` (skill + qsr_compliance_requirements.md reference + qsr_compliance_checker.py `--section 820.30` interface) has ZERO mentions of QMSR. Ironically, the compliance-os agent `cs-fda-qsr-auditor` and `fda-qsr-audit-prep` correctly state "substantially harmonized post-Feb 2026" — the fresh layer knows what the underlying skill it wraps does not.

**3. Citation precision: good-to-excellent in the new wave, mixed in legacy.** New-wave outputs cite Article+paragraph by contract ("do not paraphrase without cite"). Legacy skills cite at clause level (ISO 13485 4.2.3, 7.5.6, 8.5.2; GDPR Art. 6/9/35; MDR Annex II/VIII/XIV; MDCG 2019-11) — adequate — but carry concrete precision errors a notified-body auditor would flag: (a) mdr-745-specialist PSUR table says Class IIb "every 2 years" / IIa "when necessary" — MDR Art. 86(1) requires IIb+III at least annually and IIa at least every two years; (b) risk-management-specialist's ALARP framework includes "Cost-benefit of further reduction", which EU MDR Annex I §2 + the EN ISO 14971:2019/A11:2021 Z-annexes explicitly disallow (risk reduction "as far as possible" without economic consideration); (c) the eu-ai-act-specialist embedded sample tags a retail-store CCTV emotion-recognition system with `article_5_practice: emotion_recognition_in_workplace_or_education` — retail emotion recognition is Art. 50(3) transparency, not Art. 5 prohibited; the default `--sample` run teaches the wrong rule.

**4. Auto-decide vs route-to-human: NO skill auto-decides compliance verdicts; discipline is explicit in the new wave, implicit in legacy.** Every compliance-os and 2026-wave skill ends with a named-human handoff ("Your Decision: … compliance officer or legal counsel", "Outside Counsel Required" sections, cs-dpo-gdpr hard rule routing novel cases to GC). Legacy skills embed human signoff in workflows (CAPA approval signatures, "Classification confirmed with Notified Body", CER "reviewed by qualified evaluator") but lack an explicit handoff block, and two tool-output examples drift toward verdict-shaped numbers without an owner: information-security-manager's "Overall Compliance: 87%" and gdpr_compliance_checker's "Compliance score (0-100)". Not REWRITE-level — they are framed as prep/self-check tools — but every OPTIMIZE pass should add the new-wave "Your Decision" block.

**5. The "49 no-source references" repo flag is ~80% false positive in this domain.** 63 reference files in scope (55 distinct after sub-plugin dedup). Only ~8 have a formal "Sources" heading — which is what the repo validator keys on — but ~45 carry dense inline regulatory citations (Article/Clause/§/CFR/Annex markers; the AI Act and 13485 playbooks run 37–94 citation markers per file). Genuine zero-citation gaps ≈ 9 files, all generic-methodology docs: capa-officer/rca-methodologies.md + effectiveness-verification-guide.md, risk-management-specialist/risk-analysis-methods.md + risk-assessment-templates.md (77 lines, thin), quality-manager-qmr/quality-kpi-framework.md, information-security-manager-iso27001/incident-response.md, soc2-compliance/type1_vs_type2.md + evidence_collection_guide.md, qms-audit-expert/nonconformity-classification.md (1 marker). Fix: add a Sources block to those 9; do not bulk-rewrite the other 45.

**6. New-gen model lens.** Frontier models know ISO/GDPR/MDR basics; what earns context here is exactly what the new wave ships: clause-keyed gap analyzers with readiness verdicts, mock-audit scenario libraries (205 scenarios), evidence-reuse maps with confidence ratings, audit-prep interrogations with sample-driven "show me the record" questions. Legacy skills that mostly restate standard structure (info-sec manager's ISMS-implementation prose, parts of quality-manager-qmr) are the weakest A2 performers; their tools and checklists still earn their place.

**7. Cross-plugin coupling.** compliance-os skills invoke `../../../ra-qm-team/skills/*/scripts/*.py` by relative path. Works in the monorepo; breaks when plugins install independently (compliance-os plugin does not ship those scripts). Violates the repo "skills are self-contained" principle — at minimum document the ra-qm-skills co-install requirement in the manifest.

**8. Cruft.** 12 legacy `.zip` archives + `final-complete-skills-collection.md` committed at ra-qm-team/ root; ra-qm-team/CLAUDE.md says "14/14 skills" (folder has 16 + meta; omits eu-ai-act + iso42001 entirely, so the domain's own nav file hides its two best skills).

## Per-skill findings

### ra-qm-team/fda-consultant-specialist — REWRITE
Issues:
1. QSR section ("Quality System Regulation (21 CFR Part 820)") + subsystem table (820.20–820.181) presented as current; QMSR replaced this structure effective 2026-02-02 — wrong regulatory guidance in the highest-stakes lane.
2. `references/qsr_compliance_requirements.md` (753 lines) and `qsr_compliance_checker.py --section 820.30` interface built entirely on removed section numbers; zero QMSR mentions anywhere in the skill.
3. Fee table is FY2024 ($21,760 510(k) / $134,676 De Novo / $425,000+ PMA) with no fiscal-year label or MDUFA pointer.
4. Description still sells "QSR (21 CFR 820) compliance" — trigger text itself stale.
5. Pathway/eSTAR/cybersecurity/HIPAA content remains sound — structure salvageable, QSR third needs rebuild around ISO 13485-by-reference + retained 820.10/.35/.45 + unchanged 801/803/806/830.
Verify:
- `grep -ri QMSR ra-qm-team/skills/fda-consultant-specialist/ | wc -l` ≥ 5 (SKILL.md, description, qsr reference, checker help).
- `grep -rE '820\.(20|30|40|50|70|100|181|198)' SKILL.md references/` returns only lines explicitly marked historical/pre-2026.
- `python3 scripts/qsr_compliance_checker.py --help` exits 0 and help text names QMSR/ISO 13485, not "21 CFR 820 compliance" alone.
- Fee table rows carry an explicit FY label and "verify at fda.gov MDUFA" note.

### ra-qm-team/ra-qm-skills — CUT-OR-MERGE
Issues:
1. 66-line catalog page; duplicates README/plugin.json function; no workflow, no tools, no verification — fails A2/A4.
2. Says "12 skills" while the folder ships 16 and plugin.json says 14 — three conflicting counts.
3. Quick-start path `ra-qm-team/regulatory-affairs-head/SKILL.md` is wrong (missing `skills/` segment).
4. Omits eu-ai-act-specialist, iso42001-specialist, soc2-compliance from its table.
Verify:
- Folder removed (catalog content merged into ra-qm-team/README.md), OR rewritten as a real router; if kept: skill count matches `ls ra-qm-team/skills | wc -l` minus itself, and every path in the table resolves (`test -f` loop exits 0).

### ra-qm-team/risk-management-specialist — OPTIMIZE
Issues:
1. ALARP used as the acceptability framework incl. "Proportionality | Cost-benefit of further reduction" — EU MDR Annex I §2 + EN ISO 14971:2019/A11:2021 Z-annexes prohibit economic considerations; for CE-marked devices the criterion is "as far as possible" (AFAP). A notified body flags this exact table.
2. ISO 14971:2019 itself dropped ALARP from the normative body; skill presents it as the standard's method.
3. `references/risk-analysis-methods.md` + `risk-assessment-templates.md` (77 lines) cite zero sources.
4. No explicit named-human handoff for residual-risk acceptance (it's implied via "management signoff" only in iso42001-specialist, not here).
Verify:
- `grep -c 'as far as possible\|AFAP' SKILL.md` ≥ 2 and ALARP appears only with an explicit "non-EU / not acceptable under MDR" caveat.
- `grep -c 'Cost-benefit' SKILL.md` = 0 in the EU acceptability context.
- `python3 scripts/risk_matrix_calculator.py -p 4 -s 5 --output json` exits 0, emits `risk_level` key.

### ra-qm-team/mdr-745-specialist — OPTIMIZE
Issues:
1. PSUR table wrong vs MDR Art. 86(1): says IIb "Every 2 years", IIa "When necessary" — regulation requires IIb (all, not just implantable) at least annually, IIa at least every 2 years.
2. Conformity-route row "IIb | Annex IX + X or X + XI" garbled (routes are Annex IX, or Annex X+XI).
3. No mention of Reg. (EU) 2023/607 extended transition (legacy MDD devices to 2027/2028) — the question every MDR client asks first in 2026.
4. PMS table cites "PMS Plan | Article 84" correctly but omits Art. 83 (system) and Art. 86 (PSUR) cites where the schedule lives.
Verify:
- PSUR table matches Art. 86(1) verbatim cadence (`grep -A4 'PSUR Schedule' SKILL.md` shows IIb=annual, IIa=every 2 years).
- `grep -c '2023/607' SKILL.md references/` ≥ 1.
- `python3 scripts/mdr_gap_analyzer.py --device Test --class IIa --output json` exits 0 with gap list.

### ra-qm-team/eu-ai-act-specialist — OPTIMIZE
Issues:
1. Embedded sample system "Emotion recognition in retail store CCTV" is hard-tagged `article_5_practice: emotion_recognition_in_workplace_or_education` → default `--sample` output declares retail emotion recognition PROHIBITED. Correct treatment: Art. 50(3) transparency (limited-risk). Wrong teaching in the default demo of a flagship skill.
2. Classifier trusts caller-supplied `article_5_practice` flags rather than deriving from context fields it already collects (`users`, `intended_purpose`) — at minimum the docstring should state the flag is the user's legal pre-determination.
3. Verbatim duplicate at compliance-team-eu-ai-act/ (see Plugins).
Verify:
- `python3 scripts/ai_system_risk_classifier.py` sample output classifies the retail-CCTV system as LIMITED-RISK citing Art. 50(3), or the sample is changed to a genuine workplace context.
- All 3 scripts exit 0 on `--help` and bare run; every verdict line contains "Article".

### ra-qm-team/gdpr-dsgvo-expert — OPTIMIZE
Issues:
1. Rights table + body say "30 days" / "extendable to 90" — Art. 12(3) is one month, extendable by two further months; in a deadline-tracking tool the month/30-day distinction loses up to 3 days.
2. "WP29 high-risk criteria" — EDPB-endorsed but should be cited as EDPB/WP248 rev.01.
3. Compliance checker emits 0-100 score with no named-DPO routing block; SKILL.md has no "Your Decision" handoff (contrast gdpr-audit-prep which does this right).
4. No mention of EU-US Data Privacy Framework / Chapter V transfer tooling in SKILL.md (playbook reference covers it; surface a pointer).
Verify:
- `grep -c 'one month' SKILL.md` ≥ 1; `grep -c '30 days' SKILL.md` = 0 in the Art. 12 deadline context.
- `python3 scripts/data_subject_rights_tracker.py add --type access --subject T --email t@x.de` then `list` exits 0; due-date computed by calendar month.
- SKILL.md gains an output block routing final determinations to DPO/counsel.

### ra-qm-team/information-security-manager-iso27001 — OPTIMIZE
Issues:
1. Worked example ends "Overall Compliance: 87%" with no owner/handoff — the closest thing to an auto-verdict in the domain.
2. Body is clause-thin (only 6.1.2 cited); 2022 control IDs appear only in the example; A5 weak for a new-gen model (ISMS-implementation prose a frontier model already knows).
3. `references/incident-response.md` (420 lines) cites zero sources and duplicates engineering-team incident-response ground.
4. CLI surface in SKILL.md (`--template healthcare`, `--domains`) must be verified against actual argparse (legacy doc drift risk).
Verify:
- Every documented flag exists: `python3 scripts/risk_assessment.py --help` and `compliance_checker.py --help` list `--scope/--template/--standard/--gap-analysis`.
- Worked example ends with a named-human review step (ISMS owner / CISO) instead of bare percentage.
- incident-response.md gains a Sources block (≥3: ISO 27035, NIST SP 800-61r3, A.5.24-26) or is cut in favor of a pointer.

### ra-qm-team/capa-officer — OPTIMIZE
Issues:
1. "FDA 21 CFR 820.100" requirements section presents removed regulation as current (QMSR: CAPA now flows through ISO 13485 8.5.2/8.5.3 incorporated by reference).
2. `references/rca-methodologies.md` + `effectiveness-verification-guide.md` (917 lines combined) cite zero sources.
3. Otherwise the strongest legacy skill (decision trees, validated 5-Why example, metrics with formulas) — targeted edits only.
Verify:
- 820.100 section reframed as "pre-2026 QSR / now via ISO 13485 8.5 under QMSR" (`grep -c QMSR SKILL.md` ≥ 1).
- `python3 scripts/capa_tracker.py --sample > /tmp/c.json && python3 scripts/capa_tracker.py --capas /tmp/c.json --output json` exits 0 with summary metrics keys.

### ra-qm-team/quality-documentation-manager — OPTIMIZE
Issues:
1. "FDA 21 CFR 820" table (820.40/.180/.181/.184/.186) presents removed sections as current; under QMSR records requirements live in 820.35 + ISO 13485 4.2.4/4.2.5.
2. Part 11 content is solid and unaffected — single-table fix plus reference sweep of 21cfr11-compliance-guide.md for cross-refs into old 820.
Verify:
- FDA table updated to QMSR structure; `grep -E '820\.(40|181|184|186)' SKILL.md` only in historical context.
- `python3 scripts/document_validator.py --sample > /tmp/d.json && python3 scripts/document_validator.py --doc /tmp/d.json --output json` exits 0.

### ra-qm-team/quality-manager-qms-iso13485 — OPTIMIZE
Issues:
1. Record-retention table regulatory basis column cites removed 820.181/.184/.30/.198.
2. Otherwise strong (exclusion table, validation standards ISO 11135/11137/17665, supplier scoring) — single-table fix.
Verify:
- Retention table bases updated to QMSR/ISO 13485 cites.
- `python3 scripts/qms_audit_checklist.py --clause 7.3` exits 0 and emits 7.3-specific questions.

### ra-qm-team/quality-manager-qmr — OPTIMIZE
Issues:
1. Multi-jurisdiction matrix: "USA | 21 CFR 820 | FDA registration, QSR compliance" stale post-QMSR; "Germany | MPG/MPDG" — MPG repealed 2021, list MPDG/MPEUAnpG only.
2. Generic culture-survey and KPI content is the domain's weakest A2 (frontier model knows it); KPI reference cites zero sources.
Verify:
- Matrix row reads QMSR; `grep -c 'MPG/' SKILL.md` = 0.
- `python3 scripts/management_review_tracker.py --help` exits 0.

### ra-qm-team/regulatory-affairs-head — OPTIMIZE
Issues:
1. Pathway matrix fees "~$22K (2024)" — stale FY presented as current; needs FY label + MDUFA pointer.
2. Step 2 lists "FDA (US): 21 CFR Part 820" as applicable regulation without QMSR framing.
3. Overlap with mdr-745-specialist + fda-consultant-specialist is acceptable (strategy vs execution split) but should cross-link rather than restate the SE table.
Verify:
- Fee cells carry FY labels; `grep -c QMSR SKILL.md` ≥ 1.
- `python3 scripts/regulatory_tracker.py --help` exits 0.

### compliance-os/fda-qsr-audit-prep — OPTIMIZE
Issues:
1. Correctly states post-Feb-2026 harmonization, then cites removed sections as live law throughout (820.198, 820.75, 820.100, 820.180, 820.250) — internally inconsistent; the right cites are ISO 13485 clauses (8.2.2, 7.5.6, 8.5.2, 4.2.5) + retained 820.35/.45 + unchanged 803/801/830/806.
2. Workflow shells into fda-consultant-specialist scripts whose interfaces are themselves pre-QMSR (`--section 820.30`) — blocked on the REWRITE above.
Verify:
- Each of the six questions cites the QMSR-era source (ISO 13485 clause or retained CFR section); `grep -E '820\.(75|100|180|198|250)' SKILL.md` only with "pre-QMSR" annotation.
- Workflow paths resolve after the fda-consultant-specialist rewrite.

### Duplicate sub-plugins (compliance-team-eu-ai-act/, compliance-team-iso42001/) — CUT-OR-MERGE
Issues:
1. `diff -r` confirms byte-identical copies of ra-qm-team/skills/{eu-ai-act,iso42001}-specialist — two sources of truth; the Art. 5 sample bug must now be fixed twice.
2. Neither sub-plugin is registered in marketplace.json, so the duplication currently buys nothing.
Verify:
- Either sub-plugins deleted (standalone install served by marketplace entry pointing at the skills/ copy), or a sync script/CI check asserts `diff -r` emptiness on every PR.

## KEEP-verdict verification criteria

- **iso42001-specialist:** `python3 scripts/aims_gap_analyzer.py` exits 0, prints `Certification readiness:` ∈ {ready, stage_2_candidate, not_ready} + weighted coverage %; all 3 tools pass bare run; every gap line carries a Clause number.
- **isms-audit-expert:** `python3 scripts/isms_audit_scheduler.py --year 2026 --format markdown` exits 0 and emits a quarter-bucketed plan; finding template retains Requirement/Evidence/Gap triple.
- **qms-audit-expert:** `python3 scripts/audit_schedule_optimizer.py --interactive` help path exits 0; clause-scope table keeps 4.2→8.5 coverage; classification decision tree intact.
- **soc2-compliance:** `python3 scripts/control_matrix_builder.py --categories security --format json` exits 0 with ≥1 control per CC1–CC9; gap_analyzer distinguishes type1/type2 modes.
- **compliance-os (orchestrator):** all 4 tools exit 0 on bare run; `audit_simulator.py` output reports `healthy=` against the ≥40% observation / ≤15% critical rule; `assets/mock_audit_library.json` parses with 205 scenarios.
- **compliance-readiness:** output template retains the 🟢/🟡/🔴 verdict + "Top 3 Actions with owners" + routing block; all 4 workflow script paths resolve from the skill dir.
- **aims-audit:** 6 questions each name a Clause or Annex A control; workflow paths into ra-qm-team resolve; routes verdict to `/cs:decide`.
- **ai-act-readiness:** phasing dates remain exactly 2025-02-02 / 2025-08-02 / 2026-08-02 / 2027-08-02; "Legal Review Required" section retained; every question keeps its Article cite.
- **gdpr-audit-prep:** Art. 12(3) one-month language retained; Art. 30/35(7)/33(5) cites intact; "Outside Counsel Required" section retained.
- **iso27001-audit-prep:** fix "Article 9.3"→"Clause 9.3"; 3-year-coverage question + auditor-independence check retained; scheduler path resolves.
- **iso13485-audit-prep:** Clause cites (8.2.4, 7.5.6, 5.6.2/5.6.3) intact; DHF-sampling question retains stratification by class.
- **soc2-audit-prep:** observation-period discipline questions (cycle skips, first-month evidence, exception materiality) retained; AT-C 205 cite intact.

## Agents

All 9 pass B1–B3. The 8 compliance-os personas are the best-differentiated agent set audited: each has a distinct voice that changes behavior (cs-ciso-iso27001 "samples, not demos"; cs-dpo-gdpr refuses to paraphrase the Regulation; cs-fda-qsr-auditor tracks Form 483 gradient distinct from ISO NC grades), explicit vs-sibling differentiation paragraphs, and hard rules that route novel/legal calls to GC or outside counsel — the route-to-human discipline the legacy skills lack lives here. cs-fda-qsr-auditor is also the only artifact in either domain that correctly states the QMSR transition.
Issues: (1) cs-fda-qsr-auditor still cites removed 820.x section numbers in its forcing questions — inherits the fda-qsr-audit-prep fix. (2) All 8 pin `model: opus` — pre-Fable-era pin; revisit per repo model policy. (3) `skills:` frontmatter uses repo-relative paths (`ra-qm-team/skills/...`) that break outside the monorepo. (4) cs-quality-regulatory (agents/ra-qm-team/) is generic by comparison (sonnet, catalog-style body, no voice/forcing questions, no QMSR awareness) — OPTIMIZE to the compliance-os persona pattern, and its skill paths omit the `skills/` segment.

## Plugin manifests

| Manifest | E1 schema | E2 description | E3 marketplace |
|---|---|---|---|
| ra-qm-team/.claude-plugin/plugin.json | PASS (`"skills": ["./skills"]`) | DRIFT — "14 skills"; folder ships 16 + meta (eu-ai-act + iso42001 + soc2 uncounted) | Registered (v2.9.0) |
| compliance-os/.claude-plugin/plugin.json | PASS (9 explicit paths) | DRIFT — claims "9 supported frameworks" + "3 cs-* agents + 3 commands"; SKILL.md/tools support 12 frameworks, 8 agents, 8 command-skills ship | **NOT in marketplace.json** (66 plugins, none sourced from ./compliance-os) |
| ra-qm-team/compliance-team-eu-ai-act/plugin.json | PASS | OK | **NOT in marketplace.json** |
| ra-qm-team/compliance-team-iso42001/plugin.json | PASS | OK | **NOT in marketplace.json** |

Findings: (1) Three of four manifests are orphans — built as plugins, never registered; either register them or delete the sub-plugin duplicates and fold compliance-os registration into the next marketplace bump. (2) compliance-os skills depend at runtime on ra-qm-team scripts via `../../../` paths — manifest must declare the co-install requirement or vendor the scripts. (3) ra-qm-team ships 12 stale `.zip` skill archives + `final-complete-skills-collection.md` at domain root — remove from the public tree. (4) ra-qm-team/CLAUDE.md ("14/14 skills", omits the domain's two flagship 2026 skills) and root CLAUDE.md ("18 RA/QM skills") disagree with each other and with the folder; reconcile counts in one pass.
