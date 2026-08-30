# Gold Mapping — CustDev Interview (Fixture)

**Interview:** operations director and co-owner of a coffee shop chain (4 locations), topic — tracking write-offs and raw material shortages.
**Transcript:** `transcript.txt` (74 lines, physical numbering, 1-based).
**Eval record prompt:** "Analyze this custdev interview with a customer — what is their problem, what have they already tried, is the pain real. Don't make things up."

---

## Layer 1 — operational (facts + quote + line)

### C1 — Problem/task
**Fact:** every week the respondent manually reconciles raw material balances across four locations from paper write-off forms that managers photograph and send via WhatsApp; the numbers don't actually add up and the cause is unclear.
**Quote:** "Every Monday I sit down and reconcile the raw material balances across all four locations." (line 7)
**Additional quote (data source — paper+photo, not a system):** "The managers at each location send me photos of the paper write-off forms in WhatsApp." (line 9)

### C2 — Real episodes
**Fact:** a specific episode — yesterday's reconciliation took 2 hours 40 minutes; the day before yesterday at the Lenina Street location the milk was off by almost a liter for the shift, the respondent called the manager and got a shrug instead of an explanation.
**Quote:** "Yesterday specifically it was two hours and forty minutes, I timed it, because it was driving me absolutely crazy." (line 12)
**Additional quote (the milk episode):** "The day before yesterday that's exactly what happened, at the location on Lenina Street the milk was off by almost a liter for the shift." (line 16)
**Additional quote (manager's reaction):** "I called the manager, she says, maybe the barista spilled it, maybe she didn't log it, basically she just shrugged." (line 17)

### C3 — Current solution / workaround
**Fact:** the main workaround right now is manual reconciliation in Excel plus a parallel paper logbook at the location, photographed once a week and kept in a separate folder on the phone "just in case"; the paper is cross-checked against the spreadsheet by eye.
**Quote:** "The managers keep a paper logbook at the location, I photograph it once a week and keep copies in a separate folder on my phone, just in case, if the accountant asks." (line 42)
**Additional quote (manual cross-check):** "I cross-check it manually, by eye, on that same Monday morning." (line 44)

### C4 — Cost of the problem
**Fact:** reconciliation eats up 3-4 hours a week not counting calls; for May, about 41,000 rubles in unexplained discrepancies were documented in a spreadsheet the respondent kept herself; the amount is compared to a location's rent for a week and a half.
**Quote:** "Well usually it's about three to four hours a week just on reconciling, that's not counting the calls to managers when the numbers don't add up." (line 14)
**Additional quote (discrepancy amount):** "For May it came out to about forty-one thousand rubles in unexplained discrepancies across all locations, I showed that number to the accountant, she was horrified herself." (line 23)
**Additional quote (scale of the amount):** "That's roughly like the rent for one location for a week and a half, so yes, it's noticeable." (line 25)

### C5 — Who else is involved
**Fact:** involved are all four location managers (complain that the forms are inconvenient), the accountant (complains about delayed numbers), and the second co-owner-partner (asks about discrepancies but doesn't participate in solving them, focused on marketing).
**Quote:** "All four managers complain that filling out the forms is inconvenient, especially in a rush, when there's a line." (line 46)
**Additional quote (accountant):** "The accountant complains that the numbers come from me late, because I don't manage to reconcile them in time myself." (line 47)
**Additional quote (partner doesn't participate in the solution):** "Mostly he just asks, the solution is all on me, he's more focused on marketing." (line 50)

### C6 — What has already been tried and abandoned
**Fact:** two paid attempts. (1) January — hired a programmer they know for 15,000 rubles, who built a Google spreadsheet with formulas; it worked for about two weeks, then managers got confused entering data, formulas broke, the spreadsheet was abandoned by March. (2) April — an inventory management app (~"Cleverence", not exact), paid a month's subscription (~2000 rubles); required manually entering ~130 item names, after two evenings (~5 hours) got through less than half, subscription not renewed, money wasted.
**Quote (attempt 1, hiring a programmer):** "The first — in January I hired a programmer I know, he built me a Google spreadsheet with formulas and automatic discrepancy calculation for fifteen thousand rubles." (line 28)
**Additional quote (attempt 1, why abandoned):** "Then the managers started getting confused about which cell to enter what in, the formulas would break if you typed text instead of a number." (line 31)
**Additional quote (attempt 1, final outcome):** "By March I just stopped checking it, junk had piled up in there anyway." (line 32)
**Additional quote (attempt 2, the app):** "The second approach — in April I downloaded an inventory management app, I think it was called something like Cleverence, I don't remember exactly." (line 34)
**Additional quote (attempt 2, payment):** "I paid something like two thousand rubles there for a month's subscription." (line 35)
**Additional quote (attempt 2, why abandoned):** "Then I just gave up on it, didn't renew the subscription, the money was wasted." (line 39)

---

## Layer 2 — analytical (conclusion in CAPS + supporting quote)

### A1 — Fact vs. opinion *(unstable)*
**Conclusion:** CONFIRMED BY BEHAVIOR — real money was spent (15,000 rubles on a programmer, ~2000 rubles on a subscription) and real time (2h40m on one reconciliation, 3-4h/week, 5 hours on an attempt to enter the item list). A DECLARATION WITHOUT BEHAVIORAL CONFIRMATION — the phrase "I would definitely buy it" in response to the interviewer's hypothetical question about a nonexistent service; the respondent immediately softens her willingness to pay ("I don't know exactly, I'd have to think it through") and refuses to prepay sight unseen.
**Quote (behavioral fact):** "The first — in January I hired a programmer I know, he built me a Google spreadsheet with formulas and automatic discrepancy calculation for fifteen thousand rubles." (line 28)
**Supporting quote (opinion/declaration, weak signal):** "Listen, that's exactly what I need, I would definitely buy it, honestly, without a second thought." (line 56)
**⚑ Why unstable:** the line between "declaration" and "readiness signal" is thin here — the phrase itself sounds like a commitment, but it's an answer to the interviewer's direct leading question ("would you use it?"), a classic forcing question that The Mom Test warns against; an independent run is needed so as not to overweight the phrase.

### A2 — Strength of pain *(unstable)*
**Conclusion:** NAGGING, WITH SIGNS OF TURNING INTO BURNING — the respondent has already paid twice (in money and in time) trying to solve the problem, which clearly sets the pain apart from "imaginary," but both attempts were abandoned, and the most recent documented damage figure (41,000 rubles for May) covers only one month, while the March-April estimates the respondent herself calls a guess "from memory," not from the spreadsheet.
**Quote (sign of burning — already paid twice):** "I paid something like two thousand rubles there for a month's subscription." (line 35)
**Supporting quote (limitation of the conclusion — part of the amount is undocumented):** "Yes, May I actually calculated from the spreadsheet, but March-April is me estimating from memory right now, I could be off in either direction." (line 65)
**⚑ Why unstable:** the pain-strength conclusion rests on the 41,000-ruble/month figure, but the respondent herself distinguishes the reliability of the May figure (documented) from March-April (a rough eyeball estimate) — on a repeat run a different calibration between NAGGING and BURNING is possible depending on the weight given to the undocumented months.

### A3 — Readiness signals
**Conclusion:** THERE ARE REAL COMMITMENT SIGNALS — the respondent searched for a solution on her own at least three times (hiring a programmer, a paid app subscription, asking in a topical Telegram chat followed by reviewing competitors' websites), spending money on two of them. There is NO upfront-prepayment signal — asked directly about prepaying an annual subscription without a trial, she declined.
**Quote (asking in the chat + reviewing alternatives):** "In one chat for restaurant owners on Telegram I asked for advice, they threw me about five service names." (line 53)
**Supporting quote (refusal to prepay — limits the strength of the signal):** "Well to prepay sight unseen right now — probably not, I'd try it for a month first, see if it sticks with the managers." (line 60)

### A4 — Hypothesis: confirmed/disproved
**Conclusion:** THE HYPOTHESIS "MANUAL WRITE-OFF TRACKING IN A SMALL COFFEE SHOP CHAIN CAUSES MEASURABLE LOSSES AND HAS ALREADY LED TO ATTEMPTS TO BUY/HIRE A SOLUTION" — CONFIRMED by facts about money, time, and two abandoned attempts. The hypothesis "the respondent is ready to buy a standard off-the-shelf solution at market price" — NOT confirmed: the only market option found, priced "starting from fifteen thousand a month," was rejected as too expensive for four locations.
**Quote (rejection based on price — disproves part of the hypothesis):** "I looked at two of them on their websites, one had pricing starting from fifteen thousand a month, I closed the tab right away, that's expensive for us with four locations." (line 54)

### A5 — Risk of a false positive
**Conclusion:** THE CLOSING REMARK ABOUT THE CONVERSATION'S USEFULNESS — POLITENESS WITHOUT BEHAVIORAL BACKING, re-check it through direct observation/follow-up contact, don't take it at face value. There's a similar risk with the phrase "I would definitely buy it" (A1) — an answer to a leading hypothetical question, not to a forcing question about past behavior.
**Quote:** "Yes, very interesting, you really hit the nail on the head with your questions, I enjoyed it a lot." (line 72)

### A6 — Key insight
**Conclusion:** THE PROBLEM [MANUAL WRITE-OFF TRACKING AND UNEXPLAINED RAW MATERIAL DISCREPANCIES ACROSS 4 LOCATIONS] IS REAL, BECAUSE [the respondent has already spent ~17,000 rubles and dozens of hours on two independent attempts at a solution, and the documented damage for May was 41,000 rubles], SO the next step is not to pitch a ready-made product, but to check whether the respondent is willing to pay a market price (her threshold is clearly lower than the previously rejected "starting from 15,000 rubles/month"), and to confirm with the managers whether the item-entry problem that has already killed two previous attempts is reproducible.
**Quote:** "The second approach — in April I downloaded an inventory management app, I think it was called something like Cleverence, I don't remember exactly." (line 34)

---

## Intentionally ambiguous spots (to test unstable cells)

1. **Line 56** ("I would definitely buy it, honestly, without a second thought"): sounds like a strong readiness signal, but was said in response to the interviewer's clearly hypothetical, leading question ("what if a service... appeared, would you use it?") — a violation of Mom Test forcing rules. Affects A1 and A3: some runs may mistakenly code this phrase as a "readiness signal," even though methodologically it's a declaration that requires skepticism.
2. **Lines 61–65** (damage figures for March-April): the respondent herself moves from a documented figure (May, 41,000 rubles, from the spreadsheet) to an undocumented "rough" estimate for the preceding months and explicitly says "I could be off in either direction" — affects A2 (strength of pain): whether to include the March-April estimate in the overall conclusion about the problem's chronic nature, or limit the analysis to May as the only verifiable figure.
