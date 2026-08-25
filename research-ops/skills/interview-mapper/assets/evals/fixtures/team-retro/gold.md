# Gold mapping — lens "Team retro" (team-retro)

Source: `transcript.txt` (100 lines, diarized: Marina-facilitator, Igor-product manager,
Dima-dev team lead, Lena-designer, Nastya-backend developer, Oleg-support lead).
Project: "Express-30" feature (30-minute delivery), 3-week sprint, retro on day 8 after release.

## Layer 1 — operational

### T1 Project context
Fact: "Express-30" feature — 30-minute delivery; three-week sprint; retro held
on day 8 in prod; retro attendees — facilitator (agile coach) + product manager + dev team lead +
designer + backend developer + support lead; this is Nastya's first retro with the team.
Quote (Marina): "This is the retro for the "Express-30" launch sprint — 30-minute delivery, three weeks of work, already eight days in prod." — line 2.
Additional quote (Marina, on attendees): "Nastya's with us at retro for the first time" — line 6.
Additional quote (Dima, role): "Dima, backend team lead, three people on the team plus me." — line 8.

### T2 What worked (keep)
Fact 1: synchronous dailies strictly at 15 minutes — proposed (insisted on) by Igor.
Quote (Dima): "Keep for me is that we did dailies strictly at 15 minutes, no dragging on." — line 13.
Quote (Igor, who proposed it): "Yeah, I insisted on the timebox, because last sprint the dailies were running to forty minutes." — line 15.

Fact 2: early alignment of the slot flow mockup with API constraints — Lena's own initiative, before the design was finished.
Quote (Lena): "We locked the slot flow mockup in Figma with comments from Nastya on the API right away, that rarely goes so smoothly." — line 17.
Quote (Nastya, confirmation): "usually I find out about API constraints once the design is already done, but here Lena came to ask herself at the draft stage." — line 18.

