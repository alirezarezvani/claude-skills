# People's data: consent, de-identification, limits of use

The skill works with specific people talking about their job, their resignation, a conflict, a hiring
decision. That is personal data, and some lenses additionally feed decisions ABOUT those people. Below is
the gate to clear in S0, before the transcript goes anywhere. This is working discipline, not legal advice:
the regulatory regime (GDPR, local data-protection law, sector rules) is your counsel's call, not this file's.

## The S0 gate — three questions before you start

1. **Does the respondent consent** to recording, transcription and analysis — and does that consent cover
   THIS analysis? Consent to "a recording for the minutes" is not consent to an LLM pipeline and to being
   quoted in a stakeholder report. No clear answer → don't start, ask the client.
2. **Where the text goes.** The whole transcript travels to the model, and in S3 once per run. If the material
   must not leave your perimeter, that is settled BEFORE S1 (local model, de-identification, or declining),
   not after.
3. **Is de-identification required** — and to what degree. Default for sensitive lenses: de-identify.

## What exactly to de-identify

Replace with stable pseudonyms (`Respondent-1`, `Colleague-A`, `System-1`) rather than deleting: mapping needs
the coherence, and the mapping table is stored apart from the transcript and never reaches the report.

- Names and surnames — the respondent's, colleagues', managers', clients'.
- A job title bound to a small department: "the only registrar in the collections department" de-anonymizes
  harder than a surname does.
- Contacts, addresses, document numbers, an individual's salary figures.
- Names of internal systems and projects — where their very existence is confidential.
- Rare biographical details (illness, family composition, criminal record, religion), especially ones dropped
  in passing: they are almost never needed by a cell and almost always identify.

What NOT to de-identify: the substance of the problem, the sequence of events, process numbers — otherwise the
mapping loses its point.

**Pseudonymization ≠ anonymization.** Five interviews from an eight-person department de-anonymize each other
even without names. For small teams the honest output is aggregation to a level where no individual can be
reconstructed, or named quoting agreed with the respondents.

## De-identification vs traceability — how not to break one with the other

The skill rests on verbatim quotes and line numbers. The order that preserves both: de-identify **before**
`number_lines.py`, so the whole pipeline runs on the de-identified text and `verify_quotes.py` checks quotes
against exactly that. De-identify after mapping and the quotes stop matching the source — you get mass
`rejected` not because the model invented anything, but because the source was swapped underneath it.

## Higher-risk lenses

- **candidate** — a hiring decision about a person. Cells A2/A3/A5 (attribution, locus of responsibility, red
  flags) assess a personality from a transcript, which is where LLMs are weakest. The skill's output is material
  for the interviewer, not grounds for rejection. Discriminatory attributes (age, family, health, ethnicity,
  beliefs) are not coded at all, even when voiced.
- **exit** — a leaver is exposed, and their words often concern third parties who never consented. Quotes about
  named managers do not go into the report by name.
- **conflict-mediation** — each side is mapped separately and is NOT shown to the other side without explicit
  consent; the mediator decides what to disclose. One side's position retold in the other's words is not mapping.
- **team-retro / focus-group** — participants heard each other, but did not agree to be quoted outside; the
  report uses roles, not names, by default.

## Storage and deletion

- Transcripts, sidecars (`*_nl.timecodes.json`, `*_nl.flags.json`), `claims.json`, `support.json` and the S3 runs
  hold the same personal data as the original — they share its storage regime.
- The pseudonym table lives apart from all of the above.
- A retention period is set up front, together with who deletes it. "Until we no longer need it" is not a period.
- `build_provenance.py`/`render_board.py` assemble a board of quotes into a single file, which is the easiest
  thing of all to share — check it carries no names before sending it.
