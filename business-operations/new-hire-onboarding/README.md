# new-hire-onboarding

Get a new hire's first day and first 90 days right: everything ready before
the start date, a 30/60/90 plan whose milestones someone can actually check,
and an early warning when the onboarding drifts. Three stdlib Python scripts
over one JSON file per hire; no HRIS API, no credentials.

| Script | Answers |
|---|---|
| `preboarding_gate.py` | Can this person work on day one? Which task is late, who owns it, when is the I-9 or right-to-work deadline? |
| `plan_builder.py` | What is the 30/60/90 plan, with checkpoints and buddy meetings in the calendar? Which milestones are too vague to check? |
| `ramp_check.py` | Is the onboarding on track: checkpoints held, milestones done, buddy still meeting? |

```bash
/plugin install new-hire-onboarding@claude-code-skills
/cs-preboarding-check hire.json
/cs-onboarding-plan plan.json
/cs-ramp-check ramp.json
```

A skill-router hook adds one line pointing at this skill when a prompt is
clearly about a new hire's start (it never blocks, fails open, and is off with
`SKILL_ROUTER=0` or `SKILL_ROUTER_NEW_HIRE_ONBOARDING=0`).

The ramp check judges the onboarding, never the person: probation and
performance decisions stay with the manager and HR. For how many people to
hire, use `capacity-planner`; to write the onboarding SOP itself, use
`knowledge-ops` (both in business-operations-skills).

Agent: `cs-onboarding-lead`. References cite USCIS, GOV.UK, the Nachweisgesetz,
Bauer (2010), Bauer et al. (2007), Watkins (2003), Gallup (2021) and Microsoft's
onboarding buddy pilot. License: MIT.