Fact 3: cheat sheet for support on typical API errors — sent two days before release (written by Nastya at Igor's request).
Quote (Oleg): "From me — that cheat sheet for operators you sent two days before release." — line 20.
Quote (Nastya, authorship): "Well it was just three paragraphs about typical courier API timeout errors." — line 23.

### T3 What didn't work (stop)
Episode 1 (planning phase): final scope locked only in the second week of a three-week sprint; raised by Dima.
Quote (Dima): "We only got the final feature scope in the second week of the sprint, even though the sprint was three weeks." — line 25.
Specific moment (Dima): "Tuesday of the second week, when Igor sent over the new scope adding courier notifications about address changes — that wasn't in the original spec." — line 29.

Episode 2 (handoff phase): the feature was handed to support for testing one day before release; raised by Dima/Lena.
Quote (Lena): "Another stop — handoff. We handed the feature to support for testing literally one day before release, Oleg didn't have time to run through the scenarios." — line 44.
Quote (Oleg, confirmation): "I got access to the test environment Thursday evening, and the release was Friday afternoon." — line 45.
Consequence: "on day one alone we had twelve tickets about the slot showing "taken" even though the courier was free" (Oleg) — line 48.

Episode 3 (execution/post-release phase): the nightly slot recalculation job failed silently, no alert; raised by Nastya.
Quote (Nastya): "From me — the nightly slot recalculation job would sometimes fail silently, no alert, I'd only find out from Oleg's tickets in the morning." — line 52.
Quote (Oleg, frequency): "Right, that happened twice in the week after release." — line 53.

### T4 What to try
Idea 1: lock the feature scope no later than day one of the sprint, additional changes as a separate ticket. Proposed by Igor; no explicit reaction of support/disagreement from the group in the moment.
Quote (Igor): "Try from me — lock the feature scope no later than day one of the sprint." — line 55.

Idea 2: pre-launch checklist (incl. support access at least 3 days ahead). Proposed by Dima, supported by Lena (who added the alerts item), taken on by Dima himself.
Quote (Dima): "try number two — set up a pre-launch checklist that always includes support access at least three days ahead." — line 57.
Quote (Dima, ownership): "I'll take it, I already have a draft from the last project, I'll just add three items." — line 61.

Idea 3: automatic Slack alerts for nightly jobs on deploy. Proposed by Lena/Nastya, the group agrees it's important, but nobody takes it on.
Quote (Nastya): "it'd be great if Slack alerts got set up automatically when a new job gets deployed, instead of by hand afterward." — line 59.
Quote (Marina, logging the stalled item): "I hear that everyone agrees it's important, but nobody's picking it up... noting it as an open item with no owner" — lines 68 and 69.

Idea 4: formalize design review with backend at the draft stage by default. Proposed by Lena, supported by Nastya, but Nastya herself immediately caveats that the previous success (T2 fact 2) was more of a workload coincidence than a systemic practice.
Quote (Lena): "I want to propose doing design review with Nastya at the draft stage by default, not just when I happen to remember to come and ask." — line 70.
Quote (Nastya, caveat): "this time it happened by chance, we got lucky that I wasn't loaded up at that moment." — line 71.

### T5 Key decisions and forks
Fork 1: adding a courier notification about address changes to the scope in week two — pushed through by Igor (a legal change), which became the trigger for the deadline slip (T3, episode 1). *(ambiguous: whether the choice was justified in hindsight isn't stated directly in the text; Igor calls it an external requirement, Dima calls it the cause of the deadline slip, who is "right" isn't resolved at the retro itself.)*
Quote (Dima): "when Igor sent over the new scope adding courier notifications about address changes — that wasn't in the original spec" — line 29.
Quote (Igor): "That was a change from legal, I couldn't ignore it." — line 30.

Fork 2: who takes on the pre-launch checklist — Dima volunteered right away, no pushback.
Quote (Dima): "I'll take it, I already have a draft from the last project" — line 61.

Fork 3: who takes on nightly job alerts — Nastya and Dima explicitly declined due to workload, Igor proposed handing it to DevOps, Oleg doesn't know who's responsible — no decision was made, it stalled.
Quote (Nastya): "I could look into it, but I won't have time in the next two weeks, I've got vacation plus another project." — line 64.
Quote (Igor): "Maybe someone from DevOps? We do have a separate infrastructure team, don't we?" — line 66.

### T6 Interpersonal friction
Friction 1 (product manager vs. team lead/designer/backend — openness about deadlines): Dima, Nastya and Lena stayed silent about the deadline slip risk at the dailies in front of Igor, discussing it among themselves "during a coffee break"; Igor only learns about this at the retro and reacts with hurt.
Quote (Nastya, admitting the gap): "it felt awkward to bring it up at the daily in front of everyone... We talked about it separately with Nastya during a coffee break" (Lena) — lines 35–36.
Quote (Igor, reaction): "I don't like that you two discussed it during a coffee break instead of telling me." — line 74.
Quote (Dima, generalizing into a team pattern): "we generally tend to hold back uncomfortable news until the last moment... That happened on the personal account project too." — lines 76, 77.

Friction 2 (product manager vs. team — perception of Igor's own openness): Dima directly calls Igor hard to reach on deadline discussions, Igor disagrees.
Quote (Dima): "it felt like you weren't very open to discussing deadlines, your answer was always "we need to make it, we'll find a way."" — line 41.
Quote (Igor, disagreement): "Well the deadlines really were tight from above, I didn't make that up." — line 42.

### T7 External blockers
Blocker 1: the partner's courier API was down for 4 hours on Wednesday of the second week — blocked integration testing.
Quote (Nastya): "the partner's courier API was down for four hours on Wednesday of the second week, we couldn't test the integration all day." — line 85.

Blocker 2: legal sent changes to the courier geolocation consent 3 days before release — required a rushed redo of a screen.
Quote (Igor): "legal sent changes to the courier geolocation consent literally three days before release, we didn't make that one up either." — line 87.
Quote (Lena, consequence): "I had to redraw one consent screen on the fly, that ate up almost a whole day for me." — line 88.

## Layer 2 — analytical

### A1 Attribution of the failure's cause *(unstable)*
- For T3 episode 1 (deadline slip): COMMUNICATION — the team saw the risk (Nastya, Lena) but didn't voice it to the product manager out loud; partly PROCESS (scope was locked too late relative to sprint length).
  Support: "it felt awkward to bring it up at the daily in front of everyone" (Lena, line 35); "I remember that Tuesday, I had a feeling we weren't going to make it, but I didn't say it out loud at the time" (Nastya, line 31).
- For T3 episode 2 (handoff failure): PROCESS — support wasn't included in the plan in advance.
  Support: "That's my miss, I forgot to include Oleg in the plan early on" (Igor, line 46).
- For T3 episode 3 (silent job): PROCESS/RESOURCES — alerting wasn't set up, no owner assigned even at the retro.
  Support: "the nightly slot recalculation job would sometimes fail silently, no alert" (Nastya, line 52).
*(Flagged unstable: attribution of the first episode depends on whether "held back out of politeness" is treated as a communication failure or a personal choice by each of the three participants — the model may diverge across runs.)*

### A2 Team agreement on the cause
Divergence on episode 1: Igor explains the deadline slip via external pressure ("a change from legal, I couldn't ignore it," line 30; "the deadlines really were tight from above, I didn't make that up," line 42), whereas Dima points to Igor's own closedness to discussion ("you weren't very open to discussing deadlines," line 41), and Nastya and Lena point to their own silence ("I didn't say it out loud at the time," line 31; "it felt awkward to bring it up at the daily," line 35). Three different explanations of the same episode at once — the divergence itself is recorded as a given, not smoothed over.

### A3 Reproducibility of success (T2) *(unstable)*
The timeboxed dailies (T2 fact 1) are a systemic practice, reproducible on any project (a clear rule, not tied to team composition). The early design-API alignment (T2 fact 2) — Nastya herself calls it more of a workload-related stroke of luck than a systemic practice: "this time it happened by chance, we got lucky that I wasn't loaded up at that moment" (line 71). Marina separately flags this discrepancy (line 72): formalizing it is proposed (T4 idea 4), but the success in the past sprint was a one-off, not systemic.

### A4 Unresolved conflict
Friction over openness in discussing deadlines (T6 friction 1) — the team voiced the incident ("I don't like that you two discussed it during a coffee break" — Igor, line 74; "it's not about you personally... a pattern on the team" — Dima, lines 76, 79), but the facilitator explicitly defers resolving it: "I'll note it separately as an unresolved question about openness in discussing deadlines... let's not try to fully resolve it right now" (Marina, lines 80–81). The risk of recurrence on the next project remains open.

### A5 Priority for change
The pre-launch checklist (T4 idea 2) — roll out first: has a concrete owner (Dima), a deadline (before the start of the next sprint), and unanimous group support (Lena immediately adds an item). High effort/impact ratio — reuses Dima's already-existing draft.
Support: "I'll take it, I already have a draft from the last project, I'll just add three items." — line 61.
Contrast: the nightly job alerts idea (T4 idea 3) is supported by everyone as important, but has no owner — not ready for rollout despite a similar potential impact.

### A6 Main insight
The "Express-30" project — the key root cause of the crunch: scope was locked too late relative to sprint length, compounded by part of the team staying silent about the growing deadline risk (attribution — COMMUNICATION, partly PROCESS, *unstable*); the team diverges in its explanation between "external pressure" (Igor) and "closedness to discussion" (Dima, Nastya, Lena, A2); the next step is to roll out the pre-launch checklist (owner assigned) and, separately, outside the retro format, resolve the question of ownership for nightly job alerts and openness in discussing deadlines (both logged as open, without an owner/resolution).
