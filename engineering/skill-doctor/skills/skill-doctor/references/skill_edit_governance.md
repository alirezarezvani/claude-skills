# Skill edit governance — the filing bar for proposing changes to another agent's instructions

The core method and filing bar below are preserved from upstream skill-doctor's
`references/skill-improvements.md` (MIT, © Denver Technologies, Inc.), because
they encode the single most important discipline in this skill: **a speculative
change is worse than none.** The surrounding rationale and the repo integration
are additions.

## 1. Method (upstream, preserved)

1. Cluster the findings by root cause, across scorers and classifications, after attribution.
2. Prioritize clusters by frequency times severity.
3. Verify each finding against the current repository and the agent's configuration
   before proposing any improvements. Drop what does not verify.
4. You are editing another agent's instructions. Keep those edits small and general.
   Before editing, state the intended behavioral rule and owning surface in one
   sentence, then make the smallest change that expresses it.
5. Prefer **replacing** existing guidance over **appending** another paragraph.

## 2. When to propose changes (upstream, preserved)

Do not propose changes by default. Proceed only when a concrete instruction is
missing or wrong and amending it would have prevented the scored failure. Ask:
**would a competent agent with the current instructions still be expected to fail
this way?** If yes, there is a gap. If no, defer.

File only when all of these are true:

- The failure is caused by a missing, wrong, or underspecified instruction on a
  concrete surface: the owning actor's configuration, a skill, or in-repo guidance.
- You can name that owning surface and the one reusable rule it should have stated.
- If that rule had been present and followed, the scored failure would not have happened.
- The same gap appears in more than one source run, or is severe enough that a
  single occurrence still proves a missing contract.

Do not file when:

- The existing instruction already required the correct behavior and the model ignored it.
- The failure is model variance: same prompt, same tools, different choice.
- The only available edit is restating, hedging, or adding examples from these runs.
- The real fix is product, infra, scorer, or code outside instruction surfaces.

When nothing clears this bar, open no change and say, per finding, why not — that
is a success.

## 3. Why the bar is this high

- **Error analysis before fixes.** Husain's eval methodology (source 3): look at
  the actual failures and categorize them before changing anything; fixes filed
  from vibes recur because they never touched the failing category. Steps 1–3 of
  the method are exactly this, applied to instruction surfaces.
- **Instructions accrete; nobody prunes.** Appending a paragraph per incident
  produces prompts that contradict themselves — the instruction-surface version
  of the small-change discipline in Google's code-review practice (source 4):
  small, single-purpose changes reviewers can actually verify.
- **Validated adoption beats live editing.** SkillOpt's sleep cycle only promotes
  consolidated edits that pass a held-out validation gate, and stages rather than
  applies them (source 5). skill-doctor mirrors the staging half: proposed
  SKILL.md files live under `$RUN/proposed/`, are shown as diffs, and touch real
  files only on an explicit per-skill yes.
- **A never-firing skill is usually a description problem.** Anthropic's skill
  authoring guidance: the description is the trigger surface — it decides whether
  the skill loads at all (source 6). An installed skill with zero detections in
  the window earns a trigger-description suggestion before any body edit.

## 4. Repo integration (addition)

A proposed edit to a skill in *this* repository must also survive the house
checklist — trigger phrase in the description, SKILL.md ≤ 100 lines, concrete
example, references one level deep. Run it before presenting the diff:

```bash
python engineering/write-a-skill/skills/write-a-skill/scripts/skill_review_checklist_runner.py "$RUN/proposed/<skill>/"
```

A suggestion whose proposed file fails the checklist is not ready to file
(source 7). For repos without the checklist, the six items still work as a manual
review list.

## 5. Traceability (enforced mechanically)

`score_aggregator.py` refuses any suggestion that does not cite at least one
sampled session id. This turns "suggestions must trace back to observed waste or
defects, not generic best practices" from a request into a gate — the same
evidence-before-done posture as this repo's delivery-loop gate (source 2), and
the reason the report can print every suggestion next to the session that
motivated it (source 1).

## Sources

1. warpdotdev/common-skills — `skill-doctor/references/skill-improvements.md` at commit `f3b58c81` (MIT): the preserved method and filing bar.
2. This repo — `project-management/` `delivery_loop_gate.py` (G4: evidence-before-done) and `engineering/agent-harness/` close-out discipline: machine-checked gates over self-reported completion.
3. Husain, H. (2024). *Your AI Product Needs Evals.* hamel.dev/blog/posts/evals — error analysis and failure categorization before fixes.
4. Google Engineering Practices — *Small CLs.* google.github.io/eng-practices/review/developer/small-cls.html — small single-purpose changes are the reviewable unit.
5. microsoft/SkillOpt — `skillopt_sleep`: consolidation behind a held-out validation gate; staged, never live, until explicit adoption (vendored at `engineering/skillopt-sleep/`).
6. Anthropic — *Agent Skills* documentation (code.claude.com/docs/en/skills): the description field is the trigger surface; authoring guidance for when skills load.
7. Matt Pocock — write-a-skill review checklist (preserved in this repo at `engineering/write-a-skill/`): the six binding checks for post-v2.6.0 skills.
