# Gold mapping — «Candidate interview (hiring)» lens

**Interview:** transcript.txt
**Role:** Senior Backend Developer (Python), payments team
**Candidate:** current job — Roltech, mid-plus position

## Layer 1 — operational (facts + quote + line)

### K1 — Stated relevant experience
- Fact: 5 years of Python experience, 3 years in fintech, currently mid-plus developer at Roltech.
  Quote: "I've been writing Python for five years, three of those specifically in fintech, right now I work at a company called Roltech as a mid-plus developer" (line 6)
- Fact: names high-load services, message queues, and transactional logic as key experience.
  Quote: "I worked closely with high-load services, message queues, and generally with money, meaning with transactional logic, where a mistake is costly" (line 7)

### K2 — STAR episode(s)
**Episode 1 (strong, verifiable):** payment authorization incident.
- Situation: the authorization service started failing under load during peak hours.
  Quote: "we had a case in March last year, the payment authorization service started failing under load during peak hours" (line 10)
- Action: profiling, fixing the N+1 query, batch fetching, Redis cache.
  Quote: "found that we had an N+1 query to the database on every authorization, rewrote that piece to use batch fetching and added a Redis cache with a thirty-second TTL" (line 12)
- Result: measurable improvement in latency and timeouts.
  Quote: "p99 latency dropped from 1200 milliseconds to 180 milliseconds, and the number of timeouts in production went down to practically zero" (line 13)

**Episode 2 (weakly verifiable):** microservices migration.
- Action described impersonally, through "we", without highlighting a personal contribution.
  Quote: "Well, we all generally worked on it together, I was involved too, I wrote part of the code, I attended the architecture calls" (line 23)
- On a direct question about personal contribution, the candidate avoids specifics.
  Quote: "I'm not ready to say that this particular service is personally mine, we all moved the project forward together" (line 25)
- Result not measured (see also K2/A1 below — line 69).

### K3 — Motivation to move
- Fact: hit a growth ceiling at the current job, no senior position.
  Quote: "I've hit a growth ceiling, there just isn't a senior position there, the headcount is small, the next step up is team lead, and I'm not ready to manage people yet, I want to grow specifically as an engineer" (line 27)
- Fact: wants more autonomy in architectural decisions.
  Quote: "I want more autonomy in architectural decisions, right now a lot gets decided from above, without my input" (line 28)

### K4 — Expectations for the role
- Fact: plan for the first 90 days — get familiar with the system, take on a medium task, lead the performance work by month 3.
  Quote: "by the third month I'd like to already be leading a separate area, for example the performance of the payment service" (line 33)
- Fact: expects to participate in design reviews for new services, not just executing against a ready-made spec.
  Quote: "participating in design reviews for new services, not just writing code against a ready-made spec" (line 35)

### K5 — Reaction to a difficult/failed case
- Fact: a billing release led to double-charging for 5% of customers.
  Quote: "after the release about five percent of customers got double-charged" (line 37)
- Fact: acknowledges his own technical shortcoming — a race condition in the idempotency locking logic.
  Quote: "I didn't account for a race condition on request retries in rare cases, there was a window of a few milliseconds where two requests could pass the idempotency check at the same time, that's my shortcoming in the locking logic" (line 42)
- Fact: at the same time shifts the explanation onto external circumstances — management's deadlines and the infrastructure team's config change.
  Quote: "QA didn't have time to run the full regression because of the tight deadlines management set for us, and on top of that the infrastructure team changed the queue config right before the release, without warning" (line 39)

### K6 — Candidate's questions for us
- Question about the code review process.
  Quote: "how is your code review process set up, how many approvers are needed to merge into master" (line 57)
- Question about balancing feature velocity and tech debt — explicitly flagged by the candidate as personally important.
  Quote: "what's your approach to balancing feature velocity against tech debt, is there dedicated time for refactoring, or does product decide everything" (line 61)

### K7 — Conditions and constraints
- Salary expectations: 350-400 thousand rubles take-home.
  Quote: "I'm expecting a range from three hundred fifty to four hundred thousand rubles take-home" (line 47)
- Start timeline: three weeks after the offer.
  Quote: "realistically three weeks after the offer" (line 49)
- Work format: hybrid, 2-3 days in the office.
  Quote: "I prefer hybrid, two-three days in the office, the rest remote" (line 51)

## Layer 2 — analytical (CAPS conclusion + quote; advisory)

### A1 — Episode verifiability *(unstable)*
- For episode 1 (payment authorization): SPECIFIC FACT — documented by a postmortem in Jira, can be verified via a reference.
  Quote: "it was filed as a separate incident in Jira, there's a postmortem with graphs, I can attach the link if you need it for a reference" (line 17)
- For episode 2 (migration): GENERAL DECLARATION — the candidate himself admits there are no exact numbers.
  Quote: "I can't give exact numbers right now, I'd need to check the dashboard, but subjectively it grew noticeably, probably several times over" (line 69)

### A2 — Result attribution
- In episode 1 — attributed to HIMSELF, scope consistent with a senior level (independently drove diagnosis and implementation).
  Quote: "the main implementation and solution — that's mine, yes" (line 15)
- In episode 2 — attributed to the TEAM, the candidate clearly does not claim ownership of a specific result.
  Quote: "we all moved the project forward together" (line 25)

### A3 — Locus of responsibility for the failure (K5) *(unstable — latent trait)*
MIXED: the candidate acknowledges a specific technical mistake of his own (race condition in locking, line 42), but when summing up shifts the main weight of the cause onto external factors — management's deadlines and someone else's config change.
Quote: "if we'd been given a reasonable testing timeline and the queue config hadn't been touched at the last moment, we would have caught it back on staging" (line 43)
Note: an ambiguous spot — the balance between accepting blame and external attribution isn't resolved unambiguously in the text, requires human judgment (how much of this is a defensive reaction vs. objective analysis).

### A4 — Role fit
Matches the key criterion of the posting ("payments team", high-load transactional backend): direct relevant experience with the payment authorization service failing under load.
Quote: "the payment authorization service started failing under load during peak hours" (line 10)

### A5 — Risks and red flags
- Ambiguity/risk: willingness to relocate is not clearly determined (if relevant for the position).
  Quote: "I can't say a clear yes or no right now, I'd need to understand the details on relocation compensation" (line 53)
- Timing risk: the candidate has a parallel process with an offer in 1.5-2 weeks — a narrow window for an offer on our side.
  Quote: "they said they'd give an offer in about a week and a half to two weeks, so that's a reference point for my timeline too" (line 55)

### A6 — Key insight
The candidate confirms his stated experience with high-load payment services with a strong, verifiable STAR episode (documented in Jira), but the second episode (microservices migration) is weakly verifiable and attribution is diffused onto the team; there is a risk of a mixed locus of responsibility when unpacking the failure (partly accepts blame, partly shifts it onto external circumstances) — a risk that in a critical situation at the new job he will partly explain failures through external factors. Recommendation — next step: request a reference from the current job about the payment authorization episode, and at the technical interview ask for a more specific breakdown of his personal contribution to the microservices migration.
Quote: "the main implementation and solution — that's mine, yes" (line 15)

---
**Limitation (per SKILL.md):** cells A2/A3/A5 are latent/evaluative, candidates for mandatory human review, not a final mapping decision.
