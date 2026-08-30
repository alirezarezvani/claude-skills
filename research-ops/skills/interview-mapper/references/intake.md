# S0 — Intake "Goal survey" (adaptive, before choosing the lens)

Goal: don't guess, route. The pipeline depends on the GOAL and WHO was interviewed — these two axes
set the lens (how to extract) and the output (what to build). Ask the MINIMUM, then more only as needed.

## Adaptive survey (not a long questionnaire)
**Always (2 questions — in 90% of cases they already determine the lens):**
1. **Goal/decision:** problem discovery · org mapping · experience evaluation · positioning/brand · prioritization-roadmap · usability evaluation · expert validation · personas/segments · exit (reason for leaving) · win/loss (why bought/didn't buy) · project retro · intercept (in-the-moment reaction) · conflict resolution · natural practice (ethnography) · change readiness.
2. **Who was interviewed:** employee · customer/user · expert · visitor · stakeholder · candidate · group (focus group/team — not 1-on-1) · party to a conflict.

**As needed (only if ambiguous or required for synthesis):**
3. **The output:** mapping · insight cards · job map · personas · journey · decision memo · opportunities. (If not stated — use the default by goal.)
4. **How many interviews:** 1 / 2–4 / 5+ (determines whether we can talk about patterns: `k=3`).
5. **Is there a human baseline** to compare against (enables comparison by Δ 1–5).

**Always, when the material is sensitive** (exit, conflict, candidate, medical/HR — treat these as sensitive by default):
6. **Consent and de-identification** — does the respondent's consent cover THIS kind of processing, and must the text be de-identified before S1? Full gate — `references/ethics.md`. De-identify BEFORE `number_lines.py`, or the quotes stop matching the source.

Ask the user these questions (in Cowork — via option selection). Don't start mapping until axis-1 and axis-2 are clear.

## Routing matrix (goal × respondent → lens)
| Goal \ Who | employee | visitor | expert | customer | candidate | group | party to conflict |
|---|---|---|---|---|---|---|---|
| org mapping | org-mapping-vmdi | — | expert | — | — | — | — |
| problem discovery | custdev | custdev | — | custdev | — | — | — |
| "job"/choice (JTBD) | — | — | — | jtbd | — | — | — |
| experience evaluation | — | visitor-experience | — | visitor-experience | — | — | — |
| positioning/brand | brand-positioning | brand-positioning | brand-positioning | brand-positioning | — | — | — |
| expert validation | — | — | expert | — | — | — | — |
| usability evaluation | usability | usability | — | usability | — | — | — |
| exit | exit | — | — | — | — | — | — |
| win/loss | — | — | — | winloss | — | — | — |
| hiring | — | — | — | — | candidate | — | — |
| project retro | — | — | — | — | — | team-retro | — |
| intercept (in the moment) | — | intercept | — | intercept | — | — | — |
| conflict resolution | — | — | — | — | — | — | conflict-mediation |
| natural practice (ethnography) | ethnographic | — | — | ethnographic | — | — | — |
| change readiness | change-readiness | — | — | — | — | — | — |
| (focus group, any goal above) | — | — | — | — | — | focus-group | — |

## Goal → default output
- org mapping → insight cards · experience evaluation → journey · positioning → decision memo ·
  prioritization → opportunities · personas → personas · expert → decision memo ·
  usability → insight cards · exit → insight cards · win/loss → decision memo · retro → insight cards ·
  intercept → insight cards · conflict → decision memo · ethnography → insight cards · change readiness → decision memo.

## Group formats — special case
Respondent = "group" (focus group or team retro) requires a diarized transcript (speakers
labeled) — without it, coding can't proceed; this is an S1 blocker, not something you eyeball around.
The unit of coding there is the turn + speaker + position in the group, not an isolated statement.

## Conflict/mediation — special case
Respondent = "party to a conflict": EACH party is mapped in a SEPARATE file (don't mix them into one
document) — comparing positions/interests only happens at the synthesis stage, checked manually by the mediator.
The interviewer must stay neutral; cell A2 (interest compatibility) is high-stakes and requires
human review before use in negotiations — see `templates/conflict-mediation.md`.

## Check the route with the script
`python scripts/route.py --goal org --respondent employee --output insights --n 6 [--baseline yes]`
→ returns the lens, output, applicable pipeline steps and warnings (including "n<k → watchlist only").

## Principle
Few artifacts, smart routing: `N lenses × M outputs` cover `N×M` tasks. Don't breed duplicate templates —
for a new task, first check whether it's covered by (lens + output), and only then add one.

## Sources
- Portigal, S. — *Interviewing Users: How to Uncover Compelling Insights* (Rosenfeld Media, 2013) — goal-first framing of an interview before method selection.
- Rohrer, C. — *When to Use Which User-Experience Research Method* (Nielsen Norman Group) — method-selection matrix by goal and product stage, the model for the routing table above.
- Beyer, H. & Holtzblatt, K. — *Contextual Design: Defining Customer-Centered Systems* (Morgan Kaufmann, 1998) — respondent-type framing for in-situ/ethnographic interviews.
- Fitzpatrick, R. — *The Mom Test: How to Talk to Customers* (self-published, 2013) — CustDev/problem-discovery framing used for the `custdev` lens.
- Christensen, C. M. & Ulwick, A. — Jobs-to-be-Done theory (*Competing Against Luck*, HarperBusiness, 2016; Ulwick's Outcome-Driven Innovation) — the "job/choice" goal branch routed to `jtbd`.
