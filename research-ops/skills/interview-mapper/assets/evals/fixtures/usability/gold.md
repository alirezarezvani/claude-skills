# Gold Mapping — Usability / Think-Aloud Lens

Interview: think-aloud session, Aurora Bank mobile app (previous version).
Participant's task: dispute an unfamiliar $48.00 charge and lower the online purchase limit to $50/month.

## Layer 1 — Operational

### U1 Task and expected path
Fact: the moderator gives the participant a double task — dispute a $48.00 charge and lower the online purchase limit to $50/month.
Quote: "Today's task: you got a notification about a charge of $48.00 at an electronics store that you didn't make. You need to dispute this transaction and also temporarily lower the limit on online purchases for the card to $50 per month"
Line: 1

### U2 First action
Fact: the participant's first action after opening the app is tapping the balance on the main screen, expecting it to open the transaction list.
Quote: "Tapping on the balance."
Line: 6
(Expectation before the action — line 5: "Well, I think there'll be a list of recent transactions, that's usually how banks do it.")

### U3 Snags
Fact (snag 1 — transactions aren't where expected): after tapping the balance, nothing happens; the participant moves to the "Cards" tab, opens a card, but the transaction list isn't immediately visible there.
Quote: "Hm. Nothing happened? Or maybe that was just an animation."
Line: 7

Fact (snag 2 — no "Dispute" button on the transaction card): on the detailed transaction card, the only button is "Repeat Payment," there is no report/dispute button.
Quote: "At the bottom of the card there's only one button — "Repeat Payment." Why would I repeat a payment I never made?"
Line: 18

Fact (snag 3 — the three-dot menu doesn't contain the needed item): the participant tries the extra menu on the transaction card, it doesn't have a dispute function.
Quote: "A menu popped up: "Add to Favorites," "Export Receipt," "Share." Not it again."
Line: 23

Fact (snag 4 — the dispute function is hidden behind a swipe on the list row, not on the card itself): the participant finds the needed element only by accident, after trying a gesture she hadn't tried before.
Quote: "Oh! There it is, it appeared — "Dispute," in red. This is what I need, I didn't think you had to swipe the row specifically, not the card itself."
Line: 38

Fact (snag 5 — limits aren't where expected): the card screen (details, history) has no "Limits" item; the participant looks for it and doesn't find it.
Quote: "Besides the details and history, I don't see anything here that looks like limits. Maybe it's in the card's own settings, not in the general section."
Line: 47

Fact (snag 6 — coarse slider step for the limit): the participant can't precisely set the needed amount of $50 with the slider, the step is too large.
Quote: "For some reason it jumps straight to zero or to $100, I can't get it exactly to $50, the step is too big."
Line: 55

Fact (snag 7 — non-obvious active code input field): the SMS code field has no visual cues (border/placeholder), the participant initially mistakes this for the screen freezing.
Quote: "Entering the code... so, where do I type it, there's just an empty line here with no placeholder, at first I thought this was a bug and the screen had frozen."
Line: 64

### U4 Verbalized model
Fact: the participant expects that opening the card will immediately show the list of recent charges on it (card = entry point into the transaction history).
Quote: "Weird, I thought that if you open the card, it would immediately show the list of recent charges on it."
Line: 11

Fact: the participant expects a separate field for entering the exact limit number next to the slider, as an alternative to dragging.
Quote: "I thought you could type in the exact number by hand, not just drag with your finger. Like in most apps — either a slider, or a text field next to it."
Line: 58

### U5 Errors and recovery
Fact: the participant doesn't immediately notice the "History" item on the card screen (written in small print at the bottom), finds it after scrolling the screen down.
Quote: "Scrolling down... ah, here at the bottom it says "History" in small print. Why isn't this at the top?"
Line: 12

Fact: not finding the dispute option on the transaction card or in its menu, the participant switches to the support chat path, where the offered response speed (24 hours) doesn't fit the urgent task; she eventually goes back to the transaction list and finds the function via a swipe.
Quote: "The bot writes: "Please describe in detail, an agent will respond within 24 hours." Twenty-four hours is a long time, if money was just fraudulently taken from me right now."
Line: 31

### U6 Successful completion
Fact: both parts of the task are completed by the participant independently (without direct hints from the moderator about where elements are located) — the dispute request is submitted and confirmed with a number, the limit is changed and confirmed with an SMS code.
Quote: "A message came in — "Request #558212 accepted, status can be tracked in the Requests section." Great, got that sorted, although it took longer than I expected."
Line: 43
(Second completion — line 67: "It says — "Limit Changed." Good, I guess, but I'm not entirely sure it's exactly $50 and not $52 or something like that, the scale is too coarse to check by eye.")

### U7 Spontaneous reactions
Fact: annoyance over the single irrelevant button on the transaction card ("Repeat Payment"), which doesn't fit the case of a disputed transaction.
Quote: "Overall, honestly, it was a bit annoying that the "Repeat Payment" button on the card is the only one — that's really confusing, it seems like nothing at all is provided here for disputed transactions."
Line: 72

Fact: relief/satisfaction at the moment of finding the needed dispute function via the swipe.
Quote: "Oh! There it is, it appeared — "Dispute," in red. This is what I need"
Line: 38

## Layer 2 — Analytical

### A1 Problem type (per snag in U3)
- Snag 1 (tap on balance with no reaction) → FINDABILITY (wrong entry path into transactions).
- Snag 2 (no "Dispute" button on the card) → FINDABILITY.
- Snag 3 (three-dot menu without the needed item) → FINDABILITY.
- Snag 4 (dispute hidden behind a swipe) → FINDABILITY.
- Snag 5 (limits not on the card screen, but in settings via the gear icon) → FINDABILITY.
- Snag 6 (coarse slider step) → CLARITY (the participant understands what she's doing, but the interface doesn't give her precision) with a TRUST element (see A3).
- Snag 7 (inconspicuous code input field) → CLARITY (mistaken for a system error).
CONCLUSION: the dominant problem type in the session is FINDABILITY (5 out of 7 snags).
Quote (grounded in snag 4): "I didn't think you had to swipe the row specifically, not the card itself"
Line: 38

### A2 Barrier severity *(unstable)*
- Snags 2+3+4 (path to "Dispute") together — SLOWING: the participant ultimately completed the task herself, but it took several wrong attempts (card → menu → support chat → swipe).
  Quote: "Great, got that sorted, although it took longer than I expected."
  Line: 43
- Snag 6 (limit slider step) — AMBIGUOUS between SLOWING and COSMETIC: the task is formally completed and confirmed by the system ("Limit Changed"), but the participant explicitly expresses uncertainty about the accuracy of the final figure, which could mean the task requirement ("exactly $50") wasn't actually met.
  Quote: "I'm not entirely sure it's exactly $50 and not $52 or something like that, the scale is too coarse to check by eye"
  Line: 67
  *(unstable cell — flagged per template requirement; the verdict depends on whether an imprecise match to the target amount counts as a task failure)*

### A3 Expectation-interface gap vs. fact
- Expectation: opening the card will immediately show its transactions (U4, line 11). Fact: the card screen shows details first, history is a separate item further down the scroll (line 12).
- Expectation: there will be a field next to the limit slider for entering an exact number (U4, line 58). Fact: the interface only has a draggable slider with a large step, there is no input field (lines 54-55, 59).
Quote: "I thought you could type in the exact number by hand, not just drag with your finger. Like in most apps — either a slider, or a text field next to it."
Line: 58

### A4 Isolated case vs. systemic problem *(unstable — requires data from ≥3 sessions)*
Based on a single session, this cannot be reliably distinguished: it's hard to say whether the path "card → menu → chat → swipe" for the "Dispute" function is an architectural interface problem (no direct route to the action where the user looks for it) or a coincidence of this particular participant's individual habits (the participant herself shifts part of the blame onto herself rather than the interface — see quote below). Requires ≥3 sessions for triangulation.
Quote: "I'm just not used to swiping list rows at all, I usually tap directly on the entry itself"
Line: 70
*(unstable — single observation, systemic-problem status not confirmed)*

### A5 Fix priority
Highest priority — the path to the "Dispute" function: it affects task completion (the user nearly gave up and used the support path with a 24-hour SLA, which is unacceptable for a fraudulent transaction) and recurs across 3 consecutive points (card → menu → chat) before an accidental success via swipe. Second priority — the accuracy of the limit slider, since it's tied to uncertainty in the outcome (the exact amount isn't confirmed).
Quote: "Twenty-four hours is a long time, if money was just fraudulently taken from me right now."
Line: 31

### A6 Key insight
At the step of searching for the dispute function, the participant hit a PATH-BLOCKING (but not outcome-blocking) FINDABILITY barrier, because the "Dispute" action is only available via a non-standard gesture (swiping the list row) and is absent from the transaction card itself, where the user logically expects it and where the only offered button leads to the irrelevant "Repeat Payment" action; severity — SLOWING (the task was completed, but at the cost of several false paths and a detour to a slow support channel).
Quote: "I didn't think you had to swipe the row specifically, not the card itself"
Line: 38
