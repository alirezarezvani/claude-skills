# Deflection, automation and root-cause fixes

Confidence: 🟢 primary source, 🟡 established secondary source, 🔴 common practice.

## Three different fixes for three different problems

| Signal in the tickets | What it means | Action |
|---|---|---|
| One answer resolves most tickets, few reopen | the customer could have found it | **DEFLECT**: publish where customers look (help center, in-product, the form itself) |
| A common answer exists but agents adapt it | agents need speed, customers still need a person | **AUTOMATE**: macro, structured form, workflow |
| Many reopen, or the subject names an error | the product is the problem | **FIX_ROOT_CAUSE**: a bug report with the ticket count and hours attached |
| Answers vary | unknown | **REVIEW**: read 20 tickets before deciding |

Writing an article for a defect teaches customers to work around it and hides the cost from the team that could remove it. 🔴

## KCS: capture in the workflow, improve from use

🟢 Knowledge-Centered Service (KCS) has agents capture and reuse knowledge while solving tickets (the Solve Loop), and analyses the collected knowledge and its reuse to improve content and to feed product fixes upstream (the Evolve Loop). [1] The macro column in a ticket export is a cheap proxy for reuse: the share of tickets closed with the same answer is what `deflection_finder.py` calls concentration.

## Claims to make carefully

- Deflection hours are an **upper bound**: they assume every customer who would have written finds and trusts the article. Measure after launch: contact rate for the topic per active customer, before and after. 🔴
- A help-center view is not a deflected ticket. Count only the drop in contacts for that topic. 🔴
- Customers prefer to solve simple problems themselves, and repeat contacts drive disloyalty more than slow first answers. 🟡 [2][3]
- Pareto: in most queues a handful of reasons carry most volume; rank only the head, and only reasons with enough tickets to trust the rates. 🔴 [4]

## Sources

1. Consortium for Service Innovation, *KCS v6 Practices Guide*, library.serviceinnovation.org
2. M. Dixon, K. Freeman, N. Toman, "Stop Trying to Delight Your Customers", Harvard Business Review, July-August 2010
3. M. Dixon, N. Toman, R. DeLisi, *The Effortless Experience*, Portfolio/Penguin, 2013
4. J. M. Juran, *Quality Control Handbook*, McGraw-Hill (Pareto principle as "vital few, trivial many")
5. AXELOS, *ITIL 4 Practice Guide: Problem Management*, 2020
