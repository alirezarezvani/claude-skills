# Staffing with Erlang C

Confidence: 🟢 primary source, 🟡 established secondary source, 🔴 common practice.

## The model

🟢 Erlang C (M/M/N) gives the probability an arrival has to wait when contacts arrive at random at rate λ, N agents each handle one at a time, and handle times average AHT. Offered load A = λ · AHT (in erlangs). [1][2]

```
P(wait)  = ErlangC(N, A)
SL(t)    = 1 - P(wait) · exp(-(N - A) · t / AHT)        share answered within t
ASA      = P(wait) · AHT / (N - A)                         average speed of answer
occupancy = A / N
```

The script computes ErlangC through the Erlang B recursion, which is numerically stable for large N. Check: A = 2, N = 3 gives P(wait) = 4/9.

## What the formula leaves out, and what the script does about it

| Gap | Effect | Script |
|---|---|---|
| Abandonment | real queues lose impatient callers, so Erlang C over-staffs a little; Erlang A models it [2] | ignored (errs toward enough staff) |
| Shrinkage | breaks, training, meetings, absence | `--shrinkage` grosses on-line agents up to scheduled agents |
| Burnout at high occupancy | Erlang C happily plans 95% occupancy at high volume | `--max-occupancy` caps it (default 85%, 🔴) |
| Chat concurrency | one agent, several chats | `--concurrency` divides AHT; an approximation, since each chat slows when stacked 🔴 |
| Email and forms | no one abandons after 60 s; the goal is a backlog that clears | `--mode async`: workload hours plus backlog drain |
| Peaks inside the hour | a 15-minute spike can miss SL in an hour that meets it on average | use 15- or 30-minute intervals in the CSV when you have them |

## Defaults to state

80% in 60 s (live) is a common convention, not a standard (🔴); 30% shrinkage is a planning starting point to replace with measured shrinkage. Square-root staffing (N ≈ A + β√A) explains why large teams reach the same service level at higher occupancy than small ones: pooling queues is the cheapest capacity there is. 🟢 [2][3]

## Sources

1. A. K. Erlang, "Solution of some problems in the theory of probabilities of significance in automatic telephone exchanges", Elektroteknikeren 13, 1917
2. N. Gans, G. Koole, A. Mandelbaum, "Telephone Call Centers: Tutorial, Review, and Research Prospects", Manufacturing & Service Operations Management 5(2):79-141, 2003
3. S. Halfin, W. Whitt, "Heavy-Traffic Limits for Queues with Many Exponential Servers", Operations Research 29(3):567-588, 1981
4. G. Koole, *Call Center Optimization*, MG Books, 2013
5. J. D. C. Little, "A Proof for the Queuing Formula: L = λW", Operations Research 9(3):383-387, 1961
