# Recorded vs inferred: why the agent's memory is not evidence

## The failure this prevents

Ask an agent why it did something a while ago and it answers fluently. The answer
is a reconstruction: built from what is still in context, shaped by how the work
turned out, and missing the tool results it never re-read. Three findings explain
why that reconstruction cannot be trusted as a record:

- **Stated reasons are often not the real ones.** Chain-of-thought explanations
  can omit the factor that actually drove the answer (Turpin et al. 2023; Lanham
  et al. 2023), and reasoning models mention a hint they used only a minority of
  the time (Chen et al. 2025). An agent's account of its own steps is the same kind
  of self-report.
- **People do this too.** Subjects confidently report causes for their behaviour
  that the experiment shows were not the causes (Nisbett & Wilson 1977). Knowing
  the outcome changes what seemed likely beforehand (Fischhoff 1975).
- **Order is not cause.** That step 7 came before step 9 is recorded; that step 7
  caused step 9 is not (Lamport 1978, happened-before is not causation).

So the agent's words at the time are recorded **as a claim** (`stated-reason`),
and never promoted to "the cause".

## The two labels

| Label | Rule of thumb | Allowed phrasing |
|---|---|---|
| `recorded` | The harness wrote it at the time | "Step 9 ran `sed -i ... config.yaml` and exited 0." |
| `inferred` | Derived now, by a named rule, from recorded facts | "Step 9 probably reacted to the failure at step 7 (rule: retry-after-failure)." |

An answer may contain both, in that order, and must not blend them: "I changed the
timeout because the test failed" turns an inference into a fact.

## The inference rules

| Rule | Fires when | Strength |
|---|---|---|
| `prior-write` | An earlier step wrote the same file | Strong: it names exactly which version was replaced |
| `read-before-write` | An earlier step read the same file | Strong for "what it had seen"; that step's result holds it |
| `no-read-before-write` | The file was changed with no earlier read in the run | Strong as an absence, within this run only |
| `retry-after-failure` | One of the 3 previous tool calls failed and was not later re-run successfully | Medium: proximity, not proof |
| `target-seen-in-output` | The file's name appeared in an earlier tool's output | Weak: a lead to read, nothing more |
| `shell-*`, `git-*` | A command's text implies a file effect (`sed -i`, `>`, `rm`, `git checkout --`) | Medium: intent, not observed effect |

Upgrade an inference by reading the step it points to; never by restating it louder.

## Postmortem practice that carries over

Blameless postmortems build the timeline from logs before anyone explains it
(Google SRE Book, ch. 15), and ask "how" more than "why", because a single root
cause is usually a story told afterwards (Allspaw 2014). The same order works for
an agent run: timeline first, then the step in question, then the edges.

## Sources

1. Turpin, Michael, Perez, Bowman. "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting." NeurIPS 2023. arXiv:2305.04388 🟢
2. Lanham et al. "Measuring Faithfulness in Chain-of-Thought Reasoning." Anthropic, 2023. arXiv:2307.13702 🟢
3. Chen et al. "Reasoning Models Don't Always Say What They Think." Anthropic, 2025. arXiv:2505.05410 🟢
4. Nisbett, Wilson. "Telling More Than We Can Know: Verbal Reports on Mental Processes." Psychological Review 84(3), 1977 🟢
5. Fischhoff. "Hindsight ≠ Foresight: The Effect of Outcome Knowledge on Judgment Under Uncertainty." J. Exp. Psychology: Human Perception and Performance 1(3), 1975 🟢
6. Lamport. "Time, Clocks, and the Ordering of Events in a Distributed System." CACM 21(7), 1978 🟢
7. Beyer et al. *Site Reliability Engineering*, ch. 15 "Postmortem Culture: Learning from Failure." O'Reilly, 2016 🟢
8. Allspaw. "The Infinite Hows (or, the Dangers of the Five Whys)." 2014 🟢
